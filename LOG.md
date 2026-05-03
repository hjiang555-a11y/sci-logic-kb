# 知识库演化日志


## [2026-05-03] ingest | Fermann 2000 — 自相似抛物线脉冲（similariton）光纤放大理论 & 实验 (shared, breakthrough)

### 摄入内容
- 文件：topics/shared/papers/fermann2000.yaml
- 贡献类型：breakthrough（首次理论推导并实验证实 NLSE 含增益自相似抛物线脉冲解）
- 核心贡献：发现含增益 NLSE 渐近自相似解——抛物线包络 + 线性啁啾脉冲（similariton）；
  实验在 Yb 光纤放大器中以 FROG 确证；压缩获 68 fs/80 kW 脉冲。开创光纤放大新范式。
- 新增节点：1 实体 + 2 原理（含 1 foundational）+ 1 方法 + 2 指标 + 4 关系

## [2026-05-03] ingest | Belardi 2015 — HC-ARF 空芯反共振光纤设计与可见/近红外特性 (shared)

### 摄入内容
- 文件：topics/shared/papers/belardi2015.yaml
- 贡献类型：evidence
- 核心贡献：系统研究 HC-ARF 四种结构设计与传输特性；首次实验实现第一反共振窗 HC-ARF；报告 175 dB/km@480nm 最低损耗；提出侧切气体传感方案。
- 新增节点：1 实体 + 2 原理 + 1 方法 + 2 指标 + 4 关系

## [2026-05-03] ingest | Chiodo 2013 — Mini-DOLL 星地相干光链路大动态扫频激光系统 (shared)

### 摄入内容
- 文件：topics/shared/papers/chiodo2013.yaml
- 贡献类型：evidence
- 核心贡献：演示光纤延迟线稳频 + DDS 编程扫频方法，在保持 10⁻¹⁴ 级 ADEV 的同时实现 >25 GHz / 1 GHz/s 线性扫频，满足低轨卫星多普勒补偿需求。
- 新增节点：1 实体 + 2 原理 + 1 方法 + 3 指标 + 4 关系
- 跨文件引用：meth.allan_deviation_adev (allan1966)
> **格式约定**：每条日志以 `## [YYYY-MM-DD] type | description` 开头。
> 支持的类型：`ingest`（摄入）、`restructure`（重组）、`lint`（健康检查）、`query`（查询反哺）、`contradiction`（矛盾发现）、`schema`（Schema 升级）、`synthesis`（综合页面）
>
> **使用方法**：`grep "^## \[" LOG.md | grep "contradiction"` 可快速定位矛盾点。

---

## [2026-04-24] restructure | 文档一致性整固：去硬编码论文计数 + 精简一次性文档

### 动机
多份核心文档（`SCHEMA.md`、`topics/*/_meta/architecture.md`、`PROCESSED_PAPERS.md`）保留了历史批次的硬编码论文计数（例如 SCHEMA §1 仍写 "超稳激光 78 篇 / OFC 101 篇"；OFC `_meta/architecture.md` 仍写 "Paper Count: 90"；PROCESSED_PAPERS 仍写 "共 84 篇 / 其余 60 篇"），与实际规模（USL 89 / OFC 114 / FS 18 / TFT 31 / timescales 1 / shared 7，总计 260）全面漂移。同时 `docs/ROOT_FILE_INVENTORY.md` 为 TODO.md P0-2 一次性产物，任务已完成且全库无其他文档引用。本次整治按 TODO.md §4 "减少手填统计" 与 §1.2 "文件系统复杂度" 原则收口。

### 具体变更
- **SCHEMA.md**：§一定位 / §二系统架构 / §建设优先级 / §演进原则 的硬编码论文数全部去掉，改为链到 [`TOPICS.md`](TOPICS.md) / `python scripts/stats.py` / [`INDEX.md`](INDEX.md)；删除 §专题体系末尾孤立的表片段（L459–463，header 已缺失）。
- **topics/ultrastable-laser/_meta/architecture.md**：`Paper Count: 78` → 改为 "精确数字见 INDEX.md"。
- **topics/optical-frequency-combs/_meta/architecture.md**：`Paper Count: 90` + 2026-04-21/22 Batch 1/2/3 明细段 → 精简为 "数字见 INDEX.md / 摄入历史见 LOG.md"。
- **topics/frequency-standards/_meta/architecture.md**：`Status: skeleton, 仅 1 篇` → `growing, ≥10 篇（见 INDEX.md）`。
- **topics/time-frequency-transfer/_meta/architecture.md**：去掉 `31 篇论文` 硬编码，保留五大分支叙述。
- **PROCESSED_PAPERS.md**：`共 84 篇` / `其余 60 篇` → 改为 "见目录 / INDEX.md"。
- **docs/ROOT_FILE_INVENTORY.md**：删除（TODO.md P0-2 已完成、无反向引用）。
- 重跑 `python scripts/build_index.py`，自动索引刷新。

### 不变量
- 未改动任何 YAML 数据节点
- `python scripts/lint.py --summary`：102 error / 12 warning / 215 info（较 TODO.md 2026-04-24 基线 113/12/216 小幅下降，无新增错误类）
- `python scripts/stats.py`：260 papers / 1211 nodes / 1364 relations 不变

### 备注
后续新增论文时，不要再在 architecture.md / SCHEMA.md 里写绝对数字，统一走 `scripts/stats.py` + 自动 INDEX。



### 范围
PDF 批量投放于 `/pdfs/` 目录，共 46 个文件；其中 30 个为 time-frequency-transfer 专题
stub（已在仓库中但 YAML `authors:` flow-list 缺逗号导致整文件不可解析）。其余 16 个为
命名 PDF（`adler2009.pdf` 等），4 个之前已处理（`howe1976`、`riley2008`、`sullivan1990`、
`diddams2020`），12 个待处理。

### 本批处理

**一、time-frequency-transfer 专题（30 篇 stub → 完整 evidence，单次 PR）**
- 修复 30 个 stub 的 YAML 语法 bug（`authors:` flow-list 缺逗号）
- 从 stub 升级为完整 evidence 档 YAML（含 entities / principles / relations / metrics）
- 新建 4 个 Level 1 总节点骨架：
  - `ent.coherent_optical_fiber_link`（Calonico 2015 建立）
  - `ent.rf_over_fiber_time_transfer_link`（Krehlik 2015 建立）
  - `ent.free_space_optical_tf_link`（Sinclair 2019 建立）
  - `ent.satellite_microwave_time_transfer_link`（Exertier 2016 建立）
- 新增 13+ domain/engineering tier 原理节点（`pri.noise_cancellation_frequency_transfer`、
  `pri.fiber_propagation_reciprocity`、`pri.atmospheric_optical_phase_noise_power_law`、
  `pri.o_twtft_motion_reciprocity_breakdown`、`pri.quantum_limited_photon_counted_ott`、
  `pri.passive_reciprocal_fiber_noise_cancellation`、
  `pri.dual_polarization_coherent_endless_phase_tracking`、
  `pri.dcf_induced_differential_delay_temp_compensation` 等）

**二、frequency-standards 专题（9 篇光钟 evidence + 1 篇综述 framework）**
- evidence：`heavner2005` (NIST-F1)、`oskay2006` (Hg⁺ ion)、`rosenband2008` (Al⁺ quantum logic)、
  `nicholson2015` (JILA Sr 2.1×10⁻¹⁸)、`oelker2019` (dual Sr 4.8×10⁻¹⁷)、
  `bothwell2019` (JILA SrI 2.0×10⁻¹⁸)、`bothwell2022` (mm-scale redshift)、`bacon2021` (BACON 三钟)
- framework：`ludlow2015` (Progress on OLC, C.R. Physique)
- 新建 Level 1 `ent.microwave_frequency_standard` + `pri.si_second_cesium_definition`
- 新增 `pri.quantum_logic_clock_readout`、`pri.gravitational_redshift_within_atomic_sample`、
  `pri.blackbody_radiation_stark_shift`

**三、shared 专题（2 篇 framework）**
- `allan2016`（Allan & Levine 2016，IEEE TUFFC，Allan 方差族 50 年综述）
- `sullivan2001`（Sullivan 2001，NIST JRES，NIST 初级频标综述）

**四、optical-frequency-combs 专题（1 篇占位）**
- `adler2009` — PDF 在仓库中不可解析（文件头正常但 trailer 损坏），暂以低可靠度占位
  条目收录，仅保留 meta；待专家提供正确 DOI 后重写。`reliability: low`。

### 矛盾与降档
无新矛盾；所有系统声明复用已有 metric 节点。4 篇（Caldwell 2023、Bothwell 2022、
Bacon 2021、Guéna 2017）在 note 中标注"可考虑专家审核升 breakthrough"，默认 evidence。

### 统计
- 本批新增 42 完整 + 1 占位 = 43 条记录
- TF transfer：1 → 31 篇；Frequency standards：3 → 12 篇；Shared：5 → 7 篇；OFC：104 → 105 篇
- 本库总计：192 → 234 篇
- lint 结果：0 error / 3 warning / 200 info

### 可靠性声明
- 28/42 提取自可读 PDF 的 abstract + intro，`reliability: high/medium`
- 6/42（bothwell2019、bothwell2022、oelker2019、bacon2021、sullivan2001、adler2009）的 PDF
  损坏/部分损坏，基于公开文献元数据推定，`reliability: medium/low`，note 明确标注
- 需专家重点核对：4 篇 breakthrough 候选档位；adler2009 真实身份；5 篇 PDF 损坏论文具体参数

---

## [2026-04-23] ingest | B1 OFC 早期综述 + B5c Ludlow PhD thesis（5 篇 framework）

