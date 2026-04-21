# Ultrastable Laser — 专题内部评判原则

> **范围**：本文件仅在 `topics/ultrastable-laser/` 范围内有效，**不**向全局 knowledge base 扩展。
> **与全局规则的关系**：全局规则在 [`SCHEMA.md`](../../../SCHEMA.md) 与 [`docs/CONTRIBUTION_TIER_RULES.md`](../../../docs/CONTRIBUTION_TIER_RULES.md) 中定义；本文件补充**只针对超稳激光专题**的评判偏好。冲突时，本文件的专题偏好**优先**用于本专题内的档位判定；跨专题讨论仍以全局规则为准。

---

## 1. 稳定度 > 线宽（Stability-over-Linewidth Principle）

### 1.1 原则

在超稳激光专题内，若需在多项"新纪录"信号中分辨主次，**系统稳定度与长期可靠性**的权重高于**瞬时线宽**。

### 1.2 判据

| 信号 | 对 `contribution_type` 的影响 |
|------|------------------------------|
| 打破 σ_y（mod σ_y、Allan 偏差、fractional frequency instability）纪录 | ✅ 支持 `breakthrough`（强信号） |
| 打破长期漂移纪录（drift rate、long-term σ_y @ ≥1000 s、hour-scale drift-free） | ✅ 支持 `breakthrough`（强信号） |
| 首次达到**子分支**热噪声极限（如光纤干涉仪、SHB、空心光纤） | ✅ 支持 `breakthrough`（强信号） |
| 提出可复用的系统可靠性机制（RAM 抑制、双折射噪声消除、振动灵敏度设计原理） | ✅ 支持 `breakthrough`（强信号） |
| 打破瞬时线宽纪录（sub-Hz、mHz 线宽），但 σ_y 未刷新 | ⚠ 单独不足以升为 `breakthrough`；保持 `evidence` |
| 工程紧凑化 / 传输封装 / 低功耗，但性能未跨越 regime | `evidence` |
| 换激光波长但复用同一稳频原理 | `evidence` |

### 1.3 动机

- 超稳激光在时间频率计量链中的价值在于**长时间维持频率定义**，而非单次窄谱测量
- 线宽受测量方法（Allan vs 光谱分析）、积分时间等选择影响，可比性弱于 σ_y
- 历史上数次"亚赫兹线宽新纪录"未带来下游光钟性能提升，而 σ_y 的每一次台阶都驱动了光钟迭代
- 因此在档位评审时，把"稳定度类新纪录"视作强 breakthrough 信号，"线宽类新纪录"视作工程延伸（evidence 默认）

### 1.4 边界

- 本原则用于**档位判定**（`breakthrough` vs `evidence`），**不**改变节点建模的优先级——指标节点的 `demonstrated_value` 仍应如实填入线宽、σ_y 等所有可量化项
- 本原则**不**适用于其他专题（光学频率梳的线宽与稳定度权重逻辑可能不同；频率标准以准确度优先；时间标尺以长期时间保持优先）

---

## 2. 后续可能增补的专题原则（占位）

> 列出未来可能需要在本文件沉淀的专题级偏好，待专家在 Round 2+ 确认后补写。

- 振动 vs 热噪声的权重（环境 vs 固有限制）
- "可搬运 / 空间级" 硬性 SWaP 约束是否可单独构成 breakthrough 维度
- 对 review/roadmap 的何种引用强度可升级一篇工程论文的档位

---

*本文件随专题演化更新；每轮修改请在顶部补版本字段并在 LOG.md 追加 `restructure` 条目。*
*创建：2026-04-21（Round 2 · 专家增补）*
