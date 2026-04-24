# 光谱烧孔（SHB）稳频旁路路线

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，SHB 分支尚未系统整合，本页既是综合也是下一步工作清单） · Round 3 σ_y-first 增订
> **涉及源文件**：konz2003, leibrandt2013, gobron2017, galland2020, thorpe2011, cook2015, kartner1995, braun1995
> **关联综合页**：[stability_record_timeline.md](stability_record_timeline.md)（顶层导航）

---

## 🎯 本页对 σ_y(1 s) 主线的贡献

> 本页**回答**：**"SHB 作为 FP 腔之外的第三条子分支，当前 σ_y SOTA、理论极限与差距何在？"**

| 子分支 σ_y(1 s) | 年份 | 配置 | 代表论文 |
|--------------|------|------|---------|
| 6×10⁻¹⁶ 🏆（子 SOTA） | 2011 | Eu³⁺:YSO SHB 频率参考，~4 K | Thorpe 2011 |
| 理论预期 ~10⁻¹⁷ | — | Eu:YSO 低温 + 深井烧孔 + 长相干原子系综 | — |

**SHB vs FP 腔 σ_y 差距**：当前子 SOTA 6×10⁻¹⁶ vs FP 腔 SOTA 2.5×10⁻¹⁷，差距 **~24×**。但 SHB 分支在**振动不敏感性**和**绝对频率参考（原子跃迁）**两方面具结构性优势，工程级 σ_y 可能更易可搬运化。

**σ_y 主线瓶颈**：
- 光谱孔寿命（线性漂移） → 需低温 + 长相干晶体
- 测量噪声地板（激发-探询循环 Dick 效应）
- 待扩展的限制原理：本专题 SHB 子分支 YAML 节点尚不完整（见本页"下一步工作清单"）

详见 [stability_record_timeline.md](stability_record_timeline.md) §二 "σ_y 子分支 SOTA"。

---

## 一、SHB 与 FP 腔 / 光纤的定位关系

**光谱烧孔（Spectral Hole Burning, SHB）频率参考**（`ent.shb_eu_yso_reference_l13`）是与 FP 腔、光纤干涉仪并列的 Level 1 频率参考方案，但采用**完全不同的物理载体**：

| 维度 | FP 腔 | 光纤延迟线 | SHB 晶体 |
|------|-------|-----------|----------|
| 参考物理量 | 光学腔谐振频率 | 延迟相位 | 晶体稀土离子跃迁频率 |
| 受限类型 | 热噪声（力学） | 热噪声（光纤） | 激发寿命 / 光谱漂移 |
| 温度域 | 室温 / 124 K / 17 K / 4 K | 室温 | 液氦（~4 K） |
| 绝对参考 | 否（FSR 为参考） | 否 | 部分（原子跃迁） |

SHB 的吸引力：利用稀土离子（Eu³⁺ 等）在 Y₂SiO₅ 等宿主晶体中的**超窄光谱孔**（寿命数小时到数天）作为"刻录式"频率参考。

---

## 二、核心节点

### 实体
- `ent.shb_eu_yso_reference_l13` — Eu³⁺:Y₂SiO₅ SHB 参考（Leibrandt 2013）

### 原理
- `pri.dispersive_heterodyne_shb` — 色散外差探测光谱烧孔稳频（Gobron 2017）
- `pri.double_heterodyne_shb_probing` — 双外差探测 SHB 方案（Galland 2020）
- `pri.enhanced_shb_dynamics_theory_k95` — 增强 SHB 动力学理论（Kärtner 1995，foundational）
- `pri.enhanced_shb_pulse_shortening_b95` — 增强 SHB 脉冲缩短机制（Braun 1995，foundational）

### 指标
- `met.eu_yso_t2_k03` — Eu:YSO 相干时间（Konz 2003 基础数据）

---

## 三、主要发展节点

