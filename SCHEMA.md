# sci-logic-kb YAML 知识提取模式文档

> **版本**：v4.1（2026-04-17）  
> **变更摘要**：v4.1 在 v4.0 基础上重组专题架构——合并"光钟"+"微波频率标准"为"频率标准"；移除"基础物理应用"（暂缓）；重组光学频率梳（技术/应用清晰分离、微腔梳+电光梳归并、新增天文光梳）；新增"时频计量数学基础"跨专题模块。目录 `topics/optical-clocks/` 迁移为 `topics/frequency-standards/`。
> **向后兼容**：v3.2 YAML 文件无需修改内容即可在 v4.1 下使用。已迁移的文件保留 `# Schema版本：v3.2` 头注释不影响解析；新建文件应使用 `# Schema版本：v4.1` 并在 meta 中包含 `topic:` 字段。

---

## 一、知识库定位与核心原则

### 定位

符号主义结构化知识库，服务**时间频率计量**科研全领域。
- **当前已建专题**：超稳激光（`topics/ultrastable-laser/`，78 篇论文）、光学频率梳（`topics/optical-frequency-combs/`，8 篇论文，~147 节点）
- **当前初建专题**：频率标准（`topics/frequency-standards/`，1 篇光钟框架综述）、时间标尺与钟组（`topics/timescales/`，1 篇）
- **专题体系**：详见 [`TOPICS.md`](TOPICS.md)
- **目标查询**：当前性能极限在哪？为什么卡在这？怎么突破？
- **不是**向量知识库，**支持**逻辑推理和精确路径查询。

### 文档同步原则（v3.1 新增）

> **`SCHEMA.md` 是唯一 Schema 真源（source of truth）。**

- 若 `README.md`、`.github/copilot-instructions.md`、`scripts/` 下自动化脚本提示词、旧 YAML 文件头注释与本文件冲突，**一律以 `SCHEMA.md` 为准**
- 更新 Schema 时，需同步检查：
  1. `README.md`
  2. `.github/copilot-instructions.md`
  3. `scripts/` 下自动化脚本与提示词
  4. GitHub Actions / Issue 模板中的版本文案
  5. `TOPICS.md`
  6. `topics/*/papers/*.yaml` 头部 `# Schema版本：...`
- 若暂未同步完成，必须在相关文件中明确标注“以 `SCHEMA.md` 为准”

### 智能单元原则

> **一个节点值得存在，当且仅当它能独立回答一类有意义的边界问题。**

判断标准：
- 能孤立查询（脱离上下文仍有意义）
- 有独立的设计选择空间（材料、几何、方法）
- 在不同条件下，其"是否为限制因素"的状态会变化

**节点不应过细**：若一个节点的全部信息都能作为父节点的一个字段，则应并入父节点。

**执行判据（v3.1 新增）**：
- 若节点只是在说明父原理某一个条件变量的单向优化趋势，且没有独立的证据链/限制链/竞争关系 → 并入父节点字段
- 若节点拥有独立的 `BOUNDED-BY` / `ENABLED-BY` / `CHARACTERIZED-BY` / `COMPETES-WITH` 关系，或可被多篇论文复用引用 → 保留为独立节点
- 若单个节点内容过重，但内部存在多个可复用、可单独查询的机制/部件/争议点 → 允许向下分解为子节点，而不是继续堆字段

### 实例节点原则（v3.0 新增）

> **同一类型频率参考的不同参数配置（材料、温度、腔长）为"实例"（Level 2），不是独立竞争方案。**

- 实例保留为 Level 2 实体节点（ent.*），可承载 ENABLED-BY、BOUNDED-BY、CHARACTERIZED-BY 等关系
- 实例之间不使用 COMPETES-WITH（同类内部是"参数演进"而非"竞争"），性能对比保留在各自指标的 comparison 字段中
- COMPETES-WITH 仅用于真正不同类型的方案（如 FP 腔 vs 光纤干涉仪）

**边界判断**：
- "参数变体"（→ Level 2 实例）：同一物理工作原理，仅改变材料/温度/腔长（如 ULE 腔 vs Si 腔、124K vs 17K）
- "不同类型"（→ Level 1 独立节点）：工作原理本质不同（如 FP 腔谐振 vs 光纤延迟线非谐振），拥有独立的设计选择空间

### 跨分支原理隔离原则（v3.1 新增）

> **若两个技术分支都受“同名限制”影响，但模型、调用条件、工程含义明显不同，应保留为各自独立的完整原理节点，不强行交叉合并。**

- 例：FP 腔热噪声原理与光纤延迟线热噪声原理都可被笼统称为“热噪声限制”，但公式形式、主导变量、实验接口和工程突破路径不同
- 因此：
  - **可以**在各自分支保留完整 `pri.*` 节点
  - **不必**为了形式统一强制建立跨分支直接关系
  - 仅当跨分支比较确有研究价值、且不会损害局部清晰性时，再补充连接关系

---

## 二、系统架构

### 顶层：时间频率计量知识体系（v4.1 更新）

```
时间频率计量 (Time-Frequency Metrology)
├── 专题1：超稳激光 ← 当前已建（topics/ultrastable-laser/）
├── 专题2：光学频率梳 ← 已建（topics/optical-frequency-combs/，8篇，~147节点）
│   ├── A. 光梳技术（传统飞秒梳、微腔+电光梳、天文光梳）
│   └── B. 光梳应用（频率综合、光学频率计数、双梳光谱、梳光谱学、中红外光谱）
├── 专题3：频率标准 ← 初建（topics/frequency-standards/，合并光钟+微波标准）
├── 专题4：时间频率传递 ← 架构已定义（topics/time-frequency-transfer/）
├── 专题5：时间标尺与钟组 ← 初建（topics/timescales/）
└── 模块M：时频计量数学基础 ← 跨专题模块（topics/shared/metrics/）
```