按 TODO.md 阶段 3 批次 **B1（OFC 早期综述与原理奠基）** 与 **B5c（Ludlow PhD thesis）**
合并一次 PR 完成。

- **摄入文件**（5 篇，均 framework 档）：
  - `topics/optical-frequency-combs/papers/cundiff2003.yaml` — Cundiff & Ye 2003 *Rev. Mod. Phys.* 75:325（`CUNDIFF2003-RMP`）
  - `topics/optical-frequency-combs/papers/fortier2019.yaml` — Fortier & Baumann 2019 *Commun. Phys.* 2:153（`FORTIER2019-COMMPHYS`）
  - `topics/optical-frequency-combs/papers/diddams2020b.yaml` — Diddams/Vahala/Udem 2020 *Science* 369:eaay3676（`DIDDAMS2020-SCIENCE`）
  - `topics/frequency-standards/papers/diddams2016.yaml` — Diddams/Fortier/Ludlow 2016 *Nature Photonics* 10:502（`DIDDAMS2016-NATPHOT`）
  - `topics/frequency-standards/papers/ludlow2008_thesis.yaml` — Ludlow PhD thesis 2008, JILA（`LUDLOW2008-THESIS-JILA`）
- **新建框架原理节点**（8 个）：
  - OFC 专题（6 个）：`pri.cep_controlled_frequency_comb_time_frequency_duality`、`pri.octave_span_enables_absolute_referencing_cy03`、`pri.ofc_nine_application_threads_f19`、`pri.comb_platform_tradeoffs_f19`、`pri.ofc_unified_electromagnetic_spectrum_framework`、`pri.three_comb_platforms_triumvirate_dvu20`
  - 频率标准专题（4 个）：`pri.optical_clock_ten_minus_eighteen_geoid_bridge`、`pri.qpn_dick_two_fundamental_limits_dfl16`、`pri.magic_wavelength_operational_protocol_l08`、`pri.sr_clock_systematic_budget_framework_l08`
- **新建框架方法节点**（2 个）：`meth.comb_platform_taxonomy_f19`、`meth.sr_optical_lattice_clock_stack_l08`（后者为 B5a 批次 Sr 系列论文的共同参考底座）
- **新建指标节点**（1 个）：`met.optical_clock_fractional_uncertainty_2016_benchmark`（2016 年代光钟基准）
- **跨文件节点复用率**：5 篇新文件共 13 条关系，其中 **4 条复用已有跨专题节点**（`ent.optical_frequency_comb`@giunta2019 · `pri.self_referencing_f2f`@giunta2019 · `ent.optical_frequency_standard`@fortier2026 · `ent.optical_lattice_clock`@fortier2026 · `meth.allan_deviation_adev`@allan1966），未新建重复节点。
- **validation**：`python scripts/lint.py` 通过（**0 error**，本批 0 new warning；3 warning 为预先存在的 ultrastable-laser 问题）；`python scripts/build_index.py` 刷新：**192 papers / 1029 nodes / 1180 relations / 6 topics**（较 B9 后 187 papers / 1016 nodes 增 +5 papers / +13 nodes / +16 relations）
- **批次进度**：Stage 3 已完成 B9 + B1 + B5c = 10/32 篇（31%）
- **PR 元信息备注**：原 batches README 将 `diddams2016` 归 B1（OFC 批次），但其内容是光钟综述（NIST+JILA 光钟领军人物联合署名）；摄入时按内容主题归入 `frequency-standards` 专题，但仍计作 B1 批次完成项（保持批次计数一致）。

---

## [2026-04-23] ingest | B9 Allan–Howe 奠基白名单（shared 专题首批 framework 摄入，5 篇）

按 TODO.md 阶段 3 批次 **B9** 完成时频计量数学基础专题（`topics/shared/`）首批入库。

- **摄入文件**（5 篇，均 framework 档）：
  - `allan1966.yaml` — Allan 1966 *Proc. IEEE* 54(2):221 — σ_y(τ) 两样本 Allan 方差原始定义（zotero_key `ALLAN1966-PROCIEEE`）
  - `allan1987.yaml` — Allan 1987 *IEEE TUFFC* IM-36(2):646 — 经典方差 vs Allan 方差辨析；幂律噪声五类分类（`ALLAN1987-TUFFC`）
  - `howe1976.yaml` — Howe 1976 *NBS Tech Note 679* — 频域稳定度测量教程；相位/频率噪声 PSD 对偶（`HOWE1976-NBS-TN679`）
  - `sullivan1990.yaml` — Sullivan/Allan/Howe/Walls 1990 *NIST Tech Note 1337* — MDEV/TDEV/HDEV 扩展方差手册（`SULLIVAN1990-NIST-TN1337`）
  - `riley2008.yaml` — Riley & Howe 2008 *NIST Special Publication 1065* — OADEV/TOTDEV/Theo1/TheoH 方差手册（`RILEY2008-NIST-SP1065`）
- **新建权威方法节点**（8 个，供全库复用，减少后续 papers YAML 重复定义）：
  - `meth.allan_deviation_adev` — ADEV / σ_y(τ)
  - `meth.modified_allan_deviation_mdev` — MDEV / mod σ_y(τ)
  - `meth.time_deviation_tdev` — TDEV / σ_x(τ)
  - `meth.hadamard_deviation_hdev` — HDEV（漂移免疫）
  - `meth.overlapping_allan_deviation_oadev` — OADEV（EDF 提升）
  - `meth.total_deviation_totdev` — TOTDEV（长 τ 低偏差）
  - `meth.theo1_thedev` — Theo1 / TheoBR / TheoH（长 τ 统计效率最优）
  - `meth.phase_noise_psd_measurement` — 相位噪声 S_phi(f) 测量
- **新建权威原理节点**（7 个）：经典方差发散 / 两样本方差收敛 / 幂律噪声五类分类 / σ_y 斜率辨识噪声 /
  相位-频率噪声 PSD 对偶 / 时-频域 sin⁴ 传递函数 / MDEV sin⁶ 核 PM 分辨 / HDEV 二阶差分漂移免疫 /
  重叠估计量 EDF 提升 / Theo1 长 τ 统计效率最优
- **新建权威指标节点**：`met.fractional_frequency_instability_sigma_y`（role=primary，σ_y(τ) landmark 定义）
- **专题骨架建立**：`topics/shared/papers/` 目录首次启用（原 `shared/_meta/architecture.md` 中状态 "Not yet populated" 现更新为"已启用"）；`topics/shared/INDEX.md` 经 `scripts/build_index.py` 自动生成
- **validation**：`python scripts/lint.py` 通过（本批零 error、零 warning）；`python scripts/build_index.py` 全量刷新 INDEX / INDEX_metrics / INDEX_principles / CURRENT_NODES_REFERENCE
- **后续动作**：后续摄入的 papers 应优先引用这 8 个 `meth.*` 节点而非重复定义本地 Allan/MDEV/OADEV 方法；各 `met.*allan_deviation_*` 实例节点可通过 OPERATIONALIZED-AS 关系绑定到 `met.fractional_frequency_instability_sigma_y`

---

## [2026-04-23] restructure | JILA/NIST 扩库阶段 2 候选池批准（32 篇）

专家一次性批准阶段 2 全部候选进入阶段 3 摄入。

- **批准总量**：32 篇 = 原 31 篇 stage2 候选池 + 新增 `ludlow2008_thesis`（Andrew D. Ludlow PhD thesis, JILA 2008，符合 TODO.md §0.2 "PhD thesis ✅ 接受"规则）
- **白名单豁免**：5 篇 Allan–Howe 奠基文献（`allan1966` / `allan1987` / `howe1976` / `sullivan1990` / `riley2008`）一并批准
- **批次分配**：详见 `reports/ingest_plan/batches/README.md`（B1/B2/B5a-c/B7/B8/B9 共 7 个子批次）
- **推荐摄入顺序**：B9（奠基）→ B1（OFC 综述）→ B5c（Ludlow thesis）→ B5a/B5b（实验主体）→ B2/B7/B8
- **阻塞点**：PDF 全文 21 篇（`breakthrough` + `evidence`）受沙箱网络限制，需 allowlist 或本地 Zotero 投递

---

## [2026-04-23] ingest | time-frequency-transfer 专题种子 · `cacciapuoti2017.yaml`（ESA I-SOC 科学需求，framework）

处理 `/pdfs/SCI-ESA-HRE-ESR-ISOC_Iss.1.1_Approved.pdf`（另一 PDF `FreqStable_Si_cavity AlGaAs mirror_PRL2026.pdf`
已在 2026-04-16 以 `lee2026.yaml` 摄入，本次跳过去重）。

- **专题归属**：`time-frequency-transfer`（此前 0 篇，本文为种子 framework 文档）。
- **档位**：`framework`（ESA 任务科学需求文档，2017-06-09 Issue 1.1 Approved）。
- **顶层实体**：`ent.space_optical_clock_mission`（Level 1）——I-SOC 任务通用父节点。
- **Level 2 子系统节点**：`ent.space_lattice_optical_clock_sloc`（SLOC，Sr 光钟）、
  `ent.space_frequency_comb_sfc`（SFC）、`ent.microwave_link_mwl`（MWL）、
  `ent.pulsed_optical_link_elt_plus`（ELT+）、`ent.frequency_comb_optical_link_fcol`（FCOL，可选）。
- **原理**：`pri.gravitational_time_dilation`、`pri.einstein_equivalence_principle`（foundational）；
  `pri.common_view_clock_comparison`、`pri.non_common_view_clock_comparison`（domain）。
- **方法**：`meth.mwl_two_way_tf_transfer`、`meth.elt_plus_pulsed_optical_tf_transfer`。
- **指标**：`met.space_to_ground_link_instability`、`met.space_to_ground_link_inaccuracy`、
  `met.earth_grs_test_uncertainty`、`met.fundamental_constant_drift_search`。
