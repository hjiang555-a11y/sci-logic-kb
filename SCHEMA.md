# sci-logic-kb YAML 知识提取模式文档

> **版本**：v4.4（2026-04-21）
> **变更摘要**：v4.4 正式化论文贡献三档分级（§9.1）——`breakthrough` / `evidence` / `framework`。`evidence` 档位明确为大多数论文的合法归宿，放宽 chain-gap / orphan 要求，从源头提升信号/噪声比。同步更新 YAML 模板（§六）默认值为 `evidence`、补充向后兼容映射（§9.2）；未强制批量迁移历史 YAML 文件，改为触及时归一化。
> **上版变更（v4.3）**：v4.3 在 v4.2 基础上完成 P0 整固——新增 5 个自动化脚本（stats/lint/build_index/graph/freshness）、CI 集成（kb-lint-stats.yml）、分层 INDEX 架构（自动生成）、专题 _meta/ 目录、6 项推理就绪度量定义（§10.8）、节点粒度自检清单（§10.9）。INDEX.md 改为脚本生成，不再手工维护。
> **向后兼容**：v3.2 YAML 文件无需修改内容即可在 v4.4 下使用。历史 `contribution_type` 非规范值（`technical` / `technical_breakthrough` / `methodology` / …）按 §9.2 映射表解读，lint 不报错。新建文件应使用 `# Schema版本：v4.4`。

---

## 一、知识库定位与核心原则

### 定位

符号主义结构化知识库，服务**时间频率计量**科研全领域。
- **当前已建专题**：超稳激光（`topics/ultrastable-laser/`，78 篇论文）、光学频率梳（`topics/optical-frequency-combs/`，53 篇论文）
- **当前初建专题**：频率标准（`topics/frequency-standards/`，1 篇光钟框架综述）、时间标尺与钟组（`topics/timescales/`，1 篇）
- **专题体系**：详见 [`TOPICS.md`](TOPICS.md)
- **目标查询**：当前性能极限在哪？为什么卡在这？怎么突破？
- **不是**向量知识库，**支持**逻辑推理和精确路径查询。

### 文档同步原则（v4.5 更新：简化同步触发器）

> **`SCHEMA.md` 是唯一 Schema 真源（source of truth）。**

- 若 `README.md`、`.github/copilot-instructions.md`、`scripts/` 下自动化脚本提示词、旧 YAML 文件头注释与本文件冲突，**一律以 `SCHEMA.md` 为准**
- **更新 Schema 时，只需做两件事**（v4.5 起，取代原"同步 10 文件"要求）：
  1. 更新 `SCHEMA.md`（加版本号，补变更摘要）
  2. 重跑 `python scripts/build_index.py`（自动重建 INDEX.md / INDEX_metrics.md / INDEX_principles.md / docs/CURRENT_NODES_REFERENCE.md）
- **行为规范文件（`CLAUDE.md` / `.github/copilot-instructions.md`）** 仅在行为规范**本身**变化时才改，不随 Schema 内容更新而手工同步
- **专题级规则（`topics/<topic>/_meta/scoping_principles.md`）** 由专题维护者负责，不要求随全局 Schema 更新同步
- 追加 `LOG.md` 条目（`## [YYYY-MM-DD] schema | description`）
- 若暂未同步完成，必须在相关文件中明确标注"以 `SCHEMA.md` 为准"

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
├── 专题2：光学频率梳 ← 已建（topics/optical-frequency-combs/，53 篇，三层应用‑技术‑原理架构）
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
## 三、专题体系与演进

### 专题间关系

时间频率计量的核心技术链：

```
超稳激光 ──→ 光学频率梳 ──→ 频率标准（光学+微波）
   │              │             │
   │              │             └──→ 时间标尺
   │              │
   │              └──→ 频率标准/微波（通过梳齿分频）
   │
   └──→ 时间频率传递（统一光学/微波链路；远程比对需要相干光源与链路补偿）

时频计量数学基础 ←── 所有专题共用（表征方法、噪声模型、方差体系）
```

**关键接口**：

| 接口 | 上游专题 | 下游专题 | 核心指标 |
|------|---------|---------|---------|
| 询问激光 → 频率标准 | 超稳激光 | 频率标准 | 激光线宽、相干时间 |
| 梳齿锁定 → 频率计数 | 超稳激光 + 光学频率梳 | 频率标准/比对 | 梳齿相位噪声 |
| 时间频率传递链路 → 远程比对 | 超稳激光 + 光学频率梳 | 时间频率传递 | 链路不稳定度、补偿残差 |
| 光-微波分频 → SI 秒 | 光学频率梳 | 频率标准/微波 | 分频噪声贡献 |
| 数学基础 → 性能表征 | 时频计量数学基础 | 所有专题 | Allan 偏差、噪声谱密度、相位抖动 |