> 详见 [`TOPICS.md`](TOPICS.md) 中的完整专题架构和建设路线。
> 以下按专题补充内部架构描述；当前已补超稳激光、光学频率梳（v4.1 重组）、频率标准，并给出"时间频率传递"的统一框架草图。
```

> 详见 [`TOPICS.md`](TOPICS.md) 中的完整专题架构和建设路线。
> 以下按专题补充内部架构描述；当前已补超稳激光、光学频率梳，并给出“时间频率传递”的统一框架草图。

### 超稳激光专题内部架构（五层）

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
│   │   │   └── ent.eom（电光调制器，合并 rf_phase_modulator + waveguide_eom，含 RAM 主动抑制接口）
│   │   └── [实例节点] (Level 2, 参数变体)
│   │       ├── ent.si_crystal_fp_cavity_k12（124K Si 腔，Kessler 2012 / Matei 2017）
│   │       ├── ent.si_crystal_17k_fp_cavity_l26（17K Si 腔 + AlGaAs，Lee 2026，世界纪录）
│   │       ├── ent.si_crystal_fp_cavity_4k_r19（4K Si 腔，Robinson 2019）
│   │       ├── ent.si_crystal_fp_cavity_sub5k_c25（sub-5K 10cm Si 腔，Chen 2025）
│   │       └── ent.self_balancing_long_cavity_h15（48 cm 长腔，Häfner 2015）
│   │
│   ├── 光谱烧孔频率参考 (ent.shb_eu_yso_reference_l13) [Level 1 实体]
│   │   ├── 核心特性：低温稀土晶体、光谱孔寿命、漂移率
│   │   └── 定位：当前与 FP 腔并列；未来若扩展到更广义时频库，可上提到“光学频率参考”父层
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
│   └── meth.multi_cavity_averaging（多腔频率平均，从 pri.optical_frequency_averaging 提升）
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

### 光学频率梳专题内部架构（v4.1 重组：技术/应用分离）

```
光学频率梳系统
│
├── A. 光梳技术 ─────────────────────────────────────────────────
│   │
│   ├── A1. 飞秒锁模激光器光频梳（传统成熟光梳，Level 1）
│   │   ├── 锁模激光器
│   │   │   ├── ent.optical_frequency_comb（通用锁模激光器频率梳，权威顶层）
│   │   │   └── Level 2 实例：ent.ti_sapphire_frequency_comb
│   │   ├── 频率信号探测（含 CEO 探测）
│   │   │   ├── pri.self_referencing_f2f（f-2f 自参考）
│   │   │   └── pri.femtosecond_comb_frequency_ruler（飞秒梳频率标尺）
│   │   ├── 频率控制技术（含腔内控制部件）
│   │   │   └── （腔内 PZT、泵浦功率控制、反馈伺服等，待技术论文填充）
│   │   └── 非线性光谱拓展技术
│   │       ├── ent.photonic_crystal_fiber（超连续谱展宽）
│   │       ├── pri.supercontinuum_octave_spanning（倍频程展宽）
│   │       └── pri.nonlinear_frequency_conversion_comb（非线性频率转换）
│   │
│   ├── A2. 微腔与电光调制光梳（新型光梳平台，Level 1）
│   │   ├── ent.microresonator_frequency_comb（微腔光梳，Kerr/FWM/DKS）
│   │   │   ├── Level 2 实例：ent.silica_microtoroid_comb
│   │   │   ├── Level 2 实例：ent.crystalline_resonator_comb
│   │   │   └── Level 2 实例：ent.si3n4_integrated_comb
│   │   ├── ent.electro_optic_frequency_comb（电光调制梳，主动梳）
│   │   ├── pri.parametric_four_wave_mixing_comb（微梳 Kerr/FWM 产生）
│   │   ├── pri.dissipative_kerr_soliton（DKS 相干态范式）
│   │   ├── pri.lugiato_lefever_equation（LLE 统一描述）
│   │   ├── pri.microresonator_anomalous_dispersion（微腔反常色散）
│   │   ├── meth.cw_pumped_microcomb_generation（CW 泵浦梳产生）
│   │   ├── meth.laser_tuning_soliton_access（孤子激活方法）
│   │   └── meth.microcomb_self_referencing（微梳自参考）
│   │
│   └── A3. 天文光梳（Astro-Comb）
│       └── （光滤波技术 + 传统梳结合，待技术论文填充）
│
├── B. 光梳应用 ─────────────────────────────────────────────────
│   │
│   ├── 频率综合与计量
│   │   ├── meth.optical_frequency_counting（光学频率计数）
│   │   ├── meth.photonic_microwave_synthesis（光生微波合成）
│   │   ├── meth.wideband_optical_frequency_synthesis（宽带光学频率合成）
│   │   └── pri.optical_frequency_division_microwave（光学分频到微波）
│   │
│   ├── 双梳光谱学
│   │   ├── ent.dual_comb_spectrometer（Level 1 应用系统）
│   │   ├── meth.dual_comb_spectroscopy
│   │   ├── meth.adaptive_sampling_correction
│   │   ├── meth.cavity_enhanced_dcs
│   │   └── pri.dual_comb_multiheterodyne_detection（多外差检测原理）
│   │
│   ├── 频率梳光谱学
│   │   ├── meth.vipa_comb_spectroscopy
│   │   ├── meth.direct_two_photon_comb_spectroscopy
│   │   ├── pri.cavity_enhanced_comb_spectroscopy
│   │   └── pri.ramsey_comb_spectroscopy
│   │
│   └── 中红外梳光谱
│       ├── ent.mid_ir_frequency_comb（中红外频率梳，光谱应用导向）
│       ├── meth.dfg_comb_generation（DFG 梳产生）
│       ├── meth.opo_comb_generation（OPO 梳产生）
│       └── pri.molecular_rovibrational_fingerprint（分子指纹光谱）
│
├── 原理层（全局）
│   └── pri.frequency_ratio_measurement（光频比测量）
│
└── 外围接口层
    ├── CONDITIONED-BY ent.fp_cavity_system（超稳激光提供窄线宽光学参考）
    ├── CONDITIONED-BY ent.optical_frequency_standard（频率标准提供高准确度光学频率）
    └── 支撑专题：时间频率传递、频率标准（由梳实现跨域桥接）