- **关系**（21 条）：任务内部 PART-OF 骨架 + ENABLED-BY（GTD / EEP）+ OPERATIONALIZED-AS（共视/非共视）+
  链路 CHARACTERIZED-BY 指标 + 非共视比对 BOUNDED-BY SLOC（桥接稳定度系统极限）+
  **3 条跨专题 CONDITIONED-BY**：SLOC ↔ `ent.optical_lattice_clock`（frequency-standards）、
  SFC ↔ `ent.optical_frequency_comb`（optical-frequency-combs）、SLOC 询问激光 ↔
  `ent.fp_cavity_system` / `met.fractional_freq_instability_m17`（ultrastable-laser，Dick 效应接口）。
- **任务性能目标（入库）**：SLOC σ_y = 8×10⁻¹⁶/√τ，系统不确定度 1×10⁻¹⁷；MWL flicker floor 5×10⁻¹⁹、
  不准确度 5×10⁻¹⁹；ELT+ TDEV ≤0.5 ps @100 s、≤1 ps 至 10⁶ s，分数不准确度 1×10⁻¹⁸。
  科学目标：地球 GRS 2×10⁻⁷（vs ACES 10×）、太阳 GRS 1×10⁻⁶、月球 GRS 2×10⁻⁴、精细结构常数漂移搜索 10 000×。
- **lint / stats**：0 error（沿用基线），chain-gap 从 35 → 36（tier=framework 允许；C17_18 非共视比对受空间钟稳定度限制的缺口为有意保留，留给后续空间光钟专项论文补 breakthrough_paths）。
- **INDEX / CURRENT_NODES_REFERENCE**：已重建（182 papers / 997 nodes / 1149 relations）。

---

## [2026-04-23] ingest | optical-frequency-combs Batch 4 · `/pdfs` 增量（11 篇：3 breakthrough + 8 evidence）

承接 Batch 2+3 后，对 `/pdfs/` 中新增的 13 个 PDF 进行处理。去重后 **11 篇新入库**（光频梳 90 → 101）：

- **跳过（zotero 备份键，同 DOI 已在库）**：
  - `8NE7UAUR`（Leopardi 2017 Optica，DOI `10.1364/OPTICA.4.000879`）→ 已有 `leopardi2017.yaml`（zotero `8XUFRL4K`）
  - `LB6RJ2MZ`（Picqué & Hänsch 2019 Nat Photon，DOI `10.1038/s41566-018-0347-5`）→ 已有 `picque2019.yaml`（zotero `RZME5CH8`；另一备份键 `BL4HI3QI` 已在 Batch 3 记录）

- **Breakthrough 档（3 篇 · 里程碑 / 范式转移）**：
  - `holzwarth2000.yaml`（ZNCBFZR5，PRL 2000）：首台 PCF 八度自参考飞秒梳作为光频合成器，5.1×10⁻¹⁶ 不确定度——**现代 OFC 诞生标志**（landmark consensus）。
  - `koke2019.yaml`（ZG45BBYV，NJP 2019）：Brillouin 光纤放大 + 中继激光站 1400 km 相干光频传递，(-1.1±0.4)×10⁻²⁰——**首次 Continental-scale 光纤链路**。
  - `caldwell2022.yaml`（YD2MQC49，Nature 2022）：时间可编程梳（TPFC）+ 量子极限测距，5000× 功率降低达成 1/77 光子/脉冲测距——**"固定梳 → 可编程梳"范式转移**。
  - 3 篇均 `primary_metric_exempt_reason: new_principle/new_method/landmark_consensus`（σ_y 主线不适用）。

- **Evidence 档（8 篇）**：
  - `millo2009b.yaml`（WHNQC4FV，APL 2009）：光纤梳光生微波驱动 Cs 喷泉钟（3×10⁻¹⁵ @ 1-10 s），与 Ti:sapph 梳等效——与 USL 专题 `millo2009.yaml`（PRA 2009 振动不敏感腔）是**同一作者不同论文**，以 `b` 后缀区分。
  - `inaba2013.yaml`（Y7KZ89LA，Opt Express 2013）：窄线宽梳将 1064 nm USL 线宽传递至 578 nm 从激光，观测 ¹⁷¹Yb 钟跃迁 20 Hz 线宽（AIST/NMIJ）。
  - `carlson2017.yaml`（WCBMETLH，Opt Lett 2017）：SiN 波导低功率 f-2f 自参考（11.3 mW 入射，10× 低于 HNLF），兼容 f-3f 自参考。
  - `cossel2017.yaml`（XHCB4X6R，Optica 2017）：开放路径双梳光谱至飞行器反射镜（CO₂/CH₄/H₂O 大气剖面）。
  - `manurkar2018.yaml`（XZTNQ8D4，OSA Continuum 2018）：全自参考梳仅 5 W 电功耗（光纤电阻调制器 + SiN 波导，CubeSat 级预算）。
  - `shaw2019.yaml`（ZN7TS37H，OSA Continuum 2019）：Red Pitaya FPGA 开源数字伺服锁定梳（~0.1 rad 相位噪声，>30 h 无循环滑动，低成本普及化）。
  - `luo2020.yaml`（X6KNIXMW，Opt Express 2020）：130 W 180 fs Yb:fiber 三级 CPA + grism 压缩（ECNU）。
  - `rao2022.yaml`（ZSWYS26E，物理学报 2022）：8 支路 Er 光纤梳用于 CRDS 多波长并行光谱（国家授时中心）。

- **节点新增**：5 个新 principles（`pri.sin_waveguide_low_power_f2f_c17`、`pri.fiber_resistive_modulator_frep_tuning_m18`、`pri.tpfc_digital_coherent_pulse_control_c22` meta-tier、`pri.tpfc_tracking_oscillator_quantum_limit_c22`、`pri.brillouin_amplification_long_distance_k19`）。其余均复用已有 `pri.*` / `meth.*` / `ent.*`。

- **健康指标（刷新）**：`python scripts/lint.py --summary` → **0 error / 3 warning / 192 info**（baseline 为 3 warning / 188 info，Δ = +4 info，3 warning 不变均属 pre-existing `missing-conditions`）。`python scripts/stats.py`：Reasoning Chain Closure 76.0%，breakthrough-only **100%**，Evidence Coverage **100%**，σ_y Linkage (USL) **100%**，Limit Resolution Rate **100%**。

- **运维文件同步**：
  - `PROCESSED_PAPERS.md` 添加 11 行新条目 + Batch 4 备注
  - `TOPICS.md` 光频梳计数 90 → 101
  - `TODO.md` 阶段 D 快照与第一梯队段落同步更新
  - `INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` / `docs/CURRENT_NODES_REFERENCE.md` / 各专题 `INDEX.md` 由 `scripts/build_index.py` 自动重建（总计 **181 篇 · 981 节点 · 1128 关系**）

---

## [2026-04-22] restructure | 现状评估 + TODO/说明文档状态对齐

- 基于 `lint.py --summary` / `stats.py` / `freshness.py --check` 刷新当前基线：170 篇论文、0 error / 3 warning / 188 info、Reasoning Chain Closure 76.6%、Synthesis Coverage 1/4、Cross-file Reuse 8.7%、超稳激光 8 个 synthesis 页面 stale。
- `TODO.md` 从"阶段 A–D0 完成播报"切换为"阶段 D（专家审阅 + 覆盖扩展）准备中"，新增现状快照与后续建议，明确下一轮重点是 **OFC synthesis 启动 + USL freshness 收口**。
- `README.md` / `TOPICS.md` / `SCHEMA.md` / `CONTRIBUTING.md` 对齐当前论文数、专题状态与操作口径：
  - OFC 论文数改为 90；频率标准 / 时间标尺改为 1 篇 framework；目录路径纠正为 `frequency-standards/`、`timescales/`
  - README 移除失效的 `validate.py` / 每日同步表述，改为当前 lint/stats/freshness workflow
  - CONTRIBUTING 本地验证改为全库 lint（避免 `--topic` 下跨专题 dangling-ref 假阳性），文件头版本改为 v4.5
- `.github/PULL_REQUEST_TEMPLATE.md` / `.github/copilot-instructions.md` 同步到 v4.5 文档口径。

---

## [2026-04-22] schema | Schema v4.4 → v4.5 · SHARED-WITH 谓词 + BOUNDED-BY limit_status 枚举 + entity.instance_of 字段 + CI freshness + Cytoscape 可视化

**一次性发布 v4.5，关闭所有历史 Schema/工具 TODO（TODO-1/2/3/5 完成；TODO-4 落地为 `instance_of` 字段，`INSTANCE-OF` 谓词升格进入一年观察窗口）**。

- **Schema 层**：
  - 第 9 种谓词 `SHARED-WITH`（§5）：跨专题 Tier 2 公共机制锚定，双 lint 规则（Tier 2 注册白名单 + 跨专题要求 + pri/meth-only）
  - `BOUNDED-BY` 新增 `limit_status` 四态枚举（`active | conditional | resolved | refuted`）+ `resolved_by` + `resolution_source`（§4.2），保留 `is_system_limit` 兼容
  - 实体节点新增可选 `instance_of` 字段（§1），配套 lint 一致性检查（必须有匹配的 `PART-OF`）
  - 版本号 v4.4 → v4.5，向后兼容（所有新字段可选）
- **工具层**：
  - `scripts/freshness.py`：mtime 改基于 `git log -1 --format=%ct`（CI 中 checkout 后仍可工作）；新增 `--json` 输出
  - `scripts/lint.py`：新增 `check_shared_with` / `check_limit_status` / `check_instance_of` 三项
  - `scripts/stats.py`：新增 `limit_resolution_rate` 指标（打印为 "1b" 行）
  - `scripts/migrate_bounded_status.py`：BOUNDED-BY `limit_status` 批量推断建议（read-only）
  - `scripts/graph.py --format cytoscape`：Cytoscape.js 原生 JSON 输出
  - `scripts/build_graph_view.sh`：一键重建 `docs/graph/graph.json`
