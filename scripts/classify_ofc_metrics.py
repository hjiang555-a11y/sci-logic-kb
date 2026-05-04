import os
import yaml
import re
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
REPORT_FILE = os.path.join(KB_ROOT, "reports/active/ofc_metric_distribution.md")

# Metric Dimension Dictionary
# Each dimension contains keywords and a value-range filter to avoid confusion
METRIC_DIMENSIONS = {
    "Precision": {
        "keywords": ['sigma_y', 'stability', 'instability', 'linewidth', 'phase noise', 'adev', 'mdev', 'hadamard'],
        "value_range": (1e-25, 1e-10),
        "field": "metric_precision"
    },
    "Coverage": {
        "keywords": ['bandwidth', 'octave', 'spectral span', 'wavelength range', 'coverage'],
        "value_range": (0.1, 1000), # nm or octaves
        "field": "metric_coverage"
    },
    "Structure": {
        "keywords": ['f_rep', 'repetition rate', 'fsr', 'q-factor', 'finesse', 'comb spacing'],
        "value_range": (1e6, 1e13), # Hz or Q-factor
        "field": "metric_structure"
    },
    "Engineering": {
        "keywords": ['power', 'rin', 'footprint', 'efficiency', 'consumption', 'linewidth'],
        "value_range": (None, None), # Varies too much, rely more on keywords
        "field": "metric_engineering"
    }
}

VALUE_PATTERN = r'([-+]?\d*\.?\d+)\s*([x*×eE])\s*([-+]?10)?\s*([-+]?\d+)'

def parse_scientific(text):
    match = re.search(VALUE_PATTERN, text)
    if match:
        try:
            coef = float(match.group(1)) if match.group(1) else 1.0
            exp = int(match.group(4))
            if exp < -50 or exp > 50: return None
            return coef * (10 ** exp)
        except (ValueError, TypeError): pass
    float_match = re.search(r'([-+]?\d*\.?\d+[eE][-+]?\d+)', text)
    if float_match:
        try: return float(float_match.group(1))
        except ValueError: pass
    return None

def classify_and_update():
    if not os.path.exists(os.path.dirname(REPORT_FILE)):
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    evidence_files = [f for f in Path(EVIDENCE_DIR).glob("*.yaml") if 'comb' in f.name.lower()]
    print(f"Scanning {len(evidence_files)} OFC-related evidence nodes...")
    
    distribution = {dim: {"count": 0, "nodes": []} for dim in METRIC_DIMENSIONS}
    updated_files = 0

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict): continue

            node_id = data.get('id')
            text_blob = (str(data.get('definition', '')) + " " + str(data.get('properties', ''))).lower()
            
            modified = False
            current_props = data.get('properties', {})
            if not isinstance(current_props, dict): current_props = {}

            for dim, config in METRIC_DIMENSIONS.items():
                # Search for keywords in this dimension
                if any(kw in text_blob for kw in config['keywords']):
                    val = parse_scientific(text_blob)
                    # Validate value range if defined
                    if val is not None:
                        vr = config['value_range']
                        if vr[0] is not None and not (vr[0] <= val <= vr[1]):
                            continue
                        
                        # Update node property
                        field = config['field']
                        if current_props.get(field) != val:
                            current_props[field] = val
                            modified = True
                        
                        distribution[dim]["count"] += 1
                        distribution[dim]["nodes"].append(node_id)

            if modified:
                data['properties'] = current_props
                with open(ev_path, 'w', encoding='utf-8') as f_out:
                    yaml.dump(data, f_out, allow_unicode=True)
                updated_files += 1

    # Generate Distribution Report
    with open(REPORT_FILE, 'w', encoding='utf-8') as rep:
        rep.write("# OFC Knowledge Distribution Snapshot\n\n")
        rep.write("This report shows the coverage of la.ofc nodes across four key dimensions.\n\n")
        rep.write("| Dimension | Evidence Count | Primary Focus | Status |\n")
        rep.write("| :--- | :---: | :--- | :--- |\n")
        for dim, info in distribution.items():
            status = "Rich" if info['count'] > 10 else "Sparse" if info['count'] > 0 else "Blank"
            rep.write(f"| {dim} | {info['count']} | {METRIC_DIMENSIONS[dim]['field']} | {status} |\n")
        
        rep.write("\n\n## Detialed Node Mapping\n")
        for dim, info in distribution.items():
            rep.write(f"### {dim}\n- {', '.join(info['nodes'][:10])}{'...' if len(info['nodes']) > 10 else ''}\n\n")

    print(f"Classification complete. Updated {updated_files} nodes. Report: {REPORT_FILE}")

if __name__ == "__main__":
    classify_and_update()
