import os
import yaml
import glob

def prune_dangling_refs():
    topic_path = "/data/sci-logic-kb/topics"
    files = glob.glob(os.path.join(topic_path, "**/*.yaml"), recursive=True)

    # 1. Load all existing nodes across the entire KB
    all_nodes = set()
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                if not data: continue
                for section in ['entities', 'principles', 'methods', 'metrics']:
                    if section in data and data[section]:
                        for node in data[section]:
                            nid = node.get('id') or node.get('name')
                            if nid: all_nodes.add(nid)
            except: continue

    print(f"Indexed {len(all_nodes)} unique nodes across the KB.")

    # 2. Prune relations that point to non-existent nodes
    pruned_count = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
            except: continue

        if not data or 'relations' not in data or not data['relations']:
            continue

        original_rels = data['relations']
        valid_rels = []

        for rel in original_rels:
            # Check both subject and object
            subj = rel.get('subject')
            obj = rel.get('object')

            if subj in all_nodes and obj in all_nodes:
                valid_rels.append(rel)
            else:
                pruned_count += 1
                # Log which relation was pruned for transparency
                # print(f"Pruning {rel.get('id')} in {f}: {subj} -> {obj}")

        if len(valid_rels) != len(original_rels):
            data['relations'] = valid_rels
            with open(f, 'w', encoding='utf-8') as stream:
                yaml.dump(data, stream, allow_unicode=True, sort_keys=False)

    print(f"Pruned {pruned_count} dangling relations.")

if __name__ == "__main__":
    prune_dangling_refs()
