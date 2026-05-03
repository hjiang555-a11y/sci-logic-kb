## 暂停恢复点：sci-logic-kb 下一步建设讨论

> 记录时间：2026-05-03。当前状态：ingestion 追踪修复 + 论文筛选完成，191 篇待入库已分类。Health 7/7，Synthesis 6/6。
>
> **2026-05-03 会话完成**: ingestion_status.json 全面修复 + 191 篇论文专题筛选。
> - ingestion_status: 505 全 pending 虚假状态 → 612 条精准分类 (335 done / 191 topic-pending / 46 needs_review / 27 needs_zotero_db / 8 out_of_scope)
> - 四轮匹配: zotero_key 提取 + DOI/CrossRef API + arXiv API + PDF 内容批量提取 (pdfplumber)
> - synthesis 6/6 (补 timescales + shared)
> - health 7/7, lint 0 errors
> - 长期约定: 沿用 CLAUDE.md Step 1-7，不引入新方法，每次入库后更新 ingestion_status.json

### 当前判断

论文追踪基础设施已就绪。下一阶段：**逐篇摄入 191 篇待入库论文**，按 CLAUDE.md Step 1-7 流程执行。不需要新工具或新方法。

### 恢复方向

**E. 论文逐篇入库 (191 篇)** — 🔴 主要任务
按专题优先级（小专题优先，快速收口）:
1. `shared` (3 篇) — 数学基础，快速收口
2. `timescales` (7 篇) — 时间标尺
3. `time-frequency-transfer` (23 篇)
4. `ultrastable-laser` (26 篇)
5. `frequency-standards` (64 篇)
6. `optical-frequency-combs` (68 篇)

每篇流程: CLAUDE.md Step 1-7（读PDF→提取YAML→运维更新→commit）
质量门: commit 前 `lint.py` 0 error；入库后更新 `ingestion_status.json` 对应 key 为 done

**F. needs_review 清理 (46 篇)** — 🟡 PDF 内容不足以自动分类，需人工逐篇读 PDF 判断
**G. needs_zotero_db (27 篇)** — 🟡 纯数字 Zotero 存储键，连接 Zotero 后可解析

### 已完成方向

A. 超稳激光 / metric chains 样板区 — ✅ 2026-05-02
B. 光频梳 topic 样板区 — ✅ 2026-05-02
C. 全库健康指标与质量检查脚本 — ✅ 2026-05-02
D. 知识 schema / claim-evidence 标准 — ✅ 2026-05-02
E. ingestion 追踪修复 + 论文筛选 — ✅ 2026-05-03

---

# TODO — repository alignment, filesystem simplification, and usage/deployment plan

> 更新日期：2026-04-24  
> 目的：基于当前仓库快照，记录“现状 → 目标态”的差距、降低文件系统复杂度的整理方向、知识库部署/使用方式，以及下一步优先动作。

---

## 1. 当前状态快照（审查结论）

### 1.1 仓库骨架
- 当前主数据仍然清晰：`topics/*/papers/*.yaml` 是知识源，`SCHEMA.md` 是唯一 Schema 真源。
- 自动索引链已经存在且有效：`INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` / `docs/CURRENT_NODES_REFERENCE.md` / `topics/*/INDEX.md`。
- 根目录目前直接暴露的文件类型过多：路由文档、运行记录、同步报告、历史遗留文件并存，阅读入口成本偏高。

### 1.2 文件系统复杂度热点
- 根目录存在多份一次性同步报告：`SYNC_REPORT_*` / `SECOND_*` / `THIRD_*`，应退出主入口层。
- `reports/` 下同时混放：
  - 长期有效的诊断报告（如 `chain_gap_*` / `orphans_*`）
  - 一次性迁移材料 / backup / JSON 中间产物
  - Zotero/Obsidian 对接草案
- 手工维护文档中的统计数字存在漂移风险；当前自动索引与部分手工文档的计数已经不完全一致。

