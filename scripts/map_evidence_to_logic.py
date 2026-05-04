import os
import yaml
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci- logarithm-kb" # Correcting to the actual path
KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
LOGIC_CHAIN_FILE = os.path.join(KB_ROOT, "data/logic/chains/sigma_y_1s.yaml")
OUTPUT_REPORT = os.path.join(KB_ROOT, "reports/active/sigma_y_gap_analysis.md")

# Define keyword markers for each logic node to facilitate mapping
# In a real scenario, this would be a more complex semantic match or a separate config
MAPPING_RULES = {
    "la.mirror_coating_noise": ["coating", "crystalline", "amorphous", "mirror surface", "absorption"],
    "la.substrate_thermal_noise": ["substrate", "ule", "silicon", "cryogenic", "temp", "base material"],
    "la.cavity_geometry": ["length", "aperture", "finesse", "geometry", "radius"],
    "la.vibration_sensitivity": ["vibration", "isolation", "seismic", "acceleration", "active isolation"],
    "la.thermal_gradients": ["gradient", "thermal shield", "vacuum", "temperature stability"],
    "la.acceleration_noise": ["acceleration", "g-sensitivity", "tilt"],
    "la.pdh_locking_error": ["pdh", "locking", "servo", "frequency offset", "ram suppression"],
    "la.shot_noise_limit": ["shot noise", "photon noise", "optical power", "quantum limit"],
    "la.electronic_drift": ["electronic drift", "adc", "dac", "clock jitter", "cable"]
}

def map_evidence():
    if not os.path.exists(os.path.dirname(OUTPUT_REPORT)):
        os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)

    # Load the logic chain topology (though we mainly use the mapping rules here)
    # In the future, this should be driven by the YAML file itself
    
    evidence_files = list(Path(EVIDENCE_DIR).glob("*.yaml"))
    mappings = {node: [] for node in MAPPING_RULES.keys()}
    unmapped = []

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            try:
                node = yaml.safe_load(f)
            except Exception as e:
                print(f"Error loading {ev_path}: {e}")
                continue
        
        # Combine name and definition for keyword search
        text_to_search = (str(node.get('name', '')) + " " + str(node.get('definition', ''))).lower()
        
        is_mapped = False
        for logic_node, keywords in MAPPING_RULES.items():
            if any(kw in text_to_search for kw in keywords):
                mappings[logic_node].append({
                    "id": node.get('id'),
                    "name": node.get('name'),
                    "source": node.get('metadata', {}).get('source_paper', 'unknown')
                })
                is_mapped = True
        
        if not is_mapped:
            unmapped.append({
                "id": node.get('id'),
                "name": node.get('name')
            })

    # Generate Report
    with open(OUTPUT_REPORT, 'w', encoding='utf-8') as report:
        report.write("# Sigma_y(1s) Evidence Gap Analysis\n\n")
        report.write("This report analyzes which parts of the la.sigma_y_1s logic chain are supported by the current evidence layer.\n\n")
        
        report.write("## 1. Logic Node Coverage\n\n")
        report.write("| Logic Node | Evidence Count | Status | Primary Sources |\n")
        report.write("| :--- | :---: | :---: | :--- |\n")
        
        for node, evs in mappings.items():
            status = "✅ Covered" if len(evs) > 0 else "❌ BLANK"
            sources = ", ".join([e['source'] for e in evs[:3]]) + ("..." if len(evs) > 3 else "")
            report.write(f"| {node} | {len(evs)} | {status} | {sources} |\n")
        
        report.write("\n\n## 2. Unmapped Evidence Nodes\n")
        report.write(f"Total unmapped nodes: {len(unmapped)}\n")
        report.write("These nodes are existing in the evidence layer but don't fit the current la.sigma_y_1s la.decomposition markers.\n\n")
        
        # Only list first 20 to avoid huge files
        for u in unmapped[:20]:
            report.write(f"- {u['id']}: {u['name']}\n")
        if len(unmapped) > 20:
            report.write(f"- ... and {len(unmapped)-20} more.\n")

    print(f"Gap analysis complete. Report written to {OUTPUT_REPORT}")

if __name__ == "__main__":
    map_evidence()
