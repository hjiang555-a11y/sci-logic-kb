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

> **v2 重排（2026-04-21，Round 3）**：本榜单遵循 [`_meta/scoping_principles.md`](scoping_principles.md) v2 的"σ_y(1 s) 单一主线"原则，分三层展示。主线榜以 σ_y 为唯一坐标轴，次要指标与工程指标仅作参考，不据此评判 breakthrough。

### 🏆 主线指标榜：σ_y(τ = 1 s) 全局纪录演化

> 注意 Allan 变体类型（ADEV / MDEV / OADEV / Hadamard）会影响数值可比性——不同变体使用不同的加权窗口或前向差分阶数（例如 MDEV 对白相噪声的抑制强于 ADEV，Hadamard 方差滤除线性频率漂移），直接拿"最小数值"横向排名会产生误导。跨论文对比请以同类型为先。

| 年份 | σ_y(1 s) | 类型 | 子分支 | 使能技术 | 文献 | 意义 |
|------|---------|-----|--------|---------|-----|-----|
| 1999 | 3×10⁻¹⁶ | ADEV | FP 腔 | ULE 24 cm + PDH + 悬挂隔振 | Young 1999 | 首次抵达热噪声极限 |
| 2012 | ~1×10⁻¹⁶ | ADEV | FP 腔 | Si 124K + 低温 | Kessler 2012 | 低温 Si 路线首次演示 |
| 2015 | <1×10⁻¹⁶ | ADEV | FP 腔 | 48 cm ULE 长腔 + 自平衡安装 | Häfner 2015 | 室温长腔路线 |
| 2017 | 4×10⁻¹⁷ | mod σ_y | FP 腔 | Si 124K + IBS 镀层 | Matei 2017 | IBS 镀层极限暴露 |
| 2025 | ~10⁻¹⁷ | MDEV | FP 腔 | Si sub-5K + 振动抑制 | Chen 2025 | 深低温路线 |
| **2026** | **2.5×10⁻¹⁷** | **mod σ_y** | **FP 腔** | **Si 17K + AlGaAs + 双腔平均** | **Lee 2026** | **当前世界纪录** 🏆 |

### 🥈 子分支 SOTA（σ_y(1 s)，按 `scoping_principles.md` §1.7 界定）

| 子分支 | 当前 SOTA | 类型 | 文献 |
|--------|----------|-----|------|
| FP 腔 | 2.5×10⁻¹⁷ | mod σ_y | Lee 2026 |
| 光纤干涉仪（FDL / 自零差） | 6.3×10⁻¹⁵ @ 16 ms | — | Jeon 2025 |
| 光谱烧孔 SHB | ~6×10⁻¹⁶ | — | Thorpe 2011 |

### 📘 次要指标（参考 / informational，不进入主线榜）

| 指标 | 最佳值 | 文献 | 备注 |
|------|-------|------|------|
| 瞬时线宽 | 5–10 mHz | Matei 2017 | 已达 σ_y 主线瓶颈，增量不独立升档 |
| 光学相干时间 | 11–55 s | Matei 2017 | 主要反映 σ_y 水平，不单独升档 |
| 长期 σ_y / drift | ~10⁻¹⁹ /s | Robinson 2019 | 由下游频标技术兜底，不升档（见 §1.2） |

### 🔧 工程指标（enabling，不进入主线榜）

| 指标 | 代表值 | 文献 | 备注 |
|------|-------|------|------|
| 加速度灵敏度 | < 2×10⁻¹⁰/g 全向 | Häfner 2015 | 工程手段，不独立升档 |
| 镀层损耗角（AlGaAs） | < 2.3×10⁻⁵ @ 17 K | Lee 2026 | 使能指标 |
| 精细度 | >3×10⁵ | Cole 2016 | 使能指标 |

## Paper Count: 78

---

## 物理限制 ↔ 突破路径 ↔ 代表论文（四栏对照）

