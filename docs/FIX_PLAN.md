# sci-logic-kb 工程化运营固化计划

> **目标**：将知识库从"探索性建设"切换到"工程化运营"，固定 5 条核心流程，
>  让 SCHEMA.md 做真源、YAML 做主数据、scripts 做质量门、GitHub PR 做审核闸、
>  Dify 做查询前台和草稿辅助。
>
> **原则**：不新建体系，只确认和固化已有文件/脚本中已定义的流程。
>  每步必须可回滚、可审计、可单步验证。

---

## 阶段 1：工程闭环固化（GitHub 仓库内）

### 1.1 确认核心质量门

**现状**：scripts/lint.py、stats.py、build_index.py 已存在，GitHub Actions 已配置。
但 PR 模板可能未强制要求跑这三步。

**操作**：
- 确认 `.github/PULL_REQUEST_TEMPLATE.md` 的 checklist 包含：
  ```markdown
  - [ ] 已运行 `python scripts/lint.py --summary`（无新增 error）
  - [ ] 已运行 `python scripts/stats.py`（stats 不倒退）
  - [ ] 已运行 `python scripts/build_index.py`（INDEX 文件已更新）
  ```
- 检查 `.github/workflows/kb-lint-stats.yml` 是否确实是 PR 必过门
- 如有遗漏，补上

### 1.2 对齐 CLAUDE.md 与 CONTRIBUTING.md

**现状**：CLAUDE.md（2026-04-21）版本滞后于 CONTRIBUTING.md（2026-04-24）。
CONTRIBUTING.md 已经是 v4.4 三档规范 + checklist，CLAUDE.md 还引用旧版规则。

**操作**：
- CLAUDE.md 引用 SECTION 改为直接指向 `CONTRIBUTING.md` 和 `docs/CONTRIBUTION_TIER_RULES.md`
- 删除 CLAUDE.md 中与 CONTRIBUTING.md 重复的 content（如步骤 1-7 流程）
- 改为一句话："论文摄入流程详见 CONTRIBUTING.md，档位规则详见 docs/CONTRIBUTION_TIER_RULES.md"
- 保留 CLAUDE.md 独有内容：节点 ID 命名规范、已用节点速查路径、人机协作原则

### 1.3 确认 paper-inkb.md 的去留

**现状**：paper-inkb.md（50KB 手动维护）与 PROCESSED_PAPERS.md（26KB 自动生成）存在双源漂移风险。

**操作**：
- 判定 paper-inkb.md 是否仍然需要手动维护
- 若需要：添加注释说明它与 PROCESSED_PAPERS.md 的职责边界
- 若不需要：标记为 archive，在 repo 内保留但不更新

### 1.4 确认 synthesis 更新规则

**现状**：ultrastable-laser 有 8 篇 synthesis，OFC 仅 1 篇，其余专题 0 篇。
scripts/freshness.py 已存在但未见整合到流程中。

**操作**：
- 确认以下规则：
  ```
  某专题 papers ≥ 20 篇 → 必须至少 1 篇 synthesis 存在
  新论文入库 → freshnes.py 检查受影响 synthesis
  影响标记 → 在 synthesis 文件头部添加 `> 🟡 needs-update: YYYY-MM-DD`
  ```
- 将 freshness 检查写入 GH Actions 的 lint workflow（可作为 info 级别，不阻断）
- 或作为 `build_index.py` 的一部分自动运行

### 1.5 确认 reports 清理规则

**现状**：reports/active/ 已分层，但 archive/ 和 generated/ 下有大量一次性中间产物。

**操作**：
- 确认规则：
  ```
  reports/active/ — 仍驱动决策的报告，必须定期 review
  reports/archive/ — 历史决策/已完成的迁移，不删除
  reports/generated/ — 脚本输出，可随时删除重新生成
  ```
- 把明确的 archive 材料从 active 移走
- 清理 generated 目录（标记为"可删除"）

---

## 阶段 2：Dify 接入 — 只读 + 草稿

### 2.1 确认 Dify 知识库配置

**现状**：ultrastable_laser_kb 已创建，80 篇论文已导入（带结构化 entities/principles/metrics/methods/relations）。
embedding_model: null（economy 模式不需要 embedding），embedding_available: true。

**操作**：
- 确认"economy 模式"在这个场景下是否够用
  - economy = keyword search only（无需 embedding）
  - 当前 80 篇已传，`total_available_documents: 81`
