import os
import yaml
from pathlib import Path

KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
MAPPINGS_FILE = os.path.join(KB_ROOT, "data/logic/mappings.yaml")
CONSENSUS_DIR = os.path.join(KB_ROOT, "data/consensus")
OUTPUT_FILE = os.path.join(CONSENSUS_DIR, "sigma_y_consensus.yaml")

def load_yaml(path):
    if not os.path.exists(path): return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def generate():
    if not os.path.exists(CONSENSUS_DIR):
        os.makedirs(CONSENSUS_DIR, exist_ok=True)

    mappings_data = load_yaml(MAPPINGS_FILE)
    if not mappings_data or "mappings" not in mappings_data:
        print(f"Error: Mappings file not found or invalid at {MAPPINGS_FILE}")
        return

    consensus_results = {"version": "1.0", "metric": "sigma_y_1s", "paths": {}}

    for entry in mappings_data["mappings"]:
        ev_id = entry.get("evidence_id")
        logic_node = entry.get("logic_node")
        if not ev_id or not logic_node:
            continue

        ev_path = os.path.join(EVIDENCE_DIR, f"{ev_id}.yaml")
        ev_data = load_yaml(ev_path)
        if not ev_data:
            print(f"Warning: Evidence file {ev_path} not found.")
            continue

        val = ev_data.get("properties", {}).get("demonstrated_value")
        if val is None:
            print(f"Warning: No demonstrated_value in {ev_path}")
            continue

        path_id = "Unknown"
        if "_" in ev_id:
            parts = ev_id.split("_")
            path_id = parts[-1]
        else:
            path_id = ev_id

        if path_id not in consensus_results["paths"]:
            consensus_results["paths"][path_id] = {
                "estimated_sigma_y": val,
                "components": {},
                "status": "Determined"
            }
        
        consensus_results["paths"][path_id]["components"][logic_node] = {
            "value": val, 
            "ref": ev_id
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(consensus_results, f, allow_unicode=True)
    print(f"Consensus report generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()