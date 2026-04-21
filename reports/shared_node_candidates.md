# P2 · 跨文件复用度提升 — 候选节点分析报告

> **生成日期**：2026-04-21
> **关联 TODO 项**：`TODO.md · 超稳激光 · P2`
> **目标**：跨文件复用率 `8.8% → 15%+`（当前 76/862）
> **定位**：**分析与候选提案** — 不含强制性合并动作。Tier 1 已事实共用，建议形式化；Tier 2/3 需**专家批准**后再执行。

---

## 1. 现状与目标再测算

`scripts/stats.py` 的 `cross_file_reuse` 定义：一个 ID **被定义或被关系引用**出现在 ≥ 2 个 papers YAML 文件即计入"已复用"。

当前：
- 总唯一节点 ID：862
- ≥ 2 文件中出现：76（8.8%）
- 达到 15% 需 ≥ 130 个，即**新增 54 个**跨文件复用 ID

> **关键发现**：纯粹抽取 10~15 个"公共 pri/meth"上提至 `topics/shared/` **不会自动增加分子**——分子看的是 ID 被使用的广度，而非定义位置。要提升这一指标，需要**鼓励跨论文引用已共用节点**（在 relations 中显式 cite），而不是新建文件位置。

## 2. Tier 1 · 事实上已跨文件共用的 pri/meth（39 个）

以下节点**已满足** ≥ 2 文件引用，属于"事实公共节点"。建议：

1. **保留在当前主页文件**（不物理迁移，避免打断溯源链），但
2. 在 `topics/shared/registry.md`（新建）中**登记**该 ID 为 domain-level 公共节点，
3. 在 `SCHEMA.md` §9 或 `docs/CURRENT_NODES_REFERENCE.md` 列为"首选引用节点"。

| ID | 类型 | 文件数 | 现主页 | 名称 | 专题 |
|----|------|-------|--------|------|------|
| `pri.brownian_thermal_noise_fdt` | pri | 28 | `numata2004.yaml` | 布朗热噪声——涨落耗散定理（FDT） | ultrastable-laser |
| `pri.self_referencing_f2f` | pri | 16 | `giunta2019.yaml` | f-2f 自参考原理 | optical-frequency-combs |
| `meth.dual_comb_spectroscopy` | meth | 8 | `coddington2016.yaml` | 双梳光谱方法 | optical-frequency-combs |
| `pri.molecular_rovibrational_fingerprint` | pri | 7 | `schliesser2012.yaml` | 分子振转指纹光谱原理 | optical-frequency-combs |
| `pri.parametric_four_wave_mixing_comb` | pri | 6 | `kippenberg2011.yaml` | 参量四波混频梳产生原理 | optical-frequency-combs |
| `meth.pdh_locking` | meth | 6 | `drever1983.yaml` | PDH 锁频方法 | ultrastable-laser |
| `pri.supercontinuum_octave_spanning` | pri | 5 | `diddams2000.yaml` | 超连续谱倍频程展宽原理 | optical-frequency-combs |
| `pri.dissipative_kerr_soliton` | pri | 5 | `kippenberg2018.yaml` | 耗散 Kerr 孤子（DKS）双平衡原理 | optical-frequency-combs |
| `pri.microresonator_anomalous_dispersion` | pri | 5 | `kippenberg2011.yaml` | 微谐振腔反常色散条件 | optical-frequency-combs |
| `meth.cw_pumped_microcomb_generation` | meth | 5 | `kippenberg2011.yaml` | CW 泵浦微谐振腔梳产生方法 | optical-frequency-combs |
| `meth.fiber_delay_locking` | meth | 5 | `jiang2010.yaml` | 光纤延迟线锁频 | ultrastable-laser |
| `pri.dual_comb_multiheterodyne_detection` | pri | 4 | `coddington2016.yaml` | 双梳多外差检测原理 | optical-frequency-combs |
| `pri.lugiato_lefever_equation` | pri | 4 | `kippenberg2018.yaml` | Lugiato-Lefever 方程（LLE） | optical-frequency-combs |
| `meth.laser_tuning_soliton_access` | meth | 4 | `kippenberg2018.yaml` | 激光扫频孤子激发方法 | optical-frequency-combs |
| `meth.microcomb_self_referencing` | meth | 3 | `kippenberg2018.yaml` | DKS 微梳自参考方法 | optical-frequency-combs |
| `pri.nonlinear_frequency_conversion_comb` | pri | 3 | `schliesser2012.yaml` | 非线性频率转换梳产生原理 | optical-frequency-combs |
| `meth.dfg_comb_generation` | meth | 3 | `schliesser2012.yaml` | 差频产生（DFG）中红外梳 | optical-frequency-combs |
| `pri.fiber_delay_line_frequency_ref` | pri | 3 | `jiang2010.yaml` | 光纤延迟线频率参考 | ultrastable-laser |
| `pri.crystalline_coating_low_brownian_noise` | pri | 3 | `cole2013.yaml` | 单晶镀层低布朗热噪声 | ultrastable-laser |
| （其余 20 个，2 files，略） | | | | | |