| 年份 | 贡献 | 论文 | 意义 |
|------|------|------|------|
| 1995 | SHB 动力学理论 + 脉冲缩短 | Kärtner 1995 / Braun 1995 | 理论奠基（当前孤立原理，尚未接入 SHB 实用主干） |
| 2003 | Eu:YSO 相干时间测量 | Konz 2003 | 基础晶体物理参数 |
| 2011 | 早期 SHB 稳频探索 | Thorpe 2011 (cf. OFC 分支也引用) | 方法可行性 |
| 2013 | SHB 稳频系统演示 | Leibrandt 2013 | 首个完整 Eu:YSO 锁定系统 |
| 2015 | SHB 相关探测技术 | Cook 2015 | 探测方案拓展 |
| 2017 | 色散外差 SHB 稳频 | Gobron 2017 | 信噪比显著改善 |
| 2020 | 双外差 SHB 探测 | Galland 2020 | 抑制技术噪声的新范式 |

---

## 四、当前架构的问题与整治建议

**现状诊断**（见 [reports/active/orphans_ultrastable.md](../../../reports/active/orphans_ultrastable.md)）：
- Kärtner 1995 / Braun 1995 / Konz 2003 的原理与指标节点处于孤立状态
- Leibrandt 2013 的 SHB 实体只是单点节点，未显式承载 BOUNDED-BY / ENABLED-BY 结构

**整治建议**：
1. **建立 SHB 子分支限制链**：至少补一条 `ent.shb_eu_yso_reference_l13 BOUNDED-BY pri.shb_hole_lifetime_limit`（新原理节点，从文献抽提）
2. **连接基础理论**：将 Kärtner / Braun 的理论节点通过 `DERIVED-FROM` 关系接入 SHB 主原理族
3. **方法层补全**：Cook 2015 / Gobron 2017 / Galland 2020 的探测方法应 `OPERATIONALIZED-AS` 对应稳定度指标

---

## 五、与主流路线的互补性

SHB 相对 FP 腔/低温路线的核心互补价值：
- **绝对频率参考**：SHB 跃迁是原子级，长期漂移原则上远低于 FP 腔 FSR 漂移
- **小体积可能**：晶体尺度 < 1 cm³，天然紧凑（但需要低温）
- **极长相干时间**：hole 寿命可达数小时

目前主要瓶颈：探测信噪比、长期重复性、与主流光梳/钟系统的耦合。

---

## 六、开放问题（必须由专家补全）

- SHB 参考目前达到的最佳稳定度与 FP 腔差距？
- SHB 是否可以作为 FP 腔长期漂移的独立校准参考？
- 在低温 Si 腔进入 10⁻¹⁸ 量级的未来，SHB 的独立价值是否会被取代？

---

> 本综合页由 AI 基于 YAML + INDEX 草稿而成，**SHB 分支是超稳激光专题中结构化程度最低的部分**，最需要专家补充。

---

## 📋 数值复核日志（2026-04-21）

SHB 页面本身含数值声明较少，以**结构化缺口**为主。AI 机械复核仅能识别以下：

- SHB 相关 YAML 论文：`thorpe2011`, `leibrandt2013`, `cook2015`, `gobron2017`, `galland2020`, `braun1995` 等 6~7 篇
- 多数 paper-local SHB 原理/方法节点属 orphan（仅本文件内使用，未跨文件共用）——见 `reports/active/shared_node_candidates.md` Tier 3
- 页面中的数值声明均为**定性/量级**，未发现与 YAML 明显矛盾的条目

**SHB 专题需专家补全的核心问题**（TODO 已标记）：
- 页面 §六 的三个开放问题（SHB vs FP 差距、SHB 作为 FP 长期漂移的独立校准、10⁻¹⁸ 时代 SHB 的独立价值）
- 是否应把 `pri.dispersive_heterodyne_shb` / `pri.double_heterodyne_shb_probing` 等 SHB 专门原理正式登记为超稳激光专题公共节点（当前 Tier 1 0 个 SHB 节点）

**AI 机械复核结论**：无可修正的数值错误；保持 🟡 draft 待专家深度介入。
