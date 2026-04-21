# 超稳激光 σ_y 主线记录时间线 · 专题顶层导航

> **综合页面**：超稳激光专题的**顶层导航页**与 σ_y(τ=1 s) 主线记录总榜，跨论文综合视图（derived view），不替代 YAML 节点。YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · Round 3 σ_y-first 改造
> **涉及源文件**：young1999.yaml, numata2004.yaml, webster2008.yaml, millo2009.yaml, kessler2012.yaml, hafner2015.yaml, matei2017.yaml, lee2026.yaml, chen2025.yaml, dong2015.yaml, jeon2025.yaml, parke2025.yaml
> **状态**：🟢 当前（covers papers up to 2026-04-21）
>
> **适用主线规则**：超稳激光专题以 **σ_y(τ=1 s)** 为唯一主线指标（详见 [`_meta/scoping_principles.md` v2](../_meta/scoping_principles.md)）。本页对应的"世界纪录"与"子分支 SOTA"均以 σ_y(1 s) 锚定；线宽、加速度灵敏度、长期漂移仅为次要/工程指标，不进入主榜。

---

## 🧭 顶层导航 — 从"问题"跳转到专题视图

本页是超稳激光专题所有 synthesis 综合页的入口。当你打开一个具体研究问题时，按下表快速跳转：

| 你想查… | 进入哪一页 | 文件 |
|---------|-----------|------|
| 👉 σ_y(1 s) 历届最佳值演化 / 世界纪录榜 / 各子分支 SOTA | **本页（下方 §一 / §二 / §三）** | `stability_record_timeline.md` |
| 限制原理 × 突破路径的全矩阵（含 `expected_σy_gain` 列） | [限制 × 突破路径 矩阵](breakthrough_paths_matrix.md) | `breakthrough_paths_matrix.md` |
| 热噪声分解、基底 / 镀层 / 间隔物贡献、材料路线图 | [热噪声限制全景](thermal_noise_landscape.md) | `thermal_noise_landscape.md` |
| Si 低温 CTE 零点、124 K ↔ 17 K ↔ 4 K 路线选择 | [低温工程演化路线图](cryogenic_roadmap.md) | `cryogenic_roadmap.md` |
| 光纤干涉仪（FDL）/ 光纤延迟线 / 空心光纤分支 | [光纤稳频分支全景](fiber_stabilization_landscape.md) | `fiber_stabilization_landscape.md` |
| 光谱烧孔（SHB）分支 | [光谱烧孔稳频路线](spectral_hole_burning_track.md) | `spectral_hole_burning_track.md` |
| RAM、PDH 误差预算、伺服路径 | [RAM 与 PDH 误差预算全景](ram_and_pdh_error_budget.md) | `ram_and_pdh_error_budget.md` |
| 振动灵敏度 κ、隔振、对称几何、自平衡安装 | [振动不敏感设计路线全景](vibration_insensitivity_landscape.md) | `vibration_insensitivity_landscape.md` |

> **工具链导航**：
> - 机器可读索引：[`../INDEX.md`](../INDEX.md)（专题级，按角色分组）、[`../../../INDEX_metrics.md`](../../../INDEX_metrics.md)（全局，Primary/Secondary/Engineering/Enabling 角色分组）
> - 专题规则：[`../_meta/scoping_principles.md`](../_meta/scoping_principles.md) v2、[`../_meta/architecture.md`](../_meta/architecture.md)
> - 论文模板：[`../../../templates/ultrastable_laser_template.yaml`](../../../templates/ultrastable_laser_template.yaml)

---

## 一、σ_y(τ=1 s) 全局记录总榜（🏆 σ_y Hall of Fame）

> 唯一主线总榜。各条目标注 Allan 变体类型（ADEV / MDEV / OADEV / Hadamard），不同类型**不直接并列排序**，但可在同一表内追溯演化。

