import os
import yaml
import re
from pathlib import Path

# Configuration
EVIDENCE_DIR = "/data/sci-logic-kb/data/evidence"

# Regex for scientific notation: e.g., 2.5 x 10^-17, 2.5e-17, 2.5 * 10^-17, 2.5 x 10-17
VALUE_PATTERN = r'([-+]?\d*\.?\d+)\s*([x*×eE])\s*([-+]?10)?\s*([-+]?\d+)'

def parse_scientific(text):
    """
    Extracts the first scientific notation number found in text.
    Returns a float or None.
    """
    # Look for common patterns of sigma_y values
    # 1. Standard scientific: 2.5 x 10^-17
    match = re.search(VALUE_PATTERN, text)
    if match:
        try:
            coef = float(match.group(1))
            exp = int(match.group(4))
            # Prevent OverflowError by capping the exponent to reasonable physical limits
            if exp < -50 or exp > 50:
                return None
            return coef * (10 ** exp)
        except (ValueError, TypeError):
            return None
    
    # 2. Simple float notation: 2.5e-17
    float_match = re.search(r'([-+]?\d*\.?\d+[eE][-+]?\d+)', text)
    if float_match:
        try:
            return float(float_match.group(1))
        except ValueError:
            return None
            
    return None

def process_files():
    evidence_files = list(Path(EVIDENCE_DIR).glob("*.yaml"))
    print(f"Scanning {len(evidence_files)} evidence nodes for quantitative values...")
    
    updated_count = 0
    
    for ev_path in evidence_files:
        with open(ev_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except Exception as e:
                print(f"Error reading {ev_path}: {e}")
                continue
        
        if not data or not isinstance(data, dict): continue
        
        # Target fields for extraction
        text_to_scan = (str(data.get('definition', '')) + " " + 
                        str(data.get('properties', {}))).lower()
        
        # Focus on stability/sigma_y related values
        # We look for patterns that likely refer to sigma_y
        if any(kw in text_to_scan for kw in ['sigma_y', 'stability', 'adev', 'mdev', 'hadamard']):
            val = parse_scientific(text_to_scan)
            if val is not None:
                # Update properties to be structured
                if 'properties' not in data or not isinstance(data['properties'], dict):
                    data['properties'] = {}
                
                # Only update if current value is missing or different
                if data['properties'].get('demonstrated_value') != val:
                    data['properties']['demonstrated_value'] = val
                    data['properties']['value_type'] = 'quantitative'
                    
                    with open(ev_path, 'w', encoding='utf-8') as f:
                        yaml.dump(data, f, allow_unicode=True)
                    updated_count += 1
    
    print(f"Value extraction complete. Updated {updated_count} nodes with quantitative values.")

if __name__ == "__main__":
    process_files()
