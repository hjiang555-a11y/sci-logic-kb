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

## 单篇论文处理流程

### 步骤 1：确定目标论文

从 `QUEUE.md` 中选取下一篇 `[ ]` 状态的论文，记录其 `ZOTERO_KEY`。

### 步骤 2：获取论文 PDF

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

### 步骤 3：阅读 PDF

使用 `Read` 工具读取 PDF 文件（最多 20 页/次，大论文分批读取）。

### 步骤 4：提取 YAML

按 `SCHEMA.md` 中的模板提取：
- 识别该论文的**核心贡献**（方法创新/原理解析/实验结果，或专题框架定义）
- 决定 `meta.contribution_type`（v4.4 三档规范，详见 [SCHEMA.md §9.1](SCHEMA.md)）：
  - `breakthrough`：打破指标记录 / 提出新原理 / 证伪旧论断
  - `evidence`：在已有节点上提供新数据点、复现、工程改进（**大多数论文属此档，默认**）
  - `framework`：综述 / 路线图 / 教科书章节
- 提取节点（entities/principles/methods/metrics）
- 建立关系（relations）
- 检查是否有跨文件引用的已有节点

**超稳激光专题 σ_y-first 规则**（Round 3 起，2026-04-21）：若当前处理论文属 `ultrastable-laser`，档位判定遵循专题专属规则：
- 优先识别并量化该论文的 **σ_y(τ=1 s)** 值 —— 这是档位判定的第一依据
- 若论文未直接报告 σ_y，尝试从频噪 PSD 换算；只有线宽时在 note 中声明 `primary-metric missing: linewidth only`（不能升 breakthrough）
- 报告 σ_y 时**必须**标注 Allan 变体类型（ADEV / MDEV / OADEV / Hadamard）
- 线宽、频噪 PSD、相干时间、**长期漂移**、加速度灵敏度、镀层损耗角等单独刷新一律归 `evidence`
- 详见 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md) v2

若该论文是综述/路线图，且主要贡献在于建立专题顶层架构而非提供新的具体技术演示：
- 使用 `meta.contribution_type: framework`
- 优先定义 Level 0/1 顶层实体、tier: meta/domain 原理、跨专题 `CONDITIONED-BY` 接口
- 不把具体实验系统的 Level 2 参数实例作为该文件的主职责

若该论文是 `evidence` 档（最常见）：
- 优先复用已有节点，不强求新增 `pri.*`
- 允许不填 `breakthrough_paths`，允许产出 orphan 节点
- 详见 [CONTRIBUTING.md "Evidence 档位最低入库门槛"](CONTRIBUTING.md)

### 步骤 5：写入文件

写入 `topics/<topic>/papers/{first_author_lower}{year}.yaml`，例如 `topics/ultrastable-laser/papers/matei2017.yaml`。

当前默认专题为 `ultrastable-laser`。

### 步骤 6：更新运维文件

- 在 `PROCESSED_PAPERS.md` 中补充论文记录
- 更新 `INDEX.md`（新节点、新指标最佳值、论文计数）
- 追加 `LOG.md` 条目（格式：`## [YYYY-MM-DD] ingest | description`）
- 若新数据与已有声明矛盾，更新相关节点的 `contested_claims` 并在 LOG.md 记录 `contradiction`
- 若存在相关综合页面（`synthesis/`），检查是否需要标注为"需要更新"

### 步骤 7：提交

```bash
git add topics/<topic>/papers/{filename}.yaml PROCESSED_PAPERS.md INDEX.md LOG.md
git commit -m "add {author}{year}: {论文核心贡献一句话}"
git push
```

---

## 质量检查清单

提交前确认：

- [ ] 每个节点 ID 全局唯一（不与同专题 papers/ 目录及其他专题的文件冲突）
- [ ] 所有 relation 有 `source.claim`（原文论断）
- [ ] 所有 metric 的 `demonstrated_value` 有 `conditions`
- [ ] 原理节点有 `conditions` 或 `applicable_when`
- [ ] 跨文件引用的节点在 `note` 中注明来源文件
- [ ] 没有把"方法"建为"实体"（PDH 是 `meth`，不是 `ent`）

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
