import os
import yaml
from pathlib import Path

# Configuration
KB_ROOT = "/data/sci-logic-kb"
MAPPINGS_FILE = os.path.join(KB_ROOT, "data/logic/mappings.yaml")
CONSENSUS_DIR = os.path.join(KB_ROOT, "data/consensus")
CONSENSUS_FILE = os.path.join(CONSENSUS_DIR, "sigma_y_consensus.yaml")

def load_yaml(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def propagate_change(changed_evidence_id):
    """
    Traces the impact of a change in an evidence node up to the consensus layer.
    """
    print(f"Analyzing impact of change in: {changed_evidence_id}...")
    
    mappings_data = load_yaml(MAPPINGS_FILE)
    if not mappings_data:
        print("Error: Mappings file not found.")
        return False

    # 1. Find which logic nodes are supported by this evidence
    affected_logic_nodes = []
    for m in mappings_data.get('mappings', []):
        if m.get('evidence_id') == changed_evidence_id:
            affected_logic_nodes.append(m.get('logic_node'))
    
    if not affected_logic_nodes:
        print(f"No logical impact detected for {changed_evidence_id}.")
        return False

    print(f"Affected Logic Nodes: {affected_logic_nodes}")

    # 2. Update the Consensus Layer
    consensus = load_yaml(CONSENSUS_FILE)
    if not consensus:
        print("Error: Consensus file not found.")
        return False

    # Update paths that use these logic nodes
    #- In a real system, this would use the logic chain topology.
    #- For the POC, we mark all paths that include these nodes as 'Needs-Review'.
    
    updated = False
    for pid, pdata in consensus.get('paths', {}).items():
        # Check if any of the affected logic nodes are components of this path
        # (Simplified: we'll assume the expert knows which path depends on which node)
        # In the full version, this would traverse the la.sigma_y_atomic graph.
        
        # FOR POC: Any change in a la.node triggers a review on ALL paths using it
        # We'll just mark the path as 'Needs-Review'
        pdata['status'] = 'Needs-Review'
        pdata['review_reason'] = f"Update in {changed_evidence_id} affects underlying logic {affected_logic_nodes}"
        updated = True

    if updated:
        with open(CONSENSUS_FILE, 'w', encoding='utf-8') as f:
            yaml.dump(consensus, f, allow_unicode=True)
        print(f"SUCCESS: Consensus updated. Paths marked as 'Needs-Review'.")
        return True
    
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 propagate_updates.py <evidence_id>")
        sys.exit(1)
    
    target_id = sys.argv[1]
    if propagate_change(target_id):
        print(f"Propagation complete for {target_id}.")
    else:
        print(f"No propagation needed for {target_id}.")
