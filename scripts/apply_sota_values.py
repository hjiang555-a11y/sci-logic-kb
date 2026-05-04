import os
import yaml
from pathlib import Path

EVIDENCE_DIR = "/data/sci-logic-kb/data/evidence"

SOTA_DATA = {
    "evid_SOTA_P1": 1.0e-16,
    "evid_SOTA_P2": 5.0e-17,
    "evid_SOTA_P3": 2.5e-17,
    "evid_BWR7TEZ6_ent.optical_lattice_clock": 1.0e-17,
    "evid_NICHOLSON2015_ent.jila_sr_lattice_clock_n15": 2.2e-16,
    "evid_J37V2ZZQ_ent.precision_frequency_transfer_system_f22": 1.0e-17,
    "evid_P92ZFIAQ_ent.freespace_tf_link_113km_sh22": 3.0e-17,
    "evid_SCI-ESA-HRE-ESR-ISOC_ent.space_lattice_optical_clock_sloc": 8.0e-16,
    "evid_WHNQC4FV_ent.fiber_comb_microwave_cs_fountain_m09b": 3.0e-15
}

def apply():
    updated_count = 0
    for node_id, val in SOTA_DATA.items():
        path = os.path.join(EVIDENCE_DIR, f"{node_id}.yaml")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if not data: continue
                
                if 'properties' not in data or not isinstance(data['properties'], dict):
                    data['properties'] = {}
                
                data['properties']['demonstrated_value'] = val
                data['properties']['value_type'] = 'quantitative'
                
                with open(path, 'w', encoding='utf-8') as f_out:
                    yaml.dump(data, f_out, allow_unicode=True)
                updated_count += 1
    print(f"Successfully updated {updated_count} SOTA nodes.")

if __name__ == "__main__":
    apply()
