# 超稳激光专题 · Orphan 节点 · v2（阶段 B 档位感知重估）

> **🏁 状态（2026-04-21，阶段 C 完成后）：15 条 breakthrough-tier WARNING 已全部清零**
>
> - 14 个 orphan method 节点 + 1 个 orphan principle（`pri.ram_bias_field_cancellation`）均已在阶段 C 挂上至少一条关系（IMPLEMENTS / OPERATIONALIZED-AS / ENABLED-BY / CHARACTERIZED-BY 等）；
> - 75 条 evidence/framework 档位 INFO 按 §9.1 保留，不强制挂接；
> - 详见 `LOG.md`「[2026-04-21] lint \| 阶段 C 落地」条目。
> - 本文件保留为阶段 C 前的工作底稿，下表动作栏已加 ✅ 完成标记。

---

> **生成方式**：`python scripts/lint.py --topic ultrastable-laser --json`（2026-04-21，阶段 B 完成后）
>
> **变更说明**：v1（2026-04-21）统计出 90 个 orphan。阶段 B（v4.4 档位感知）按论文 `contribution_type` 归并：只有 **breakthrough** 档位论文定义的 orphan 计为真实工作项（WARNING），`evidence` / `framework` 档位的 orphan 降级为 `INFO`（符合 SCHEMA §9.1 — evidence 档位允许 orphan 存在）。
>
> **v2 真实缺口：15 条 WARNING + 75 条 INFO**（总 90 未变，但性质重新归类）。
>
> v1 报告保留于 [`orphans_ultrastable.md`](orphans_ultrastable.md) 作为历史存档。

---

## 一、真实 orphan（breakthrough-tier · 15 条 WARNING · ✅ 阶段 C 已清零）

### 1.1 方法节点（14 条）

| 文件 | 节点 ID | 建议治理 |
|------|---------|---------|
| `cole2013.yaml` | `meth.substrate_transferred_crystalline_coating_c13` | ✅ 阶段 C `rel.C07`：`ent.algaas_crystalline_mirror_c13 IMPLEMENTS meth.*` |
| `hafner2015.yaml` | `meth.self_balancing_mount_h15` | ✅ 阶段 C `rel.H04a`：`ent.self_balancing_long_cavity_h15 IMPLEMENTS meth.*` |
| `huang2023.yaml` | `meth.multilayer_thermal_shielding_fdl_h23` | ✅ 阶段 C `rel.HU05`：`ent.fiber_interferometer IMPLEMENTS meth.*` |
| `kedar2023.yaml` | `meth.dual_polarization_suppression_kedar23` | ✅ 阶段 C `rel.Ked04`：`met.fractional_freq_instability_kedar23 OPERATIONALIZED-AS meth.*` |
| `michaudbelleau2022.yaml` | `meth.hcf_thermal_noise_characterization_mb22` | ✅ 阶段 C `rel.MB22_03`：`met.thermal_noise_psd_hcf_mb22 OPERATIONALIZED-AS meth.*` |
| `numata2004.yaml` | `meth.thermal_noise_analysis_fp_cavity_num04` | ✅ 阶段 C `rel.N15`：`met.thermal_noise_freq_psd OPERATIONALIZED-AS meth.*` |
| `parke2025.yaml` | `meth.eom_bias_field_ram_cancellation_p25` | ✅ 阶段 C `rel.P07 / P08`：`meth ENABLED-BY pri.ram_bias_field_cancellation` + `IMPLEMENTS meth.pdh_locking` |
| `parke2025.yaml` | `meth.long_fp_cavity_design_fabrication_p25` | ✅ 阶段 C `rel.P06`：`ent.long_cavity_68cm_p25 IMPLEMENTS meth.*` |
| `robinson2019.yaml` | `meth.low_power_cavity_drift_characterization_r19` | ✅ 阶段 C `rel.R12`：`met.cavity_frequency_drift_r19 OPERATIONALIZED-AS meth.*` |
| `thorpe2011.yaml` | `meth.two_stage_shb_fp_lock_thorpe11` | ✅ 阶段 C `rel.TH03`：`met.shb_stability_thorpe11 OPERATIONALIZED-AS meth.*` |
| `webster2008.yaml` | `meth.vibration_insensitive_cavity_lock_w08` | ✅ 阶段 C `rel.We08_04`：`met.fractional_freq_instability_w08 OPERATIONALIZED-AS meth.*` |
| `yan2018.yaml` | `meth.multi_cavity_frequency_averaging_y18` | ✅ 阶段 C `rel.YA02`：`met.synthesized_laser_instability_y18 OPERATIONALIZED-AS meth.*` |
| `zhang2014_ram.yaml` | `meth.dual_channel_ram_cancellation_z14` | ✅ 阶段 C `rel.Z14_04a / 04b`：`meth ENABLED-BY pri.ram_active_cancellation` + `IMPLEMENTS meth.pdh_locking` |