### 1.3 当前知识库运行状态
- 自动统计（2026-05-03，`scripts/health.py`）：
  - 335 papers（done，有 YAML）
  - 191 papers（pending，PDF 已确认专题，待入库）
  - 1232 nodes / 1382 relations / 6 topics
- Health: 7/7 ✅（synthesis 6/6，chain_closure 70.2%，evidence_coverage 99.0%）
- `lint.py --summary`：**0 errors / 31 warnings**。全库一致性已达到可维护基线。
- `ingestion_status.json`：612 条分类追踪

---

## 2. 目标态

希望仓库最终达到以下状态：

1. **根目录只保留稳定入口**
   - `README.md`
   - `SCHEMA.md`
   - `CONTRIBUTING.md`
   - `TOPICS.md`
   - `TODO.md`
   - 自动生成的 `INDEX*.md`
   - 运维文件（`LOG.md` / `PROCESSED_PAPERS.md` / `paper-inkb.md`）

2. **一次性材料退出根目录**
   - 所有 sync report / backup / 临时分析文件统一进入 `reports/archive/`

3. **报告区分层**
   - `reports/active/`：仍会驱动后续整治的报告
   - `reports/archive/`：历史过程材料、迁移记录、backup、一次性 JSON
   - `reports/README.md`：报告索引页，说明每个报告“是否仍有效”

4. **统计信息尽量索引化、少手填**
   - 高频变化的计数优先由脚本输出
   - 手工文档尽量写“状态/阶段”，少写易过期绝对数字

5. **使用路径按角色固定**
   - 读者：`README.md` → `docs/USAGE.md` → `INDEX*.md` / `topics/*/synthesis/`
   - 审核者：`README.md` → `docs/REVIEW_GUIDE.md` → `_meta/architecture.md`
   - 建设者：`CONTRIBUTING.md` → `SCHEMA.md` → `scripts/*.py`

---

## 3. 现状与目标的主要差距

| 维度 | 当前状况 | 目标状况 | 差距判断 |
|---|---|---|---|
| 根目录可读性 | 稳定入口与历史一次性文件混放 | 根目录只保留长期入口 | **差距大** |
| 报告管理 | `reports/` 内容杂糅，缺少总索引 | active/archive 分层 + 索引 | **差距大** |
| 统计一致性 | 自动索引与部分手工文档计数可能漂移 | 计数尽量自动生成 | **差距中等** |
| 用户入口 | 主入口清晰，但“部署/使用模式”未单列说明 | GitHub 阅读 / 本地维护 / 静态浏览三种模式固定 | **差距中等** |
| 知识闭环 | papers/index 已成型，synthesis 覆盖不足 | 每个成熟专题至少有核心 synthesis | **差距大** |
| 质量收口 | lint 仍有较多历史问题 | 错误逐步归零，warnings 不倒退 | **差距大** |

---

## 4. 文件对齐与复杂度降低策略

### P0：先做“路由收口”，不要先做“大搬家”
- 先补齐 `TODO.md`、`reports/README.md` 这类**索引入口**
- 先让“人知道去哪里看”，再移动历史文件
- 所有移动都应是**语义不变的整理**，不要与 Schema/YAML 结构改造耦合

### P1：把根目录中非入口文件迁出
- 候选迁出对象：
  - `SYNC_REPORT_OBSIDIAN_UPDATE.md`
  - `SECOND_SYNC_REPORT_OBSIDIAN_UPDATE.md`
  - `THIRD_SYNC_REPORT_OBSIDIAN_UPDATE.md`
  - `SYNC_REPORT_POST_PULL_20260421_220032.md`
- 建议迁入：`reports/archive/obsidian-sync/`

### P1：把 `reports/` 再分层
- 建议长期保留为 active 的报告：
  - `chain_gap_ultrastable*.md`
  - `orphans_ultrastable*.md`
  - `contribution_tier_draft_ultrastable.md`
  - 仍驱动整治工作的 assessment / candidate 类报告
