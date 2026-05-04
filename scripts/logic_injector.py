import os
import yaml
import glob
import re

def sanitize(s):
    return s.lower().replace(" ", "_").replace("-", "_")

def logic_injection_tool():
    topic_path = "/data/sci-logic-kb/topics/ultrastable-laser"
    files = glob.glob(os.path.join(topic_path, "papers/*.yaml"))

    # 1. Load all data
    all_papers = {}
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                if data:
                    all_papers[f] = data
            except Exception as e:
                print(f"Error loading {f}: {e}")

    # 2. Build Global Maps
    all_nodes = {}
    all_relations = []

    for f, data in all_papers.items():
        # Map nodes
        for section in ['entities', 'principles', 'methods', 'metrics']:
            if section in data and data[section]:
                for node in data[section]:
                    nid = node.get('id') or node.get('name')
                    if nid:
                        all_nodes[nid] = {'type': section.rstrip('s'), 'file': f, 'data': node}

        # Collect relations
        if 'relations' in data and data['relations']:
            for rel in data['relations']:
                rel['file'] = f
                all_relations.append(rel)

    # 3. Find "Logic Gaps" using breakthrough_paths
    # We look for: Entity -> BOUNDED-BY -> Principle.
    # Then we check the breakthrough_paths of that relation.

    new_relations_to_add = [] # (file, relation_obj)

    for rel in all_relations:
        if rel.get('predicate') == 'BOUNDED-BY':
            target_principle = rel.get('object')
            paths = rel.get('breakthrough_paths', [])
            if not paths: continue

            for path in paths:
                direction_pri = path.get('direction')
                if not direction_pri: continue

                # We now look for a METHOD that resolves this direction_pri
                # Logic: a method that is BASED_ON or IMPLEMENTS this principle
                possible_methods = [
                    nid for nid, n in all_nodes.items()
                    if n['type'] == 'method' and
                    any(r['object'] == direction_pri and r['predicate'] in ['BASED_ON', 'IMPLEMENTS']
                       for r in all_relations if r['subject'] == nid)
                ]

                for meth in possible_methods:
                    # Create RESOLVED-BY relation: Principle -> Method
                    # We add this to the file where the principle is defined or the path is defined
                    new_rel = {
                        'id': f"rel.logic_bridge_{meth.split('.')[-1]}_{direction_pri.split('.')[-1]}",
                        'subject': direction_pri,
                        'predicate': 'RESOLVED-BY',
                        'object': meth,
                        'confidence': 'inferred',
                        'source': {'note': 'Auto-injected via Logic Tool based on breakthrough_paths'}
                    }
                    new_relations_to_add.append((rel['file'], new_rel))

                    # Also try to find a metric that this method produces
                    # Logic: Method -> PRODUCES -> Metric
                    # Since we might not have 'PRODUCES' yet, we look for metrics characterized by the entity
                    # that the principle was bounding.
                    subject_ent = rel.get('subject')
                    if subject_ent:
                        metrics = [
                            r['object'] for r in all_relations
                            if r['subject'] == subject_ent and r['predicate'] == 'CHARACTERIZED-BY'
                        ]
                        for met in metrics:
                            new_rel_prod = {
                                'id': f"rel.logic_prod_{meth.split('.')[-1]}_{met.split('.')[-1]}",
                                'subject': meth,
                                'predicate': 'PRODUCES',
                                'object': met,
                                'confidence': 'inferred',
                                'source': {'note': 'Auto-injected via Logic Tool as the result of the resolution'}
                            }
                            new_relations_to_add.append((rel['file'], new_rel_prod))

    # 4. Apply Injections (Deduplicating)
    for file_path, new_rel in new_relations_to_add:
        data = all_papers[file_path]
        if 'relations' not in data:
            data['relations'] = []

        # Check for duplicates
        if any(r.get('id') == new_rel['id'] for r in data['relations']):
            continue

        data['relations'].append(new_rel)

    # 5. Write back to files
    for file_path, data in all_papers.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    print(f"Injected {len(new_relations_to_add)} logical relations across the topic.")

if __name__ == "__main__":
    logic_injection_tool()