| 排名 | σ_y(1 s) | Allan 变体 | 年份 | 代表文件 | 使能配置 | 子分支 |
|------|---------|-----------|------|---------|---------|--------|
| 🥇 | **2.5×10⁻¹⁷** | mod σ_y | 2026 | [lee2026](../papers/lee2026.yaml) | 6 cm Si 腔 + AlGaAs + 17 K | FP 腔 |
| 🥈 | 4×10⁻¹⁷ | mod σ_y | 2017 | [matei2017](../papers/matei2017.yaml) | 21 cm Si 腔 + IBS + 124 K | FP 腔 |
| 🥉 | ≈4×10⁻¹⁷ | σ_y (τ=4–12 s) | 2025 | [chen2025](../papers/chen2025.yaml) | 10 cm Si 腔 + IBS + 4.9 K | FP 腔 |
| 4 | <1×10⁻¹⁶ | σ_y | 2015 | [hafner2015](../papers/hafner2015.yaml) | 48 cm ULE 长腔 + 室温 | FP 腔 |
| 5 | ~1×10⁻¹⁶ | mod σ_y | 2012 | [kessler2012](../papers/kessler2012.yaml) | 21 cm Si 腔 + IBS + 124 K | FP 腔 |
| 6 | 6×10⁻¹⁶ | σ_y | 2011 | Thorpe 2011 | Eu³⁺:YSO SHB | SHB |
| 7 | 6.3×10⁻¹⁵ | σ_y | 2025 | [jeon2025](../papers/jeon2025.yaml) | 自零差光纤干涉仪，4–200 Hz 热噪声极限 | 光纤 |
| 8 | 3×10⁻¹⁶ | σ_y | 1999 | [young1999](../papers/young1999.yaml) | 20 cm ULE + 室温 + PDH | FP 腔（历史） |

---

## 二、σ_y 子分支 SOTA

> 专题规则承认三个物理路线各有独立 breakthrough 地位（见 [scoping_principles.md](../_meta/scoping_principles.md) §1.7）。

| 子分支 | 当前 SOTA σ_y(1 s) | 代表论文 | 理论极限估计 | 距极限差距 |
|-------|--------------------|---------|-------------|-----------|
| **FP 腔（主流）** | 2.5×10⁻¹⁷ | Lee 2026 | ~10⁻¹⁸ 级（Si 4 K + 更低 φ 镀层批次） | ~25× |
| **光纤干涉仪（FDL / 自零差）** | 6.3×10⁻¹⁵ | Jeon 2025 | ~10⁻¹⁶–10⁻¹⁷（空心光纤 + 双缠绕） | ~100× |
| **光谱烧孔 SHB** | 6×10⁻¹⁶ | Thorpe 2011 (Eu:YSO) | ~10⁻¹⁷（Eu:YSO 低温 + 深井烧孔） | ~10× |

---

## 三、FP 腔稳定度演化详细里程碑

### 主线时间轴（σ_y 主线视角）

```
1999 ──── 2004 ──── 2008 ──── 2009 ──── 2012 ──── 2015 ──── 2017 ──── 2025/26
3×10⁻¹⁶   理论框架   热噪声   5.6×10⁻¹⁶  1×10⁻¹⁶   <1×10⁻¹⁶  4×10⁻¹⁷   2.5×10⁻¹⁷
Young      Numata    Webster   Millo      Kessler   Häfner   Matei     Lee
ULE/室温   FDT模型   FS验证   抗振ULE    Si/124K   48cm ULE  Si/124K   Si/17K+AlGaAs
                                                                       ★世界纪录
```

### 详细里程碑

| 年份 | σ_y (τ=1s) | 线宽（次要） | 使能技术 | 文献 | 意义 |
|------|-----------|------|---------|------|------|
| **1999** | 3×10⁻¹⁶ | 0.6 Hz | ULE 腔 + PDH + 弹性悬挂 | Young 1999 | 首次抵达热噪声极限 |
| **2004** | — | — | FDT 热噪声模型建立 | Numata 2004 | 理论框架：84%基底+15%镀层 |
| **2008** | ~2×10⁻¹⁶ | ~0.5 Hz | FS 镜基底替代 ULE | Webster 2008 | 首次全面验证热噪声模型 |
| **2009** | 5.6×10⁻¹⁶ | — | 振动不敏感腔设计 | Millo 2009 | 工程化抗振方案 |
| **2012** | ~1×10⁻¹⁶ | <40 mHz | **Si 单晶 124K** + 低温 | Kessler 2012 | 材料突破：Si+低温首次演示 |
| **2015** | <1×10⁻¹⁶ | — | 48 cm ULE 长腔 | Häfner 2015 | 室温路线：增长腔长降噪 |
| **2017** | **4×10⁻¹⁷** | 5–10 mHz | Si 124K + IBS 镀层 | Matei 2017 | 单腔记录，镀层极限暴露 |
| **2025** | ~4×10⁻¹⁷ | — | Si sub-5K + IBS 镀层 | Chen 2025 | 深低温路线验证 |
| **2026** | **2.5×10⁻¹⁷** | — | Si 17K + AlGaAs + 双腔平均 | Lee 2026 | **当前世界纪录** |

