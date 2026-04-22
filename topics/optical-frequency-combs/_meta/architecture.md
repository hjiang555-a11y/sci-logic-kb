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

## Paper Count: 90

> **更新 2026-04-22**：Batch 2（计量链路 / 频率综合，10 篇）+ Batch 3（新平台与光谱应用，9 篇；`BL4HI3QI` 为 `picque2019.yaml` 的 zotero 备份键，跳过）完成，合计 +19 → 90 篇。
>
> Batch 2：`marra2012` · `nardelli2023` · `rolland2018` · `hisai2021` · `ning2020` · `sinclair2015` · `zhang_s2024` · `chen_z2024` · `zhang2017b` · `lee2015`。
>
> Batch 3：`diddams2010` · `porat2018` · `cheng2024` · `holzwarth2001` · `ideguchi2016` · `spaun2016` · `timmers2018` · `diddams2007` · `papp2013b`。
>
> **更新 2026-04-21**：Batch 1（飞秒锁模激光器 A1 技术平台主线）+10 篇完成：washburn2004, newbury2005, bartels2009, meyer2013, wang2014, zhang2015, kuse2016, li2017b, ma2018, cai2020。子域主线指标 v2 定义见 [`scoping_principles.md`](scoping_principles.md)。
