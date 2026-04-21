# 知识库演化日志

> **格式约定**：每条日志以 `## [YYYY-MM-DD] type | description` 开头。
> 支持的类型：`ingest`（摄入）、`restructure`（重组）、`lint`（健康检查）、`query`（查询反哺）、`contradiction`（矛盾发现）、`schema`（Schema 升级）、`synthesis`（综合页面）
>
> **使用方法**：`grep "^## \[" LOG.md | grep "contradiction"` 可快速定位矛盾点。

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

*本日志由 AI 自动维护。每次 Ingest/Restructure/Lint 后追加条目。*
