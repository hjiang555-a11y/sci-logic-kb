# GitHub Copilot 任务说明 — sci-logic-kb 超稳激光知识提取

> **当前优先任务（SCHEMA v2.0 重整）**：在处理新论文之前，必须先按新 Schema 重整已有的 5 篇论文。见第一节。

---

## 【第一优先】重整已有 5 篇论文（SCHEMA v2.0）

**背景**：Schema 已从 v1.0 升级到 v2.0，关系类型和节点字段有重大变更。已有 5 篇 YAML 需要按新规范重写。

### 重整顺序

| 顺序 | 文件 | 重整重点 |
|------|------|---------|
| 1 | `papers/numata2004.yaml` | BOUNDED-BY 关系原型（含 breakthrough_paths）；DERIVED-FROM 原理层级 |
| 2 | `papers/young1999.yaml` | 跨论文 temporal_role: validates；CONDITIONED-BY 外围条件接口 |
| 3 | `papers/drever1983.yaml` | ENABLED-BY 原型；合并 FP 腔实体 |
| 4 | `papers/shaddock1999.yaml` | COMPETES-WITH（Tilt vs PDH）；元原理 DERIVED-FROM 链 |
| 5 | `papers/jiang2010.yaml` | CONDITIONED-BY（光纤分支外围条件）；COMPETES-WITH（光纤 vs FP腔） |

### 每篇重整的具体变更

**所有文件通用变更：**

1. **废弃 `GOVERNED-BY`**，替换为：
   - `ENABLED-BY`：当该原理解释"为什么方法能工作"（机制）
   - `BOUNDED-BY`：当该原理设定"性能上限在哪"（极限）

2. **所有实体节点新增字段**：
   ```yaml
   hierarchy_level: 1      # 1=主分支实体，2=子单元，ext=外围条件
   status: demonstrated    # demonstrated | theoretical | obsolete
   ```

3. **所有原理节点新增字段**：
   ```yaml
   tier: domain            # meta=元原理 | domain=领域原理 | engineering=工程推论
   verification_status: calculated   # observed | calculated | inferred
   ```

4. **BOUNDED-BY 必须包含完整结构**：
   ```yaml
   - predicate: BOUNDED-BY
     object: pri.some_principle
     is_system_limit: true/false
     dominated_by: null              # 若 false，填写压制它的原理 ID
     quantitative_contribution: "X%" # 若已知
     regime: all                     # all | short-term | long-term | during-sweep
     verification_status: observed   # observed | calculated | inferred
     temporal_role: null             # proposes | validates | refutes | extends
     breakthrough_paths:             # 当 is_system_limit: true 时填写
       - direction: pri.or_meth.xxx
         expected_gain: "预期改善"
         status: demonstrated        # demonstrated | theoretical | speculative
         source: {zotero_key: "KEY"}
   ```

**numata2004.yaml 特定变更：**
- N09/N10/N11 已修正（PART-OF 方向正确）
- 新增 DERIVED-FROM 链：
  - `pri.mirror_substrate_noise_dominance DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `pri.beam_radius_scaling DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `pri.low_loss_substrate_improvement DERIVED-FROM pri.brownian_thermal_noise_fdt`
- `ent.rigid_fp_cavity` 改名为 `ent.fp_cavity_system`，hierarchy_level: 1
- `ent.spacer_ule` 保留但标注 `is_system_limit: false, dominated_by: pri.mirror_substrate_noise_dominance`
- 所有 GOVERNED-BY → BOUNDED-BY（含完整字段，包括 breakthrough_paths）

**young1999.yaml 特定变更：**
- `ent.ule_fp_cavity_young99` 改为引用 `ent.fp_cavity_system`（作为 reference_implementation 实例）
- `ent.vibration_isolated_table_young99` 改为 `ent.vibration_isolation`，hierarchy_level: 2
- 新增 CONDITIONED-BY 关系：
  ```yaml
  subject: ent.fp_cavity_system
  predicate: CONDITIONED-BY
  object: ent.vibration_environment   # 外围条件节点，新建
  interface_metric: met.frequency_noise_from_vibration   # 新建接口指标
  coupling_formula: "Δν = acceleration_sensitivity × ambient_acceleration"
  internal_property: "acceleration_sensitivity: ~100 kHz/(m/s²)"
  ```
- rel.N08 跨论文关系（Young 1999 结果在热噪声极限）：
  - 改为 BOUNDED-BY，temporal_role: validates

