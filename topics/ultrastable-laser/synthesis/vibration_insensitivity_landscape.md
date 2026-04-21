# 振动不敏感设计路线全景

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，需要专家补充证据细节）
> **涉及源文件**：young1999, webster2007, millo2009, webster2011, chen2014, chen2020, sanjuan2019, tao2018, hafner2015, hafner2020, didier2018, herbers2022
> **关联综合页**：[thermal_noise_landscape.md](thermal_noise_landscape.md), [stability_record_timeline.md](stability_record_timeline.md)

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
| Chen 2014 | `ent.compact_transportable_cavity_c14` | STE-QUEST 紧凑可搬运 | 2×10⁻¹⁰ /g |
| Tao 2018 | `ent.robust_cuboid_cavity_t18` | 抗冲击方形 ULE | 5×10⁻¹¹ /g |
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
