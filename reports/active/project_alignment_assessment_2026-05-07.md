# sci-logic-kb 项目整合与对齐评估（2026-05-07）

> **背景**：用户要求"整体评估项目，整合和简化项目内容，对齐所有描述文档"。
> **范围**：根目录入口文档 + `docs/` + `.github/copilot-instructions.md` + `reports/` 分层 +
> 各 INDEX 计数一致性。**不**评估单篇论文 YAML 质量与节点结构（已有专项报告）。
> **方法**：对照阅读所有路由级文档、抽样关键交叉引用、对比自动索引与手工统计。
> **执行原则**：本报告只产出诊断与建议，**不**直接重写 SCHEMA / CONTRIBUTING / CLAUDE 等
> 长期入口（这类文档的修改应由专家拍板，按 CLAUDE.md 「人类必须拍板的事项」 §Schema 演进条款）。

---

## 0 · TL;DR

**总体判断**：项目骨架与运维基础设施（YAML 主数据 + 自动 INDEX + lint/stats/health + reports 三层 + GitHub Pages）已成熟，
**质量不在数据层，而在描述层**。由于 SCHEMA 在 2026-05 升级到 v5.0（引入"S-ARK 三层原子推理架构"）但**周边路由文档未同步**，
当前所有入口文档（`README.md` / `CLAUDE.md` / `CONTRIBUTING.md` / `TOPICS.md` / `docs/WORKFLOW.md` / `docs/USAGE.md` / `.github/copilot-instructions.md`）
都还停留在 v4.4 / v4.5 心智模型下。这是**唯一一处真正影响新人和 AI 上手准确性的系统性问题**。

**最高优先级建议**：用一个最小补丁版本（建议 v5.1）把 SCHEMA.md 补全（恢复 v4.5 中已被裁掉、但仍被周边文档引用的章节），
然后再批量对齐周边文档的版本号、章节编号与字段名。在 SCHEMA 补全之前，**不要**在周边文档里手工写 v5.0 适配，
否则会再度漂移。

---

## 1 · 现状速写

### 1.1 数据层（健康）
- 6 个专题，自动索引（`INDEX.md`，2026-05-04 重建）：**399 papers / 1464 nodes / 1547 relations**。
- `lint.py --summary` 0 errors / 31 warnings；`health.py` 7/7；`synthesis` 6/6（每专题至少 1 页）。
- `topics/<topic>/papers/*.yaml` 是唯一主数据源，`INDEX*.md` / `docs/CURRENT_NODES_REFERENCE.md` 由脚本生成。

### 1.2 工程层（健康）
- `scripts/`：lint / stats / build_index / health / freshness 都齐备且通过 PR 必过门
  （`.github/workflows/kb-lint-stats.yml`）。
- `reports/` 已经按 active / archive / generated 三层落地（TODO §P0–P1 全部 ✅）。
- 根目录文件清单已收敛到「长期入口」（CONTRIBUTING §根目录约定）。
- GitHub Pages + 交互式图谱已上线（`.github/workflows/pages.yml` + `.nojekyll` + README badge）。

### 1.3 描述层（**失谐**）
这是本次评估的核心问题区。下一节展开。

---

## 2 · 漂移与不一致清单（按严重度排序）

### 2.1 🔴 严重 · SCHEMA v5.0 与周边文档版本不一致

`SCHEMA.md` 现版本是 **v5.0（S-ARK 三层原子架构）**，但所有路由文档仍引用旧版本：

