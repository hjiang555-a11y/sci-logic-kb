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
