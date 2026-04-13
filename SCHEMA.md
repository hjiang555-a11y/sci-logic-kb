# sci-logic-kb YAML 知识提取模式文档

## 核心设计原则

### 知识库定位

符号主义结构化知识库，服务时间频率计量科研。
- **不是** 向量知识库（统计模式匹配）
- **支持** 逻辑推理和精确路径查询
- 节点信息需足够丰富，使推理链上每步都有明确语义

### 三层结构

```
原始素材（Zotero PDF）→ 知识图谱（YAML，本仓库）→ Schema（SCHEMA.md，CLAUDE.md）
```

### 超稳激光的三大技术分支

```
超稳激光
├── 分支1：频率参考部件（决定稳定度的核心器件）
│   ├── 刚性 FP 腔（ULE/Zerodur 间隔物 + 高精细度腔镜）
│   │   ├── 内禀极限：热噪声（布朗运动，Numata 2004）
│   │   └── 外部噪声：振动、温漂（需隔振平台、温控）
│   └── 光纤干涉仪（延迟线参考，Jiang 2010）
│       ├── 内禀极限：热噪声（光纤热相位噪声）
│       └── 扫频极限：Rayleigh 背向散射
├── 分支2：频率误差探测与反馈方法
│   ├── PDH 锁频（Drever 1983）— 对应 FP 腔
│   ├── Tilt Locking（Shaddock 1999）— 对应 FP 腔
│   └── 光纤延迟线锁频（Jiang 2010）— 对应光纤干涉仪
└── 分支3：反馈执行部件（与方法并行，独立设计）
    ├── EOM（电光调制器，电场调频）
    ├── AOM（声光调制器，声场调频）
    └── PZT（压电陶瓷，机械调腔长）
```

---

## 五类节点（固定）

| 代码前缀 | 类型 | 说明 | 示例 |
|---------|------|------|------|
| `ent.` | 技术实体 | 具体装置/系统/部件 | FP 腔、分割探测器、PZT |
| `pri.` | 原理 | 物理/数学原理，解释"为什么"，有适用条件 | 布朗热噪声、Gouy 相位鉴别 |
| `meth.` | 方法 | 解决问题的技术手段，连接原理与实体 | PDH 锁频、Tilt Locking |
| `met.` | 指标/特性 | 可量化的性能指标，包括数值与条件 | 激光线宽、Allan 偏差 |
| `src.` | 素材 | 论文/标准/教材（通过 `source` 字段引用，不单建节点）|  |

---

## 七种关系类型（固定）

| 谓词 | 方向语义 | 典型用法 |
|------|---------|---------|
| `PART-OF` | subject 是 object 的组成部分 | `ent.mirror PART-OF ent.fp_cavity` |
| `CHARACTERIZED-BY` | subject 的性质由 object 刻画 | `ent.fp_cavity CHARACTERIZED-BY met.finesse` |
| `OPERATIONALIZED-AS` | 指标通过某方法实现/操控 | `met.linewidth OPERATIONALIZED-AS meth.pdh` |
| `GOVERNED-BY` | subject 的行为受 object 支配 | `meth.pdh GOVERNED-BY pri.heterodyne_detection` |
| `INFLUENCES` | subject 对 object 有因果影响（方向可定性） | `pri.thermal_noise INFLUENCES met.linewidth` |
| `SUPPORTED-BY` | subject 被 object 支持/验证 | `meth.tilt SUPPORTED-BY src.shaddock1999` |
| `CHALLENGED-BY` | subject 被 object 质疑/反驳 | 用于争议性关系 |
| `EQUIVALENT-IN-CONTEXT` | 在特定条件下两节点等价 | 物理同源性连接 |

---

## YAML 文件结构（模板）

