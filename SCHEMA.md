# sci-logic-kb YAML 知识提取模式文档

> **版本**：v2.0（2026-04-14）  
> **变更摘要**：重构关系类型（GOVERNED-BY拆分）；引入分层封装架构；新增外围条件层；新增状态与验证字段。

---

## 一、知识库定位与核心原则

### 定位

符号主义结构化知识库，服务时间频率计量科研（超稳激光专题）。
- **目标查询**：当前性能极限在哪？为什么卡在这？怎么突破？
- **不是**向量知识库，**支持**逻辑推理和精确路径查询。

### 智能单元原则

> **一个节点值得存在，当且仅当它能独立回答一类有意义的边界问题。**

判断标准：
- 能孤立查询（脱离上下文仍有意义）
- 有独立的设计选择空间（材料、几何、方法）
- 在不同条件下，其"是否为限制因素"的状态会变化

**节点不应过细**：若一个节点的全部信息都能作为父节点的一个字段，则应并入父节点。

---

## 二、系统架构（四层）

```
超稳激光
├── 分支1：频率参考部件          [Level 1]
│   ├── FP 腔系统                [Level 1 实体]
│   │   ├── 腔镜基底             [Level 2 子单元]
│   │   ├── 高反镀层             [Level 2 子单元]
│   │   ├── 间隔物               [Level 2 子单元]
│   │   └── 隔振系统             [Level 2 子单元]（内部属性：加速度灵敏度）
│   └── 光纤干涉仪               [Level 1 实体]
│       ├── 光纤延迟线           [Level 2 子单元]
│       └── 法拉第旋转镜         [Level 2 子单元]
├── 分支2：误差探测与反馈方法    [方法层，与 Level 1 实体关联]
│   ├── PDH 锁频（→ FP 腔）
│   ├── Tilt Locking（→ FP 腔）
│   └── 光纤延迟线锁频（→ 光纤干涉仪）
├── 分支3：反馈执行部件          [Level 1，暂缓发展]
│   └── EOM / AOM / PZT
└── 外围条件层                   [独立层，通过接口连接主分支]
    ├── ent.vibration_environment    ← 环境振动谱 + 隔振技术
    ├── ent.thermal_environment      ← 温度稳定性 + 温控技术
    └── ent.acoustic_environment     ← 声学噪声（待建）

原理层（全局，无分支归属，可被任意层引用）
```

### 封装规则

1. **层级归属**：每个实体节点有且只有一个层级归属，`PART-OF` 只向上一级。
2. **交互局部性**：Level 2 子单元的关系只在本分支内部建立；跨分支比较只在 Level 1 之间进行，通过 `COMPETES-WITH`。
3. **外围条件隔离**：外围条件节点通过 `CONDITIONED-BY` 接口连接到 Level 1/2，不直接进入分支内部逻辑。
4. **原理全局性**：原理节点不属于任何分支，可被任意层引用，但每个分支有自己独立的工作原理（不跨分支共享 Level 1 内部原理）。

---

## 三、五类节点

| 前缀 | 类型 | 说明 |
|------|------|------|
| `ent.` | 技术实体 | 具体装置/系统/部件，有层级归属 |
| `pri.` | 原理 | 物理/数学原理，全局，无分支归属 |
| `meth.` | 方法 | 技术手段，连接原理与实体 |
| `met.` | 指标 | 可量化性能指标（含接口指标） |
| `src.` | 素材 | 通过 `source` 字段引用，不单建节点 |

### 节点通用新字段

```yaml
# 实体节点新增
hierarchy_level: 1          # 0=系统 | 1=主分支实体 | 2=子单元 | ext=外围条件
status: demonstrated        # demonstrated | theoretical | obsolete

# 原理节点新增
tier: domain                # meta=跨领域元原理 | domain=领域工作原理 | engineering=工程推论

# 所有节点
verification_status: observed   # observed=实验测量 | calculated=理论推导 | inferred=推断
```

---

## 四、九种关系类型

### 4.1 关系总览

| 谓词 | 方向语义 | 典型用法 |
|------|---------|---------|
| `PART-OF` | subject 是 object 的组成部分 | `ent.mirror_substrate PART-OF ent.fp_cavity_system` |
| `CHARACTERIZED-BY` | subject 的性质由 object 刻画 | `ent.fp_cavity_system CHARACTERIZED-BY met.laser_linewidth` |
| `OPERATIONALIZED-AS` | 指标通过某方法实现/操控 | `met.laser_linewidth OPERATIONALIZED-AS meth.pdh_locking` |
| `ENABLED-BY` | subject 能工作是因为 object（机制） | `meth.pdh_locking ENABLED-BY pri.pdh_heterodyne_detection` |
| `BOUNDED-BY` | subject 的性能上限由 object 决定（极限） | `ent.fp_cavity_system BOUNDED-BY pri.brownian_thermal_noise_fdt` |
| `DERIVED-FROM` | subject 原理由 object 原理推导 | `pri.beam_radius_scaling DERIVED-FROM pri.brownian_thermal_noise_fdt` |
| `CONDITIONED-BY` | subject 的工作受 object 外部条件制约 | `ent.fp_cavity_system CONDITIONED-BY ent.vibration_environment` |
| `COMPETES-WITH` | 同层级的并列方案，有权衡 | `ent.fp_cavity_system COMPETES-WITH ent.fiber_interferometer` |
| `BREAKTHROUGH-VIA` | 突破 subject 限制的路径是 object | `pri.brownian_thermal_noise_fdt BREAKTHROUGH-VIA pri.low_loss_substrate_improvement` |