### 1.2 指标节点（1 条）

| 文件 | 节点 ID | 建议治理 |
|------|---------|---------|
| `thorpe2011.yaml` | `met.shb_environmental_sensitivity_thorpe11` | ✅ 阶段 C `rel.TH02`：`ent.shb_eu_yso_reference_l13 CHARACTERIZED-BY met.*` |

### 1.3 原理节点（1 条）

| 文件 | 节点 ID | 建议治理 |
|------|---------|---------|
| `parke2025.yaml` | `pri.ram_bias_field_cancellation` | ✅ 阶段 C `rel.P07`：`meth.eom_bias_field_ram_cancellation_p25 ENABLED-BY pri.*`（同条关系一并解除 meth 与 pri 双 orphan） |

---

## 二、降级为 INFO 的 orphan（evidence-tier · 75 条）

> 这些节点定义在 `contribution_type: evidence` 的论文里；按 SCHEMA §9.1，evidence 档位允许 orphan。lint 输出形如：
>
> `[INFO] <file>: Node '<id>' is defined but never referenced in any relation (tier=evidence; orphan allowed per §9.1)`
>
> 完整清单可通过 `python scripts/lint.py --topic ultrastable-laser --json` 过滤 `level==INFO && category==orphan-node` 获取（75 条不逐条列出以免混淆优先级）。

分布概览（按文件，Top 10）：

| 文件 | INFO orphan 数 | 备注 |
|------|---------------|------|
| `hafner2020.yaml` | ~8 | 可搬运低温系统实例 |
| `kedar2023.yaml` | ~6 | Si 腔实例指标 |
| `jin2018.yaml` | ~5 | ULE 30cm 578nm |
| `chen2020.yaml` | ~5 | 立方双腔 |
| `chen2025.yaml` | ~4 | Sub-5K Si 腔 |
| `lee2026.yaml` | ~4 | 双腔平均 |
| 其他 ~20 文件 | ≤3 each | — |

> ⚠ 上述数字为粗略分布，以 lint 最新输出为准。

---

## 三、治理建议（v2）

### P0 · 真实缺口的 15 条（breakthrough-tier WARNING）

- 全部为"方法 / 指标 / 原理在 breakthrough 论文内但缺一条出边关系"
- 典型补法：每条加 1–2 条关系即可解除 orphan（`OPERATIONALIZED-AS` / `IMPLEMENTS` / `CHARACTERIZED-BY` / `ENABLED-BY`）
- 预计总工作量：一轮 PR 可完成

### P1 · INFO 级 75 条

- **不是阶段 B 的强制关闭项**
- 建议在专家审核某批 evidence 论文重入库时顺手补关系；或在未来"桶 A/B/C 归属专家会审"时集中处理
- 目标仍参考 v1：总 orphan ≤ 30（含 P0 清零后的 INFO 残留）

---

## 四、阶段 B 收尾条件

- ✅ 已完成：lint / stats 引入档位感知，真实缺口重新定级
- ⏳ 推荐后续：清零 15 条 breakthrough-tier orphan WARNING（一轮 PR）
- 📋 延后：75 条 INFO 级 orphan 留待 C 阶段"精准收敛"按专家节奏处理

---

*v2 报告生成于 2026-04-21 阶段 B 完成后；请勿在本文件手工增删——重跑 `lint.py --json` 即可刷新。*
