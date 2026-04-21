# GitHub Copilot 任务说明 — sci-logic-kb 时间频率计量知识提取

> **最高规则**：若本文件与 `SCHEMA.md` 冲突，**一律以 `SCHEMA.md` 为准**。

> **当前 Schema 版本**：v4.1（2026-04-18）

---

## 1. 项目定位

本仓库是一个**面向科研探索的结构化知识库**，服务**时间频率计量**全领域。当前已建主专题：超稳激光；已初建专题：光学频率梳、频率标准（合并光钟+微波标准）、时间标尺与钟组。需要注意：这些初建专题当前主要由框架型综述/路线图条目建立顶层架构。专题体系详见 `TOPICS.md`。

核心问题：

1. 当前性能极限在哪？
2. 为什么卡在这里？
3. 怎样突破？
4. 在什么条件下成立、失效、存在争议，或仍是开放问题？

知识以 `topics/<topic>/papers/*.yaml` 保存，不做纯文本摘要堆积。当前超稳激光仍是论文最多的主专题，论文位于 `topics/ultrastable-laser/papers/`。

---

## 2. 提取时的总体原则

### 2.1 人类认知优先

- 节点应能独立回答有意义的问题
- 关系应体现机制、限制、条件、竞争、层级推导
- 不要为了“图谱好看”制造没有独立价值的节点

### 2.2 Source of Truth

提取、重整、修复时，按以下优先级解释规则：

1. `SCHEMA.md`
2. `README.md`
3. 本文件
4. 既有 YAML 条目中的历史写法

### 2.3 跨分支处理原则

如果两个分支都受“同名限制”影响，但**模型、调用条件、接口、工程意义明显不同**，应保留为各自独立的完整原理节点，不强行交叉合并。

例：
- FP 腔热噪声原理
- 光纤延迟线热噪声原理

只有在跨分支比较**确有研究价值**时，才补充显式连接。

---

## 3. 当前推荐的知识表达重点

除基础实体/原理/方法/指标外，优先显式提取以下维度：

1. **限制链**：`BOUNDED-BY`
2. **突破路径**：`breakthrough_paths`
3. **外围条件接口**：`CONDITIONED-BY`
4. **结构化前提**：`preconditions`
5. **失效条件**：`invalidated_when`
6. **争议**：`contested_claims`
7. **开放问题**：`open_questions`
8. **技术演化时间点**：优先记录
   - `historical_landmarks.first_demonstration`
   - `historical_landmarks.best_demonstration`
   - 必要时再补 `selected_milestones`

> 时间维度遵循：**先记首次，再记最佳，其余关键拐点按需补充。**


    
### 3.1 问题-解决方案-结果推理链条（新增重点）
为强化知识库的科研推理能力，提取时需显式构建以下推理链条：

**1. 问题识别**
- 通过 `BOUNDED-BY` 关系清晰定义技术限制
- 通过 `open_questions` 字段记录未解问题
- 通过 `contested_claims` 字段记录有争议的论断

**2. 解决方案追踪**
- 通过 `breakthrough_paths` 字段记录已验证或待验证的突破路径
- 每个突破路径必须包含：
  - `direction`: 指向 `pri.*` 或 `meth.*` 节点（不得引用 `ent.*`）
  - `expected_gain`: 预期性能提升描述
  - `status`: `proposed`（待验证）、`demonstrated`（已验证）、`refuted`（已证伪）
  - `source`: 引用原文论断
  - 可选的 `note` 字段提供补充说明

**3. 结果验证**
- 通过 `verification_status`（observed/calculated/inferred）记录证据类型
- 通过 `temporal_role`（proposes/validates/refutes/extends）记录论文在知识演进中的角色
- 通过 `breakthrough_paths[*].status` 记录解决方案的验证状态

**4. 证据溯源**
- 每个重要论断必须有 `source` 字段引用原文
- 跨论文验证需在 `note` 中说明证据链

**提取优先级**：优先确保每个 `BOUNDED-BY` 关系都配有相应的 `breakthrough_paths`，形成完整的问题-解决方案对。---

## 4. 节点与关系速查

### 4.1 节点前缀

| 前缀 | 类型 |
|------|------|
| `ent.` | 技术实体 |
| `pri.` | 原理 |
| `meth.` | 方法 |
| `met.` | 指标 |
| `rel.` | 关系 |

### 4.2 关系类型

