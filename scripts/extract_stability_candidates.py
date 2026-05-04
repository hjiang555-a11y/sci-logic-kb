import os
import yaml
from pathlib import Path

KB_ROOT = "/data/sci-//log-kb" # Correcting path
KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
OUTPUT_CSV = os.path.join(KB_ROOT, "reports/active/stability_candidates_for_review.csv")

def extract():
    if not os.path.exists(os.path.dirname(OUTPUT_CSV)):
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    evidence_files = list(Path(EVIDENCE_DIR).glob("*.yaml"))
    candidates = []

    # Broad markers to ensure we don't miss anything
    MARKERS = ['sigma_y', 'stability', 'instability', 'adev', 'mdev', 'hadamard', 'sota', 'record', 'limit']

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict): continue

            # Build a search string from definition and properties
            props = data.get('properties', {})
            props_text = str(props) if isinstance(props, dict) else str(props)
            defn = data.get('definition', '')
            full_text = (defn + " " + props_text).lower()

            if any(m in full_text for m in MARKERS):
                candidates.append({
                    "id": data.get('id'),
                    "name": data.get('name'),
                    "source": data.get('metadata', {}).get('source_paper', 'unknown'),
                    "definition": defn[:200] + "..." if len(defn) > 200 else defn,
                    "properties": props
                })

    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        f.write("node_id,name,source,definition,properties\n")
        for c in candidates:
            # Cleaning strings for CSV
            def_clean = f"\"{c['definition'].replace('\"', '\"\"')}\""
            props_clean = f"\"{str(c['properties']).replace('\"', '\"\"')}\""
            f.write(f"{c['id']},{c['name']},{c['source']},{def_clean},{props_clean}\n")

    print(f"Candidate extraction complete. {len(candidates)} nodes exported to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract()
