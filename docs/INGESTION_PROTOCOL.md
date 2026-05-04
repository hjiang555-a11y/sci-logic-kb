# Knowledge Base Ingestion Protocol (v1.0)

This document defines the formal, mandatory pipeline for transforming raw PDF research papers into structured knowledge nodes within `sci-logic-kb`. The goal is to move from "AI drafts" to "Verified Knowledge" with a focus on quantification and boundary conditions.

## 1. Ingestion Pipeline Overview

The pipeline consists of four distinct stages. No paper may be marked as `verified` until all stages are complete.

$\text{PDF Source} \rightarrow \text{Structured Extraction} \rightarrow \text{Metric Normalization} \rightarrow \text{Expert Verification} \rightarrow \text{Graph Integration}$

---

## 2. Stage-by-Stage Requirements

### Stage 1: Mandatory Metadata Extraction (The "Entry Gate")
Before extracting knowledge, the following metadata must be captured. Missing metadata results in an immediate "Incomplete" status.
- **Formal Identifiers**: DOI, Zotero Key, and a full BibTeX entry.
- **Contextual Role**: Determine `contribution_type` based on SCHEMA.md:
    - `breakthrough`: New performance limit or fundamental principle.
    - `evidence`: Quantified data points for existing nodes (Default).
    - `framework`: Architecture, roadmaps, or state-of-the-art reviews.

### Stage 2: Structured Knowledge Extraction (The "Skeletal" Phase)
Extraction must follow the `SCHEMA.md` precisely.
- **Node Identification**: Identify `entities`, `principles`, `methods`, and `metrics`.
- **Relationship Mapping**: Map connections using only approved predicates (e.g., `BOUNDED-BY`, `RESOLVED-BY`, `IMPLEMENTS`).
- **Source Grounding**: Every `relation` and `metric` must have a `source.claim` — a direct quote from the PDF.

### Stage 3: Metric Normalization & Boundary Mapping (The "Logic" Phase)
This is the most critical stage for ensuring the knowledge base is useful for reasoning. **A metric without conditions is a dead node.**
- **Metric Quantification**: Every `met.*` node must have a `demonstrated_value` that is numeric.
- **Boundary Condition Mapping**: Every metric must be associated with its constraints:
  - **Physical Conditions**: Temperature, vacuum level, fiber length, etc.
  - **Operational Conditions**: Sweep rate, lock state, etc.
  - **Verification Status**: (e.g., `observed`, `calculated`, `simulated`).
- **Allan Variant Specification**: For frequency stability, the specific Allan variant (ADEV, MDEV, etc.) MUST be explicitly stated.

### Stage 4: Expert Verification (The "Truth" Phase)
AI-generated YAMLs are treated as "Drafts" until signed off by a Domain Expert.
- **The Verification Checklist**:
    1. [ ] Does the `contribution_type` match the actual impact of the paper?
    2. [ ] Are the `metrics` accurately extracted and quantified?
    3. [ ] Are the `boundary conditions` sufficient to reproduce the result?
    4. [ ] Is the `metric chain` (Metric $\rightarrow$ Principle $\rightarrow$ Method) logically sound?
- **Sign-off**: Change `reliability: medium` (AI Draft) $\rightarrow$ `reliability: high` (Verified).

---

## 3. The "Metric Chain" Indexing Logic

To support the "Metric Chain" boundary logic, contributors must ensure that every metric provided in a paper is linked to the principle that limits it.

**Logic Flow for Extraction**:
$\text{New Metric Value} \rightarrow \text{Which Principle bounds this?} \rightarrow \text{Which Method resolves/improves this?}$

Example: 
- **Metric**: $\sigma_y(1s) = 10^{-15}$
- **Bounded-By**: `pri.brownian_thermal_noise` (Thermal noise limit)
- **Resolved-By**: `meth.cryogenic_cooling` (Cryogenic operation)

## 4. Quality Gates & Rejection Criteria

A paper ingestion is rejected or sent back for rework if:
1. **Lack of Quantification**: The paper claims a "significant improvement" but provides no numeric value or condition.
2. **Broken Traceability**: A relation exists without a corresponding `source.claim` from the text.
3. **Schema Violation**: Use of deprecated predicates or invalid ID naming conventions.
4. **Condition Gap**: A performance record is entered without specifying the environment (e.g., "room temperature" vs "vacuum").
