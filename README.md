# sci-logic-kb — 超稳激光科研知识库

> 一个面向科研探索的结构化知识库，用来回答：**当前极限在哪、为什么受限、如何突破。**

---

## 1. 项目目标

本仓库面向**时间频率计量 / 超稳激光**研究，目标不是做通用检索，而是沉淀可推理、可追溯、可扩展的科研知识结构。

核心查询目标：

1. **当前性能极限在哪？**
2. **为什么卡在这里？**
3. **有哪些已验证/待验证的突破路径？**
4. **某个方案在什么条件下成立、失效、存在争议，或仍是开放问题？**

---

## 2. 设计理念

### 2.1 面向科学家的知识组织，而非纯索引

本库采用**符号主义结构化知识图谱**，强调：

- 节点能独立回答有意义的边界问题
- 关系区分“机制”“限制”“条件”“竞争”“层级推导”
- 每个重要结论都可追溯到文献原句或标准来源

### 2.2 人类认知优先，机器处理兼容

- 对人：每个节点保留中文语义说明、核心洞见、适用条件、限制与突破方向
- 对机器：统一前缀命名、层级约束、关系类型、字段结构、可校验的 YAML 模式

### 2.3 Source of Truth 规则

> **`/home/runner/work/sci-logic-kb/sci-logic-kb/SCHEMA.md` 是唯一 Schema 真源。**

若以下文件与 `SCHEMA.md` 冲突，一律以 `SCHEMA.md` 为准：

- `/home/runner/work/sci-logic-kb/sci-logic-kb/README.md`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/.github/copilot-instructions.md`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/scripts/process_paper.py`
- GitHub Actions / Issue 模板文案
- `papers/*.yaml` 的头部版本注释

更新 Schema 时，必须同步检查上述文件，避免再次发生版本漂移。

---

## 3. 输入材料与知识来源

本库当前接受三类主要知识来源：

1. **基本原理**
   - 来源：经典教材、基础论文、必要时的权威网络资料
   - 例：高斯光束、谐振腔理论、涨落耗散定理

2. **前沿知识**
   - 来源：专家认可的研究论文（当前以 Zotero 管理）
   - 例：Kessler 2012、Matei 2017、Lee 2026

3. **标准定义 / 权威约定**
   - 来源：BIPM 等权威机构发布的标准、定义、术语说明
   - 用途：单位定义、测量标准、概念边界

---

## 4. 目录结构

```text
/home/runner/work/sci-logic-kb/sci-logic-kb
├── README.md
├── SCHEMA.md
├── QUEUE.md
├── CLAUDE.md
├── BATCH_PROCESSING_PLAN.md
├── papers/                 # 已提取的论文知识条目（YAML）
├── pdfs/                   # 待处理 PDF
├── scripts/
│   └── process_paper.py    # GitHub Models/Claude 提取脚本
└── .github/
    ├── copilot-instructions.md
    ├── workflows/process-paper.yml
    └── ISSUE_TEMPLATE/
```

---

## 5. 知识节点规范（概览）

### 5.1 五类节点

| 前缀 | 类型 | 用途 |
|------|------|------|
| `ent.` | 技术实体 | 系统、装置、部件、外围条件 |
| `pri.` | 原理 | 物理/数学/工程原理 |
| `meth.` | 方法 | 稳频、探测、补偿等方法 |
| `met.` | 指标 | 线宽、Allan 偏差、频噪等可量化指标 |
| `rel.` | 关系 | 节点间语义连接 |

### 5.2 层级设计

- **Level 1**：主分支实体（如 `ent.fp_cavity_system`、`ent.fiber_interferometer`）
- **Level 2**：子单元或参数变体实例
- **ext**：外围条件（如振动环境、热环境、激光源）

### 5.3 最小知识单元原则

一个节点值得存在，当且仅当它能：

- 独立回答一个重要问题；
- 被多篇论文复用引用；
- 拥有独立设计选择空间；
- 或拥有独立的限制链/证据链/竞争关系。

若一个“节点”只是父节点某个字段的展开，应并回父节点。
若一个节点内容过重、内部又有多个可复用机制，则允许继续向下分解。

---

## 6. 关系规范（概览）

| 谓词 | 作用 |
|------|------|
| `PART-OF` | 组件归属 |
| `CHARACTERIZED-BY` | 实体由指标刻画 |
| `OPERATIONALIZED-AS` | 指标通过方法实现/操控 |
| `ENABLED-BY` | 方法由某原理支撑 |
| `BOUNDED-BY` | 性能上限由某原理设定 |
| `DERIVED-FROM` | 原理由更上层原理推导 |
| `CONDITIONED-BY` | 外围条件通过接口制约系统 |
| `COMPETES-WITH` | 同层方案或方法之间的权衡 |

重点关系：

- **`BOUNDED-BY`**：回答“为什么受限”
- **`breakthrough_paths`**：回答“如何突破”
- **`CONDITIONED-BY`**：回答“边界条件和接口要求是什么”

---

## 7. 如何表达科研知识

本库要求尽量显式区分以下维度：

- **事实**：论文实测值、理论值、比较结果
- **机制**：为什么一个方法能工作（`ENABLED-BY`）
- **限制**：为什么性能卡住（`BOUNDED-BY`）
- **前提条件**：成立需要什么（`conditions` / `preconditions`）
- **失效条件**：何时不再适用（`invalidated_when`）
- **证据强度**：`verification_status` / `confidence`
- **争议**：`contested_claims`
- **开放问题**：`open_questions`
- **技术演化**：优先记录**首次实现**和**当前最佳**

