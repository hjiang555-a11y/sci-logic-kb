# TODO — 知识库待处理工作登记

> **定位**：集中登记各专题尚未完成的结构化工作，避免分散遗忘。
>
> **维护原则**：
> - 本文件是"导航器"，具体细节链接到 `reports/` 或 issue
> - 每完成一项更新对应状态 / 同步 LOG.md
> - 新增待办请加到对应专题段落，严重缺口请同时在 TOPICS.md 降级对应专题优先级

---

## 📌 当前优先级：阶段 A（机制落地闭环）已完成 · 阶段 B（档位感知）已完成 · 阶段 C（breakthrough 档位真缺口清零）已完成 · 阶段 D-0（整治手册沉淀 P2/P3 AI 机械部分）已完成 — 专家审核后进入阶段 D

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
> - ⏳ **阶段 D**：沉淀专题整治手册，再启动其他专题扩展

### 超稳激光（重点整治专题）

#### ✅ P0 · Chain-gap 闭环（7 条 breakthrough WARNING → 0，阶段 C 已完成）
- 详见 [`reports/chain_gap_ultrastable_v2.md`](reports/chain_gap_ultrastable_v2.md)
- 已补 `breakthrough_paths`：`chen2025.Che02`（Si sub-5K）· `kedar2023.Ked03`（AlGaAs 低温 Si 腔）· `numata2004.N04/N05`（镀层 15% / spacer 1%）· `webster2008.We08_01`（ULE 父级 Brownian）· `zhang2014_ram.Z14_01/Z14_05`（RAM）
- 14 条 evidence-tier chain-gap INFO 按 §9.1 保留不强制闭环

#### ✅ P1 · Orphan 收敛（15 条 breakthrough WARNING → 0，阶段 C 已完成）
- 详见 [`reports/orphans_ultrastable_v2.md`](reports/orphans_ultrastable_v2.md)
- 已挂关系的 breakthrough-tier 节点：`cole2013/hafner2015/huang2023/kedar2023/michaudbelleau2022/numata2004/parke2025(×3) / robinson2019/thorpe2011(×2)/webster2008/yan2018/zhang2014_ram` 共 15 个
- 75 条 evidence-tier orphan INFO 按 §9.1 保留

#### ⏳ P2 · 跨文件复用度提升（8.8% → 15%+）— AI 分析已完成，待专家审核合并
- 已产出 [`reports/shared_node_candidates.md`](reports/shared_node_candidates.md)（Tier 1 已共用 39 / Tier 2 跨专题 1 / Tier 3 疑似可合并 30）
- 已新建 [`topics/shared/registry.md`](topics/shared/registry.md)——登记事实上已共用的 39 个 pri/meth 节点
- **关键发现**：仅靠 pri/meth 整治无法单独达到 15% 目标，需要下一轮扩展到 `ent.*` / `met.*`
- 专家待决动作：
  - [ ] 逐条审核 Tier 3 的 10 个重点候选（保留+补关系 vs 合并删除）
  - [ ] 授权是否在论文 YAML 中显式补 `SHARED-WITH pri.brownian_thermal_noise_fdt`（当前只有隐式引用）
  - [ ] 启动 P2.2 `ent.*` / `met.*` 共用候选扫描（本轮未覆盖）

#### ⏳ P3 · Synthesis 页面数值复核（AI 机械复核完成，🟡 draft 保留待专家签字）
- 每篇追加"📋 数值复核日志"章节，记录发现的问题与已修正内容
- [x] `vibration_insensitivity_landscape.md` — 修正 Tao 2018（5×10⁻¹¹ → 0.8~2.5×10⁻¹⁰/g）和 Chen 2014（2×10⁻¹⁰ → 1.7e-11~3.9e-10 区间）两处数值错误；标注 Chen 2020 / Sanjuan 2019 YAML 缺 κ metric
- [x] `ram_and_pdh_error_budget.md` — 修正 κ 单位错误（kHz/(m/s²) → kHz 腔线宽）；修正 Tai 2016 σ_y（~10⁻¹⁶ → <3×10⁻¹⁷）；新增 Parke 2025 breakthrough 路径（σ_y 3×10⁻¹⁹ @ 10–100s）
- [x] `fiber_stabilization_landscape.md` — 修正 Huang 2023 短期 σ_y（漏写 3.2×10⁻¹⁵ @ 1s）；修正 Jeon 2025 τ 标注（应为 16ms 非 1s）；修正 FP-vs-光纤差距（250× → ~10³× 时标对齐后）
- [x] `cryogenic_roadmap.md` — 修正 124K 两行的 AlGaAs/IBS 错配；补入 Robinson 2019 (6.5×10⁻¹⁷ @ 4K) 与 Kedar 2023 (5.5/3.5×10⁻¹⁷ Si6/Si5) 的 mod σ_y 数据
- [x] `spectral_hole_burning_track.md` — 无数值错误可改（定性表述为主），标注需专家深度参与
- [x] `breakthrough_paths_matrix.md` — 追加"阶段 C 后刷新日志"，记录 Parke 2025 等单元格更新
- 专家待决动作：
  - [ ] 审核每页"📋 数值复核日志"下的"遗留动作"项（典型为 YAML 缺 metric 节点 / 时标呈现风格选择）
  - [ ] 决定是否移除 🟡 draft 标记

---

### 光学频率梳（已入库待深化）

- [ ] 修 36 条低成本 lint warnings（主要是 `missing-conditions`）
- [ ] 其他整固（orphan、chain-gap）延后到未来轮次
- [ ] 无综合页面（`synthesis/`），未来可参考超稳激光专题模式补建

---

### 频率标准（骨架）

> **状态**：仅接受新摄入，不投入整治资源
- [ ] 摄入 ≥ 3 篇代表论文（光钟类：Sr、Yb、Hg、Al⁺；微波类：Cs fountain、H-maser）
- [ ] 激活 Level 1 实体节点

---

### 时间标尺与钟组（骨架）

> **状态**：仅接受新摄入
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
- [ ] CI 集成 freshness 检查：synthesis 页面依赖的 yaml 更新时自动标 `needs-refresh` 标签
- [ ] 探索 graph.py 输出的交互式可视化（d3 / cytoscape）

---

## 📋 Schema / 架构层面

- [ ] 评估是否需要新增"`status: resolved`"字段到 BOUNDED-BY 关系（当限制已被工程超越时）
- [ ] 评估 `INSTANCE-OF` 是否作为正式谓词（或继续用 `PART-OF` 表示 Level 2 参数变体）
- [ ] 评估 `SHARED-WITH` 关系的使用规范（当前零使用，需要实际案例触发规则定稿）

---

> 本文件随工作推进持续更新；每次 PR 合并后请检查并勾选 / 删减对应条目，保持 TODO 长度收敛。
