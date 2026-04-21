# Ultrastable Laser — Topic Architecture

> This file describes the internal architecture of the ultrastable-laser topic.
> Source of truth: SCHEMA.md §2 (超稳激光专题内部架构)

## Five-Layer Architecture

```
超稳激光系统
├── 分支1：频率参考部件 [Level 1]
│   ├── FP 腔系统 (ent.fp_cavity_system)
│   │   ├── 热噪声子单元 → BOUNDED-BY pri.brownian_thermal_noise_fdt
│   │   ├── 振动灵敏度子单元 → CONDITIONED-BY ent.vibration_environment
│   │   ├── 调制解调子单元 → BOUNDED-BY pri.ram_pdh_frequency_offset
│   │   └── 实例节点 (Level 2 参数变体)
│   ├── 光谱烧孔频率参考 (ent.shb_eu_yso_reference_l13)
│   └── 光纤干涉仪 (ent.fiber_interferometer)
│
├── 分支2：误差探测方法
│   ├── meth.pdh_locking → FP 腔
│   ├── meth.tilt_locking → FP 腔
│   └── meth.fiber_delay_locking → 光纤干涉仪
│
├── 分支3：稳频策略
│   ├── meth.multi_stage_locking
│   └── meth.multi_cavity_averaging
│
└── 外围条件层
    ├── ent.vibration_environment
    ├── ent.thermal_environment
    └── ent.laser_source
```

## Core Limitation Chains

1. **Thermal Noise**: `ent.fp_cavity_system` → BOUNDED-BY → `pri.brownian_thermal_noise_fdt`
   - Mirror substrate: 84%, Mirror coating: 15%, Spacer: 1%
   - Breakthrough paths: crystalline coatings, cryogenic operation, longer cavities

2. **Fiber Thermal Noise**: `ent.fiber_interferometer` → BOUNDED-BY → `pri.fiber_thermal_noise_wanser`
   - Breakthrough: hollow-core fiber

3. **Vibration**: `ent.fp_cavity_system` → CONDITIONED-BY → `ent.vibration_environment`
   - Mitigation: force-insensitive designs, active isolation

## Key Performance Records

| Metric | Best Value | Source |
|--------|-----------|--------|
| Fractional instability | mod σ_y = 2.5×10⁻¹⁷ | Lee 2026 |
| Laser linewidth | 5–10 mHz | Matei 2017 |
| Optical coherence time | 11–55 s | Matei 2017 |

## Paper Count: 78

---

## 物理限制 ↔ 突破路径 ↔ 代表论文（三栏对照）

> 新增于 Round 1 整固（2026-04-21）。本表是 `_meta` 层的"专题认知地图"，与 `synthesis/breakthrough_paths_matrix.md` 保持结构一致（后者含更细的条件维度）。

| 物理限制 (pri.*) | 主要突破路径 | 代表论文（状态） |
|------------------|-------------|-----------------|
| `pri.brownian_thermal_noise_fdt` | 晶体镀层 (`pri.crystalline_coating_low_brownian_noise`) | Cole 2013 ✅、Matei 2017 ✅、Kedar 2023 ✅、Lee 2026 ✅ |
|  | 低温 Si 腔 (`pri.cryogenic_mechanical_q_enhancement`) | Kessler 2012 ✅、Robinson 2019 ✅、Chen 2025 ✅、Lee 2026 🏆 |
|  | 长腔 (`pri.long_cavity_thermal_noise_reduction`) | Häfner 2015 ✅（48 cm）、Parke 2025 ✅（68 cm） |
|  | 多腔频率平均 (`pri.optical_frequency_averaging`) | Chen 2020 ✅、Lee 2026 ✅ |
| `pri.ram_pdh_frequency_offset` | 布儒斯特角被动抑制 (`pri.brewster_angle_ram_suppression`) | Tai 2016 ✅ |
|  | 主动 RAM 伺服 | Zhang 2014 ✅ |
| `pri.fiber_thermal_noise_wanser` | 空心光纤 (HC-ARF / ULE-HCF) | Belardi 2015 ✅、Michaud-Belleau 2022 ✅、Ding 2025 ✅ |
|  | 双缠绕抵消 | Huang JC 2019b ✅ |
| `pri.rayleigh_backscattering_noise` | AOM 外差频移 | Jiang 2010 ✅ |
|  | 空心光纤低散射 (`pri.hollow_core_fiber_low_backscattering`) | Michaud-Belleau 2021 ✅ |
| `pri.acceleration_induced_length_change`（通过 CONDITIONED-BY） | 对称几何 + 形变补偿 (`pri.cavity_deformation_compensation`) | Webster 2007 ✅、Webster 2011 ✅、Chen 2020 ✅、Sanjuan 2019 ✅ |
|  | 外部隔振 | Young 1999 ✅ |
|  | 自平衡长腔安装 | Häfner 2015 ✅ |
| `pri.shot_noise_frequency_limit` | 提高光功率 / 精度检测 | Drever 1983（理论）✅ |

> 🏆 = 当前领域世界纪录。YAML `breakthrough_paths` 逐项补全进度见 [`reports/chain_gap_ultrastable.md`](../../../reports/chain_gap_ultrastable.md)。

---

## Synthesis 页面索引（跨论文综合视图）

- [stability_record_timeline.md](../synthesis/stability_record_timeline.md) — 稳定度记录演化
- [thermal_noise_landscape.md](../synthesis/thermal_noise_landscape.md) — 热噪声限制全景
- [vibration_insensitivity_landscape.md](../synthesis/vibration_insensitivity_landscape.md) — 振动不敏感设计路线
- [ram_and_pdh_error_budget.md](../synthesis/ram_and_pdh_error_budget.md) — RAM / PDH 误差预算
- [fiber_stabilization_landscape.md](../synthesis/fiber_stabilization_landscape.md) — 光纤稳频分支全景
- [cryogenic_roadmap.md](../synthesis/cryogenic_roadmap.md) — 低温工程演化路线图
- [spectral_hole_burning_track.md](../synthesis/spectral_hole_burning_track.md) — SHB 旁路路线
- [breakthrough_paths_matrix.md](../synthesis/breakthrough_paths_matrix.md) — 限制×路径 查询矩阵