| 谓词 | 用途 | 典型例子 |
|------|------|---------|
| `PART-OF` | 组件归属 | `ent.mirror_substrate PART-OF ent.fp_cavity_system` |
| `CHARACTERIZED-BY` | 实体→指标 | `ent.fp_cavity_system CHARACTERIZED-BY met.laser_linewidth` |
| `OPERATIONALIZED-AS` | 指标→方法 | `met.laser_linewidth OPERATIONALIZED-AS meth.pdh_locking` |
| `ENABLED-BY` | 方法→机制原理 | `meth.pdh_locking ENABLED-BY pri.pdh_heterodyne_detection` |
| `BOUNDED-BY` | 任意→限制原理 | `ent.fp_cavity_system BOUNDED-BY pri.brownian_thermal_noise_fdt` |
| `DERIVED-FROM` | 原理层级 | `pri.xxx DERIVED-FROM pri.yyy` |
| `CONDITIONED-BY` | 实体→外围条件 | `ent.fp_cavity_system CONDITIONED-BY ent.vibration_environment` |
| `COMPETES-WITH` | 同层级并列方案/方法 | `ent.fp_cavity_system COMPETES-WITH ent.fiber_interferometer` |

**禁止使用**：
- `GOVERNED-BY`
- `EQUIVALENT-IN-CONTEXT`
- `SUPPORTED-BY`
- `BREAKTHROUGH-VIA`

---

## 5. 新增节点的判断原则

仅在以下情况新建节点：

- 可以独立回答一个重要问题
- 拥有独立设计选择空间
- 会被多篇论文复用
- 拥有独立的限制链 / 证据链 / 竞争关系

若某内容只是父节点某个字段的展开，应并回父节点。
若某节点已经过重，且内部存在多个可复用机制/部件/争议点，则允许向下继续拆分。

如 AI 认为需要新节点，但不确定，应输出建议理由，交由专家确认。

---

## 6. 处理新论文时的步骤

1. 阅读摘要、引言、方法、结果、讨论
2. 查询 `papers/` 中已有核心节点，优先复用
3. 提取：
   - entities
   - principles
   - methods
   - metrics
   - relations
4. 重点追问每个关键指标：
   - 被什么限制？
   - 该限制当前是否活跃？
   - 有何突破路径？
   - 有什么外部条件接口？
   - 是否有争议或开放问题？
   - 是否值得记录首次/最佳时间点？

若论文本身的贡献是**专题框架定义**而非具体技术点（如综述、路线图、教科书章节），应：
- 在 `meta.contribution_type` 中标记为 `framework`
- 主要定义 Level 0/1 顶层实体、tier: meta/domain 原理与跨专题接口关系
- 避免把具体实验系统的 Level 2 参数实例写成该框架文档的主内容

**贡献分级（v4.4）**：`meta.contribution_type` 使用三档规范（详见 [SCHEMA.md §9.1](../SCHEMA.md)）：
- `breakthrough`：打破指标记录 / 提出新原理 / 证伪旧论断（需补完整限制链 + `breakthrough_paths`）
- `evidence`：在已有节点上提供新数据点、复现、工程改进（**默认档位**；不强求新增 pri.* 或 `breakthrough_paths`，允许 orphan）
- `framework`：综述 / 路线图 / 教科书章节（如上）

---

## 7. 质量要求

必须做到：

- 全局唯一 ID
- 每条关键 relation 尽量有 `source.claim`
- 每个关键数值尽量有 `conditions`
- 原理节点至少有 `conditions`，鼓励补 `preconditions` / `invalidated_when`
- `BOUNDED-BY` 关系结构完整
- 若论文明确提出争议或未解问题，不只写进 `note`
- 若需表达时间演化，优先填写首次与当前最佳

---

## 8. 使用入口建议

目前没有正式前端，建议优先使用成熟入口：

1. **Claude Code / Copilot 对话式入口**：适合导入材料、讨论节点边界
2. **GitHub Issue + Actions + PR**：适合标准化处理单篇论文
3. **Obsidian**：适合作为阅读与研究笔记界面

YAML 仍是主库；Obsidian 等工具是阅读层，而不是事实真源。

---

## 9. 当前文档维护要求

每次 Schema 更新后，至少同步检查：

- `/home/runner/work/sci-logic-kb/sci-logic-kb/README.md`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/.github/copilot-instructions.md`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/scripts/` 下自动化脚本与辅助工具
- `/home/runner/work/sci-logic-kb/sci-logic-kb/.github/workflows/process-paper.yml`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/TOPICS.md`
- `/home/runner/work/sci-logic-kb/sci-logic-kb/topics/*/papers/*.yaml` 头部版本注释
