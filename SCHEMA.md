# sci-logic-kb YAML 知识提取模式文档

> **版本**：v3.0（2026-04-15）  
> **变更摘要**：实例节点降级（Level 1→2）；噪声源分类；原理节点精简合并；方法层重组（新增稳频策略分支）；探测硬件合并；外围条件层完善。

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

### 实例节点原则（v3.0 新增）

> **同一类型频率参考的不同参数配置（材料、温度、腔长）为"实例"（Level 2），不是独立竞争方案。**

- 实例保留为 Level 2 实体节点（ent.*），可承载 ENABLED-BY、BOUNDED-BY、CHARACTERIZED-BY 等关系
- 实例之间不使用 COMPETES-WITH（同类内部是"参数演进"而非"竞争"），性能对比保留在各自指标的 comparison 字段中
- COMPETES-WITH 仅用于真正不同类型的方案（如 FP 腔 vs 光纤干涉仪）

---

## 二、系统架构（五层）

```
超稳激光系统
├── 分支1：频率参考部件                    [Level 1]
│   ├── FP 腔系统 (ent.fp_cavity_system)    [Level 1 实体]
│   │   ├── [热噪声子单元] → BOUNDED-BY pri.brownian_thermal_noise_fdt
│   │   │   ├── ent.mirror_substrate（基底，84% 热噪声贡献）
│   │   │   ├── ent.mirror_coating（镀层，15% 热噪声贡献）
│   │   │   ├── ent.spacer_ule（间隔物，1% 热噪声贡献）
│   │   │   └── ent.algaas_crystalline_mirror_c13（晶体镀层，替代方案）
│   │   ├── [振动灵敏度子单元] → CONDITIONED-BY ent.vibration_environment
│   │   │   ├── ent.vibration_isolation（弹性悬挂隔振）
│   │   │   ├── ent.cutout_cavity_mount_w07（切口安装设计）
│   │   │   └── ent.cubic_force_insensitive_cavity_w11（力不敏感立方腔）
│   │   ├── [调制解调子单元] → BOUNDED-BY pri.ram_pdh_frequency_offset
│   │   │   └── ent.eom（电光调制器，合并 rf_phase_modulator + waveguide_eom）
│   │   └── [实例节点] (Level 2, 参数变体)
│   │       ├── ent.si_crystal_fp_cavity_k12（124K Si 腔，Kessler 2012 / Matei 2017）
│   │       ├── ent.si_crystal_17k_fp_cavity_l26（17K Si 腔 + AlGaAs，Lee 2026，世界纪录）
│   │       ├── ent.si_crystal_fp_cavity_4k_r19（4K Si 腔，Robinson 2019）
│   │       └── ent.self_balancing_long_cavity_h15（48 cm 长腔，Häfner 2015）
│   │
│   └── 光纤干涉仪 (ent.fiber_interferometer) [Level 1 实体]
│       ├── 核心特性：延迟时间、等效 Q 值、温度灵敏度
│       └── 内部组件：FRM、AOM 等已并入 key_parameters
│
├── 分支2：误差探测方法（核心方法）
│   ├── meth.pdh_locking（PDH 锁频）→ FP 腔
│   ├── meth.tilt_locking（倾斜锁频）→ FP 腔
│   │   └── required_hardware: split_photodetector, tilting_mirror（已并入方法节点）
│   └── meth.fiber_delay_locking（光纤延迟线锁频）→ 光纤干涉仪
│
├── 分支3：稳频策略（高级，可叠加于核心方法之上）  ← v3.0 新增
│   ├── meth.multi_stage_locking（多级级联稳频，原 two_stage_pdh 泛化）
│   ├── meth.multi_cavity_averaging（多腔频率平均，从 pri.optical_frequency_averaging 提升）
│   └── meth.ram_cancellation_z14（RAM 双通道主动消除）
│
└── 外围条件层                              [独立层，通过接口连接主分支]
    ├── ent.vibration_environment（环境振动谱）
    ├── ent.thermal_environment（温度稳定性）
    └── ent.laser_source（激光源，含初始噪声特性）  ← v3.0 新增

原理层（全局，无分支归属，可被任意层引用）
├── 核心物理原理（~15 个，tier: domain）
│   例：pri.brownian_thermal_noise_fdt, pri.pdh_heterodyne_detection, ...
├── 工程推论（已精简，合并到父原理的 condition_variables 中）
└── 已并入父节点：pri.mirror_substrate_noise_dominance, pri.beam_radius_scaling,
    pri.low_loss_substrate_improvement, pri.shot_noise_power_efficiency_scaling,
    pri.shorter_delay_line_rbs_tradeoff
```

### 封装规则

