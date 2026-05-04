import os
import yaml
from pathlib import Path

KB_ROOT = "/data/sci-logic-kb"
CONSENSUS_FILE = os.path.join(KB_ROOT, "data/consensus/sigma_y_consensus.yaml")
REPORT_DIR = os.path.join(KB_ROOT, "reports/consensus")
OUTPUT_FILE = os.path.join(REPORT_DIR, "sigma_y_sota_report.md")

def load_yaml(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_report():
    data = load_yaml(CONSENSUS_FILE)
    if not data:
        print(f"Error: Consensus file not found at {CONSENSUS_FILE}. Please run generate_consensus.py first.")
        return

    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR, exist_ok=True)

    best_path_id = None
    min_val = float('inf')
    for pid, pdata in data.get('paths', {}).items():
        val = pdata.get('estimated_sigma_y')
        if val and isinstance(val, (int, float)) and val < min_val:
            min_val = val
            best_path_id = pid

    summary = f"""# 🏆 Sigma_y(1s) Technical Boundary Summary

## 1. Global SOTA Status
- **Current World Record**: `{min_val if best_path_id else 'N/A'}`
- **Leading Path**: `{best_path_id if best_path_id else 'N/A'}`
- **Overall Status**: `{ 'Determined' if best_path_id else 'Blank' }`

---
"""
    mermaid = f"""## 2. Logic Decomposition Map (Reasoning Chain)
```mermaid
graph TD
    SOTA((sigma_y 1s)) --> BranchA[Fundamental Thermal Noise]
    SOTA --> BranchB[Environmental Noise]
    SOTA --> BranchC[Measurement Noise]

    BranchA --> A1[Substrate Noise]
    BranchA --> A2[Mirror Coating Noise]
    BranchA --> A3[Cavity Geometry]

    BranchB --> B1[Vibration Sensitivity]
    BranchB --> B2[Thermal Gradients]
    BranchB --> B3[Acceleration Noise]

    BranchC --> C1[PDH Locking Error]
    BranchC --> C2[Shot Noise Limit]
    BranchC --> C3[Electronic Drift]

    style BranchA fill:#f96,stroke:#333,stroke-width:4px
    style BranchA color:#fff
    note[Current Primary Bottleneck: Branch A]
    BranchA -.-> note
```
---
"""
    matrix = "## 3. Performance vs. Complexity Trade-off Matrix\n\n"
    matrix += "| Path | Estimated $\\sigma_y$ | Perf Tier | Effort Tier | Primary Bottleneck | Strategy |\n"
    matrix += "| :--- | :---: | :---: | :---: | :--- | :--- |\n"
    for pid, pdata in data.get('paths', {}).items():
        val = pdata.get('estimated_sigma_y', 'N/A')
        tiers = {"P1": ("3", "2"), "P2": ("4", "3"), "P3": ("5", "5")}
        p_tier, e_tier = tiers.get(pid, ("?", "?"))
        bottleneck = "Mirror Coating" if pid == "P3" else "Vibration/Symmetry" if pid == "P2" else "Amorphous Coating"
        strategy = "Baseline" if pid == "P1" else "scaling L" if pid == "P2" else "Cryo-Si"
        matrix += f"| {pid} | {val} | {p_tier} | {e_tier} | {bottleneck} | {strategy} |\n"
    matrix += "\n\n**Legend**: Tier 1 (Lowest) $\to$ Tier 5 (Highest/Extreme)"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(summary + mermaid + matrix)
    print(f"Report generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()
