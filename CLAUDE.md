# Claude Code 行为规范 — sci-logic-kb

本文件是 Claude Code 在此仓库中工作时的行为规范。

## 仓库用途

**时间频率计量科研知识库**（v5.0 双层架构）。
- **事实层（v4.5）**：从论文 PDF 中提取结构化知识，存储为 YAML 节点图（topics/*/papers/*.yaml）
- **推理层（v5.0）**：因果推理链和共识报告，叠加在事实层之上（logic/chains/, consensus/, evidence/）

- **操作流程**：[docs/WORKFLOW.md](docs/WORKFLOW.md)
- **质量门**：[CONTRIBUTING.md](CONTRIBUTING.md)
- **Schema 规范**：[SCHEMA.md](SCHEMA.md)（v5.0 架构见 §十一）
- **专题体系**：[TOPICS.md](TOPICS.md)
- **档位判定**：[docs/CONTRIBUTION_TIER_RULES.md](docs/CONTRIBUTION_TIER_RULES.md)
- **推理链规范**：[docs/v5/PLAN.md](docs/v5/PLAN.md) · [CONTRIBUTING.md §推理链贡献](CONTRIBUTING.md)

---

## 核心规则速查

> 以下为 AI agent 在 sci-logic-kb 操作时必须遵守的核心规则。
> 完整摄入流程见 [docs/WORKFLOW.md](docs/WORKFLOW.md)，完整质量门见 [CONTRIBUTING.md](CONTRIBUTING.md)。

### 贡献类型判定（v4.5）

- `evidence`: 默认，占大多数。允orp新han/chain-gap，不强求补 `breakthrough_paths`
- `breakthrough`: 打破指标记录/提出新原理/证伪旧论断
- `framework`: 综述/路线图/教科书章节
- 详细边界裁决见 [docs/CONTRIBUTION_TIER_RULES.md](docs/CONTRIBUTION_TIER_RULES.md)

### 超稳激光专题专属规则

- σ_y(1 s) 单一主线（ADEV/MDEV/OADEV/Hadamard 等价）
- 线宽/频噪 PSD/相干时间单独刷新一律归 `evidence`
- 详见 `topics/ultrastable-laser/_meta/scoping_principles.md`

### 节点新建判据

至少满足一条：能独立回答一类查询 / 拥有独立设计选择空间 / 会被多篇论文复用 / 拥有独立限制链或证据链

### 已有节点速查

处理新论文前优先查阅：
- [`docs/CURRENT_NODES_REFERENCE.md`](docs/CURRENT_NODES_REFERENCE.md) — 全专题节点一览
- [`INDEX_principles.md`](INDEX_principles.md) — 跨专题原理/方法
- 运行 `python scripts/build_index.py` 确保索引最新

### 人机分工

| 角色 | 职责 |
|------|------|
| **人类专家** | 选择论文、确认节点边界、审核争议、决定 Schema 方向 |
| **AI Agent** | YAML 提取、交叉引用维护、INDEX/LOG 自动更新、健康检查 |

详见 [CONTRIBUTING.md §AI-Human 协作契约](CONTRIBUTING.md)。

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
- **v5.0 推理层**：evidence 索引生成、逻辑链和共识报告的编写与验证

即：**与知识库内容相关的所有操作**。

---

## v5.0 推理层操作规范

### 核心命令

```bash
python scripts/build_evidence_index.py --topic <topic>     # 生成证据注册表
python scripts/validate_chains.py                           # 验证推理链引用
python scripts/reasoning_stats.py                           # 推理就绪度量
python scripts/generate_consensus.py --topic <topic> --dry-run  # 共识报告预览
```

### 推理链编写规则

1. `limiting_principle.id` 必须以 `pri.` 开头，且在 v4.5 YAML 中已定义
2. `evidence[].relation_id` 必须是 v4.5 中实际的 relation ID（如 `rel.kessler_2012_06`）
3. 每条推理链回答一个核心问题，用 `breakthrough_narrative` 写 >=50 词因果叙述
4. 运行 `validate_chains.py` 验证后方可提交

### v5.0 目录约定

- `evidence/` — 脚本自动生成，不可手工编辑
- `logic/chains/` — 人工编写，每文件一条链
- `consensus/` — 人工编写，每文件一个指标
- `docs/v5/` — v5.0 计划与阶段文档

