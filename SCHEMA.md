# sci-logic-kb 原子推理架构规范 (S-ARK)

> **版本**：v5.0 (Atomic Reasoning Architecture)
> **核心哲学**：证据驱动 $\to$ 逻辑分解 $\to$ 共识达成。
> **目标**：将知识库从“论文存档”升级为“物理边界推理引擎”。

---

## 一、 三层知识架构 (The 3-Layer Model)

系统将所有知识解耦为三个逻辑层，禁止跨层直接修改，必须通过定义的同步流转。

### 1. 证据层 (Evidence Layer) —— 【不可篡改的原件库】
- **存储路径**：`/data/sci-logic-kb/data/evidence/`
- **定义**：直接从 PDF 提取的原始 Claim、数值和结论。
- **唯一性**：每个证据节点必须绑定具体的论文来源（Paper ID + Quote）。
- **原则**：只记录“论文 A 说了 X”，不记录“事实是 X”。

### 2. 逻辑层 (Logic Layer) —— 【物理建模蓝图】
- **存储路径**：`/data/sci-logic-kb/data/logic/`
- **定义**：专家定义的物理分解图（ la Decomposition Graph）。
- **内容**：
    - **原子节点**：独立、朴实的物理原件（原理、指标、材料、方法）。
    - **逻辑链条 (Metric Chains)**：定义顶层指标是如何被底层因素 $\text{BOUNDED-BY}$ 或 $\text{DETERMINED-BY}$ 的拓扑结构。
- **原则**：独立于具体论文，描述物理实在的通用因果关系。

### 3. 共识层 (Consensus Layer) —— 【当前技术真值】
- **存储路径**：`/data/sci-logic-kb/data/consensus/`
- **定义**：证据层数据填充进逻辑层链条后，经专家校准得出的最终结论。
- **内容**：当前全球性能极限、已知瓶颈节点、已证实的物理路径。
- **原则**：这是用户查询的最终入口，必须是高度精准且经过校准的。

---

## 二、 原子节点定义 (Atomic Node Specification)

所有节点必须满足：**独立完备且朴实**。即脱离上下文后仍能清晰定义自身。

### 1. 节点类型与核心字段

| 类型 | 核心职责 | 关键字段 (Required) | 示例 |
| :--- | :--- | :--- | :--- |
| **原理 (Principle)** | 定义物理规律/限制 | `id`, `formula`, `conditions`, `scope` | 布朗热噪声限制 |
| **指标 (Metric)** | 定义可量化的性能 | `id`, `unit`, `global_record`, `conditions` | 频率稳定性 $\sigma_y$ |
| **材料 (Material)** | 定义物理实体的属性 | `id`, `specs`, `source_material` | ULE 玻璃 |
| **方法 (Method)** | 定义实现路径 | `id`, `procedure`, `expected_effect` | PDH 锁相技术 |

### 2. 通用元数据 (Common Metadata)
- `id`: 语义化唯一 ID (例如 `pri.brownian_noise`)。
- `definition`: 朴实、直接的物理语言描述（不含外部依赖）。
- `status`: `Determined` (已定论) $\mid$ `Blank` (留白/待填) $\mid$ `Contested` (有争议)。
- `evidence_refs`: 指向证据层 $\text{EvidenceNode}$ 的引用列表。
- `inputs`: 成立该节点所需的依赖原件。
- `outputs`: 该节点能为上层链条提供的贡献。

---

## 三、 指标链条与拓扑逻辑 (Metric Chain Topology)

指标链条不再是 emergent 的路径，而是**显式管理**的实体。

### 1. 关系谓词
- $\text{DETERMINED-BY}$ (由...决定)：强因果关系，通常伴随数学公式。
- $\text{BOUNDED-BY}$ (受限于)：定义性能上限的瓶颈关系。
- $\text{IMPLEMENTS}$ (实现)：方法 $\to$ 原理。
- $\text{SUPPORTED-BY}$ (由...支撑)：节点 $\to$ 证据。

### 2. 分解图逻辑
一个顶层指标 (Top-level Metric) 的分解路径如下：
$$\text{Metric} \xrightarrow{\text{BOUNDED-BY}} \text{Critical Factor} \xrightarrow{\text{DETERMINED-BY}} \text{Physics Principle} \xrightarrow{\text{ASSOCIATED-WITH}} \text{Material/Method}$$

---

## 四、 联动更新机制 (Linked Update Mechanism)

为了防止知识漂移，系统采用**依赖触发 $\to$ 局部审查**机制。

### 1. 影响半径 (Impact Radius)
每个节点维护一个反向依赖列表。当节点 $N$ 的 $\text{value\_range}$ 或 $\text{status}$ 发生变更时：
1. 触发所有依赖于 $N$ 的上层节点。
2. 将所有受影响的逻辑链条标记为 `Needs-Review` (需要审查)。
3. 在共识层中，受影响的顶层指标显示为 `Under-Calibration` (校准中)。

### 2. 升级流水线 (Sync Pipeline)
$\text{Evidence} \xrightarrow{\text{Trigger}} \text{Logic Node} \xrightarrow{\text{Update}} \text{Metric Chain} \xrightarrow{\text{Propagation}} \text{Consensus}$

---

## 五、 角色接口规范

### 1. 专家接口 (Maintenance Interface)
- **操作**：定义逻辑链 $\to$ 审核证据 $\to$ 校准共识 $\to$ 处理联动审查。
- **权限**：唯一拥有修改 `Logic Layer` 和 `Consensus Layer` 的权限。

### 2. 用户接口 (Reasoning Interface)
- **操作**：查询指标 $\to$ 展开分解图 $\to$ 追踪瓶颈 $\to$ 辅助写作。
- **权限**：只读访问 `Consensus Layer` 和 `Logic Layer`。

---

**版本记录**：
- v5.0: 引入三层原子架构，定义联动更新机制。

**关联标准**：声明-证据操作标准见 [`docs/CLAIM_EVIDENCE_STANDARD.md`](docs/CLAIM_EVIDENCE_STANDARD.md)。
