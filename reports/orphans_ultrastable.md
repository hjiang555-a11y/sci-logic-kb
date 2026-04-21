# 超稳激光专题 · Orphan 节点收敛工作清单

> **生成方式**：`python scripts/lint.py --topic ultrastable-laser --json`（2026-04-21）
> **目的**：90 个 orphan 节点按类型分面，供专家与 AI 共同决策"并入父节点 / 建立关系 / 删除"。
>
> **本文件性质**：派生报告（derived report）。修复完成后重跑 lint 刷新。

---

## 一、总览

| 节点类型 | 数量 | 主要成因 |
|---------|------|---------|
| `meth.*` | 54 | 论文特定的工程方法，未与 `OPERATIONALIZED-AS` / `IMPLEMENTS` 关系挂接 |
| `met.*` | 23 | 论文演示值指标，未通过 `CHARACTERIZED-BY` 连到系统实体 |
| `pri.*` | 13 | 论文贡献原理，未被任何实体 `BOUNDED-BY` / `ENABLED-BY` 引用 |
| **合计** | **90** | |

---

## 二、治理分桶

### 桶 A · 并入父节点字段（~30 候选）

> 若该节点全部信息能作为父节点的一个字段（典型：仅支持单向优化趋势、无独立限制链），应并回父节点。SCHEMA §2「执行判据」直接适用。

常见模式：
- 论文特有方法，仅服务于该论文演示 → 并入对应实体的 `key_parameters` 或 `note`
- 论文特有指标，仅报告一次演示值 → 保留节点但补 `CHARACTERIZED-BY` 关系

### 桶 B · 补缺关系（~50 候选）

> 节点本身有独立价值，只是缺关系。这是主流治理路径。

典型补法：
- `meth.xxx_method_abbrev` → 补 `OPERATIONALIZED-AS met.target_metric` + `ENABLED-BY pri.underlying_principle`
- `met.xxx_demonstrated_y`  → 补 `CHARACTERIZED-BY ent.parent_system`
- `pri.xxx_principle`       → 补 `BOUNDED-BY` 或 `ENABLED-BY` 引用边

### 桶 C · 保留为"概念孤岛"（~10 候选）

> 极少数节点属于尚未接入主体的新分支（如早期 SHB 理论 Kärtner 1995、Braun 1995），保留孤立是正确的，但应在节点 `note` 中标注"pending integration into SHB sub-topic"。

---

## 三、按文件 × 节点 ID 的完整清单

> 原始报告：`/tmp/usl_orphans.txt`（生成于 lint 时；以下为快照摘要）

治理计划建议按以下顺序推进：

1. **优先处理"代表性实体仍在但其 Level-2 实例指标孤立"的文件**：  
   `chen2020.yaml` / `chen2025.yaml` / `hafner2020.yaml` / `jin2018.yaml` / `kedar2023.yaml` / `lee2026.yaml`  
   → 这些文件补 `CHARACTERIZED-BY` 关系即可收敛大批 met/meth 孤点
2. **中期处理 SHB 相关原理孤岛**：
   `kartner1995.yaml` / `braun1995.yaml` / `leibrandt2013.yaml`  
   → 等 `synthesis/spectral_hole_burning_track.md` 落地后，决定是否提升到 domain 级
3. **晚期处理论文特定工程方法**：
   `hu2015.yaml` / `huangjc2019.yaml` / `huangjc2019b.yaml` / `shi2021.yaml`  
   → 判定是并入 `meth.fiber_delay_locking` 的变体字段，还是保留独立

---

## 四、后续动作

- [ ] 由专家逐文件勾选 A/B/C 归属
- [ ] AI 根据归属执行 YAML 编辑 PR（每 PR 不超过 10 个文件）
- [ ] 每轮合并后重跑 `lint.py --topic ultrastable-laser` 跟踪 orphan 数量
- [ ] 目标：Round 1 结束时 orphan 节点 ≤ 30（从 90 收敛）