| 文件 | 引用的版本 | 当前 SCHEMA 实际 |
|---|---|---|
| `.github/copilot-instructions.md:3` | "当前版本 v4.5" | v5.0 |
| `CLAUDE.md:41` | "贡献类型判定（v4.4）" | v5.0 §未明确写贡献档位 |
| `CLAUDE.md:129` | "SCHEMA.md（第十节定义运维操作）" | **SCHEMA 只有 5 节，无第十节** |
| `CONTRIBUTING.md:24` | "v4.4 三档规范" | 同上 |
| `CONTRIBUTING.md:64` | YAML 文件头要求写 `# Schema版本：v4.5` | v5.0 |
| `CONTRIBUTING.md:157` | "v4.5+" 根目录约定 | v5.0 |
| `docs/WORKFLOW.md:101` | YAML 模板示例标 v4.5 | v5.0 |
| `docs/USAGE.md:88` | "Synthesis 页新鲜度机制（v4.5+）" | v5.0 |
| `docs/FIX_PLAN.md:32` | 已自我承认"CLAUDE.md 还引用旧版规则" | — |

### 2.2 🔴 严重 · SCHEMA v5.0 比 v4.5 缩水，丢失关键规范

`SCHEMA.md` v5.0 只有 118 行、5 节。它**改写了哲学层**（三层架构 + 12/14 谓词），但以下被周边文档大量引用的内容**已不在 SCHEMA 里**：

- `meta.contribution_type` 三档（breakthrough / evidence / framework）的判据 → 仍只在 `CONTRIBUTING.md` §Step 2 与 `docs/CONTRIBUTION_TIER_RULES.md` 中
- `breakthrough_paths` / `historical_landmarks` / `selected_milestones` / `contested_claims` / `open_questions` 字段 → CONTRIBUTING 在用，SCHEMA 不再定义
- 节点 ID 命名规则（`ent.* / pri.* / meth.* / met.* / rel.*`）→ 只在 CLAUDE.md §节点 ID 命名规范 中描述
- 跨专题节点提升与 `topics/shared/` 路径 → CONTRIBUTING / TOPICS 提及，SCHEMA 不写
- 「专题体系与演进」章节 → `TOPICS.md:3` 明文写"完整规范已合并至 SCHEMA 的『专题体系与演进』章节"，**该章节实际不存在**
- v5.0 §1 提出的物理路径 `/data/sci-logic-kb/data/evidence/`、`data/logic/`、`data/consensus/` → **仓库实际目录不存在**，主数据仍在 `topics/<topic>/papers/`

→ SCHEMA 现在与周边文档**互不自洽**，且与仓库实际目录结构**也不自洽**。

### 2.3 🟠 高 · 谓词集不一致

- `SCHEMA.md` §3.1 表头写"12 种标准化关系"，但表中实际列了 14 行。
- `docs/INGESTION_PROTOCOL.md:26` 举例使用 `RESOLVED-BY` 谓词 → 这一谓词**不在** SCHEMA v5.0 的标准谓词表中。
- `docs/CONTRIBUTION_TIER_RULES.md:3` 称自己是"v4.4 schema 机制落地的配套规范" → 与 SCHEMA v5.0 不同步。

### 2.4 🟠 高 · 专题列表不一致

| 来源 | 列出的专题 |
|---|---|
| `README.md:85-91` | 超稳激光、光学频率梳、**离子/原子光钟**、**微波原子钟**、时间频率传递、**精密测量应用** |
| `TOPICS.md` & 文件系统实际 | ultrastable-laser、optical-frequency-combs、**frequency-standards**（光+微波合并）、time-frequency-transfer、**shared**、**timescales** |

README 的专题清单**完全错误**——3 个名字错的、缺 2 个实际存在的。新读者第一站就会被误导。

### 2.5 🟡 中 · 文档冗余、重复与归属不当

`docs/` 当前 12 个文件，混合了三类东西：

| 类型 | 文件 | 该归到哪里 |
|---|---|---|
| **稳定路由（保留）** | `WORKFLOW.md` · `USAGE.md` · `REVIEW_GUIDE.md` · `CLAIM_EVIDENCE_STANDARD.md` · `CONTRIBUTION_TIER_RULES.md` · `INGESTION_PROTOCOL.md` · `CURRENT_NODES_REFERENCE.md` | 保留在 `docs/` |
| **一次性规划（迁出）** | `FIX_PLAN.md` · `DEPLOYMENT_PLAN.md` · `DIFY_INGEST_PLAN.md` · `DIFY_INGEST_WORKFLOW.md` | 迁入 `reports/active/`（仍在驱动）或 `reports/archive/`（已落地） |
| **专题专属（迁出）** | `ULTRASTABLE_GOVERNANCE_HANDBOOK.md` | 迁入 `topics/ultrastable-laser/_meta/governance_handbook.md` |

