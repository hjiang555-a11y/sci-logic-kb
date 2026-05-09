# Claim-Evidence Standard (声明-证据标准)

> **版本**：v1.0 · 2026-05-02  
> **适用范围**：sci-logic-kb 全库（所有 topic / paper YAML）  
> **关联文件**：[`SCHEMA.md`](../SCHEMA.md) · [`CONTRIBUTING.md`](../CONTRIBUTING.md) · [`docs/WORKFLOW.md`](WORKFLOW.md)

---

## 1. 声明类型

| 类型 | 定义 | 必须包含 | 示例 |
|------|------|---------|------|
| **事实声明** | 某物理系统存在或某现象被观测到 | 实体 ID + 观测条件 | `ent.xxx` 被制造并测到 finesse = 400k |
| **因果声明** | A 限制/导致/使能 B | 关系 ID + 主语 + 谓语 + 宾语 | `met.σ_y` BOUNDED-BY `pri.brownian_noise` |
| **定量声明** | 某指标在某条件下达到某值 | 指标 ID + 值 + 条件 + 不确定度 | `met.σ_y` = 8×10⁻¹⁷ @ 1s, τ = 1 s |
| **概念声明** | 某原理/模型成立或某机制有效 | 原理 ID + 适用条件 | `pri.xxx` 当 D₂ > 0 时成立 |

> 每个声明最终都锚定在知识图谱的一个节点（entity / principle / method / metric）或一条关系（relation）上。

---

## 2. 证据等级

证据按可信度排序：

| 等级 | 名称 | 定义 | 对应 confidence |
|------|------|------|----------------|
| L1 | **直接实验观测** | 论文中报告的原始实验数据，经同行评议 | `established` |
| L2 | **间接实验推断** | 从实验数据推导但非直接测量 | `established` 或 `provisional` |
| L3 | **理论推导** | 从已建立理论出发的数学推导 | `provisional`（待实验验证） |
| L4 | **数值仿真** | 有限元/时域仿真结果 | `provisional` |
| L5 | **专家意见** | 综述中的判断或预测，无直接数据支撑 | `provisional`（必须标注 `review` 来源） |

**证据升级规则**：L3–L5 可在被独立 L1 验证后升级至 `established`。L2 保留为 `established` 当且仅当推导链完全透明且被领域广泛接受。

---

## 3. 声明溯源要求

**每一条关系必须携带 `source.claim`，其值为论文中的原文直接引用。**

- ✅ 正确：`"the fractional frequency instability reaches 8×10⁻¹⁷ at 1 s of averaging"`
- ❌ 错误：`"the system achieves low phase noise"`（AI 概括，非原文）
- ❌ 错误：`"see figure 3"`（无实质内容）

**定量声明**必须同时给出：
- `demonstrated_value.value`：数值
- `demonstrated_value.conditions`：测量条件（平均时间、带宽、温度等）
- `demonstrated_value.confidence`：`established` | `provisional`
- `demonstrated_value.source.claim`：原文直接引用

**因果声明**必须同时给出：
- 关系谓词（`BOUNDED-BY` / `GOVERNED-BY` / `ENABLED-BY` 等）
- `source.claim`：证明该因果关系的原文引用
- `confidence`：`established` | `provisional`

---

## 4. 验证状态生命周期

```
proposed ──→ observed ──→ established
                │
                └──→ contested ──→ resolved (new established)
                             ──→ refuted (marked invalid)
```

| 状态 | 含义 | 触发条件 |
|------|------|---------|
| `proposed` | 理论上预测，未经验证 | 新原理/方法首次提出 |
| `observed` | 实验观测到，但未被独立复现 | 单篇论文报告 |
| `established` | 被 ≥2 个独立实验组验证，或被领域广泛接受 | 多源汇聚（见 §5） |
| `contested` | 存在互相矛盾的证据 | 冲突处理协议（见 §6） |

---

## 5. 多源汇聚规则