---


### 各专题状态

| 编号 | 专题 | 目录 | 状态 | 论文数 | 核心节点数(估) |
|------|------|------|------|--------|---------------|
| 1 | 超稳激光 | `topics/ultrastable-laser/` | ✅ 已建（78/78 YAML，全部升级为 ✅ v4.1） | 78 | ~200+ |
| 2 | 光学频率梳 | `topics/optical-frequency-combs/` | ✅ 已建（应用‑技术‑原理三层框架） | 53 | 见各论文 |

### 光学频率梳专题内部结构（重构后）

基于专家反馈，光学频率梳专题按 **应用‑技术‑原理** 三层重构，消除按波段划分造成的语义重叠：

```
光学频率梳专题
├── **应用层**（面向科学测量任务）
│   ├── 频率梳光谱学（广义，含六大方法）
│   │   ├── 双梳光谱（DCS，多外差检测）
│   │   ├── 直接梳光谱（双光子激发）
│   │   ├── Ramsey‑comb 光谱（脉冲对干涉）
│   │   ├── 色散光谱仪 + 梳（VIPA 交叉色散）
│   │   ├── 傅里叶变换光谱 + 梳（腔增强）
│   │   └── 非线性梳光谱（相干 Raman、泵浦‑探测）
│   └── 频率计量应用（光学频率合成、精密测频）
│
├── **技术层**（梳源实现方案）
│   ├── 传统锁模激光器梳（飞秒激光器）
│   ├── 微腔光学频率梳（DKS、参量四波混频）
│   ├── 电光调制梳（EOM‑based）
│   ├── 量子级联激光梳
│   └── **非线性光谱展宽技术**（按光谱波段）
│       ├── 中红外梳产生（DFG、OPO、直接锁模）
│       ├── 可见/紫外梳产生（谐波产生）
│       └── THz 梳产生（差频、光电导天线）
│
└── **原理层**（跨专题通用物理机制）
    ├── 非线性频率转换原理（DFG、OPO、SHG）
    ├── 参量四波混频原理（Kerr 非线性）
    ├── 分子振转指纹光谱原理（中红外特异性）
    └── 多外差检测原理（双梳光谱基础）
```

**重构要点**：

1. **合并应用层重复**：`双梳光谱学`（coddington2016）是`频率梳光谱学`（picque2019）的子类，统一在应用层描述
2. **消除波段独立子域**：`中红外梳光谱`（schliesser2012）不再作为独立子域，其内容按性质拆分：
   - 应用部分（中红外分子光谱）→ 应用层（频率梳光谱学）
   - 技术部分（DFG/OPO 产生方案）→ 技术层（非线性光谱展宽技术）
   - 原理部分（非线性频率转换）→ 原理层
3. **建立普世原理层**：非线性光学原理（OPO、DFG 等）具有跨专题普适性，从技术描述中剥离，便于共享引用

**已入库论文在新框架中的定位**：

| 论文 | 原分类 | 新定位 |
|------|--------|--------|
| `giunta2019.yaml` | 专题框架 | 总览/框架（跨层） |
| `udem2002.yaml` | 奠基文献 | 总览/框架（跨层） |
| `coddington2016.yaml` | 双梳光谱框架 | 应用层（频率梳光谱学子类） |
| `picque2019.yaml` | 频率梳光谱分类 | 应用层（频率梳光谱学总纲） |
| `schliesser2012.yaml` | 中红外子域 | 拆分：应用+技术+原理 |
| `kippenberg2011/2018.yaml` | 微腔梳 | 技术层（微腔光学频率梳） |
| `giunta2020.yaml` | 技术论文 | 技术层（相位追踪技术） |

**下一步梳理原则**：
1. 新入库论文按应用‑技术‑原理三层明确归类
2. 跨专题共享原理移至 `topics/shared/principles/`
3. 波段特性作为技术/应用的属性字段，而非独立类别

---
| 3 | 频率标准 | `topics/frequency-standards/` | 🚧 初建（1篇光钟框架综述；微波部分待建） | 1 | ~10 |
| 4 | 时间频率传递 | `topics/time-frequency-transfer/` | 📋 待建 | — | — |
| 5 | 时间标尺与钟组 | `topics/timescales/` | 🚧 初建（仅框架） | 1 | ~8 |
| M | 时频计量数学基础 | `topics/shared/metrics/` | 📋 待建（跨专题共享模块） | — | — |

---


### 建设优先级建议

