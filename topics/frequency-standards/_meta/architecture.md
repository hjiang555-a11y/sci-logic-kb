# Frequency Standards — Topic Architecture

> **Status**: 🟢 `growing` — 已从 framework 骨架扩展为 ≥10 篇规模（精确数字见 [`INDEX.md`](../INDEX.md) / `python scripts/stats.py`）。本架构定义顶层骨架，后续继续补充 Level 2 实例（Al⁺/Sr/Yb/²²⁹Th 光钟、Cs fountain / H maser / Rb / CSAC 微波标准）与具体限制链。
>
> <!-- TODO: 补微波标准分支代表论文、跨专题 CONDITIONED-BY 接口；光钟物种的系统误差预算综述 -->
>
> Source of truth: SCHEMA.md §2 (频率标准专题内部架构)

## Architecture (v4.1)

```
频率标准系统
├── 分支1：光学频率标准
│   ├── ent.optical_frequency_standard（通用顶层）
│   ├── ent.trapped_ion_optical_clock（囚禁离子光钟）
│   ├── ent.optical_lattice_clock（光晶格钟）
│   └── ent.nuclear_clock_229th（²²⁹Th 核钟）
│
├── 分支2：微波频率标准（待建）
│   ├── 铯喷泉钟 (Cs Fountain)
│   ├── 氢脉泽 (H Maser)
│   ├── 铷标准 (Rb Standard)
│   └── 芯片级原子钟 (CSAC / CPT)
│
├── 分支3：核心原理
│   ├── pri.quantum_projection_noise_limit
│   ├── pri.dick_effect
│   └── pri.magic_wavelength_lattice
│
└── 外围接口层
    ├── CONDITIONED-BY ent.fp_cavity_system（超稳激光）
    ├── CONDITIONED-BY ent.optical_frequency_comb（光梳）
    └── CONDITIONED-BY ent.si_second_definition（秒定义）
```

## Status: Growing topic

> 精确论文数 / 节点数见 [`INDEX.md`](../INDEX.md) / `python scripts/stats.py`。

Next priorities:
- Individual clock species papers (Al+, Sr, Yb, ²²⁹Th)
- Microwave standard papers (Cs fountain, H maser)
- Clock comparison / ratio measurement papers