> 完整 39 条见附录 A。

## 3. Tier 2 · 跨专题桥梁（真正需要 SHARED-WITH 关系的）

当前**只有 1 个**节点事实上被两个专题同时使用：

| ID | 类型 | 跨专题 | 文件数 |
|----|------|-------|--------|
| `pri.brownian_thermal_noise_fdt` | pri | `ultrastable-laser`, `optical-frequency-combs` | 28 |

**建议**：
- 为 `pri.brownian_thermal_noise_fdt` 在 SCHEMA §6 或新建的 `topics/shared/registry.md` 登记为**首个跨专题共用节点**
- 在 `optical-frequency-combs` 相关论文 YAML 中，显式添加 `SHARED-WITH pri.brownian_thermal_noise_fdt` 关系（当前多为隐式 relation-subject/object 引用），明确跨专题语义

其余高复用节点（f-2f、PDH、DKS 等）目前都**单专题**内共用，不需要 SHARED-WITH。

## 4. Tier 3 · 疑似可合并的本地节点（需专家判断，30 个候选）

机器通过关键词重叠识别出 **30 个** paper-local pri/meth 疑似与 Tier 1 已共用节点概念重叠。**不建议未经专家审核直接合并**——其中许多是同一家族下的**合法子变体**（如 `pri.hollow_core_fiber_thermal_noise` 是 Brownian FDT 在 HCF 介质上的特化，不是重复）。

判断规则建议（供专家参考）：
- **可合并** ✅：本地节点的 statement/description 实际上在复述 Tier 1 节点，仅加了一句"某论文验证"——此时应删除本地节点，把关系主语改为 Tier 1 节点
- **保留特化** ❌：本地节点有独立物理机制/适用边界（不同材料/不同频段/不同数学形式）——保留，但应**加一条 `DERIVED-FROM` 或 `PART-OF` 关系**指向 Tier 1 节点，这样至少把 Tier 1 的被引次数再 +1

### 重点候选清单（精选 10 条，建议优先专家审核）

