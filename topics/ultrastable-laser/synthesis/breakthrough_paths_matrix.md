# 限制 × 突破路径 矩阵（Breakthrough Paths Matrix）

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，随 chain-gap 修复同步演进）
> **来源数据**：`python scripts/graph.py --format json` + `reports/chain_gap_ultrastable.md`
> **关联综合页**：所有其他 synthesis 页面（本页是它们的"交叉索引"）

---

## 一、阅读指南

本页是一张**查询矩阵**：
- **行** = 限制原理（pri.*，活跃 BOUNDED-BY 的靶点）
- **列** = 已知突破路径（pri.* 或 meth.*）
- **单元格** = 路径的状态（`demonstrated` / `proposed` / `refuted`）+ 代表论文

目的：当你面对一个"10⁻¹⁶ 基准如何进一步提升"的问题时，可以直接定位**哪条限制仍未被哪条路径攻克**。

---

## 二、主矩阵（超稳激光主分支）

> 约定：✅ = 已演示 · 🟡 = 提出但待验证 · ⛔ = 已排除 · — = 不适用

### 限制 A · `pri.brownian_thermal_noise_fdt`（布朗热噪声）

| 路径 \ 条件 | ULE 室温 | Si 124 K | Si 17 K | Si 4 K | 长腔 (≥ 48 cm) |
|-------------|---------|----------|---------|--------|---------------|
| `pri.crystalline_coating_low_brownian_noise` | ✅ Cole 2013 | ✅ Matei 2017 / Kedar 2023 | ✅ Lee 2026 | 🟡 部分 | ✅ Marchio 2018 (大面积) |
| `pri.cryogenic_mechanical_q_enhancement` | — | ✅ Kessler 2012 | ✅ Lee 2026 | ✅ Robinson 2019 / Chen 2025 | 🟡 |
| `pri.long_cavity_thermal_noise_reduction` | ✅ Häfner 2015 (48 cm) | 🟡 | 🟡 | — | ✅ Parke 2025 (68 cm) |
| `pri.optical_frequency_averaging` | ✅ Chen 2020 (双腔) | 🟡 | ✅ Lee 2026 (Si2-Si3) | — | — |
| beam radius 增大（父原理字段） | ✅ 多数实现 | ✅ | ✅ | 🟡 | ✅ |

### 限制 B · `pri.ram_pdh_frequency_offset`（RAM 诱导频偏）

| 路径 | 状态 | 代表 |
|------|------|------|
| `pri.brewster_angle_ram_suppression` | ✅ | Tai 2016 |
| `meth.active_ram_servo` (待命名化) | ✅ | Zhang 2014 |
| 波导 EOM 低 RAM | 🟡 | 待论文摄入 |

### 限制 C · `pri.fiber_thermal_noise_wanser`（光纤热相噪声）

| 路径 | 状态 | 代表 |
|------|------|------|
| 空心光纤（HC-ARF/ULE-HCF） | ✅ | Michaud-Belleau 2022 / Ding 2025 |
| 双缠绕抵消 | ✅ | Huang JC 2019b |
| 温控与隔离 | ✅ | Dong 2015 (工程基础) |

### 限制 D · `pri.rayleigh_backscattering_noise`（Rayleigh 背散射）

| 路径 | 状态 | 代表 |
|------|------|------|
| AOM 外差频移区分 | ✅ | Jiang 2010 |
| 空心光纤低散射 | ✅ | Michaud-Belleau 2021 (`pri.hollow_core_fiber_low_backscattering`) |
| 短延迟 (tradeoff Q) | 🟡 | Jiang 2010 讨论 |

### 限制 E · `pri.acceleration_induced_length_change`（隐式，通过 CONDITIONED-BY）

| 路径 | 状态 | 代表 |
|------|------|------|
| 腔镜中心位移补偿 / 对称几何 | ✅ | Webster 2007 / 2011, Chen 2020, Sanjuan 2019 |
| 外部隔振 | ✅ | Young 1999 起多数实验 |
| 自平衡长腔安装 | ✅ | Häfner 2015 |

---

## 三、未关闭的限制链（从 chain_gap 报告提取）

截至 2026-04-21，以下限制关系**尚未在 YAML 中显式给出 `breakthrough_paths`**，即"矩阵上有理论可填但 YAML 尚空"的条目。修复目标见 [reports/chain_gap_ultrastable.md](../../../reports/chain_gap_ultrastable.md)：

| 限制 | 待补条目数 | 状态 |
|------|-----------|------|
| `pri.brownian_thermal_noise_fdt` | 17 | P0 批量补 |
| `pri.ram_pdh_frequency_offset` | 2 | P1 精修 |
| `pri.fdl_locking_noise_nonlinearity` | 1 | P2 专家裁决 |
| `pri.fiber_thermal_phase_noise_giant_ifog` | 1 | P2 专家裁决 |

---

## 四、查询用法示例

**问："我用 10 cm ULE 腔室温做到 5×10⁻¹⁶，下一步怎么走？"**

- 查行 A（热噪声）→ 当前限制是 `pri.brownian_thermal_noise_fdt`
- 查路径列：
  - 晶体镀层 → 最小工程代价，可直接替换（参考 Cole 2013）
  - 低温 Si → 升级最大但工程重（参考 Kessler 2012）
  - 长腔 → 室温内可行但体积代价（参考 Häfner 2015）
- 推荐路径组合：**晶体镀层 + 温控改善**（低风险）或 **低温 Si + 晶体镀层**（高收益）

---

## 五、演进机制

当 chain-gap 条目被修复（即 YAML 中补 `breakthrough_paths`），本页对应单元格应从"🟡 / —"升级到"✅ 论文引用"。建议：

- 每次 YAML 修改 PR 合并后，重跑 `scripts/graph.py` 重新计算限制链闭环率
- 在 LOG.md 记录 `synthesis | breakthrough_paths_matrix 刷新`
- 当某限制下所有路径都为 `demonstrated` 时，考虑把该限制标 `status: historically resolved` 并归档

---

> 本矩阵是超稳激光专题的"认知地图"，应作为新论文摄入时的**第一张检查表**：
> 新论文是否落在某个已知单元格（补证据）？还是发现了新路径（新列）？或新限制（新行）？