> 当前已入库的下游专题中，`giunta2019.yaml`、`fortier2026.yaml`、`dimarcq2024.yaml` 的主要作用都是定义专题顶层架构和跨专题接口；其中光学频率梳专题已进一步扩展到多篇框架综述与技术论文，不应与"仅有框架骨架"的专题混淆。

### 第一梯队（与超稳激光耦合最紧密）

1. **光学频率梳**：超稳激光的直接下游；梳齿相位噪声直接影响频率标准性能。
   - **当前状态**：已建立应用‑技术‑原理三层完整框架（8篇论文）
   - **应用层**：频率梳光谱学总纲（picque2019） + 双梳光谱学子类（coddington2016）
   - **技术层**：微腔梳（kippenberg2011/2018）、非线性展宽技术（schliesser2012 技术部分）
   - **原理层**：非线性频率转换原理、分子光谱原理（schliesser2012 原理部分）
   - **下一步重点**：按三层框架填充具体技术论文，重点补充非线性展宽技术实例（DFG/OPO 实验）
2. **频率标准**：超稳激光的主要应用场景；询问激光线宽是当前限制之一。光学频率标准部分已有框架，微波频率标准部分待建。


    
### 当前重点：强化问题-解决方案-结果推理链条
为提升知识库的科研推理能力，当前重点任务是对已入库论文进行系统性梳理，显式提取和嵌入以下推理元素：

1. **问题识别**：通过 `BOUNDED-BY` 关系清晰定义技术限制，通过 `open_questions` 字段记录未解问题
2. **解决方案追踪**：通过 `breakthrough_paths` 字段记录已验证或待验证的突破路径
3. **结果验证**：通过 `verification_status`、`temporal_role` 和 `status` 字段追踪解决方案的证据状态
4. **证据溯源**：确保每个论断都有可追溯的 `source` 引用

**首轮梳理对象**：超稳激光专题（78篇论文），将按照重新梳理的关键技术架构进行组织。### 第二梯队

3. **时间频率传递**：统一光频传递、微波传递与授时链路，是远程频率标准比对和跨实验室溯源的必要环节
4. **时频计量数学基础**：Allan 偏差族、噪声谱密度、相位抖动等数学工具是所有专题共用的基础，独立梳理有助于统一表征体系

### 第三梯队

5. **时间标尺与钟组**：顶层应用

---


### 跨专题节点共享规则

### 5.1 通用原理

某些物理原理跨越多个专题，例如：
- Allan 偏差（表征方法）→ 所有专题（归入时频计量数学基础模块）
- 散粒噪声极限 → 超稳激光 + 频率标准 + 频率梳
- Dick 效应 → 频率标准 + 超稳激光

**处理方式**：若同一原理在不同专题中的公式形式、主导变量、工程含义明显不同，各专题保留独立 `pri.*` 节点（遵循跨分支原理隔离原则）。若确实是同一原理的同一表达，则在 `shared/` 目录中定义一次，各专题引用。

### 5.2 共享节点目录

```
topics/
├── shared/                          # 跨专题共享节点
│   ├── principles/                  # 通用物理原理
│   └── metrics/                     # 时频计量数学基础（Allan 偏差、噪声谱密度等）
├── ultrastable-laser/               # 专题1（已建）
│   └── papers/
├── optical-frequency-combs/         # 专题2（已建）
│   └── papers/
├── frequency-standards/             # 专题3（初建，合并光钟+微波标准）
│   └── papers/
├── time-frequency-transfer/         # 专题4（待建）
│   └── papers/
├── timescales/                      # 专题5（初建）
│   └── papers/
└── ...
```

### 5.3 跨专题引用规范

```yaml
object: pri.shot_noise_frequency_limit
note: "跨专题引用，定义于 topics/ultrastable-laser/papers/drever1983.yaml"
```

---


### 演进原则

1. **渐进扩展**：保持一个主专题深耕，同时允许下游专题先以少量代表论文预热
2. **Schema 复用**：所有专题共用同一 SCHEMA.md 中的节点类型、关系类型和质量要求
3. **架构适配**：SCHEMA.md 中的"系统架构"部分按专题分区描述
4. **现有内容不破坏**：超稳激光的 78 篇论文 YAML 内容不变，仅调整存放路径
5. **向前兼容**：新专题的节点 ID 避免与已有专题冲突，通过前缀或命名空间区分


## 四、五类节点

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

## 五、九种关系类型

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
| `SHARED-WITH` (v4.5+) | subject 与 object 是跨专题同一机制的锚定 | `pri.local_hcf_thermal_noise SHARED-WITH pri.brownian_thermal_noise_fdt` |