理由：`docs/` 应只承载"全库通用、长期有效"的指引；专题专属手册按 SCHEMA 与 TOPICS 的目录约定属于专题 `_meta/`；
一次性规划文档按 CONTRIBUTING §根目录约定本就**不**该出现在 docs/，而应进 reports/。

#### 重复与可合并

- `INGESTION_PROTOCOL.md` 与 `CONTRIBUTING.md` 都描述论文摄入 pipeline，前者英文 + Stage 模型，后者中文 + 10-step checklist。**重叠 70%**。建议把 `INGESTION_PROTOCOL.md` 缩为"高层 4-stage 概念图"，详细 checklist 收敛到 CONTRIBUTING；或反之统一到一份。
- `CLAUDE.md §单篇论文处理流程`（Step 1–7） vs `CONTRIBUTING.md §Step 1–10` vs `docs/WORKFLOW.md §一` vs `docs/INGESTION_PROTOCOL.md §2`：**4 份描述同一流程**，编号还不一致（7/10/4 stage）。建议 CONTRIBUTING 是唯一详细版，其他三份只链接过去。
- `DIFY_INGEST_PLAN.md` 与 `DIFY_INGEST_WORKFLOW.md` 内容高度重叠（都讲 Dify 接入），可以合并成一份并迁入 `reports/active/dify_integration/`。

### 2.6 🟡 中 · 计数与状态漂移

- `TODO.md:67-69`（2026-05-03）：335 done + 191 pending = 526 papers total。
- `INDEX.md`（2026-05-04 自动生成）：399 papers。
- `reports/active/knowledge_base_assessment_report.md:6-19`：141 papers / 859 nodes（旧快照，未标过期）。
- `paper-inkb.md`：266 行论文条目。
- `LOG.md`：844 行历史记录混叠多个版本。

此处 `INDEX.md` 是脚本权威，其他都是手工/历史快照。建议：
- 给 `reports/active/knowledge_base_assessment_report.md` 加显式过期标记或归档。
- `paper-inkb.md` 与 `PROCESSED_PAPERS.md` 的去重职责需在头注里互相点名（目前 PROCESSED_PAPERS 已点名 paper-inkb，反向未点）。
- `TODO.md` 顶部「暂停恢复点」是 2026-05-03 快照，应在 SCHEMA / 入库批次更新后同步刷新。

### 2.7 🟢 低 · 编码细节

- `SCHEMA.md:23` "（ la Decomposition Graph）" → 应为 "（à la Decomposition Graph）"，Unicode 损坏。
- `SCHEMA.md:62` "12 种" 与表中 14 行不一致（同 §2.3）。
- `CLAUDE.md` 文件名约定（`ent.{描述词}_{后缀}` 等）应在 SCHEMA 中固化，而不是只在 CLAUDE 中。
- `LOG.md` 已 844 行，可以按版本切片归档（v4 之前的迁入 `reports/archive/log_v4_and_earlier.md`），主 LOG 只留 v5+ 之后的演进。

---

## 3 · 整合与对齐方案（建议执行顺序）

### Phase 0 · 真源补全（专家亲自做 · 1–2 天）

> 必须先做 SCHEMA 补全，再做周边对齐。否则任何对齐工作都是把错按到错上。

