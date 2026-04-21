# Optical Frequency Combs — 专题内部评判原则

> **版本**：v1（2026-04-21）
> **范围**：本文件仅在 `topics/optical-frequency-combs/` 范围内有效，**不**向全局 knowledge base 扩展。
> **与全局规则的关系**：全局规则在 [`SCHEMA.md`](../../../SCHEMA.md) 与 [`docs/CONTRIBUTION_TIER_RULES.md`](../../../docs/CONTRIBUTION_TIER_RULES.md) 中定义；本文件补充**只针对光学频率梳专题**的评判偏好。冲突时，本文件的专题偏好**优先**用于本专题内的档位判定；跨专题讨论仍以全局规则为准。
>
> **v1 建立说明**：光学频率梳专题涵盖多个应用子域（频率综合/频率梳光谱/双梳光谱/中红外梳/天文梳等），各子域的主线指标不一致。本版本先建立框架性原则，等各子域积累 ≥ 3 篇论文后再逐一定义子域主线。

---

## 1. 专题结构与主线指标（Multi-Track Principle）

### 1.1 原则

> **光学频率梳专题不适合单一主线指标；按应用子域分别定义。**

动机：
- 频率综合/计量子域：关注的是梳齿到参考激光的**相位噪声传递**和**频率不确定度**
- 双梳光谱子域：关注的是**双梳互相干时间**（mutual coherence time）和**光谱覆盖宽度**
- 天文光梳子域：关注的是**梳齿均匀性**（comb line uniformity）和**长期稳定度**
- 微腔梳子域（DKS）：关注的是**泵浦效率**、**相位噪声**和**集成化 SWaP**

强制单一主线会导致大量非最优分类（尤其对于跨子域的综述/应用论文）。

### 1.2 当前已定义子域及其初步主线指标

| 子域 | 主线指标（候选） | 状态 |
|------|----------------|------|
| 频率综合/计量（Frequency Synthesis） | 梳齿相位噪声 PSD @ 1 Hz offset；或 f–2f 自参考后的 CEO 频率不确定度 | 🟡 待专家确认 |
| 双梳光谱（Dual-Comb Spectroscopy） | 互相干时间（mutual coherence time）；或光谱覆盖范围（cm⁻¹ 或 THz） | 🟡 待专家确认 |
| 天文光梳（Astro-Comb） | 梳齿均匀性（dB）；长期稳定度（hours-scale） | 🟡 待专家确认 |
| 微腔梳 DKS（Microresonator Comb） | 相位噪声 @ offset；或转换效率 | 🟡 待专家确认 |
| 中红外光谱（Mid-IR Spectroscopy） | 探测灵敏度（cm⁻¹/Hz^1/2）；或覆盖波段（μm） | 🟡 待专家确认 |

> 在专家确认前，按全局 `docs/CONTRIBUTION_TIER_RULES.md` 的通用判据处理档位。

### 1.3 框架型论文（framework）的特殊处理

光学频率梳专题包含大量综述/路线图型论文（如 `picque2019.yaml`、`kippenberg2018.yaml`、`giunta2019.yaml`）。这类论文：

- 使用 `meta.contribution_type: framework`
- 主要职责是定义 Level 0/1 顶层实体与 tier: meta/domain 原理
- 不负责具体实验的 Level 2 参数实例
- **不要求**补 `breakthrough_paths`

---

## 2. 档位判据（过渡期：子域主线确认前）

在子域主线指标未经专家确认前，使用以下过渡判据：

| 信号 | 对档位的影响 |
|------|------------|
| **首次演示某新型梳技术原理**（如首篇 DKS 论文、首篇双梳光谱论文） | ✅ `breakthrough`（强信号） |
| **刷新某子域的关键指标纪录**（如最宽光谱覆盖、最低相位噪声） | ✅ `breakthrough`（强信号） |
| **提出可复用的新 `pri.*` 原理**（不只是从已有原理派生） | ✅ `breakthrough` |
| 在已有梳技术上换材料/平台/波长复现 | ⚠ `evidence` |
| 综述 / 路线图 / 教科书 | `framework` |
| 其余（新数据点、工程改进、参数扫描） | `evidence`（默认） |

---

## 3. 与超稳激光专题的接口

光学频率梳专题通过以下接口与超稳激光专题耦合：

- `CONDITIONED-BY ent.fp_cavity_system`：梳的相位噪声下限受询问激光稳定度约束
- `CONDITIONED-BY met.fractional_freq_instability_*`：梳齿频率不确定度受参考激光 σ_y 约束

处理跨专题边界论文时：
- 若主贡献在**超稳激光稳定度**而非梳技术 → 归 `ultrastable-laser` 专题
- 若主贡献在**梳技术/梳应用** → 归 `optical-frequency-combs` 专题

---

## 4. 子域主线指标定义计划（待专家确认）

> 以下问题请专家在下次专题规划会议中回答，用于确定子域主线：

1. **频率综合/计量**：主线指标用"梳齿相位噪声"还是"CEO 频率不稳定度"？是否有类似 σ_y 的统一表征量？
2. **双梳光谱**：互相干时间是否足以作为主线？还是应以"光谱分辨率 × 覆盖宽度"为二维主线？
3. **微腔梳 DKS**：SWaP 是否应作为 breakthrough 维度（考虑到芯片集成化是该子域的核心价值）？
4. **各子域是否需要独立的 scoping_principles 文件**，或统一维护在本文件？

---

## 版本历史

- **v1（2026-04-21）** · 初建：Multi-Track 原则、过渡期档位判据、与超稳激光接口、子域主线待确认问题

*本文件随专题演化更新；每轮修改请在顶部补版本字段并在 LOG.md 追加 `restructure` 条目。*
