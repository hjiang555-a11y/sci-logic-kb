# TODO — 知识库待处理工作登记

> **定位**：集中登记各专题尚未完成的结构化工作，避免分散遗忘。
>
> **维护原则**：
> - 本文件是"导航器"，具体细节链接到 `reports/` 或 issue
> - 每完成一项更新对应状态 / 同步 LOG.md
> - 新增待办请加到对应专题段落，严重缺口请同时在 TOPICS.md 降级对应专题优先级

---

## 📌 当前优先级：**阶段 D（专家审阅 + 覆盖扩展）准备中** — v4.5 基线已稳定（2026-04-22）

> **现状快照（基于 `python scripts/lint.py --summary` / `python scripts/stats.py` / `python scripts/freshness.py --check`）**
>
> - 库存：**170 篇论文**（超稳激光 78 / 光学频率梳 90 / 频率标准 1 / 时间标尺 1）
> - 质量基线：**lint 0 error / 3 warning / 188 info**
> - 推理指标：Reasoning Chain Closure **76.6%**；breakthrough-only **100%**；Evidence Coverage **100%**；Condition Completeness **98.8%**
> - 结构瓶颈：**Synthesis Coverage 仅 1/4 topic**；Cross-file Reuse **8.7%**
> - 维护瓶颈：freshness 检查显示**超稳激光 8/8 个 synthesis 页面 stale**
>
> **建议结论**：超稳激光专题已经从"主线闭环建设"转入"维护收口"；下一轮系统投入应转向**光学频率梳 synthesis 启动**，同时把超稳激光综合页 freshness / 专家签字收尾。

> **v4.4 机制落地进度（2026-04-21）**：按"先形成工作机制再扩展规模"迭代计划：
>
> - ✅ **阶段 A1**：档位分级操作规则书 → [`docs/CONTRIBUTION_TIER_RULES.md`](docs/CONTRIBUTION_TIER_RULES.md)（含"专题级偏好"索引节）
> - ✅ **阶段 A2 · Round 1**：78 篇档位建议草案（🟥 16 / 🟧 17 / 🟦 3 / 🟩 42）
> - ✅ **阶段 A2 · Round 2**：专家增补**专题原则"稳定度 > 线宽"**（见 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md)），清空 🟧 档——8 升 🟥 / 9 降 🟩。新分布 🟥 24 / 🟦 3 / 🟩 51 → [`reports/contribution_tier_draft_ultrastable.md`](reports/contribution_tier_draft_ultrastable.md)
> - ✅ **阶段 A3**：专家批量裁决完毕（76 accept + 2 override：`aasi2013` 🟥→🟩；`yan2018` 🟩→🟥），最终分布 🟥 24 / 🟦 3 / 🟩 51
> - ✅ **阶段 A4**：78 篇 YAML 的 `meta.contribution_type` 已批量回写（lint 0 errors）
> - ✅ **阶段 B · 2026-04-21 完成**：
>   - `scripts/lint.py` 引入档位感知：`reasoning-chain-gap` / `orphan-node` 对 `evidence` / `framework` 档位论文降级为 `INFO`，仅 `breakthrough` 档位保持 `WARNING`
>   - `scripts/stats.py` 引入 `reasoning_chain_closure.breakthrough_only` 子视图（tier-scoped 73.1% [19/26]）
>   - 新增 `meta.primary_metric_exempt_reason` 字段供 breakthrough 论文显式声明"σ_y 主线不适用原因"（`new_principle` / `new_method` / `landmark_consensus` / `psd_only`）
>   - 12 条 `breakthrough-missing-primary-metric` 告警全部清零（4 篇补 `role: primary` + 8 篇补 `primary_metric_exempt_reason`）
>   - lint 档位感知重估后真实缺口：**chain-gap 21 → 7 WARNING + 14 INFO**；**orphan 90 → 15 WARNING + 75 INFO**
>   - 重估报告：[`reports/chain_gap_ultrastable_v2.md`](reports/chain_gap_ultrastable_v2.md) · [`reports/orphans_ultrastable_v2.md`](reports/orphans_ultrastable_v2.md)
>   - σ_y Linkage（stats 指标 #7）：66.7% (16/24) → **100% (16/16)** — 8 篇豁免后分母修正
> - ✅ **阶段 C · 2026-04-21 完成**：基于 v2 报告的 **7 条 breakthrough chain-gap** 与 **15 条 breakthrough orphan** 精准收敛
>   - chain-gap：7 → 0（`chen2025.Che02` · `kedar2023.Ked03` · `numata2004.N04/N05` · `webster2008.We08_01` · `zhang2014_ram.Z14_01/Z14_05` 全部补 `breakthrough_paths`）
>   - orphan（breakthrough 档位）：15 → 0（14 个方法节点 + 1 个原理节点 `pri.ram_bias_field_cancellation` 全部挂关系）
>   - lint 结果：0 error / 3 warning（仅 3 条 `missing-conditions` 遗留，且均属 evidence 档，非阶段 C 范围）
> - ⏳ **阶段 D**：完成专家审阅、综合页 freshness 收口，并把方法论迁移到光学频率梳专题