指标层（跨分支）
├── 梳本体指标：met.comb_mode_equidistancy_u02, met.microcomb_mode_spacing_uniformity
├── 稳定度/合成指标：met.photonic_microwave_phase_noise, met.comb_frequency_synthesis_accuracy_g20,
│   met.comb_transfer_stability_g20
└── 光谱学指标：met.dcs_acquisition_speed, met.dcs_frequency_resolution,
    met.comb_spectroscopy_spectral_coverage, met.trace_gas_sensitivity
```

### 频率标准专题内部架构（v4.1 新增，合并光钟+微波标准）

```
频率标准系统
├── 分支1：光学频率标准（Level 1）
│   ├── ent.optical_frequency_standard（通用光学频率标准，权威顶层）
│   ├── ent.trapped_ion_optical_clock（囚禁离子光钟，Level 2 架构子类型）
│   ├── ent.optical_lattice_clock（光晶格钟，Level 2 架构子类型）
│   └── ent.nuclear_clock_229th（²²⁹Th 核钟，Level 2 架构子类型）
│
├── 分支2：微波频率标准（Level 1，待建）
│   ├── 铯喷泉钟 (Cs Fountain)
│   ├── 氢脉泽 (H Maser)
│   ├── 铷标准 (Rb Standard)
│   └── 芯片级原子钟 (CSAC / CPT)
│
├── 分支3：核心原理
│   ├── pri.quantum_projection_noise_limit（量子投影噪声极限）
│   ├── pri.dick_effect（Dick 效应）
│   └── pri.magic_wavelength_lattice（魔术波长光晶格）
│
├── 分支4：钟比对与绝对频率测量
│   └── meth.ramsey_spectroscopy_clock（Ramsey 光谱钟方法）
│
└── 外围接口层
    ├── CONDITIONED-BY ent.fp_cavity_system（超稳激光→询问激光线宽/Dick 效应耦合）
    ├── CONDITIONED-BY ent.optical_frequency_comb（光学频率梳→频率读出与比对）
    └── CONDITIONED-BY ent.si_second_definition（时间标尺→秒定义溯源）

指标层
├── met.optical_clock_fractional_instability（分数频率不稳定度）
└── met.optical_clock_fractional_uncertainty（分数频率不确定度）
```

### 时频计量数学基础模块（v4.1 新增，跨专题共享）

```
时频计量数学基础 (Metrology Mathematical Foundations)
├── Allan 偏差族
│   ├── Allan 偏差（ADEV）
│   ├── 修正 Allan 偏差（MDEV）
│   ├── 时间偏差（TDEV）
│   ├── Hadamard 方差
│   └── 重叠 Allan 偏差（OADEV）
│
├── 频率噪声谱密度
│   ├── S_y(f)：分数频率噪声谱密度
│   ├── S_φ(f)：相位噪声谱密度
│   └── 噪声模型分类（白相位噪声、闪变相位噪声、白频率噪声、闪变频率噪声、随机游走频率噪声）
│
├── 相位与时间抖动
│   ├── 相位抖动（phase jitter）
│   └── 时间抖动（time jitter）
│
├── 方差间转换关系
│   └── ADEV ↔ MDEV ↔ S_y 的解析/数值转换
│
└── 噪声类型辨识
    └── 从 ADEV 斜率或谱密度斜率辨识噪声类型
```

### 时间频率传递专题内部架构（统一框架）

```
时间频率传递系统
├── Level 1 统一目标实体：ent.time_frequency_transfer
│   └── 定位：统一“光频传递”“微波传递”“时间传递”为同一专题，
│       区分介质、链路结构与补偿机制，而不按信号频段拆成两个平行专题
│
├── 分支1：链路介质 / 场景
│   ├── 光纤链路传递（可承载超稳光频、梳分频微波、授时信号）
│   ├── 自由空间链路传递（地基 / 空地 / 星地）
│   ├── 卫星双向链路（TWSTFT / 未来光学双向链路）
│   └── GNSS 载波相位 / PPP 比较链路
│
├── 分支2：核心原理
│   ├── 双向噪声抵消 / reciprocity 近似
│   ├── 相位噪声主动补偿
│   ├── 链路时延波动与同步误差传播
│   └── 不同介质下的非互易效应、气象/电离层/机械扰动限制
│
├── 分支3：方法层
│   ├── 光纤相位噪声补偿
│   ├── 双向卫星时间频率传递
│   ├── GNSS 载波相位解算
│   └── 远程频率比对 / 时差比对
│
└── 外围接口层
    ├── CONDITIONED-BY ent.optical_frequency_standard（远程频率标准比对目标）
    ├── CONDITIONED-BY ent.optical_frequency_comb（光-微波桥接与频率读出）
    ├── CONDITIONED-BY ent.fp_cavity_system（相干光源稳定度）
    └── CONDITIONED-BY 环境链路条件（振动、温度、湍流、电离层、卫星轨道）

核心指标
├── 链路分数频率不稳定度
├── 时间偏差 / 时差不确定度
├── 补偿残余相位噪声
└── 有效可比对距离、链路可用度与系统偏差
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

# 原理节点（可选，v3.1 新增）
preconditions:              # 结构化前提；比自由文本 conditions 更适合长期维护
  - "需要满足的前提"
invalidated_when:           # 何时不再适用/被更强机制压制
  - "失效条件"
open_questions:             # 尚未解决的问题（面向科研探索）
  - "开放问题"
contested_claims:           # 明确存在争议的论断
  - claim: "争议论断"
    status: unresolved      # unresolved | resolved_for | resolved_against
    disputed_by: {zotero_key: "KEY"}