**drever1983.yaml 特定变更：**
- `ent.fp_cavity_reference` 改名为 `ent.fp_cavity_system`（与 numata 合并为同一节点）
- 所有 GOVERNED-BY → ENABLED-BY（PDH 的机制类原理）
- `pri.shot_noise_frequency_limit` 改为 BOUNDED-BY 关系

**shaddock1999.yaml 特定变更：**
- 新增 COMPETES-WITH 关系：
  ```yaml
  subject: meth.tilt_locking
  predicate: COMPETES-WITH
  object: meth.pdh_locking
  context: "FP腔误差探测方法选择"
  tradeoffs:
    subject_wins: ["无需EOM/RF源/混频器", "量子噪声极限相同", "适合空间应用"]
    object_wins: ["伺服带宽>1MHz", "成熟度高", "工程经验丰富"]
  ```
- `pri.off_resonance_reference_light` 标注 tier: meta
- 新增 DERIVED-FROM：`pri.gouy_phase_discrimination DERIVED-FROM pri.off_resonance_reference_light`

**jiang2010.yaml 特定变更：**
- `ent.fiber_interferometer` 新增 hierarchy_level: 1
- 新增 COMPETES-WITH：
  ```yaml
  subject: ent.fiber_interferometer
  predicate: COMPETES-WITH
  object: ent.fp_cavity_system
  context: "频率参考选择"
  tradeoffs:
    subject_wins: ["可捷变扫频", "无精密装调", "成本低", "工程化友好"]
    object_wins: ["长期稳定度3×10⁻¹⁶", "热噪声极限更低", "绝对频率参考"]
  ```
- 删除 J10（已废弃的猜测性关系）
- J09 已修正（CHARACTERIZED-BY 方向）
- 新增外围条件节点 `ent.thermal_environment`（外围条件层）
- 光纤分支的温度耦合物理不同于 FP 腔：Δν ∝ T × (dn/dT) × L，需单独接口指标

### 重整后提交格式

```
git add papers/{filename}.yaml
git commit -m "refactor {author}{year}: update to SCHEMA v2.0

- Replace GOVERNED-BY with ENABLED-BY/BOUNDED-BY
- Add hierarchy_level, status, tier, verification_status fields
- [paper-specific changes]

Co-Authored-By: GitHub Copilot"
```

---

## 【第二优先】处理新 PDF（重整完成后）

按以下顺序处理 `pdfs/` 目录中的论文：

| 优先级 | PDF 文件 | 说明 |
|--------|---------|------|
| 1 | `TVY7T59A_matei2017.pdf` | Matei 2017 — 1.5μm 10mHz 线宽 |
| 2 | `YKPFKDD9_kessler2012.pdf` | Kessler 2012 — Si 单晶腔 |
| 3 | `CWIHQRJD_cole2013.pdf` | Cole 2013 — 晶体镀层降低热噪声 |
| 4 | `UCNS7EM7_webster2007.pdf` | Webster 2007 — 防振 FP 腔 |
| 5 | `VU2V2PTX_webster2004.pdf` | Webster 2004 — 热噪声极限实验 |
| 6 | `A96XGR82_webster2011.pdf` | Webster 2011 — 力不敏感腔 |
| 7 | `MW3RDB68_legero2010.pdf` | Legero 2010 — CTE 调谐 |
| 8 | `UV6S5FFL_hafner2015.pdf` | Häfner 2015 — 8×10⁻¹⁷ |
| 9 | `GLXHEIPV_millo2009.pdf` | Millo 2009 — 防振腔超稳激光 |
| 10 | `H5MYBTXH_leibrandt2011.pdf` | Leibrandt 2011 — 加速度灵敏度 |
| 11 | `JIZCUZLY_robinson2019.pdf` | Robinson 2019 — 4K 晶体腔 |
| 12 | `8YK6EH22_kedar2023.pdf` | Kedar 2023 — 低温 Si 腔 |
| 13 | `4GUXEM2C_cole2016.pdf` | Cole 2016 — 高性能晶体镀层 |
| 14 | `N6HILT6B_chen2025.pdf` | Chen 2025 — 4×10⁻¹⁷（最新） |
| 15 | `MN54T4F3_kefelian2009.pdf` | Kefelian 2009 — 光纤延迟线 |
| 16 | `W8K5GLK6_dong2015.pdf` | Dong 2015 — 光纤延迟亚赫兹 |
| 17 | `JYGVFJBN_huang2023.pdf` | Huang 2023 — 全光纤超稳激光 |
| 18 | `4GT5VD54_michaudbelleau2022a.pdf` | Michaud-Belleau 2022 |
| 19 | `DD6SE43C_michaudbelleau2021.pdf` | Michaud-Belleau 2021 |
| 20 | `AHUZI4A7_tai2017.pdf` | Tai 2017 — 可搬运超稳激光 |

