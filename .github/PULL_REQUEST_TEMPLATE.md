# Pull Request

## 变更概要

<!-- 一段话描述本 PR 的目标与完成方式 -->

## 变更类型

- [ ] 📄 论文摄入（ingest）— 单篇或批量新论文入库
- [ ] 🔧 节点整固（restructure）— orphan 收敛 / chain-gap 修复 / 节点粒度调整
- [ ] 📊 综合页更新（synthesis）— 新建或刷新 `topics/*/synthesis/*.md`
- [ ] 📘 规范 / 文档（docs）— SCHEMA.md / README.md / CONTRIBUTING.md / USAGE.md
- [ ] 🛠️ 工具 / 脚本（tooling）— scripts/ / CI / 模板
- [ ] 🧹 Lint 修复（lint）— 纯机械性质量修复
- [ ] 🗂️ 索引重建（index）— INDEX.md / INDEX_*.md 重新生成

## 关联 Issue / 报告

<!-- 链接相关 issue 或 reports/*.md 条目 -->
Closes #
关联报告：

## 质量门（Quality Gates）

### 若涉及 YAML 变更
- [ ] `python scripts/lint.py` — 0 errors，warnings 数量不倒退
- [ ] `python scripts/stats.py` — 6 项推理就绪度量不倒退
- [ ] `python scripts/build_index.py` 已重跑且输出已提交
- [ ] 新增节点通过 SCHEMA §1.4 的独立性判据（至少满足其一）
- [ ] 所有新 relation 均含 `source.claim`

### 若涉及新论文
- [ ] `CONTRIBUTING.md` Step 1–10 全部完成
- [ ] `PROCESSED_PAPERS.md` / `LOG.md` 已同步
- [ ] 检查是否影响现有 synthesis 页面（若影响，已标 `needs-refresh` 或已更新）

### 若涉及 Schema / 规范变更
- [ ] SCHEMA.md 同步更新 + 版本号 bump
- [ ] 受影响的下游文件已同步（README / CLAUDE.md / copilot-instructions / templates）
- [ ] LOG.md 追加 `schema` 类型条目

### 若涉及综合页
- [ ] 在页面 header 写明"最后更新"日期与涉及源文件
- [ ] 数值引用可被溯源到具体 YAML 节点

## AI-Human 协作标注

若本 PR 由 AI agent 提出，请选择：

- [ ] AI 可自主合并类（见 CONTRIBUTING.md "AI 可自主完成的事项"）
- [ ] 需要专家拍板类（节点新建/删除、争议裁决、Schema 演进、限制 status 变更、跨专题节点提升）

## 其他说明

<!-- 任何需要审核者注意的上下文、已知限制、后续工作 -->
