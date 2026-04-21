# Timescales & Clock Ensembles — Topic Architecture

> **Status**: 🟡 `skeleton` — 当前仅 1 篇框架 + 6 节点，**暂不作为 Round 1–4 整治重点**。
>
> <!-- TODO: 待信息补全 —— UTC/TAI 算法综述、本地 UTC(k) 实现论文、钟组合成算法与 Kalman 滤波类论文 -->
>
> Source of truth: SCHEMA.md

## Architecture (planned)

```
时间标尺系统
├── SI 秒定义 (ent.si_second_definition)
│   ├── 当前定义（Cs 超精细跃迁）
│   └── 重新定义路线图（光学标准）
│
├── 时间标尺生成
│   ├── UTC / TAI
│   ├── 本地实现 UTC(k)
│   └── 钟组算法
│
├── 钟组技术
│   ├── 氢脉泽钟组
│   ├── 商用铯钟组
│   └── 光钟（未来）
│
└── 外围接口层
    ├── CONDITIONED-BY frequency-standards（光学标准→秒重新定义）
    └── CONDITIONED-BY time-frequency-transfer（远程比对链路）
```

## Status: Initial framework (1 paper: dimarcq2024.yaml)

Needs expansion with:
- Clock ensemble algorithm papers
- UTC/TAI generation papers
- Redefinition roadmap papers
