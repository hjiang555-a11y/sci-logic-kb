import os
import yaml
import glob

def add_node_if_missing(file_path, section, node_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    if section not in data:
        data[section] = []

    # Check if node already exists
    if any(n.get('id') == node_data['id'] for n in data[section]):
        return False

    data[section].append(node_data)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    return True

def add_relation_if_missing(file_path, rel_data):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}

    if 'relations' not in data:
        data['relations'] = []

    if any(r.get('id') == rel_data['id'] or
           (r.get('subject') == rel_data['subject'] and
            r.get('predicate') == rel_data['predicate'] and
            r.get('object') == rel_data['object'])
           for r in data['relations']):
        return False

    data['relations'].append(rel_data)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    return True

def build_final_poc():
    # --- 1. Define Missing Nodes ---
    # Cryo-Silicon Method & Metric
    robinson_file = "/data/sci-logic-kb/topics/ultrastable-laser/papers/robinson2019.yaml"
    cryo_meth = {
        'id': 'meth.cryogenic_silicon_stabilization',
        'name': '低温单晶硅稳频法',
        'status': 'demonstrated',
        'applies_to': 'ent.cryogenic_silicon_cavity',
        'steps_summary': 'Si-crystal spacer -> Cool to 4K -> High-Q mirroring -> Lock laser'
    }
    cryo_met = {
        'id': 'met.allan_deviation_cryo',
        'name': '低温硅腔分数频率不稳定度',
        'unit': 'fractional',
        'description': ' la-Cryo therm-noise limited stability',
        'demonstrated_value': {'value': '6.5e-17', 'conditions': '4K, 6cm cavity, Robinson 2019'}
    }

    # Coating Method & Metric
    cole_file = "/data/sci-logic-kb/topics/ultrastable-laser/papers/cole2013.yaml"
    coating_meth = {
        'id': 'meth.crystalline_coating_deposition',
        'name': '单晶镀层外延制备法',
        'status': 'demonstrated',
        'applies_to': 'ent.mirror_coating',
        'steps_summary': 'MBE growth -> Substrate transfer -> Van der Waals bonding'
    }
    # Coating metric already exists as met.algaas_coating_loss_angle_c13 in cole2013.yaml

    # Add them
    add_node_if_missing(robinson_file, 'methods', cryo_meth)
    add_node_if_missing(robinson_file, 'metrics', cryo_met)
    add_node_if_missing(cole_file, 'methods', coating_meth)

    # --- 2. Define the Logic Bridges ---
    bridges = [
        # Chain 1: Cryo-Silicon
        {"file": robinson_file, "rel": {"id": "rel.bridge_cryo_01", "subject": "ent.fp_cavity_system", "predicate": "BOUNDED-BY", "object": "pri.brownian_thermal_noise_fdt"}},
        {"file": robinson_file, "rel": {"id": "rel.bridge_cryo_02", "subject": "pri.brownian_thermal_noise_fdt", "predicate": "RESOLVED-BY", "object": "meth.cryogenic_silicon_stabilization"}},
        {"file": robinson_file, "rel": {"id": "rel.bridge_cryo_03", "subject": "meth.cryogenic_silicon_stabilization", "predicate": "PRODUCES", "object": "met.allan_deviation_cryo"}},
        {"file": robinson_file, "rel": {"id": "rel.bridge_cryo_04", "subject": "ent.cryogenic_silicon_cavity", "predicate": "CHARACTERIZED-BY", "object": "met.allan_deviation_cryo"}},

        # Chain 2: AlGaAs Coating
        {"file": cole_file, "rel": {"id": "rel.bridge_coat_01", "subject": "ent.mirror_coating", "predicate": "BOUNDED-BY", "object": "pri.brownian_thermal_noise_fdt"}},
        {"file": cole_file, "rel": {"id": "rel.bridge_coat_02", "subject": "pri.brownian_thermal_noise_fdt", "predicate": "RESOLVED-BY", "object": "meth.crystalline_coating_deposition"}},
        {"file": cole_file, "rel": {"id": "rel.bridge_coat_03", "subject": "meth.crystalline_coating_deposition", "predicate": "PRODUCES", "object": "met.algaas_coating_loss_angle_c13"}},
    ]

    for b in bridges:
        add_relation_if_missing(b['file'], b['rel'])

if __name__ == "__main__":
    build_final_poc()
