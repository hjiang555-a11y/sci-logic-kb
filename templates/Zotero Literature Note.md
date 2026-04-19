---
zotero_key: "{{zotero_key}}"
title: "{{title}}"
authors: "{{authors}}"
year: {{year}}
doi: "{{doi}}"
url: "{{url}}"
tags:
  - literature-note
  - "{{topic}}"
  - "{{subtopic}}"
status: "unprocessed"  # unprocessed, extracted, reviewed, integrated
sci_logic_nodes: []  # 关联的知识库节点ID列表
extracted_info: {{extracted_info_json}}  # AI提取的结构化信息
created: "{{date}}"
updated: "{{date}}"
---

# {{title}}

**Authors:** {{authors}}  
**Year:** {{year}}  
**DOI:** {{doi}}  
**Zotero Key:** `{{zotero_key}}`  
**Status:** {{status}}

## Abstract
{{abstract}}

## AI提取的核心信息
> 以下信息由AI自动提取，需要专家审核确认

### 研究问题
{{research_question}}

### 核心贡献
{{core_contributions}}

### 方法学
{{methodology}}

### 关键结果
{{key_results}}

### 限制因素
{{limitations}}

### 与知识库的关联
{{knowledge_base_connections}}

## 专家笔记
> 在此处添加您的分析、评论和见解

### 重要性评估
- [ ] 基础性工作
- [ ] 突破性进展  
- [ ] 技术优化
- [ ] 综述总结

### 质量评估
- [ ] 实验设计严谨
- [ ] 数据充分
- [ ] 结论合理
- [ ] 可重复性高

### 关联节点
- [[node-id-1]] - 关联描述
- [[node-id-2]] - 关联描述

## 参考文献
```bibtex
{{citation}}
```

## 处理历史
- {{date}}: 自动创建笔记
- {{date}}: AI信息提取完成
- {{date}}: 专家审核通过
- {{date}}: 集成到知识库节点 [[node-id]]

---

*此笔记基于模板 `templates/Zotero Literature Note.md` 生成*  
*使用Zotero-Obsidian智能集成系统*