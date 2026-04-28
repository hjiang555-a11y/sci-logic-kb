# sci-logic-kb

> 时间频率计量领域的结构化科研知识库  
> **核心问题**：当前性能极限在哪、为什么卡在这里、怎样突破

---

## 快速入口

| 我要... | 查看文档 |
|---------|----------|
| **上手操作** | [WORKFLOW.md](docs/WORKFLOW.md) - 操作流程指南 |
| **提交论文** | [CONTRIBUTING.md](CONTRIBUTING.md) - 完整质量门 |
| **查询知识** | [docs/USAGE.md](docs/USAGE.md) - 查询和诊断 |
| **审核专题** | [docs/REVIEW_GUIDE.md](docs/REVIEW_GUIDE.md) - 审核入口 |
| **了解规范** | [SCHEMA.md](SCHEMA.md) - 节点、关系、字段定义 |
| **AI协作** | [CLAUDE.md](CLAUDE.md) - AI agent 行为约束 |

---

## 文档分层

| 层级 | 适合谁 | 入口文档 |
|------|--------|----------|
| **操作** | 所有参与者 | [docs/WORKFLOW.md](docs/WORKFLOW.md) |
| **审核** | 审核者/维护者 | [docs/REVIEW_GUIDE.md](docs/REVIEW_GUIDE.md) |
| **使用** | 研究者/读者 | [docs/USAGE.md](docs/USAGE.md) |
| **建设** | 摄入者/贡献者 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **规范** | Schema维护者 | [SCHEMA.md](SCHEMA.md) |
| **索引** | 所有人 | [TOPICS.md](TOPICS.md) / INDEX*.md |

---

## 仓库结构

```
sci-logic-kb/
├── docs/
│   ├── WORKFLOW.md              # 操作流程指南（新）
│   ├── REVIEW_GUIDE.md          # 审核入口
│   └── USAGE.md                 # 查询指南
├── topics/
│   └── <topic>/
│       ├── _meta/               # 专题架构和原则
│       ├── papers/*.yaml        # 论文节点
│       └── synthesis/*.md       # 综合分析
├── scripts/
│   ├── lint.py                  # 质量检查
│   ├── stats.py                 # 统计报告
│   └── build_index.py           # 索引生成
├── SCHEMA.md                    # 规范真源
├── CONTRIBUTING.md              # 贡献指南
├── CLAUDE.md                    # AI 协作规范
├── TOPICS.md                    # 专题状态
└── INDEX*.md                    # 自动生成索引

```

---

## 三个最常用命令

```bash
python scripts/lint.py --summary    # 质量检查
python scripts/stats.py             # 统计报告
python scripts/build_index.py      # 重建索引
```

---

## 核心约束

1. **SCHEMA.md** 是唯一真源，冲突时优先级最高
2. **INDEX*.md** 和 **docs/CURRENT_NODES_REFERENCE.md** 自动生成，不手工编辑
3. 专题审查先看 **_meta/architecture.md**，不从零散 YAML 盲扫
4. **GitHub 优先**：完成后立即同步到协作平台

---

## 专题列表

详见 [TOPICS.md](TOPICS.md)

当前专题：
- 超稳激光 (ultrastable-laser)
- 光学频率梳 (optical-frequency-combs)
- 离子/原子光钟 (optical-atomic-clocks)
- 微波原子钟 (microwave-atomic-clocks)
- 时间频率传递 (time-frequency-transfer)
- 精密测量应用 (precision-measurement-applications)

---

## 已入库论文参考

快速查重：[paper-inkb.md](paper-inkb.md)（标题 + Zotero Key + DOI 三列快查）

---

*构建理念：人做策展与提问，AI 做簿记与维护*  
*灵感来源：Karpathy LLM Wiki*