同一节点/关系的证据来自多篇论文时：

| 条件 | 置信度 | 标记 |
|------|--------|------|
| ≥2 独立实验组报告一致结果 | `established` | 在节点 `note` 标注支持论文 |
| 仅 1 篇论文报告 | `provisional` | 标注 "单源；待独立验证" |
| 多篇论文报告但数值/结论矛盾 | `contested` | 触发冲突处理协议（§6） |
| 综述/框架论文总结多源 | 与所引原始来源一致 | 标注 `via_review` |

**独立实验组定义**：不同机构、不同一作、不同实验装置。同一组在不同论文中的重复报告不算独立验证。

---

## 6. 冲突处理协议

```
检测冲突 → 分级 → 记录 → 标记 → 等待新数据
```

| 级别 | 定义 | 处理 |
|------|------|------|
| **mild** | 数值差异在 3σ 以内，可能来自不同条件 | 节点 `note` 记录差异 + 条件 |
| **strong** | 数值差异 > 3σ，或定性结论相反但可调和 | 节点标记 `contested` + `contested_claims` 列出双方 |
| **direct-contradiction** | 逻辑上互斥的定性声明 | 创建独立 `contested_claim` 节点 + 两篇论文间的 `CONTRADICTS` 关系 |

**冲突不自动解决**。当新论文提供决定性证据时，由人类专家标记 `resolved` 并更新共识。

---

## 7. 置信度传播

沿关系链的置信度遵循衰减规则：

| 关系类型 | 传播规则 |
|---------|---------|
| `BOUNDED-BY` | 子节点置信度 ≤ 父节点置信度。若子为 `established` 但父为 `provisional`，子降级为 `provisional`。 |
| `GOVERNED-BY` | 同 `BOUNDED-BY`。 |
| `ENABLED-BY` | 若使能原理为 `provisional`，被使能实体不高于 `provisional`。 |
| `CHARACTERIZED-BY` | 指标置信度独立于实体置信度（指标可以直接测量而实体机制未完全理解）。 |
| `DERIVED-FROM` | 推导结果置信度 ≤ 前提置信度。 |

**链式传播**：一条 3 跳链 `A → B → C` 中，C 的置信度 = min(A.confidence, B.confidence, C.confidence)。

---

## 8. 与 contribution_type 的关系

| contribution_type | 声明要求 |
|-------------------|---------|
| **breakthrough** | 必须包含 ≥1 个 `established` 级别的新记录或 `proposed` 级别的新原理。所有声明必须有 `source.claim`。必须定义 `breakthrough_paths`。 |
| **evidence** | 所有关系必须有 `source.claim`。节点可以为 `provisional`。允许 orphan 节点。 |
| **framework** | 允许无 `source.claim` 的跨论文综合声明（标注 `via_review`）。鼓励标记 `open_questions`。 |

---

## 9. lint 强制项

以下条款由 `scripts/lint.py` 自动检查：

| 检查 | 类别 | 说明 |
|------|------|------|
| `missing-evidence` | WARNING | 关系缺少 `source.claim` |
| `missing-conditions` | WARNING | 原理缺少 `conditions` |
| `reasoning-chain-gap` | WARNING | `BOUNDED-BY` 关系缺少 `breakthrough_paths` |
| `dangling-ref` | ERROR | 引用不存在的节点 ID |

---

## 10. 审核清单（人类专家用）

在标记声明为 `established` 前，确认：

- [ ] 至少 2 个独立实验组报告了定量一致的结果
- [ ] 每个来源的 `source.claim` 是原文直接引用
- [ ] 测量条件明确且可比
- [ ] 无已知的 `contested_claims` 或 `open_questions` 与此声明矛盾
- [ ] 传播路径上所有上游节点的置信度不低于 `established`

---

*首建：2026-05-02（D: claim-evidence 标准）*
*维护规范：当 SCHEMA.md 更新或 lint 规则变更时同步刷新本文档*