> **废弃**：`GOVERNED-BY`（已拆分为 ENABLED-BY + BOUNDED-BY）、`EQUIVALENT-IN-CONTEXT`（用共同 ENABLED-BY 表达）、`SUPPORTED-BY`（用 temporal_role 字段表达）、`BREAKTHROUGH-VIA`（已内化为原理节点的 `condition_variables` 字段）

### 4.2 BOUNDED-BY 完整结构（最重要）

```yaml
- id: rel.X##
  subject: {node_id}
  predicate: BOUNDED-BY
  object: {pri.limiting_principle}
  confidence: established
  source: {zotero_key: "KEY", claim: "原文论断"}

  # 限制状态（v4.2 规范字段）
  is_system_limit: true           # 当前条件下是否为主动瓶颈
  dominated_by: null              # 若 false，填写压制它的原理 ID
  quantitative_contribution: "84%"  # 占总限制的比例（如已知）
  regime: all                     # all | short-term | long-term | during-sweep

  # 限制状态枚举（v4.5+，与 breakthrough_paths.status 联动）
  # active      — 当前条件下主动瓶颈（等价 is_system_limit: true）
  # conditional — 被另一原理压制，条件变化会回归（等价 dominated_by 非空）
  # resolved    — 已被工程路径突破并退出极限序列（需填 resolved_by）
  # refuted     — 论断被后续实验证伪
  # 未填则视为 unknown（历史数据兼容），lint 不强制。
  limit_status: active
  resolved_by: null               # 仅 limit_status=resolved 时必填：
                                  # 列表，条目必须是 pri.* 或 meth.* 节点 ID
  resolution_source: null         # 仅 limit_status=resolved 时建议填：
                                  # {zotero_key: "...", claim: "原文论断"}

  # 认识论状态（Feynman 原则）
  verification_status: observed   # observed | calculated | inferred
  temporal_role: validates        # proposes | validates | refutes | extends

  # 突破路径（可选但鼓励）——问题-解决方案-结果推理链条的核心
  breakthrough_paths:
    - direction: pri.new_principle          # 必须引用 pri.* 或 meth.* 节点
      expected_gain: "预期性能提升描述"
      expected_σy_gain: null                # v4.4+ 超稳激光专题可选
                                            # 明确该路径对 σ_y(τ=1 s) 的影响
                                            # (例如："mod σ_y: 4×10⁻¹⁷ → 1×10⁻¹⁷")
                                            # 非 σ_y 相关路径填 "indirect" 并在 note 说明
      status: proposed                      # proposed | demonstrated | refuted
      source: {zotero_key: "KEY", claim: "原文论断"}
      note: "可选的补充说明"
    # 可添加多个突破路径，每个代表一个潜在的解决方案方向
```

> **突破路径**在 BOUNDED-BY 关系的 `breakthrough_paths` 字段中写，`direction` 必须引用 `pri.*` 或 `meth.*` 节点（不得引用 `ent.*`）。

> **v4.5+ `limit_status` 联动规则**：当某条 `breakthrough_paths[].status == "demonstrated"` 时，其所属的 BOUNDED-BY 关系**建议**同步将 `limit_status` 从 `active` 改为 `resolved` 并补 `resolved_by`。lint 在发现该情况但 `limit_status` 仍为非 `resolved|refuted` 时发出 INFO-级 nudge（不阻塞）。`scripts/migrate_bounded_status.py` 可做批量初始推断。
>
> **新指标 `limit_resolution_rate`**：`scripts/stats.py` 基于 `limit_status` 新增一项"极限突破闭环率" `resolved / (active + resolved)`，补充原有 `reasoning_chain_closure`，量化"已突破 vs 仍卡死"。

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

### 4.5 SHARED-WITH 结构（跨专题公共机制锚定，v4.5+）

> **定位**：`SHARED-WITH` 是第 9 种谓词，**仅**用于显式声明"本专题的这个原理/方法，与某个跨专题公共节点是同一机制"。它不替代 `DERIVED-FROM` / `PART-OF` / `ENABLED-BY`，而是为**跨专题叙事**提供清晰锚点。

**触发条件（必要且充分）**：

1. `object` 必须是登记在 [`topics/shared/registry.md`](topics/shared/registry.md) **§3 Tier 2 段**的 domain-level 公共节点（即事实上被 ≥ 2 个**不同专题**的论文引用）
2. `subject` 必须与 `object` 的主页文件分属**不同专题目录**（`topics/<A>/` vs `topics/<B>/`；同专题复用走 Tier 1 隐式引用即可）
3. `subject` 与 `object` 必须同为 `pri.*` 或 `meth.*`（不用于 `ent.*` / `met.*` — 这些走 `CONDITIONED-BY` / `OPERATIONALIZED-AS`）

