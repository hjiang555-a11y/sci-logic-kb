# sci-logic-kb

> 时间频率计量领域的结构化科研知识库。核心问题只有三类：**当前性能极限在哪、为什么卡在这里、怎样突破。**

`sci-logic-kb` 把论文中的系统、原理、方法、指标和关系抽取为可检查的 YAML 节点图，并用自动索引生成跨专题导航。它既是科研阅读入口，也是 AI + 人类专家协作维护的长期知识底座。

## 文档分层

> **唯一技术真源始终是 [`SCHEMA.md`](SCHEMA.md)。** 其他文档只负责不同角色的阅读入口，不重复扩张规则。

| 层级 | 适合谁 | 只解决什么问题 | 入口 |
|------|--------|----------------|------|
| L0 | **审核者 / 维护者** | 我该从哪里审专题结构、核心指标、关键节点？ | [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md) |
| L1 | **研究者 / 使用者** | 我怎么查询、诊断、读综合页？ | [`docs/USAGE.md`](docs/USAGE.md) |
| L2 | **建设者 / 摄入者** | 我怎么新增论文、维护 YAML、过质量门？ | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| L3 | **Schema / 工具维护者** | 节点、关系、专题体系、模板到底怎么定义？ | [`SCHEMA.md`](SCHEMA.md) |
| 辅助索引 | 所有人 | 各专题现状、优先级、自动生成索引在哪？ | [`TOPICS.md`](TOPICS.md)、`INDEX*.md`、`topics/*/INDEX.md` |
| 文档目录 | 所有人 | `docs/` 下有哪些长期文档？分别给谁看？ | [`docs/README.md`](docs/README.md) |
| 入库速查 | **摄入者 / 查重者** | 某篇论文是否已入库？（标题 + Zotero Key + DOI 三列快查） | [`paper-inkb.md`](paper-inkb.md) |

## 最短阅读顺序

- **第一次了解项目**：本 README → `docs/README.md` → `docs/USAGE.md`
- **做审核**：`docs/REVIEW_GUIDE.md` → 对应专题 `_meta/architecture.md` → 代表 YAML
- **做查询**：`docs/USAGE.md` → `INDEX.md` / `INDEX_metrics.md` → `topics/*/synthesis/`
- **做摄入/维护**：`CONTRIBUTING.md` → `SCHEMA.md` → `scripts/lint.py` / `stats.py` / `build_index.py`
- **改规则**：直接看 `SCHEMA.md`

## 仓库骨架

```text
sci-logic-kb/
├── SCHEMA.md                    # 唯一 Schema 真源
├── README.md                    # 文档总路由（本文件）
├── CONTRIBUTING.md              # 建设/摄入流程
├── TOPICS.md                    # 专题状态与优先级
├── INDEX.md                     # 自动生成的全局导航
├── INDEX_metrics.md             # 自动生成的指标快查
├── INDEX_principles.md          # 自动生成的原理快查
├── paper-inkb.md                # 已入库论文参考索引（标题+ZoteroKey+DOI，手动维护）
├── docs/
│   ├── README.md                # docs/ 文档目录与适用对象
│   ├── REVIEW_GUIDE.md          # 审核入口
│   ├── USAGE.md                 # 读者入口
│   ├── DEPLOYMENT_PLAN.md       # 部署/发布规划
│   ├── CONTRIBUTION_TIER_RULES.md
│   ├── ULTRASTABLE_GOVERNANCE_HANDBOOK.md
│   └── CURRENT_NODES_REFERENCE.md
├── topics/
│   └── <topic>/
│       ├── _meta/architecture.md
│       ├── papers/*.yaml
│       ├── synthesis/*.md
│       └── INDEX.md
└── scripts/
    ├── lint.py
    ├── stats.py
    └── build_index.py
```

## 维护时最常用的三个命令

```bash
python scripts/lint.py --summary
python scripts/stats.py
python scripts/build_index.py
```

## 约束

维护这个仓库时，只需先守住下面这些边界：

- `SCHEMA.md` 冲突优先级最高
- `INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` / `docs/CURRENT_NODES_REFERENCE.md` / `topics/*/INDEX.md` 为自动生成文件，不手工编辑
- 专题审查先看 `_meta/architecture.md` 与 `docs/REVIEW_GUIDE.md`，不要从零散 YAML 盲扫
