# Claude Code 行为规范 — sci-logic-kb

本文件是 Claude Code 在此仓库中工作时的行为规范。

## 仓库用途

**时间频率计量科研知识库**（多专题架构）。  
从 Zotero 管理的论文 PDF 中提取结构化知识，存储为 YAML 节点图。

- **操作流程**：[docs/WORKFLOW.md](docs/WORKFLOW.md)
- **Schema 规范**：[SCHEMA.md](SCHEMA.md)
- **专题体系**：[TOPICS.md](TOPICS.md)
- **质量门**：[CONTRIBUTING.md](CONTRIBUTING.md)

---

## GitHub Copilot 优先原则

**优先使用 GitHub Copilot 完成工作，仅在 GitHub Copilot 无法完成时才使用本地 Claude Code 处理。**

### 分工原则

| 工具 | 适用场景 |
|------|----------|
| **GitHub Copilot** | YAML 模板、脚本生成、文档撰写、代码审查、重复性工作 |
| **本地 Claude Code** | PDF 阅读、本地工具调用、交互式探索、复杂逻辑推理 |

### 工作流整合
1. 尽可能将任务分解为可 GitHub Copilot 完成的子任务
2. 使用 GitHub PR 流程管理所有更改
3. 本地处理结果必须通过 GitHub PR 提交

---

## 单篇论文处理流程

> 详细步骤见 [docs/WORKFLOW.md](docs/WORKFLOW.md)，此处仅列核心要点

### 核心要点

1. **贡献类型判定**（v4.4）：
   - `evidence`: 默认，占大多数
   - `breakthrough`: 打破指标记录/提出新原理/证伪旧论断
   - `framework`: 综述/路线图/教科书章节

2. **超稳激光专题**：σ_y-first 规则（见 `topics/ultrastable-laser/_meta/scoping_principles.md`）

3. **节点新建判据**（至少满足一条）：
   - 能独立回答一类查询
   - 拥有独立的设计选择空间
   - 会被多篇论文复用
   - 拥有独立的限制链/证据链

### 获取论文 PDF

```bash
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
ZOTERO_KEY="替换为实际KEY"

# 获取论文元数据
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('title','')); print(d.get('DOI',''))"

# 获取附件 PDF 路径
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}/children" \
  | python3 -c "
import json, sys
items = json.load(sys.stdin)
for i in items:
    d = i.get('data', {})
    if d.get('itemType') == 'attachment':
        key = d.get('key', '')
        fn = d.get('filename', d.get('path', '').split('/')[-1])
        print(f'/mnt/d/Users/hjian/Zotero/storage/{key}/{fn}')
"
```

---

## 节点 ID 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 实体 | `ent.{描述词}_{后缀}` | `ent.fp_cavity_system` |
| 原理 | `pri.{描述词}` | `pri.brownian_thermal_noise` |
| 方法 | `meth.{描述词}` | `meth.pdh_locking` |
| 指标 | `met.{描述词}_{后缀}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{首字母}{序号}` | `rel.M01` |

---

## 已有节点速查

处理新论文时，通过以下文件查找已有节点（避免重复建节点）：

- **全专题节点一览**（AI 摄入推荐）：[`docs/CURRENT_NODES_REFERENCE.md`](docs/CURRENT_NODES_REFERENCE.md)
- **跨专题原理/方法**：[`INDEX_principles.md`](INDEX_principles.md)
- **超稳激光专题**：[`topics/ultrastable-laser/INDEX.md`](topics/ultrastable-laser/INDEX.md)
- **光学频率梳专题**：[`topics/optical-frequency-combs/INDEX.md`](topics/optical-frequency-combs/INDEX.md)

> 若索引文件不存在，运行 `python scripts/build_index.py` 生成

---

## 人机协作原则

> **核心理念**：人做策展与提问，AI 做簿记与维护（inspired by Karpathy LLM Wiki）

### 人类角色（Domain Expert）
- 选择论文、确认节点边界
- 审核争议性论断、综合页面
- 提出探索性问题
- 决定 Schema 方向

### AI 角色（Knowledge Engineer）
- YAML 节点提取与维护
- 跨文件交叉引用维护
- INDEX/LOG/PROCESSED_PAPERS 自动更新
- 综合页面生成与更新
- 健康检查与一致性检测

---

*最后更新：2026-04-28*  
*版本：v4.5*