**方向**：`local_node SHARED-WITH shared_node`（单向，本地指向公共节点）。

**结构**：

```yaml
- id: rel.X##
  subject: pri.local_variant_or_anchor       # 本专题内的原理/方法（可以是 paper-local 节点）
  predicate: SHARED-WITH
  object: pri.brownian_thermal_noise_fdt     # 必须出现在 registry.md §3 Tier 2 表
  confidence: established
  source: {zotero_key: "KEY", claim: "原文论断（说明跨专题借用语义）"}
  note: "跨专题锚定：说明 subject 在本专题的体现与 shared 节点的物理对应关系"
```

**lint 规则**（`scripts/lint.py`，v4.5+）：

| 违规 | 级别 | 说明 |
|------|------|------|
| `SHARED-WITH.object` 不在 `registry.md §3 Tier 2` | ERROR | 防止滥用；若确需扩展 Tier 2，应先补 registry |
| `subject` 与 `object.defining_file` 属同一专题目录 | WARNING | 同专题复用应降级为 Tier 1 隐式引用 |
| `subject` / `object` 不是 `pri.*` / `meth.*` | ERROR | 实体/指标不用此谓词 |

**关键原则**：SHARED-WITH 应**稀有、显式、有溯源**。不追求数量——目标是为跨专题"公共机制"提供 navigable 锚点，不是补丁式连接谓词。

---

## 六、YAML 文件完整模板

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
  contribution_type: evidence    # breakthrough | evidence | framework（v4.4 三档规范，见第九节）
                                 # breakthrough: 打破指标记录 / 提出新原理 / 证伪旧论断
                                 # evidence:    在已有节点上提供新数据点、复现、工程改进（大多数论文属此档）
                                 # framework:   综述 / 路线图 / 教科书章节（定义顶层架构，见第九节）
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
    role: primary                       # v4.4+ 可选，超稳激光专题强烈建议
                                        # primary | secondary | engineering | enabling | interface
                                        # 详见 topics/ultrastable-laser/_meta/scoping_principles.md v2
                                        # 若省略，build_index.py / lint.py / stats.py 按 ID/name 启发式推断
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

## 七、提取质量要求

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

## 八、已处理论文

> **详细论文列表已迁移至 [`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md)**。本节仅保留统计摘要。

### 各专题论文统计

| 专题 | 论文总数 | 框架型 | 技术型 | Schema 版本 | 最近处理日期 |
|------|---------|-------|-------|------------|-------------|
| 超稳激光 | 78 | 0 | 78 | 全部 ✅ v4.1 | 2026-04-17 |
| 光学频率梳 | 61 | 4 | 57 | 全部 ✅ v4.1 | 2026-04-19 |
| 频率标准 | 1 | 1 | 0 | ✅ v4.0 | 2026-04-16 |
| 时间标尺 | 1 | 1 | 0 | ✅ v4.0 | 2026-04-16 |
| **合计** | **141** | **6** | **135** | | |

### 核心文档导航

- **完整论文列表与历史重构记录**：[`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md)
- **全局导航索引**：[`INDEX.md`](INDEX.md)
- **演化日志**：[`LOG.md`](LOG.md)

---

## 九、论文贡献分级与框架型论文处理规范（v4.4 更新）

### 9.1 三档贡献分级（v4.4 新增）

> **动机**：时间频率计量领域的关键比较指标清晰（σ_y、linewidth、accuracy、SWaP…），绝大多数论文只是在已有坐标轴上提供新数据点。此前把"技术论文"和"框架论文"二分粗暴对称，导致 evidence 级论文被要求补完整限制链，催生大量 chain-gap / orphan 假缺口。v4.4 明确三档分级。

| 档位 | 典型贡献 | 节点责任 | 最低入库要求 |
|------|---------|---------|-------------|
| `breakthrough` | 打破指标记录 / 提出新原理 / 证伪旧论断 | 可新增 pri.*、配套 `breakthrough_paths`、刷新 `historical_landmarks.best_demonstration` | 完整限制链、`source.claim`、条件变量；若挑战既有论断须补 `contested_claims` |
| `evidence` | 在已有节点上提供新数据点、新条件验证、工程复现 | 仅挂钩到已有 ent/pri/meth/met，必要时新增 Level 2 实例节点；**不强求新增 pri.*** | 至少 1 条关系的 `subject` 或 `object` 指向已有节点（跨文件引用 OK）+ 1 个 `demonstrated_value`（带 `conditions`）+ `source.claim` |
| `framework` | 综述 / 路线图 / 教科书章节 | 定义 Level 0/1 顶层实体、tier: meta/domain 原理、跨专题 CONDITIONED-BY 接口 | 不定义具体参数实例；领域共识值须标注 `verification_status: inferred` |