- 创建第一个 Dify App："科研查询助手"
  - 类型：Text Generator 或 Chat
  - 关联知识库：ultrastable_laser_kb
  - System Prompt 约束：
    ```
    你是一个时间频率计量结构化知识库的查询助手。
    规则：
    1. 优先从知识库检索，其次用自己的知识
    2. 每个结论必须引用来源论文（ID）
    3. 不确定时明确说"需要专家确认"
    4. 不回答与时间频率计量无关的问题
    ```

### 2.2 验证 Dify → free-claude-code 链路

**现状**：已有能力验证（Dify 容器 → 172.17.0.1:8082 → free-claude-code → DeepSeek V4 Pro）。

**操作**：
- 在 Dify 中创建一个 Workflow：
  ```
  [开始] → [LLM 节点: 理解用户问题] 
         → [HTTP 节点: POST 172.17.0.1:8082/v1/messages]
         → [Code 节点: 提取 content[0].text]
         → [结束]
  ```
- 验证 Workflow 能通
- 记录延迟基线（DeepSeek V4 Pro ~60-90s）

### 2.3 草稿 Dify 论文入库助手

**操作**：
- 在 Dify 中创建 App："论文入库草稿助手"
  - 输入：DOI / Zotero Key / 摘要
  - 参考：SCHEMA.md + CONTRIBUTING.md
  - 输出：YAML 草稿 + PR checklist
  - 明确标注：`🟡 AI-generated draft, pending expert review`
- 这个 App **不写入主库**，只生成建议

---

## 阶段 3：增量 Fix — 已知问题修复

### 3.1 lint 历史错误收口

**现状**：113 error / 12 warning / 216 info（2026-04-24）

**操作**：
- 按 lint 大类生成问题清单
- 分类：机械修复（批量改） vs 需专家判断（开 issue）
- 每次选一个 lint 大类治理，不混着修

### 3.2 失败论文修复

**现状**：9 篇论文 YAML 解析失败（`'str' object has no attribute 'get'`），未入库

**操作**：
- 逐篇检查这 9 个 YAML 文件的结构问题
- 修好后重新导入 Dify

### 3.3 OFC synthesis 扩展

**现状**：OFC 114 篇论文，仅 1 篇 synthesis

**操作**：
- 至少补充 2-3 篇 synthesis（梳齿生成原理/频率锁定方法/应用场景）
- 建立 synthesis 更新节奏

---

## 固化后的工程流程总览

```
                     ┌──────────────────────┐
                     │    用户（读者/建设者）    │
                     └────┬────────────┬─────┘
                          │            │
                    ┌─────▼──┐   ┌─────▼──────┐
                    │ Dify   │   │ GitHub      │
                    │ 查询   │   │ 浏览/PR     │
                    │ 草稿   │   │ Issue       │
                    └──┬─────┘   └──┬──────────┘
                       │            │
                 ┌─────▼────────────▼──────────┐
                 │    质量门 (GH Actions)        │
                 │  lint.py │ stats.py │        │
                 │  build_index.py              │
                 └──────────────┬───────────────┘
                                │
                 ┌──────────────▼───────────────┐
                 │    主数据 (GitHub main)       │
                 │  SCHEMA.md (真源)             │
                 │  YAML (实体数据)              │
                 │  INDEX*.md (自动生成)         │
                 │  PROCESSED_PAPERS.md          │
                 └──────────────────────────────┘
```

## 执行顺序

| 优先级 | 任务 | 预估时间 | 依赖 |
|--------|------|---------|------|
| P0 | 1.1 确认 PR 质量门 | 15min | 无 |
| P0 | 1.2 对齐 CLAUDE.md | 20min | 无 |
| P0 | 1.3 确认 paper-inkb.md | 10min | 无 |
| P0 | 2.1 建第一个 Dify App | 30min | 阶段 1 |
| P1 | 1.4 synthesis 更新规则 | 20min | 无 |
| P1 | 1.5 reports 清理规则 | 15min | 无 |
| P1 | 2.2 验证 Dify Workflow 链路 | 30min | 2.1 |
| P1 | 2.3 草稿入库助手 | 30min | 2.1 |
| P2 | 3.1 lint 历史收口 | 按需 | 1.1 |
| P2 | 3.2 失败论文修复 | 20min | 无 |
| P2 | 3.3 OFC synthesis 扩展 | 按需 | 1.4 |

---

## 不做的事

- 不新建文件（只确认和修正已有文件）
- 不改 SCHEMA.md 核心规则
- 不重构现有 YAML 文件内容（lint 修格式不修内容）
- 不让 Dify 直接写 main（只做只读和草稿）
- 不设 GitHub Pages（阶段 2 的事）