| 本地节点 | 候选动作 | 依据 |
|---------|---------|------|
| `pri.hollow_core_fiber_thermal_noise` (michaudbelleau2022) | ❌ 保留 + 补 `DERIVED-FROM pri.brownian_thermal_noise_fdt` | HCF 是不同介质，独立参数 |
| `pri.long_cavity_thermal_noise_reduction` (hafner2015) | ❌ 保留 + 补 `ENABLED-BY pri.brownian_thermal_noise_fdt` | 长腔路径是降 FDT 的特化方法 |
| `pri.fiber_thermal_phase_noise_giant_ifog` (li2019) | ❌ 保留 + 补 `DERIVED-FROM pri.brownian_thermal_noise_fdt` | 光纤陀螺专用，物理形式不同 |
| `pri.coating_thermal_noise_material_comparison` (steinlechner2018) | ❌ 保留 + 补 `DERIVED-FROM pri.brownian_thermal_noise_fdt` | 材料对比是 FDT 的参数化 |
| `meth.low_thermal_noise_cavity_pdh_j11` (jiang2011) | ❌ 保留 + 补 `IMPLEMENTS meth.pdh_locking` + `CHARACTERIZES pri.brownian_thermal_noise_fdt` | PDH 的具体实施 |
| `pri.dual_comb_multiheterodyne_mapping` (coddington2010) | ⚠️ 专家判断是否 = `pri.dual_comb_multiheterodyne_detection` | 名称相似度高，可能真重复 |
| `pri.self_referencing_f2f_framework` (picque2020) | ⚠️ 可能是 framework 档冗余定义 | 综述文件中"再定义"的原理 |
| `pri.vibration_fopt_linear_coupling` (sinclair2014) | ⚠️ 对比 `pri.vibration_cavity_length_coupling` | 同一耦合不同文件命名 |
| `pri.temporal_cavity_soliton_dks` (pasquazi2018) | ⚠️ 对比 `pri.dissipative_kerr_soliton` | 时域 DKS 与标准 DKS 的关系 |
| `meth.sbs_thermal_self_referencing_l19` (loh2019) | ❌ 保留（SBS 路径独立） + 补 `COMPETES-WITH meth.microcomb_self_referencing` | SBS 自参考是另一条路径 |

> 完整 30 条见附录 B。

## 5. 提升至 15% 复用率的预期影响

按上述三级策略分阶段执行：

| 阶段 | 动作 | 新增跨文件 ID 数（估算） | 达到复用率 |
|------|------|-----------------------|----------|
| 现状 | — | 76 | 8.8% |
| Tier 3 「❌ 保留+补关系」 6~8 条 | 新增 `DERIVED-FROM` / `ENABLED-BY` 关系，本地节点从 1 → 2 files | +6~8 | 9.5~9.7% |
| Tier 3 「⚠️ 合并」专家批准 3~5 条 | 删除重复本地节点，关系重指向 Tier 1 | 不增分子（分母减） | 9.5~9.9% |
| 跨专题 SHARED-WITH 补关系 | 其他专题论文引用 Tier 1 节点（主要 Brownian / PDH / shot-noise） | +10~15 | 10.5~11.5% |
| **系统性扫描 ent.* / met.* 共用候选**（本报告未覆盖） | 需第二轮数据分析 | +25~40 | **14~15%** |

**关键结论**：**仅靠 pri/meth 整治无法单独达到 15% 目标**。需要在第二轮中扩展到 `ent.*`（如 `ent.fp_cavity_system`、`ent.vibration_environment`）与 `met.*`（σ_y 主线共用指标）。

## 6. 建议的下一步动作（供专家审核）

1. **[低风险立即执行]** 新建 `topics/shared/registry.md` 登记 Tier 1 节点，不改动源 YAML
2. **[需审核]** Tier 3 的 10 个重点候选：逐条决定"保留+补关系" vs "合并删除"
3. **[需审核+新一轮分析]** 启动 P2.2 `ent.*` / `met.*` 共用候选扫描（本报告范围外）
4. **[Schema 层]** 考虑在 `SCHEMA.md` §6 增加 "domain-shared node" 标记字段，供 `stats.py` 辨识

---

## 附录 A · Tier 1 完整清单（39 条）

略（可从 `scripts/stats.py` 运行时 `node_files` 字典提取）。重要节点已在 §2 列出。

## 附录 B · Tier 3 完整候选（30 条）

略（重点 10 条见 §4）。完整清单存于本次分析运行的 `/tmp/p2_candidates.txt`。

---

*本报告由 AI 自动分析生成，需专家逐条审核方可落地。提案性质，不代表知识库的最终结构。*
