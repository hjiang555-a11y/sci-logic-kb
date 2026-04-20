# Frequency Standards — Topic Architecture

> This file describes the internal architecture of the frequency-standards topic.
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

## Status: Initial framework (1 paper: fortier2026.yaml)

Needs expansion with:
- Individual clock species papers (Al+, Sr, Yb, ²²⁹Th)
- Microwave standard papers (Cs fountain, H maser)
- Clock comparison / ratio measurement papers