# 所有节点
verification_status: observed   # observed=实验测量 | calculated=理论推导 | inferred=推断

# 指标节点（可选，v3.1 新增）
historical_landmarks:
  first_demonstration:
    value: "首次达到的代表值"
    year: YYYY
    source: {zotero_key: "KEY"}
    note: "为什么这是首次"
  best_demonstration:
    value: "当前最佳值"
    year: YYYY
    source: {zotero_key: "KEY"}
    note: "当前最佳实现"
  selected_milestones:      # 可选，仅记录关键拐点；不要求完整年表
    - year: YYYY
      value: "代表值"
      source: {zotero_key: "KEY"}
      note: "关键演进节点"
```

### 子单元接口字段（约定）

当某种“方法”实质上只是某个 Level 2 子单元的实现接口、执行回路或工程变体，
且不再保留为独立 `meth.*` 节点时，可并入对应实体的 `key_parameters` 字段。

推荐模式：

```yaml
key_parameters:
  interface_group_name:
    variant_name:
      source: {zotero_key: "KEY"}
      mechanism: "该接口/变体如何工作"
      performance: "代表性性能或抑制水平"
      conditions: "可选，适用条件"
```

适用场景：如 `ent.eom` 下的 RAM 主动抑制接口、某安装子单元的特定支撑变体等。
若该内容后来形成可独立复用、可跨分支比较的方法，再提升回独立 `meth.*` 节点。

---

### 面向科研的附加知识维度（v3.1 新增）

- **事实**：`demonstrated_value` / `estimated_value` / `source.claim`
- **机制**：`ENABLED-BY` + `pri.*`
- **限制**：`BOUNDED-BY`
- **边界条件/前提**：`conditions` + `preconditions` + `invalidated_when`
- **证据强度**：`verification_status` + `confidence`
- **争议**：`confidence: contested` + `contested_claims`
- **开放问题**：`open_questions`
- **技术演化**：`historical_landmarks.first_demonstration` / `best_demonstration`

> 时间维度遵循**“先抓首次、再抓当前最佳、必要时补关键里程碑”**的原则，不要求为每个指标穷尽完整年表。

---

## 四、八种关系类型

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
  scaling_law: "Δν/ν ∝ 1/L²  (thermal noise); κ ∝ M (vibration sensitivity)"  # 定量比例关系（v3.2新增）
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
  # 多维权衡矩阵（v3.2新增，用于架构级技术路线比较）
  comparison_matrix:
    - dimension: "vibration_insensitivity"
      subject: "low (requires active isolation)"
      object: "high (coil design)"
    - dimension: "ultimate_stability"
      subject: "2.5×10⁻¹⁷ (demonstrated)"
      object: "10⁻¹⁷? (theoretical)"
    - dimension: "portability"
      subject: "low"
      object: "high"
    - dimension: "engineering_complexity"
      subject: "high (vacuum, cryogenics)"
      object: "medium (fiber spool, thermal control)"
```

---

## 五、YAML 文件完整模板

```yaml
# {Author} {Year} — {简述}
# 提取者：Claude / GitHub Copilot（AI草稿，待专家确认）
# 提取日期：YYYY-MM-DD
# Schema版本：v4.0
# 专题：ultrastable-laser

meta:
  zotero_key: "{8位Zotero KEY}"
  topic: ultrastable-laser         # 所属专题（对应 topics/ 子目录名）
  source_type: technical_paper   # technical_paper | review | textbook | standard
  contribution_type: technical   # technical=具体技术贡献 | framework=专题框架定义
                                 # technical: 原始研究论文，提供新的实验结果/方法
                                 # framework: 综述/路线图/教科书，定义专题顶层架构（见第八节）
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
    # 代价/可行性评估（v3.2新增）
    feasibility_assessment:
      engineering_complexity: "high | medium | low"
      cost_estimate: "$$$ | $$ | $ （相对评估）"
      space_requirements: "描述空间需求"
      vibration_management_difficulty: "描述振动管理难度"
    practical_limitations:        # 实际工程限制（如支撑力均衡、温度梯度等）
      - description: "限制描述"
        source_claim: "原文依据（可选）"
        impact: "对系统性能或可扩展性的影响"
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
    preconditions:
      - "结构化前提（可选）"
    invalidated_when:
      - "失效条件（可选）"
    source_claim: >
      "原文关键论断（引号内为原文）"
    open_questions:
      - "本文留下的开放问题（可选）"
    contested_claims:
      - claim: "存在争议的论断（可选）"
        status: unresolved
        disputed_by: {zotero_key: "KEY"}
    # 改善潜力与路线图预测（v3.2新增）
    improvement_potential:
      parameter: "{关键参数（如 φ, T, L, w₀）}"
      current_best: "当前最佳值（含来源）"
      theoretical_limit: "理论极限值（如已知）"
      bottleneck: "限制继续改善的瓶颈（如材料、工艺、测量）"
    roadmap_estimates:
      - timeline: "3–5 years"
        expected_value: "预期可达到的值"
        conditions: "所需条件（如工艺改进、新材料）"
      - timeline: "5–10 years"
        expected_value: "远期预期值"
        conditions: "所需突破（如新物理机制）"

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
    historical_landmarks:
      first_demonstration:
        value: "首次达到的代表值"
        year: YYYY
        source: {zotero_key: "KEY"}
        note: "首次演示（优先填写）"
      best_demonstration:
        value: "当前最佳值"
        year: YYYY
        source: {zotero_key: "KEY"}
        note: "当前最佳（优先填写）"
      selected_milestones:
        - year: YYYY
          value: "关键拐点值"
          source: {zotero_key: "KEY"}
          note: "仅在需要时补充"

relations:
  - id: rel.{X##}               # X=论文首字母，##=两位序号
    subject: {node_id}
    predicate: {PREDICATE}       # 见第四节八种关系
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
7. **时间信息优先级**：指标优先填写 `first_demonstration` 与 `best_demonstration`，其余里程碑按需补充
8. **争议/开放问题显式化**：若论文明确提出未解决问题或存在文献分歧，不要只写入 `note`，应优先使用 `open_questions` / `contested_claims`

### 严格禁止

- Level 2 子单元跨分支直接连接（如 `ent.mirror_substrate` 不得直接连接光纤分支的任何 Level 2 节点）
- 同一 Level 1 实体下的 Level 2 实例节点之间使用 `COMPETES-WITH`（用指标 comparison 字段替代）
- 使用已废弃的 `GOVERNED-BY`、`EQUIVALENT-IN-CONTEXT`、`SUPPORTED-BY`
- 在文档冲突时自行选择非 `SCHEMA.md` 的版本作为依据
- 将外部环境因素（振动、温度）建为某分支的内部节点
- 创建无任何关系的孤立节点
- `breakthrough_paths.direction` 引用 `ent.*` 节点（必须用 `pri.*` 或 `meth.*`）

### 跨文件引用规范

```yaml
# 同一专题内跨文件引用
object: pri.off_resonance_reference_light
note: "跨文件引用，定义于 shaddock1999.yaml"

