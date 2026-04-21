# 低温工程演化路线图

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，需要专家补充证据细节） · Round 3 σ_y-first 增订
> **涉及源文件**：kessler2012, matei2017, robinson2019, chen2025, lee2026, kedar2023
> **关联综合页**：[thermal_noise_landscape.md](thermal_noise_landscape.md), [stability_record_timeline.md](stability_record_timeline.md)（顶层导航）

---

## 🎯 本页对 σ_y(1 s) 主线的贡献

> 本页**回答**：**"降温这条路径，在 σ_y 主线上已经走到哪里、还能走多远？"**

| 温度工作点 | σ_y(1 s) 已实现 | σ_y(1 s) 理论极限（当前镀层） | 差距 | 主要瓶颈 |
|----------|----------------|-----------------------------|------|---------|
| 室温 (ULE CTE 零点) | 3×10⁻¹⁶ | ~10⁻¹⁶（ULE φ 主导） | 已达 | 基底损耗角 φ_ULE ~10⁻⁴ |
| 124 K (Si 第一零点 + IBS) | 4×10⁻¹⁷ | ~4×10⁻¹⁷ | 已达 | 镀层 φ_IBS ~4×10⁻⁴ |
| 124 K (Si + AlGaAs) | ~1×10⁻¹⁷（预期） | ~1×10⁻¹⁷ | 未达（待 Yu 2023 后续） | — |
| 17 K (Si + AlGaAs) 🏆 | 2.5×10⁻¹⁷ | ~1.5×10⁻¹⁷ | ~1.5× | AlGaAs 低温批次 φ |
| 4 K (Si + IBS) | ~4×10⁻¹⁷ (Chen 2025) | ~few×10⁻¹⁸（理论，若 AlGaAs） | ~10× | 振动、镀层未升级 |

**σ_y 主线启示**：降温路线的核心杠杆是 **热噪声 ∝ T（或 √T）**，但**仅当镀层 φ_coat 随之下降**时才转化为 σ_y 改善。17 K 和 4 K 工作点的真正收益在于"温度+晶体镀层"协同：
- **17 K**：已实现世界纪录 2.5×10⁻¹⁷
- **4 K**：未与 AlGaAs 协同（Chen 2025 仍用 IBS），故 σ_y 与 17 K 相当而非更优 → **下一步突破点**

详见 [breakthrough_paths_matrix.md](breakthrough_paths_matrix.md) §A.2 σ_y 增益矩阵的 "Si 4 K" 列。

---

## 一、问题

布朗热噪声公式给出 `S_ν ∝ T · φ / (stuff)`：降低 T 与降低 φ 是两条并行路径。硅单晶（Si）提供了一条独特的协同窗口：

1. **Si 的 CTE 存在零点**（124 K 和 17 K）→ 线性热漂移为零（`pri.silicon_cte_zero_crossing_124k` / `pri.silicon_cte_zero_crossing_17k`）
2. **Si 的机械 Q 随温度下降而增大**（`pri.cryogenic_mechanical_q_enhancement`）→ φ 下降
3. **Si 热导率高、比热适中** → 工程可实现

因此：**Si 单晶 FP 腔在低温点工作**成为进入 < 10⁻¹⁷ 的主流路线。

---

## 二、四个已演示温度工作点

| 工作温度 | 代表实体 | 论文 | mod σ_y | 关键特性 |
|---------|---------|------|---------|---------|
| **124 K** | `ent.si_crystal_fp_cavity_k12` | Kessler 2012 | ~1×10⁻¹⁶ | Si CTE 第一零点，液氮可达 |
| **124 K** (+AlGaAs 镀层) | 同上 | Matei 2017 | 4×10⁻¹⁷ | 首次叠加晶体镀层 |
| **17 K** (+AlGaAs) | `ent.si_crystal_17k_fp_cavity_l26` | Lee 2026 | **2.5×10⁻¹⁷** 🏆 | Si CTE 第二零点，更低 φ |
| **4 K** | `ent.si_crystal_fp_cavity_4k_r19` | Robinson 2019 | — | 极低 φ，工程复杂度高 |
| **< 5 K** (10 cm) | `ent.si_crystal_fp_cavity_sub5k_c25` | Chen 2025 | 4×10⁻¹⁷ | 10 cm 紧凑低温 |
| **124 K** (+ AlGaAs 深入) | — | Kedar 2023 | — | 晶体镀层低温长期测试 |

---

## 三、温度-性能权衡

随温度下降：

| 优点 | 挑战 |
|------|------|
| φ 下降（机械 Q 提升） | 冷却系统复杂、振动噪声 |
| 温度波动对频率的耦合（过零点）下降 | 材料特性数据稀少（如 < 10 K 下 AlGaAs 性能） |
| 黑体辐射降低 | 光学窗口、光纤馈入热漂移 |
| 分子吸附脱气下降 | 漏热控制、超导磁场干扰 |

**17 K 是目前的"甜蜜点"**：φ 已接近 4 K 水平，但工程上比 4 K 液氦系统简单得多，Lee 2026 一举创下世界纪录。

---

## 四、晶体镀层与低温协同

`pri.crystalline_coating_low_brownian_noise`（AlGaAs/GaAs，Cole 2013 室温 φ ≤ 2.5×10⁻⁵）

- 单独使用（室温）：性能改善因子 √(φ_IBS/φ_crystal) ≈ 4
- 叠加低温：φ 进一步下降，Lee 2026 测得 17 K AlGaAs 镀层 φ < 2.3×10⁻⁵
- 大面积挑战：Marchio 2018 演示 2 英寸晶体镀层光学性能 → 为长腔（`pri.long_cavity_thermal_noise_reduction`）开路

**Kedar 2023 是关键中间节点**：在 Kessler 2012 平台上长期测试 AlGaAs 镀层低温稳定性，是 Matei→Lee 演进的工程基础。

---

## 五、时间线（文字版）

```
2012 ─── 2017 ─── 2019 ─── 2023 ─── 2025 ─── 2026
Kessler  Matei    Robinson Kedar    Chen     Lee
124 K    124 K+   4 K Si   AlGaAs   <5 K     17 K + AlGaAs
Si 腔    AlGaAs   超低 φ   长期测试  10cm    2.5×10⁻¹⁷ 🏆
~10⁻¹⁶  4×10⁻¹⁷           低温镀层  4×10⁻¹⁷  世界纪录
```

---

## 六、开放问题

- **4 K 低温的工程-性能比**：Robinson 2019 是否能被 17 K 路线彻底取代？
- **次日量级（< 1 天）重启稳定性**：低温腔的启停循环对基准漂移影响仍缺乏系统数据
- **运输与低温结合**：迄今所有 < 10⁻¹⁷ 级系统都是实验室固定装置，可搬运低温腔（向 transportable fountain-like 系统迈进）是未竟挑战

---

## 七、推荐阅读顺序

```
1. Numata 2004  → 热噪声模型基础
2. Kessler 2012 → 低温 Si 腔首次演示
3. Cole 2013    → 晶体镀层独立通道
4. Matei 2017   → 两者叠加首胜
5. Lee 2026     → 17 K 优化 + 世界纪录
(可选) Robinson 2019 / Chen 2025 → 极限温度方向的两种回答
```

---

> 本综合页由 AI 基于 YAML + INDEX 草稿而成，需要专家逐条复核数值与年代。
