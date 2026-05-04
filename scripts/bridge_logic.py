import os
import yaml
import glob

def sanitize(s):
    return s.lower().replace(" ", "_").replace("-", "_")

def bridge_logic_v2():
    topic_path = "/data/sci-logic-kb/topics/ultrastable-laser"
    files = glob.glob(os.path.join(topic_path, "papers/*.yaml"))

    all_papers = {}
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            try:
                data = yaml.safe_load(stream)
                if data: all_papers[f] = data
            except: continue

    cryo_meth = None
    for f, data in all_papers.items():
        if 'methods' in data:
            for m in data['methods']:
                if 'cryogenic' in m.get('name', '').lower() or 'silicon' in m.get('name', '').lower():
                    cryo_meth = m.get('id')
                    break
        if cryo_meth: break

    coating_meth = None
    for f, data in all_papers.items():
        if 'methods' in data:
            for m in data['methods']:
                if 'crystalline' in m.get('name', '').lower() or 'algaas' in m.get('name', '').lower():
                    coating_meth = m.get('id')
                    break
        if coating_meth: break

    cryo_met = None
    for f, data in all_papers.items():
        if 'metrics' in data:
            for m in data['metrics']:
                if 'allan' in m.get('name', '').lower() and 'cryo' in m.get('name', '').lower():
                    cryo_met = m.get('id')
                    break
        if cryo_met: break

    coating_met = None
    for f, data in all_papers.items():
        if 'metrics' in data:
            for m in data['metrics']:
                if 'loss_angle' in m.get('name', '').lower() or 'algaas' in m.get('name', '').lower():
                    coating_met = m.get('id')
                    break
        if coating_met: break

    print(f"Resolved IDs: CryoMeth={cryo_meth}, CoatingMeth={coating_meth}, CryoMet={cryo_met}, CoatingMet={coating_met}")

    bridges = []
    if cryo_meth and cryo_met:
        bridges.append(("ent.fp_cavity_system", "BOUNDED-BY", "pri.brownian_thermal_noise_fdt", "established"))
        bridges.append(("pri.brownian_thermal_noise_fdt", "RESOLVED-BY", cryo_meth, "established"))
        bridges.append((cryo_meth, "PRODUCES", cryo_met, "established"))
        bridges.append(("ent.cryogenic_silicon_cavity", "CHARACTERIZED-BY", cryo_met, "established"))

    if coating_meth and coating_met:
        bridges.append(("ent.mirror_coating", "BOUNDED-BY", "pri.brownian_thermal_noise_fdt", "established"))
        bridges.append(("pri.brownian_thermal_noise_fdt", "RESOLVED-BY", coating_meth, "established"))
        bridges.append((coating_meth, "PRODUCES", coating_met, "established"))

    injection_map = {
        "robinson2019.yaml": [b for b in bridges if "cryo" in b[2].lower() or "silicon" in b[2].lower()],
        "cole2013.yaml": [b for b in bridges if "coating" in b[2].lower() or "algaas" in b[2].lower()],
        "numata2004.yaml": [b for b in bridges if b[1] == "BOUNDED-BY" and b[2] == "pri.brownian_thermal_noise_fdt"]
    }

    for filename, target_bridges in injection_map.items():
        file_path = os.path.join(topic_path, "papers", filename)
        if not os.path.exists(file_path): continue

        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if 'relations' not in data: data['relations'] = []

        for b in target_bridges:
            exists = any(r.get('subject') == b[0] and r.get('predicate') == b[1] and r.get('object') == b[2] for r in data['relations'])
            if not exists:
                # Simplified ID to avoid crashes
                rel_id = f"rel.bridge_{len(data['relations'])+1}"
                data['relations'].append({
                    'id': rel_id,
                    'subject': b[0],
                    'predicate': b[1],
                    'object': b[2],
                    'confidence': b[3],
                    'source': {'note': 'Bridge injected for Metric Chain POC'}
                })

        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            print(f"Injected bridges into {filename}")

if __name__ == "__main__":
    bridge_logic_v2()
