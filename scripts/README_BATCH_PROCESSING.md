# 批量论文处理自动化流程

## 概述

本自动化流程用于批量处理Zotero中未处理的超稳激光相关论文，实现"agent流水处理"。

## 核心脚本

### 1. `batch_process_zotero.py`
- 从QUEUE.md读取未处理论文（`[ ]`状态）
- 通过Zotero API获取PDF文件
- 复制PDF到`pdfs/`目录
- 创建GitHub Issue触发处理（每批10篇）
- 需要环境变量：`GITHUB_TOKEN`

### 2. `batch_quality_check.py`
- 检查最近处理的论文YAML质量
- 验证节点唯一性、关系完整性
- 标注新节点为"未审核"
- 生成质量检查报告
- 可选：自动添加未审核标记

### 3. `auto_pipeline.sh`
- 主控制脚本，协调整个流程
- 三步流程：获取PDF → 质量检查 → 清理PDF
- 交互式操作，可暂停和继续

## 使用流程

### 快速开始
```bash
cd /home/hjian/sci-logic-kb

# 设置GitHub Token
export GITHUB_TOKEN=your_github_token

# 运行自动化流水线
./scripts/auto_pipeline.sh
```

### 分步执行
```bash
# 步骤1: 获取并上传PDF，创建Issue
python3 scripts/batch_process_zotero.py --batch-size 10

# 等待GitHub Actions处理完成...

# 步骤2: 质量检查
python3 scripts/batch_quality_check.py --count 10 --mark-unverified --output quality_report.md

# 步骤3: 清理PDF（可选）
rm pdfs/*.pdf
git rm pdfs/*.pdf
git commit -m "cleanup: remove processed PDF files"
```

## 设计原则

### 1. 批量处理
- 每10篇论文为一批
- 每批处理完成后进行质量检查
- 避免一次性处理过多论文导致混乱

### 2. 节点管理
- **优先复用已有节点**：跨文件引用现有节点
- **新节点为次级别**：尽量不开顶级节点
- **原理节点可开**：新的物理原理可创建节点
- **标注未审核**：所有新节点自动标记"未审核"

### 3. 存储优化
- PDF文件临时存储在`pdfs/`目录
- 处理完成后可删除PDF节省空间
- YAML文件（知识主体）保留在仓库中

### 4. 质量控制
- 检查节点ID全局唯一性
- 验证关系有`source.claim`
- 确保指标有`conditions`
- 保证原理节点有`conditions/preconditions`

## 配置要求

### 环境变量
```bash
# GitHub API token（创建Issue/PR）
export GITHUB_TOKEN="ghp_..."

# Zotero用户ID（默认已设置）
export ZOTERO_USER_ID="19944378"
```

### Zotero设置
- Zotero桌面版必须运行
- 启用API（工具 → 开发者 → 启用HTTP API）
- PDF文件必须存在于Zotero存储中

### 网络要求
- 可访问GitHub API
- 可访问Zotero本地API（http://127.0.0.1:23119）

## 故障排除

### PDF找不到
- 检查Zotero中是否有PDF附件
- 确认PDF文件路径正确
- 运行Zotero API测试：
  ```bash
  curl -H "Host: 127.0.0.1:23119" "http://$(ip route | grep default | awk '{print $3}'):23119/api/users/19944378/items/{ZOTERO_KEY}/children"
  ```

### GitHub Issue创建失败
- 检查`GITHUB_TOKEN`是否正确
- 验证token是否有创建Issue权限
- 检查网络连接

### 质量检查警告
- 重复节点：检查节点ID是否全局唯一
- 缺失source.claim：为关系补充原文引用
- 缺失conditions：为指标和原理添加条件

## 与现有流程集成

### GitHub Actions
- 本流程创建Issue触发现有`process-paper.yml`工作流
- 工作流使用claude-sonnet-4-6处理PDF生成YAML
- 自动创建PR等待审核

### QUEUE.md维护
- 脚本读取QUEUE.md中的未处理论文（`[ ]`状态）
- 处理完成后需要**手动**更新状态为`[x]`
- 可在SCHEMA.md中补充论文记录

### Obsidian记忆库
- 处理完成后可更新Obsidian中的项目记忆
- 记录光纤路线进展和其他关键发现

## 扩展建议

### 未来改进
1. **自动状态更新**：处理完成后自动更新QUEUE.md状态
2. **PDF智能清理**：根据处理状态自动清理PDF
3. **质量自动修复**：尝试自动修复常见质量问题
4. **批处理监控**：监控GitHub Actions状态自动继续

### 注意事项
- 新节点需要专家审核，AI标注"未审核"只是临时标记
- 原理节点创建需谨慎，确保有独立研究价值
- 跨文件引用时注意节点ID准确性