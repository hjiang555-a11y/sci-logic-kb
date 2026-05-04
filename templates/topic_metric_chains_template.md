# [Topic Name] — Metric Chains (Curated)

> **Curated from knowledge graph + `_meta/architecture.md` 四栏对照表.**
> Each chain = one real research trajectory, not a combinatorial permutation.
>
> **Instructions for new topics**:
> 1. Copy this file to `reports/active/metric_chains_<topic-name>.md`
> 2. Fill in each chain group below using the `_meta/architecture.md` 物理限制↔突破路径 table as source
> 3. Each chain should have: Start Metric → Entity → Bounding Principle → Resolution Method → Improved Metric
> 4. Add σ_y (or equivalent primary metric) contribution quantification for each path
> 5. Delete this instruction block when done
>
> **Related files to reference while filling**:
> - `_meta/architecture.md` — limitation → breakthrough path table (primary source)
> - `_meta/scoping_principles.md` — primary metric definition for this topic
> - `synthesis/breakthrough_paths_matrix.md` — path × condition matrix (if exists)
> - `reports/active/chain_gap_<topic>.md` — known chain gaps
>
> **Template structure**: one Chain Group per limitation principle. Within each group, one sub-section per breakthrough path.

---

## Chain Structure

Each chain follows the pattern:

```
Start Metric → Entity → Bounding Principle → Resolution Method → Improved Metric
```

- **Start Metric** = the performance bottleneck (e.g. σ_y instability).
- **Entity** = the physical system under limitation.
- **Bounding Principle** = the physical mechanism that limits performance.
- **Resolution Method** = how researchers overcome (or partially overcome) that limit.
- **Improved Metric** = the resulting performance gain (quantified where possible).

---

## Chain Group A: [Limitation Name] (`pri.<limitation_id>`)

**Limitation**: [1–2 sentence description of the physical mechanism and why it matters.]

### A1. [Breakthrough Path Name]

| Step | Node | Description |
|------|------|-------------|
| Start Metric | `met.<id>` | [Description with representative paper] |
| Entity | `ent.<id>` | [Description] |
| Bounding Principle | `pri.<id>` | [Description] |
| Resolution Method | `meth.<id>` or (technique) | [How this path addresses the limitation] |
| → Improved Metric | `met.<id>` | [Resulting performance, with value and paper] |

**[Primary metric] contribution**: [Quantify the gain, e.g. "σ_y: ~10⁻¹⁶ → 2.5×10⁻¹⁷" or "Engineering-enabling — suppresses X below Y floor".]  
**Key papers**: [Author Year (key contribution), ...]  
**Status**: [✅ Demonstrated / 🟡 Proposed / ⛔ Refuted].

### A2. [Next Breakthrough Path]

[Same structure as A1.]

---

## Chain Group B: [Next Limitation] (`pri.<id>`)

[Same structure as Group A.]

---

## Cross-Reference: Synthesis Pages

| Chain Group | Synthesis Page |
|-------------|---------------|
| A ([Limitation]) | [`synthesis/<file>.md`](../topics/<topic>/synthesis/<file>.md) |
| B ([Limitation]) | [`synthesis/<file>.md`](../topics/<topic>/synthesis/<file>.md) |

---

## Chain Coverage Summary

| Limitation | Breakthrough Paths | Status | [Primary Metric] Impact |
|------------|-------------------|--------|------------------------|
| [Limitation 1] | [Path 1, Path 2, ...] | [✅/🟡/⛔] | [Quantified gain] |
| [Limitation 2] | [Path 1, Path 2, ...] | [✅/🟡/⛔] | [Quantified gain] |

---

*Created [YYYY-MM-DD]. Update this file when: a new primary-metric record is set; a new limitation principle is identified; a new breakthrough path is demonstrated.*