---

## 处理新论文的步骤

### 1. 阅读 PDF（重点）

- **摘要**：核心贡献一句话
- **引言**：问题定义，与已有工作关系
- **方法/实验**：技术路线，核心装置参数
- **结果**：关键数值 + 测量条件
- **讨论**：适用范围、限制、改进方向（这是 BOUNDED-BY + breakthrough_paths 的来源）

### 2. 查询已有节点

查看 `papers/` 目录所有文件，确认以下核心节点是否已存在（直接引用，不重定义）：
- `ent.fp_cavity_system`（主 FP 腔节点）
- `pri.brownian_thermal_noise_fdt`（热噪声根本原理）
- `pri.pdh_heterodyne_detection`（PDH 原理）
- `pri.off_resonance_reference_light`（元原理）
- `met.laser_linewidth`、`met.fractional_freq_instability_y99`（基准指标）

### 3. 确定新节点归属

每个新节点必须明确：
- `hierarchy_level`（1=主分支 / 2=子单元 / ext=外围条件）
- `status`（demonstrated / theoretical）
- 是否与已有节点存在 COMPETES-WITH 关系

### 4. 重点建立 BOUNDED-BY 链

对每个新的性能指标，必须追问：
1. 什么原理限制它？（BOUNDED-BY）
2. 这个限制当前是否活跃？（is_system_limit）
3. 如何突破？（breakthrough_paths）
4. 这篇论文对已有知识的角色？（temporal_role）

### 5. 提交

```
git add papers/{filename}.yaml QUEUE.md
git commit -m "add {author}{year}: {核心贡献一句话}"
git push
```

---

## Schema v2.0 关系类型速查

| 谓词 | 用途 | 典型例子 |
|------|------|---------|
| `PART-OF` | 组件归属 | mirror_substrate PART-OF fp_cavity_system |
| `CHARACTERIZED-BY` | 实体→指标 | fp_cavity CHARACTERIZED-BY met.linewidth |
| `OPERATIONALIZED-AS` | 指标→方法 | met.linewidth OPERATIONALIZED-AS meth.pdh |
| `ENABLED-BY` | 方法→机制原理 | meth.pdh ENABLED-BY pri.pdh_heterodyne |
| `BOUNDED-BY` | 任意→限制原理 | fp_cavity BOUNDED-BY pri.brownian_fdt |
| `DERIVED-FROM` | 原理层级 | pri.beam_radius DERIVED-FROM pri.brownian_fdt |
| `CONDITIONED-BY` | 实体→外围条件 | fp_cavity CONDITIONED-BY ent.vibration_env |
| `COMPETES-WITH` | 同级并列方案 | fp_cavity COMPETES-WITH fiber_interferometer |
| `BREAKTHROUGH-VIA` | 限制→突破路径 | pri.brownian BREAKTHROUGH-VIA pri.low_loss_substrate |

**禁止使用**：`GOVERNED-BY`、`EQUIVALENT-IN-CONTEXT`、`SUPPORTED-BY`

---

## 领域背景

**核心性能指标**（重要性递减）：
1. 分数频率不稳定度 σ_y(τ)（Allan 偏差）
2. 激光线宽（Hz）
3. 频率噪声谱密度 S_ν(f)（Hz²/Hz）

**当前性能前沿**（2026年）：
- FP腔最佳：~4×10⁻¹⁷（Chen 2025，低温Si腔+晶体镀层）
- 光纤方案最佳：~10⁻¹⁴ 量级（与FP腔差约3个量级）

**热噪声突破路径（已建立的知识链）**：
- 镜底物：ULE(φ~10⁻⁵) → 熔融石英(φ~10⁻⁷) → Si单晶(低温, φ更低)
- 镀层：Ta₂O₅/SiO₂ → AlGaAs晶体镀层（Cole 2013/2016）
- 腔型：室温ULE → 低温Si（Robinson 2019, Kessler 2012）
- 几何：增大光束半径 w₀（噪声∝1/w₀）

---

*Schema v2.0 | 更新：2026-04-14*
