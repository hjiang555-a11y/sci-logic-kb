# 专题审核入口文档

> 这份文档只服务一件事：**让专家能够集中审三项内容——专题内部构架、核心指标、关键节点。**
>
> 若这里与 Schema 细节冲突，**一律以 [`SCHEMA.md`](../SCHEMA.md) 为准**。

---

## 1. 审核顺序（固定）

### 1.1 先审专题内部构架

先看：

1. [`SCHEMA.md` §二 系统架构](../SCHEMA.md)
2. 各专题 `topics/<topic>/_meta/architecture.md`

审核重点只看三件事：

- 顶层分支是否清楚
- 主线限制链是否清楚
- 跨专题接口是否清楚

### 1.2 再审核心指标

不是每个专题都用同一条指标主线：

- **超稳激光**：单主线 `σ_y(τ=1 s)`
- **光学频率梳**：多主线，按子域分别审
- **频率标准**：优先看系统不确定度 / 稳定度
- **时间标尺与钟组**：优先看秒定义重定义条件与长期保持接口
- **时间频率传递**：当前只有骨架，先审接口，不审记录榜

### 1.3 最后审关键节点

关键节点不是“全量节点”，而是**决定主线能否读通的节点**：

- 顶层实体（Level 0 / 1）
- 主限制原理（`pri.*`）
- 主方法（`meth.*`）
- 主线指标（`met.*`）

---

## 2. 专题审核总览

| 专题 | 当前状态 | 构架入口 | 核心指标入口 | 关键节点入口 |
|------|---------|---------|-------------|-------------|
| 超稳激光 | 维护中（143篇） | [`topics/ultrastable-laser/_meta/architecture.md`](../topics/ultrastable-laser/_meta/architecture.md) | [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md) | 见 §3 |
| 光学频率梳 | 已入库（213篇） | [`topics/optical-frequency-combs/_meta/architecture.md`](../topics/optical-frequency-combs/_meta/architecture.md) | [`topics/optical-frequency-combs/_meta/scoping_principles.md`](../topics/optical-frequency-combs/_meta/scoping_principles.md) | 见 §4 |
| 频率标准 | 成长中（72篇） | [`topics/frequency-standards/_meta/architecture.md`](../topics/frequency-standards/_meta/architecture.md) | `fortier2026.yaml` 中汇总指标 | 见 §5 |
| 时间标尺 | 初建（8篇） | [`topics/timescales/_meta/architecture.md`](../topics/timescales/_meta/architecture.md) | `dimarcq2024.yaml` 中路线图指标 | 见 §6 |
| 时间频率传递 | 成长中（76篇） | [`topics/time-frequency-transfer/_meta/architecture.md`](../topics/time-frequency-transfer/_meta/architecture.md) | 见 `_meta/architecture.md` 中指标 | 见 §7 |
| 共享基础 | 初建（20篇） | [`topics/shared/_meta/architecture.md`](../topics/shared/_meta/architecture.md) | — | — |

---

## 3. 超稳激光（优先审）

### 3.1 构架要点

- 主体是**五层结构**
- 核心 Level 1 实体是 `ent.fp_cavity_system`
- 替代分支是 `ent.shb_eu_yso_reference_l13` 与 `ent.fiber_interferometer`
- 主线限制是热噪声、振动、RAM / PDH 偏移

建议先读：

1. [`topics/ultrastable-laser/_meta/architecture.md`](../topics/ultrastable-laser/_meta/architecture.md)
2. [`topics/ultrastable-laser/synthesis/stability_record_timeline.md`](../topics/ultrastable-laser/synthesis/stability_record_timeline.md)
3. [`topics/ultrastable-laser/synthesis/thermal_noise_landscape.md`](../topics/ultrastable-laser/synthesis/thermal_noise_landscape.md)

### 3.2 核心指标

**唯一主线：`σ_y(τ=1 s)`**

- 之所以选它，是因为它直接对应超稳激光在下游光钟询问时间尺度上的实际价值，比单独的线宽或频噪 PSD 更能代表主线性能边界
- 审核时先看该值是否被明确给出
- 必须看 Allan 变体类型（ADEV / MDEV / OADEV / Hadamard）
- 线宽、频噪 PSD、相干时间只作 secondary metrics
- 加速度灵敏度、漂移、损耗角只作 engineering / enabling metrics

快速入口：

- [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md)
- [`topics/ultrastable-laser/_meta/architecture.md`](../topics/ultrastable-laser/_meta/architecture.md) 的 “Key Performance Records”

### 3.3 关键节点包

