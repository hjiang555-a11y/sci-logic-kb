# 知识库全局导航索引

> **自动维护说明**：本文件是知识库的全局导航入口，由 AI 在每次 Ingest 后更新。
> YAML 文件仍是 source of truth（事实层），本文件是 derived view（导航层）。
>
> **最后更新**：2026-04-20
> **Schema 版本**：v4.1

---

## 一、专题概览

| 编号 | 专题 | 目录 | 状态 | 论文数 | 节点数 | 关系数 |
|------|------|------|------|--------|--------|--------|
| 1 | **超稳激光** | `topics/ultrastable-laser/` | ✅ 已建（重点梳理中） | 78 | ~337 (50 ent + 78 pri + 78 meth + 131 met) | 318 |
| 2 | **光学频率梳** | `topics/optical-frequency-combs/` | ✅ 已建 | 61 | ~456 (98 ent + 131 pri + 60 meth + 167 met) | 544 |
| 3 | **频率标准** | `topics/frequency-standards/` | 🚧 初建 | 1 | ~21 | — |
| 4 | **时间频率传递** | `topics/time-frequency-transfer/` | 📋 待建 | 0 | — | — |
| 5 | **时间标尺与钟组** | `topics/timescales/` | 🚧 初建 | 1 | ~12 | — |
| M | **时频计量数学基础** | `topics/shared/metrics/` | 📋 待建 | — | — | — |

**总计**：~141 篇论文，~826 节点，~862 关系

---

## 二、核心实体节点清单（Level 0–1）

### 超稳激光专题

| 节点 ID | 名称 | 层级 | 定义文件 |
|---------|------|------|---------|
| `ent.fp_cavity_system` | 刚性 F-P 参考腔系统 | Level 1 | `numata2004.yaml` |
| `ent.fiber_interferometer` | 光纤迈克尔逊干涉仪 | Level 1 | `jiang2010.yaml` |
| `ent.shb_eu_yso_reference_l13` | SHB 光谱烧孔频率参考 | Level 1 | `leibrandt2013.yaml` (WK9QLCGF) |
| `ent.superradiant_laser_m09` | 超辐射 mHz 激光 | Level 1 | `meiser2009.yaml` |
| `ent.brillouin_fiber_laser_l19` | 布里渊光纤激光 | Level 1 | `loh2019.yaml` |
| `ent.self_balancing_long_cavity_h15` | 48 cm 自平衡 ULE 长腔 | Level 1 | `hafner2015.yaml` |

**FP 腔 Level 2 实例**（PART-OF `ent.fp_cavity_system`）：

| 节点 ID | 描述 | 关键参数 |
|---------|------|---------|
| `ent.si_crystal_fp_cavity_k12` | 124K Si 腔 | mod σ_y ≈ 1×10⁻¹⁶ (Kessler 2012) |
| `ent.si_crystal_17k_fp_cavity_l26` | 17K Si 腔 + AlGaAs 镀层 | mod σ_y = 2.5×10⁻¹⁷ (Lee 2026, 世界纪录) |
| `ent.si_crystal_fp_cavity_4k_r19` | 4K Si 腔 | 热噪声极限验证 (Robinson 2019) |
| `ent.si_crystal_fp_cavity_sub5k_c25` | sub-5K 10cm Si 腔 | 10⁻¹⁷ 级 (Chen 2025) |

### 光学频率梳专题

| 节点 ID | 名称 | 层级 | 定义文件 |
|---------|------|------|---------|
| `ent.optical_frequency_comb` | 光学频率梳（权威顶层） | Level 1 | `giunta2019.yaml` |
| `ent.microresonator_frequency_comb` | 微腔光学频率梳 | Level 1 | `kippenberg2018.yaml` |
| `ent.electro_optic_frequency_comb` | 电光调制梳 | Level 1 | `giunta2019.yaml` |
| `ent.dual_comb_spectrometer` | 双梳光谱仪 | Level 1 | `coddington2016.yaml` |
| `ent.mid_ir_frequency_comb` | 中红外频率梳 | Level 1 | `schliesser2012.yaml` |

### 频率标准专题

