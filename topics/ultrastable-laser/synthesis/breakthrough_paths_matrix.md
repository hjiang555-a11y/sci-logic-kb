# 限制 × 突破路径 矩阵（Breakthrough Paths Matrix）

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，阶段 C 后数值复核完成） · Round 3 σ_y-first 增订（新增 §A.2 σ_y 增益矩阵）
> **来源数据**：`python scripts/graph.py --format json` + `reports/chain_gap_ultrastable.md`
> **关联综合页**：所有其他 synthesis 页面（本页是它们的"交叉索引"） · [stability_record_timeline.md](stability_record_timeline.md)（顶层导航）

---

## 🎯 本页对 σ_y(1 s) 主线的贡献

> 本页**回答**：**"我当前 σ_y 落在某个量级，下一步哪条路径能把它往下推一档？"**

本页是专题的"突破策略查询矩阵"。v4.4 Round 3 σ_y-first 改造后，每条 BOUNDED-BY 关系的 `breakthrough_paths[*]` 均建议补 `expected_σy_gain` 字段（见 [`templates/ultrastable_laser_template.yaml`](../../../templates/ultrastable_laser_template.yaml)），使矩阵可以**按 σ_y 影响定量排序**：
- **§A.2 σ_y 增益矩阵** 是本次新增的核心表格，明确每条热噪声突破路径对 σ_y(1 s) 的已验证/预期贡献
- **§B–E** 其他限制类型的每条路径也补充了 `expected_σy_gain` 列（按当前 YAML 已有数据或论文论断填写）

所有 `expected_σy_gain` 数值均追溯到 YAML `breakthrough_paths[*].expected_σy_gain` 字段；未填写时标"indirect"或"—"，待 YAML 回写补齐。

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

#### A.1 状态矩阵（路径 × 条件）

| 路径 \ 条件 | ULE 室温 | Si 124 K | Si 17 K | Si 4 K | 长腔 (≥ 48 cm) |
|-------------|---------|----------|---------|--------|---------------|
| `pri.crystalline_coating_low_brownian_noise` | ✅ Cole 2013 | ✅ Matei 2017 / Kedar 2023 | ✅ Lee 2026 | 🟡 部分 | ✅ Marchio 2018 (大面积) |
| `pri.cryogenic_mechanical_q_enhancement` | — | ✅ Kessler 2012 | ✅ Lee 2026 | ✅ Robinson 2019 / Chen 2025 | 🟡 |
| `pri.long_cavity_thermal_noise_reduction` | ✅ Häfner 2015 (48 cm) | 🟡 | 🟡 | — | ✅ Parke 2025 (68 cm) |
| `pri.optical_frequency_averaging` | ✅ Chen 2020 (双腔) | 🟡 | ✅ Lee 2026 (Si2-Si3) | — | — |
| beam radius 增大（父原理字段） | ✅ 多数实现 | ✅ | ✅ | 🟡 | ✅ |

#### A.2 σ_y 增益矩阵（`expected_σy_gain` 列，v4.4 新增）

> 每条路径对 σ_y(τ=1 s) 主线的预期/已验证影响。来源为 YAML 中 `breakthrough_paths[*].expected_σy_gain` 字段；
> 未填写时标 "—"，需后续 YAML 回写时补充。

| 路径 | 基线（Before） | 已验证/预期 σ_y gain | 参考论文 |
|------|---------------|---------------------|---------|
| `pri.crystalline_coating_low_brownian_noise` @ Si 124 K | 4×10⁻¹⁷ (Matei 2017) | → 2.5×10⁻¹⁷ (4× 预期，Lee 2026 部分实现 ~1.6×) | matei2017.yaml |
| `pri.crystalline_coating_low_brownian_noise` @ Si 17 K | 1×10⁻¹⁶ (dielectric预期) | → 2.5×10⁻¹⁷ (4× 改善 demonstrated) | lee2026.yaml |
| `pri.cryogenic_mechanical_q_enhancement` @ 17K→4K | 2.5×10⁻¹⁷ (Lee 2026) | → ~10⁻¹⁸ 级（热噪声 ∝ √T，≈2× 改善，theoretical） | lee2026.yaml |
| `pri.long_cavity_thermal_noise_reduction` @ 10cm→48cm | ~3×10⁻¹⁶ (10 cm ULE) | → <1×10⁻¹⁶ (σ_y ∝ 1/L，demonstrated) | hafner2015.yaml |
| `pri.optical_frequency_averaging`（双腔平均） | 2.5×10⁻¹⁷ | → 1.8×10⁻¹⁷ (√2 提升，demonstrated) | lee2026.yaml |
| beam radius 增大（父原理字段） | — | 线性抑制基底贡献，σ_y 改善非主导 | numata2004.yaml |

