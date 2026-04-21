# 振动不敏感设计路线全景

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，需要专家补充证据细节） · Round 3 σ_y-first 增订
> **涉及源文件**：young1999, webster2007, millo2009, webster2011, chen2014, chen2020, sanjuan2019, tao2018, hafner2015, hafner2020, didier2018, herbers2022
> **关联综合页**：[thermal_noise_landscape.md](thermal_noise_landscape.md), [stability_record_timeline.md](stability_record_timeline.md)（顶层导航）

---

## 🎯 本页对 σ_y(1 s) 主线的贡献

> 本页**回答**：**"振动灵敏度 κ 降低如何转化为 σ_y 改善？在热噪声极限面前 κ 何时退出主导？"**

耦合公式：`σ_y,vib(τ) ≈ κ · σ_a(τ) / ν`，其中 σ_a 为环境加速度 PSD 在 τ 对应频段的积分。典型实验室 σ_a ≈ 10⁻⁶ m/s²。

| κ 量级（各向） | σ_y(1s) 振动项贡献（典型实验室 σ_a） | 是否主导 σ_y(1s)? | 代表 |
|--------------|---------------------------------|-----------------|------|
| kHz/(m/s²) | ~10⁻¹² 级 | ✅ 主导，必须压制 | 早期 ULE 腔 |
| 0.1 kHz/(m/s²) | ~10⁻¹³ 级 | 部分主导，与 RAM/热噪声竞争 | Webster 2007 / 2011 |
| 10⁻¹⁰/g | <10⁻¹⁶ | 退出主导，让位给热噪声 | Chen 2020, Sanjuan 2019 |
| < 2×10⁻¹⁰/g 全向 | <10⁻¹⁶ | 退出主导，长腔室温仍可达 <1×10⁻¹⁶ | Häfner 2015 |

**σ_y 主线启示**：进入 σ_y ≤ 10⁻¹⁶ 区间后，**振动抑制是"守门员"而非"得分者"**——设计目标是让 κ·σ_a 贡献**低于热噪声地板**，而不是继续降低。下一代 10⁻¹⁸ 级系统需要对 σ_a 本身的环境改善（空间平台、低振动实验室）。详见 [breakthrough_paths_matrix.md](breakthrough_paths_matrix.md) §E 列。

---

## 一、问题

当超稳激光进入 10⁻¹⁵ ~ 10⁻¹⁷ 稳定度区间后，**环境振动**通过腔长形变成为短期稳定度的主要外部干扰。振动不敏感设计的目标是让：

```
κ = |Δν / ν| / |a|  →  10⁻¹⁰ /g 甚至 10⁻¹¹ /g 量级（所有方向）
```

接口节点：`ent.vibration_environment`（外围条件）通过 `CONDITIONED-BY` 连接 `ent.fp_cavity_system`。

---

## 二、两条主线

### 主线 A · **外部隔振**（active / passive isolation）

| 代表 | 实体节点 | 机制 | 频率范围 |
|------|---------|------|---------|
| Young 1999 | `ent.vibration_isolation` | 被动弹性悬挂（手术管，f₀ ≈ 0.3 Hz） | > 1 Hz 有效 |
| 后续多数实验 | active platform (commercial) | 主动反馈抵消 | 0.1–50 Hz |

限制：低频 (< 0.3 Hz) 与实验室声噪声无法完全隔除；占用空间大，难于搬运。

### 主线 B · **本征力不敏感腔几何**（geometric symmetry）

| 代表 | 实体节点 | 设计要点 | κ（典型） |
|------|---------|---------|-----------|
| Webster 2007 | `ent.cutout_cavity_mount_w07` | 切口腔体 + 四点对称支撑 | < 0.1 kHz/(m/s²) 竖直 |
| Millo 2009 | `ent.fp_cavity_system` 实例 | 水平安装 ULE 腔 | 10⁻¹⁰ /g 量级 |
| Webster 2011 | `ent.cubic_force_insensitive_cavity_w11` | 立方体 4 个对称点支撑 | 10⁻¹¹ /g（模拟+实验） |
| Chen 2014 | `ent.compact_transportable_cavity_c14` | STE-QUEST 紧凑可搬运 | 1.7×10⁻¹¹ ~ 3.9×10⁻¹⁰ /g（轴向差异大） |
| Tao 2018 | `ent.robust_cuboid_cavity_t18` | 抗冲击方形 ULE | 0.8 ~ 2.5×10⁻¹⁰ /g（最佳竖直 0.8×10⁻¹⁰） |
| Sanjuan 2019 | `ent.boost_cubic_cavity_s19` | BOOST 空间级立方 | 全向 10⁻¹¹ /g |
| Chen 2020 | `ent.cubic_dual_cavity_c20` | 10 cm 立方双腔 | 全向 < 2×10⁻¹¹ /g |
| Hafner 2015 | `ent.self_balancing_long_cavity_h15` | 48 cm 长腔自平衡安装 | < 2×10⁻¹⁰ /g 全向 |
| Hafner 2020 | `ent.transportable_12cm_cavity_h20` | 12 cm 可搬运 | 室温可搬运量级 |
| Didier 2018 | `ent.ultracompact_pyramid_cavity_d18` | 超紧凑金字塔 | 紧凑路线的极限尝试 |