1. **层级归属**：每个实体节点有且只有一个层级归属，`PART-OF` 只向上一级。
2. **交互局部性**：Level 2 子单元的关系只在本分支内部建立；跨分支比较只在 Level 1 之间进行，通过 `COMPETES-WITH`。
3. **实例不竞争**：同一 Level 1 实体下的 Level 2 实例节点之间不使用 `COMPETES-WITH`（参数演进而非竞争）。
4. **外围条件隔离**：外围条件节点通过 `CONDITIONED-BY` 接口连接到 Level 1/2，不直接进入分支内部逻辑。
5. **原理全局性**：原理节点不属于任何分支，可被任意层引用。
6. **breakthrough_paths 约束**：`direction` 字段必须引用 `pri.*` 或 `meth.*` 节点，不得引用 `ent.*`。

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
| `DERIVED-FROM` | subject 原理由 object 原理推导 | `pri.cryogenic_mechanical_q_enhancement DERIVED-FROM pri.brownian_thermal_noise_fdt` |
| `CONDITIONED-BY` | subject 的工作受 object 外部条件制约 | `ent.fp_cavity_system CONDITIONED-BY ent.vibration_environment` |
| `COMPETES-WITH` | 同层级的并列方案，有权衡 | `ent.fp_cavity_system COMPETES-WITH ent.fiber_interferometer` |