- **CI / 可视化**：
  - `.github/workflows/synthesis-freshness.yml`：PR 自动打 `needs-refresh` 标签 + sticky 评论（不阻塞合并）
  - `docs/graph/index.html` + `viewer.js`：只读交互式 Cytoscape.js 图浏览器（按 type / topic / tier 上色、ID 搜索、谓词过滤）
- **数据层示范落地**：
  - `limit_status: resolved` 首批 3 条：`cole2013.C05`（AlGaAs 晶体镀层）· `hafner2015.H05`（48 cm 长腔 + AlGaAs）· `chen2025.Che02`（sub-5K Si 腔）
  - `instance_of` 首批 3 条：`chen2025.si_crystal_fp_cavity_sub5k_c25` · `chen2020.cubic_dual_cavity_c20` · `hafner2015.self_balancing_long_cavity_h15` → `ent.fp_cavity_system`
  - `SHARED-WITH` 首批：**infrastructure ready**，首个实际关系待下一篇在 OFC/频率标准定义热噪声变体原理的论文触发
- **lint/stats 状态（v4.5 基线）**：0 error · 3 warning · 188 info。Reasoning Chain Closure 76.6%（breakthrough-only 100%），σ_y Linkage 100%，Limit Resolution Rate 100%（resolved 3 / active 0 · unset 138，首批示范）。
- **文档**：
  - `SCHEMA.md` 顶部变更摘要更新 + §1/§4.2/§5 具体规范
  - `docs/USAGE.md` 新增 "Synthesis 页新鲜度机制（v4.5+）" 小节
  - `topics/shared/registry.md §3` 补 Tier 2 完整元数据 + lint 契约说明
  - `README.md` 增加交互式图谱入口
  - `TODO.md` 四项全部勾选，附完成日期与交付指针

---

## [2026-04-22] ingest | optical-frequency-combs Batch 2+3 · 计量链路 + 新平台与光谱应用（19 篇）

承接 Batch 1（10 篇 · A1 技术平台子域）后摄入 Batch 2 + Batch 3，合计 +19 篇（光频梳 71 → 90）。原计划 20 篇，其中 `BL4HI3QI` 与已处理 `picque2019.yaml`（zotero `RZME5CH8`）DOI 完全相同（`10.1038/s41566-018-0347-5`，Picqué & Hänsch 2019 Nature Photonics 综述），确认为 zotero 备份键，**跳过不创建重复 YAML**。

- **Batch 2 计量链路 / 频率综合子域**（B-FreqSyn 为主，10 篇全部新增）：
  - `marra2012.yaml`（P7A5Z647，**breakthrough**）：首次光频梳结构光纤传递 3×10⁻¹⁸ 精度（NPL，> 数 km）。
  - `nardelli2023.yaml`（R9HNIBTE，evidence）：Er/Yb:glass 梳 10⁻¹⁸ 级光学/微波计量（NIST）。
  - `rolland2018.yaml`（U5C8AJYM，**breakthrough**）：首次双分支 Er 梳 <10⁻¹⁸ 传递稳定度（IMRA，被动差分抵消）。
  - `hisai2021.yaml`（SZL4V3W8，evidence）：NMIJ 8 分支 Er:fiber 梳服务 Sr/Yb 光钟（架构里程碑）。
  - `ning2020.yaml`（ST825B59，evidence）：全 PM 多分支 Er:fiber 梳 for CRDS（国家授时中心）。
  - `sinclair2015.yaml`（LMFFEUFX，**framework**）：紧凑全 PM 相干光纤梳技术综合（NIST Rev Sci Instrum invited）。
  - `zhang_s2024.yaml`（QEJS62JG，evidence）：门控+平衡探测提升梳-CW 拍频 SNR ≥20 dB（USTC）。
  - `chen_z2024.yaml`（QIFVVUIH，evidence）：双梳微波钟同步 fs 级（PKU+BUPT Optica）。
  - `zhang2017b.yaml`（V7MNFM68，evidence）：偏振态旋转控制梳频率（国家授时中心 Opt Lett）。
  - `lee2015.yaml`（L6ZZII7R，**breakthrough**）：单片 SESAM+graphene EOM 锁模与稳频集成（Schibli 组）。
- **Batch 3 新平台与光谱应用**（A2-DKS / A3-Astro / B-Spec / B-DCS / B-MIR 多主线，9 篇全部新增）：
  - `diddams2010.yaml`（VKLU3BG6，**framework**）：JOSA B "The evolving optical frequency comb" 综述。
  - `porat2018.yaml`（L88UAAEQ，**breakthrough**）：首次相位匹配 XUV 光梳（77 MHz 高温气体，JILA，Nature Photonics）；刷新 B-Spec 主线。
  - `cheng2024.yaml`（NDSVHPF5，**breakthrough**）：首次连续 UV–蓝绿（390–520 nm）天文光梳；刷新 A3-Astro + B-Spec 主线。
  - `holzwarth2001.yaml`（UNL7SSP3，**breakthrough**）：首个二极管泵浦倍频程梳（Cr:LiSAF + PCF，Opt Lett 2001）；开创便携式 OFC 路线。
  - `ideguchi2016.yaml`（PBGQXUED，**breakthrough**）：首个单腔 KLM 双向双梳环形激光器（B-DCS 主线里程碑）。
  - `spaun2016.yaml`（NNLDMCDD，**breakthrough**）：首次腔增强梳 + 缓冲气体冷分子红外光谱（Nature 2016）。
  - `timmers2018.yaml`（TFUBQQB8，**breakthrough**）：脉冲内 DFG + OP-GaP 超八度中红外指纹梳（4–12 μm）；刷新 B-MIR 主线。
  - `diddams2007.yaml`（U9WDX7JI，**breakthrough**）：首次 VIPA 空间分辨梳齿分子指纹光谱（Nature 2007）。
  - `papp2013b.yaml`（SE4C2RWR，**breakthrough**）：CO₂ 激光微棒梳 + 机械 f_rep 控制（PRX 2013，5×10⁻¹⁵ @ 1 s，较此前 +200×）。注：`papp2013.yaml` 已存在（Papp 2013 parametric-seeding，zotero BG93PZPK），本文件使用 `b` 后缀区分。
- **节点复用**：广泛跨文件引用 `ent.optical_frequency_comb`（giunta2019）、`ent.er_fiber_frequency_comb`（droste2016）、`ent.dual_comb_spectrometer`（coddington2016）、`ent.microresonator_frequency_comb`（kippenberg2011）、`ent.mid_ir_frequency_comb`（schliesser2012）、`pri.self_referencing_f2f` / `pri.comb_equation` / `pri.cavity_enhanced_hhg_comb`（zhang2022）/ `pri.parametric_four_wave_mixing_comb`（kippenberg2011）/ `pri.dissipative_kerr_soliton` 等核心节点。无节点重复定义。
- **Schema 一致性修复**：Batch 3 初稿使用了非标准字段名（`type:` / `source_entity:` / `target_entity:`），已批量归一化为 Schema 规范字段（`predicate:` / `subject:` / `object:`），避免 orphan-node 误判。
- **lint 结果**：0 error · 3 warning（全部 pre-existing，来自 ultrastable-laser 的 `missing-conditions`）· 129 info，与 Batch 1 前一致。新增 breakthrough 论文全部携带 `breakthrough_paths`，无 chain-gap WARNING。
- **索引重建**：`python scripts/build_index.py` — 170 papers · 953 nodes · 1093 relations（光频梳 90 papers · 600 nodes · 735 relations）；`_meta/architecture.md` 论文计数 71 → 90。

---



## [2026-04-21] ingest | optical-frequency-combs Batch 1 · 飞秒锁模激光器技术平台主线（10 篇）

用户指示光频梳 30 篇分 3 批摄入；Batch 1 聚焦 A1 技术平台（重频、相噪、工程化子域）。同步升级 `_meta/scoping_principles.md` v1 → v2，将子域主线指标从"🟡 待专家确认"升级为 v2 正式 9 条主线（A1-Rep / A1-Noise / A1-Robust / A2-DKS / A3-Astro / B-Spec / B-FreqSyn / B-DCS / B-MIR），明确"光频梳不存在单一主线指标，各子域独立判档"。

