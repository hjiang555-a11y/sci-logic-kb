# Zotero-Obsidian智能集成方案（方案C扩展）

## 概述

本方案实现Zotero论文库与Obsidian知识库的**智能自动关联**，基于AI辅助的文献分析，实现：
1. **自动化数据流**：Zotero新论文自动导入Obsidian
2. **智能信息提取**：使用LLM分析PDF，提取结构化知识
3. **知识图谱集成**：自动生成sci-logic-kb兼容的YAML节点
4. **双向链接管理**：维护Zotero↔Obsidian↔知识库的完整引用链

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Zotero    │────▶│  监控模块   │────▶│   PDF处理模块   │
│  (Windows)  │     │ (WSL Python)│     │  (文本提取)     │
└─────────────┘     └─────────────┘     └─────────────────┘
                                                   │
┌─────────────┐     ┌─────────────┐               ▼
│  Obsidian   │◀────│  笔记生成   │◀────┌─────────────────┐
│  (Windows)  │     │   模块      │     │   AI提取模块    │
└─────────────┘     └─────────────┘     │  (LLM分析)      │
         │                               └─────────────────┘
         ▼                                       │
┌─────────────┐     ┌─────────────┐             ▼
│ sci-logic-kb│◀────│ 知识库集成  │◀─────┌─────────────────┐
│   (WSL)     │     │   模块      │      │  映射与链接模块  │
└─────────────┘     └─────────────┘      └─────────────────┘
```

## 当前状态验证

### ✅ 已验证的功能
1. **Zotero API可访问**：`http://172.20.96.1:23119/api/users/19944378/`
2. **Obsidian API可连接**：`https://172.20.96.1:27124/vault/`（需认证）
3. **现有脚本基础**：`scripts/batch_process_zotero.py`提供基础框架
4. **成功测试记录**：已创建`LiteratureNotes/TRFV3Y5G.md`文献笔记

### 🔧 需要配置的组件
1. **AI API密钥**：OpenAI或Anthropic API密钥（用于LLM分析）
2. **Obsidian API密钥**：Local REST API的认证令牌
3. **环境变量文件**：`.env`存储敏感配置
4. **PDF处理库**：PyPDF2/pdfplumber用于文本提取

## 核心模块设计

### 模块1：监控模块（monitor.py）
```python
# 功能：定期检查Zotero中的新论文
# 输入：Zotero API端点
# 输出：新论文列表（Zotero Key, 标题, 作者, 年份）
# 触发：定时任务（cron）或手动执行
```

### 模块2：PDF处理模块（pdf_processor.py）
```python
# 功能：下载PDF并提取文本
# 输入：Zotero Key → PDF文件路径
# 输出：PDF文本内容（分章节）
# 依赖：PyPDF2/pdfplumber, Zotero存储路径映射
```

### 模块3：AI提取模块（ai_extractor.py）
```python
# 功能：使用LLM分析论文，提取结构化信息
# 输入：PDF文本、论文元数据
# 输出：结构化JSON，包含：
#   - 研究问题
#   - 核心贡献
#   - 方法学创新
#   - 关键结果
#   - 限制因素
#   - 与现有知识库的关联点
# 依赖：OpenAI/Anthropic API，精心设计的提示词
```

### 模块4：笔记生成模块（note_generator.py）
```python
# 功能：创建Obsidian文献笔记
# 输入：结构化提取信息
# 输出：Markdown文件（遵循模板）
# 特性：
#   - 使用模板`templates/Zotero Literature Note.md`
#   - 包含YAML frontmatter
#   - 自动添加双向链接
#   - 保存到`LiteratureNotes/`目录
```

### 模块5：知识库集成模块（kb_integrator.py）
```python
# 功能：更新sci-logic-kb YAML文件
# 输入：结构化提取信息、论文元数据
# 输出：新的或更新的YAML节点文件
# 逻辑：
#   - 检查是否已有相关节点（通过zotero_key）
#   - 创建新节点或更新现有节点
#   - 遵循SCHEMA.md v4.1规范
#   - 建立COMPETES-WITH/ENABLED-BY等关系
```

### 模块6：链接管理模块（link_manager.py）
```python
# 功能：维护完整的引用链
# 输入：Zotero Key, Obsidian笔记路径, YAML节点路径
# 输出：更新所有相关文件的引用
# 包括：
#   - Zotero项目添加Obsidian笔记链接
#   - Obsidian笔记添加知识库节点链接
#   - 知识库节点添加Zotero引用
```

## 实施路线图

### 阶段1：基础自动化（1-2天）
1. **扩展现有脚本**：修改`batch_process_zotero.py`，添加Obsidian笔记创建
2. **配置环境**：设置`.env`文件，包含所有API密钥
3. **创建模板**：完善文献笔记模板，支持AI提取字段
4. **测试端到端流**：从Zotero→Obsidian的基础流程

### 阶段2：AI信息提取（2-3天）
1. **PDF文本提取**：实现PDF处理模块
2. **LLM集成**：实现AI提取模块，设计提示词
3. **结构化输出**：定义与sci-logic-kb兼容的JSON schema
4. **质量验证**：人工审核AI提取结果，优化提示词

### 阶段3：知识库集成（2-3天）
1. **YAML生成**：实现知识库集成模块
2. **节点关系建立**：自动识别与现有节点的关系
3. **链接管理**：实现双向引用更新
4. **批量处理**：处理现有文献库

