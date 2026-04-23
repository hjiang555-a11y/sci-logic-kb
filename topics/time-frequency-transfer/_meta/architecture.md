# Time-Frequency Transfer — Topic Architecture

> **Status**: 🟡 `skeleton` — 当前 1 篇 framework 种子文档（`cacciapuoti2017.yaml`，ESA I-SOC 科学需求）+ ~15 节点（任务顶层 + MWL / ELT+ / FCOL / SLOC / SFC 子系统 + GTD / EEP / 共视 / 非共视 原理 + 链路指标）。**仍不作为当前整治重点**，下一步等待代表性地面光纤 / 自由空间 / 卫星链路论文摄入。
>
> <!-- TODO: 待信息补全 —— 光纤相干链路代表论文、TWSTFT 代表论文、GNSS 载波相位时频比对论文；需至少 3 篇代表论文才能激活 Level 1 实体 `ent.fiber_link` / `ent.free_space_link` / `ent.satellite_link` -->
>
> Source of truth: SCHEMA.md

## Architecture (planned)

```
时间频率传递系统
├── 空间光钟任务（已种子）
│   ├── ent.space_optical_clock_mission（I-SOC 代表实例，Level 1）
│   ├── ent.space_lattice_optical_clock_sloc（SLOC，Sr 光钟）
│   ├── ent.space_frequency_comb_sfc
│   ├── ent.microwave_link_mwl（Ku 波段双向，继承 ACES）
│   ├── ent.pulsed_optical_link_elt_plus（SLR 脉冲激光）
│   └── ent.frequency_comb_optical_link_fcol（可选）
│
├── 光纤链路（待补）
│   ├── 相干光学链路（phase-coherent optical fiber link）
│   ├── 微波频率传递（RF over fiber）
│   └── 时间传递（1PPS / two-way）
│
├── 自由空间链路（待补）
│   ├── 双向卫星时频传递（TWSTFT）
│   ├── 光学自由空间链路
│   └── GNSS 时频比对（GPS/Galileo carrier phase）
│
├── 核心原理（部分已种子）
│   ├── pri.gravitational_time_dilation（foundational，已建）
│   ├── pri.einstein_equivalence_principle（foundational，已建）
│   ├── pri.common_view_clock_comparison（domain，已建）
│   ├── pri.non_common_view_clock_comparison（domain，已建）
│   ├── 相位噪声补偿（active noise cancellation）（待补）
│   ├── 色散补偿（待补）
│   └── 大气湍流限制（待补）
│
└── 外围接口层（已建 CONDITIONED-BY）
    ├── CONDITIONED-BY ultrastable-laser（ent.fp_cavity_system，作为 SLOC 询问激光）
    ├── CONDITIONED-BY optical-frequency-combs（ent.optical_frequency_comb，SFC 父类）
    └── CONDITIONED-BY frequency-standards（ent.optical_lattice_clock，SLOC 父类）
```

## Status: Seed framework (1 paper: cacciapuoti2017.yaml)

Priority papers to ingest (保留原计划):
- Fiber link: Ma 1994, Predehl 2012, Droste 2013
- Free-space: Giorgetta 2013, Bergeron 2019
- Satellite: Fujieda 2018