- **Batch 1 论文**（10 篇，全部新增）：
  - `washburn2004.yaml`（TP9NSD4F，**breakthrough**）：首台 Er:fiber 近红外全锁梳；定义 `ent.er_fiber_comb_washburn04`、`pri.dispersion_flattened_hnlf_octave_broadening`、`meth.dual_pll_frep_fceo_rf_reference`。
  - `newbury2005.yaml`（NHJ84W8G，**framework**）：光纤梳扰动响应理论；定义 `pri.fiber_comb_perturbative_response_theory`、`pri.fiber_comb_mimo_feedback_topology`。
  - `bartels2009.yaml`（RDBWYLKJ，**breakthrough**）：首台 10 GHz 自参考 Ti:sapph 梳；定义 `ent.ti_sapph_10ghz_comb_bartels09`、`pri.high_frep_bandwidth_power_tradeoff`（跨文件共用的 A1-Rep 核心原理）。
  - `meyer2013.yaml`（T6AF6HJF，**evidence**）：Yb:KYW 光学稳频梳 + 10 GHz 微波生成；1 Hz @ -99 dBc/Hz，Allan <2.6e-15 @ 1 s。
  - `wang2014.yaml`（VATLBIAD，**evidence**）：500 MHz Yb:ring 光纤梳振荡器直出（无放大）；in-loop 4.46e-13/√τ。
  - `zhang2015.yaml`（R4M8SE4F，**evidence**）：Er:fiber 腔内 EOM + PZT 双执行器；定义 `pri.intracavity_eom_frep_wideband_feedback`、`meth.eom_pzt_dual_actuator_frep_lock_z15`。
  - `kuse2016.yaml`（QXC7FSMC，**breakthrough**）：全 PM Er NALM 梳，40 as 积分时延抖动（子域当时纪录）；与 `kuse2015`（3RT4U4TV）通过 `COMPETES-WITH` 关系相连（不同低噪声路径）。
  - `li2017b.yaml`（RWPYUXTB，**breakthrough**）：首次全 PM Yb NALM 梳 f-2f 自参考；in-loop 10⁻¹⁹ @ 1 s（注：in-loop 严格度低于 out-of-loop）。
  - `ma2018.yaml`（P4TCLWW2，**breakthrough**）：首次 750 MHz Yb:fiber 梳紧锁（<1 rad @ 0.1 Hz–10 MHz）；定义 `pri.high_frep_yb_tight_lock_challenges`。
  - `cai2020.yaml`（LBSZCU7P，**evidence**）：紧凑全 PM Er 梳 + 单光纤执行器 + GRIN 微型 f-2f；330 μHz Allan @ 1 s vs H-maser。
- **scoping_principles.md v1 → v2**：9 条子域主线正式定义；明确光谱展宽类档位判据为"转移 PSD + 转换效率"，高重频类为"基频 f_rep + self-ref"。
- **节点复用**：大量跨文件引用 `ent.optical_frequency_comb`（giunta2019）、`ent.er_fiber_frequency_comb`（droste2016）、`pri.self_referencing_f2f`（giunta2019）、`pri.comb_equation`、`pri.supercontinuum_octave_spanning`、`pri.gain_lifetime_servo_bandwidth_limit`（kuse2015）、`pri.figure9_nalm_pm_self_starting`。无节点重复定义。
- **lint 结果**：0 error（与 Batch 1 前持平），3 warning（pre-existing），新增 reasoning-chain-gap 2 条（均 tier=framework/evidence 允许）。
- **Batch 2/3 待续**：计量链路子域（10 篇）+ 新平台与光谱应用（10 篇）在后续会话追加。

---

## [2026-04-21] restructure | 阶段 D-0 延伸：P2 Tier 3 批准落地 + P3 尾巴收口

基于专家批示"同意之前 AI 归类判断，类似表述合并"，执行 `reports/shared_node_candidates.md` §4 的 10 条重点候选。