> **废弃**：`GOVERNED-BY`（已拆分为 ENABLED-BY + BOUNDED-BY）、`EQUIVALENT-IN-CONTEXT`（用共同 ENABLED-BY 表达）、`SUPPORTED-BY`（用 temporal_role 字段表达）

### 4.2 BOUNDED-BY 完整结构（最重要）

```yaml
- id: rel.X##
  subject: {node_id}
  predicate: BOUNDED-BY
  object: {pri.limiting_principle}
  confidence: established
  source: {zotero_key: "KEY", claim: "原文论断"}

  # 限制状态（必填）
  is_system_limit: true           # 当前条件下是否为主动瓶颈
  dominated_by: null              # 若 false，填写压制它的原理 ID
  quantitative_contribution: "84%"  # 占总限制的比例（如已知）
  regime: all                     # all | short-term | long-term | during-sweep

  # 认识论状态（Feynman 原则）
  verification_status: observed   # observed | calculated | inferred
  temporal_role: validates        # proposes | validates | refutes | extends

  # 突破路径（当 is_system_limit: true 时填写）
  breakthrough_paths:
    - direction: pri.or_meth.improvement
      expected_gain: "预期改善量"
      status: demonstrated        # demonstrated | theoretical | speculative
      source: {zotero_key: "KEY"}
```

### 4.3 CONDITIONED-BY 结构（外围条件接口）

```yaml
- id: rel.X##
  subject: {ent.device_node}
  predicate: CONDITIONED-BY
  object: {ent.external_condition_node}

  # 接口契约（必填）
  interface_metric: met.frequency_noise_from_vibration  # 耦合指标节点 ID
  coupling_formula: "Δν = acceleration_sensitivity × ambient_acceleration"
  internal_property: "acceleration_sensitivity: ~100 kHz/(m/s²)"
  is_system_limit:
    current: false
    conditions: "Young 1999 充分隔振后退出限制序列；Webster 2007 场景下可能主导"
```

### 4.4 COMPETES-WITH 结构

```yaml
- id: rel.X##
  subject: ent.fp_cavity_system
  predicate: COMPETES-WITH
  object: ent.fiber_interferometer
  context: "频率参考选择"
  tradeoffs:
    subject_wins: ["长期稳定度 3×10⁻¹⁶", "绝对频率参考", "热噪声极限更低"]
    object_wins: ["可捷变扫频", "无需精密光学装调", "成本低", "工程化友好"]
```

---

## 五、YAML 文件完整模板

```yaml
# {Author} {Year} — {简述}
# 提取者：Claude / GitHub Copilot（AI草稿，待专家确认）
# 提取日期：YYYY-MM-DD
# Schema版本：v2.0

meta:
  zotero_key: "{8位Zotero KEY}"
  source_type: technical_paper   # technical_paper | review | textbook | standard
  reliability: medium            # high | medium | low
  title: "完整论文标题"
  year: YYYY
  first_author: "姓氏"
  journal: "期刊名"
  doi: "10.xxxx/xxxxx"
  note: "一句话说明本文核心贡献；在知识图谱中填补哪个空白"

entities:
  - id: ent.{snake_case_name}
    name: "中文名称"
    aliases: ["英文名", "别称"]
    hierarchy_level: 1            # 0|1|2|ext
    status: demonstrated          # demonstrated | theoretical | obsolete
    function: >
      核心功能（1-3句）。聚焦在超稳激光语境中的作用。
    key_parameters:               # 关键内部属性（非外部条件）
      param_name: "值或描述"
    interface_requirements:       # 需要外部条件满足什么（接口规格）
      vibration: "残余加速度 < X nm/s²"
      temperature: "稳定性 < X mK/day"
    note: "补充说明（可选）"

principles:
  - id: pri.{snake_case_name}
    name: "原理名称（中文）"
    tier: domain                  # meta | domain | engineering
    verification_status: calculated  # observed | calculated | inferred
    statement: >
      精确表述（2-5句）：物理机制 + 数学关系 + 适用条件。
    domain: "所属领域"
    formula: "核心公式"
    key_insight: "一句话核心洞见"
    conditions: "适用条件"
    formulations:                 # 同一原理的多种表达形式（可选）
      - id: full
        formula: "完整公式"
        applicable_when: "精确计算"
      - id: simplified
        formula: "简化公式"
        applicable_when: "工程估算"
        derived_from: full
    source_claim: >
      "原文关键论断（引号内为原文）"

methods:
  - id: meth.{snake_case_name}
    name: "方法名称"
    status: demonstrated
    applies_to: ent.fp_cavity_system   # 适用的频率参考类型
    steps_summary: >
      步骤1 → 步骤2 → 步骤3 → 输出
    required_hardware:
      - ent.some_entity
    advantages:
      - "优势"
    disadvantages:
      - "劣势（含定量说明）"
    conditions:
      - "适用条件"
    source_claim: >
      "原文关键论断"

metrics:
  - id: met.{snake_case_name}
    name: "指标名称（中文）"
    unit: "单位"
    description: "物理意义（1-2句）"
    # 接口指标（仅用于外围条件耦合时填写）
    is_interface_metric: false
    coupling_formula: null
    # 实测值
    demonstrated_value:
      value: "数值或范围"
      conditions: "测量条件（必填）"
      verification_status: observed   # observed | calculated | inferred
      confidence: established         # established | likely | contested
      source: {zotero_key: "KEY", claim: "原文论断"}
    # 理论下限（若已知）
    theoretical_floor:
      value: "理论极限值"
      basis: "计算依据"
      gap_note: "当前值距理论下限的距离"

relations:
  - id: rel.{X##}               # X=论文首字母，##=两位序号
    subject: {node_id}
    predicate: {PREDICATE}       # 见第四节九种关系
    object: {node_id}
    confidence: established      # established | likely | contested
    source: {zotero_key: "KEY", claim: "原文支撑"}
    conditions: null             # 成立条件
    temporal_role: null          # proposes | validates | refutes | extends（跨论文时填）
    note: "跨文件引用时注明来源文件"
```

