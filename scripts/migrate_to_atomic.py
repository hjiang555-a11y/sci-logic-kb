import os
import yaml
import json
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci-logic-kb"
TOPICS_DIR = os.path.join(KB_ROOT, "topics")
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")

def migrate():
    if not os.path.exists(EVIDENCE_DIR):
        os.makedirs(EVIDENCE_DIR)

    all_yaml_files = list(Path(TOPICS_DIR).glob("**/*.yaml"))
    print(f"Found {len(all_yaml_files)} YAML files for migration.")

    processed_count = 0
    node_count = 0

    for yaml_path in all_yaml_files:
        if "templates" in str(yaml_path): continue
        
        with open(yaml_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"Error loading {yaml_path}: {e}")
                continue

        if not data or not isinstance(data, dict) or 'meta' not in data:
            continue

        meta = data.get('meta', {})
        zotero_key = meta.get('zotero_key', 'unknown')
        paper_id = os.path.basename(yaml_path).replace('.yaml', '')

        # 1. Migrate Entities -> EvidenceNodes
        entities = data.get('entities', [])
        if entities is None: entities = []
        for ent in entities:
            if not isinstance(ent, dict): continue
            node_id = ent.get('id', f"unknown_{node_count}")
            evidence_node = {
                "id": f"evid_{zotero_key}_{node_id}",
                "original_id": node_id,
                "type": "Entity/Factor",
                "name": ent.get('name'),
                "definition": ent.get('function', ent.get('note', '')),
                "properties": ent.get('key_parameters', {}),
                "metadata": {
                    "source_paper": paper_id,
                    "zotero_key": zotero_key,
                    "original_file": str(yaml_path)
                },
                "status": "Determined"
            }

            with open(os.path.join(EVIDENCE_DIR, f"{evidence_node['id']}.yaml"), 'w', encoding='utf-8') as ef:
                yaml.dump(evidence_node, ef, allow_unicode=True)
            node_count += 1

        # 2. Migrate Relations -> EvidenceRelations
        relations = data.get('relations', [])
        if relations is None: relations = []
        for rel in relations:
            if not isinstance(rel, dict): continue
            rel_id = rel.get('id', f"rel_{node_count}")
            evidence_rel = {
                "id": f"evrel_{zotero_key}_{rel_id}",
                "subject": rel.get('subject'),
                "predicate": rel.get('predicate'),
                "object": rel.get('object'),
                "evidence": rel.get('source', {}).get('claim', '') if isinstance(rel.get('source'), dict) else '',
                "metadata": {
                    "source_paper": paper_id,
                    "zotero_key": zotero_key
                }
            }
            with open(os.path.join(EVIDENCE_DIR, f"{evidence_rel['id']}.yaml"), 'w', encoding='utf-8') as rf:
                yaml.dump(evidence_rel, rf, allow_unicode=True)

        processed_count += 1

    print(f"Migration completed.")
    print(f"Papers processed: {processed_count}")
    print(f"Evidence nodes created: {node_count}")

if __name__ == "__main__":
    migrate()
