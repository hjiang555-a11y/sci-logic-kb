# 超稳激光专题 · 限制链缺口（Chain-Gap）审阅清单

> **生成方式**：`python scripts/lint.py --topic ultrastable-laser --json`（2026-04-21）
> **目的**：按「限制原理 → 受限实体 → 缺失 breakthrough_paths」分组，作为专家与 AI 共同审阅、逐条修复的工作底稿。
>
> **本文件性质**：派生报告（derived report），非 source of truth。修复完成后应同步更新对应 YAML 并重跑 lint。
>
> **使用说明**：
> - 🟢 建议直接补 `breakthrough_paths`（原文或领域共识已支持）
> - 🟡 建议标 `status: resolved`（该限制对当前实例已不再活跃）
> - 🟣 需要专家裁决（证据不充分或涉及争议）

---

## 一、总览

| 限制原理 | 受限实体 / 方法计数 | 占比 |
|-----------|------------|------|
| `pri.brownian_thermal_noise_fdt` | 17 | 81% |
| `pri.ram_pdh_frequency_offset` | 2 | 10% |
| `pri.fdl_locking_noise_nonlinearity` | 1 | 5% |
| `pri.fiber_thermal_phase_noise_giant_ifog` | 1 | 5% |
| **合计** | **21** | 100% |

> 超稳激光专题 lint warnings 细分：`orphan-node` 90 · `reasoning-chain-gap` 21 · `missing-conditions` 3。本报告仅覆盖 chain-gap 部分；orphan 清理见 [`reports/orphans_ultrastable.md`](orphans_ultrastable.md)。

---

## 二、按限制原理分组

### 🔴 Group 1 · `pri.brownian_thermal_noise_fdt`（布朗热噪声，17 条）

> **通用突破路径模板**（可被以下大多数实体引用，供专家勾选）：
>
> 1. `direction: pri.crystalline_coating_low_brownian_noise` — 晶体镀层降低 φ_coat（AlGaAs/GaAs，φ ≤ 2.5×10⁻⁵）
> 2. `direction: pri.cryogenic_mechanical_q_enhancement` — 低温工作（124 K Si、17 K Si、4 K Si）
> 3. `direction: pri.long_cavity_thermal_noise_reduction` — 增长腔长（σ_y ∝ 1/L，Häfner 2015 48 cm、Parke 2025 68 cm）
> 4. `direction: pri.optical_frequency_averaging` — 多腔频率平均（Lee 2026 双腔 √2 提升）
> 5. `direction: pri.beam_radius_scaling`（嵌入父原理 condition_variables）— 增大光斑面积

| 文件 | rel_id | 受限实体 | 原文论断摘录 | 建议动作 |
|------|--------|---------|-------------|---------|
| `argence2012.yaml` | rel.A03 | `ent.space_cavity_prototype_a12` | ~4×10⁻¹⁶ dominated by coating mechanical Q | 🟢 path 1 (晶体镀层) · path 2 (低温) |
| `chen2014.yaml` | rel.CHF03 | `ent.compact_transportable_cavity_c14` | calculated flicker floor σ_y = 4×10⁻¹⁶ | 🟢 path 1 · path 3 (长腔对紧凑型不适用，标 N/A) |
| `chen2020.yaml` | rel.CH02 | `ent.cubic_dual_cavity_c20` | thermal-noise limited σ_y = 4.3×10⁻¹⁶ | 🟢 path 1 · path 2 · path 4 (dual cavity averaging) |
| `chen2025.yaml` | rel.Che02 | `ent.si_crystal_fp_cavity_sub5k_c25` | fundamentally limited by Brownian thermal noise | 🟢 已是低温 Si，补 path 1 (AlGaAs 镀层未用) · 标 path 2 status: demonstrated |
| `didier2018.yaml` | rel.DD02 | `ent.ultracompact_pyramid_cavity_d18` | 10⁻¹⁷ at cost of complex systems | 🟣 超紧凑路线与突破路径有张力，专家裁决 |
| `hafner2020.yaml` | rel.HF20_03 | `ent.transportable_12cm_cavity_h20` | mod σ_y ≈ 3×10⁻¹⁶ thermal floor | 🟢 path 1 · path 2 (transportable 低温难度) |
| `jiang2011.yaml` | rel.JI02 | `ent.low_thermal_noise_cavity_j11` | Brownian thermal noise fundamental limit | 🟢 path 1 · path 2 · path 3 |
| `jin2018.yaml` | rel.JN02 | `ent.ule_cavity_30cm_578nm_j18` | approaching thermal-noise length instability | 🟢 已用长腔 (path 3 demonstrated)，补 path 1 · path 2 |
| `kedar2023.yaml` | rel.Ked03 | `ent.si_crystal_fp_cavity_k12` | Brownian noise from mirror dissipation | 🟢 path 1 (AlGaAs 晶体镀层，Kedar 2023 本身演示) status: demonstrated |
| `legero2010.yaml` | rel.Leg02 | `ent.fp_cavity_system` | 10 cm cavity flicker floor at 10⁻¹⁶ | 🟢 父节点级，补完整 path 1–5 |
| `li2018.yaml` | rel.LI02 | `ent.ule_cavity_30cm_sr_l18` | 10⁻¹⁶ stabilization | 🟢 path 1 · path 2 · path 3 (已 demonstrated) |
| `millo2009.yaml` | rel.Mil01 | `ent.fp_cavity_system` | lower than all-ULE noise floor | 🟢 path 1 · path 2 |
| `numata2004.yaml` | rel.N04 | `ent.mirror_coating` | coating contributes ~15% | 🟢 path 1 (晶体镀层直接针对镀层贡献) |
| `numata2004.yaml` | rel.N05 | `ent.spacer_ule` | spacer contributes ~1% | 🟡 spacer 贡献已次要，建议 status: resolved (not active bottleneck) |
| `tai2017.yaml` | rel.Tai01 | `ent.fp_cavity_system` | thermal fluctuation fundamental limit | 🟢 父节点级，同 legero2010 |
| `tao2018.yaml` | rel.T05 | `ent.robust_cuboid_cavity_t18` | close to thermal noise limit of 10 cm cavity | 🟢 path 1 · path 2 (transportable 约束视情况) |
| `webster2008.yaml` | rel.We08_01 | `ent.fp_cavity_system` | Brownian motion of substrate + coating | 🟢 父节点级，引用 Numata 分解作为起点 |

