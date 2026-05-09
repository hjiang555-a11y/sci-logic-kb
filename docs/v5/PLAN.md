# sci-logic-kb v5.0 — 三层原子推理架构计划

> **状态**: 计划草案，待确认
> **日期**: 2026-05-08
> **前置**: v4.5 知识库（534 papers / 1470 nodes / 1551 relations, lint 0 error）

---

## 一、v4.5 的局限（为什么需要 v5.0）

当前 v4.5 以论文级 YAML 组织知识，已形成完整的事实层。但在**推理**层面存在三个结构性缺陷：

| 缺陷 | 表现 | 数据 |
|------|------|------|
| **推理链隐式** | BOUNDED-BY 的 breakthrough_paths 嵌入在关系内部，无法跨论文追溯完整因果链 | 161 BOUNDED-BY, 65.2% 有路径 |
| **共识分散** | 同一指标的多个测量值分散在不同论文中，没有系统化的"当前最佳共识" | 4 contested claims, 97 open questions |
| **节点不可复用** | 1461 个节点 ID 的跨文件复用率为 0%——每个节点只有一个"家"文件 | 401 条跨文件引用依赖人工维护 |

**核心问题**: v4.5 回答了"这篇论文说了什么"，但很难回答"这个领域现在卡在哪里、谁能突破、可靠度多高"。

---

## 二、v5.0 架构设计

### 核心理念：推理叠加层（Reasoning Overlay）

