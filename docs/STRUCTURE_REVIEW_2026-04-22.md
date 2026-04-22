# 知识库结构审查 · 2026-04-22

> **定位**：给专家（= 你）一份**可勾选、可选项、可改写**的结构诊断 + 优化提案。
>
> **读法**：每个"优化项"给出【现状】→【问题】→【选项 A/B/C】→【我的建议】→`[ ]` 勾选框。你只需要：① 在每项里选一个字母，或直接在"改写"栏写你的版本；② 最后我按你批的结果分 PR 执行。
>
> **本轮不改任何结构文件**。这是纯审核文档。
>
> **评估基准**：以 v4.5 基线（170 篇论文，超稳激光 78 / OFC 90 / 频标 1 / 时间标尺 1）为准。

---

## 0. TL;DR — 一页纸结论

**用例评估**（用"超稳激光稳定度最高多少？限制是什么？"实测）：

| 维度 | 得分 | 说明 |
|------|------|------|
| 能否答出"最高多少" | 🟢 强 | `stability_record_timeline.md §一` 直出：**2.5×10⁻¹⁷ (mod σ_y, Lee 2026, Si 17K + AlGaAs + 双腔平均)** |
| 能否答出"限制是什么" | 🟢 强 | `_meta/architecture.md §物理限制↔突破路径↔代表论文` 四栏表直出；热噪声 / RAM·PDH / 振动 / 光纤热噪声 / 散粒噪声全覆盖 |
| 边界定义是否清晰 | 🟢 强 | σ_y-first 原则（`scoping_principles.md`）明确锚定专题主线；Allan 变体类型强制标注；长期稳定度 / 线宽 / 灵敏度降为 secondary |
| 逻辑索引跳转效率 | 🟡 中 | 问题 → 答案**首跳过长**：读者要先经 README → USAGE 场景 → synthesis 目录 → 具体页，实际只需 1 跳就能到 `stability_record_timeline.md`。顶层导航**入口过多**（README / INDEX / TOPICS / REVIEW_GUIDE / USAGE / _meta/architecture 都在做类似导航表），信号被稀释 |
| 文档简洁度 | 🟡 中 | 3800 行结构文档 + 8 张 synthesis ≈ 4000 行。`architecture.md §Key Performance Records` 与 `stability_record_timeline.md §一/§三` 高度重复；TODO.md 含大量已完成进度日志 |

**核心结论**：
- **内容层**（YAML + synthesis 的知识本体）**已经能答好上述问题**，σ_y-first 的边界定义显著改善了档位判定和记录榜口径
- **路由层**（README / INDEX / USAGE / REVIEW_GUIDE / architecture 头部 / stability_record_timeline 头部）**存在 5 处重复入口**，是简洁度的主要失血点
- **长尾膨胀**：TODO.md 已完成阶段日志 + `architecture.md` 的 Performance Records 与 synthesis 重复是两个"只要删就立刻轻"的目标

**建议改动体量**：不大，约 5 个选项批后合并 → 预计减少 400–600 行重复 / 冗余内容，不触碰 YAML 与 SCHEMA。

---

## 1. 用例评估详述：两个代表性问题走查

### 1.1 问题 Q1：「超稳激光稳定度最高多少？」

**最短成功路径**（今天实际可走通的）：

```
README.md          → 指向 docs/USAGE.md / REVIEW_GUIDE.md / architecture.md
 (5 个入口都可用)     
   ↓ 任选其一
docs/USAGE.md §场景A → 第一跳：architecture.md 三栏表
                     → 第二跳：breakthrough_paths_matrix.md
                     → 第三跳：具体 paper YAML                 [3 跳]

或更直接：
INDEX.md §按研究问题 → stability_record_timeline.md           [1 跳命中] ✅
                     → §一 Hall of Fame：2.5×10⁻¹⁷ Lee 2026
```

**观察**：
- `INDEX.md` 头部的"我想…→入口"表**已经能 1 跳命中**，但它是**自动生成的**，读者第一眼先被 README 引到了 USAGE 的"三跳"模型。
- `USAGE.md` 场景 B（诊断）的三跳合理；但场景 A（选型）和场景 C（综述）对"最高多少"这种**单点事实查询**显得过长。
- `docs/REVIEW_GUIDE.md` 是给审核者的，不应出现在读者 Q1 的路径上，但它和 USAGE 的"入口表"结构几乎一致。

