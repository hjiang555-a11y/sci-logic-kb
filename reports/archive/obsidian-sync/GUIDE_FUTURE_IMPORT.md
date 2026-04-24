# 未来论文导入自动关联指南

## 目标
确保未来新导入的论文自动与Zotero关联，避免手动添加`zotero_key`字段。

## 当前状态
- ✅ 现有88篇论文已全部关联（zotero_key有效性100%）
- ✅ Zotero API连接正常（用户ID: 19944378，主机: 172.20.96.1）
- ✅ 验证脚本可用（`scripts/validate_zotero_keys.py`）
- ✅ 匹配脚本可用（`scripts/match_missing_keys.py`）

## 自动关联工作流

### 方案A：通过GitHub Copilot创建新论文YAML（推荐）
1. **搜索Zotero论文**
   ```bash
   cd /home/hjian/sci-logic-kb/sci-logic-kb
   python scripts/zotero_helper.py search --title "论文标题" [--author "作者" --year "年份"]
   ```

2. **获取zotero_key**
   ```bash
   python scripts/zotero_helper.py get ZOTERO_KEY
   ```

3. **生成YAML模板**
   ```bash
   python scripts/zotero_helper.py template ZOTERO_KEY --topic "专题名称"
   ```

4. **使用Copilot完善YAML内容**
   - 将生成的模板复制到 `topics/专题名称/papers/`
   - 使用GitHub Copilot填充逻辑单元、证据和关系
   - 确保`meta.zotero_key`字段已正确设置

### 方案B：批量导入（通过QUEUE.md）
1. **在QUEUE.md中添加新论文**
   ```
   [ ] `ZOTERO_KEY` | Author Year | Title
   ```

2. **运行批量处理脚本**
   ```bash
   python scripts/batch_process_zotero.py --batch-size 10
   ```

3. **扩展建议**：修改`batch_process_zotero.py`，使其在创建Issue时同时生成YAML模板

### 方案C：手动创建时使用助手
创建新YAML文件时，始终运行：
```bash
python scripts/zotero_helper.py match --title "标题" --author "作者" --year "年份"
```

## 关键脚本说明

### 1. `scripts/zotero_helper.py`
- **search**：按标题/作者/年份搜索Zotero论文
- **get**：获取指定zotero_key的论文详情
- **template**：生成包含zotero_key的YAML模板
- **match**：智能匹配并建议zotero_key

### 2. `scripts/validate_zotero_keys.py`
验证所有YAML文件的zotero_key有效性：
```bash
python scripts/validate_zotero_keys.py
```
输出：有效性报告（保存到`ZOTERO_KEY_VALIDATION_REPORT.md`）

### 3. `scripts/match_missing_keys.py`
自动匹配缺少zotero_key的YAML文件：
```bash
python scripts/match_missing_keys.py
```
注意：此脚本已自动更新了6个缺失key的文件。

## 质量保证措施

### 1. 提交前验证
```bash
# 验证所有zotero_key
python scripts/validate_zotero_keys.py

# 检查是否有缺失key
python scripts/match_missing_keys.py --dry-run
```

### 2. GitHub Copilot提示词
在创建新论文YAML时，可提示Copilot：
```
请确保YAML文件的meta部分包含zotero_key字段。
可使用以下命令查找zotero_key：
python scripts/zotero_helper.py search --title "论文标题"
```

### 3. 定期维护
每月运行一次验证：
```bash
# 生成验证报告
python scripts/validate_zotero_keys.py

# 如果有无效key，重新匹配
python scripts/match_missing_keys.py --auto-update
```

## 故障排除

### 问题1：Zotero API连接失败
**症状**：脚本返回"连接失败"或"HTTP错误"
**解决**：
1. 确保Zotero在Windows上运行且启用API
2. 检查`.env`文件中的配置：
   ```
   ZOTERO_USER_ID=19944378
   ZOTERO_API_HOST=172.20.96.1
   ZOTERO_API_PORT=23119
   ```
3. 验证网络连接：
   ```bash
   curl "http://172.20.96.1:23119/api/users/19944378/items?limit=1"
   ```

### 问题2：zotero_key不存在
**症状**：验证报告显示无效key
**解决**：
1. 检查key是否输入错误（8位大写字母数字）
2. 确认论文仍在Zotero库中
3. 重新匹配：
   ```bash
   python scripts/match_missing_keys.py --file 路径/到/文件.yaml
   ```

### 问题3：匹配不准确
**症状**：自动匹配到错误的论文
**解决**：
1. 使用更精确的搜索条件：
   ```bash
   python scripts/zotero_helper.py match --title "完整标题" --author "第一作者" --year "年份"
   ```
2. 手动指定zotero_key：
   ```bash
   python scripts/zotero_helper.py get ZOTERO_KEY
   ```

## 最佳实践

1. **先查后建**：创建新论文YAML前，先用`zotero_helper.py`搜索确认zotero_key
2. **验证提交**：提交到GitHub前运行验证脚本
3. **定期维护**：每月验证一次所有关联
4. **文档更新**：新导入流程如有变化，更新此指南

## 扩展建议

### 1. 集成到GitHub Actions
添加CI检查，确保新提交的YAML包含有效的zotero_key：
```yaml
name: Validate Zotero Keys
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: python scripts/validate_zotero_keys.py
```

### 2. 增强batch_process_zotero.py
扩展现有脚本，使其：
- 生成YAML模板（而不仅仅是PDF和Issue）
- 自动添加zotero_key到生成的模板中

### 3. 创建Copilot技能
编写GitHub Copilot技能，指导用户：
- 如何查找zotero_key
- 如何创建包含正确字段的YAML文件

---

## 总结
通过上述工作流，可以实现未来论文导入的自动关联。核心原则是：
1. **保持zotero_key字段**：所有YAML文件的meta部分必须包含zotero_key
2. **验证优先**：创建/修改后立即验证
3. **工具辅助**：使用提供的脚本减少手动错误

当前所有88篇论文已100%关联，为未来导入建立了良好基础。