- 建议归档的内容：
  - `*.backup`
  - 一次性 migration / restructuring / sync 过程文件
  - 不再驱动决策的 JSON 中间产物

### P2：减少“手填统计”
- `TOPICS.md`、`PROCESSED_PAPERS.md`、部分综述性说明中，避免重复写经常变化的论文总数
- 若必须保留数字，应明确“截至日期”
- 更推荐写“已入库 / 成长 / 初建 / 维护中”等阶段性状态，把精确数字交给自动索引

---

## 5. 知识库部署与使用方式规划

### 5.1 默认部署方式：GitHub 原生浏览
- 适合当前阶段，成本最低
- 依赖：
  - 根目录路由文档
  - 自动生成的 `INDEX*.md`
  - `docs/USAGE.md` / `docs/REVIEW_GUIDE.md`
- 目标：先把“在 GitHub 网页里可读可导航”做到稳定

### 5.2 第二阶段：静态只读发布
- 建议用 GitHub Pages 托管：
  - `docs/graph/`
  - 自动索引页面
  - 报告索引页
- 作用：
  - 给非维护者一个更轻量的浏览入口
  - 降低直接进入仓库树的理解成本

### 5.3 第三阶段：维护者本地工作流
- 本地维护继续以脚本为核心：
  - `python scripts/lint.py --summary`
  - `python scripts/stats.py`
  - `python scripts/build_index.py`
- 若后续要增强部署，不应改变 YAML 为真源这一原则，只在“呈现层”加壳

---

## 6. 下一步建议（按优先级）

- [x] **P0** 新增 `reports/README.md`，按 active / archive / generated 三类建立报告索引 ✅ 已完成
- [x] **P0** 清点所有根目录一次性文件，列出”保留 / 迁移 / 删除”清单 ✅ 已完成（根目录已干净，15 个文件均为长期入口）
- [x] **P0** 统一约定：根目录只保留稳定入口，不再新增一次性报告 ✅ 已确立
- [x] **P1** 将根目录 `SYNC_REPORT*` 文件迁入 `reports/archive/obsidian-sync/` ✅ 已完成
- [x] **P1** 将 `reports/*.backup` 与一次性 JSON 迁入 `reports/archive/` ✅ 已完成
- [x] **P1** 对 `TOPICS.md`、`PROCESSED_PAPERS.md` 做一次”去高频数字化”整理，降低后续漂移 ✅ 已完成 (2026-05-02)
- [x] **P1** 针对 `optical-frequency-combs` 优先补首批 synthesis 页面，解决 1/6 topics coverage 的主要缺口 ✅ 已完成（B-1: metric_chains, B-2: 3 synthesis 页）
- [x] **P1** 选择一个 lint 大类（建议从 `duplicate-def` 或 `dangling-ref` 开始）做专项收口 ✅ 已完成 (2026-05-02): duplicate-def 4→0, invalid-predicate 4→0; lint errors 8→0
- [x] **P2** 评估 GitHub Pages 只读发布方案，把 `docs/graph/` 与索引页面作为第一批可视化入口 ✅ 已完成 (2026-05-02): `.nojekyll` + `.github/workflows/pages.yml` + README badge; 需管理员在 GitHub Settings → Pages 选 Actions 源即可激活
- [ ] **P2** 若后续读者增多，再考虑增加”面向查询者”的单页总入口，而不是继续增加根目录文档

---

## 7. 本次审查后的执行原则

- 不手工编辑自动生成索引，统一通过 `python scripts/build_index.py`
- 不在根目录继续堆积一次性过程文件
- 任何“新入口”都应先回答：它是长期入口，还是应当进入 `reports/archive/`
- 任何“统计数字”都应先回答：它是否值得手工维护，还是应该交给脚本/索引