| 节点 ID | 名称 | 层级 | 定义文件 |
|---------|------|------|---------|
| `ent.optical_frequency_standard` | 光学频率标准（权威顶层） | Level 1 | `fortier2026.yaml` |
| `ent.trapped_ion_optical_clock` | 囚禁离子光钟 | Level 2 | `fortier2026.yaml` |
| `ent.optical_lattice_clock` | 光晶格钟 | Level 2 | `fortier2026.yaml` |
| `ent.nuclear_clock_229th` | ²²⁹Th 核钟 | Level 2 | `fortier2026.yaml` |

### 时间标尺专题

| 节点 ID | 名称 | 层级 | 定义文件 |
|---------|------|------|---------|
| `ent.si_second_definition` | SI 秒定义（权威顶层） | Level 1 | `dimarcq2024.yaml` |

---

## 三、关键指标——当前最佳值快查表

### 超稳激光稳定度记录

| 指标 | 当前最佳值 | 来源 | 条件 |
|------|----------|------|------|
| **分数频率不稳定度** | mod σ_y = **2.5×10⁻¹⁷** | Lee 2026 | 17K Si 腔 + AlGaAs 晶体镀层，双腔平均 |
| 分数频率不稳定度 (单腔) | mod σ_y = 4×10⁻¹⁷ | Matei 2017 | 124K Si 腔，IBS 镀层极限 |
| **激光线宽** | **5–10 mHz** | Matei 2017 | Si2-Si3 拍频 |
| 光学相干时间 | 11 s (Ramsey) / 55 s (回溯) | Matei 2017 | Si 腔 |
| 腔存储时间 | 300 μs | Parke 2025 | 68 cm 长腔 |
| 加速度灵敏度 | < 10⁻¹²/g | Leibrandt 2013 | 惯性力前馈 |
| 光纤锁频稳定度 | 6.3×10⁻¹⁵ @ 16 ms | Jeon 2025 | 自零差，4–200 Hz 热噪声极限 |

### 光学频率梳关键指标

| 指标 | 当前最佳值 | 来源 |
|------|----------|------|
| 光频合成精度 | 10⁻²⁰ 级 | Giunta 2020 |
| 光微波分频相位噪声 | < −180 dBc/Hz @ X 波段 | Kalubovilage 2022 |
| 梳齿等距性 | < 10⁻¹⁹ | Udem 2002 |

---

## 四、核心限制链快查（Top BOUNDED-BY 关系）

### 超稳激光 FP 腔分支

```
ent.fp_cavity_system
  └─ BOUNDED-BY pri.brownian_thermal_noise_fdt (84% 镜基底 + 15% 镀层 + 1% 间隔物)
       ├─ 突破路径 1: pri.crystalline_coating_low_brownian_noise (φ 降低 16×, demonstrated)
       ├─ 突破路径 2: pri.cryogenic_mechanical_q_enhancement (Si @ 124K/17K/4K, demonstrated)
       └─ 突破路径 3: pri.long_cavity_thermal_noise_reduction (σ_y ∝ 1/L, demonstrated)
  └─ BOUNDED-BY pri.flicker_noise_linewidth_divergence (闪变噪声线宽发散)
  └─ CONDITIONED-BY ent.vibration_environment (环境振动)
  └─ CONDITIONED-BY ent.thermal_environment (温度稳定性)
```

### 超稳激光光纤分支

```
ent.fiber_interferometer
  └─ BOUNDED-BY pri.fiber_thermal_noise_wanser (光纤热噪声)
  └─ BOUNDED-BY pri.rayleigh_backscattering_noise (Rayleigh 背向散射)
  └─ 突破路径: pri.antiresonant_hollow_core_guidance (空心光纤, proposed→demonstrated)
```

---

## 五、核心原理清单（tier: domain，跨论文复用）

### 超稳激光

