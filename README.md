# sci-logic-kb: 逻辑驱动的科研知识库

> 一个为时间频率计量领域设计的结构化知识库，支持科研推理链条的显式提取与嵌入。

## 项目目标

本知识库为**领域专家本人**服务，不是通用 AI 问答库。目标分主次：

### 主要目标（专家本人视角）

- **梳理技术边界**：在时间频率计量的每条技术分支上，显式标出"当前性能极限在哪、由什么限制决定、在什么 regime 下活跃"
- **探索突破路线**：把已演示 / 已提出 / 已证伪的突破路径组织为可扫视的矩阵，辅助专家决策下一步该走哪条

### 次要目标（复用副产品）

- **辅助写作**：为综述、提案、引言自动派生 related work / motivation 草稿
- **梳理思路**：在阅读、讨论、讲授时作为外置长期记忆
- **学习综合**：新同事 / 学生通过 synthesis 页面快速建立专题全局观

> **定位提醒**：KB 不是推理引擎，真正的突破判断仍由专家做出。KB 做的是把**限制–路径–状态图**压缩到专家一眼就能决策的结构。符号层面能做到这一点就够了。

### 非目标

- ❌ 不做向量检索 / 语义搜索的通用数据库
- ❌ 不要求每篇论文都贡献新原理（见下文"论文贡献分级"）
- ❌ 不追求"AI 自动写出突破方案"——这超出符号知识库能力

## 论文贡献分级（v4.4 新增）

时间频率计量领域的核心优势是**关键比较指标清晰**（σ_y、linewidth、accuracy、SWaP…）。因此绝大多数论文不需要提供新原理，只需要在已有坐标轴上提供一个新数据点。强行要求每篇论文都补完整限制链会导致信噪比下降、TODO 永远降不下去。

知识库按 `meta.contribution_type` 把论文分三档，对应不同的入库门槛：

| 档位 | 典型贡献 | 最低入库要求 |
|------|---------|-------------|
| `breakthrough` | 打破指标记录 / 提出新原理 / 证伪旧论断 | 完整限制链、`breakthrough_paths`、`historical_landmarks.best_demonstration` |
| `evidence` | 在已有节点上提供新数据点、新条件验证、工程复现 | 挂钩到已有节点 + 一个 `demonstrated_value` + `source.claim`，**不强求**补 chain-gap / orphan |
| `framework` | 综述 / 路线图 / 教科书章节 | 定义 Level 0/1 顶层实体与 meta/domain 原理；不定义具体参数实例 |

- 科学史里绝大多数论文都是 `evidence` 级——这是合理状态，不是缺陷
- `evidence` 档位的存在保证了**时代背景 / 佐证论文**能被低成本收录，不被结构要求拖住
- 详细规范见 [SCHEMA.md 第九节](SCHEMA.md) 与 [CONTRIBUTING.md](CONTRIBUTING.md) Step 2

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

> **交互式图谱可视化（v4.5+）**：`docs/graph/index.html` 提供基于 [Cytoscape.js](https://js.cytoscape.org/) 的只读图浏览，支持按 type / topic / tier 上色、按节点 ID 搜索、按谓词过滤。本地预览：`python -m http.server 8000 --directory docs/graph`，然后打开 <http://localhost:8000>。数据刷新：`bash scripts/build_graph_view.sh`。

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
│   ├── optical-frequency-combs/  # 光学频率梳（90篇论文）
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
# 在仓库根目录执行

# 创建 YAML 文件（参考现有模板）
# 编辑文件，填写节点、关系、指标与必要的推理链条
python scripts/lint.py --summary
python scripts/stats.py
python scripts/build_index.py
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

超稳激光专题（78 篇）Round 1–4 主线整治已基本闭环；当前工作重心转为：

- 收口超稳激光 `synthesis/` 页面的 freshness / 专家签字尾项
- 为光学频率梳专题（90 篇）补首批 synthesis 页面与跨论文综述入口
- 推进跨专题复用度与下游骨架专题的代表论文摄入

统一待办与建议见 [`TODO.md`](TODO.md)；历史整治背景见 [`reports/REORGANIZATION_PLAN.md`](reports/REORGANIZATION_PLAN.md)。

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

- **知识库校验**：`kb-lint-stats.yml` 在相关 PR / push 上运行 `lint.py`、`stats.py` 与 freshness 检查
- **综合页新鲜度**：`synthesis-freshness.yml` 会在 PR 中自动标记 `needs-refresh`
- **论文处理**：`process-paper*.yml` 支持自动化处理 / 回填工作流

### 贡献指南

1. **选择专题**：优先从「当前重点」专题开始（见 SCHEMA.md 中的「建设优先级建议」）
2. **遵循 SCHEMA**：所有 YAML 文件必须符合 SCHEMA.md 规范
3. **保持一致性**：新节点 ID 使用已有命名约定，避免冲突
4. **按档位补结构**：`breakthrough` 论文补完整推理链；`evidence` 论文至少挂已有节点、relation 与可溯源指标

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