### 🟠 Group 2 · `pri.ram_pdh_frequency_offset`（RAM 诱导的 PDH 频偏，2 条）

> **候选突破路径**：
> 1. `pri.brewster_angle_ram_suppression`（Tai 2016，被动 RAM 抑制）
> 2. `meth.active_ram_servo` / `meth.dual_wavelength_ram_cancellation`（Zhang 2014 主动补偿）
> 3. `pri.waveguide_eom_low_ram`（材料/结构优化 EOM）

| 文件 | rel_id | 受限实体 / 方法 | 建议动作 |
|------|--------|-----------------|---------|
| `zhang2014_ram.yaml` | rel.Z14_01 | `meth.pdh_locking` | 🟢 path 1 · path 2 (本文演示 active servo) · path 3 |
| `zhang2014_ram.yaml` | rel.Z14_05 | `met.ram_fractional_instability` | 🟢 同上（指标层与方法层共享路径） |

### 🟣 Group 3 · `pri.fdl_locking_noise_nonlinearity`（光纤延迟线锁定白噪声，1 条）

| 文件 | rel_id | 受限实体 | 建议动作 |
|------|--------|---------|---------|
| `grabielle2025.yaml` | rel.GR01 | `ent.fiber_interferometer` | 🟣 候选路径：双平衡探测 / 前置放大降底噪 / 非线性抑制；需专家结合原文确认 |

### 🟣 Group 4 · `pri.fiber_thermal_phase_noise_giant_ifog`（巨型 IFOG 光纤热相噪声，1 条）

| 文件 | rel_id | 受限实体 | 建议动作 |
|------|--------|---------|---------|
| `li2019.yaml` | rel.LIG01 | `ent.fiber_interferometer` | 🟣 候选路径：空心光纤降热敏感性 · 温控改善 · 差分/双缠绕抵消；结合已有 `pri.hollow_core_fiber_thermal_noise` 引用 |

---

## 三、修复优先级建议

| 级别 | 条目数 | 说明 |
|------|-------|------|
| P0（可批量补） | ~14 | Group 1 中标 🟢 且指向三大成熟突破路径（晶体镀层 / 低温 / 长腔）的实例 |
| P1（单条精修） | 4 | Group 2 RAM 相关、Group 1 父节点（legero2010 / tai2017 / webster2008） |
| P2（专家裁决） | 3 | Group 3 / 4 / didier2018 |

---

## 四、执行后预期收益

- 推理链闭环率：71.3% → 预计 ≥ 85%（超出 Round 1 目标）
- 超稳激光 lint chain-gap warnings：21 → 0~3
- 为后续 `synthesis/breakthrough_paths_matrix.md` 提供现成的"限制×路径"矩阵源数据

---

## 五、操作建议（给 AI 执行者）

1. 按 P0 批量补 `breakthrough_paths`，每条含 `direction` / `expected_gain` / `status` / `source.claim`（引自论文讨论段或已有综合页）
2. 每次编辑后运行：`python scripts/lint.py --topic ultrastable-laser --summary`
3. 全部修复完成后重建 INDEX：`python scripts/build_index.py`
4. 在 LOG.md 追加 `## [YYYY-MM-DD] lint | Round 1-① chain-gap 批量修复`

> ⚠ **专家审核门**：P1/P2 条目必须由领域专家确认 status 与 direction；P0 条目可由 AI 基于本报告模板批量提 PR，但仍需专家签核合并。
