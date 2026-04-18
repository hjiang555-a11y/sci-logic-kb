# sci-logic-kb: 逻辑驱动的科研知识库

> 一个为时间频率计量领域设计的结构化知识库，支持科研推理链条的显式提取与嵌入。

## 项目目标

构建一个**逻辑驱动**的科研知识库，将领域论文转化为结构化、机器可读的知识节点与关系网络。核心目标：

- **科研推理显式化**：提取论文中的问题、解决方案、验证结果，形成可追溯的推理链条
- **知识结构可计算**：通过五类节点、八种关系建立语义网络，支持 AI 辅助的文献分析、趋势发现与假设生成
- **专家可持续**：设计符合领域专家思维习惯的架构，支持长期迭代与跨专题扩展
- **AI 能力延伸**：为大型语言模型提供精准的领域上下文，提升科研问答、综述撰写与创新建议的可靠性

## 设计理念

- **质量优先**：每条知识节点必须通过人工审核与交叉验证
- **机器可读**：所有内容以结构化 YAML 存储，支持自动化查询与分析
- **专家可持续**：知识架构贴近专家认知，降低长期维护成本
- **稳定度优于线宽**：在知识表示中，系统稳定度与长期可靠性比瞬时性能更重要

## 核心架构

知识库采用 **“专题‑节点‑关系”** 三层结构：

1. **专题 (Topics)**：按技术领域划分（超稳激光、光学频率梳、频率标准等），每个专题有独立目录与架构
2. **节点 (Nodes)**：分为五类——技术实体 (`ent.`)、原理 (`pri.`)、方法 (`meth.`)、指标 (`met.`)、素材 (`src.`)
3. **关系 (Relations)**：八种语义关系（`PART‑OF`, `COMPETES‑WITH`, `BOUNDED‑BY`, `FOLLOWS`, `CONTRIBUTES‑TO`, `CONDITIONED‑BY`, `REFERENCES`, `SHARED‑WITH`）

详细规范请参阅 [SCHEMA.md](SCHEMA.md)。

## 目录结构

```
sci-logic-kb/
├── SCHEMA.md                     # 完整规范（节点、关系、专题体系、演进原则）
├── README.md                     # 项目概览（本文件）
├── CLAUDE.md                     # AI 协作规范与最佳实践
├── TOPICS.md                     # 专题架构概览（已合并至 SCHEMA.md，本文件为轻量索引）
├── scripts/                      # 自动化脚本
│   ├── extract.py                # 从论文 PDF/文本提取结构化 YAML
│   ├── validate.py               # 验证 YAML 符合 SCHEMA
│   ├── sync_obsidian.py          # 同步到 Obsidian 知识库
│   └── stats.py                  # 生成知识库统计报告
├── topics/                       # 专题目录
│   ├── ultrastable-laser/        # 超稳激光（78篇论文，当前重点梳理对象）
│   ├── optical-frequency-comb/   # 光学频率梳
│   ├── frequency-standard/       # 频率标准（光学+微波）
│   ├── time-frequency-transfer/  # 时间频率传递
│   └── shared/                   # 跨专题共享节点（原理、方法、指标）
└── .github/workflows/            # GitHub Actions 自动化流水线
    └── sync-obsidian.yml         # 定时同步到 Obsidian
```

## 快速开始

### 1. 添加新论文

```bash
# 进入专题目录
cd topics/ultrastable-laser/papers/

# 创建 YAML 文件（参考现有模板）
# 编辑文件，填写节点、关系、问题‑解决方案‑结果链条
# 运行验证脚本
python ../../scripts/validate.py your_paper.yaml
```

### 2. 使用知识库

```bash
# 生成统计报告
python scripts/stats.py

# 同步到 Obsidian（需要配置 API 密钥）
python scripts/sync_obsidian.py

# 搜索特定节点
grep -r "ent.laser" topics/
```

### 3. 重新梳理现有论文（当前重点）

我们正在对超稳激光专题（78篇论文）进行系统性重新梳理，重点强化 **问题‑解决方案‑结果** 推理链条。具体步骤参见 [REORGANIZATION_PLAN.md](REORGANIZATION_PLAN.md)。

## 维护与贡献

### 自动化流水线

- **每日同步**：GitHub Actions 自动将最新更改同步到 Obsidian 知识库（通过 REST API）
- **验证检查**：每次提交自动运行 `validate.py`，确保 YAML 符合 SCHEMA
- **统计报告**：每周生成知识库规模、节点分布、关系密度等指标

### 贡献指南

1. **选择专题**：优先从「当前重点」专题开始（见 SCHEMA.md 中的「建设优先级建议」）
2. **遵循 SCHEMA**：所有 YAML 文件必须符合 SCHEMA.md 规范
3. **保持一致性**：新节点 ID 使用已有命名约定，避免冲突
4. **添加推理链条**：每篇论文必须显式标注 `open_questions`、`breakthrough_paths`、`verification_status`

### 同步到 Obsidian

知识库通过 `sync_obsidian.py` 脚本与 Obsidian 仓库保持同步，确保：

- 原始 YAML 文件保留在 `topics/` 目录
- Obsidian 中生成友好的 Markdown 视图，便于人工浏览
- 双向链接自动建立，支持图谱导航

详细配置见脚本注释。

## 联系与许可

- **维护者**：时间频率计量领域资深科学家（AI 与计算机网络新人）
- **协作模式**：GitHub Issues + Pull Requests，AI 辅助代码审查与知识提取
- **许可证**：知识库内容遵循 CC‑BY‑4.0，代码部分遵循 MIT License

---

> 本知识库是**科研能力的延伸**，而非转行 AI。核心价值在于将领域专家的深度理解转化为可计算、可推理的结构化知识，为下一代 AI 辅助科研工具提供高质量领域语料。
