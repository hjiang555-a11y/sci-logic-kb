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

## 三种使用场景

知识库面向三类用户，每类用户有独立的入口文件：

| 我是谁 | 我要做什么 | 从哪里开始 |
|--------|-----------|-----------|
| **使用者**（研究者 / 综述作者 / 学生） | 基于领域知识做查询、诊断、综述 | → [`docs/USAGE.md`](docs/USAGE.md)（三类典型查询 × 三跳路径） |
| **建设者**（论文摄入、节点整治） | 贡献论文、维护节点与关系 | → [`CONTRIBUTING.md`](CONTRIBUTING.md)（Step 1–10 + AI 协作契约） |
| **开发者**（脚本、CI、工具链） | 扩展自动化、改进 Schema | → [`SCHEMA.md`](SCHEMA.md) + [`scripts/`](scripts/) + [`.github/workflows/`](.github/workflows/) |

> 首次打开仓库？推荐阅读顺序：[`INDEX.md`](INDEX.md) 顶部的"🧭 按研究问题导航"→ [`docs/USAGE.md`](docs/USAGE.md)。

## 目录结构

```
sci-logic-kb/
├── SCHEMA.md                     # 完整规范（节点、关系、专题体系、运维操作）
├── README.md                     # 项目概览（本文件）
├── CLAUDE.md                     # AI 协作规范与最佳实践
├── TOPICS.md                     # 专题架构概览
├── INDEX.md                      # ← 自动生成（build_index.py），全局导航
├── INDEX_metrics.md              # ← 自动生成，跨专题指标快查
├── INDEX_principles.md           # ← 自动生成，跨专题原理快查
├── LOG.md                        # 知识库演化日志（时间线追踪变更历史）
├── PROCESSED_PAPERS.md           # 已处理论文完整列表
├── scripts/                      # 自动化脚本
│   ├── stats.py                  # 6 项推理就绪度量 + 库存统计
│   ├── lint.py                   # 11 项健康检查（CI 强制运行）
│   ├── build_index.py            # 从 YAML 自动生成分层 INDEX 文件
│   ├── graph.py                  # 知识图谱导出（JSON/GraphML）+ 诊断
│   ├── freshness.py              # 综合页面新鲜度追踪
│   ├── batch_quality_check.py    # 批量质量检查
│   ├── process_paper.py          # GitHub Actions 论文处理
│   └── ...                       # Zotero 集成脚本
├── topics/                       # 专题目录
│   ├── ultrastable-laser/        # 超稳激光（78篇论文）
│   │   ├── papers/               # YAML 知识节点（source of truth）
│   │   ├── synthesis/            # 跨论文综合分析页面（derived view）
│   │   ├── _meta/                # 专题架构图与元数据
│   │   └── INDEX.md              # ← 自动生成，专题详表
│   ├── optical-frequency-combs/  # 光学频率梳（61篇论文）
│   ├── frequency-standards/      # 频率标准（光学+微波）
│   ├── time-frequency-transfer/  # 时间频率传递
│   ├── timescales/               # 时间标尺与钟组
│   └── shared/                   # 跨专题共享节点
└── .github/workflows/            # GitHub Actions 自动化流水线
    ├── process-paper.yml         # 论文处理工作流
    └── kb-lint-stats.yml         # 知识库 lint + stats（PR 时自动运行）
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
# 6 项推理就绪度量（核心进度条）
python scripts/stats.py

# 健康检查（孤立节点、悬空引用、重复等 11 项检查）
python scripts/lint.py --summary

# 重新生成所有 INDEX 文件（修改 YAML 后运行）
python scripts/build_index.py

# 导出知识图谱 + 诊断（hub 节点、孤岛等）
python scripts/graph.py --diagnostics
python scripts/graph.py --format json --output kb_graph.json

# 综合页面新鲜度检查
python scripts/freshness.py --check

# 搜索特定节点
grep -r "ent.fp_cavity_system" topics/
```

### 3. 重新梳理现有论文（当前重点）

我们正在对超稳激光专题（78篇论文）进行系统性重新梳理，重点强化 **问题‑解决方案‑结果** 推理链条。具体步骤参见 [REORGANIZATION_PLAN.md](REORGANIZATION_PLAN.md)。

## 知识库运维（v4.3 更新）

知识库采用三大运维操作，受 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式启发：

| 操作 | 描述 | 输出 |
|------|------|------|
| **Ingest** | 摄入新论文，提取 YAML 节点 | YAML 文件 + INDEX/LOG 更新 |
| **Query** | 跨论文综合分析，结果反哺回知识库 | `synthesis/` 综合页面 |
| **Lint** | 健康检查（孤立节点、悬空引用、矛盾数值） | 修复建议 |

**三层架构**：
```
Raw Sources (Zotero PDF) → YAML 节点图 (source of truth) → 运维层 (INDEX/LOG/synthesis)
```

详见 [SCHEMA.md §10](SCHEMA.md) 的完整运维操作规范。

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

完整流程（Step 1–10 摄入 checklist）见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### AI‑Human 协作契约

本知识库由领域专家（人类）与 AI agent（Copilot / Claude Code）协同建设。职责边界：

- **专家必须拍板**：节点新建/删除、争议裁决（`contested_claims`）、Schema 演进、限制状态（`resolved`）变更、跨专题节点提升（到 `topics/shared/`）
- **AI 可自主**：YAML 摄入 PR、INDEX 重建、synthesis 草稿、lint 机械修复、chain-gap 批量补（🟢 级别）
- **灰色地带（AI 先出草稿，专家审定）**：节点粒度拆合、synthesis 结论细节、跨文件复用抽象

详见 [CONTRIBUTING.md · "AI‑Human 协作契约"](CONTRIBUTING.md#ai-human-协作契约)。

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