> **废弃**：`GOVERNED-BY`（已拆分为 ENABLED-BY + BOUNDED-BY）、`EQUIVALENT-IN-CONTEXT`（用共同 ENABLED-BY 表达）、`SUPPORTED-BY`（用 temporal_role 字段表达）、`BREAKTHROUGH-VIA`（已内化为原理节点的 `condition_variables` 字段）

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
```

> **突破路径**在 BOUNDED-BY 关系的 `breakthrough_paths` 字段中写，`direction` 必须引用 `pri.*` 或 `meth.*` 节点（不得引用 `ent.*`）。

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
    source_claim: >
      "原文关键论断（引号内为原文）"
    # 条件变量分析（仅对 BOUNDED-BY 引用的限制性原理填写）
    # 边界值 = 公式(条件变量)。每个变量说明当前水平和已实现的最佳水平。
    # 有清晰解析关系的写 analytical_relation；没有的只记录 best_demonstrated。
    condition_variables:
      - symbol: "{公式中的符号}"
        name: "变量中文名"
        analytical_relation: "S_ν ∝ 1/w₀"   # 有解析关系则写；否则填 null
        current_value: "当前典型值（含参考腔型）"
        best_demonstrated:
          value: "已实现的最佳技术水平"
          source: {zotero_key: "KEY"}
        constraints: "限制该变量继续改善的约束（可选）"

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
  # ── 指标优先级原则 ──────────────────────────────────────────
  # 主指标：分数频率不稳定度 σ_y(τ)（Allan偏差，无量纲）
  #         → 波长归一化，可跨系统/跨波段公平比较，测量标准统一
  # 次指标：激光线宽（Hz，波长相关）
  #         → 未归一化，不同波段比较需注明 ν₀ 和积分时间
  # 提取时优先报告 σ_y(τ)；若论文只给线宽，需注明换算条件。
  # ────────────────────────────────────────────────────────────
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
- 同一 Level 1 实体下的 Level 2 实例节点之间使用 `COMPETES-WITH`（用指标 comparison 字段替代）
- 使用已废弃的 `GOVERNED-BY`、`EQUIVALENT-IN-CONTEXT`、`SUPPORTED-BY`
- 将外部环境因素（振动、温度）建为某分支的内部节点
- 创建无任何关系的孤立节点
- `breakthrough_paths.direction` 引用 `ent.*` 节点（必须用 `pri.*` 或 `meth.*`）

### 跨文件引用规范

```yaml
object: pri.off_resonance_reference_light
note: "跨文件引用，定义于 shaddock1999.yaml"
```

---

## 七、已处理论文

| 文件 | Zotero Key | 论文 | v3.0状态 |
|------|-----------|------|---------|
| `drever1983.yaml` | 694DPR5F | Drever 1983 — PDH 技术 | ✅ v3.0（ent.rf_phase_modulator→ent.eom，merge shot_noise_power_efficiency_scaling） |
| `young1999.yaml` | EGAZKLXR | Young 1999 — 亚赫兹线宽可见激光 | ✅ v3.0（ent.dye_laser_563nm→ent.laser_source ext，meth.two_stage_pdh→meth.multi_stage_locking） |
| `shaddock1999.yaml` | S5PX7GHC | Shaddock 1999 — Tilt Locking | ✅ v3.0（merge split_photodetector/tilting_mirror into tilt_locking，off_resonance_reference_light meta→domain） |
| `numata2004.yaml` | VDXBPUQB | Numata 2004 — FP 腔热噪声极限 | ✅ v3.0（noise_source_classification，merge 3 engineering principles into brownian_thermal_noise_fdt） |
| `jiang2010.yaml` | T8JR8IJ7 | Jiang 2010 — 光纤干涉仪可捷变激光 | ✅ v3.0（merge faraday_rotation_mirror into fiber_interferometer，agile_laser→ext，merge shorter_delay_line_rbs_tradeoff） |
| `webster2007.yaml` | UCNS7EM7 | Webster 2007 — 振动不敏感 FP 腔 | ✅ v2.0（无 v3.0 变更） |
| `kessler2012.yaml` | YKPFKDD9 | Kessler 2012 — Si 单晶低温腔 <40 mHz 线宽 | ✅ v3.0（Level 1→2，COMPETES-WITH→PART-OF，fix breakthrough_paths） |
| `cole2013.yaml` | CWIHQRJD | Cole 2013 — AlGaAs 晶体镀层 10× 热噪声降低 | ✅ v2.0（无 v3.0 变更） |
| `matei2017.yaml` | TVY7T59A | Matei 2017 — Si 腔 5–10 mHz 线宽，mod σ_y=4×10⁻¹⁷ | ✅ v3.0（remove COMPETES-WITH，fix breakthrough_paths） |
| `hafner2015.yaml` | UV6S5FFL | Häfner 2015 — 48 cm 室温 ULE 腔，σ_y < 1×10⁻¹⁶ | ✅ v3.0（Level 1→2，remove 2 COMPETES-WITH，fix breakthrough_paths） |
| `lee2026.yaml` | 4QVEXY63 | Lee 2026 — 2.5×10⁻¹⁷ Si 腔 + AlGaAs 晶体镀层（世界纪录） | ✅ v3.0（Level 1→2，remove 2 COMPETES-WITH，add meth.multi_cavity_averaging） |
| `webster2011.yaml` | A96XGR82 | Webster 2011 — 立方体力不敏感光学腔 | ✅ v2.0（无 v3.0 变更） |
| `robinson2019.yaml` | JIZCUZLY | Robinson 2019 — 4 K Si 腔热噪声极限 | ✅ v3.0（Level 1→2，COMPETES-WITH→PART-OF） |
| `zhang2014_ram.yaml` | S5GJNVG8 | Zhang 2014 — RAM 主动消除 | ✅ v3.0（merge waveguide_eom_z14 into ent.eom） |

**v3.0 重构摘要**（2026-04-15）：

### 核心改动
1. **实例节点降级**：4 个 FP 腔"独立方案"（Si 124K/17K/4K、48cm 长腔）从 Level 1 降为 Level 2（PART-OF fp_cavity_system），取消 8 条 COMPETES-WITH 关系
2. **噪声源分类**：在 ent.fp_cavity_system 中建立热噪声/振动/调制解调三个子类
3. **原理节点精简**：6 个工程推理并入父原理 condition_variables（mirror_substrate_noise_dominance、beam_radius_scaling、low_loss_substrate_improvement、shot_noise_power_efficiency_scaling、shorter_delay_line_rbs_tradeoff、pri.off_resonance_reference_light tier: meta→domain）
4. **方法层重组**：新增"稳频策略"分支（meth.multi_stage_locking、meth.multi_cavity_averaging），meth.ram_cancellation_z14 归入
5. **探测硬件合并**：split_photodetector/tilting_mirror 并入 tilt_locking；faraday_rotation_mirror 并入 fiber_interferometer；rf_phase_modulator + waveguide_eom → ent.eom
6. **外围条件完善**：ent.dye_laser_563nm → ent.laser_source (ext)；ent.agile_laser_system → ext
7. **breakthrough_paths 修正**：所有 direction 字段从 ent.* 改为 pri.*/meth.*（schema 合规）

### 疑问决议
- **疑问 1（实例节点的原理关联）**：采用方案 A——实例保留为 Level 2 节点，可承载 ENABLED-BY 等关系
- **疑问 2（EOM 合并）**：rf_phase_modulator + waveguide_eom 合并为 ent.eom，Zhang 2014 参数作为 implementations.waveguide 字段
- **疑问 3（off_resonance_reference_light）**：降级为 domain tier，不再标注 meta
- **疑问 4（多腔平均）**：新建 meth.multi_cavity_averaging（方法），保留 pri.optical_frequency_averaging 作为 ENABLED-BY 的物理原理
- **疑问 5（agile_laser_system）**：降为 ext（外围条件/系统描述），不是独立频率参考
- **疑问 6（实例 YAML 表达）**：采用方案 (a)——在各论文 YAML 中保留为 Level 2 实体节点
- **疑问 7（Webster 2011）**：已确认为 ent.cubic_force_insensitive_cavity_w11
- **疑问 8（分支3 反馈执行部件）**：替换为"稳频策略"分支，EOM 归入 FP 腔调制解调子单元
