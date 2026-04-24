# Contributing to sci-logic-kb

> 这份文档规定**如何向知识库贡献内容**——单篇论文摄入的标准流程、节点设计判据、质量门。
>
> 补充关系：
> - 规范（真源）：[SCHEMA.md](SCHEMA.md)
> - 审核入口（专家视角）：[docs/REVIEW_GUIDE.md](docs/REVIEW_GUIDE.md)
> - 使用指南（读者视角）：[docs/USAGE.md](docs/USAGE.md)
> - AI 协作行为：[CLAUDE.md](CLAUDE.md) · [.github/copilot-instructions.md](.github/copilot-instructions.md)

---

## 快速上手：单篇论文摄入 Checklist

用作 PR 模板与 AI agent 的共享 checklist。勾选完成项以进入合并流程。

### Step 1 · 准备
- [ ] 从 `QUEUE.md`（若存在）或 issue 中选定目标论文
- [ ] 记录 `ZOTERO_KEY`、`DOI`、`first_author`、`year`
- [ ] 确认论文的专题归属（超稳激光 / 光学频率梳 / …；若跨专题标注 shared）

### Step 2 · 阅读与提取
- [ ] 阅读摘要、引言、方法、结果、讨论（至少这 5 节）
- [ ] 识别该论文的**核心贡献类型**（写入 `meta.contribution_type`，v4.4 三档规范，详见 [SCHEMA.md §9.1](SCHEMA.md)）：
  - `breakthrough`：打破指标记录 / 提出新原理 / 证伪旧论断
  - `evidence`：在已有节点上提供新数据点、新条件验证、工程复现（**大多数论文属此档**）
  - `framework`：综述 / 路线图 / 教科书章节
- [ ] 若不确定在 `breakthrough` 还是 `evidence`：默认 `evidence`，由专家在审核时决定是否升档
- [ ] **超稳激光专题专属**（若论文属该专题）：
  - 定位论文的 σ_y(τ=1 s) 在主线时间线上的位置（刷新全局 / 刷新子分支 / 平齐 / 落后）——档位判定的第一依据
  - 若论文报告了 Allan 偏差，**必须**在 `demonstrated_value` 中标注 Allan 变体类型（ADEV / MDEV / OADEV / Hadamard）
  - 若论文只报告线宽或频噪 PSD：优先从 PSD 换算 σ_y 并在 note 标注换算方法；只有线宽则在 note 中声明 `primary-metric missing: linewidth only`，此情况**不能**升 breakthrough 档
  - 规则细节见 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md)

> 📌 **Evidence 档位是合法状态**：科学史里大多数论文贡献不大但有佐证价值。KB 接受它们存在，**不强求**每篇论文都新增 pri.* 或补完整限制链。

### Step 3 · 节点新建判据（关键）
对每个候选节点，检查以下判据至少满足其一：
- [ ] 能独立回答一类有意义的查询
- [ ] 拥有独立的设计选择空间
- [ ] 会被多篇论文复用
- [ ] 拥有独立的限制链 / 证据链 / 竞争关系

> ⚠ **若不确定，新建时留 `note: "pending consolidation"` 字段，提 PR 前请专家确认**。SCHEMA §1.4 提供了边界判断示例。

### Step 4 · 关系填写（SCHEMA §4.2）
- [ ] 每个新 entity/method 至少有 1 条 `PART-OF` 或 `CHARACTERIZED-BY` / `OPERATIONALIZED-AS`
- [ ] 每个新 principle 至少被 1 条 `BOUNDED-BY` 或 `ENABLED-BY` 引用
- [ ] 每条 relation 填 `source.claim`（引自原文的一句论断）
- [ ] 若为 `BOUNDED-BY` 且本文是 `breakthrough` 档，尽量配套写 `breakthrough_paths`（避免新建 chain-gap）
- [ ] **Evidence 档位豁免**：`contribution_type: evidence` 的论文**不强求**新增 `breakthrough_paths`，也**允许**产出 orphan 节点——这是该档位的正常形态，不计入缺口指标

### Step 5 · 时间维度
- [ ] `historical_landmarks.first_demonstration` —— 若本文是首次演示
- [ ] `historical_landmarks.best_demonstration` —— 若本文刷新最佳值
- [ ] `selected_milestones` —— 其他关键拐点按需

### Step 6 · 矛盾与开放
- [ ] 若与已有论点矛盾 → 在相关节点补 `contested_claims`
- [ ] 若论文明确提出未解问题 → 填 `open_questions`

### Step 7 · 文件保存
- [ ] 位置：`topics/<topic>/papers/{first_author_lower}{year}.yaml`
- [ ] 文件头：`# Schema版本：v4.5`
- [ ] ID 全局唯一（`grep -r "ent.new_id" topics/` 验证）

### Step 8 · 运维文件同步
- [ ] `PROCESSED_PAPERS.md` 追加记录
- [ ] `LOG.md` 追加 `## [YYYY-MM-DD] ingest | description`
- [ ] 检查是否影响 `synthesis/` 页面（若影响，追加"需要更新"标记或直接更新）

### Step 9 · 本地验证（必须全过）
```bash
python scripts/lint.py --summary                   # 0 errors（权威检查；跨专题引用需全库解析）
python scripts/stats.py                            # 6 指标不倒退
python scripts/build_index.py                      # 重建 INDEX
```

### Step 10 · 提 PR
- [ ] PR 标题：`add {author}{year}: {论文核心贡献一句话}`
- [ ] 勾选 PR 模板中的全部质量门
- [ ] 关联相关 issue（若由 issue 驱动）

---

## Evidence 档位最低入库门槛（v4.4 新增）