# 跨专题引用（v4.0 新增）
object: pri.dick_effect
note: "跨专题引用，定义于 topics/frequency-standards/papers/xxx.yaml"
```

---

## 七、已处理论文

| 文件 | Zotero Key | 论文 | 历史重构状态 |
|------|-----------|------|---------|
| `drever1983.yaml` | 694DPR5F | Drever 1983 — PDH 技术 | ✅ v3.0（ent.rf_phase_modulator→ent.eom，merge shot_noise_power_efficiency_scaling） |
| `young1999.yaml` | EGAZKLXR | Young 1999 — 亚赫兹线宽可见激光 | ✅ v3.0（ent.dye_laser_563nm→ent.laser_source ext，meth.two_stage_pdh→meth.multi_stage_locking） |
| `shaddock1999.yaml` | S5PX7GHC | Shaddock 1999 — Tilt Locking | ✅ v3.0（merge split_photodetector/tilting_mirror into tilt_locking，off_resonance_reference_light meta→domain） |
| `numata2004.yaml` | VDXBPUQB | Numata 2004 — FP 腔热噪声极限 | ✅ v3.0（noise_source_classification，merge 3 engineering principles into brownian_thermal_noise_fdt） |
| `jiang2010.yaml` | T8JR8IJ7 | Jiang 2010 — 光纤干涉仪可捷变激光 | ✅ v3.0（merge faraday_rotation_mirror into fiber_interferometer，agile_laser→ext，merge shorter_delay_line_rbs_tradeoff） |
| `webster2007.yaml` | UCNS7EM7 | Webster 2007 — 振动不敏感 FP 腔 | ✅ 兼容（无 v3.0 专项变更） |
| `kessler2012.yaml` | YKPFKDD9 | Kessler 2012 — Si 单晶低温腔 <40 mHz 线宽 | ✅ v3.0（Level 1→2，COMPETES-WITH→PART-OF，fix breakthrough_paths） |
| `cole2013.yaml` | CWIHQRJD | Cole 2013 — AlGaAs 晶体镀层 10× 热噪声降低 | ✅ 兼容（无 v3.0 专项变更） |
| `matei2017.yaml` | TVY7T59A | Matei 2017 — Si 腔 5–10 mHz 线宽，mod σ_y=4×10⁻¹⁷ | ✅ v3.0（remove COMPETES-WITH，fix breakthrough_paths） |
| `hafner2015.yaml` | UV6S5FFL | Häfner 2015 — 48 cm 室温 ULE 腔，σ_y < 1×10⁻¹⁶ | ✅ v3.0（Level 1→2，remove 2 COMPETES-WITH，fix breakthrough_paths） |
| `lee2026.yaml` | 4QVEXY63 | Lee 2026 — 2.5×10⁻¹⁷ Si 腔 + AlGaAs 晶体镀层（世界纪录） | ✅ v3.0（Level 1→2，remove 2 COMPETES-WITH，add meth.multi_cavity_averaging） |
| `webster2011.yaml` | A96XGR82 | Webster 2011 — 立方体力不敏感光学腔 | ✅ 兼容（无 v3.0 专项变更） |
| `robinson2019.yaml` | JIZCUZLY | Robinson 2019 — 4 K Si 腔热噪声极限 | ✅ v3.0（Level 1→2，COMPETES-WITH→PART-OF） |
| `zhang2017.yaml` | N9AGEQ8S | Zhang 2017 — 闭循环 4 K Si 腔 1×10⁻¹⁶ 稳定度 | ✅ 符合v3.2（首次提取） |
| `zhang2014_ram.yaml` | S5GJNVG8 | Zhang 2014 — RAM 主动消除 | ✅ v3.0（merge waveguide_eom_z14 into ent.eom） |
| `dong2015.yaml` | W8K5GLK6 | Dong 2015 — 光纤延迟线锁频首次亚赫兹线宽（0.67 Hz） | ✅ 符合v3.1（首次提取） |
| `kefelian2009.yaml` | MN54T4F3 | Kéfélian 2009 — 光纤延迟线锁频首次实现超低频率噪声 | ✅ 符合v3.1（首次提取） |
| `huang2023.yaml` | JYGVFJBN | Huang 2023 — 全光纤超稳激光长期稳定度 1.1×10⁻¹⁴ | ✅ 符合v3.1（首次提取） |
| `jeon2025.yaml` | SBPRDKPV | Jeon 2025 — 自零差光纤锁频 6.3×10⁻¹⁵ @ 16 ms，4–200 Hz 达到热噪声极限 | ✅ 符合v3.2（首次提取） |
| `kedar2023.yaml` | 8YK6EH22 | Kedar 2023 — 低温硅腔晶体镀层频率噪声与双折射 | ✅ 符合v3.1（首次提取） |
| `chen2025.yaml` | N6HILT6B | Chen 2025 — 10 cm Si 腔 sub-5K 10⁻¹⁷ 级稳定度 | ✅ 符合v3.1（首次提取） |
| `webster2008.yaml` | VU2V2PTX | Webster 2008 — 热噪声极限光学腔（首次全面验证） | ✅ 符合v3.1（首次提取） |
| `legero2010.yaml` | MW3RDB68 | Legero 2010 — FS 镜参考腔 CTE 调谐 | ✅ 符合v3.1（首次提取） |
| `leibrandt2013.yaml` | H5MYBTXH | Leibrandt 2013 — 惯性力前馈加速度灵敏度 <10⁻¹²/g | ✅ 符合v3.1（首次提取） |
| `millo2009.yaml` | GLXHEIPV | Millo 2009 — 振动不敏感腔超稳激光 5.6×10⁻¹⁶ | ✅ 符合v3.1（首次提取） |
| `cole2016.yaml` | 4GUXEM2C | Cole 2016 — 高性能晶体镀层 NIR/MIR 3 ppm 损耗 | ✅ 符合v3.1（首次提取） |
| `tai2017.yaml` | AHUZI4A7 | Tai 2017 — 可搬运 1555 nm 超稳激光 185 mHz 线宽 | ✅ 符合v3.1（首次提取） |
| `herbers2022.yaml` | NU79W75P | Herbers 2022 — 可搬运钟激光系统达到 1.6×10⁻¹⁶ 不稳定度 | ✅ 符合v3.2（首次提取） |
| `michaudbelleau2021.yaml` | DD6SE43C | Michaud-Belleau 2021 — 空心光纤背向散射 −118 dB/m | ✅ 符合v3.1（首次提取） |
| `michaudbelleau2022.yaml` | 4GT5VD54 | Michaud-Belleau 2022 — 空心光纤热噪声理论+实测 | ✅ 符合v3.1（首次提取） |
| `kim2008.yaml` | H5YVF5AR | Kim 2008 — 远程光学/微波源漂移自由飞秒同步 | ✅ 符合v3.2（首次提取） |
| `belardi2015.yaml` | 2F3PD62T | Belardi 2015 — 反谐振空心光纤在可见/近红外的宽带设计与低损耗特性 | ✅ 符合v3.2（首次提取） |
| `parke2025.yaml` | U2LXSU62 | Parke 2025 — 68 cm 腔 300 μs 存储时间与 10⁻⁷ RAM 消除 | ✅ 符合v3.2（首次提取） |
| `wu2016.yaml` | PZGR9S7S | Wu 2016 — 1557 nm 0.26 Hz 线宽室温超稳激光 | ✅ 符合v3.2（首次提取） |
| `marchio2018.yaml` | LCMWCIWB | Marchio 2018 — 大面积晶体镀层光学性能表征 | ✅ 符合v3.2（首次提取） |
| `steinlechner2018.yaml` | L6KKLLSR | Steinlechner 2018 — 引力波探测器镜面镀层发展综述 | ✅ 符合v3.2（首次提取） |
| `tao2018.yaml` | U4Z95559 | Tao 2018 — 抗 100g 冲击振动不敏感腔设计 | ✅ 符合v3.2（首次提取） |
| `mohle2013.yaml` | 8MNIBZEW | Möhle 2013 — 高稳定压电可调谐参考腔 | ✅ 符合v3.2（首次提取） |
| `argence2012.yaml` | RP8Q44RZ | Argence 2012 — 空间应用超稳腔原型 | ✅ 符合v3.2（首次提取） |
| `didier2018.yaml` | PHRXF4IL | Didier 2018 — 超紧凑 25mm 金字塔形参考腔 | ✅ 符合v3.2（首次提取） |
| `sanjuan2019.yaml` | H3HYK5D3 | Sanjuan 2019 — BOOST 空间狭义相对论检验光学腔 | ✅ 符合v3.2（首次提取） |
| `hafner2020.yaml` | X7XXKXDZ | Häfner 2020 — 可搬运 12cm 腔询问激光 3×10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `chen2014.yaml` | WTUHUAQ7 | Chen 2014 — STE-QUEST 紧凑可搬运超稳激光 | ✅ 符合v3.2（首次提取） |
| `herbers2019.yaml` | WP8FMS5N | Herbers 2019 — 光钟频率倍频器相位噪声 | ✅ 符合v3.2（首次提取） |
| `jin2018.yaml` | 6R3RCHPT | Jin 2018 — 30cm 腔 578nm 2×10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `jiang2011.yaml` | RAC23NZV | Jiang 2011 — 10⁻¹⁶ 腔稳激光 Yb 光钟 | ✅ 符合v3.2（首次提取） |
| `li2018.yaml` | AFFU5KGB | Li 2018 — 30cm 腔 Sr 钟 10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `didier2019.yaml` | MIAVJSIK | Didier 2019 — 946nm 数字锁定+传递锁定 | ✅ 符合v3.2（首次提取） |
| `chen2020.yaml` | Z37PT8RC | Chen 2020 — 10cm 立方双腔 6×10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `yan2018.yaml` | XWBUNX3P | Yan 2018 — 多腔频率平均超稳激光 | ✅ 符合v3.2（首次提取） |
| `leibrandt2013.yaml` | WK9QLCGF | Leibrandt 2013 — SHB 光谱烧孔频率参考 | ✅ 符合v3.2（首次提取） |
| `huang2023.yaml` | JYGVFJBN | Huang 2023 — 全光纤长期稳定度 1.1×10⁻¹⁴ | ✅ 符合v3.2（首次提取） |
| `huangjc2019.yaml` | F2GG2N6W | Huang 2019 — 全光纤 200mHz 线宽 | ✅ 符合v3.2（首次提取） |
| `hu2015.yaml` | KH82PQJ2 | Hu 2015 — 超低加速度灵敏度光纤盘 | ✅ 符合v3.2（首次提取） |
| `shi2021.yaml` | QLXRP462 | Shi 2021 — HCF 涂层热灵敏度 | ✅ 符合v3.2（首次提取） |
| `zuba2023.yaml` | GIUQZ2EE | Zuba 2023 — HCF 耦合效率极限 | ✅ 符合v3.2（首次提取） |
| `gao2025.yaml` | JAW66GYL | Gao 2025 — 循环干涉仪超低频噪声 | ✅ 符合v3.2（首次提取） |
| `ding2025.yaml` | QGLVTMB7 | Ding 2025 — ULE 玻璃空心光纤 | ✅ 符合v3.2（首次提取） |
| `shi2022.yaml` | UKBFZLXG | Shi 2022 — 温度不敏感光纤干涉仪 | ✅ 符合v3.2（首次提取） |
| `grabielle2025.yaml` | XSMPRNT3 | Grabielle 2025 — FDL 锁定噪声 | ✅ 符合v3.2（首次提取） |
| `tai2016.yaml` | FIJXUVZV | Tai 2016 — 超低 RAM EOM | ✅ 符合v3.2（首次提取） |
| `potnis2016.yaml` | WDGF2B36 | Potnis 2016 — PDH 光电探测器 | ✅ 符合v3.2（首次提取） |
| `grote2016.yaml` | VM5MJ9B3 | Grote 2016 — GW 光电探测器 | ✅ 符合v3.2（首次提取） |
| `nelson2008.yaml` | XAKCIXKT | Nelson 2008 — RIN 抑制 | ✅ 符合v3.2（首次提取） |
| `gobron2017.yaml` | HKYLIW8U | Gobron 2017 — 色散外差 SHB | ✅ 符合v3.2（首次提取） |
| `dixneuf2020.yaml` | HJZ6BVYE | Dixneuf 2020 — 365W 低 RIN 激光 | ✅ 符合v3.2（首次提取） |
| `thorpe2011.yaml` | Q2MRB267 | Thorpe 2011 — SHB 6×10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `cook2015.yaml` | KZJHGH3N | Cook 2015 — 稳态 SHB | ✅ 符合v3.2（首次提取） |
| `konz2003.yaml` | MNIZVIMG | Könz 2003 — Eu:YSO 材料参数 | ✅ 符合v3.2（首次提取） |
| `galland2020.yaml` | MPWLNUIH | Galland 2020 — 双外差 SHB | ✅ 符合v3.2（首次提取） |
| `meiser2009.yaml` | WW9ESVMK | Meiser 2009 — 超辐射 mHz 激光 | ✅ 符合v3.2（首次提取） |
| `loh2019.yaml` | UP2Q8F9Y | Loh 2019 — 布里渊激光 | ✅ 符合v3.2（首次提取） |
| `li2019.yaml` | ELKHJ5GL | Li 2019 — 光纤陀螺热噪声 | ✅ 符合v3.2（首次提取） |
| `kogelnik1966.yaml` | UQL6FYN7 | Kogelnik 1966 — 激光光束谐振腔 | ✅ 符合v3.2（首次提取） |
| `braun1995.yaml` | LY9I8I9I | Braun 1995 — SHB 锁模（实验）| ✅ 符合v3.2（首次提取） |
| `kartner1995.yaml` | 5XG8FTEE | Kärtner 1995 — SHB 锁模（理论）| ✅ 符合v3.2（首次提取） |
| `aasi2013.yaml` | 8NUIA2K7 | Aasi 2013 — LIGO 压缩光 | ✅ 符合v3.2（首次提取） |
| `adhikari2014.yaml` | FTXSM9QC | Adhikari 2014 — GW 探测综述 | ✅ 符合v3.2（首次提取） |
| `olson2019.yaml` | CDX3DFQR | Olson 2019 — RB 干涉仪 <2×10⁻¹⁶ | ✅ 符合v3.2（首次提取） |
| `huangjc2019b.yaml` | 5DCNFGX4 | Huang 2019b — 双缠绕抗振光纤盘 | ✅ 符合v3.2（首次提取） |
| `fortier2026.yaml` | BWR7TEZ6 | Fortier 2026 — 光学原子钟综述（Optica）**[框架型]** | ✅ 符合v4.0（contribution_type:framework，定义 frequency-standards 专题（光学频率标准部分）顶层架构） |
| `giunta2019.yaml` | KTHCQRJ2 | Giunta 2019 — 光学频率梳 20 年回顾**[框架型]** | ✅ 符合v4.0（contribution_type:framework，定义 optical-frequency-combs 专题顶层架构） |
| `giunta2020.yaml` | UFWLAXMA | Giunta 2020 — 10⁻²⁰ 级宽带光学频率合成（Nature Photonics）**[技术型]** | ✅ 符合v4.0（contribution_type:technical，首篇技术论文） |
| `dimarcq2024.yaml` | SDG6KXNZ | Dimarcq 2024 — SI 秒重定义路线图（Metrologia）**[框架型]** | ✅ 符合v4.0（contribution_type:framework，定义 timescales 专题顶层架构；ent.optical_frequency_standard 改为跨文件引用） |

**历史重构摘要**（v3.0 起，含 2026-04-16 的 v3.2 增补）：

### 核心改动
1. **实例节点降级**：4 个 FP 腔"独立方案"（Si 124K/17K/4K、48cm 长腔）从 Level 1 降为 Level 2（PART-OF fp_cavity_system），取消 8 条 COMPETES-WITH 关系
2. **噪声源分类**：在 ent.fp_cavity_system 中建立热噪声/振动/调制解调三个子类
3. **原理节点精简**：6 个工程推理并入父原理 condition_variables（mirror_substrate_noise_dominance、beam_radius_scaling、low_loss_substrate_improvement、shot_noise_power_efficiency_scaling、shorter_delay_line_rbs_tradeoff、pri.off_resonance_reference_light tier: meta→domain）
4. **方法层重组**（v3.0，2026-04-16 补充 RAM 决议）：新增"稳频策略"分支（meth.multi_stage_locking、meth.multi_cavity_averaging）；RAM 抑制不再单列方法节点，而并入 ent.eom 子单元接口
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
- **疑问 8（分支3 反馈执行部件）**：替换为"稳频策略"分支，EOM 归入 FP 腔调制解调子单元；RAM 抑制作为该子单元接口而非独立 meth 节点

---

## 八、综述/框架型论文处理规范（v4.0 新增）

### 8.1 两类论文的区分原则

| 维度 | 技术论文（`contribution_type: technical`） | 框架型论文（`contribution_type: framework`） |
|------|------------------------------------------|--------------------------------------------|
| 来源 | 报告具体实验结果或方法创新的原始研究论文 | 综述（review）、路线图（roadmap）、教科书章节 |
| 节点职责 | 新增 Level 2 实例节点、具体 met.* 指标值 | 定义专题 Level 0–1 顶层实体、meta/domain 原理 |
| 关系职责 | 深化某条技术链的 BOUNDED-BY/ENABLED-BY 关系 | 建立**跨专题** CONDITIONED-BY 接口关系 |
| 数值责任 | 提供首次/最佳演示值，必须附 conditions | 提供领域共识范围值；对于汇总数据须注明来源 |
| 争议/开放问题 | 实验层面的争议和未解决技术问题 | 领域方向层面的争议和战略开放问题 |
| `source_type` | `technical_paper` | `review` / `standard` / `textbook` |
| `contribution_type` | `technical` | `framework` |

> **注意**：`source_type` 和 `contribution_type` 独立使用。某些技术论文因是专题第一篇而承担部分框架角色时，可用 `contribution_type: technical`（默认），并在 `note` 中说明其"首篇"地位。

### 8.2 框架型论文的节点提取规则

**可以（鼓励）**：
1. 定义专题最顶层实体（hierarchy_level: 0 或 1），成为该专题 ID 的**权威来源**（canonical source）
2. 定义 tier: meta 或 tier: domain 的原理，特别是跨专题共用的物理机制
3. 建立跨专题 CONDITIONED-BY 关系（如光钟 CONDITIONED-BY 超稳激光）
4. 在 `open_questions` 和 `contested_claims` 中记录**领域战略级**未解问题
5. 在指标节点的 `historical_landmarks` 中系统梳理演化历程

**避免**：
1. 定义 Level 2 实例节点（如某特定实验系统的参数；这类节点应由具体技术论文定义）
2. 将综述摘要改写为 `demonstrated_value`（只有原始测量才算 `observed`，综述转述须标注 `inferred`）
3. 在关系 `source.claim` 中引用综述的转述，而非原始论文的论断

### 8.3 跨文件引用与重复定义禁令

> **全局唯一 ID 是最高准则**：同一节点 ID 只能在一个文件中**完整定义**，其他文件只引用。

当框架型论文 A（如 `dimarcq2024.yaml`）需要使用已在框架型论文 B（如 `fortier2026.yaml`）中定义的实体时：

```yaml
# dimarcq2024.yaml 中的正确写法（引用而非重复定义）
relations:
  - id: rel.D24_02
    subject: ent.optical_frequency_standard   # 跨文件引用：定义于 fortier2026.yaml
    predicate: CHARACTERIZED-BY
    object: met.optical_clock_systematic_uncertainty
    note: "跨专题引用，ent.optical_frequency_standard 定义于 topics/frequency-standards/papers/fortier2026.yaml"