### 超稳激光（重点整治专题）

#### ✅ P0 · Chain-gap 闭环（7 条 breakthrough WARNING → 0，阶段 C 已完成）
- 详见 [`reports/chain_gap_ultrastable_v2.md`](reports/chain_gap_ultrastable_v2.md)
- 已补 `breakthrough_paths`：`chen2025.Che02`（Si sub-5K）· `kedar2023.Ked03`（AlGaAs 低温 Si 腔）· `numata2004.N04/N05`（镀层 15% / spacer 1%）· `webster2008.We08_01`（ULE 父级 Brownian）· `zhang2014_ram.Z14_01/Z14_05`（RAM）
- 14 条 evidence-tier chain-gap INFO 按 §9.1 保留不强制闭环

#### ✅ P1 · Orphan 收敛（15 条 breakthrough WARNING → 0，阶段 C 已完成）
- 详见 [`reports/orphans_ultrastable_v2.md`](reports/orphans_ultrastable_v2.md)
- 已挂关系的 breakthrough-tier 节点：`cole2013/hafner2015/huang2023/kedar2023/michaudbelleau2022/numata2004/parke2025(×3) / robinson2019/thorpe2011(×2)/webster2008/yan2018/zhang2014_ram` 共 15 个
- 75 条 evidence-tier orphan INFO 按 §9.1 保留

#### ✅ P2 · 跨文件复用度提升（Tier 3 审批落地完成，2026-04-21 晚批次）
- 已产出 [`reports/shared_node_candidates.md`](reports/shared_node_candidates.md)（Tier 1 已共用 39 / Tier 2 跨专题 1 / Tier 3 疑似可合并 30）
- 已新建 [`topics/shared/registry.md`](topics/shared/registry.md)——登记事实上已共用的 39 个 pri/meth 节点
- **P2.1 已执行**：5 条"❌ 保留+补关系" + 1 条 SBS COMPETES-WITH = 6 个新关系落地（详见 LOG 2026-04-21 restructure 条目）
- **P2.2 已执行**：3 条"⚠️ 类似表述"合并（`dual_comb_multiheterodyne_mapping` / `self_referencing_f2f_framework` / `temporal_cavity_soliton_dks`），本地重复定义删除并重定向关系到 Tier 1 规范节点
- **P2.3 AI 回报专家异议**：`pri.vibration_fopt_linear_coupling` (sinclair2014) 与 `pri.vibration_cavity_length_coupling` (lezius2016) 物理观测量实为不同（f_opt 相噪 vs f_rep/f_ceo 噪声），**未执行合并**，建议改为保留+补 `DERIVED-FROM` 关系——等专家裁决
- **指标结果**：cross_file_reuse 76/862 → 76/859（8.8% 保持；pri/meth 整治已做到极限，达 15% 必须启动 P2.4 的 `ent.*` / `met.*` 扫描）
- 剩余待决动作：
  - [ ] 专家审核 P2.3 的 vibration 节点异议（合并 vs 保留）
  - [ ] 专家授权是否在论文 YAML 中显式补 `SHARED-WITH pri.brownian_thermal_noise_fdt`（当前只有隐式 subject/object 引用）
  - [ ] **P2.4 启动：`ent.*` / `met.*` 共用候选系统性扫描**（本轮未覆盖，是推进 15% 目标的关键一步）

