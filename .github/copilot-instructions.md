# GitHub Copilot 任务说明 — sci-logic-kb

> **最高规则**：若本文件与 `SCHEMA.md` 冲突，**一律以 `SCHEMA.md` 为准**（当前版本 v4.5）。

## 项目定位

时间频率计量领域的结构化科研知识库。核心问题：当前性能极限在哪？为什么卡在这里？怎样突破？知识以 `topics/<topic>/papers/*.yaml` 存储。

---

## 工作流路由

| 我要做什么 | 去哪里 |
|-----------|-------|
| 了解节点/关系规范（Schema） | [`SCHEMA.md`](../SCHEMA.md) — 唯一技术真源 |
| 摄入一篇论文（Step 1–10） | [`CONTRIBUTING.md`](../CONTRIBUTING.md) |
| 本地 PDF / Zotero 工作流 | [`CLAUDE.md`](../CLAUDE.md) |
| 档位判定（breakthrough/evidence/framework） | [`docs/CONTRIBUTION_TIER_RULES.md`](../docs/CONTRIBUTION_TIER_RULES.md) |
| 超稳激光专题专属规则（σ_y-first） | [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md) |
| 光学频率梳专题专属规则 | [`topics/optical-frequency-combs/_meta/scoping_principles.md`](../topics/optical-frequency-combs/_meta/scoping_principles.md) |
| 已有节点速查（自动生成） | [`docs/CURRENT_NODES_REFERENCE.md`](../docs/CURRENT_NODES_REFERENCE.md) · [`INDEX_principles.md`](../INDEX_principles.md) |
| 专题架构与论文统计 | [`TOPICS.md`](../TOPICS.md) · 各专题 `_meta/architecture.md` |
| 读者查询指南 | [`docs/USAGE.md`](../docs/USAGE.md) |

---

## GitHub Copilot 专属约束

1. **优先复用已有节点**：摄入新论文前先查 `docs/CURRENT_NODES_REFERENCE.md`（或 `INDEX_principles.md`），避免重复定义已有 `pri.*` / `meth.*`。
2. **档位判定默认 `evidence`**：不确定时归 `evidence`，等专家在 PR 审核时决定是否升档。
3. **不手工修改自动生成文件**：`INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` / `docs/CURRENT_NODES_REFERENCE.md` 由脚本生成，不直接编辑。
4. **提 PR 而非直接推送**：所有摄入、修复、重构工作通过 PR 流程，专家审核合并。
5. **Schema 更新只需同步两处**：(a) 更新 `SCHEMA.md`；(b) 重跑 `python scripts/build_index.py`。本文件和 `CLAUDE.md` 仅在行为规范本身变化时才改。