1. **SCHEMA.md → v5.1**：在保留 v5.0 三层架构哲学的前提下，补回以下章节：
   - 节点 ID 命名规范（从 CLAUDE.md 迁入 / 复述）
   - `meta.contribution_type` 三档定义（从 CONTRIBUTING.md / TIER_RULES.md 提炼）
   - 字段词典：`breakthrough_paths` / `historical_landmarks` / `selected_milestones` / `contested_claims` / `open_questions` / `verification_status` / `demonstrated_value`（CLAIM_EVIDENCE_STANDARD 中已有，复述要点即可）
   - 「专题体系与演进」章节（TOPICS.md:3 已许诺存在）
   - 决定 v5.0 §1 的 `/data/sci-logic-kb/data/{evidence,logic,consensus}/` 物理路径**到底是不是要落地**：
     - 若要落地 → 写迁移计划（任务 P0），并在 SCHEMA 中说明过渡期 `topics/<topic>/papers/` 仍是兼容路径
     - 若不落地 → 改写 v5.0 §1 把"三层"定义为**逻辑分层**，物理路径仍是 `topics/<topic>/papers/*.yaml` 内部的 evidence / logic / consensus 块
   - 修订谓词表：表头数量与表行一致；并把 `INGESTION_PROTOCOL.md` 用过的 `RESOLVED-BY` 要么纳入正式表，要么在该 doc 里换成 `BOUNDED-BY` 反向。

2. **TOPICS.md** 要么把那句"完整规范已合并至 SCHEMA 的『专题体系与演进』章节"改写成"详见 SCHEMA §X"（X 须真实存在），要么把章节真的写进 SCHEMA。

### Phase 1 · 周边路由对齐（AI 可代劳 · 1 天）

SCHEMA v5.1 落地后，按下表批量更新（这是机械性替换，AI 可生成 PR）：

| 文件 | 改动 |
|---|---|
| `.github/copilot-instructions.md:3` | "v4.5" → "v5.1" |
| `CLAUDE.md` 全文 | 删去与 SCHEMA 重复的 ID 命名表（让 SCHEMA 唯一权威）；版本号 v4.4 → v5.1；删 "第十节" 这种点名引用，改成 "§运维操作"，由章节标题去匹配 |
| `CONTRIBUTING.md` | 文件头模板要求 `# Schema版本：v5.1`；版本提示 v4.4/v4.5 → v5.1 |
| `docs/WORKFLOW.md` | 同上；并把详细流程缩为 "见 CONTRIBUTING.md §Step 1–10"，避免 4-份重复维护 |
| `docs/INGESTION_PROTOCOL.md` | Stage 模型保留但改为引用 SCHEMA / CONTRIBUTING；移除非标准谓词；标注语言（建议保留为英文版，作为对外速览） |
| `docs/USAGE.md` | "v4.5+" → "v5.1+" |
| `docs/CONTRIBUTION_TIER_RULES.md` | "v4.4 schema 配套" → "v5.1 schema 配套" |
| `README.md:85-91` | 专题列表整段重写，与 `TOPICS.md` 当前 6 个一致；建议直接 transclude 自 TOPICS（写成"详见 TOPICS.md"，不再列名字）|

### Phase 2 · 文档归位整理（AI 可代劳 · 0.5 天）

| 操作 | 源 | 目标 |
|---|---|---|
| 迁移 | `docs/FIX_PLAN.md` | `reports/archive/fix_plan_2026-04.md`（计划已基本落地，归档） |
| 迁移 | `docs/DEPLOYMENT_PLAN.md` | `reports/active/deployment_plan.md`（仍驱动 P2 决策） |
| 合并 + 迁移 | `docs/DIFY_INGEST_PLAN.md` + `docs/DIFY_INGEST_WORKFLOW.md` | `reports/active/dify_integration/{plan,workflow}.md` |
| 迁移 | `docs/ULTRASTABLE_GOVERNANCE_HANDBOOK.md` | `topics/ultrastable-laser/_meta/governance_handbook.md` |
| 留 | `docs/{WORKFLOW, USAGE, REVIEW_GUIDE, CLAIM_EVIDENCE_STANDARD, CONTRIBUTION_TIER_RULES, INGESTION_PROTOCOL, CURRENT_NODES_REFERENCE}.md` | 不动 |

每次迁移都在 `reports/README.md` 的索引里登记，旧位置写一行 stub `> 已迁移至 …` 保留 30 天后删除。

