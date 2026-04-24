# Optical Frequency Combs — Topic Architecture

> This file describes the internal architecture of the optical-frequency-combs topic.
> Source of truth: SCHEMA.md §2 (光学频率梳专题内部架构)

## Technology / Application Separation (v4.1)

```
光学频率梳系统
│
├── A. 光梳技术
│   ├── A1. 飞秒锁模激光器光频梳（传统成熟光梳）
│   ├── A2. 微腔与电光调制光梳（新型平台）
│   └── A3. 天文光梳
│
├── B. 光梳应用
│   ├── 频率综合与计量
│   ├── 双梳光谱学
│   ├── 频率梳光谱学
│   └── 中红外梳光谱
│
├── 原理层（全局）
└── 外围接口层
    ├── CONDITIONED-BY ent.fp_cavity_system（超稳激光）
    ├── CONDITIONED-BY ent.optical_frequency_standard（频率标准）
    └── 支撑专题：时间频率传递、频率标准
```

## Core Enabling Principles

- `pri.self_referencing_f2f` — f-2f self-referencing
- `pri.femtosecond_comb_frequency_ruler` — femtosecond comb as frequency ruler
- `pri.optical_frequency_division_microwave` — optical-to-microwave frequency division
- `pri.dissipative_kerr_soliton` — DKS paradigm for microcombs

## Cross-Topic Interfaces

| Interface | Direction | Core Metric |
|-----------|-----------|-------------|
| Ultrastable laser → OFC | CONDITIONED-BY | Laser linewidth, coherence time |
| OFC → Frequency standards | Enables | Frequency counting, ratio measurement |
| OFC → Time-frequency transfer | Enables | Coherent link phase noise |

## Paper Count

> 精确数字以 [`INDEX.md`](../INDEX.md) / `python scripts/stats.py` 为准；摄入历史见 [`LOG.md`](../../../LOG.md)。本文件不硬编码论文总数，避免漂移。
>
> 子域主线指标 v2 定义见 [`scoping_principles.md`](scoping_principles.md)。