### 阶段4：部署与优化（1-2天）
1. **定时任务**：设置cron job监控新论文
2. **错误处理**：添加重试、日志、警报机制
3. **性能优化**：缓存、批量处理、并行处理
4. **文档完善**：用户指南、故障排除

## 技术细节

### API端点
```bash
# Zotero API
GET http://172.20.96.1:23119/api/users/19944378/items/{key}
GET http://172.20.96.1:23119/api/users/19944378/items/{key}/children

# Obsidian API (需认证)
PUT https://172.20.96.1:27124/vault/{path}.md
Headers: { "Authorization": "Bearer YOUR_TOKEN" }

# AI API (示例: OpenAI)
POST https://api.openai.com/v1/chat/completions
Headers: { "Authorization": "Bearer YOUR_OPENAI_KEY" }
```

### 环境变量配置（.env）
```bash
# Zotero配置
ZOTERO_USER_ID=19944378
ZOTERO_API_HOST=172.20.96.1
ZOTERO_API_PORT=23119

# Obsidian配置
OBSIDIAN_API_HOST=172.20.96.1
OBSIDIAN_API_PORT=27124
OBSIDIAN_API_TOKEN=your_token_here
OBSIDIAN_VAULT_PATH=/path/to/vault

# AI配置
OPENAI_API_KEY=sk-...
# 或
ANTHROPIC_API_KEY=sk-ant-...

# 路径配置
SCI_LOGIC_KB_PATH=/home/hjian/sci-logic-kb/sci-logic-kb
PDF_STORAGE_PATH=/home/hjian/sci-logic-kb/sci-logic-kb/pdfs
LITERATURE_NOTES_PATH=LiteratureNotes
```

### AI提示词设计（示例）
```python
system_prompt = """
你是一位时间频率计量领域的专家助手。请分析以下学术论文，提取结构化信息。

请提取以下信息：
1. 研究问题：论文要解决的核心科学或技术问题
2. 核心贡献：论文的主要创新点或贡献
3. 方法学：使用的实验方法、理论模型或技术方案
4. 关键结果：最重要的实验结果或理论发现
5. 限制因素：研究中提到的限制或未来改进方向
6. 关联节点：与sci-logic-kb中以下专题的潜在关联：
   - 超稳激光（ultrastable-laser）
   - 光学频率梳（optical-frequency-combs）
   - 频率标准（frequency-standards）

请以JSON格式返回，包含上述字段。
"""

user_prompt = f"""
论文标题：{title}
作者：{authors}
年份：{year}
摘要：{abstract}
PDF文本（节选）：{pdf_excerpt}
"""
```

## 预期成果

### 自动化工作流
- Zotero中添加新论文 → 自动在Obsidian创建文献笔记
- PDF自动下载 → AI提取关键信息 → 生成知识节点草稿
- 专家审核 → 确认或修改 → 正式入库

### 知识发现辅助
- **相似论文聚类**：自动识别研究主题相似的论文
- **技术演进追踪**：跟踪特定技术路线的进展
- **知识缺口识别**：发现研究不足的领域

### 质量保证机制
- **AI提取验证**：专家审核AI提取结果
- **一致性检查**：确保遵循SCHEMA.md规范
- **版本控制**：Git追踪所有变更

## 风险评估与缓解

### 风险1：AI提取准确性不足
- **缓解**：人工审核阶段，优化提示词，使用高质量LLM（Claude Opus/GPT-4）

### 风险2：PDF文本提取问题
- **缓解**：多引擎备用（PyPDF2 + pdfplumber），手动上传选项

### 风险3：API连接不稳定
- **缓解**：重试机制，本地缓存，离线模式

### 风险4：知识库架构变更
- **缓解**：版本感知，向后兼容，架构检查脚本

## 立即行动步骤

### 今天可以开始的：
1. **测试现有脚本**：运行`python scripts/batch_process_zotero.py --batch-size=1`
2. **配置环境变量**：创建`.env`文件，填入已知API密钥
3. **验证API连接**：测试Zotero和Obsidian API的连通性
4. **创建文献笔记模板**：完善`templates/Zotero Literature Note.md`

### 本周目标：
1. 实现基础自动化流程（Zotero→Obsidian）
2. 完成PDF文本提取模块
3. 设计并测试AI提示词
4. 处理5-10篇核心论文作为试点

## 后续扩展方向

### 短期（1个月）
- 添加Web界面用于审核和编辑
- 实现实时监控（webhook替代轮询）
- 集成更多文献数据库（arXiv, DOI查询）

### 中期（3个月）
- 多模态分析（图表提取，数据表格识别）
- 自动生成综述文档
- 预测研究趋势

### 长期（6个月+）
- 知识图谱可视化
- 智能问答系统
- 研究助手AI代理

---

## 附录

### 相关文件
1. `ZOTERO_OBSIDIAN_INTEGRATION_PLAN.md` - 基础集成方案
2. `SCHEMA.md` - 知识库架构规范
3. `scripts/batch_process_zotero.py` - 现有批量处理脚本
4. `templates/Zotero Literature Note.md` - 文献笔记模板

### 技术依赖
```bash
# Python包
pip install requests pyyaml python-dotenv
pip install pypdf2 pdfplumber  # PDF处理
pip install openai anthropic   # AI API
```

### 测试用例
1. **单元测试**：各模块功能测试
2. **集成测试**：端到端工作流测试
3. **质量测试**：AI提取准确性评估
4. **性能测试**：大批量处理能力

---

**建议**：从阶段1开始，快速建立可用的自动化流程，然后逐步添加AI功能。优先处理超稳激光专题的论文，验证工作流后再扩展到其他专题。