**结论**：内容到位；**入口路由有 1 跳即可命中，但 README 没把这条最短路径当作默认推荐**。

### 1.2 问题 Q2：「限制是什么？」

**最短成功路径**：

```
stability_record_timeline.md §顶层导航 → _meta/architecture.md §物理限制↔突破路径   [1–2 跳]
                                       或 synthesis/thermal_noise_landscape.md
                                       或 synthesis/breakthrough_paths_matrix.md
```

**观察**：
- 四栏对照表 `物理限制 (pri.*) | 主要突破路径 | 对 σ_y(1 s) 贡献量级 | 代表论文` 非常好用，是专题的"认知地图"。
- 但这张表**同时在 `architecture.md` §物理限制 和 `breakthrough_paths_matrix.md` §A.2** 各出现一次，**格式略不同**（前者按 pri.* 分行、后者按 σ_y 增益量级分行），读者要回答 Q2 时会被"哪张是权威"困扰。
- `scoping_principles.md §1.2 档位判据表` 也间接回答了"什么算限制"，但它的目标是档位判定，不是 Q2 的正面回答。

**结论**：限制维度的内容**覆盖充分甚至过剩**；问题是**同一信息在 architecture / synthesis / scoping_principles 三处各有一版**。

### 1.3 评估小结

| 评估项 | 当前状态 | 需要动的层 |
|--------|---------|-----------|
| 答案是否在库里 | ✅ 在 | — |
| 答案是否**唯一源**（SSoT） | 🟡 σ_y 主线记录有 2 处冗余（architecture §Key Performance Records / stability_record_timeline §一） | 内容层 |
| 问题→答案跳转距离 | 🟡 1 跳可达但默认路由不是最短 | 路由层 |
| 边界定义清晰度（σ_y-first） | ✅ 非常好 | — |

---

## 2. 结构诊断：五个高优先级问题

### 2.1 【路由重复】顶层"我想…→入口"表在 5 处重复出现

**现状**：
| 文件 | "导航表"章节 | 面向对象 |
|------|-------------|---------|
| `README.md` | L5-15「文档分层」表 + L17-21「最短阅读顺序」 | 所有角色 |
| `INDEX.md` | §按研究问题导航（自动生成） | 读者 |
| `TOPICS.md` | §专题列表 + §建设优先级 | 读者/维护者 |
| `docs/USAGE.md` | §三种典型使用场景 + §其他常用入口 | 读者 |
| `docs/REVIEW_GUIDE.md` | §2 专题审核总览 + §8 审核建议 | 审核者 |
| `topics/ultrastable-laser/_meta/architecture.md` 与 `stability_record_timeline.md` | 各含一段"页面索引 / 顶层导航" | 专题读者 |

**问题**：同一个读者在同一次查询中，会在 3–5 个文件里看到**格式各异、但内容大致重叠**的导航表。这是"信号稀释"的主要来源，而非内容不足。

**选项**：

- [ ] **A. 最小化**：只保留 `INDEX.md §按研究问题导航`（自动生成）+ `README.md` 一句话引到它。USAGE / REVIEW_GUIDE / architecture / stability_record_timeline 的导航表全部删除，仅保留"本页内容 + 一行返回 INDEX.md 的链接"。
- [ ] **B. 分角色收口**（推荐）：README 只做**角色→文档**的 1 张表；INDEX.md 自动保留"我想…→入口"；USAGE/REVIEW_GUIDE/architecture 保留**各自角色专用**的导航表，但**严格不再重复**"我想…"通用查询的条目。删掉 stability_record_timeline.md §顶层导航（§一就是答案，不需要内部跳转）。
- [ ] **C. 不动**：保留当前多入口冗余，等读者反馈再调。
- [ ] **改写**：_______________________________

**我的建议**：**B**。它把路由层收敛为三条互不重叠的流线（通用 = INDEX / 读者 = USAGE / 审核 = REVIEW_GUIDE），同时保留专题内的本地导航但清掉和全局重复的条目。**预计删减 70–100 行**。

---

### 2.2 【内容重复】σ_y 记录榜在 3 处各存一版

**现状**：

