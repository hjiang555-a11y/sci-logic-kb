import os
import yaml
import re
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci-//log-kb" # Fixing path
KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
OUTPUT_CSV = os.path.join(KB_ROOT, "reports/active/value_review_queue.csv")

# Regex for scientific notation
VALUE_PATTERN = r'([-+]?\d*\.?\d+)\s*([x*×eE])\s*([-+]?10)?\s*([-+]?\d+)'

def parse_scientific(text):
    match = re.search(VALUE_PATTERN, text)
    if match:
        try:
            coef = float(match.group(1)) if match.group(1) else 1.0
            exp = int(match.group(4))
            return coef * (10 ** exp)
        except (ValueError, TypeError):
            pass
    
    float_match = re.search(r'([-+]?\d*\.?\d+[eE][-+]?\d+)', text)
    if float_match:
        try:
            return float(float_match.group(1))
        except ValueError:
            pass
    return None

def extract_candidates():
    if not os.path.exists(os.path.dirname(OUTPUT_CSV)):
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    evidence_files = list(Path(EVIDENCE_DIR).glob("*.yaml"))
    candidates = []

    # Strict stability markers to avoid frequency/power confusion
    STABILITY_MARKERS = [
        'sigma_y', 'stability', 'adev', 'mdev', 'hadamard', 
        'fractional frequency instability', 'instability'
    ]

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict): continue

            node_id = data.get('id')
            
            # Scan properties and definition
            texts_to_scan = []
            props = data.get('properties', {})
            if isinstance(props, dict):
                for k, v in props.items():
                    texts_to_scan.append(f"prop:{k} = {v}")
            
            defn = data.get('definition', '')
            if defn:
                texts_to_scan.append(f"def: {defn}")

            for text in texts_to_scan:
                # CRITICAL FILTER: Must contain a stability marker AND a scientific notation
                if any(marker in text.lower() for marker in STABILITY_MARKERS):
                    val = parse_scientific(text)
                    if val is not None:
                        # PHYSICAL RANGE FILTER: sigma_y should be between 1e-12 and 1e-20 typically
                        if 1e-25 < val < 1e-10:
                            candidates.append([
                                node_id, 
                                val, 
                                data.get('metadata', {}).get('source_paper', 'unknown'), 
                                text.strip(),
                                "Needs-Review"
                            ])

    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        f.write("node_id,value,source_paper,context,status\n")
        for c in candidates:
            f.write(f"{c[0]},{c[1]},{c[2]},\"{c[3]}\",{c[4]}\n")

    print(f"Deep extraction complete. {len(candidates)} candidates written to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract_candidates()
