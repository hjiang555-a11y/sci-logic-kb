# Time-Frequency Transfer — Topic Architecture

> Source of truth: SCHEMA.md

## Architecture (planned)

```
时间频率传递系统
├── 光纤链路
│   ├── 相干光学链路（phase-coherent optical fiber link）
│   ├── 微波频率传递（RF over fiber）
│   └── 时间传递（1PPS / two-way）
│
├── 自由空间链路
│   ├── 双向卫星时频传递（TWSTFT）
│   ├── 光学自由空间链路
│   └── GNSS 时频比对（GPS/Galileo carrier phase）
│
├── 核心原理
│   ├── 相位噪声补偿（active noise cancellation）
│   ├── 色散补偿
│   └── 大气湍流限制
│
└── 外围接口层
    ├── CONDITIONED-BY ultrastable-laser（相干光源）
    ├── CONDITIONED-BY optical-frequency-combs（频率梳桥接）
    └── CONDITIONED-BY frequency-standards（需要比对的钟）
```

## Status: Framework only (0 papers)

Priority papers to ingest:
- Fiber link: Ma 1994, Predehl 2012, Droste 2013
- Free-space: Giorgetta 2013, Bergeron 2019
- Satellite: Fujieda 2018