| 位置 | 章节 | 覆盖 |
|------|------|------|
| `topics/ultrastable-laser/_meta/architecture.md` | §Key Performance Records（主线榜 + 子分支 SOTA + 次要 + 工程） | 压缩版 |
| `topics/ultrastable-laser/synthesis/stability_record_timeline.md` | §一 Hall of Fame + §二 子分支 SOTA + §三 FP 腔里程碑 | 扩展版 |
| `topics/ultrastable-laser/synthesis/breakthrough_paths_matrix.md` | §A.2 σ_y 增益矩阵 | 按路径切片的投影 |

三处数值一致，但**三个口径**（按时间 / 按子分支 / 按路径）。风险：
- 专家更新一处，忘了另外两处
- 读者不确定哪个是 SSoT

**选项**：

- [ ] **A. 以 synthesis 为 SSoT**：`architecture.md §Key Performance Records` 精简为**一个表 + 一行指向 stability_record_timeline.md**；`breakthrough_paths_matrix.md §A.2` 保留但**显式声明"以 timeline 为数值 SSoT，本表是按路径切片的投影"**。
- [ ] **B. 以 architecture.md 为 SSoT**：synthesis 三张表全部瘦身成"看 architecture.md §Key Performance Records 即可"，synthesis 只留"使能技术变化 / 趋势预测 / 开放问题"这类 architecture.md 不装的内容。
- [ ] **C. 不动，加一个 CI 检查**：写脚本比对三处数值一致性，每次 PR 自动检查。

- [ ] **改写**：_______________________________

**我的建议**：**A**。理由：(1) synthesis 是设计来承载跨论文综合视图的，`stability_record_timeline.md` 已经是天然 SSoT；(2) architecture.md 的定位应该是"结构骨架"，榜单数值不是骨架；(3) matrix §A.2 是投影而非副本，保留它但明确声明从属关系即可。**预计删减 30–50 行**。

---

### 2.3 【Synthesis 饱和度】超稳激光 8 个 synthesis 页是否过多？

**现状**：8 张 synthesis（stability_record_timeline / breakthrough_paths_matrix / thermal_noise_landscape / cryogenic_roadmap / fiber_stabilization_landscape / ram_and_pdh_error_budget / spectral_hole_burning_track / vibration_insensitivity_landscape）。

**观察**：
- `stability_record_timeline.md` 和 `breakthrough_paths_matrix.md` **都自称是"顶层导航 / 交叉索引"**——即 2 张顶层，风险是读者不知道先看哪张。
- `spectral_hole_burning_track.md`（124 行）对应的 SHB 分支目前库里只有 2–3 篇 SOTA 论文（Thorpe 2011 等），**页面长度与分支重量不匹配**——它与 `fiber_stabilization_landscape.md`（光纤分支，≥ 8 篇）放在同一级目录显得权重不对。
- `thermal_noise_landscape.md` 与 `cryogenic_roadmap.md` 有一定交集（低温 Si 是热噪声突破路径之一），是否合并？

**选项**（可多选）：

- [ ] **A. 明确"唯一顶层导航页"**：只让 `stability_record_timeline.md` 做顶层导航；把 `breakthrough_paths_matrix.md` 的"交叉索引"自称改为"按限制×路径切片查询表"，不再做导航角色。
- [ ] **B. 把 SHB track 降级**：把 `spectral_hole_burning_track.md` 内容合并到 `stability_record_timeline.md §五 其他频率参考方案`，或迁移到独立的 `branches/` 子目录。
- [ ] **C. 合并 cryogenic_roadmap 到 thermal_noise_landscape**：低温路线是热噪声路径之一，放在一张页上讨论热噪声的全部突破路径。
- [ ] **D. 不合并，只补"冲突说明"**：每张页首明确自己与其他 synthesis 的分工边界。
- [ ] **E. 不动**：维持现状。
- [ ] **改写**：_______________________________

**我的建议**：**A + D**。不做合并（合并会打破既有引用链和 freshness 追踪），但通过"顶层导航唯一化 + 每页首行分工边界声明"把导航混乱解决。SHB 页保留是合理的（分支虽小但物理路线独立，符合专题的"三分支承认"规则）；cryogenic vs thermal_noise 维持拆分（一张讲限制分解、一张讲工程路线图，视角不同）。

---

### 2.4 【TODO 膨胀】TODO.md 含 60%+ 的已完成阶段日志