#### ✅ P3 · Synthesis 页面数值复核（AI 机械部分完成，🟡 draft 仍待专家签字）
- 每篇追加"📋 数值复核日志"章节，记录发现的问题与已修正内容
- [x] `vibration_insensitivity_landscape.md` — 修正 Tao 2018（5×10⁻¹¹ → 0.8~2.5×10⁻¹⁰/g）和 Chen 2014（2×10⁻¹⁰ → 1.7e-11~3.9e-10 区间）两处数值错误；标注 Chen 2020 / Sanjuan 2019 YAML 缺 κ metric
- [x] `ram_and_pdh_error_budget.md` — 修正 κ 单位错误（kHz/(m/s²) → kHz 腔线宽）；修正 Tai 2016 σ_y（~10⁻¹⁶ → <3×10⁻¹⁷）；新增 Parke 2025 breakthrough 路径（σ_y 3×10⁻¹⁹ @ 10–100s）；「涉及源文件」已含 `parke2025`
- [x] `fiber_stabilization_landscape.md` — 修正 Huang 2023 短期 σ_y（漏写 3.2×10⁻¹⁵ @ 1s）；修正 Jeon 2025 τ 标注（应为 16ms 非 1s）；修正 FP-vs-光纤差距（250× → ~10³× 时标对齐后）
- [x] `cryogenic_roadmap.md` — 修正 124K 两行的 AlGaAs/IBS 错配；补入 Robinson 2019 (6.5×10⁻¹⁷ @ 4K) 与 Kedar 2023 (5.5/3.5×10⁻¹⁷ Si6/Si5) 的 mod σ_y 数据
- [x] `spectral_hole_burning_track.md` — 无数值错误可改（定性表述为主），标注需专家深度参与
- [x] `breakthrough_paths_matrix.md` — 追加"阶段 C 后刷新日志"，记录 Parke 2025 等单元格更新
- **P3 AI 机械可闭环项均已完成**（ram_and_pdh 的 parke2025 源文件登记已在既有 PR 中落地）。遗留动作全部属于专家决策/风格选择：
  - [ ] 统一处理 freshness 报警的 8 个超稳激光 synthesis 页面（逐页刷新或在 header 明确延后）
  - [ ] 专家确认 Kedar 2023 在 cryogenic_roadmap 单列行 vs 合并行（呈现）
  - [ ] 专家确认 fiber_stabilization 的「子分支 SOTA 按时标分桶」呈现风格
  - [ ] 专家决定 Chen 2020 / Sanjuan 2019 的 κ 是补入对应 YAML metrics 还是页面改为定性（这一决策也影响 Hafner 2020 κz 表格是否加列）
  - [ ] 专家确认 ram_and_pdh §四 的 `ent.brewster_eom_t16` 是否入 `meth.pdh_locking` family
  - [ ] 专家决定 6 篇 synthesis 的 🟡 draft 标记是否移除（批量签字 vs 按页逐一）

---

### 光学频率梳（已入库待深化）

> **现状**：已入库 **90 篇**，三层架构与 9 条子域主线已明确，但 `synthesis/` 仍为空，是当前全库最大的读者入口缺口。
- [ ] 建立首批 synthesis 页面（建议最小集：频率综合 / 双梳光谱 / 微梳平台 / 光谱应用）
- [ ] 把 9 条子域主线映射到页面结构，明确"哪个页面服务哪个查询"
- [ ] 梳理 OFC ↔ USL / 频率标准 的跨专题接口节点，优先提升可复用 `pri.*` / `meth.*`
- [ ] 其他 orphan / chain-gap 整固延后到 synthesis 骨架搭起之后

