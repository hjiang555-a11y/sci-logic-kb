# docs/ — 长期文档目录

> 本目录存放面向读者、审核者、维护者和部署者的长期说明文档。主数据仍以 `topics/*/papers/*.yaml` 为真源；自动生成的节点引用以 `docs/CURRENT_NODES_REFERENCE.md` 为准。

## 阅读入口

| 文件 | 适合谁 | 用途 | 维护方式 |
|------|--------|------|----------|
| [`USAGE.md`](USAGE.md) | 研究者 / 查询者 | 说明如何按研究问题查询知识库、阅读索引与综合页 | 手工维护，随查询方式变化更新 |
| [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md) | 审核者 / 专家 | 提供专题结构、节点边界、指标链路的审核路径 | 手工维护，随审核流程变化更新 |
| [`CONTRIBUTION_TIER_RULES.md`](CONTRIBUTION_TIER_RULES.md) | 摄入者 / 审核者 | 解释 `breakthrough` / `evidence` / `framework` 的判定细则 | 规则性文档；若与 `SCHEMA.md` 冲突，以 `SCHEMA.md` 为准 |
| [`ULTRASTABLE_GOVERNANCE_HANDBOOK.md`](ULTRASTABLE_GOVERNANCE_HANDBOOK.md) | 超稳激光专题维护者 | 汇总超稳激光专题治理、节点边界与维护约定 | 专题治理文档，随专题整治更新 |
| [`DEPLOYMENT_PLAN.md`](DEPLOYMENT_PLAN.md) | 维护者 / 发布者 | 规划 GitHub 原生浏览、静态发布与本地维护工作流 | 规划性文档，阶段性更新 |
| [`CURRENT_NODES_REFERENCE.md`](CURRENT_NODES_REFERENCE.md) | 摄入者 / AI agent | 当前节点速查引用，辅助避免重复建点 | **自动生成，不手工编辑** |
| [`graph/`](graph/) | 可视化使用者 / 发布者 | 预留给图谱、静态页面和可视化产物 | 生成或半自动维护 |

## 推荐路径

- **第一次读项目**：先看根目录 [`README.md`](../README.md)，再读 [`USAGE.md`](USAGE.md)。
- **准备审核专题**：读 [`REVIEW_GUIDE.md`](REVIEW_GUIDE.md)，再进入对应专题的 `_meta/architecture.md`。
- **准备摄入论文**：读 [`../CONTRIBUTING.md`](../CONTRIBUTING.md)，必要时查 [`CONTRIBUTION_TIER_RULES.md`](CONTRIBUTION_TIER_RULES.md)。
- **需要部署或发布**：读 [`DEPLOYMENT_PLAN.md`](DEPLOYMENT_PLAN.md)。

## 维护约定

- `SCHEMA.md` 是规则真源；本目录文档只做角色化解释和工作流说明。
- `CURRENT_NODES_REFERENCE.md` 由 `python scripts/build_index.py` 生成，不手工编辑。
- 若新增长期文档，请在本文件登记其适用对象、用途和维护方式。
- 一次性过程报告不要放入 `docs/`，应放入 `reports/active/` 或 `reports/archive/`。