| 原理 ID | 名称 | 类型 |
|---------|------|------|
| `pri.brownian_thermal_noise_fdt` | 布朗热噪声——涨落耗散定理 | 限制性 |
| `pri.pdh_heterodyne_detection` | PDH 射频外差探测 | 使能性 |
| `pri.crystalline_coating_low_brownian_noise` | 晶体镀层低热噪声 | 突破性 |
| `pri.cryogenic_mechanical_q_enhancement` | 低温机械 Q 增强 | 突破性 |
| `pri.fiber_delay_line_frequency_ref` | 光纤延迟线频率参考 | 使能性 |
| `pri.fiber_thermal_noise_wanser` | 光纤热噪声（Wanser 模型） | 限制性 |
| `pri.ule_zero_cte` | ULE 零膨胀系数 | 使能性 |
| `pri.force_insensitive_tetrahedral_symmetry` | 力不敏感四面体对称 | 突破性 |
| `pri.flicker_noise_linewidth_divergence` | 闪变噪声线宽发散 | 限制性 |

### 光学频率梳

| 原理 ID | 名称 | 类型 |
|---------|------|------|
| `pri.self_referencing_f2f` | f-2f 自参考 | 使能性 |
| `pri.femtosecond_comb_frequency_ruler` | 飞秒梳频率标尺 | 使能性 |
| `pri.optical_frequency_division_microwave` | 光学分频到微波 | 使能性 |
| `pri.dissipative_kerr_soliton` | 耗散 Kerr 孤子 | 使能性 |
| `pri.dual_comb_multiheterodyne_detection` | 双梳多外差检测 | 使能性 |

### 频率标准

| 原理 ID | 名称 | 类型 |
|---------|------|------|
| `pri.quantum_projection_noise_limit` | 量子投影噪声极限 | 限制性 |
| `pri.dick_effect` | Dick 效应 | 限制性 |
| `pri.magic_wavelength_lattice` | 魔术波长光晶格 | 使能性 |

---

## 六、跨专题接口清单

| 接口 | 上游 | 下游 | 核心指标 | 接口类型 |
|------|------|------|---------|---------|
| 询问激光 → 频率标准 | 超稳激光 | 频率标准 | 激光线宽、相干时间 | CONDITIONED-BY |
| 梳齿锁定 → 频率计数 | 超稳激光 + 光梳 | 频率标准/比对 | 梳齿相位噪声 | CONDITIONED-BY |
| 时频传递链路 → 远程比对 | 超稳激光 + 光梳 | 时间频率传递 | 链路不稳定度 | CONDITIONED-BY |
| 光-微波分频 → SI 秒 | 光学频率梳 | 频率标准/微波 | 分频噪声贡献 | CONDITIONED-BY |
| 数学基础 → 性能表征 | 数学基础 | 所有专题 | Allan 偏差、噪声谱密度 | 共享模块 |

---

## 七、框架型文档目录

| 文件 | 专题 | 定义的顶层实体 |
|------|------|--------------|
| `topics/frequency-standards/papers/fortier2026.yaml` | frequency-standards | `ent.optical_frequency_standard`、`ent.trapped_ion_optical_clock`、`ent.optical_lattice_clock`、`ent.nuclear_clock_229th` |
| `topics/optical-frequency-combs/papers/giunta2019.yaml` | optical-frequency-combs | `ent.optical_frequency_comb` |
| `topics/timescales/papers/dimarcq2024.yaml` | timescales | `ent.si_second_definition` |

---

## 八、综合分析页面

> 综合页面是 YAML 节点的派生视图（derived view），不替代 YAML 作为 source of truth。

| 综合页面 | 专题 | 内容 |
|---------|------|------|
| [`thermal_noise_landscape.md`](topics/ultrastable-laser/synthesis/thermal_noise_landscape.md) | 超稳激光 | 热噪声限制全景：材料路线图、温度路线图、理论极限与实测差距 |
| [`stability_record_timeline.md`](topics/ultrastable-laser/synthesis/stability_record_timeline.md) | 超稳激光 | 稳定度演化时间线：1999–2026 关键突破 |

---

## 九、快速查找

- **按论文查找**：见 [`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md) 的完整已处理论文列表
- **按 Schema 规范查找**：见 [`SCHEMA.md`](SCHEMA.md)
- **按专题查找**：见 [`TOPICS.md`](TOPICS.md)
- **按时间线查找**：见 [`LOG.md`](LOG.md) 的演化日志
- **演化日志**：见 [`LOG.md`](LOG.md)

---

*本索引由 AI 自动维护，每次论文 Ingest 后更新。*
