# Knowledge Mapping & Consensus Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal**: Implement an explicit mapping layer between the Evidence Layer and the Logic Layer to enable accurate, traceable consensus generation for the $\sigma_y(1\text{s})$ stability metric.

**Architecture**: 
- **Evidence Layer** (Existing): Atomic nodes with values.
- **Mapping Layer** (New): A registry (`mappings.yaml`) that explicitly links `evid_*` nodes to `la.*` logic nodes.
- **Consensus Engine** (Updated): An aggregator that traverses the mapping $\to$ retrieves values $\to$ computes the branch-wise and global SOTA.
- **Reporting Layer** (Existing): Visualizes the resulting consensus.

**Tech Stack**: Python 3, PyYAML, Markdown.

---

### Task 1: Mapping Registry Definition

**Files:**
- Create: `/data/sci-logic- polycrystalline-kb/data/logic/mappings.yaml`

- [ ] **Step 1: Define the mapping schema**
  The file should follow this structure:
  ```yaml
  mappings:
    - evidence_id: "evid_SOTA_P1"
      logic_node: "la.substrate_thermal_noise"
      weight: 1.0
      contribution: "primary_value"
    - evidence_id: "evid_SOTA_P3"
      logic_node: "la.mirror_coating_noise"
      weight: 1.0
      contribution: "primary_value"
  ```

- [ ] **Step 2: Populate initial mappings for SOTA anchors**
  Map the `evid_SOTA_P1`, `evid_SOTA_P2`, and `evid_SOTA_P3` nodes created previously to their respective logic nodes in `sigma_y_atomic.yaml`.

- [ ] **Step 3: Commit**
  ```bash
  git add /data/sci-logic-kb/data/logic/mappings.yaml
  git commit -m "feat: add mapping registry for la.sigma_y_1s"
  ```

### Task 2: Consensus Engine Upgrade

**Files:**
- Modify: `/data/sci-logic-kb/scripts/generate_consensus.py`

- [ ] **Step 1: Implement Mapping-Based Retrieval**
  Rewrite the `find_best_evidence` logic to:
  1. Load `mappings.yaml`.
  2. For each `logic_node` in the chain, find all associated `evidence_id`s.
  3. Retrieve the `demonstrated_value` from the specific `evid_*.yaml` files in the evidence layer.

- [ ] **Step 2: Implement SOTA Calculation**
  Ensure the script picks the minimum value (best stability) among la-mapped evidence nodes for each branch.

- [ ] **Step 3: Verify output**
  Run the script and verify `data/consensus/sigma_y_consensus.yaml` now contains the actual values from the evidence layer.

- [ ] **Step 4: Commit**
  ```bash
  git add /data/sci-logic-kb/scripts/generate_consensus.py
  git commit -m "refactor: implement mapping-driven consensus generation"
  ```

### Task 3: End-to-End Validation & Report Generation

**Files:**
- Run: `/data/sci-logic-kb/scripts/generate_consensus_report.py`
- Review: `/data/sci-logic-kb/reports/consensus/sigma_y_sota_report.md`

- [ ] **Step 1: Run the full pipeline**
  Run: `python3 scripts/generate_consensus.py && python3 scripts/generate_consensus_report.py`

- [ ] **Step 2: Verify values in the report**
  Check that the `Global SOTA Status` and the `Trade-off Matrix` now show the correct values (e.g., P3 $\to$ 2.5e-17) instead of `N/A`.

- [ ] **Step 3: Commit report**
  ```bash
  git add /data/sci-logic-kb/reports/consensus/sigma_y_sota_report.md
  git commit -m "docs: update sigma_y sota report with mapped evidence"
  ```

---

## Self-Review
- **Spec coverage**: Covers the transition from "guessing via keywords" to "explicit mapping."
- **Placeholder scan**: No placeholders. All file paths and logic defined.
- **Type consistency**: Uses `evid_*` and `la.*` consistently across files.