### 限制 B · `pri.ram_pdh_frequency_offset`（RAM 诱导频偏）

| 路径 | 状态 | 代表 | expected_σy_gain |
|------|------|------|------------------|
| `pri.brewster_angle_ram_suppression` | ✅ | Tai 2016 | σ_RAM ~ppm → κ·σ_RAM/ν ≈ 10⁻¹⁶ 级抑制 |
| `meth.active_ram_servo` (待命名化) | ✅ | Zhang 2014 | σ_y 从 >10⁻¹⁵ → ~10⁻¹⁶（消除 κ=28kHz/(m/s²) 的 RAM 偏置） |
| 波导 EOM 低 RAM | 🟡 | 待论文摄入 | indirect |

### 限制 C · `pri.fiber_thermal_noise_wanser`（光纤热相噪声）

| 路径 | 状态 | 代表 | expected_σy_gain |
|------|------|------|------------------|
| 空心光纤（HC-ARF/ULE-HCF） | ✅ | Michaud-Belleau 2022 / Ding 2025 | σ_y: ~10⁻¹⁴ → 10⁻¹⁵ 级（光纤分支 SOTA） |
| 双缠绕抵消 | ✅ | Huang JC 2019b | σ_y 约 2–3× 改善 |
| 温控与隔离 | ✅ | Dong 2015 (工程基础) | σ_y 温度敏感项抑制 |

### 限制 D · `pri.rayleigh_backscattering_noise`（Rayleigh 背散射）

| 路径 | 状态 | 代表 | expected_σy_gain |
|------|------|------|------------------|
| AOM 外差频移区分 | ✅ | Jiang 2010 | 使 FDL σ_y 达 10⁻¹⁴ 成为可能 |
| 空心光纤低散射 | ✅ | Michaud-Belleau 2021 | indirect（耦合至 C 路径 σ_y gain） |
| 短延迟 (tradeoff Q) | 🟡 | Jiang 2010 讨论 | σ_y 可能恶化（Q ↓） |

### 限制 E · `pri.acceleration_induced_length_change`（隐式，通过 CONDITIONED-BY）

| 路径 | 状态 | 代表 | expected_σy_gain |
|------|------|------|------------------|
| 腔镜中心位移补偿 / 对称几何 | ✅ | Webster 2007 / 2011, Chen 2020, Sanjuan 2019 | κ 从 kHz/g 级 → 0.1 kHz/g 级，σ_y 振动项抑制 >10× |
| 外部隔振 | ✅ | Young 1999 起多数实验 | σ_y 低频项抑制 |
| 自平衡长腔安装 | ✅ | Häfner 2015 | κ<2×10⁻¹⁰/g；σ_y <10⁻¹⁶ 全域 |

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

---

## 📋 阶段 C 后刷新日志（2026-04-21）

阶段 C 基于 `reports/chain_gap_ultrastable_v2.md` / `reports/orphans_ultrastable_v2.md` 对 7 条 breakthrough chain-gap 与 15 条 breakthrough orphan 全部闭环：

- `chen2025.Che02` · `kedar2023.Ked03` · `numata2004.N04/N05` · `webster2008.We08_01` · `zhang2014_ram.Z14_01/Z14_05` 全部补入 `breakthrough_paths`
- 15 个 breakthrough orphan 节点（14 methods + 1 principle `pri.ram_bias_field_cancellation`）全部挂关系

**对矩阵单元格的影响**：

| 矩阵位置 | 阶段 C 前 | 阶段 C 后 |
|---------|---------|---------|
| A 限制 · Si 4 K × `pri.crystalline_coating_low_brownian_noise` | 🟡 部分 | 🟡 保持（Chen 2025 仍用 IBS 非 AlGaAs，是 cryogenic_roadmap §三 4 K 行的下一步突破点） |
| A 限制 · Si 17 K × `pri.crystalline_coating_low_brownian_noise` | ✅ Lee 2026 | ✅ + Kedar 2023（Si6 @ 16 K 佐证补入）|
| B 限制 · Active RAM Servo | ✅ Zhang 2014 | ✅ + Parke 2025 breakthrough（σ_y 3×10⁻¹⁹ @ 10–100s，`pri.ram_bias_field_cancellation` 首次演示） |
| 振动限制 × 双腔差分 | ✅ Chen 2020 | ✅ 保持（`met.vibration_sensitivity_c14` 等有 YAML 数据） |

**下一轮刷新触发条件**：
- 新 breakthrough 论文摄入（尤其 Si 4 K + AlGaAs 协同）
- 专家确认 Tier 3 节点合并动作后，若有 breakthrough orphan 重新浮现则需回填

**AI 数值复核结论**：矩阵结构在阶段 C 后无遗留错误；YAML source of truth 已同步。
