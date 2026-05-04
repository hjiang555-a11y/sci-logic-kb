import os
import yaml
import re
from pathlib import Path

KB_ROOT = "/data/sci-logic-kb"
EVIDENCE_DIR = os.path.join(KB_ROOT, "data/evidence")
REPORT_FILE = os.path.join(KB_ROOT, "reports/active/ofc_bandwidth_sota.md")

# Regex for wavelength ranges: e.g., "1000-2200 nm", "1550 to 1650 nm", "1.5-2.2 um"
RANGE_PATTERN = r'(\d*\.?\d+)\s*(?:-|–|—|to)\s*(\d*\.?\d+)\s*(nm|um|microns|octave[s]?)'
# Regex for octaves: e.g., "1.5 octaves", "over 1 octave"
OCTAVE_PATTERN = r'(\d*\.?\d+)\s*octave[s]?'

def parse_range(text):
    match = re.search(RANGE_PATTERN, text, re.IGNORECASE)
    if match:
        low = float(match.group(1))
        high = float(match.group(2))
        unit = match.group(3).lower()
        if 'um' in unit or 'micron' in unit:
            return (low * 1000, high * 1000) # Convert to nm
        return (low, high)
    return None

def parse_octaves(text):
    match = re.search(OCTAVE_PATTERN, text, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def extract_bandwidth():
    if not os.path.exists(os.path.dirname(REPORT_FILE)):
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    evidence_files = [f for f in Path(EVIDENCE_DIR).glob("*.yaml") if 'comb' in f.name.lower()]
    results = []

    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if not data or not isinstance(data, dict): continue

            node_id = data.get('id')
            name = data.get('name', 'Unknown')
            text_blob = (str(data.get('definition', '')) + " " + str(data.get('properties', ''))).lower()
            
            # Try extracting range and octaves
            wavelength_range = parse_range(text_blob)
            octaves = parse_octaves(text_blob)
            
            if wavelength_range or octaves:
                # Update the file with structured data
                props = data.get('properties', {})
                if not isinstance(props, dict): props = {}
                
                modified = False
                if wavelength_range and props.get('metric_coverage_range') != wavelength_range:
                    props['metric_coverage_range'] = wavelength_range
                    modified = True
                if octaves and props.get('metric_coverage_octaves') != octaves:
                    props['metric_coverage_octaves'] = octaves
                    modified = True
                
                if modified:
                    data['properties'] = props
                    with open(ev_path, 'w', encoding='utf-8') as f_out:
                        yaml.dump(data, f_out, allow_unicode=True)

                results.append({
                    "id": node_id,
                    "name": name,
                    "range": wavelength_range,
                    "octaves": octaves,
                    "source": data.get('metadata', {}).get('source_paper', 'unknown')
                })

    # Generate Report
    with open(REPORT_FILE, 'w', encoding='utf-8') as rep:
        rep.write("# 🌈 OFC Spectral Coverage SOTA Report\n\n")
        rep.write("This report identifies the widest spectral coverage across the la.ofc evidence layer.\n\n")
        
        # Sort by octaves if available
        sorted_res = sorted([r for r in results if r['octaves']], key=lambda x: x['octaves'], reverse=True)
        if sorted_res:
            rep.write("## 1. Octave Reach Ranking\n\n")
            rep.write("| Rank | Node ID | Name | Octaves | Source |\n")
            rep.write("| :--- | :--- | :--- | :---: | :--- |\n")
            for i, r in enumerate(sorted_res[:10], 1):
                rep.write(f"| {i} | {r['id']} | {r['name']} | {r['octaves']} | {r['source']} |\n")
            rep.write("\n---\n")

        # Sort by range (max - min)
        range_res = []
        for r in results:
            if r['range']:
                span = r['range'][1] - r['range'][0]
                range_res.append({**r, "span": span})
        
        sorted_range = sorted(range_res, key=lambda x: x['span'], reverse=True)
        if sorted_range:
            rep.write("## 2. Absolute Spectral Span Ranking\n\n")
            rep.write("| Rank | Node ID | Name | Range (nm) | Span (nm) | Source |\n")
            rep.write("| :--- | :--- | :--- | :---: | :---: | :--- |\n")
            for i, r in enumerate(sorted_range[:10], 1):
                rep.write(f"| {i} | {r['id']} | {r['name']} | {r['range'][0]}-{r['range'][1]} | {r['span']:.1f} | {r['source']} |\n")

    print(f"Bandwidth extraction complete. {len(results)} nodes updated. Report: {REPORT_FILE}")

if __name__ == "__main__":
    extract_bandwidth()