- **P2.1 · 6 条保留+补关系**（5 ❌ + 1 COMPETES-WITH）：
  - `michaudbelleau2022`：新增 `rel.MB22_04` — `pri.hollow_core_fiber_thermal_noise DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `hafner2015`：新增 `rel.H09` — `pri.long_cavity_thermal_noise_reduction DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `li2019`：新增 `rel.LIG02` — `pri.fiber_thermal_phase_noise_giant_ifog DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `steinlechner2018`：新增 `rel.ST04` — `pri.coating_thermal_noise_material_comparison DERIVED-FROM pri.brownian_thermal_noise_fdt`
  - `jiang2011`：新增 `rel.JI03`（IMPLEMENTS meth.pdh_locking）+ `rel.JI04`（CHARACTERIZED-BY pri.brownian_thermal_noise_fdt）
  - `loh2019`：新增 `rel.LO03` — `meth.sbs_thermal_self_referencing_l19 COMPETES-WITH meth.microcomb_self_referencing`（跨专题 Tier 1 引用）
- **P2.2 · 3 条类似表述合并**：
  - `coddington2010.pri.dual_comb_multiheterodyne_mapping` → `pri.dual_comb_multiheterodyne_detection`（coddington2016 canonical）；本地定义删除，`rel.C10_03` object 重指向
  - `picque2020.pri.self_referencing_f2f_framework` → `pri.self_referencing_f2f`（giunta2019 canonical）；本地定义删除，`rel.PD20_01` object + `rel.PD20_03` subject 重指向
  - `pasquazi2018.pri.temporal_cavity_soliton_dks` → `pri.dissipative_kerr_soliton`（kippenberg2018 canonical）；本地定义删除，`rel.P18_04`/`rel.P18_05` subject + breakthrough_paths `direction` 重指向（Tier 1 边的 corroborative citation 保留）
- **P2.3 · 1 条异议回报**：`pri.vibration_fopt_linear_coupling (sinclair2014)` 与 `pri.vibration_cavity_length_coupling (lezius2016)` 经 AI 复查实为**不同物理观测量**（前者是 f_opt 相噪 vs 后者是 f_rep/f_ceo 噪声），**建议保留并改为"保留+补关系"**，未执行合并，留专家再决。
- **P3.1**：AI 机械可闭环项仅 `ram_and_pdh_error_budget.md` 顶部补 `parke2025` — 复查发现前次 PR 已完成，无新增动作。
- **P3.2~P3.4 遗留动作**：其余 synthesis 页面遗留项全部属于专家决策/呈现风格选择（补缺 metric YAML vs 页面改定性；表格增列；draft 标记移除），不执行，转入"下一步建议"回报专家。
- **指标验证**：lint 0 error / 3 warning（与阶段 C 结束一致）；stats `cross_file_reuse` 76/862 → 76/859（分母 -3，纯粹来自节点合并），**指标前进有限**——符合报告 §5 预测，要到 15% 必须扩展到 `ent.*` / `met.*`。

---

## [2026-04-21] synthesis | 阶段 D-0：P2 跨文件复用分析 + P3 六篇 synthesis 数值复核

- **P2 · 跨文件复用**
  - 产出 `reports/shared_node_candidates.md`：Tier 1 已共用 39 / Tier 2 跨专题 1（`pri.brownian_thermal_noise_fdt`）/ Tier 3 疑似可合并 30
  - 新建 `topics/shared/registry.md` 登记 Tier 1 的 39 个事实公共 pri/meth（不物理迁移源文件）
  - 关键发现：仅靠 pri/meth 整治最多能把复用率从 8.8% 推至 ~11%；要达 15% 需要 P2.2 扩展到 `ent.*` / `met.*`
- **P3 · Synthesis 数值复核（6 篇）**
  - `vibration_insensitivity_landscape.md`：修正 Tao 2018（5×10⁻¹¹ → 0.8~2.5×10⁻¹⁰/g）、Chen 2014（2×10⁻¹⁰ → 1.7e-11~3.9e-10 区间）
  - `ram_and_pdh_error_budget.md`：修正 κ 单位（kHz/(m/s²) → kHz 腔线宽，避免与振动页 κ 混淆）、Tai 2016 σ_y（~10⁻¹⁶ → <3×10⁻¹⁷）；新增 Parke 2025 breakthrough 路径（σ_y 3×10⁻¹⁹）
  - `fiber_stabilization_landscape.md`：修正 Huang 2023 短期 σ_y（补 3.2×10⁻¹⁵ @ 1s）、Jeon 2025 τ 限定词（16ms 非 1s）、FP-vs-光纤差距（250× → ~10³× 时标对齐后）
  - `cryogenic_roadmap.md`：修正 124K × (IBS vs AlGaAs) 错配；补入 Robinson 2019 / Kedar 2023 mod σ_y
  - `spectral_hole_burning_track.md`：无数值错误，标注需专家深度参与
  - `breakthrough_paths_matrix.md`：阶段 C 后刷新日志（Parke 2025 / Kedar 2023 等单元格更新）
- **验证**：`python scripts/lint.py` = 0 error / 3 warning（与阶段 C 结束时一致）；`stats.py` 各指标未退化
- **残留专家决策**：Tier 3 的 10 条 pri/meth 合并判断、YAML 中补显式 SHARED-WITH 关系的授权、🟡 draft 标记移除

---



- **动机**：阶段 B 档位感知重估后暴露出真实缺口：7 条 breakthrough chain-gap + 15 条 breakthrough orphan（共 22 条 WARNING）。阶段 C 针对这两类 WARNING 做精准收敛。
- **Chain-gap 修复（7 → 0）**：为每条相关 BOUNDED-BY 关系补齐 `breakthrough_paths`（保留每条路径的 `direction` / `expected_gain` / `status` / `source.claim`）：
  - `chen2025::rel.Che02`（sub-5K Si 腔）— 新增 2 条（crystalline coating · cryogenic Q）
  - `kedar2023::rel.Ked03`（Si 腔 + AlGaAs）— 新增 1 条（crystalline coating demonstrated）
  - `numata2004::rel.N04`（镀层 ~15%）— 新增 1 条（crystalline coating demonstrated）
  - `numata2004::rel.N05`（spacer ~1%）— 新增 1 条（long-cavity 稀释，已非主动瓶颈）
  - `webster2008::rel.We08_01`（父级 Brownian on ent.fp_cavity_system）— 新增 3 条（crystalline coating · long cavity · cryogenic Q）
  - `zhang2014_ram::rel.Z14_01`（meth.pdh_locking BOUNDED-BY RAM）— 新增 3 条（brewster · active cancellation · bias field）
  - `zhang2014_ram::rel.Z14_05`（met.ram_fractional_instability BOUNDED-BY RAM）— 新增 3 条（同上）
- **Orphan 修复（15 → 0）**：按关系语义为每个 breakthrough 档位 orphan 节点挂单条关系，通常为 `ent IMPLEMENTS meth`、`met OPERATIONALIZED-AS meth`、`meth ENABLED-BY pri`：
  - `cole2013`（rel.C07：AlGaAs 镜 IMPLEMENTS 基底转移方法）
  - `hafner2015`（rel.H04a：长腔 IMPLEMENTS 自平衡安装方法）
  - `huang2023`（rel.HU05：光纤干涉仪 IMPLEMENTS 五层热屏蔽方法）
  - `kedar2023`（rel.Ked04：σ_y 指标 OPERATIONALIZED-AS 双偏振抑制方法）
  - `michaudbelleau2022`（rel.MB22_03：HCF 热噪声 PSD OPERATIONALIZED-AS 表征方法）
  - `numata2004`（rel.N15：热噪声 PSD OPERATIONALIZED-AS 分部件 FDT 分析方法）
  - `parke2025`（rel.P06/P07/P08：68 cm 腔 IMPLEMENTS · EOM 偏置方法 ENABLED-BY pri.ram_bias_field_cancellation · IMPLEMENTS PDH；一并解除 pri 与两条 meth 的 orphan 状态）
  - `robinson2019`（rel.R12：光功率漂移 OPERATIONALIZED-AS 低功率扫描方法）
  - `thorpe2011`（rel.TH02/TH03：SHB 参考 CHARACTERIZED-BY 环境灵敏度 · SHB σ_y OPERATIONALIZED-AS 两级锁定方法）
  - `webster2008`（rel.We08_04：σ_y OPERATIONALIZED-AS 振动不敏感 PDH 锁频方法）
  - `yan2018`（rel.YA02：合成激光 σ_y OPERATIONALIZED-AS 本文双腔 AOM 合成方法）
  - `zhang2014_ram`（rel.Z14_04a/04b：双通道 RAM 方法 ENABLED-BY pri.ram_active_cancellation · IMPLEMENTS PDH）
- **lint 结果**：breakthrough-tier WARNING 22 → 0；总体 warning 从 3 类 25 条 → 1 类 3 条（仅剩 evidence 档 `missing-conditions`，非阶段 C 范围）
- **验证**：
  - `python scripts/lint.py --topic ultrastable-laser --summary` → 0 error / 3 warning / 89 info
  - `python scripts/build_index.py` → 141 papers / 862 nodes / 973 relations（关系数增长对应阶段 C 新增 17 条关系）
- **运维**：更新 `TODO.md` 阶段 C 状态（标记完成）；`reports/chain_gap_ultrastable_v2.md` 与 `reports/orphans_ultrastable_v2.md` 的 22 条 WARNING 已全部转为 INFO / 已关系化。



- **动机**：阶段 A4 激活了 12 条 `breakthrough-missing-primary-metric` 告警，需要配套机制一次性完成：(1) lint / stats 按 `contribution_type` 分档、(2) 清零 12 条 σ_y 首批告警、(3) 重估 chain-gap / orphan 真实缺口。
- **lint.py 变更**（`scripts/lint.py`）：
  - 新增 `INFO` 等级；`check_orphan_nodes` 与 `check_reasoning_chain_gaps` 接收 `file_metas`，对 `evidence` / `framework` 档位论文降级为 `INFO`，仅 `breakthrough` 保持 `WARNING`
  - `check_breakthrough_primary_metric` 支持 `meta.primary_metric_exempt_reason` 豁免（允许值：`new_principle` / `new_method` / `landmark_consensus` / `psd_only`）
  - `format_grouped` / `format_json` 输出三段计数（error / warning / info）
- **stats.py 变更**（`scripts/stats.py`）：
  - `reasoning_chain_closure` 新增 `breakthrough_only` 子视图（BOUNDED-BY 仅统计 breakthrough 档位论文）
  - `sigma_y_linkage` 分母扣除 `primary_metric_exempt_reason` 标注的论文
- **YAML 回写**：12 条 σ_y 首批告警全部处理
  - 补 `role: primary` 到 σ_y 类指标（4 篇）：`huang2023` / `kim2008` (optical-microwave jitter) / `thorpe2011` (SHB stability) / `yan2018` (synthesized laser instability)
  - 补 `meta.primary_metric_exempt_reason`（8 篇）：`cole2013` (`new_principle`) / `drever1983` (`new_method`) / `kefelian2009` (`psd_only`) / `michaudbelleau2022` (`new_principle`) / `parke2025` (`new_method`) / `shaddock1999` (`new_method`) / `webster2007` (`new_principle`) / `zhang2014_ram` (`new_method`)
- **档位感知重估后指标**：
  - lint `breakthrough-missing-primary-metric`: 12 → 0
  - lint `reasoning-chain-gap` (超稳激光): 21 WARNING → 7 WARNING + 14 INFO
  - lint `orphan-node` (超稳激光): 90 WARNING → 15 WARNING + 75 INFO
  - stats `σ_y Linkage (USL)`: 66.7% (16/24) → 100% (16/16)
  - stats `reasoning_chain_closure.breakthrough_only`: 73.1% (19/26) — 已达 70% 目标
- **派生报告**：`reports/chain_gap_ultrastable_v2.md` + `reports/orphans_ultrastable_v2.md`（v1 报告保留为历史存档）
- **规范文档**：`docs/CONTRIBUTION_TIER_RULES.md` 升到 v1.2，§五从"提前公示"改为"已生效"并记录 `primary_metric_exempt_reason` 取值表
- **TODO.md 同步**：阶段 B 打勾；阶段 C 目标缩小到 v2 报告的 7 + 15 条 breakthrough 真缺口

---

## [2026-04-21] restructure | 阶段 A3 专家裁决 + A4 批量回写 `meta.contribution_type`

- **动机**：A2 Round 2 草案已交付 78 篇档位建议，专家在 `reports/contribution_tier_draft_ultrastable.md` 的 `决定` 列完成批量裁决，需要把最终档位固化到 YAML。
- **A3 变更**：在报告末尾新增"Round 3 · 阶段 A3 专家裁决结果（2026-04-21 定稿）"小节，记录：
  - 76 条 `ok`（accept AI 建议）
  - 2 条 override：`aasi2013.yaml` 🟥→🟩（LIGO 压缩光属外部应用，非本专题稳定度突破）；`yan2018.yaml` 🟩→🟥（multi-cavity-stabilized 新机制分支）
  - 最终分布：🟥 24 / 🟦 3 / 🟩 51（两条 override 自平衡，计数不变）
- **A4 变更**：把 `meta.contribution_type` 批量写入 `topics/ultrastable-laser/papers/*.yaml` 全部 78 个文件（插入位置：`meta:` 块内 `source_type:` 之后，符合 SCHEMA §v4.4 模板）。
- **TODO.md 同步**：阶段 A 状态改为"已完成，进入阶段 B"，A3/A4 打勾。
- **验证**：`python scripts/lint.py` → 0 errors（从 168 warnings → 180 warnings，新增 12 条均为"breakthrough 论文缺 σ_y primary-role 指标"告警——这是 A4 回写后 lint 档位感知首次激活带来的真实信号，是阶段 B 的工作对象，而非本次回归）。
- **影响**：阶段 A 机制落地闭环完成，为阶段 B（lint/stats 档位感知 + chain-gap/orphan 重估）解锁前置条件。

---

## [2026-04-21] restructure | 说明文件架构精简 · Karpathy 策展/簿记分离

- **动机**：对照知识库目标做评估，发现三大问题：(1) copilot-instructions.md 与 CLAUDE.md 大量重叠，AI agent 容易混读；(2) CLAUDE.md 末尾的"已有节点速查表"是手工维护的簿记，永远过时；(3) 阶段 A3 缺少清晰的专家操作触发器。
- **变更**：
  - `.github/copilot-instructions.md`：从 208 行精简为 33 行，仅保留项目定位 + 工作流路由表 + Copilot 专属约束；删除与 CLAUDE.md / SCHEMA.md 重叠的全部内容
  - `CLAUDE.md`：删除"已有节点速查表"（~150 行手工节点列表）和"处理顺序建议"节，改为指向自动生成的 `docs/CURRENT_NODES_REFERENCE.md`
  - `reports/contribution_tier_draft_ultrastable.md`：在文件顶部添加**阶段 A3 操作说明**（专家使用手册：如何填写 accept/override/批量 accept）
  - `topics/optical-frequency-combs/_meta/scoping_principles.md`：新建光学频率梳专题级评判原则 v1（Multi-Track 原则；过渡期档位判据；待专家确认的子域主线指标问题）
  - `scripts/build_index.py`：新增 `build_nodes_reference()` 函数，生成 `docs/CURRENT_NODES_REFERENCE.md`（按专题 × Level 0/1 实体 + 原理 + 方法三分类，替代手工节点速查表）
  - `SCHEMA.md`：§文档同步原则 升级至 v4.5——从"同步 10 文件"简化为"只做两件事"（更新 SCHEMA.md + 重跑 build_index.py）
- **验证**：`python scripts/build_index.py` → 成功生成所有 INDEX 文件 + `docs/CURRENT_NODES_REFERENCE.md`（59KB）
- **不涉及**：YAML 内容、论文数据、lint 规则均未改动



- **动机**：接续 Round 3 PR#1（文档层），完成 PR#2（综合视图层）+ PR#3（脚本与 YAML 数据层）。
- **PR#2 综合视图层**：
  - [`synthesis/stability_record_timeline.md`](topics/ultrastable-laser/synthesis/stability_record_timeline.md) 升级为**专题顶层导航页**：新增 §🧭 顶层导航跳转表、§一 σ_y Hall of Fame 世界记录总榜（标注 Allan 变体类型）、§二 子分支 SOTA（FP / 光纤 / SHB）
  - [`synthesis/breakthrough_paths_matrix.md`](topics/ultrastable-laser/synthesis/breakthrough_paths_matrix.md) 新增 §A.2 σ_y 增益矩阵（基线 × 预期 σ_y_gain × 代表论文）；B/C/D/E 各限制列补 `expected_σy_gain` 列
  - 其余 6 个 synthesis 页（thermal_noise / cryogenic / fiber / ram_pdh / vibration / shb）统一在开头新增 **"🎯 本页对 σ_y(1 s) 主线的贡献"** 小节，量化各条路径在 σ_y 主线上的角色
- **PR#3 脚本 + YAML 层**：
  - [`scripts/build_index.py`](scripts/build_index.py)：新增 `_infer_metric_role`（primary/secondary/engineering/enabling/interface），INDEX_metrics.md 与专题 INDEX 中按角色分组；BOUNDED-BY 输出补 `expected_σy_gain` 行
  - [`scripts/lint.py`](scripts/lint.py)：新增 `breakthrough-missing-primary-metric` 检查（超稳激光 breakthrough 档必须链接 σ_y primary metric，定义于本文件或关系引用外部 σ_y 指标）
  - [`scripts/stats.py`](scripts/stats.py)：推理就绪度量新增第 7 项 **σ_y-linkage rate**（ultrastable-laser breakthrough 论文中链接 σ_y primary 指标的比例，target=1.00）
  - [`templates/ultrastable_laser_template.yaml`](templates/ultrastable_laser_template.yaml)：新增超稳激光专用 YAML 模板，包含 `role` 字段文档化、`expected_σy_gain` 字段文档化、档位判定规则
  - YAML 回写代表论文：matei2017 / lee2026 / kessler2012 的 σ_y 指标写 `role: primary`，线宽/相干时间 `role: secondary`，振动灵敏度 `role: engineering`，镀层损耗角 `role: enabling`；matei2017 和 lee2026 的 3 条 breakthrough_paths 补 `expected_σy_gain`
  - [`SCHEMA.md`](SCHEMA.md) §六模板记录新字段（metric `role`、breakthrough_paths `expected_σy_gain`），均为可选字段，超稳激光专题建议使用
- **验证**：`python scripts/lint.py --summary` → 0 errors / 168 warnings（与基线一致）；`python scripts/stats.py` → 第 7 项 σ_y-linkage 指标就绪（当前无 USL breakthrough 论文，显示 n/a）；`python scripts/build_index.py` → 全部 INDEX 按新角色分组重新生成
- **遗留 / 下一步**：
  - 目前 USL 78 篇中无一篇 `contribution_type: breakthrough`（历史多为 `technical`），σ_y-linkage 指标当前 n/a，待 contribution_type 归一化（按 v4.4 映射）后激活
  - YAML `role` 回写仅覆盖 3 篇代表论文；启发式可覆盖 99% 的其余情况（通过 ID / name 模式），如需完全显式化可进一步批量回写

---

## [2026-04-21] restructure | Round 3 · 超稳激光 σ_y-first 主线化 · PR#1（文档层）

- **动机**：专家给出专题关键指标聚焦度判断——超稳激光高度聚焦于 σ_y(1 s)，线宽/频噪 PSD 为次要指标；**长期漂移**也降级（由下游光频标技术解决，非本专题核心战场）；频率标准聚焦于 accuracy；光学频率梳发散，需要 sub-topic 拆分。本轮聚焦超稳激光专题改造，按 3 个 PR 节奏推进。
- **信息层次/范围控制**：
  - 升级 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md) v1 → v2：σ_y(1 s) 单一主线；ADEV/MDEV/OADEV/Hadamard 等价但必须标注变体；长期 σ_y / 漂移降级为 evidence；子分支 SOTA 界定（FP 腔 / 光纤干涉仪 / SHB）；新增 §1.5 关键指标换算、§1.6 Allan 类型标注规范、§1.7 子分支 SOTA
  - 重排 [`topics/ultrastable-laser/_meta/architecture.md`](topics/ultrastable-laser/_meta/architecture.md) Key Performance Records 为三层（主线 / 次要 / 工程）；三栏表 → 四栏表，新增 `对 σ_y(1 s) 贡献量级` 列
  - [`docs/CONTRIBUTION_TIER_RULES.md`](docs/CONTRIBUTION_TIER_RULES.md) v1 → v1.1：Step 2 指标纪录条款添加超稳激光专题特别规则；§四专题级偏好节扩充为完整覆盖规则
  - [`CONTRIBUTING.md`](CONTRIBUTING.md) Step 2 checklist、[`CLAUDE.md`](CLAUDE.md) 步骤 4、[`.github/copilot-instructions.md`](. github/copilot-instructions.md) §6 同步 σ_y-first 规则
- **未触及**（推到 PR#2 / PR#3）：
  - PR#2：synthesis 页面补"对 σ_y 主线贡献总结"小节、`stability_record_timeline.md` 升级为顶层导航页、`breakthrough_paths_matrix.md` 补 `expected_σy_gain` 列
  - PR#3：scripts（build_index 启用 metric role 分类、lint 加 breakthrough 必须有 σ_y 检查、stats 加 σ_y-linkage rate）、YAML 回写 `met.*.role` + `breakthrough_paths[*].expected_σy_gain`、新增超稳激光专用 template、TODO/TOPICS 登记频率标准与光梳 sub-topic 规划
- **零 YAML 改动**，仅文档与规则层调整，现有 Round 2 档位建议仍然有效（σ_y-first 与 Round 2 的"稳定度 > 线宽"方向一致，只是更严格）

---

## [2026-04-21] restructure | v4.4 机制落地 · Round 2 · 专题原则 "稳定度>线宽" 纳入档位仲裁

- **动机**：Round 1 输出的 🟧 breakthrough? 17 条是"有弱纪录信号但需仲裁"的集合；专家提出**超稳激光专题内**应以系统稳定度与长期可靠性优于瞬时线宽作为偏好。该原则是**专题级**的，不是知识库整体原则。
- **信息层次/范围控制**：
  - 新增 `topics/ultrastable-laser/_meta/scoping_principles.md`（专题级，不上升为全局）
  - 在 `docs/CONTRIBUTION_TIER_RULES.md` §四 仅留一个指向该专题偏好的索引条目，全局规则本身不改
- **应用**：用新原则把 Round 1 的 17 条 🟧 全部仲裁完毕——8 条升 🟥（kim2008 / webster2008 / kefelian2009 / thorpe2011 / zhang2014_ram / kedar2023 / huang2023 / michaudbelleau2022，均为稳定度/长期/子分支纪录或新 `pri.*` 级机制），9 条降 🟩（millo2009 / jiang2011 / dong2015 / cole2016 / didier2018 / marchio2018 / herbers2019 / michaudbelleau2021 / ding2025，均为线宽/工程延伸/characterization）
- **交付**（零 YAML 改动）：
  - 更新 [`reports/contribution_tier_draft_ultrastable.md`](reports/contribution_tier_draft_ultrastable.md) 为 Round 2 版本；新分布 🟥 24 / 🟦 3 / 🟩 51（breakthrough 占比 30.8%，略高于 SCHEMA §9.1 预期上沿，但反映超稳激光突破史密度）
  - 新增 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md)
  - `docs/CONTRIBUTION_TIER_RULES.md` §四 增加"专题级偏好"索引节
- **下一步**：等待专家在 Round 2 建议表上 accept / override，再触发阶段 A4 批量回写 YAML `meta.contribution_type`。

---



## [2026-04-21] restructure | v4.4 机制落地 · 阶段 A1+A2 交付

- **动机**：v4.4 schema 在架构层面已就位，但 78 篇超稳激光论文 YAML 中 `meta.contribution_type` **实际填充率为 0**，导致 lint / stats 的 chain-gap / orphan 指标仍按旧预设报警，TODO.md 上的 21 / 90 数字不反映真实缺口。
- **本轮交付**（零 YAML 改动、完全可逆）：
  - 新增 [`docs/CONTRIBUTION_TIER_RULES.md`](docs/CONTRIBUTION_TIER_RULES.md)——三档分级操作规则书（判定次序 + 10 条边界案例 + 3 条互检问题）
  - 新增 [`reports/contribution_tier_draft_ultrastable.md`](reports/contribution_tier_draft_ultrastable.md)——78 篇论文档位建议表（AI 初判 🟥 16 / 🟧 17 / 🟦 3 / 🟩 42）
  - 更新 [`TODO.md`](TODO.md) 顶部优先级板块——把整治节奏切换到"阶段 A→B→C→D"
- **待专家介入**：在草案表 `决定` 列 accept / override / ❓，提交后触发阶段 A4 批量回写 YAML。
- **不改动**：本轮不修改任何 YAML，不调整 lint / stats 逻辑，不更改 schema 规范文本。

---

## [2026-04-21] schema | v4.3 → v4.4 引入三档贡献分级

- **动机**：专家反馈"逻辑推理机制没形成"，根因之一是 `contribution_type` 旧 enum 过粗（`technical` / `framework` 二分），导致 evidence 级论文被要求补完整限制链，催生大量假 chain-gap / orphan。
- **变更**：
  - SCHEMA.md §9.1 新增三档分级：`breakthrough` / `evidence` / `framework`，明确 evidence 档位最低门槛
  - SCHEMA.md §9.2 新增向后兼容映射表（7 种历史值 → 3 档）
  - SCHEMA.md §六 YAML 模板默认值 `technical` → `evidence`
  - SCHEMA.md 头注释版本 v4.3 → v4.4
  - README.md 新增"项目目标"主/次分层 + "论文贡献分级"小节
  - CONTRIBUTING.md Step 2 切换到三档；新增"Evidence 档位最低入库门槛"小节
  - .github/ISSUE_TEMPLATE/ingest-paper.yml dropdown 统一到三档
  - scripts/process_paper.py 基础模板默认 `evidence`
  - TODO.md 增加"v4.4 重估提示"，提醒 chain-gap / orphan 数字在分级生效后需重算
- **不改动**：未批量迁移既有 YAML 文件的历史 `contribution_type` 值（按 §9.2 映射解读，触及时归一化）；未改 Schema 主干（ent/pri/meth/met/rel 保留）；未引入新 lint 规则。
- **后续**：Step 2（regime / resolves / exposes 状态层）需专家先确认 regime 枚举范围，暂不实施。

---

## [2026-04-20] lint | P1+P2 质量修复——消除全部 lint 错误 + 证据覆盖 100%

- **Lint 错误归零**：198 errors → 0 errors（三类全部修复）
  - 5 dangling-ref：补充缺失节点定义（`meth.oscat_dual_comb`、`ent.filtered_tisa_astrocomb_y12`、`pri.eom_acoustic_resonance_limit_t17`、`pri.am_pm_conversion_photodetection`）
  - 21 duplicate-def：10 个重复节点 ID 去重，保留权威定义（涉及 8 个 OFC 文件）
  - 172 duplicate-rel-id：11 个文件 relation ID 重命名（解决首字母缩写冲突）
- **Lint 警告大幅降低**：294 warnings → 168 warnings（missing-evidence 分类完全消除）
- **证据覆盖率**：86.9% → **100%**（957/957 relations 均有 source.claim）
- **条件完备率**：94.8% → 95.3%（新增原理节点自带 conditions）
- **更新度量对比**（P0 baseline → P1+P2 修复后）：

| 度量 | P0 值 | P1+P2 值 | 目标 | 状态变化 |
|------|-------|----------|------|---------|
| 限制链闭环率 | 71.3% | 71.3% | ≥70% | ✅→✅ |
| 证据覆盖率 | 86.9% | **100%** | ≥90% | ❌→✅ |
| 条件完备率 | 94.8% | 95.3% | ≥80% | ✅→✅ |
| 跨文件复用度 | 8.8% | 8.8% | higher | — |
| 综合页面覆盖 | 1/4 | 1/4 | 全覆盖 | ⚠️ |
| 矛盾可见度 | 119 | 118 | more | — |

## [2026-04-20] restructure | P0 整固——自动化基础设施与度量体系

- **新增脚本**（5 个）：
  - `scripts/stats.py` — 6 项推理就绪度量（限制链闭环率、证据覆盖率、条件完备率、跨文件复用度、综合覆盖、矛盾可见度）
  - `scripts/lint.py` — 11 项健康检查（孤立节点、悬空引用、重复定义、推理链缺口等）
  - `scripts/build_index.py` — 从 YAML 自动生成分层 INDEX（替代手工维护）
  - `scripts/graph.py` — 知识图谱导出（JSON/GraphML）+ hub/orphan/bridge 诊断
  - `scripts/freshness.py` — 综合页面新鲜度追踪
- **分层索引**：INDEX.md 改为脚本自动生成 + 新增 INDEX_metrics.md、INDEX_principles.md、各专题 INDEX.md
- **专题元数据**：每个专题新增 `_meta/architecture.md`（架构图、限制链、路线图）
- **CI 集成**：新增 `.github/workflows/kb-lint-stats.yml`（PR 时自动运行 lint + stats）
- **Baseline 度量**（2026-04-20，141 篇论文 / 869 节点 / 957 关系）：

| 度量 | 当前值 | 目标 | 状态 |
|------|--------|------|------|
| 限制链闭环率 | 71.3% (87/122) | ≥70% | ✅ |
| 证据覆盖率 | 86.9% (832/957) | ≥90% | ❌ |
| 条件完备率 | 94.8% (220/232) | ≥80% | ✅ |
| 跨文件复用度 | 8.8% (76/862) | higher | — |
| 综合页面覆盖 | 1/4 专题 | 全覆盖 | ⚠️ |
| 矛盾可见度 | 119 (6 contested + 113 open_q) | more | — |

- **Lint baseline**：198 errors (5 dangling-ref + 21 duplicate-def + 172 duplicate-rel-id), 294 warnings
- **图谱诊断**：113 孤立节点，hub 节点前3: ent.fp_cavity_system (75度), ent.optical_frequency_comb (56度), ent.microresonator_frequency_comb (37度)

## [2026-04-20] restructure | 引入 Karpathy LLM Wiki 运维层

- 新增 `INDEX.md`（全局导航索引）、`LOG.md`（本文件）、`PROCESSED_PAPERS.md`（论文详细列表）
- 新增 `topics/ultrastable-laser/synthesis/` 综合分析页面目录（首批 2 个页面）
- SCHEMA.md 新增第十节「知识库运维操作」（Ingest/Query/Lint 工作流形式化）
- SCHEMA.md 第八节精简（详细论文列表迁移至 PROCESSED_PAPERS.md）
- CLAUDE.md 新增「人机协作原则」（Karpathy 人机分工思想）
- README.md 更新反映新文件和运维流程
- **设计理念**：在保持 YAML 符号主义架构核心优势的基础上，叠加面向人类可读性和 AI 可维护性的运维基础设施

## [2026-04-19] ingest | OFC 批量提取（~40 篇技术论文）

- 光学频率梳专题新增约 40 篇技术论文 YAML（v4.1 格式）
- 覆盖：飞秒激光器梳、微腔梳、电光梳、天文光梳、双梳光谱、中红外梳
- 关键新增节点：ent.battery_operated_microcomb_s18、ent.cep_hhg_comb_system_l22 等
- OFC 专题论文总数达到 61 篇，节点总数 ~456

## [2026-04-19] ingest | OFC 框架型综述（3 篇）

- `picque2020.yaml`：Picqué/Diddams/Vahala/Udem 2020 Science — 光频梳 20 年回顾
- `droste2016.yaml`：Droste & Newbury 2016 — Er:fiber 梳综述
- `endo2018.yaml`：Endo 2018 — 超低噪声光频梳综述

## [2026-04-18] schema | Schema v4.1

- 合并"光钟"+"微波频率标准"为"频率标准"专题
- 光学频率梳重组为应用-技术-原理三层架构
- 新增天文光梳子分支
- 新增"时频计量数学基础"跨专题模块
- 目录 `topics/optical-clocks/` 迁移为 `topics/frequency-standards/`

## [2026-04-17] restructure | 超稳激光 78 篇全量升级至 v4.1

- 所有 78 篇超稳激光论文 YAML 补充 principles/methods/metrics/relations 推理链条
- 补充 `breakthrough_paths`、`open_questions`、`contested_claims`
- 关系结构全面合规（direction 字段从 ent.* → pri.*/meth.*）