### Phase 3 · 漂移防御（AI 可代劳 · 0.5 天）

加一个轻量"文档体检"脚本（不要纳入 PR 必过门，只做周报提醒）：

- `scripts/doc_health.py`（新增，~80 行）：
  - 抽取所有 markdown 中形如 `v\d+\.\d+` 的版本字符串，与 `SCHEMA.md` 头部版本对比，列出不一致项
  - 检查 `README.md` 专题列表与 `topics/` 子目录是否一致
  - 检查 `docs/` 里出现的字段名（如 `breakthrough_paths`）是否在 SCHEMA 中定义
  - 输出到 `reports/generated/doc_health_<date>.md`

这样以后 SCHEMA 一升级，doc_health 立刻报警，避免又一次 v5.0 漂移半年没人发现。

---

## 4 · 简化建议（不属于上述对齐，但顺便提）

1. **SKIPPED.md（2 行）** —— 内容几乎为空，可以删除或合并到 PROCESSED_PAPERS.md 末尾。
2. **TODO.md** 多版本叠加（2026-05-03 快照 + 2026-04-24 计划）已经形成"考古地层"。建议保留 P0/P1/P2 主清单 + 当前快照，把 2026-04-24 那段 P0–P1 已 ✅ 完成的内容剪到 `reports/archive/todo_2026-04.md`。
3. **`agents/sci-logic-kb-engineer.agent.md`** —— 一份独立 agent 描述，未在任何路由文档中提及。要么并入 CLAUDE.md，要么在 README 加一句"AI agent 描述见 agents/"。
4. **`paper-inkb.md`（266 行）** 与 **`PROCESSED_PAPERS.md`（326 行）** 的职责切分（前者快查，后者详表）已经清晰，但建议每月由 `build_index.py` 顺手刷一次（目前是手工维护，未来必漂）。

---

## 5 · 给"专家"的最简执行清单

> 全部完成后，描述层与数据层重新自洽。预计专家 3 天 + AI 1 天可完工。

- [ ] **专家 1 ·** 决定 SCHEMA v5.0 §1 三层物理路径是真要落地还是改为逻辑分层
- [ ] **专家 2 ·** 把 SCHEMA 升到 v5.1，补回§2 列出的所有缺失章节；同步 TOPICS.md
- [ ] **AI ·** 提一个 PR：按 §3 Phase 1 表格批量替换版本号 + ID 规范引用
- [ ] **AI ·** 提第二个 PR：按 §3 Phase 2 表格做文件迁移 + reports/README.md 同步
- [ ] **AI ·** 提第三个 PR：写 `scripts/doc_health.py`（§3 Phase 3）
- [ ] **专家 3 ·** 修 README.md §专题列表（最快 5 分钟，但影响所有新读者）

---

## 6 · 给"AI agent"的副本（Copilot / Claude Code 阅读优先级）

如果你（AI）正在新会话里准备摄入论文，**在 SCHEMA v5.1 发布之前**，请按以下优先级解读冲突：

1. `SCHEMA.md` 中**仍存在**的规则 → 服从（如三层架构、谓词表）
2. `SCHEMA.md` 中**已不存在**但 `CONTRIBUTING.md` / `CLAIM_EVIDENCE_STANDARD.md` / `CONTRIBUTION_TIER_RULES.md` 中存在的规则
   → 按这些次级文档执行（如 `contribution_type`、字段集），并在 PR 描述里**显式说明**该规则当前未在 SCHEMA 中定义
3. README 的专题列表**不可信**，请以 `TOPICS.md` 与 `topics/` 目录为准
4. CLAUDE.md "SCHEMA §第十节" 是死链接，请忽略
5. YAML 文件头按 CONTRIBUTING.md 当前要求写 `# Schema版本：v4.5`，**直到** SCHEMA v5.1 发布后再切到 `v5.1`

---

*报告作者：Copilot 任务代理*
*日期：2026-05-07*
*下一次复盘建议：SCHEMA v5.1 发布并 §3 三个 PR 落地后归档至 `reports/archive/`*
