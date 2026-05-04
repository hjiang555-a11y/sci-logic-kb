import os
import yaml
import re
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
OUTPUT_CSV = os.path.join(KB_ROOT, "reports/active/value_candidates.csv")

# Enhanced Regex for scientific notation and common stability patterns
# Captures: 2.5 x 10^-17, 2.5e-17, 2.5 * 10^-17, 2.5 x 10-17, 10^-17, etc.
VALUE_PATTERN = r'([-+]?\d*\.?\d+)?\s*([x*×eE])\s*([-+]?10)?\s*([-+]?\d+)'

def parse_scientific(text):
    """
    Tries to extract a numeric value from a string.
    """
    # 1. Try the complex scientific pattern
    match = re.search(VALUE_PATTERN, text)
    if match:
        try:
            coef = float(match.group(1)) if match.group(1) else 1.0
            exp = int(match.group(4))
            return coef * (10 ** exp)
        except (ValueError, TypeError):
            pass
    
    # 2. Try simple float/exp notation (e.g., 2.5e-17)
    float_match = re.search(r'([-+]?\d*\.?\d+[eE][-+]?\d+)', text)
    if float_match:
        try:
            return float(float_match.group(1))
        except ValueError:
            pass
            
    return None

def extract_all_candidates():
    if not os.path.exists(os.path.dirname(OUTPUT_CSV)):
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    evidence_files = list(Path(EVIDENCE_DIR).glob("*.yaml"))
    candidates = []

    # Keywords that signal a high-probability value for sigma_y
    STABILITY_KWS = ['sigma_y', 'stability', 'instability', 'adev', 'mdev', 'hadamard', 'floor', 'limit', 'record']

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict): continue

            node_id = data.get('id')
            name = data.get('name', 'Unknown')

            # Scan Area 1: Properties
            props = data.get('properties', {})
            if isinstance(props, dict):
                for k, v in props.items():
                    if any(kw in k.lower() or (isinstance(v, str) and kw in v.lower()) for kw in STABILITY_KWS):
                        val = parse_scientific(str(v))
                        if val:
                            candidates.append([node_id, val, data.get('metadata', {}).get('source_paper', 'unknown'), f"prop:{k}", "High"])

            # Scan Area 2: Definition text
            defn = data.get('definition', '')
            if defn and any(kw in defn.lower() for kw in STABILITY_KWS):
                val = parse_scientific(defn)
                if val:
                    candidates.append([node_id, val, data.get('metadata', {}).get('source_paper', 'unknown'), f"def: {defn[:50]}...", "Med"])

    # Write to CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        f.write("node_id,value,source_paper,context,confidence\n")
        for c in candidates:
            f.write(f"{c[0]},{c[1]},{c[2]},\"{c[3]}\",{c[4]}\n")

    print(f"Deep extraction complete. {len(candidates)} candidates written to {OUTPUT_CSV}")

if __name__ == "__main__":
    extract_all_candidates()