```yaml
# {Author} {Year} — {简述}
# 提取者：Claude（AI草稿，待专家确认）
# 提取日期：YYYY-MM-DD

meta:
  zotero_key: "{8位Zotero KEY}"
  source_type: technical_paper   # technical_paper | review | textbook | standard
  reliability: medium            # high | medium | low
  title: "完整论文标题"
  year: YYYY
  first_author: "姓氏"
  journal: "期刊名"
  volume: 数字
  pages: "起-止"
  doi: "10.xxxx/xxxxx"
  note: "一句话说明本文核心贡献和在知识图谱中的位置"

entities:
  - id: ent.{snake_case_name}       # 全局唯一，跨文件引用时使用此 ID
    name: "中文名称"
    aliases: ["英文名", "别称"]
    function: >
      该实体的核心功能（1-3 句）。
      聚焦于在"超稳激光"语境中的作用。
    parameters:                      # 可选，列出关键参数
      key_param: "值或描述"
    note: "补充说明（可选）"

principles:
  - id: pri.{snake_case_name}
    name: "原理名称（中文）"
    statement: >
      原理的精确表述（2-5 句）。
      需包含：物理机制 + 数学关系（如有）+ 适用条件。
    domain: "所属领域"
    formula: "核心公式（可选）"
    key_insight: "一句话核心洞见（可选）"
    conditions: "适用条件"
    applicable_when: "何时适用"
    source_claim: >
      "原文中的关键论断（引号内为原文，用于溯源）"

methods:
  - id: meth.{snake_case_name}
    name: "方法名称"
    full_name: "完整名称（可选）"
    steps_summary: >
      步骤摘要（流程箭头格式）：
      步骤1 → 步骤2 → 步骤3 → 输出
    required_hardware:               # 列出该方法依赖的实体 ID
      - ent.fp_cavity_reference
      - ent.rf_phase_modulator
    advantages:
      - "优势1"
    disadvantages:
      - "劣势1"
    conditions:
      - "适用条件1"
    source_claim: >
      "原文关键论断"

metrics:
  - id: met.{snake_case_name}
    name: "指标名称（中文）"
    unit: "单位"
    description: "指标的物理意义（1-2 句）"
    demonstrated_value:
      value: "数值或范围"
      conditions: "测量条件"
      confidence: established        # established | likely | contested
      source: {zotero_key: "KEY", claim: "原文论断"}
    comparison:                      # 可选，横向对比
      method_a: "值A"
      method_b: "值B"

relations:
  - id: rel.{X##}                   # X=首字母缩写，##=两位数序号，如 rel.D01
    subject: {node_id}
    predicate: {PREDICATE_TYPE}
    object: {node_id}
    confidence: established          # established | likely | contested
    source: {zotero_key: "KEY", claim: "原文支撑"}
    conditions: "成立条件（可为 null）"
    speculative: false               # true 时需加猜测说明
    note: "跨文件引用时说明来源文件（可选）"
```

---

## 提取质量要求

### 必须做到

1. **节点 ID 全局唯一**：跨文件引用时使用相同 ID（如 `pri.off_resonance_reference_light` 在 shaddock1999.yaml 中定义，其他文件可直接引用）
2. **关系有明确溯源**：每条 `relation` 必须有 `source.claim`（原文原句或核心论断）
3. **数值有条件**：`demonstrated_value` 中的 `value` 必须配有 `conditions`（测量条件）
4. **适用性有边界**：原理节点必须有 `conditions` 或 `applicable_when`
5. **指标置信度标注**：区分 `established`（文中明确给出）、`likely`（推断）、`contested`（有争议）

### 避免

- 不要创建没有任何关系连接的孤立节点
- 不要把"方法"建为"实体"（PDH 是方法 `meth`，不是实体 `ent`）
- 不要在单篇论文中重复定义已有节点——改用跨文件引用（注明来源文件）
- 不要把设备组合（整个激光系统）建为单一实体——分解为部件

### 跨文件引用规范

若某节点已在其他 YAML 中定义，在新文件的 relations 中可直接引用其 ID，但需在 `note` 字段注明：
```yaml
object: pri.off_resonance_reference_light   # 定义在 shaddock1999.yaml
note: "跨文件引用，shaddock1999.yaml 中的元原理"
```

---

## 已处理论文（勿重复）

| 文件 | Zotero Key | 论文 |
|------|-----------|------|
| `drever1983.yaml` | 694DPR5F | Drever 1983 — PDH 技术 |
| `young1999.yaml` | EGAZKLXR | Young 1999 — 亚赫兹线宽可见激光 |
| `shaddock1999.yaml` | S5PX7GHC | Shaddock 1999 — Tilt Locking |
| `numata2004.yaml` | VDXBPUQB | Numata 2004 — FP 腔热噪声极限 |
| `jiang2010.yaml` | T8JR8IJ7 | Jiang 2010 — 光纤干涉仪可捷变激光 |
