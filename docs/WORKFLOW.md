# 知识库操作流程指南

> **面向**：所有参与者（人类 + AI agent）  
> **定位**：日常操作的核心流程。详细 checklist → [CONTRIBUTING.md](../CONTRIBUTING.md)，规范定义 → [SCHEMA.md](../SCHEMA.md)，档位判定 → [CONTRIBUTION_TIER_RULES.md](CONTRIBUTION_TIER_RULES.md)

---

## 文档导航

| 我要... | 看哪个 |
|---------|--------|
| 按步骤摄入一篇论文 | [§一 单篇论文流程](#一单篇论文摄入流程) |
| 了解专题架构 | [TOPICS.md](../TOPICS.md) → `topics/<topic>/_meta/architecture.md` |
| 查询知识 | [USAGE.md](USAGE.md) |
| 审核专题 | [REVIEW_GUIDE.md](REVIEW_GUIDE.md) |
| AI 协作规则 | [CLAUDE.md](../CLAUDE.md) |
| 档位判定规则 | [CONTRIBUTION_TIER_RULES.md](CONTRIBUTION_TIER_RULES.md) |

---

## 一、单篇论文摄入流程

完整 checklist 见 [CONTRIBUTING.md](../CONTRIBUTING.md) Step 1–10。此处仅列核心命令。

### 1. 获取论文 PDF（从 Zotero）

```bash
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
ZOTERO_KEY="替换为实际KEY"
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('title','')); print(d.get('DOI',''))"
```

### 2. 提取并创建 YAML

- 遵循 [SCHEMA.md](../SCHEMA.md) 的节点/关系规范
- 档位判定参考 [CONTRIBUTION_TIER_RULES.md](CONTRIBUTION_TIER_RULES.md)
- 文件命名：`{first_author_lower}{year}.yaml`，位置：`topics/<topic>/papers/`
- 超稳激光专题：遵循 `topics/ultrastable-laser/_meta/scoping_principles.md` 的 σ_y-first 规则

### 3. 本地验证（必须全过）

```bash
python scripts/lint.py --summary    # 0 errors
python scripts/stats.py             # 指标不倒退
python scripts/build_index.py       # 重建索引
```

### 4. 更新运维文件

- `PROCESSED_PAPERS.md` — 追加记录
- `LOG.md` — 追加 `## [YYYY-MM-DD] ingest | {author}{year}: {描述}`
- `paper-inkb.md` — 追加行条目

### 5. 提交

```bash
git add topics/<topic>/papers/{filename}.yaml PROCESSED_PAPERS.md LOG.md paper-inkb.md
git add INDEX*.md topics/*/INDEX.md docs/CURRENT_NODES_REFERENCE.md
git commit -m "add {author}{year}: {论文核心贡献一句话}"
git push origin main
```

---

## 二、三个最常用命令

```bash
python scripts/lint.py --summary      # 质量检查
python scripts/stats.py               # 统计报告
python scripts/build_index.py         # 重建索引
```

---

## 三、索引文件说明

**自动生成（不要手工编辑）**：
- `INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` — 全局索引
- `docs/CURRENT_NODES_REFERENCE.md` — 节点速查（AI 摄入推荐入口）
- `topics/*/INDEX.md` — 各专题索引

**手工维护**：
- `paper-inkb.md` — 按专题的论文速查（标题 + Zotero Key + DOI）
- `PROCESSED_PAPERS.md` — 按时间的入库记录（含处理日志和档位）
- `LOG.md` — 演化日志

---

## 四、故障排查

### Git 操作失败

```bash
git remote -v
git remote set-url origin https://github.com/hjiang555-a11y/sci-logic-kb.git
```

### Zotero 连接失败

```bash
ip route | grep default | awk '{print $3}'                    # 检查 Windows IP
curl -s "http://${WINDOWS_IP}:23119/api/users/19944378/items?limit=1"  # 测试连接
```

### 脚本执行错误

```bash
python --version
python scripts/lint.py --help
python scripts/stats.py --help
```

---

## 五、常见错误

❌ 手工编辑自动生成的索引文件  
❌ 把 PDF 存入知识库（通过 Zotero 查找）  
❌ 盲目新建节点（先运行 `build_index.py` 查看已有节点）  
❌ 提交前不运行验证命令  

✅ Evidence 档论文允许产出 orphan 节点，不强求补 `breakthrough_paths`  
✅ 不确定时默认 `contribution_type: evidence`，由专家 review 时决定是否升档  

---

*最后更新：2026-05-08*