### 使能技术变化总结（σ_y 视角）

```
第一阶段（1999–2008）：ULE/FS 材料 + PDH 方法 → 热噪声极限首次抵达与验证
  ↓ 瓶颈：ULE/FS 损耗角 ~10⁻⁴–10⁻⁶，室温热噪声无法进一步降低
第二阶段（2012–2017）：Si 单晶 + 低温 124K → 1–2 个数量级改善
  ↓ 瓶颈：IBS 镀层损耗角 ~4×10⁻⁴ 成为新的主导限制
第三阶段（2023–2026）：AlGaAs 晶体镀层 + Si 17K/4K → 突破镀层极限
  ↓ 当前前沿：2.5×10⁻¹⁷，下一目标 10⁻¹⁸
```

---

## 四、光纤稳频稳定度演化

| 年份 | σ_y(1 s) | 线宽（次要） | 使能技术 | 文献 |
|------|--------|------|---------|------|
| **2009** | ~10⁻¹⁴ | — | 光纤延迟线锁频首次 | Kéfélian 2009 |
| **2015** | — | 0.67 Hz | FDL 亚赫兹线宽 | Dong 2015 |
| **2019** | — | 200 mHz | 全光纤 | Huang 2019 |
| **2023** | 1.1×10⁻¹⁴ 长期 | — | 全光纤，多层热屏蔽 | Huang 2023 |
| **2025** | **6.3×10⁻¹⁵** | — | 自零差，4–200 Hz 热噪声极限 | Jeon 2025 |

**光纤 vs FP 腔差距**：当前 FP 腔（2.5×10⁻¹⁷）vs 光纤（6.3×10⁻¹⁵），差距约 **250×**。但光纤方案在便携性、成本、工程化方面有显著优势。详见 [`fiber_stabilization_landscape.md`](fiber_stabilization_landscape.md)。

---

## 五、其他频率参考方案

| 方案 | 最佳 σ_y(1 s) | 优势 | 劣势 | 文献 |
|------|----------|------|------|------|
| SHB (Eu:YSO) | 6×10⁻¹⁶ | 低振动灵敏度 | 低温需求、光谱孔寿命 | Thorpe 2011 |
| 超辐射激光 | mHz 级（理论 → σ_y ~10⁻¹⁶级推测） | 无腔频率参考 | 理论阶段 | Meiser 2009 |
| 布里渊激光 | Hz 级 → σ_y ~10⁻¹³ 级 | 紧凑、低成本 | 稳定度较低 | Loh 2019 |
| Ramsey-Bordé 干涉仪 | <2×10⁻¹⁶ | 惯性参考 | 技术复杂度 | Olson 2019 |

---

## 六、σ_y 性能趋势预测

基于当前技术路线外推：

| 时间线 | 预期 σ_y(1 s) | 使能条件 |
|--------|----------|---------|
| 2026–2028 | ~10⁻¹⁷ | Si 4K + 改进 AlGaAs + 更好的低温恒温器 |
| 2028–2030 | few×10⁻¹⁸ | 新型超低损耗镀层 + 超大模场腔 + 多腔平均 |
| >2030 | 10⁻¹⁸ ? | 可能需要全新物理方案（超辐射激光？量子压缩？） |

---

## 七、关键开放问题（σ_y 主线）

1. **10⁻¹⁸ 瓶颈在哪？** 当热噪声降至 10⁻¹⁸ 级，其他噪声源（残余气体、光子散粒噪声、辐射压力）是否率先暴露？
2. **镀层极限**：AlGaAs 晶体镀层的损耗角能降到什么程度？低温下机械 Q 增强是否存在饱和？
3. **工程化**：实验室级 10⁻¹⁷ σ_y 能否被工程化为可搬运系统？
4. **替代路线**：光纤方案能否通过空心光纤突破 10⁻¹⁵ σ_y 屏障？

---

*本综合页面由 AI 生成，需专家审核。数据来源均为上述 YAML 文件中的已验证节点。*
