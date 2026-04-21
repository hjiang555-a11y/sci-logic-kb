# Shared Node Registry — 跨文件共用节点首选引用清单

> **定位**：本文件登记**事实上已跨 ≥ 2 papers YAML 文件使用**的 `pri.*` / `meth.*` 节点。
>
> **作用**：
> - AI 在摄入新论文时，遇到这些概念应**优先引用**本清单节点，**而非**新建 paper-local 节点
> - 专家审核 PR 时可快速识别是否有"重复定义"风险
>
> **生成方式**：由 `scripts/stats.py` 统计 `node_files[id] >= 2` 节点；未来考虑自动化产出（见 P2 报告 §6）
>
> **最后手工复核**：2026-04-21（Round 3 结束 + 阶段 C 后 + **P2 Tier 3 合并落地**）
>
> **变更记录（2026-04-21 晚批次，P2 Tier 3 批准落地）**：
> - 3 个局部重复节点已合并到 Tier 1 规范节点（本地定义删除，关系重定向）：
>   - `pri.dual_comb_multiheterodyne_mapping` → `pri.dual_comb_multiheterodyne_detection`
>   - `pri.self_referencing_f2f_framework` → `pri.self_referencing_f2f`
>   - `pri.temporal_cavity_soliton_dks` → `pri.dissipative_kerr_soliton`
> - 因此 Tier 1 清单中三条规范节点的「使用文件数」各 +1（`dual_comb_multiheterodyne_detection` 4→5、`self_referencing_f2f` 16→17、`dissipative_kerr_soliton` 5→6）——本表下次自动扫描时同步
>
> **关联文档**：
> - 完整分析报告：[`../../reports/shared_node_candidates.md`](../../reports/shared_node_candidates.md)
> - Tier 2 跨专题桥梁说明：见本文件 §3
> - Tier 3 合并候选（待专家判断）：[`../../reports/shared_node_candidates.md#4-tier-3`](../../reports/shared_node_candidates.md)

---

## 1. 使用规范

1. **不物理迁移源文件**：节点仍定义在"现主页文件"，此处仅为引用注册表。迁移会打断现有 `source.claim` 的溯源链。
2. **新论文引用方式**：在 `relations:` 中直接以现有 ID 作为 `subject` / `object` 即可；不需要在 `entities/principles/methods` 段复述定义。
3. **若本地变体合法存在**：定义本地节点（如 `pri.X_hcf_variant`），并在 relations 中补一条 `DERIVED-FROM` / `PART-OF` 指向此处登记的父节点。
4. **跨专题引用**：见 §3 Tier 2 节。当前只有 1 条真正跨专题（Brownian FDT）。

---

## 2. Tier 1 · 单专题内事实共用节点（39）

### 超稳激光（ultrastable-laser）

| ID | 类型 | 使用文件数 | 主页 YAML | 一句话 |
|----|------|----------|-----------|--------|
| `pri.brownian_thermal_noise_fdt` | pri | **28** | `numata2004.yaml` | 布朗热噪声—涨落耗散定理（FDT） |
| `meth.pdh_locking` | meth | 6 | `drever1983.yaml` | Pound–Drever–Hall 激光锁频 |
| `meth.fiber_delay_locking` | meth | 5 | `jiang2010.yaml` | 光纤延迟线锁频 |
| `pri.fiber_delay_line_frequency_ref` | pri | 3 | `jiang2010.yaml` | 光纤延迟线频率参考原理 |
| `pri.crystalline_coating_low_brownian_noise` | pri | 3 | `cole2013.yaml` | 单晶镀层低布朗热噪声 |
| `pri.fiber_thermal_noise_wanser` | pri | 2 | `dong2015.yaml` | 光纤固有热噪声 Wanser 模型 |
| `pri.pdh_heterodyne_detection` | pri | 2 | `drever1983.yaml` | PDH 射频边带光学外差探测 |
| `pri.shb_crystal_thermal_shift` | pri | 2 | `cook2015.yaml` | SHB 晶体热频移 |

### 光学频率梳（optical-frequency-combs）

