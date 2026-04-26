# Claude Code 行为规范 — sci-logic-kb

本文件是 Claude Code 在此仓库中工作时的行为规范。

## 仓库用途

**时间频率计量科研知识库**（多专题，当前已建超稳激光专题）。
从 Zotero 管理的论文 PDF 中提取结构化知识，存储为 YAML 节点图。

详细 Schema 见 `SCHEMA.md`，专题体系见 `TOPICS.md`。

---

## GitHub Copilot 优先原则

**优先使用 GitHub Copilot 完成工作，仅在 GitHub Copilot 无法完成时才使用本地 Claude Code 处理。**

具体实施：
1. **GitHub Copilot 适用场景**：
   - 代码生成（YAML 模板、Python 脚本、bash 脚本）
   - 文档撰写（README、注释、说明）
   - 代码审查和问题修复
   - 基于已有模式的重复性工作

2. **本地 Claude Code 适用场景**：
   - 需要读取本地 PDF 文件（Zotero 存储）
   - 需要调用本地工具（Read、Edit、Bash 等）
   - 需要交互式探索和决策（如关系提取、节点识别）
   - GitHub Copilot 无法直接处理的复杂逻辑推理

3. **工作流整合**：
   - 尽可能将任务分解为可 GitHub Copilot 完成的子任务
   - 使用 GitHub PR 流程管理所有更改
   - 本地处理结果必须通过 GitHub PR 提交

## 论文摄入流程

论文摄入的全流程（从选论文到 YAML 提取到 PR 提交）已归档至：

- **完整流程**：[`CONTRIBUTING.md`](CONTRIBUTING.md)（Step 1–10，v4.4 三档规范）
- **档位判定规则**：[`docs/CONTRIBUTION_TIER_RULES.md`](docs/CONTRIBUTION_TIER_RULES.md)
- **PR 提交前检查**：[`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md)

### 获取论文 PDF（本文件特有内容）

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
| 实体 | `ent.{描述词}_{可选后缀}` | `ent.fp_cavity_system` |
| 原理 | `pri.{描述词}` | `pri.brownian_thermal_noise_fdt` |
| 方法 | `meth.{描述词}` | `meth.pdh_locking` |
| 指标 | `met.{描述词}_{可选后缀}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{文件首字母缩写}{两位序号}` | `rel.N01`（N=Numata） |

---

## 已有节点速查（自动生成）

> ⚠ **不要在本文件手工维护节点列表**——那是"簿记"，不是行为规范。
>
> 处理新论文时，通过以下自动生成文件查找已有节点：
>
> - **跨专题原理/方法速查**：[`INDEX_principles.md`](INDEX_principles.md)
> - **超稳激光专题节点**：[`topics/ultrastable-laser/INDEX.md`](topics/ultrastable-laser/INDEX.md)
> - **光学频率梳专题节点**：[`topics/optical-frequency-combs/INDEX.md`](topics/optical-frequency-combs/INDEX.md)
> - **全专题节点一览（AI 摄入推荐入口）**：[`docs/CURRENT_NODES_REFERENCE.md`](docs/CURRENT_NODES_REFERENCE.md)（由 `scripts/build_index.py` 自动生成）
>
> 若 `docs/CURRENT_NODES_REFERENCE.md` 不存在，运行 `python scripts/build_index.py` 生成。

---

*本文件由 Claude Code 生成，更新日期：2026-04-21*
*多专题架构升级：v4.0*
*运维层引入：v4.2（Karpathy LLM Wiki 思想整合）*
*贡献分级（breakthrough/evidence/framework）：v4.4*

---

## 人机协作原则（v4.2 新增，inspired by Karpathy LLM Wiki）

> **核心理念**：人做策展与提问，AI 做簿记与维护。知识库的价值在于**持久复合知识**的增量构建，而非每次查询时重新发现。

### 人类角色（Domain Expert）
- **选择论文**（sourcing）：决定下一篇处理的论文
- **确认节点边界**：判断"这是新实体还是参数变体？"
- **审核争议性论断**：决定 `contested_claims` 的最终判定
- **提出探索性问题**：如"为什么 17K 比 4K 的镀层损耗更低？"
- **审核综合页面**：确认 `synthesis/` 目录下页面的准确性
- **决定 Schema 方向**：Schema 升级由人类主导

### AI 角色（Knowledge Engineer）
- **Ingest**：YAML 节点提取与维护
- **Cross-referencing**：跨文件交叉引用维护
- **Bookkeeping**：INDEX.md / LOG.md / PROCESSED_PAPERS.md 自动更新
- **Synthesis**：综合页面生成与更新
- **Lint**：健康检查与修复建议
- **Consistency check**：新论文与已有知识的矛盾检测
- **Freshness tracking**：新论文入库后标记受影响的综合页面为"需要更新"

### 运维文件导航
- **全局导航索引**：[`INDEX.md`](INDEX.md)
- **演化日志**：[`LOG.md`](LOG.md)
- **已处理论文列表**：[`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md)
- **综合分析页面**：`topics/<topic>/synthesis/`
- **完整 Schema 规范**：[`SCHEMA.md`](SCHEMA.md)（第十节定义运维操作）