---

### 频率标准（骨架）

> **状态**：1 篇 framework；仅接受新摄入，不投入整治资源
- [ ] 摄入 ≥ 3 篇代表论文（光钟类：Sr、Yb、Hg、Al⁺；微波类：Cs fountain、H-maser）
- [ ] 激活 Level 1 实体节点

---

### 时间标尺与钟组（骨架）

> **状态**：1 篇 framework；仅接受新摄入
- [ ] 摄入 UTC/TAI 综述、本地 UTC(k) 实现、Kalman 合成算法论文

---

### 时间频率传递（骨架空壳）

> **状态**：0 论文，仅架构占位
- [ ] 摄入 ≥ 3 篇代表论文：光纤相干链路 + TWSTFT + GNSS 载波相位比对
- [ ] 激活 Level 1 实体节点

---

### 时频计量数学基础（未建）

> **状态**：架构未启动
- [ ] 确定是作为独立专题还是放在 `topics/shared/metrics/`
- [ ] 摄入基础方差体系论文（Allan, Hadamard, Mod-σ, Dynamic Allan, …）

---

## 🛠️ 开发 / 工具 / CI

### Round 4 延后项
- [x] CI 集成 freshness 检查：synthesis 页面依赖的 yaml 更新时自动标 `needs-refresh` 标签（2026-04-22，v4.5；`.github/workflows/synthesis-freshness.yml` + `scripts/freshness.py --json`，git-log 时间戳）
- [x] 探索 graph.py 输出的交互式可视化（d3 / cytoscape）（2026-04-22，v4.5；Cytoscape.js，静态 `docs/graph/index.html` + `docs/graph/viewer.js`，`bash scripts/build_graph_view.sh` 一键刷新）
- [ ] 固化"文档状态对齐"维护约定：涉及论文数 / 专题状态 / 当前重点的文档统一以 `stats.py`、`PROCESSED_PAPERS.md` 与 `TODO.md` 为对照源

---

## 📋 Schema / 架构层面

- [x] 评估是否需要新增 `limit_status: resolved` 字段到 BOUNDED-BY 关系（当限制已被工程超越时）（2026-04-22，v4.5；采用 4 态枚举 `limit_status: active | conditional | resolved | refuted` + `resolved_by` + `resolution_source`，见 SCHEMA §4.2；stats 新增 `limit_resolution_rate` 指标；migrator `scripts/migrate_bounded_status.py`；3 条示范落地：`cole2013.C05` / `hafner2015.H05` / `chen2025.Che02`）
- [x] 评估 `INSTANCE-OF` 是否作为正式谓词（或继续用 `PART-OF` 表示 Level 2 参数变体）（2026-04-22 **决策：不新增谓词**；改为在 `ent.*` 上新增可选字段 `instance_of`，配套 lint 一致性检查；进入一年观察窗口，≥ 20 节点使用后再评估升格。已回填 3 节点：`chen2025.si_crystal_fp_cavity_sub5k_c25` / `chen2020.cubic_dual_cavity_c20` / `hafner2015.self_balancing_long_cavity_h15`）
- [x] 评估 `SHARED-WITH` 关系的使用规范（当前零使用，需要实际案例触发规则定稿）（2026-04-22，v4.5；正式纳入第 9 种谓词，SCHEMA §5 规定触发条件 / 禁用场景 / lint 双规则；`topics/shared/registry.md §3` Tier 2 作为白名单唯一源；首批真实 SHARED-WITH 关系待下一篇在 OFC/频率标准定义 thermal-noise 变体原理的论文触发）

---

> 本文件随工作推进持续更新；每次 PR 合并后请检查并勾选 / 删减对应条目，保持 TODO 长度收敛。
