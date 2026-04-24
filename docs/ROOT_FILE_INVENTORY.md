# Root File Inventory — 保留 / 迁移 / 删除清单

> **生成日期**：2026-04-24（TODO.md P0-2 产出）
> **用途**：审查当前仓库根目录所有文件，判定每份文件在"目标态"下的去留。
> **配套约定**：见 [`CONTRIBUTING.md` §根目录约定](../CONTRIBUTING.md)、[`reports/README.md`](../reports/README.md)。

---

## 1. 保留（Long-term entries）

根目录的长期稳定入口，任何时候都应存在。

| 文件 | 类别 | 说明 |
|------|------|------|
| `README.md` | 路由 | 仓库首页 |
| `SCHEMA.md` | 规范 | 唯一 Schema 真源 |
| `CONTRIBUTING.md` | 路由 | 贡献流程 |
| `CLAUDE.md` | 路由 | Claude Code 行为规范 |
| `TOPICS.md` | 路由 | 专题列表（应去高频数字化） |
| `TODO.md` | 规划 | 当前优先级清单 |
| `INDEX.md` | 自动 | 全局节点索引（脚本生成） |
| `INDEX_metrics.md` | 自动 | 指标索引（脚本生成） |
| `INDEX_principles.md` | 自动 | 原理索引（脚本生成） |
| `LOG.md` | 运维 | 演化日志 |
| `PROCESSED_PAPERS.md` | 运维 | 已处理论文列表（应去高频数字化） |
| `paper-inkb.md` | 运维 | 论文入库参考索引 |
| `.env.example` · `.gitignore` | 基础设施 | 工程化文件 |

## 2. 迁移至 `reports/archive/obsidian-sync/`（P1）

一次性 Obsidian / Zotero 同步过程记录，已完成其历史使命。

| 文件 | 原因 |
|------|------|
| `SYNC_REPORT_OBSIDIAN_UPDATE.md` | 2026-04-21 07:58 一次性同步报告 |
| `SECOND_SYNC_REPORT_OBSIDIAN_UPDATE.md` | 2026-04-21 08:15 二次同步 |
| `THIRD_SYNC_REPORT_OBSIDIAN_UPDATE.md` | 第三次同步 |
| `SYNC_REPORT_OBSIDIAN_UPDATE_20260421_215834.md` | 带时间戳的同步 |
| `SYNC_REPORT_POST_PULL_20260421_220032.md` | 拉取后同步 |

## 3. 删除（None proposed）

目前不建议从根目录直接删除任何文件。一次性文件一律通过归档（保留可追溯性）处理。

---

## 4. 执行状态

- [x] P0-1 `reports/README.md` 已建立分层索引
- [x] P0-2 本清单已产出
- [x] P0-3 `CONTRIBUTING.md` 已补根目录约定
- [ ] P1-1 迁移 SYNC_REPORT* → `reports/archive/obsidian-sync/`（下一步）
- [ ] P1-2 迁移 `reports/*.backup` + 一次性 JSON → `reports/archive/`（下一步）

迁移完成后本文件会保留作为"根目录清单"的备忘记录。