---

## 六、提取质量要求

### 必须做到

1. **全局唯一 ID**：跨文件引用时使用相同 ID，不重复定义
2. **关系有溯源**：每条 relation 必须有 `source.claim`
3. **数值有条件**：`demonstrated_value.value` 必须配 `conditions`
4. **原理有边界**：必须有 `conditions` 或 `applicable_when`
5. **BOUNDED-BY 要完整**：`is_system_limit` + `verification_status` 必填
6. **外围条件用接口**：振动/温度等环境因素必须通过 `CONDITIONED-BY` + 接口指标连接，不直接进入分支内部

### 严格禁止

- Level 2 子单元跨分支直接连接（如 `ent.mirror_substrate` 不得直接连接光纤分支的任何 Level 2 节点）
- 使用已废弃的 `GOVERNED-BY`、`EQUIVALENT-IN-CONTEXT`、`SUPPORTED-BY`
- 将外部环境因素（振动、温度）建为某分支的内部节点
- 创建无任何关系的孤立节点

### 跨文件引用规范

```yaml
object: pri.off_resonance_reference_light
note: "跨文件引用，定义于 shaddock1999.yaml"
```

---

## 七、已处理论文

| 文件 | Zotero Key | 论文 | v2.0状态 |
|------|-----------|------|---------|
| `drever1983.yaml` | 694DPR5F | Drever 1983 — PDH 技术 | ✅ v2.0 完成（2026-04-14） |
| `young1999.yaml` | EGAZKLXR | Young 1999 — 亚赫兹线宽可见激光 | ✅ v2.0 完成（2026-04-14） |
| `shaddock1999.yaml` | S5PX7GHC | Shaddock 1999 — Tilt Locking | ✅ v2.0 完成（2026-04-14） |
| `numata2004.yaml` | VDXBPUQB | Numata 2004 — FP 腔热噪声极限 | ✅ v2.0 完成（2026-04-14） |
| `jiang2010.yaml` | T8JR8IJ7 | Jiang 2010 — 光纤干涉仪可捷变激光 | ✅ v2.0 完成（2026-04-14） |
| `webster2007.yaml` | UCNS7EM7 | Webster 2007 — 振动不敏感 FP 腔 | ✅ v2.0 完成（2026-04-14） |

**v2.0 重整摘要**：
- `numata2004`：`ent.rigid_fp_cavity` → `ent.fp_cavity_system`；GOVERNED-BY → BOUNDED-BY（含 breakthrough_paths）；修正 PART-OF 方向；删除语义错误的工程路径 BOUNDED-BY；新增 DERIVED-FROM 链
- `young1999`：新增 `ent.vibration_environment`（ext）+ CONDITIONED-BY 接口；GOVERNED-BY → ENABLED-BY/BOUNDED-BY；新增 COMPETES-WITH；temporal_role: proposes
- `drever1983`：GOVERNED-BY → ENABLED-BY（PDH 机制）；BOUNDED-BY（散粒噪声极限）；temporal_role: proposes
- `shaddock1999`：`pri.off_resonance_reference_light` tier: meta；GOVERNED-BY → ENABLED-BY；新增 COMPETES-WITH + DERIVED-FROM；temporal_role: proposes
- `jiang2010`：新增 `ent.thermal_environment`（ext）+ CONDITIONED-BY 接口；GOVERNED-BY → ENABLED-BY/BOUNDED-BY；新增 COMPETES-WITH；删除猜测性 J10（原 GOVERNED-BY 元原理）；修正 J09 方向