> 对应 `meta.contribution_type: evidence` 的论文，占库中绝大多数。本节明确这类论文的最低要求，避免"每篇都要补完整限制链"的隐含期待。

**必须满足（任何论文都不能省）**：
- [ ] `meta` 块完整（zotero_key / topic / source_type / contribution_type / title / year / first_author / doi）
- [ ] 至少 1 条 `relation`，`subject` 或 `object` 指向**已有节点**（跨文件引用 OK）
- [ ] 至少 1 个带 `conditions` 的 `demonstrated_value`（若论文报告了具体数据点）
- [ ] 所有 relation 带 `source.claim`

**允许（不构成缺陷）**：
- ✅ 不新增 `pri.*`（只引用已有原理）
- ✅ 不填 `breakthrough_paths`（若论文没有提出或演示新路径）
- ✅ 产出 orphan 节点（Level 2 实例节点挂不上多条关系是正常的）
- ✅ `verification_status: inferred` 占多数（综述转述、二手数据）

**触发升档为 `breakthrough` 的信号**（若命中其一，请重新评估）：
- ⚠ 论文明确声称"打破 XX 指标记录"
- ⚠ 提出新原理并给出实验验证
- ⚠ 证伪已有论断（需同步补 `contested_claims`）
- ⚠ 首次在某 regime 下演示某路径

> **为什么放宽**：`evidence` 级论文的价值在于**佐证当时代的状态**和**提供指标数据点**——这是时频领域沿着清晰坐标轴推进的必要材料。硬性要求补限制链会淹没真正的 `breakthrough` 信号。

---

## AI-Human 协作契约

本知识库采用 AI（Copilot / Claude Code）+ 人类专家协作模式。职责划分：

### 专家（人类）必须拍板的事项
- ✋ **节点新建 / 删除**：尤其是 pri.* 层级的 domain / foundational 节点
- ✋ **争议裁决**：`contested_claims` 的最终判定
- ✋ **Schema 演进**：SCHEMA.md 的任何修改
- ✋ **限制的生命周期**：何时把限制标 `limit_status: resolved`
- ✋ **跨专题节点提升**：从单专题 ent/pri 提升到 `topics/shared/`

### AI 可自主完成的事项
- ✅ **YAML 摄入**：按 Step 1–9 完成单篇摄入 PR，专家审核合并
- ✅ **INDEX / 索引重建**：`scripts/build_index.py` 自动重跑
- ✅ **Synthesis 草稿**：基于现有 YAML 生成综合页 draft（标 `🟡 draft`）
- ✅ **Lint 修复 PR**：duplicate-def / dangling-ref / missing-conditions 的机械性修复
- ✅ **Chain-gap 批量补**：按 `reports/chain_gap_*.md` 中 🟢 级别条目批量补 `breakthrough_paths`
- ✅ **Orphan 诊断报告**：生成 `reports/orphans_*.md`

### 灰色地带（AI 先做草稿，专家审定）
- 🟡 节点粒度拆合（"是并入父节点还是独立？"）
- 🟡 Synthesis 页内容（AI 提供草稿，专家添加数值与结论细节）
- 🟡 跨文件复用抽象（"这个 pri.* 是否应该成为公共节点？"）

---

## 新建专题 vs 合并 vs 使用 shared 的判据

| 情形 | 推荐做法 |
|------|---------|
| 当前专题内已有类似但不同的工作原理，且积累 ≥ 3 篇论文 | 考虑新建子分支（同专题内） |
| 新内容完全不同物理载体、有独立限制链与工程路线 | 新建专题（更新 TOPICS.md + 添加 `_meta/architecture.md`） |
| 节点被 ≥ 2 个专题共用（如"Allan 方差"、"Cramér-Rao 下限"） | 提升到 `topics/shared/`，通过 SHARED-WITH 关系引用 |
| 内容只出现在 1 篇论文的某个字段，无复用前景 | **不**新建节点，写入父节点 `note` 字段 |

---

## 代码贡献（脚本 / CI）

- 脚本：`scripts/` 目录，Python 3.10+，依赖 `pyyaml` 即可运行（见 `.env.example`）
- 每个脚本应支持 `--help`，并在 PR 中附示例输出
- CI：`.github/workflows/kb-lint-stats.yml` 会在每个 PR 自动运行 lint + stats，零 error 才可合并

---

## 根目录约定（v4.5+ · TODO.md P0）

仓库根目录只保留**长期稳定入口**，不再新增任何一次性报告 / 同步记录 / backup / 临时分析文件。

**根目录允许的文件类型**：
- 路由文档：`README.md` · `SCHEMA.md` · `CONTRIBUTING.md` · `CLAUDE.md` · `TOPICS.md` · `TODO.md`
- 自动生成索引：`INDEX.md` · `INDEX_metrics.md` · `INDEX_principles.md`
- 运维文件：`LOG.md` · `PROCESSED_PAPERS.md` · `paper-inkb.md`

**一次性 / 过程性 / 诊断性文档**一律放入 `reports/` 子目录，分层规则见 [`reports/README.md`](reports/README.md)：
- `reports/active/`：仍驱动决策
- `reports/archive/`：已完成使命，仅留可追溯性
- `reports/generated/`：脚本输出

PR 审核时若发现向根目录新增非入口文件，应在 review 中要求迁入 `reports/` 对应子目录。

---

## 报告问题 / 请求新功能

- Issue 模板：见 `.github/ISSUE_TEMPLATE/`
  - `ingest-paper.yml`：请求摄入一篇新论文
  - `suggest-new-node.yml`：建议新建节点
  - `process-paper.yml`：论文加工请求（自动化）

---

> 本文件是"路由器"：具体判据由 SCHEMA.md 决定，具体查询由 docs/USAGE.md 指导，AI 行为由 CLAUDE.md 规范。
