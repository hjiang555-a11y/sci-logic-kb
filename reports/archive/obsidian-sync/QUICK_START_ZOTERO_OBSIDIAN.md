# Zotero-Obsidian智能集成快速启动指南

## 已为您完成的工作

1. **分析当前状态**：确认Zotero API和Obsidian API已配置且可访问
2. **设计完整方案**：创建`ZOTERO_OBSIDIAN_AI_INTEGRATION.md`详细实施计划
3. **开发测试工具**：创建`scripts/test_integration.py`环境测试脚本
4. **提供配置模板**：生成`.env.example`配置文件示例

## 立即开始（10分钟）

### 步骤1：测试当前环境
```bash
cd /home/hjian/sci-logic-kb/sci-logic-kb
python3 scripts/test_integration.py
```

### 步骤2：配置环境变量
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑.env文件，填入实际值
# 主要需要配置：
# 1. OBSIDIAN_API_TOKEN（从Obsidian插件获取）
# 2. AI API密钥（可选，如OPENAI_API_KEY）
nano .env  # 或使用其他编辑器
```

### 步骤3：安装依赖
```bash
pip install requests python-dotenv
# 可选PDF处理依赖
pip install pypdf2 pdfplumber
```

### 步骤4：运行基础集成测试
```bash
# 测试单篇论文处理
python3 scripts/batch_process_zotero.py --batch-size=1
```

## 分阶段实施建议

### 第一阶段：基础自动化（本周）
1. **目标**：实现Zotero→Obsidian自动导入
2. **关键任务**：
   - 完善文献笔记模板
   - 配置obsidian-zotero-desktop-connector自动导入
   - 测试10篇核心论文的导入流程
3. **预期成果**：新添加的Zotero论文自动在Obsidian中创建笔记

### 第二阶段：智能提取（1-2周）
1. **目标**：添加AI辅助信息提取
2. **关键任务**：
   - 实现PDF文本提取模块
   - 设计并优化LLM提示词
   - 创建结构化信息提取流水线
3. **预期成果**：论文PDF自动分析，生成知识节点草稿

### 第三阶段：知识库集成（1周）
1. **目标**：自动更新sci-logic-kb
2. **关键任务**：
   - 实现YAML节点生成模块
   - 建立双向引用系统
   - 添加质量检查机制
3. **预期成果**：论文信息自动转换为知识库节点

## 重要配置说明

### 1. Obsidian Local REST API配置
- 在Obsidian中：设置 → Community plugins → Local REST API
- 启用插件，生成API Token
- 将Token填入`.env`文件的`OBSIDIAN_API_TOKEN`

### 2. Zotero Better BibTeX配置（可选但推荐）
- 安装Better BibTeX插件
- 配置自动导出，便于引用管理

### 3. 文献笔记模板位置
- 模板文件：`templates/Zotero Literature Note.md`
- 如果不存在，请创建并定义您的笔记结构

## 故障排除

### 常见问题1：Zotero API连接失败
- 检查Zotero是否正在运行
- 确认端口23119未被占用
- 验证Windows防火墙设置

### 常见问题2：Obsidian API认证失败
- 确认Local REST API插件已启用
- 检查API Token是否正确
- 验证WSL→Windows网络连通性

### 常见问题3：PDF文件找不到
- 检查Zotero存储路径配置
- 确认PDF文件已附加到Zotero条目
- 验证路径映射（Windows→WSL）

## 获取帮助

1. **查看详细文档**：
   - `ZOTERO_OBSIDIAN_AI_INTEGRATION.md` - 完整技术方案
   - `ZOTERO_OBSIDIAN_INTEGRATION_PLAN.md` - 原始集成计划
   - `SCHEMA.md` - 知识库架构规范

2. **检查现有脚本**：
   - `scripts/batch_process_zotero.py` - 批量处理基础
   - `scripts/batch_quality_check.py` - 质量检查工具

3. **测试环境**：
   - `scripts/test_integration.py` - 全面环境测试

## 后续开发建议

### 如果您有编程经验：
- 直接修改`scripts/`目录下的Python脚本
- 参考现有代码模式扩展功能
- 使用Git进行版本控制

### 如果您希望最小化编码：
- 主要使用`obsidian-zotero-desktop-connector`插件
- 配合现有脚本进行批量处理
- 手动审核AI提取结果

## 联系支持
- 如有问题，请提供`scripts/test_integration.py`的输出结果
- 包含相关错误信息和环境信息
- 参考现有成功案例：`LiteratureNotes/TRFV3Y5G.md`

---

**建议**：从基础自动化开始，先建立可靠的数据流，再逐步添加智能功能。优先处理超稳激光专题的论文，验证工作流后再扩展到其他专题。