| 节点 | 为什么先审它 | 代表来源文件 |
|------|-------------|-------------|
| `ent.fp_cavity_system` | 整个专题的主实体，后续限制链都挂在它上面 | [`topics/ultrastable-laser/papers/numata2004.yaml`](../topics/ultrastable-laser/papers/numata2004.yaml) |
| `pri.brownian_thermal_noise_fdt` | 当前主线最核心物理限制 | [`topics/ultrastable-laser/papers/numata2004.yaml`](../topics/ultrastable-laser/papers/numata2004.yaml) |
| `meth.pdh_locking` | FP 腔主方法入口 | [`topics/ultrastable-laser/papers/drever1983.yaml`](../topics/ultrastable-laser/papers/drever1983.yaml) |
| `ent.fiber_interferometer` | 非 FP 腔替代分支入口 | [`topics/ultrastable-laser/papers/jiang2010.yaml`](../topics/ultrastable-laser/papers/jiang2010.yaml) |
| `ent.shb_eu_yso_reference_l13` | SHB 替代分支入口 | [`topics/ultrastable-laser/papers/leibrandt2013.yaml`](../topics/ultrastable-laser/papers/leibrandt2013.yaml) |

推荐审查问题：

- `ent.fp_cavity_system` 的子单元拆分是否符合认知边界？
- `pri.brownian_thermal_noise_fdt` 是否足够支撑“为什么卡在这里”？
- `meth.pdh_locking` 是否明确写清了输入、输出和限制？

---

## 4. 光学频率梳（按子域审，不用单主线）

### 4.1 构架要点

- 架构分成 **A. 技术平台** 和 **B. 应用**
- 这不是一个适合单一主线指标的专题
- 审核重点是：**子域划分是否清楚，接口是否清楚**

建议先读：

1. [`topics/optical-frequency-combs/_meta/architecture.md`](../topics/optical-frequency-combs/_meta/architecture.md)
2. [`topics/optical-frequency-combs/_meta/scoping_principles.md`](../topics/optical-frequency-combs/_meta/scoping_principles.md)

### 4.2 核心指标

本专题按子域维护主线，不要把全部论文都压到 `σ_y` 上。

当前最需要审的是这几条主线定义是否合理：

- **A1-Rep**：`f_rep + self-referencing`
- **A1-Noise**：`f_CEO` / beat-note 积分相位噪声
- **A2-DKS**：相位噪声 + 泵浦-梳光转换效率 + 集成度
- **B-FreqSyn**：光-光 / 光-微波传递残差 `σ_y`
- **B-DCS**：mutual coherence time + 覆盖带宽
- **B-Spec / B-MIR**：绝对光谱 PSD + 转换效率 / 灵敏度

快速入口：

- [`topics/optical-frequency-combs/_meta/scoping_principles.md`](../topics/optical-frequency-combs/_meta/scoping_principles.md) §1.2

### 4.3 关键节点包

| 节点 | 为什么先审它 | 代表来源文件 |
|------|-------------|-------------|
| `ent.optical_frequency_comb` | 整个专题的通用顶层实体 | [`topics/optical-frequency-combs/papers/giunta2019.yaml`](../topics/optical-frequency-combs/papers/giunta2019.yaml) |
| `pri.self_referencing_f2f` | 绝对频率标尺成立的关键原理 | [`topics/optical-frequency-combs/papers/giunta2019.yaml`](../topics/optical-frequency-combs/papers/giunta2019.yaml) |
| `ent.microresonator_frequency_comb` | 微梳平台入口 | [`topics/optical-frequency-combs/papers/kippenberg2011.yaml`](../topics/optical-frequency-combs/papers/kippenberg2011.yaml) |
| `pri.dissipative_kerr_soliton` | 微梳从低相干到可用计量平台的关键原理 | [`topics/optical-frequency-combs/papers/kippenberg2018.yaml`](../topics/optical-frequency-combs/papers/kippenberg2018.yaml) |
| `ent.dual_comb_spectrometer` | 应用侧最重要 Level 1 实体之一 | [`topics/optical-frequency-combs/papers/coddington2016.yaml`](../topics/optical-frequency-combs/papers/coddington2016.yaml) |
| `meth.dual_comb_spectroscopy` | 双梳应用的主方法入口 | [`topics/optical-frequency-combs/papers/coddington2016.yaml`](../topics/optical-frequency-combs/papers/coddington2016.yaml) |

推荐审查问题：

- 技术平台节点和应用节点是否分得够清楚？
- `pri.self_referencing_f2f` 与 `ent.optical_frequency_comb` 的接口是否足够明确？
- DKS、DCS 这些高价值节点的内容是否已经达到“可独立阅读”的水平？