### 时间维度规则

不要求为每个指标穷尽完整时间轴；优先级如下：

1. `first_demonstration`
2. `best_demonstration`
3. `selected_milestones`（仅在关键拐点时补充）

---

## 8. 当前使用入口建议

目前仓库还没有正式的图形化入口，现阶段建议按成熟工具优先：

### 推荐入口 1：Claude Code / Copilot 交互式入口

适合：

- 导入新论文
- 讨论是否新建节点
- 审核 AI 提出的关系与字段
- 迭代知识结构原则

### 推荐入口 2：GitHub Issue + Actions 自动处理

适合：

- 标准化处理单篇论文
- 触发自动提取 YAML
- 用 PR 做专家审核

### 推荐入口 3：Obsidian 作为人类阅读视图

适合：

- 浏览知识条目
- 建立研究笔记
- 将结构化 YAML 与研究者个人笔记联动

> 当前建议优先：**结构化知识仍以 YAML 为主库，Obsidian 作为阅读/整理界面，而不是反过来。**

---

## 9. 节点治理与专家确认流程

前期不追求完全自动化“发明节点”，而强调**专家交互定节点原则**。

### 9.1 新节点提议流程

1. AI 导入论文或材料
2. AI 判断是否已有节点足够覆盖
3. 若疑似需要新节点：
   - 给出理由
   - 说明与现有节点的区别
   - 说明若不建会损失什么查询/推理能力
4. 由专家确认是否新建

目标是：在框架稳定后，绝大多数后续新增材料应主要表现为**补充已有节点内容**，而不是不断膨胀节点类型。

### 9.2 临时节点创建规则

当 AI 处理论文或材料时，若确需新节点但专家尚不可用，允许**临时创建**，但必须满足以下全部条件：

1. **标记**：在节点的 `note` 字段或独立的 `status` 字段中明确标注：
   ```yaml
   expert_review_status: pending  # pending | approved | rejected | needs_revision
   temporary_node: true
   temporary_reason: "简要说明为何已有节点不够覆盖"
   ```

2. **记录**：在同一 YAML 文件的 `meta` 区域或专门的 registry 文件中记录：
   - 临时节点 ID
   - 创建原因
   - 与现有节点的关系
   - 建议的长期处理方式（保留 / 合并 / 删除）

3. **使用限制**：
   - 临时节点可被其他节点引用（以 `note: "临时节点，待专家确认"` 标注）
   - 临时节点的 `confidence` 不得标为 `established`
   - 临时节点不应被用作 `BOUNDED-BY` 关系的 object，除非该限制关系本身也是临时的

### 9.3 专家确认流程

| 步骤 | 操作 | 工具 |
|------|------|------|
| 1. 提交提议 | AI 使用 `suggest-new-node` Issue 模板提交 | GitHub Issue |
| 2. 专家审阅 | 专家审查提议，检查独立价值、重叠风险、粒度 | Issue 评论 |
| 3. 决议 | 专家选择：接受 / 修改后接受 / 拒绝 / 合并到现有节点 | Issue 标签 |
| 4. 执行 | 根据决议更新 YAML：移除 `temporary_node` 标记，或执行合并/删除 | PR |

### 9.4 专家拒绝/修改处理

- **拒绝（合并）**：专家指定目标节点，AI 将临时节点内容合并到指定节点的相应字段中，然后删除临时节点
- **拒绝（删除）**：直接删除临时节点及其所有关系，更新引用该节点的其他条目
- **修改后接受**：专家指定修改内容（改名、调整层级、合并部分字段），AI 执行修改后移除临时标记
- **延期**：保留临时标记，等待更多证据或后续论文处理

### 9.5 Issue 模板

新节点提议使用 `.github/ISSUE_TEMPLATE/suggest-new-node.yml` 模板，包含：

- 节点名称、类型、父节点位置
- 为何已有节点不够
- 最小独立价值说明
- 与已有节点的关系
- 重叠/歧义风险
- 来源引用
- AI 草稿内容
- 专家决议栏

---

## 10. 维护建议

### 10.1 文档同步

每次更新 `SCHEMA.md` 后，至少同步检查：

- `README.md`
- `.github/copilot-instructions.md`
- `scripts/process_paper.py`
- workflow / issue template
- `papers/*.yaml` 头部 Schema 版本

### 10.2 条目维护

- 每条关系尽量有 `source.claim`
- 每个数值尽量有 `conditions`
- 不要把争议和开放问题只埋在 `note` 里
- 跨分支是否建立直接关系，以“是否真的有研究价值”为准，不强求形式统一

### 10.3 版本一致性

若未来 Schema 再升级，建议在 PR 中同时完成：

1. `SCHEMA.md` 变更
2. README 同步
3. Copilot / automation prompt 同步
4. 受影响 YAML 头部版本同步

---

## 11. 未来演进方向

1. 增强争议与开放问题的结构化管理
2. 强化“首次实现 / 当前最佳 / 关键拐点”的时间表达
3. 增加专家审阅支持的节点新增流程
4. 视需要补充 Obsidian/前端接口，但不改变 YAML 为主库的原则
5. 在跨分支比较确有价值时，再逐步增加更高层的共性原理组织

---

## 12. 进一步阅读

- Schema 规范：`/home/runner/work/sci-logic-kb/sci-logic-kb/SCHEMA.md`
- 队列与主题覆盖：`/home/runner/work/sci-logic-kb/sci-logic-kb/QUEUE.md`
- 本地处理规范：`/home/runner/work/sci-logic-kb/sci-logic-kb/CLAUDE.md`
