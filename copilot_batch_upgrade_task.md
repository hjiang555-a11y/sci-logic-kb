# 批量升级任务：10篇超稳激光论文从v3.2到v4.1

## 任务概述
将以下10篇超稳激光主题论文从Schema v3.2升级到v4.1：

1. `zhang2017.yaml` (Zotero key: N9AGEQ8S) - PDF: `pdfs/zhang2017.pdf`
2. `jeon2025.yaml` (Zotero key: SBPRDKPV) - PDF: `pdfs/jeon2025.pdf`
3. `herbers2022.yaml` (Zotero key: NU79W75P) - PDF: `pdfs/herbers2022.pdf`
4. `kim2008.yaml` (Zotero key: H5YVF5AR) - PDF: `pdfs/kim2008.pdf`
5. `belardi2015.yaml` (Zotero key: 2F3PD62T) - PDF: `pdfs/belardi2015.pdf`
6. `wu2016.yaml` (Zotero key: PZGR9S7S) - PDF: `pdfs/wu2016.pdf`
7. `marchio2018.yaml` (Zotero key: LCMWCIWB) - PDF: `pdfs/marchio2018.pdf`
8. `steinlechner2018.yaml` (Zotero key: L6KKLLSR) - PDF: `pdfs/steinlechner2018.pdf`
9. `tao2018.yaml` (Zotero key: U4Z95559) - PDF: `pdfs/tao2018.pdf`
10. `mohle2013.yaml` (Zotero key: 8MNIBZEW) - PDF: `pdfs/mohle2013.pdf`

## 升级目标
为每篇论文补充或完善以下部分，形成完整的推理链条：
1. **原理 (principles)** - 如果为空，从PDF中提取核心物理原理；如果已有，检查完整性
2. **方法 (methods)** - 补充实验方法或理论方法，建立从原理到实现的桥梁
3. **指标 (metrics)** - 补充量化指标，区分技术论文（实测值）与综述论文（理论参数）
4. **关系 (relations)** - 建立实体、原理、方法、指标之间的逻辑关系（CHARACTERIZED-BY, ENABLED-BY, BOUNDED-BY等）

## 具体步骤（每篇论文）

### 1. 预处理
- 读取现有YAML文件，了解当前状态
- 查阅PDF文件，提取关键信息
- 根据`meta.source_type`区分技术论文(`technical_paper`)和综述论文(`review_paper`)

### 2. 补充原理 (principles)
- 每篇论文至少1个原理节点，ID格式：`pri.[简短描述]_[作者年份后缀]`
- 原理节点包含：`description`, `conditions`, `preconditions`, `assumptions`
- 对于综述论文：原理可能是理论框架或分类体系
- 对于技术论文：原理是实验背后的物理机制

### 3. 补充方法 (methods)
- 每篇论文至少1个方法节点，ID格式：`meth.[简短描述]_[作者年份后缀]`
- 方法节点包含：`description`, `inputs`, `outputs`, `steps`, `limitations`
- 方法应连接原理和实体/指标

### 4. 补充指标 (metrics)
- 每篇论文至少2个指标节点，ID格式：`met.[简短描述]_[作者年份后缀]`
- 指标节点包含：`quantity`, `value`, `unit`, `conditions`, `uncertainty`
- 技术论文：使用实测值；综述论文：使用理论参数或典型范围

### 5. 补充关系 (relations)
- 每篇论文至少3-5个关系，ID格式：`rel.[论文代码]_[两位序号]`
- 关系类型：`CHARACTERIZED-BY`, `ENABLED-BY`, `BOUNDED-BY`, `FOLLOWS-FROM`, `REFINES`等
- 每个关系必须包含：`subject`, `predicate`, `object`, `confidence`, `source`, `conditions`
- 对于`BOUNDED-BY`关系，鼓励包含`breakthrough_paths`字段

### 6. 跨文件引用
- 检查是否可复用已有节点（搜索现有YAML中的节点ID）
- 优先复用已有节点，避免重复创建
- 新创建节点需保证全局唯一性

### 7. 更新文件
- 使用`patch`工具进行精确编辑，避免破坏现有内容
- 保留原始文件结构和注释
- 在文件头部更新Schema版本注释（如`# Schema版本：v4.1`）

### 8. 更新SCHEMA.md状态
- 将SCHEMA.md中对应论文的状态从"✅ 符合v3.2（首次提取）"更新为"✅ v4.1（补充principles/methods/metrics/relations推理链条）"
- 使用`patch`工具精确更新

## 质量要求
1. **准确性**：所有提取内容必须有PDF原文支持，在`source.claim`中注明具体引用
2. **一致性**：节点ID命名遵循项目约定，关系逻辑连贯
3. **完整性**：四大部分（原理、方法、指标、关系）均需充实
4. **可读性**：YAML结构清晰，注释恰当

## 输出
- 每篇论文升级后的YAML文件
- SCHEMA.md中10篇论文的状态更新
- 处理总结报告（成功/失败篇数，主要补充内容）

## 工作目录
当前目录：`/home/hjian/sci-logic-kb/sci-logic-kb`
论文路径：`topics/ultrastable-laser/papers/`
PDF路径：`pdfs/`

## 工具限制
- 使用`read_file`读取YAML和PDF文本
- 使用`patch`进行文件编辑
- 使用`search_files`查找现有节点
- 使用`terminal`执行简单命令（如grep）
- 避免直接调用Zotero API

## 时间预算
每篇论文预计15-20分钟，总计3-4小时。

## 开始处理
请按论文列表顺序处理，每完成一篇后立即更新SCHEMA.md状态，避免遗漏。