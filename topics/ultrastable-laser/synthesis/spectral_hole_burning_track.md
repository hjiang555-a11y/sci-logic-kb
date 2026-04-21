# 光谱烧孔（SHB）稳频旁路路线

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，SHB 分支尚未系统整合，本页既是综合也是下一步工作清单）
> **涉及源文件**：konz2003, leibrandt2013, gobron2017, galland2020, thorpe2011, cook2015, kartner1995, braun1995
> **关联综合页**：[stability_record_timeline.md](stability_record_timeline.md)

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

**现状诊断**（见 [reports/orphans_ultrastable.md](../../../reports/orphans_ultrastable.md)）：
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
