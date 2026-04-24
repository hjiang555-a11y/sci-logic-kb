# 超稳激光论文v4.1升级测试任务

## 任务概述
将以下3篇论文从v3.2（仅metadata和entities）升级到v4.1（完整的principles/methods/metrics/relations推理链条）：

1. `topics/ultrastable-laser/papers/grote2016.yaml` - Zotero key: VM5MJ9B3
2. `topics/ultrastable-laser/papers/gobron2017.yaml` - Zotero key: HKYLIW8U  
3. `topics/ultrastable-laser/papers/thorpe2011.yaml` - Zotero key: Q2MRB267

## 工作流程
对每篇论文执行以下步骤：

### 1. 分析现有内容
- 阅读YAML文件的meta、entities、现有relations
- 理解论文的核心贡献和技术要点（从note字段获取）

### 2. 补充缺失部分
遵循v4.1 Schema规范，补充：

#### A. Principles（原理）
- 从论文中提取核心物理或工程原理
- 格式：id、name、statement、domain、subdomain、foundation、evidence、note
- id格式：pri.[简短描述]_[作者年份首字母]（如：pri.high_power_low_noise_pd_g16）

#### B. Methods（方法）
- 描述实现该原理的具体实验或工程方法
- 格式：id、name、procedure（步骤列表）、domain、subdomain、inputs、outputs、note
- id格式：meth.[简短描述]_[作者年份首字母]

#### C. Metrics（指标）
- 提取论文中报告的关键性能指标
- 格式：id、name、quantity、unit、demonstrated_value、conditions、measurement_method、significance、source_claim
- id格式：met.[简短描述]_[作者年份首字母]

#### D. Relations（关系）
- 建立entities、principles、methods、metrics之间的逻辑关系
- 至少包含：IMPLEMENTS（方法实现原理）、CHARACTERIZES（指标表征实体/方法/原理）、ENABLED-BY（实体/原理依赖其他实体）
- 使用已有的实体ID或新定义的ID
- id格式：rel.[作者年份首字母][两位数字]

### 3. 更新文件
- 使用patch工具或直接写入更新后的YAML
- 确保YAML语法正确

### 4. 更新SCHEMA.md
- 在SCHEMA.md中找到对应论文的行
- 将状态从"✅ 符合v3.2（首次提取）"更新为"✅ v4.1（补充principles/methods/metrics/relations推理链条）"

## 质量要求
1. **准确性**：基于论文实际内容，不杜撰
2. **完整性**：principles、methods、metrics、relations四部分都必须补充完整
3. **一致性**：ID命名遵循规范，关系逻辑清晰
4. **机器可读性**：YAML格式正确，便于后续程序处理

## 时间限制
每篇论文处理时间建议10-15分钟，总计30-45分钟。

## 报告要求
处理完成后，请提供：
1. 每篇论文的处理状态（成功/失败）
2. 补充的具体内容数量（如：新增2个principles、1个method、3个metrics、4个relations）
3. 遇到的任何问题或需要澄清的地方