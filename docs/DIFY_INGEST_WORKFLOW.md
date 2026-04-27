# ultrastable-laser 知识库 → Dify 导入工作流

> 最后更新：2026-04-26
> 执行者：Claude Code（timefreq）
> 状态跟踪：每步完成后更新本文件开头的进度表

---

## 进度

| 步骤 | 状态 | 最后执行 | 结果 |
|------|------|----------|------|
| 0. Dify API 验证 | ⏳ | - | - |
| 1. Pilot 试点导入（3篇） | ⏳ | - | - |
| 2. Pilot 验证 | ⏳ | - | - |
| 3. 全量 YAML → Markdown 转换 | ⏳ | - | - |
| 4. 第一批导入（24 breakthrough） | ⏳ | - | - |
| 5. 第二批导入（62 evidence） | ⏳ | - | - |
| 6. 第三批导入（11 framework+synthesis） | ⏳ | - | - |
| 7. 全量验证与报告 | ⏳ | - | - |

---

## 前置条件

- Dify 运行在 http://localhost:8090
- Dataset API Token: `ds-c242093e604d4d2a89297b3af603730e`
- 工作目录: `/data/sci-logic-kb/`

---

## 步骤 0：Dify API 验证

**目标**：确保 Dify API 可达。

```bash
curl -s http://localhost:8090/v1/datasets \
  -H "Authorization: Bearer ds-c242093e604d4d2a89297b3af603730e"
```

**回滚**：无需回滚，纯验证操作。

---

## 步骤 1：Pilot 试点导入（3 篇）

**目标**：选 3 篇代表论文（breakthrough×1 + evidence×1 + framework×1），手动转换并上传，验证整个流程。

**选哪三篇**：
- `numata2004.yaml`（breakthrough，25KB，含完整节点和关系）
- `young1999.yaml`（evidence，含实体+指标）
- 任一篇 `contribution_type: framework` 的论文

**操作**：
1. 用 Read 工具读每篇 YAML 的完整内容
2. 按以下格式转换为 Markdown：
   ```markdown
   # {author}{year} — {title}

   ## 元数据
   - contribution_type: {type}

   ## 实体
   - ent.xxx — 名称（Level X）

   ## 原理
   - pri.xxx — 名称

   ## 方法
   - meth.xxx — 名称

   ## 指标
   - met.xxx — 值

   ## 关系
   - BOUNDED-BY: ...
   - COMPETES-WITH: ...
   ```
3. 通过 Dify API 上传到知识库（以下是 Dify 1.13.3 已验证的 API 端点）：
   - **创建知识库**：`POST /v1/datasets`
   - **文本创建文档**：`POST /v1/datasets/{id}/document/create-by-text`
   - **文件上传创建文档**：`POST /v1/datasets/{id}/document/create-by-file`
   - **列出文档**：`GET /v1/datasets/{id}/documents`
   
   文本方式示例：
   ```bash
   curl -X POST http://localhost:8090/v1/datasets/{dataset_id}/document/create-by-text \
     -H "Authorization: Bearer ds-c242093e604d4d2a89297b3af603730e" \
     -H "Content-Type: application/json" \
     -d '{"name":"numata2004.md","text":"# 转换后的Markdown内容...","process_rule":{"mode":"automatic"}}'
   ```
   
   文件上传方式示例：
   ```bash
   curl -X POST http://localhost:8090/v1/datasets/{dataset_id}/document/create-by-file \
     -H "Authorization: Bearer ds-c242093e604d4d2a89297b3af603730e" \
     -F "file=@_dify_ingest/md/numata2004.md" \
     -F "data={\"name\":\"numata2004.md\",\"indexing_technique\":\"high_quality\",\"process_rule\":{\"mode\":\"automatic\"}}"
   ```
4. 保存在 `_dify_ingest/md/` 目录作为备份

**回滚**：删除 pilot 知识库（Dify Web 界面或 API delete）。

---

## 步骤 2：Pilot 验证

**目标**：确认导入的 3 篇论文在 Dify 中可检索。

**操作**：
1. 通过 API 查询文档数量和分段状态
2. 执行一次检索测试：
   ```bash
   curl -X POST http://localhost:8090/v1/datasets/{dataset_id}/retrieve \
     -H "Authorization: Bearer ds-c242093e604d4d2a89297b3af603730e" \
     -H "Content-Type: application/json" \
     -d {query: 热噪声极限 σ_y}
   ```
3. 检查检索结果是否包含预期节点和关系

**回滚**：无需回滚，验证操作。

---

## 步骤 3：全量 YAML → Markdown 转换

**目标**：把 89 篇 YAML + 8 个 synthesis 全部转换为 Dify 可导入的 Markdown。

**操作**：
1. 写转换脚本 `scripts/yaml2dify.py`，解析 YAML 的 entities/principles/methods/metrics/relations
2. 输出到 `_dify_ingest/md/` 目录
3. 验证：检查输出文件数（应为 97）、抽查格式

**回滚**：删除 `_dify_ingest/` 目录即可。

---

## 步骤 4-6：分批导入

**分批方案**：

| 步 | 内容 | 数量 | 总大小 |
|----|------|------|--------|
| 4 | breakthrough 论文 | 24 篇 | ~200 KB |
| 5 | evidence 论文 | 62 篇 | ~400 KB |
| 6 | framework + synthesis | 11 篇 | ~100 KB |

**操作**：
1. 写导入脚本 `scripts/dify_import.py`
2. 每批导入后用 API 验证文档数
3. 记录导入日志

**回滚策略**：
- 单批导入后：Dify Web 界面删除对应文档
- 全量导入后：直接删除整个知识库，重新创建

---

## 步骤 7：全量验证与报告

**目标**：确认 97 个文档全部成功导入并可检索。

**操作**：
1. API 查询文档总数
2. 执行 3-5 个典型查询验证检索效果
3. 输出导入报告

**产出**：一份完整的导入报告。