```

**不允许**在 `dimarcq2024.yaml` 的 `entities:` 中再次完整定义 `ent.optical_frequency_standard`。

### 8.4 综述论文处理的典型结构

```yaml
# {Author} {Year} — {综述主题} [框架文档]
# contribution_type: framework
# 此文件是 {topic} 专题的顶层架构定义文档

meta:
  source_type: review
  contribution_type: framework
  note: >
    [综述论文] {专题名称}专题框架文档。
    定义：顶层实体 ent.xxx（Level 0/1）、核心原理 pri.xxx（meta/domain 级）、
    跨专题接口 CONDITIONED-BY 关系。
    不负责具体技术实现细节（Level 2 节点由技术论文提供）。

entities:
  # 只定义 Level 0/1 实体；不定义 Level 2 具体实现
  - id: ent.{topic_main_entity}
    hierarchy_level: 1
    ...

principles:
  # 只定义 tier: meta 或 tier: domain 的原理
  - id: pri.{domain_principle}
    tier: domain
    ...

relations:
  # 重点建立跨专题 CONDITIONED-BY 关系
  - id: rel.X##
    predicate: CONDITIONED-BY
    note: "跨专题接口：..."
```

### 8.5 当前框架型文档目录

| 文件 | 专题 | 定义的顶层实体 | 定义的核心原理 |
|------|------|--------------|-------------|
| `topics/frequency-standards/papers/fortier2026.yaml` | frequency-standards | `ent.optical_frequency_standard`（权威来源）、`ent.trapped_ion_optical_clock`、`ent.optical_lattice_clock`、`ent.nuclear_clock_229th` | `pri.quantum_projection_noise_limit`、`pri.dick_effect`、`pri.magic_wavelength_lattice` |
| `topics/optical-frequency-combs/papers/giunta2019.yaml` | optical-frequency-combs | `ent.optical_frequency_comb`（权威来源） | `pri.self_referencing_f2f`、`pri.optical_frequency_division_microwave`、`pri.frequency_ratio_measurement` |
| `topics/timescales/papers/dimarcq2024.yaml` | timescales | `ent.si_second_definition`（权威来源）| `pri.redefinition_criteria_second`、`pri.secondary_representation_si_second` |

> `time-frequency-transfer` 专题尚无框架型 YAML 文档；在首篇 framework 文档入库前，以“二、系统架构”中的统一框架描述为准，并明确将光频传递与微波传递合并到同一专题下。