## [2026-04-16] restructure | Schema v4.0 多专题架构

- 从单专题（超稳激光）扩展为六专题体系
- 新增框架型论文处理规范（第九节）
- 首批框架文档：`fortier2026.yaml`（频率标准）、`giunta2019.yaml`（光学频率梳）、`dimarcq2024.yaml`（时间标尺）

## [2026-04-16] ingest | lee2026.yaml — 世界纪录

- 新世界纪录：mod σ_y = 2.5×10⁻¹⁷（17K Si 腔 + AlGaAs 晶体镀层）
- 确认 `pri.silicon_cte_zero_crossing_17k`（Si CTE 第二零点）
- 确认 `pri.optical_frequency_averaging`（多腔光学频率平均）

## [2026-04-10] schema | Schema v3.0 — 实例节点降级

- 4 个 FP 腔"独立方案"从 Level 1 降为 Level 2
- 取消 8 条 COMPETES-WITH 关系
- 6 个工程推理并入父原理 condition_variables
- 新增"稳频策略"分支

## [2026-04-06] ingest | 首批超稳激光论文（~15 篇核心文献）

- 建立超稳激光专题基础架构
- 核心节点：ent.fp_cavity_system、pri.brownian_thermal_noise_fdt、meth.pdh_locking
- 首批文献：Drever 1983、Young 1999、Numata 2004、Kessler 2012、Matei 2017 等