| ID | 类型 | 使用文件数 | 主页 YAML | 一句话 |
|----|------|----------|-----------|--------|
| `pri.self_referencing_f2f` | pri | 16 | `giunta2019.yaml` | f-2f 自参考原理 |
| `meth.dual_comb_spectroscopy` | meth | 8 | `coddington2016.yaml` | 双梳光谱方法 |
| `pri.molecular_rovibrational_fingerprint` | pri | 7 | `schliesser2012.yaml` | 分子振转指纹光谱 |
| `pri.parametric_four_wave_mixing_comb` | pri | 6 | `kippenberg2011.yaml` | 参量四波混频梳产生 |
| `pri.supercontinuum_octave_spanning` | pri | 5 | `diddams2000.yaml` | 超连续谱倍频程展宽 |
| `pri.dissipative_kerr_soliton` | pri | 5 | `kippenberg2018.yaml` | 耗散 Kerr 孤子双平衡 |
| `pri.microresonator_anomalous_dispersion` | pri | 5 | `kippenberg2011.yaml` | 微谐振腔反常色散条件 |
| `meth.cw_pumped_microcomb_generation` | meth | 5 | `kippenberg2011.yaml` | CW 泵浦微谐振腔梳产生 |
| `pri.dual_comb_multiheterodyne_detection` | pri | 4 | `coddington2016.yaml` | 双梳多外差检测 |
| `pri.lugiato_lefever_equation` | pri | 4 | `kippenberg2018.yaml` | Lugiato–Lefever 方程 |
| `meth.laser_tuning_soliton_access` | meth | 4 | `kippenberg2018.yaml` | 激光扫频孤子激发 |
| `meth.microcomb_self_referencing` | meth | 3 | `kippenberg2018.yaml` | DKS 微梳自参考 |
| `pri.nonlinear_frequency_conversion_comb` | pri | 3 | `schliesser2012.yaml` | 非线性频率转换梳产生 |
| `meth.dfg_comb_generation` | meth | 3 | `schliesser2012.yaml` | 差频产生（DFG）中红外梳 |
| `pri.microcomb_self_injection_locking` | pri | 2 | `delhaye2014.yaml` | 微梳自注入锁定 |
| `pri.rayleigh_backscattering_noise` | pri | 2 | `jiang2010.yaml` | 光纤扫频 Rayleigh 背向散射极限 |
| `pri.ramsey_comb_spectroscopy` | pri | 2 | `picque2019.yaml` | Ramsey-comb 光谱 |
| `meth.direct_two_photon_comb_spectroscopy` | meth | 2 | `picque2019.yaml` | 直接双光子梳光谱 |
| `pri.photodetection_shot_noise_limit` | pri | 2 | `kalubovilage2022.yaml` | 光电探测散粒噪声 |
| `pri.pump_rin_to_fceo_coupling` | pri | 2 | `mcferran2007.yaml` | 泵浦 RIN→fceo 耦合 |
| `pri.photon_starved_open_path_dcs_limit` | pri | 2 | `han2024.yaml` | 开放路径 DCS 散粒噪声极限 |
| `pri.optical_frequency_division_microwave` | pri | 2 | `giunta2019.yaml` | 光学分频微波合成 |
| `pri.vibration_cavity_length_coupling` | pri | 2 | `lezius2016.yaml` | 振动→腔长线性耦合 |
| `pri.eom_acoustic_resonance_limit_t17` | pri | 2 | `torcheboeuf2017.yaml` | EOM 声学谐振带宽极限 |
| `meth.carrier_envelope_amplitude_modulation_spectroscopy` | meth | 2 | `lesko2022.yaml` | 载波包络幅度调制光谱（CAMS） |

> 其余 ≥ 2 文件的 ent/met 节点未列入本清单（本注册表仅跟踪 pri/meth）。

---

## 3. Tier 2 · 跨专题共用节点（真正需要 SHARED-WITH 语义）

当前**仅 1 条**：

| ID | 类型 | 涉及专题 | 文件数 | 主页 |
|----|------|---------|-------|------|
| `pri.brownian_thermal_noise_fdt` | pri | `ultrastable-laser`, `optical-frequency-combs` | 28 | `topics/ultrastable-laser/papers/numata2004.yaml` |

**语义**：超稳激光中该节点刻画 FP 腔镀层的热噪声；光学频率梳中在 `michaudbelleau2022`（HCF 光梳）等 evidence 文件中作为 source of thermal noise 的通用父原理被引用。

**未来扩展候选**（待跨专题摄入更多论文后激活）：
- `meth.pdh_locking`（超稳激光 → 频率标准）
- `pri.photodetection_shot_noise_limit`（光梳 → 超稳激光 → 微波光子学）
- `pri.self_referencing_f2f`（光梳 → 频率标准 UTC 溯源）

---

## 4. 维护指令

- **新论文摄入时**：优先搜索本清单；若本地变体必要，添加 `DERIVED-FROM` / `PART-OF` 关系指向此处节点
- **更新本清单**：每个 Round 结束或 `stats.py` cross-file reuse 指标大幅变化时，重新扫描 `node_files[id] >= 2` 节点
- **不要**手工编辑使各节点"主页 YAML" 字段迁移——主页是按 `load_yaml_files` 顺序首次遇到的文件，迁移会破坏现有 `source.claim` 链路

---

*初版：2026-04-21 · 基于阶段 C 完成时的节点快照。*