**设计含义**：
- 大多数论文是 `evidence` 级，这是合理状态，不是缺陷
- `evidence` 级论文**允许** orphan / chain-gap 的存在——它们是该档位的正常形态，不应计入缺口指标
- `breakthrough` 级论文必须走完整 checklist（[CONTRIBUTING.md](CONTRIBUTING.md) Step 1–10）
- `framework` 级论文规则见 §9.3–9.5

### 9.2 向后兼容映射（v4.4 新增）

v4.3 及以前的 YAML 文件里出现过的非规范值按下表解读（不做批量迁移，以 lint / 后续 PR 逐步归一化）：

| 历史值 | 归一化为 | 说明 |
|--------|---------|------|
| `technical` | `evidence`（默认）或 `breakthrough`（若论文 note 明确提到"首次 / 打破记录 / 提出新原理"） | 最常见的遗留值 |
| `technical_breakthrough` | `breakthrough` | 直接映射 |
| `principle_validation` | `breakthrough` | 原理首次验证 |
| `methodology` / `technique` / `experimental_demonstration` | `evidence` | 方法或装置级的演示/改进 |
| `framework` | `framework` | 不变 |

> **原则**：新建 YAML 必须使用三档规范值之一；旧文件在被专家触及时按上表归一化，不做大规模脚本迁移（避免改动签名影响 git blame）。

### 9.3 框架型 vs 技术型（breakthrough+evidence）的区分原则

| 维度 | 技术论文（`breakthrough` / `evidence`） | 框架型论文（`framework`） |
|------|--------------------------------------|--------------------------|
| 来源 | 报告具体实验结果或方法创新的原始研究论文 | 综述（review）、路线图（roadmap）、教科书章节 |
| 节点职责 | 新增 Level 2 实例节点、具体 met.* 指标值 | 定义专题 Level 0–1 顶层实体、meta/domain 原理 |
| 关系职责 | 深化某条技术链的 BOUNDED-BY/ENABLED-BY 关系 | 建立**跨专题** CONDITIONED-BY 接口关系 |
| 数值责任 | 提供首次/最佳演示值，必须附 conditions | 提供领域共识范围值；对于汇总数据须注明来源 |
| 争议/开放问题 | 实验层面的争议和未解决技术问题 | 领域方向层面的争议和战略开放问题 |
| `source_type` | `technical_paper` | `review` / `standard` / `textbook` |
| `contribution_type` | `breakthrough` 或 `evidence` | `framework` |

> **注意**：`source_type` 和 `contribution_type` 独立使用。某些技术论文因是专题第一篇而承担部分框架角色时，可用 `contribution_type: breakthrough`（不是 `framework`），并在 `note` 中说明其"首篇"地位。

### 9.4 框架型论文的节点提取规则

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

### 9.5 跨文件引用与重复定义禁令

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

### 9.6 综述论文处理的典型结构

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

### 9.7 当前框架型文档目录

| 文件 | 专题 | 定义的顶层实体 | 定义的核心原理 |
|------|------|--------------|-------------|
| `topics/frequency-standards/papers/fortier2026.yaml` | frequency-standards | `ent.optical_frequency_standard`（权威来源）、`ent.trapped_ion_optical_clock`、`ent.optical_lattice_clock`、`ent.nuclear_clock_229th` | `pri.quantum_projection_noise_limit`、`pri.dick_effect`、`pri.magic_wavelength_lattice` |
| `topics/optical-frequency-combs/papers/giunta2019.yaml` | optical-frequency-combs | `ent.optical_frequency_comb`（权威来源） | `pri.self_referencing_f2f`、`pri.optical_frequency_division_microwave`、`pri.frequency_ratio_measurement` |
| `topics/timescales/papers/dimarcq2024.yaml` | timescales | `ent.si_second_definition`（权威来源）| `pri.redefinition_criteria_second`、`pri.secondary_representation_si_second` |

> `time-frequency-transfer` 专题尚无框架型 YAML 文档；在首篇 framework 文档入库前，以“二、系统架构”中的统一框架描述为准，并明确将光频传递与微波传递合并到同一专题下。

---

## 十、知识库运维操作（v4.2 新增）

> **设计理念**：受 Karpathy "LLM Wiki" 模式启发，在保持 YAML 符号主义架构核心优势的基础上，叠加面向人类可读性和 AI 可维护性的运维基础设施。YAML 是 source of truth（事实层），Markdown 文件（INDEX.md、LOG.md、synthesis/）是 derived view（导航/综合层）。

### 10.1 三层架构