> 新增于 Round 1 整固（2026-04-21）；Round 3（2026-04-21）补"对 σ_y(1s) 贡献量级"列，使每条突破路径都直接挂到专题主线指标上。本表是 `_meta` 层的"专题认知地图"，与 `synthesis/breakthrough_paths_matrix.md` 保持结构一致（后者含更细的条件维度）。

| 物理限制 (pri.*) | 主要突破路径 | 对 σ_y(1 s) 贡献量级 | 代表论文（状态） |
|------------------|-------------|---------------------|-----------------|
| `pri.brownian_thermal_noise_fdt` | 晶体镀层 (`pri.crystalline_coating_low_brownian_noise`) | ~10⁻¹⁶ → ~10⁻¹⁷ | Cole 2013 ✅、Matei 2017 ✅、Kedar 2023 ✅、Lee 2026 ✅ |
|  | 低温 Si 腔 (`pri.cryogenic_mechanical_q_enhancement`) | ~10⁻¹⁶ → 2.5×10⁻¹⁷ | Kessler 2012 ✅、Robinson 2019 ✅、Chen 2025 ✅、Lee 2026 🏆 |
|  | 长腔 (`pri.long_cavity_thermal_noise_reduction`) | σ_y ∝ 1/L（L: 10→48 cm ≈ 5× 改善） | Häfner 2015 ✅（48 cm）、Parke 2025 ✅（68 cm） |
|  | 多腔频率平均 (`pri.optical_frequency_averaging`) | √N 改善（N 腔平均） | Chen 2020 ✅、Lee 2026 ✅ |
| `pri.ram_pdh_frequency_offset` | 布儒斯特角被动抑制 (`pri.brewster_angle_ram_suppression`) | 工程使能（低于 σ_y 主线） | Tai 2016 ✅ |
|  | 主动 RAM 伺服 | 工程使能 | Zhang 2014 ✅ |
| `pri.fiber_thermal_noise_wanser` | 空心光纤 (HC-ARF / ULE-HCF) | 光纤分支 ~10⁻¹⁴ → ~10⁻¹⁵ | Belardi 2015 ✅、Michaud-Belleau 2022 ✅、Ding 2025 ✅ |
|  | 双缠绕抵消 | 光纤分支 | Huang JC 2019b ✅ |
| `pri.rayleigh_backscattering_noise` | AOM 外差频移 | 工程使能 | Jiang 2010 ✅ |
|  | 空心光纤低散射 (`pri.hollow_core_fiber_low_backscattering`) | 光纤分支 | Michaud-Belleau 2021 ✅ |
| `pri.acceleration_induced_length_change`（通过 CONDITIONED-BY） | 对称几何 + 形变补偿 (`pri.cavity_deformation_compensation`) | 工程使能（振动受限环境下可保护 σ_y） | Webster 2007 ✅、Webster 2011 ✅、Chen 2020 ✅、Sanjuan 2019 ✅ |
|  | 外部隔振 | 工程使能 | Young 1999 ✅ |
|  | 自平衡长腔安装 | 工程使能（叠加长腔路径） | Häfner 2015 ✅ |
| `pri.shot_noise_frequency_limit` | 提高光功率 / 精度检测 | 探测下限（非当前主线瓶颈） | Drever 1983（理论）✅ |

> 🏆 = 当前领域世界纪录。YAML `breakthrough_paths` 逐项补全进度见 [`reports/chain_gap_ultrastable.md`](../../../reports/chain_gap_ultrastable.md)。
>
> **"工程使能"标签含义**：该路径自身不刷新 σ_y 主线纪录，但在合适条件下保护或使能 σ_y 主线路径（典型如振动隔离让热噪声极限能够被观测到；RAM 抑制让 PDH 锁频残余偏移不掩盖热噪声；温度稳定在 CTE 零点让长期漂移不吃掉短期 σ_y 测量窗口）。按 [`scoping_principles.md`](scoping_principles.md) §1.2，单独命中工程使能路径的论文默认为 `evidence`。
>
> PR#3 计划在 YAML `breakthrough_paths[*]` 下补 `expected_σy_gain` 字段，使本表可从 YAML 自动生成。

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