**现状**：`TODO.md` 145 行，其中 L24-44 的阶段 A1/A2/A3/A4/B/C、L45-83 的超稳激光 P0-P3 **几乎全部已完成**（✅）。真正活跃的 `[ ]` 待办只有十来条。

**问题**：新来者进入 TODO 的第一印象是"大量遗产任务"，实际活跃清单被淹没。

**选项**：

- [ ] **A. 归档**：把阶段 A–C 的完成日志迁移到 `docs/archive/round3_governance_log.md`（或合并到 `ULTRASTABLE_GOVERNANCE_HANDBOOK.md` 的"历史记录"段）；TODO.md 只保留：当前优先级 + 活跃 `[ ]` 待办 + 最近 2–4 周内完成的里程碑。目标长度 < 50 行。
- [ ] **B. 折叠**：在 Markdown 中用 `<details>` 折叠已完成段落。
- [ ] **C. 不动**：历史信息对新手有价值，保留。
- [ ] **改写**：_______________________________

**我的建议**：**A**。`LOG.md` + `ULTRASTABLE_GOVERNANCE_HANDBOOK.md` 已经承担历史记录职责，TODO.md 应是"现在/马上做什么"的快照。**预计 TODO.md 从 145 行缩到 40–50 行**。

---

### 2.5 【CONTRIBUTING 冗余】单篇摄入 Checklist 与 Schema §9.1 部分重复

**现状**：`CONTRIBUTING.md` L13-83 的 Step 1–10 摄入 Checklist，和 SCHEMA.md §9.1 档位规范 + `docs/CONTRIBUTION_TIER_RULES.md` 三处都在讲"如何判定 contribution_type"。

**问题**：规则变动时要在 3 处同步；AI agent 读到的规则是否一致依赖文档维护纪律。

**选项**：

- [ ] **A. 强收敛到 CONTRIBUTION_TIER_RULES.md**：CONTRIBUTING.md 只保留**过程性**内容（Step 1–10 的流程），所有档位判据的**判断细节**都转引 `CONTRIBUTION_TIER_RULES.md`。Step 2 的档位判据表从 CONTRIBUTING 删除，改为 "见 §档位判据"。
- [ ] **B. 不动，加一个脚本**：写个检查脚本验证三处"三档定义"字面一致。
- [ ] **C. 不动**：多处冗余是为了让不同角色看到自己视角的描述。
- [ ] **改写**：_______________________________

**我的建议**：**A**。这和 README 约定的"SCHEMA 是唯一技术真源"一致——让 CONTRIBUTING 只做流程清单，判据细节都在 TIER_RULES。**预计 CONTRIBUTING.md 从 166 行缩到 110–130 行**。

---

## 3. 次级优化项（可选，低优先级）

下列各项不是结构性问题，但可顺手收拾。每项用一行勾选就行：

- [ ] **3.1** `TOPICS.md` 与 `README.md` 专题列表重复 → TOPICS.md 改为只保留"专题间关系图 + 建设优先级"，去掉"专题列表"表（README + INDEX 都已经有）
- [ ] **3.2** `INDEX_principles.md` / `INDEX_metrics.md` / `INDEX.md` / `docs/CURRENT_NODES_REFERENCE.md` 四个自动生成索引是否精简到 3 个？（例如 CURRENT_NODES_REFERENCE 是否可并入 INDEX.md？）
- [ ] **3.3** `docs/ULTRASTABLE_GOVERNANCE_HANDBOOK.md` 专题专属 → 迁到 `topics/ultrastable-laser/_meta/governance_handbook.md`，`docs/` 下只放**跨专题通用**文档
- [ ] **3.4** `topics/ultrastable-laser/_meta/scoping_principles.md` 已是 v2，稳定后是否抽象出一份 `docs/TOPIC_SCOPING_TEMPLATE.md`，供 OFC 等后续专题套用？（TOPICS.md 显示 OFC 是下一轮重点，正合适）
- [ ] **3.5** `stability_record_timeline.md §六 性能趋势预测` 包含外推（2028 / 2030 年的 σ_y 预期）——是否统一标注为 🟡 draft 或迁移到 `reports/`，避免读者误以为是库中验证过的事实？
- [ ] **3.6** `_meta/architecture.md` L52 到 L86 的三层指标表（主线 / 次要 / 工程）是否补一张"指标 × 角色"的快查索引（已存在 `INDEX_metrics.md` 但未强制 role 分组）
- [ ] **3.7** `breakthrough_paths_matrix.md` 已自称"draft"，但落地数据已充分，建议确认并去掉 🟡 draft 标记（和 P3 专家签字一并处理）