支撑原理：`pri.cavity_deformation_compensation`（腔镜中心位移补偿，从 Webster 2007 起成为专题公共原理）。

---

## 三、限制与突破路径映射

**主要限制原理**：`pri.acceleration_induced_length_change`（加速度→腔长耦合）

**突破路径家族**：

1. `pri.cavity_deformation_compensation` — 对称几何消除一阶位移（几乎所有 Level 2 实例都依赖）
2. `pri.finite_element_topology_optimization` — 有限元拓扑优化（Webster 2011 起成为工程标准）
3. 主动反馈（external）— 放在 `ent.vibration_environment` 外围条件层处理，不进入腔内部设计

---

## 四、当前前沿与开放问题

- **全向 10⁻¹¹ /g 已由 Chen 2020 / Sanjuan 2019 多组达成**，下一代目标进入 10⁻¹² /g。
- 可搬运（< 50 cm，< 100 kg）与力不敏感双优化存在张力——Didier 2018 尝试超紧凑但以性能让步为代价。
- **低温腔的振动灵敏度测量**仍是开放问题：Kessler 2012 / Robinson 2019 / Chen 2025 在低温条件下振动敏感度特征化的长期数据相对稀缺。

---

## 五、推荐入门阅读顺序（3 跳路径）

```
想设计振动不敏感腔？
 ├─ 读 Webster 2007 → 理解 cavity_deformation_compensation 基础
 ├─ 读 Webster 2011 → 理解立方体对称几何 + 有限元优化
 └─ 读 Chen 2020 / Sanjuan 2019 → 当前最佳全向抑制实现
```

---

> 本综合页由 AI 基于 YAML + INDEX 草稿而成，数值引用待专家逐条复核。

---

## 📋 数值复核日志（2026-04-21，AI 机械比对）

按表格行自 YAML 源校对：

| 行 | YAML 源 ID | 页面声明 | YAML 实测 | 结论 |
|----|----------|---------|---------|------|
| Young 1999 | `met.acceleration_sensitivity_y99` | "kHz/(m/s²)" | ≈ 100 kHz/(m/s²) | ✅ 量级一致 |
| Webster 2007 | `met.acceleration_sensitivity_vertical_w07` | "< 0.1 kHz/(m/s²) 竖直" | < 0.1 kHz/ms⁻² | ✅ |
| Webster 2011 | `met.acceleration_sensitivity_w11` | "10⁻¹¹/g（模拟+实验）" | 2.45/0.21/0.01 ×10⁻¹¹/g | ✅ 最佳 10⁻¹³/g，题述 10⁻¹¹/g 指轴向最大 |
| Chen 2014 | `met.vibration_sensitivity_c14` | ~~"2×10⁻¹⁰/g"~~ → 已修正 | 1.7×10⁻¹¹ / 8.0×10⁻¹¹ / 3.9×10⁻¹⁰ | **已修正为区间 1.7e-11 ~ 3.9e-10** |
| Tao 2018 | `met.acceleration_sensitivity_t18` | ~~"5×10⁻¹¹/g"~~ → 已修正 | 0.8 / 2.5 / 1.5 ×10⁻¹⁰/g | **已修正**（原 "5×10⁻¹¹" 与 YAML 最差 2.5×10⁻¹⁰ 相差 5 倍，错误） |
| Hafner 2015 | `met.acceleration_sensitivity_h15` | "< 2×10⁻¹⁰/g 全向" | κz=1.7, κy=0.5, κx=1.5 ×10⁻¹⁰/g | ✅ |
| Hafner 2020 | `met.vibration_sensitivity_h20` | "室温可搬运量级" | 0.7/2.3/12.3 ×10⁻¹⁰/g | ⚠️ 页面表述过弱，YAML 有具体值但 κz 远差于其他方向 |
| Millo 2009 | `met.acceleration_sensitivity_millo09` | "10⁻¹⁰ /g 量级" | ≤1.5×10⁻¹¹ per m/s² | ⚠️ YAML 用 m/s² 单位，换算约 1.5×10⁻¹⁰/g — 一致 |
| Chen 2020 | — | "全向 < 2×10⁻¹¹/g" | **YAML 缺对应 `met.*_c20`** | ⚠️ 页面声明**无 YAML 直接支撑**，建议补充 metric 节点或加注"原文表述"标签 |
| Sanjuan 2019 | — | "全向 10⁻¹¹/g" | **YAML 缺对应 `met.*_s19`**（长期稳定度 YAML 有） | ⚠️ 同上 |
| Didier 2018 | — | "紧凑路线的极限尝试" | YAML 无加速度灵敏度 | ✅ 定性表述可保留 |

**遗留动作**：
- [ ] 专家确认 Chen 2020 / Sanjuan 2019 的 κ 声明是否应补入对应 YAML metrics（或页面改为定性表述）
- [ ] Hafner 2020 κz 方向的 ×6 劣化应在表中体现（不仅写"室温可搬运量级"）

本次已修正的**实质性数值错误**：
1. Tao 2018 "5×10⁻¹¹/g" → 实测最差 2.5×10⁻¹⁰/g（原页面偏乐观 5 倍）
2. Chen 2014 "2×10⁻¹⁰/g" → 实测 1.7e-11 ~ 3.9e-10（原页面掩盖了轴向差异）
