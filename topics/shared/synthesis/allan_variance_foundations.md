# Allan 方差族: 时频计量数学基础

> 基于 B9 批次 7 篇奠基论文 | 专题: shared | 最后更新: 2026-05-03

---

## 核心概念

频率稳定度的量化需要专门的统计工具——经典方差对幂律噪声发散，Allan 方差族解决了这一问题。

### 基础方差

| 方差类型 | 来源 | 核心贡献 |
|---------|------|---------|
| **σ²_y(τ)** (Allan 方差) | Allan 1966 | 两样本方差，对各类幂律噪声收敛 |
| **MDEV** (修正 Allan 方差) | Sullivan/Howe 1990 | 可区分 White PM 和 Flicker PM |
| **TDEV** (时间方差) | Sullivan/Howe 1990 | 时间域稳定度度量 |
| **OADEV** (重叠 Allan 方差) | Riley/Howe 2008 | 更高置信度的 Allan 方差估计 |
| **TOTDEV** (总方差) | Riley/Howe 2008 | 长 τ 区间改进估计 |
| **Theo1** (理论方差 #1) | Riley/Howe 2008 | 最长 τ 区间估计 |

---

## 幂律噪声五分类 (Allan 1987)

| 噪声类型 | α | S_y(f) ∝ | σ_y(τ) ∝ | 物理来源 |
|---------|---|----------|-----------|---------|
| White PM | 2 | f² | τ⁻¹ | 探测器散粒噪声、电子热噪声 |
| Flicker PM | 1 | f | τ⁻¹ | 电子闪烁噪声 |
| White FM | 0 | const | τ⁻½ | 激光自发辐射、热噪声底 |
| Flicker FM | -1 | 1/f | τ⁰ | 电子器件 1/f 噪声、腔漂移 |
| Random Walk FM | -2 | 1/f² | τ½ | 环境温度慢漂、老化 |

**诊断规则**: σ_y(τ) 在不同 τ 区间的斜率变化可识别主导噪声类型。

---

## 频域稳定度测量 (Howe 1976)

NBS Technical Note 679 建立了频域稳定度测量的标准方法:
- 相位噪声 PSD: S_φ(f) [rad²/Hz]
- 频率噪声 PSD: S_y(f) = (f/ν₀)² S_φ(f) [1/Hz]
- Allan 方差与 S_y(f) 的积分转换关系

---

## 使用规范 (本项目强制)

1. **报告 σ_y 必须标注 Allan 变体类型** (ADEV / MDEV / OADEV / Hadamard)
2. **不同 τ 区间的主导噪声类型不同** — 单点 σ_y(1s) 不能完整表征系统
3. **τ 范围选择**: 至少覆盖 1s 到 10,000s，完整展示噪声 floor 和长期漂移
4. **置信区间**: 估计值应附带 1σ 误差条 (OADEV 的标准方法)

---

## 参考文献

| 论文 | 年份 | 来源 |
|------|------|------|
| Allan — Statistics of Atomic Frequency Standards | 1966 | Proc. IEEE |
| Allan — Classical Variance vs Allan Variance | 1987 | IEEE TUFFC |
| Howe — Frequency Domain Stability Measurements | 1976 | NBS TN 679 |
| Sullivan/Allan/Howe/Walls — MDEV/TDEV/HDEV | 1990 | NIST TN 1337 |
| Riley/Howe — Handbook of Frequency Stability Analysis | 2008 | NIST SP 1065 |
| Allan & Levine — 50 Years of Allan Variance | 2016 | IEEE TUFFC |
| Sullivan et al. — NIST Primary Frequency Standards | 2001 | NIST JRES |

---

## 关联专题

- `ultrastable-laser`: σ_y 是核心性能指标 (`thermal_noise_landscape.md`)
- `frequency-standards`: 光钟频率稳定度表征
- `time-frequency-transfer`: 传递链路稳定度评估
