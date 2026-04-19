# Zotero与Obsidian集成方案

## 当前状态检查

### 1. Zotero配置
- ✅ Zotero本地API已启用，端口23119
- ✅ 用户ID：19944378
- ✅ API可正常访问（已测试）
- ✅ 文献数据库包含光学频率梳等论文

### 2. Obsidian配置
- ✅ Obsidian Local REST API已启用，端口27124
- ✅ API密钥已配置
- ✅ `obsidian-zotero-desktop-connector`插件已安装
- ✅ Zotero文献笔记模板已配置
- ✅ 文献导入目录：`LiteratureNotes/`

### 3. sci-logic-kb知识库
- ✅ YAML文件包含`meta.zotero_key`字段
- ✅ 已建立Zotero键与知识库节点的关联
- ✅ 核心文档（SCHEMA.md等）已同步到Obsidian

## 已完成的集成演示

### 成功测试：
1. **从Zotero API获取文献信息**
   - 获取了Kippenberg 2018关于微腔Kerr孤子频率梳的论文
   - 提取了标题、作者、年份、摘要等信息

2. **通过Obsidian API创建文献笔记**
   - 在`LiteratureNotes/TRFV3Y5G.md`创建了结构化笔记
   - 笔记包含YAML frontmatter和完整内容
   - 成功建立了Zotero键与Obsidian笔记的关联

3. **双向API连通性验证**
   - Zotero API：`http://172.20.96.1:23119/api/users/19944378/...`
   - Obsidian API：`https://172.20.96.1:27124/vault/...`

## 建议的集成方案

### 方案A：基础集成（快速启动）
1. **配置Zotero插件自动导入**
   - 启用`obsidian-zotero-desktop-connector`插件的自动导入
   - 使用现有模板`templates/Zotero Literature Note.md`
   - 文献自动保存到`LiteratureNotes/`目录

2. **建立知识库引用链接**
   - 在Obsidian笔记中添加sci-logic-kb节点链接
   - 在YAML文件中添加Obsidian笔记引用

3. **创建文献索引**
   - 生成`LiteratureNotes/INDEX.md`，按专题分类文献

### 方案B：自动化工作流（中级）
1. **自动化文献导入脚本**
   ```python
   # 从Zotero导入文献到Obsidian
   # 1. 查询Zotero API获取新文献
   # 2. 检查是否已在知识库中存在
   # 3. 自动创建Obsidian笔记
   # 4. 更新文献索引
   ```

2. **知识库-文献双向链接**
   - 自动在YAML文件中添加`obsidian_note`字段
   - 在Obsidian笔记中自动添加知识库节点链接

3. **定期同步机制**
   - 检查Zotero中新添加的文献
   - 自动触发导入流程

### 方案C：智能知识提取（高级）
1. **AI辅助文献分析**
   - 从PDF提取关键信息
   - 自动生成知识节点草稿
   - 辅助专家审核与确认

2. **动态知识图谱**
   - 实时更新文献-知识节点关系
   - 可视化引用网络

3. **自动化质量检查**
   - 检查Zotero键的一致性
   - 验证文献-知识库对应关系

## 推荐实施步骤

### 第1步：基础集成配置（1-2天）
1. 配置Zotero插件进行批量导入
2. 创建文献索引系统
3. 测试基本工作流程

### 第2步：自动化脚本开发（2-3天）
1. 开发Zotero-Obsidian同步脚本
2. 建立知识库引用系统
3. 创建监控和报告机制

### 第3步：智能功能扩展（按需）
1. AI辅助知识提取
2. 高级搜索与发现
3. 可视化分析工具

## 需要您的决策

1. **首选集成方案**：A（基础）、B（自动化）还是C（智能）？
2. **导入范围**：仅超稳激光专题，还是所有专题？
3. **自动化程度**：完全自动导入，还是人工审核后导入？
4. **时间安排**：希望多快看到初步结果？

## 下一步行动建议

1. **立即行动**：配置Zotero插件，导入10-20篇核心文献到Obsidian
2. **验证工作流**：测试从文献笔记到知识库节点的引用
3. **扩展范围**：逐步导入更多文献，建立完整索引

## 技术细节

### Zotero API端点
```
# 获取文献列表
GET http://172.20.96.1:23119/api/users/19944378/items?itemType=journalArticle

# 获取单篇文献
GET http://172.20.96.1:23119/api/users/19944378/items/{KEY}
```

### Obsidian API端点
```
# 创建文件
PUT https://172.20.96.1:27124/vault/{path}.md

# 列出目录
GET https://172.20.96.1:27124/vault/{path}/
```

### 现有模板位置
- `templates/Zotero Literature Note.md` - 文献笔记模板
- `scripts/batch_process_zotero.py` - 批量处理脚本（可扩展）

---

**建议**：从方案A开始，快速建立基础集成，然后根据使用情况逐步升级到方案B。