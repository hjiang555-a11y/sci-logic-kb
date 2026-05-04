import os
import yaml
import glob
from collections import defaultdict

def load_yaml_files(topic_path):
    files = glob.glob(os.path.join(topic_path, "papers/*.yaml"))
    all_data = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                if data:
                    all_data.append(data)
            except Exception as e:
                print(f"Error loading {f}: {e}")
    return all_data

def extract_nodes(all_data):
    nodes = {}
    for data in all_data:
        for section in ['entities', 'principles', 'methods', 'metrics']:
            if section in data and data[section]:
                for node in data[section]:
                    # Handle different schema versions (id vs name)
                    node_id = node.get('id') or node.get('name')
                    if node_id:
                        nodes[node_id] = {
                            'type': section.rstrip('s'),
                            'name': node.get('name', node_id),
                            'data': node
                        }
    return nodes

def extract_relations(all_data):
    relations = []
    for data in all_data:
        if 'relations' in data and data['relations']:
            for rel in data['relations']:
                relations.append({
                    'id': rel.get('id'),
                    'subject': rel.get('subject'),
                    'predicate': rel.get('predicate'),
                    'object': rel.get('object'),
                    'conditions': rel.get('conditions', 'N/A')
                })
    return relations

def find_chains(nodes, relations):
    # Goal: Metric -> Bounded-By -> Principle -> Resolved-By -> Method -> Produces -> Metric
    chains = []

    # 1. Find all metrics
    metrics = [nid for nid, n in nodes.items() if n['type'] == 'metric']

    for met in metrics:
        # Find entities characterized by this metric
        entities = [r['subject'] for r in relations if r['object'] == met and r['predicate'] == 'CHARACTERIZED-BY']

        for ent in entities:
            # Find principles that bound this entity
            principles = [r['object'] for r in relations if r['subject'] == ent and r['predicate'] == 'BOUNDED-BY']

            for pri in principles:
                # Find methods that resolve this principle
                methods = [r['object'] for r in relations if r['subject'] == pri and r['predicate'] == 'RESOLVED-BY']

                for meth in methods:
                    # Find new metrics produced by this method
                    new_metrics = [r['object'] for r in relations if r['subject'] == meth and r['predicate'] == 'PRODUCES']

                    for new_met in new_metrics:
                        chains.append({
                            'start_metric': met,
                            'entity': ent,
                            'bounding_principle': pri,
                            'resolution_method': meth,
                            'end_metric': new_met
                        })
    return chains

def generate_report(topic_name, chains, nodes):
    report = f"# Metric Chain Analysis: {topic_name}\n\n"
    report += "This report automatically extracts technical reasoning chains from the knowledge base.\n"
    report += "Logic: Metric $\\rightarrow$ Entity $\\rightarrow$ Bounding Principle $\\rightarrow$ Resolution Method $\\rightarrow$ Improved Metric\n\n"

    if not chains:
        report += "No complete metric chains found. This may indicate gaps in the 'Resolved-By' or 'Produces' relations.\n"
    else:
        for i, chain in enumerate(chains, 1):
            report += f"## Chain {i}\n"
            report += f"- **Start Metric**: {nodes[chain['start_metric']]['name']} ({chain['start_metric']})\n"
            report += f"- **Entity**: {nodes[chain['entity']]['name']} ({chain['entity']})\n"
            report += f"- **Bounding Principle**: {nodes[chain['bounding_principle']]['name']} ({chain['bounding_principle']})\n"
            report += f"- **Resolution Method**: {nodes[chain['resolution_method']]['name']} ({chain['resolution_method']})\n"
            report += f"- **Improved Metric**: {nodes[chain['end_metric']]['name']} ({chain['end_metric']})\n"
            report += "\n---\n\n"

    return report

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_metric_chains.py <topic_name>")
        sys.exit(1)

    topic_name = sys.argv[1]
    topic_path = f"/data/sci-logic-kb/topics/{topic_name}"

    if not os.path.exists(topic_path):
        print(f"Topic path {topic_path} does not exist.")
        sys.exit(1)

    data = load_yaml_files(topic_path)
    nodes = extract_nodes(data)
    relations = extract_relations(data)
    chains = find_chains(nodes, relations)

    report = generate_report(topic_name, chains, nodes)

    output_file = f"/data/sci-logic-kb/reports/metric_chains_{topic_name}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Report generated: {output_file}")