---

## 4. 后续建议：三个递进方向

> 这一节不是"待办清单"，而是给你决策用的**方向选择**。每个方向对应不同战略侧重。

### 4.1 方向 X · 路由层收口（≈ 1 周内可完成）

即上面 §2.1 + §2.2 + §2.4。三个改动加起来体量小、风险低、读者受益立竿见影。**如果只选一个方向，推荐这个**。

预期结果：
- 顶层导航入口从 5–6 处收敛到 3 条清晰分支
- σ_y 记录榜 SSoT 明确
- TODO.md 从 145 行降到 50 行

### 4.2 方向 Y · 专题方法论迁移到 OFC（≈ 2–4 周）

`TODO.md` 已点名：下一轮重点是启动光学频率梳 synthesis。超稳激光专题的整治经验（σ_y-first / scoping_principles / 8 张 synthesis）已经沉淀为 `ULTRASTABLE_GOVERNANCE_HANDBOOK.md`。

该方向的关键动作：
1. 决定 OFC 的**多主线指标体系**（库里已识别 9 条子域主线：A1-Rep, A1-Noise, A2-DKS, B-FreqSyn, B-DCS, B-Spec, B-MIR…）
2. 每条子域主线选一张代表 synthesis 页作为首批（建议：双梳光谱 DCS + 微梳 DKS + 频率综合 FreqSyn，3 张启动）
3. 把 §3.4 的"专题 scoping 模板"抽象出来，OFC 第一个使用

**风险**：OFC 不适合单主线锚定，`scoping_principles` 的套用方式需要专家决策（USL 是 σ_y-first 这种 1D 模型；OFC 可能需要 2D 甚至多维的 role 分类）。

### 4.3 方向 Z · 建立"问题 → 答案"的自动化评测（≈ 1–2 周）

把本文件 §1 的评估方法固化：

1. 在 `docs/` 或 `reports/` 建立 `kb_evaluation_queries.md`——列举 10–20 个代表性研究问题（超稳激光稳定度最高多少 / 当前瓶颈 / 设计 5×10⁻¹⁶ 系统 / 诊断振动主导 / ...）
2. 每个问题标注：**预期答案所在文件**（期望 1 跳达）+ **实际验证时间**
3. 每次 schema / 路由层改动后，重跑这份评测，防止回归

**好处**：以后"结构是不是变好了"不再靠感觉，有可量化口径。**这也是你提问里"问题评估边界定义和逻辑索引的效果"的天然固化点**。

---

## 5. 决策汇总表（专家填写区）

> 批完后我按这份批结果分 PR 执行。每个选项默认不选。

| # | 优化项 | 选择 (A/B/C/D/E) | 备注 / 改写 |
|---|--------|------------------|-------------|
| 2.1 | 路由重复 | _____ | |
| 2.2 | σ_y 记录榜 SSoT | _____ | |
| 2.3 | Synthesis 饱和度 | _____ | |
| 2.4 | TODO 膨胀 | _____ | |
| 2.5 | CONTRIBUTING 冗余 | _____ | |
| 3.1 | TOPICS.md 专题列表 | 收/不收 | |
| 3.2 | 索引文件数 | 收/不收 | |
| 3.3 | GOVERNANCE_HANDBOOK 迁移 | 收/不收 | |
| 3.4 | TOPIC_SCOPING_TEMPLATE | 收/不收 | |
| 3.5 | 趋势预测标注 | 收/不收 | |
| 3.6 | 指标×角色快查 | 收/不收 | |
| 3.7 | breakthrough_paths_matrix 去 draft | 收/不收 | |
| 4.x | 后续方向 | X / Y / Z / 组合 | |

**签字**：____________________  **日期**：__________

---

## 6. 本文件的定位

- **不是** SCHEMA、规范、索引，也**不是**长期维护文档
- 只服务"专家一次性批准一轮结构优化"的场景
- 批准动作完成后，本文件归档到 `docs/archive/` 或直接删除