v5.0 **不替代** v4.5 的 YAML 知识图，而是在其上叠加三层推理结构。v4.5 的 topics/*/papers/*.yaml 依然是事实真源。

```
v5.0 推理叠加层
═══════════════════════════════════
  Layer 3: Consensus（共识层）
  ├── 关键指标的最佳值和争论状态
  └── 领域共识报告

  Layer 2: Logic（逻辑层）
  ├── 因果推理链（chain）
  ├── 突破路径（path）
  └── 证据→逻辑映射

  Layer 1: Evidence（证据层）
  ├── 原子证据索引（从 v4.5 relations 提取）
  └── 声明去重与冲突检测
═══════════════════════════════════
v4.5 事实层（不变）
  topics/*/papers/*.yaml  ← 唯一真源
```

### 三层定义

#### Layer 1 — Evidence（证据层）

**目标**: 将每条 relation 注册为可独立检索、可验证的原子证据单元。

```yaml
# evidence/registry.yaml (单一索引文件，非每关系一文件)
evidence:
  - id: ev.BROWNIAN_THERMAL_LIMIT_FP_CAVITY
    question: "What limits FP cavity stability?"
    conclusion: "Brownian thermal noise in mirror coatings"
    confidence: established
    supporting_papers: 12       # 支持该结论的论文数
    conflicting_papers: 0       # 提出异议的论文数
    key_relations:              # 关联的 v4.5 relations
      - cole2013.rel_07
      - robinson2019.rel_07
      - numata2004.rel_01
    best_evidence: cole2013.rel_07
    open_issues: []
```

**产物**: `evidence/registry.yaml`（一个文件，~500 条证据条目）

#### Layer 2 — Logic（逻辑层）

**目标**: 将证据串联成因果推理链，显式回答"为什么卡在这里、怎样突破"。

```yaml
# logic/chains/sigma_y_cavity.yaml
chain: sigma_y_cavity_stability
question: "What determines the ultimate fractional frequency instability of FP cavity-stabilized lasers?"
current_best:
  system: ent.si_crystal_17k_fp_cavity_l26
  value: "mod σ_y = 2.5×10⁻¹⁷"
  paper: lee2026
  year: 2026

nodes:
  - id: lgn.sigma_y_cavity_root
    type: question
    statement: "FP cavity σ_y(τ=1s) limit"

  - id: lgn.thermal_noise_dominant
    type: limiting_principle
    statement: "Brownian thermal noise in mirror coatings is the dominant limit at τ=0.1-100s"
    evidence: [ev.BROWNIAN_THERMAL_LIMIT_FP_CAVITY]

  - id: lgn.coating_loss_angle
    type: condition_variable
    statement: "Coating mechanical loss angle φ determines thermal noise floor"
    current_value: "φ_IBS ≈ 5×10⁻⁴"
    best_value: "φ_AlGaAs ≤ 2.5×10⁻⁵ (室温), ~4.5×10⁻⁶ (10K)"

  - id: lgn.algaas_breakthrough
    type: breakthrough
    statement: "AlGaAs crystalline coatings reduce loss angle 10-100× vs IBS"
    evidence: [ev.CRYSTALLINE_COATING_NOISE_REDUCTION]
    status: demonstrated

edges:
  - from: lgn.sigma_y_cavity_root
    to: lgn.thermal_noise_dominant
    relation: BOUNDED-BY
  - from: lgn.thermal_noise_dominant
    to: lgn.coating_loss_angle
    relation: CONDITIONED-BY
  - from: lgn.coating_loss_angle
    to: lgn.algaas_breakthrough
    relation: RESOLVED-BY
```

**产物**: `logic/chains/` 目录（每个关键问题一个 YAML 文件，首期 6-8 条链）

#### Layer 3 — Consensus（共识层）

**目标**: 汇总跨论文证据，给出关键指标的系统级共识值。

```yaml
# consensus/sigma_y_1s_fp_cavity.yaml
metric: met.fractional_frequency_instability
context: "FP cavity-stabilized laser, σ_y(τ=1 s)"
updated: 2026-05-08

timeline:
  - year: 1999
    value: "~1×10⁻¹⁵"
    system: "Young 1999"
    note: "首次亚赫兹线宽"

  - year: 2012
    value: "~1×10⁻¹⁶"
    system: "Kessler 2012 (124K Si cavity)"
    note: "Si 腔突破"

  - year: 2026
    value: "2.5×10⁻¹⁷"
    system: "Lee 2026 (17K Si + AlGaAs)"
    note: "当前世界纪录"

consensus:
  best_demonstrated: "mod σ_y = 2.5×10⁻¹⁷"
  best_system: "Lee 2026 (17K Si cavity + AlGaAs coating)"
  theoretical_limit: "~10⁻¹⁸ (with further coating optimization)"
  confidence: established
  contested: false

remaining_gap:
  current_to_theory: "~25×"
  primary_bottleneck: "Coating thermal noise (still AlGaAs-limited at 17K)"
  next_breakthrough_candidates:
    - "Further coating material optimization (GaP, SiN)"
    - "Cryogenic operation at <4K with crystalline coatings"
    - "Longer cavity (30+ cm) to dilute coating noise"
```

**产物**: `consensus/` 目录（每个关键指标一个文件，首期 5-8 个指标）

---

## 三、与 v4.5 的关系（非破坏性）

| v4.5 | v5.0 |
|------|------|
| 论文级 YAML（事实真源） | 推理叠加层（衍生视图） |
| 写入: `topics/*/papers/*.yaml` | 读取 v4.5 YAML → 生成推理结构 |
| 由 ingest 流程维护 | 由 `scripts/build_reasoning.py` 生成 |
| 回答 "论文 X 说了什么" | 回答 "领域卡在哪里" |

**关键约束**:
1. v5.0 文件**不修改 v4.5 YAML**，仅读取
2. v5.0 YAML 的 `evidence` 字段引用 v4.5 的 relation ID（如 `cole2013.rel_07`）
3. v5.0 文件可由脚本从 v4.5 自动初始化，再由人类专家调优

---

## 四、执行计划（4 个 Phase）

### Phase 0 — 架构验证（1 天）

**目标**: 用一个专题验证三层架构可行。

**范围**: ultrastable-laser 专题（143 papers, 最成熟）

**交付**:
1. `evidence/registry_ultrastable.yaml` — 从 143 篇 USL 论文自动提取的证据索引
2. `logic/chains/sigma_y_cavity.yaml` — 一条完整推理链（人工编写）
3. `consensus/sigma_y_1s_fp_cavity.yaml` — FP 腔 σ_y 共识报告

**脚本**: `scripts/build_evidence_index.py` — 自动扫描 USL YAML，生成证据注册表草案

**成功标准**: 
- 推理链能回答 "FP 腔 σ_y(1s) 的当前极限是多少、为什么卡在这里、怎样突破"
- 共识报告包含完整时间线（1999-2026）

### Phase 1 — 推理链扩展（2-3 天）

**目标**: 为每个专题建立 1-2 条核心推理链。

| 专题 | 推理链 | 核心问题 |
|------|--------|----------|
| ultrastable-laser | `sigma_y_cavity` | FP 腔稳定度极限 |
| ultrastable-laser | `fiber_stabilization` | 光纤稳频极限 |
| optical-frequency-combs | `comb_noise_transfer` | 梳齿相位噪声传递 |
| optical-frequency-combs | `microcomb_soliton` | 微腔梳孤子产生效率 |
| frequency-standards | `optical_clock_accuracy` | 光钟系统不确定度 |
| time-frequency-transfer | `fiber_link_instability` | 光纤链路不稳定度 |
| timescales | `si_second_redefinition` | SI 秒重新定义路径 |
| shared | `allan_variance_foundations` | Allan 方差数学基础 |

**交付**: 8 个 `logic/chains/*.yaml` + 对应 `consensus/*.yaml`

### Phase 2 — 工具链建设（2 天）

**脚本**:
1. `scripts/build_evidence_index.py` — 从 v4.5 YAML 自动生成 evidence/registry.yaml
2. `scripts/validate_chains.py` — 验证推理链的引用完整性
3. `scripts/generate_consensus.py` — 从 evidence 索引生成共识报告草案
4. `scripts/reasoning_stats.py` — 推理就绪度量（扩展 stats.py）

**CI**: `.github/workflows/v5-reasoning.yml` — 自动验证推理链一致性

### Phase 3 — 整合与文档（1 天）

- 更新 SCHEMA.md（v5.0 架构章节）
- 更新 CONTRIBUTING.md（推理链贡献指南）
- 更新 README.md（三层架构导航）
- docs/v5/USAGE.md — 如何查询推理链
- 清理旧的 v5.0 遗留引用

---

## 五、风险与应对

| 风险 | 概率 | 应对 |
|------|------|------|
| 推理链编写需要深度领域知识，AI 产出的因果逻辑可能有误 | 高 | Phase 0 用 USL 样板验证 AI 产出质量；推理链标记 `confidence: draft` 待专家审核 |
| v5.0 增加复杂度但实际查询价值有限 | 中 | Phase 0 后评估：如果推理链不能提供比直接读 YAML 明显更好的洞察，终止扩展 |
| evidence 索引与 v4.5 YAML 不同步 | 中 | 脚本自动生成，CI 自动检查 freshness |
| 社区不 buy in 三层抽象 | 低 | Phase 0 先出样板，专家反馈后再决定是否全量铺开 |

---

## 六、不做什么（明确边界）

- ❌ 不创建 1600+ 个 evrel_*.yaml 文件（之前 v5.0 实验的错误方向）
- ❌ 不替代 v4.5 YAML（v5.0 是叠加层）
- ❌ 不自动化推理链生成（人工编写 + AI 辅助，不搞全自动）
- ❌ 不修改 v4.5 的 YAML 模板（向后兼容）
- ❌ 不在 Phase 0 通过前扩展到所有专题

---

## 七、决策点

Phase 0 完成后，评估以下问题决定是否继续：

1. **推理链的价值**: 人工编写的推理链是否比直接读 YAML + synthesis 页面提供明显更好的洞察？
2. **AI 产出质量**: AI 辅助生成的推理链是否需要大量人工修正？
3. **维护成本**: 自动生成的 evidence 索引是否可靠？手工编写的链是否容易过时？
4. **用户反馈**: ultrastable-laser 样板是否解决了实际查询需求？