```
Raw Sources（原始文献，Zotero 管理）
  ↓ Ingest
YAML 节点图（source of truth，topics/*/papers/*.yaml）
  ↓ Derive
运维层（INDEX.md / LOG.md / synthesis/ / PROCESSED_PAPERS.md）
```

### 10.2 Ingest（摄入）

当前流程：论文 PDF → YAML 提取 → 提交（已成熟）。

**新增要求**：
1. 摄入后运行 `python scripts/build_index.py` 重新生成分层 INDEX 文件
2. 摄入后**必须**追加 [`LOG.md`](LOG.md) 条目（格式：`## [YYYY-MM-DD] ingest | description`）
3. 若新论文的数据与已有声明矛盾，必须：
   - (a) 更新原有节点的 `contested_claims` 或 `open_questions`
   - (b) 若存在相关综合页面（`synthesis/`），标注为"需要更新"
   - (c) 在 LOG.md 中记录类型为 `contradiction`

### 10.3 Query（查询反哺）

当对知识库的查询产生有价值的跨论文综合分析时：

1. **应**将结果存为 `topics/<topic>/synthesis/` 目录下的 Markdown 页面
2. 综合页面头部必须注明：
   - `最后更新`：日期
   - `涉及源文件`：YAML 文件列表
   - `状态`：🟢 当前 / 🟡 需要更新 / 🔴 过时
3. 综合页面**不替代** YAML 节点（YAML 仍是事实真源）
4. 查询结果写入综合页面后，在 LOG.md 中记录类型为 `query` 或 `synthesis`

### 10.4 Lint（健康检查）

**触发条件**：每 20 篇论文入库或每次 Schema 升级后运行。

**检查项目**：

| 检查类型 | 描述 | 严重度 |
|---------|------|--------|
| 孤立节点 | 无任何关系引用的节点 | ⚠ 警告 |
| 悬空引用 | 引用了不存在的节点 ID | ❌ 错误 |
| 数值矛盾 | 同一指标在不同文件中的值不一致（非 `contested_claims`） | ⚠ 警告 |
| 陈旧声明 | `best_demonstration` 已被新论文超越但未更新 | ⚠ 警告 |
| 缺失字段 | BOUNDED-BY 缺少 `breakthrough_paths` | ⚠ 警告 |
| 跨专题接口完整性 | CONDITIONED-BY 是否有对应的 `interface_metric` | ⚠ 警告 |
| 综合页面过期 | 综合页面 `covers_papers_up_to` 早于最新 ingest | ℹ 提示 |

**执行方式**：`python scripts/lint.py`（CI 中自动运行，见 `.github/workflows/kb-lint-stats.yml`）。`--strict` 模式将 warnings 视为 errors。

### 10.5 文件职责矩阵

| 文件 | 职责 | 更新频率 | 维护方 |
|------|------|---------|-------|
| `SCHEMA.md` | 规范定义（source of truth） | Schema 升级时 | 人类审核 + AI 起草 |
| `INDEX.md` | 全局导航索引 | 每次 ingest（`build_index.py` 自动生成） | **脚本生成** |
| `INDEX_metrics.md` | 跨专题指标快查 | 每次 ingest（`build_index.py` 自动生成） | **脚本生成** |
| `INDEX_principles.md` | 跨专题原理快查 | 每次 ingest（`build_index.py` 自动生成） | **脚本生成** |
| `topics/*/INDEX.md` | 各专题详表 | 每次 ingest（`build_index.py` 自动生成） | **脚本生成** |
| `LOG.md` | 演化日志 | 每次变更 | AI 自动追加 |
| `PROCESSED_PAPERS.md` | 论文详细列表 | 每次 ingest | AI 自动更新 |
| `topics/*/papers/*.yaml` | 知识节点（source of truth） | 论文入库时 | AI 提取 + 人类审核 |
| `topics/*/synthesis/*.md` | 跨论文综合视图 | 定期或 query 后 | AI 生成 + 人类审核 |
| `TOPICS.md` | 专题架构索引 | 专题变更时 | AI 更新 |
| `CLAUDE.md` | AI 行为规范 | 工作流变更时 | 人类定义 |

### 10.6 人机协作原则

> **核心理念**（inspired by Karpathy LLM Wiki）：人做策展与提问，AI 做簿记与维护。

**人类角色（Domain Expert）**：
- 选择论文（sourcing）
- 确认节点边界判断（"这是新实体还是参数变体？"）
- 审核争议性论断（contested claims resolution）
- 提出探索性问题（"为什么 17K 比 4K 的镀层损耗更低？"）
- 审核综合页面的准确性
- 决定 Schema 升级方向

