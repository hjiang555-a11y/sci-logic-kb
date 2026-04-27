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

### 运维文件导航
- **全局导航索引**：[`INDEX.md`](INDEX.md)
- **演化日志**：[`LOG.md`](LOG.md)
- **已处理论文列表**：[`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md)
- **综合分析页面**：`topics/<topic>/synthesis/`
- **完整 Schema 规范**：[`SCHEMA.md`](SCHEMA.md)（第十节定义运维操作）

---

## 基础设施约束（v1 — 2026-04-26）

> Claude Code 在 sci-logic-kb 项目中操作时，必须遵守以下基础设施边界。

### 1. Dify 端口 — 不可变

Dify 是知识库对外服务的核心入口。Claude Code 不得修改任何涉及 Dify 端口、网络、路由的配置：

| 不可变参数 | 值 | 说明 |
|-----------|-----|------|
| Dify 监听端口 | `:8090` | Dify Nginx 容器内部 80→宿主 8090 |
| Dify 绑定地址 | `0.0.0.0:8090` | 不变 |
| Dify MCP 地址 | `http://localhost:8090` | Claude Code MCP 配置中已注册 |
| 业务端口 | `:8091` (Dify HTTPS) | 不变 |

**Claude Code 不得：**
- 修改 `/home/room115/dify/.env` 中的端口或网络配置
- 修改 `/home/room115/dify/docker-compose.yaml` 中的端口映射
- 停止、重启或修改 Dify 容器（除非你明确要求）
- 直接在 timefreq 上开放 Dify 端口到公网

### 2. FRP 隧道 — 不可变

FRP 隧道是 timefreq 对外服务的唯一通道：

| 隧道 | 本地端口 | 公网端口 |
|------|---------|---------|
| SSH | `:22` | `:60022` |
| Dify Web（预留） | `:8090` | `:8092` |

**Claude Code 不得：**
- 修改 `/opt/frp/frpc.toml` 中的任何配置
- 操作 FRP 客户端 systemd 服务

### 3. 公网入口 — 不可变

阿里云 ECS 和腾讯云安全组由外部分配：

| 入口 | IP | 用途 |
|------|-----|------|
| time-freq.top | 47.100.32.3 | 主站 |
| kb.time-freq.top | 47.100.32.3 | Dify 子域名（待配） |

**Claude Code 不得：**
- 修改阿里云 ECS 上的 Nginx 配置
- 修改 DNS 记录
- 修改腾讯云安全组规则

### 4. 知识库操作边界 — 可操作

Claude Code 在以下范围内可以自由操作：

| 目录/文件 | 权限 | 说明 |
|-----------|------|------|
| `/data/sci-logic-kb/topics/` | ✅ 读写 | YAML 论文提取 |
| `/data/sci-logic-kb/scripts/` | ✅ 读写 | 构建脚本、查询工具 |
| `/data/sci-logic-kb/docs/` | ✅ 读写 | 文档 |
| `/data/sci-logic-kb/reports/` | ✅ 读写 | 报告 |
| `/data/sci-logic-kb/SCHEMA.md` | ✅ 读写 | Schema规范 |
| `/data/sci-logic-kb/CLAUDE.md` | ✅ 读写 | 本文件 |
| `/home/room115/dify/` | ❌ 只读（如需查看） | Dify 配置 |
| `/opt/frp/` | ❌ 不可访问 | FRP 配置 |
| 阿里云 ECS 上的 Nginx/DNS | ❌ 不可访问 | 公网入口 |
| 腾讯云安全组 | ❌ 不可访问 | 防火墙 |

### 5. 异常处理

如果 Claude Code 在操作中发现需要修改基础设施配置才能完成任务：
1. 先记录需求（日志或注释）
2. 直接告诉我，由我决策后执行
3. 不得自行修改

### 6. 适用场景

本约束适用于下列任务类型：
- 知识库论文入库和 YAML 提取
- 知识库脚本开发和维护（query.py 等）
- 知识库质量检查和 lint 修复
- 知识库综合页面生成
- 通过 Dify MCP 接口查询知识库
- 与 GitHub 的代码同步

即：**与知识库内容相关的所有操作**。

