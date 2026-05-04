# Sci-Logic-KB v5: 证据驱动的物理推理知识库设计规格书

## 1. 项目概述
`sci-logic-kb v5` 旨在构建一个服务于时间频率计量领域的专家级符号知识库。其核心目标是通过构建高度结构化的“物理底层图谱”，通过证据链支撑的逻辑推理，回答关于性能极限、技术边界及瓶颈分析的深层问题。

### 1.1 核心理念
- **基于有证据的推理**：所有结论必须可追溯至原始证据（PDF页码、公式、实验数据）。
- **结构化指标链条**：采用复杂有向图结构，描述技术指标间的制约关系，符合物理实在。
- **物理底层粒度**：节点必须拆解至底层物理量（而非宏观概念），以支持精确量级推理。
- **专家中心化**：系统通过“建议-选择-微调”模式，减轻专家的录入负担，强化其决策权重。

---

## 2. 系统架构设计

系统采用分层解耦架构，确保原始证据的不可变性与推理逻辑的灵活性。

### 2.1 证据层 (Evidence Layer) - 基石
- **目标**：存储不可变的原始证据碎片。
- **核心对象**：`EvidenceFragment`
- **内容**：原始文本块、LaTeX 公式、数值数据、PDF 坐标、页码、文档 ID。
- **原则**：只读，不可变。

### 2.2 逻辑推理层 (Logic & Reasoning Layer) - 图谱
- **目标**：构建可计算、可校验的底层物理图谱。
- **核心对象**：`PhysicalNode` (原子节点), `IndicatorChain` (制约关系)。
- **结构**：多对一有向图。一个高性能指标由多个底层物理量共同制约。
- **原则**：每个节点必须关联至少一个证据 ID；支持符号推理与量级计算。

### 2.3 专家接口层 (Expert Interface Layer) - 控制平面
- **目标**：提供高效的“选择-修改”工作台。
- **交互模式**：`Proposal` $\rightarrow$ `Selection` $\rightarrow$ `Tweak`。
- **功能**：审核候选链条、补全经验知识（Expert-Override）、分析边界瓶颈。

### 2.4 消费层 (Consumption Layer) - 访问接口
- **目标**：将专家图谱转化为用户可理解的知识答案。
- **视图投影**：
    - **摘要视图**：直接结果与瓶颈识别。
    - **证据视图**：结论 $\rightarrow$ 链条 $\rightarrow$ 公式 $\rightarrow$ PDF 截图。
    - **结构化 API**：JSON 格式的路径查询。

---

## 3. 数据结构定义

### 3.1 物理节点 (PhysicalNode)
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `UID` | String | 唯一标识符 |
| `Name` | String | 物理量名称 (如：频率漂移) |
| `Symbol` | String | 标准符号 (如：$\delta f/f$) |
| `Dimension`| Enum | 量纲 (来自标准库) |
| `Unit` | String | 单位 |
| `Value_Range`| Range | $[Min, Max]$ 预期量级区间 |
| `Status` | Enum | `Candidate` / `Confirmed` / `Expert-Fixed` |
| `Evidence_Refs`| List[ID] | 关联的证据碎片 ID 列表 |

### 3.2 指标链条 (IndicatorChain)
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Sources` | List[UID] | 前置制约节点的 ID 列表 |
| `Target` | UID | 被制约的目标节点 ID |
| `Type` | Enum | `Direct-Limit` / `Product-Sum` / `Functional` |
| `Formula` | String | 数学关系式/公式 ID |
| `Coefficient`| Float/Expr| 权重或系数 |
| `Is_Bottleneck`| Boolean | 是否为当前瓶颈 (系统自动标记/专家确认) |

### 3.3 证据碎片 (EvidenceFragment)
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `Frag_ID` | String | 碎片唯一 ID |
| `Doc_Meta` | Object | {Doc_ID, Page, Section, Coordinate} |
| `Content` | Mixed | 文本 / LaTeX / JSON 表格 |
| `Confidence` | Float | LLM 提取时的置信度 |

---

## 4. 自动化入库与校验流程

### 4.1 流水线 (Pipeline)
1. **粗提取**：LLM 扫描 PDF $\rightarrow$ 生成 `EvidenceFragment`。
2. **符号化**：NER 识别物理量 $\rightarrow$ 匹配量纲库 $\rightarrow$ 构建候选 `PhysicalNode` $\rightarrow$ 推演候选 `IndicatorChain`。
3. **预校验** $\rightarrow$ **专家审核** $\rightarrow$ **正式入库**。

### 4.2 校验机制
- **逻辑一致性校验 (A)**：
    - **环路检测**：禁止 $A \rightarrow B \rightarrow A$。
    - **连通性检查**：检测断链情况，确保目标指标有完备的支撑路径。
- **量级合法性校验 (C)**：
    - **区间比对**：提取值与物理常数/理论极限对比，识别量级异常。

### 4.3 专家审核工作流
- **差异高亮**：低置信度、量级异常、逻辑存疑的点在界面高亮。
- **操作路径**：`候选方案` $\rightarrow$ `[一键确认]` 或 `[快速修改数值]` 或 `[调整链条结构]`。

---

## 5. 兼容性与扩展性
- **API 兼容**：消费层通过语义 API (如 `get_limit`) 屏蔽底层图谱细节。
- **知识演进**：支持在证据层外直接注入专家经验节点，优先级高于 PDF 提取节点。

## 6. 知识演进与自进化机制 (Knowledge Evolution)
为了使知识库在实际应用中动态升级，引入“查询-反馈-修正”的闭环机制。

### 6.1 交互式反馈采集
- **对话即采集**：将专家的查询对话视为潜在的知识补丁来源。
- **差异捕捉**：当专家在对话中对系统的推理结论提出质疑或修正时，系统自动将其转化为一个 `UpdateProposal`。

### 6.2 知识升级接口 (Upgrade Interface)
- **异步提案池**：建立一个暂存区，存储所有来自对话的修正建议。
- **审核流程**：专家可通过一个专门的“知识升级”入口，以“选择-确认”模式批量审核提案 $\rightarrow$ 一键同步至主图谱。
- **闭环路径**：`用户查询` $\rightarrow$ `发现偏差` $\rightarrow$ `对话纠正` $\rightarrow$ `生成提案` $\rightarrow$ `审核确认` $\rightarrow$ `同步更新`。