**AI 角色（Knowledge Engineer）**：
- YAML 节点提取与维护（ingest）
- 跨文件交叉引用维护（cross-referencing）
- INDEX.md / LOG.md / PROCESSED_PAPERS.md 自动更新（bookkeeping）
- 综合页面生成与更新（synthesis）
- 健康检查与修复建议（lint）
- 新论文与已有知识的矛盾检测（consistency check）
- 新论文入库后自动标记受影响的综合页面为"需要更新"

### 10.7 自动化工具链（P0 整固阶段产物）

以下脚本位于 `scripts/` 目录，均支持 `--repo-path` 参数，可在 CI 中运行。

| 脚本 | 用途 | CI 集成 |
|------|------|---------|
| `stats.py` | 6 项推理就绪度量 + 库存统计 | ✅ `kb-lint-stats.yml` |
| `lint.py` | 11 项健康检查（孤立节点、悬空引用、重复、推理链缺口等） | ✅ `kb-lint-stats.yml` |
| `build_index.py` | 从 YAML 自动生成分层 INDEX 文件 | 手动或 ingest 后运行 |
| `graph.py` | 知识图谱导出（JSON/GraphML）+ hub/orphan/bridge 诊断 | 手动 |
| `freshness.py` | 综合页面新鲜度追踪 | ✅ `kb-lint-stats.yml` |

**使用规范**：
- `build_index.py` 生成的 INDEX 文件以 `<!-- AUTO-GENERATED -->` 标记，人不应手动编辑
- `lint.py --strict` 在 CI 中运行时，warnings 也视为 errors
- `stats.py --json` 输出可被其他脚本消费（如月度报告生成器）

### 10.8 推理就绪度量（Reasoning Readiness Metrics）

这 6 项指标是知识库"逼近专家"的唯一进度条，由 `stats.py` 计算：

| # | 度量 | 公式 | 目标 | 含义 |
|---|------|------|------|------|
| 1 | **限制链闭环率** | (有 breakthrough_paths 的 BOUNDED-BY) / (全部 BOUNDED-BY) | ≥70% | "知道什么限制了性能" 且 "知道怎么突破" |
| 2 | **证据覆盖率** | (有 source.claim 的 relations) / (全部 relations) | ≥90% | 每条关系都有原文依据 |
| 3 | **条件完备率** | (有 conditions/preconditions/invalidated_when 的 principles) / (全部 principles) | ≥80% | 原理不是无条件成立的 |
| 4 | **跨文件复用度** | (在 ≥2 文件出现的 node ID) / (全部 unique ID) | 越高越好 | 知识在复合增长 |
| 5 | **综合页面覆盖** | 有 synthesis/ 的专题数 / 有论文的专题数 | 全覆盖 | 每个专题都有跨论文综合分析 |
| 6 | **矛盾可见度** | contested_claims 总数 + open_questions 总数 | 越多越好 | 知识库敢于存疑 |

### 10.9 节点粒度自检清单（Node Granularity Checklist）

在创建新节点前，AI 应自检以下条件。满足 ≥2 条的建为独立节点，否则并入父节点字段：

- [ ] **能独立回答有意义的边界问题**（"什么条件下 X 是性能瓶颈？"）
- [ ] **有独立设计选择空间**（材料、几何、方法可独立优化）
- [ ] **会被 ≥2 篇论文复用引用**
- [ ] **拥有独立的限制链**（BOUNDED-BY）或证据链或竞争关系（COMPETES-WITH）
- [ ] **在不同条件下，其"是否为限制因素"的状态会变化**

若全不满足 → 并入父节点的字段（如 `condition_variables`、`key_parameters`）。

### 10.10 分层索引架构

INDEX 文件由 `build_index.py` 自动生成，结构如下：

```
INDEX.md                        ← 总览/跳转页（专题表、节点汇总、BOUNDED-BY 链）
├── topics/<topic>/INDEX.md     ← 各专题详表（实体/原理/方法/指标 + 限制链 + 跨专题引用）
├── INDEX_metrics.md            ← 跨专题指标快查（最佳值、条件、来源）
└── INDEX_principles.md         ← 跨专题原理快查（按 tier 分组）
```

**规则**：所有 INDEX 文件头部含 `<!-- AUTO-GENERATED -->` 标记，**人不应手动编辑**。需要修改时修改 YAML source of truth 后重新运行 `build_index.py`。

### 10.11 专题元数据目录

每个专题目录下的 `_meta/` 存放该专题的架构级文档：

```
topics/<topic>/_meta/
├── architecture.md  ← 专题内部架构图、核心限制链、路线图
└── (未来: roadmap.md, boundary_questions.md)
```

这些文件由人类审核，不是自动生成的。