---

## [2026-04-23] ingest | Batch 2：超稳激光专题 6 篇新论文摄入

新增 6 个 YAML 文件（5 篇至 ultrastable-laser，1 篇自由空间时频）：

- `xia2025.yaml`（IUCMUIEI）：Xia et al. 2025 — 全数字 FPGA 多环路 USL 自动锁定
  1.5×10⁻¹⁵ @1 s（载波锁定），FNC 75 dB 噪声抑制，10 s 内复锁
- `wang2024a.yaml`（CYS7GEVR）：Wang et al. 2024 — 光频净化中继（NTSC/CAS）
  8.43×10⁻¹⁹ @10,000 s，106 km 通信光纤，消除相位周期跳变
- `giunta2020b.yaml`（H7A8L8LT）：Giunta et al. 2020 — 紧凑光子微波振荡器
  12 GHz，−83 dBc/Hz @1 Hz（腔热噪声限），OFD 残余底 −115 dBc/Hz
- `kudelin2024.yaml`（AF34FGMU）：Kudelin et al. 2024 — 芯片集成光子微波振荡器
  20 GHz，−135 dBc/Hz @10 kHz，SiN 微腔梳 + 6.3 mm 微型 F-P 腔
- `schioppo2021.yaml`（K5JMAYPZ）：Schioppo et al. 2021 — 2220 km 光纤网络 NPL↔PTB 比对
  合并 MDEV 7×10⁻¹⁷（30–200 s），PTB Si 腔 4×10⁻¹⁷，NPL ULE 腔 6×10⁻¹⁷
- `shen2022.yaml`（P92ZFIAQ）：Shen et al. 2022 — 113 km 自由空间时频传递
  < 4×10⁻¹⁹ @10,000 s，双向 OFC + LOS + 自适应光学，Nature 2022

---

*本日志由 AI 自动维护。每次 Ingest/Restructure/Lint 后追加条目。*