---

## 5. 频率标准（当前以 framework 审骨架）

### 5.1 构架要点

- 现在先审 Level 1 骨架是否合理
- 当前主实体是 `ent.optical_frequency_standard`
- 当前最关键的跨专题接口是：
  - 向上接 `ent.si_second_definition`
  - 向下受 `ent.fp_cavity_system`、`ent.optical_frequency_comb` 约束

入口：

- [`topics/frequency-standards/_meta/architecture.md`](../topics/frequency-standards/_meta/architecture.md)
- [`topics/frequency-standards/papers/fortier2026.yaml`](../topics/frequency-standards/papers/fortier2026.yaml)

### 5.2 核心指标

优先审两条：

- `met.optical_clock_fractional_instability`
- `met.optical_clock_fractional_uncertainty`

审核时关注：

- 是否把**稳定度**和**系统不确定度**分清
- 是否把超稳激光通过 Dick 效应的耦合写清

### 5.3 关键节点包

| 节点 | 为什么先审它 | 代表来源文件 |
|------|-------------|-------------|
| `ent.optical_frequency_standard` | 频率标准专题总入口 | [`topics/frequency-standards/papers/fortier2026.yaml`](../topics/frequency-standards/papers/fortier2026.yaml) |
| `pri.quantum_projection_noise_limit` | 光钟稳定度理论下限 | [`topics/frequency-standards/papers/fortier2026.yaml`](../topics/frequency-standards/papers/fortier2026.yaml) |
| `pri.dick_effect` | 与超稳激光专题最重要的接口原理 | [`topics/frequency-standards/papers/fortier2026.yaml`](../topics/frequency-standards/papers/fortier2026.yaml) |

---

## 6. 时间标尺（当前以 framework 审接口）

### 6.1 构架要点

- 当前重点不是补实例，而是先看顶层接口是否合理
- 顶层实体是 `ent.si_second_definition`
- 核心问题是“什么条件下秒可以重定义”

入口：

- [`topics/timescales/_meta/architecture.md`](../topics/timescales/_meta/architecture.md)
- [`topics/timescales/papers/dimarcq2024.yaml`](../topics/timescales/papers/dimarcq2024.yaml)

### 6.2 核心指标

优先审：

- `met.optical_clock_systematic_uncertainty`
- `met.frequency_ratio_agreement_cross_lab`

这两条指标决定“重定义就绪度”是否被正确表达。

### 6.3 关键节点包

| 节点 | 为什么先审它 | 代表来源文件 |
|------|-------------|-------------|
| `ent.si_second_definition` | 整个 timescales 专题顶层实体 | [`topics/timescales/papers/dimarcq2024.yaml`](../topics/timescales/papers/dimarcq2024.yaml) |
| `pri.redefinition_criteria_second` | 秒重定义的核心限制链 | [`topics/timescales/papers/dimarcq2024.yaml`](../topics/timescales/papers/dimarcq2024.yaml) |
| `pri.secondary_representation_si_second` | 从当前定义过渡到新定义的桥梁机制 | [`topics/timescales/papers/dimarcq2024.yaml`](../topics/timescales/papers/dimarcq2024.yaml) |

---

## 7. 时间频率传递（76篇已入库，按链路子域审）

当前已有 76 篇论文入库，覆盖光纤链路/自由空间链路/卫星链路。审核重点：

- 光纤链路 / 自由空间链路 / 卫星链路的一级划分是否合理
- 与超稳激光 / 频梳 / 频率标准的接口是否清楚
- 核心指标：链路残差不稳定度 `met.*_link_instability`

入口：

- [`topics/time-frequency-transfer/_meta/architecture.md`](../topics/time-frequency-transfer/_meta/architecture.md)
- [`topics/time-frequency-transfer/INDEX.md`](../topics/time-frequency-transfer/INDEX.md)

---

## 8. 当前审核建议（按优先级）

1. **先审超稳激光**：它已经具备"结构 + 指标 + 节点"的最完整闭环，当前 143 篇论文
2. **再审光学频率梳**：213 篇最大论文量，子域多主线指标体系需要验证
3. **再审频率标准 / 时间频率传递**：各有 72/76 篇论文，当前先确认框架和接口
4. **时间标尺 / 共享基础不展开**：论文规模尚小，守住骨架和接口

---

## 9. 这份文档的定位

这不是 Schema，也不是摄入指南，而是**审核入口页**。

- 它帮你决定**先看什么**
- 它帮你把审查聚焦到**结构 / 指标 / 关键节点**
- 它不代替具体 YAML，也不代替 `SCHEMA.md`
