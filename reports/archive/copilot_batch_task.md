# GitHub Copilot 批量任务：SCHEMA v4.1 论文升级

## 任务概述

**目标**：将测试批次中的8篇论文升级到SCHEMA v4.1规范。

**批次信息**：
- 批次文件：`test_batch_v1.json`
- 论文数量：8篇
- 任务类型：简单任务（只缺少1个主要字段）
- 预计时间：30-45分钟

**核心要求**：
1. 每篇论文补充缺失字段（主要是`methods`）
2. 确保符合v4.1规范
3. 更新SCHEMA.md中的状态标记
4. 保持YAML格式正确

## 详细步骤

### 步骤1：准备工作
1. 阅读指南：`v4.1_upgrade_guide.md`
2. 查看示例：参考`grote2016.yaml`（技术论文完整示例）
3. 检查批次：`test_batch_v1.json` 中的8篇论文

### 步骤2：处理单篇论文流程
对于每篇论文：

1. **读取文件**：打开对应的YAML文件
2. **分析现状**：
   - 检查已有字段（principles、metrics、relations）
   - 理解论文核心贡献（通过title和note字段）
3. **补充methods**：
   - 创建1-2个method条目
   - 使用格式：`meth.[描述性名称]_[作者年份缩写]`
   - 提供详细描述、输入、输出
   - 确保与existing principles和metrics逻辑一致
4. **扩展relations**（如有需要）：
   - 如果relations不足3个，补充至至少3个
   - 创建连接：method IMPLEMENTS principle
   - 创建连接：metric CHARACTERIZES method
5. **更新SCHEMA.md**：
   - 查找论文在SCHEMA.md中的行
   - 更新状态为"✅ v4.1（补充principles/methods/metrics/relations推理链条）"

### 步骤3：质量检查
处理完每篇论文后检查：
1. YAML语法是否正确（无解析错误）
2. method ID格式是否正确
3. method描述是否详细、具体
4. relations逻辑是否合理
5. SCHEMA.md更新是否正确

## 论文特定指导

### 1. webster2007.yaml
- **现状**：缺少methods，但有principles(1)、metrics(2)、relations(6)
- **核心**：Vibration insensitive optical cavity（振动不敏感光学腔）
- **建议**：补充振动隔离/抑制的具体方法

### 2. parke2025.yaml
- **现状**：缺少methods，但有principles(2)、metrics(2)、relations(5)
- **核心**：Three hundred microsecond optical cavity storage time and 10⁻⁷ active RAM cancellation
- **建议**：补充光腔存储时间延长和RAM抵消的具体方法

### 3. hafner2020.yaml
- **现状**：缺少methods，但有principles(1)、metrics(2)、relations(4)
- **核心**：Transportable interrogation laser system with an instability of mod σ_y = 3×10⁻¹⁶
- **建议**：补充可搬运询问激光系统的具体实现方法

### 4. olson2019.yaml
- **现状**：relations不足(2<3)，其他字段完整
- **核心**：Frequency‑comb‑based photonic‑microwave synthesis with 10⁻¹⁹ instability
- **建议**：扩展relations至至少3个，连接现有元素

### 5. kessler2012.yaml
- **现状**：缺少methods，但有principles(2)、metrics(3)、relations(9)
- **核心**：A sub‑40‑mHz‑linewidth laser based on a silicon single‑crystal optical cavity
- **建议**：补充硅单晶光腔激光器实现方法

### 6. sanjuan2019.yaml
- **现状**：缺少methods，但有principles(1)、metrics(1)、relations(3)
- **核心**：Sub‑millihertz linewidth laser via self‑injection locking to a crystalline‑coated cavity
- **建议**：补充自注入锁定到晶体涂层腔的具体方法

### 7. mohle2013.yaml
- **现状**：缺少methods，但有principles(1)、metrics(2)、relations(4)
- **核心**：Brillouin lasing in a monolithic CaF₂ whispering‑gallery‑mode resonator
- **建议**：补充单片CaF₂回音壁模式谐振器中布里渊激光的具体方法

### 8. belardi2015.yaml
- **现状**：缺少methods，但有principles(2)、metrics(2)、relations(6)
- **核心**：Tunable Brillouin laser in a microsphere resonator
- **建议**：补充微球谐振器中可调谐布里渊激光的具体方法

## 模板参考

### Method模板
```yaml
methods:
  - id: meth.[方法名称]_[年份缩写]
    name: "方法名称（年份）"
    description: >
      详细描述方法，包括关键技术步骤、实现方式。
      基于论文实际内容，避免空洞描述。
    inputs: ["输入1", "输入2"]
    outputs: ["输出1", "输出2"]
    note: "可选备注"
```

### Relation模板
```yaml
  - id: rel.[论文缩写][序号]
    subject: meth.[方法名称]_[年份缩写]
    predicate: IMPLEMENTS
    object: pri.[原理名称]_[年份缩写]
    confidence: established
    source: {zotero_key: "XXXXXXX", claim: "相关声明"}
    note: "方法实现原理"
```

## 时间分配建议

- 每篇论文：5-7分钟
- 总时间：40-60分钟
- 节奏：稳定推进，确保质量

## 验证

完成所有论文后：
1. 运行简单验证：`python -c "import yaml; yaml.safe_load(open('paper.yaml'))"`
2. 检查SCHEMA.md更新：搜索"v4.1"确认8篇论文状态已更新
3. 抽样检查：随机选择2-3篇论文，人工检查method质量

## 遇到问题

1. **不确定method内容**：阅读论文note字段，理解核心贡献
2. **ID命名冲突**：检查是否已有相似method，避免重复
3. **relations不足**：创建更多逻辑连接，如method-characterizes-metric等
4. **时间不足**：优先完成methods补充，relations可稍后补充

## 完成标志

1. 8篇论文的methods字段已补充完整
2. relations达到最少数量要求（≥3）
3. SCHEMA.md中8篇论文状态已更新为v4.1
4. 所有YAML文件语法正确

---
**任务分配**：GitHub Copilot (使用Claude Opus 4.6)
**监督**：Hermes Agent
**开始时间**：立即
**报告**：完成后提供简要总结