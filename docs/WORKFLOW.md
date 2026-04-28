# 知识库操作流程指南

> 本文档说明 sci-logic-kb 日常操作的核心流程，面向所有参与者。

## 文档定位

| 文档 | 用途 |
|------|------|
| 本文档 (WORKFLOW.md) | **操作流程** —— 我该按什么顺序做什么事 |
| [SCHEMA.md](../SCHEMA.md) | **规范真源** —— 节点、关系、字段的定义 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | **质量门** —— 提交前的完整 checklist |
| [CLAUDE.md](../CLAUDE.md) | **AI 协作规范** —— AI agent 的行为约束 |

---

## 一、新增单篇论文（最常见）

### 1.1 准备阶段

```bash
# 确认工作目录
cd /home/ubuntu/sci-logic-kb

# 从 GitHub 拉取最新版本
git pull origin main

# 确认专题归属（超稳激光 / 光学频率梳 / ...）
# 查看专题列表和状态
cat TOPICS.md
```

### 1.2 获取论文 PDF

从 Zotero 获取论文（需要 Windows IP 和 Zotero Key）：

```bash
# 获取 Windows 主机 IP
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')

# 设置论文的 Zotero Key
ZOTERO_KEY="替换为实际KEY"

# 获取论文元数据
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('title','')); print(d.get('DOI',''))"

# 获取 PDF 路径
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

### 1.3 提取节点和关系

**关键判据（SCHEMA §1.4）**：

每个节点必须满足至少一条：
- 能独立回答一类查询
- 拥有独立的设计选择空间
- 会被多篇论文复用
- 拥有独立的限制链/证据链

**贡献类型判定（v4.4）**：

```yaml
meta:
  contribution_type: evidence  # 默认，占大多数
  # breakthrough: 打破指标记录 / 提出新原理 / 证伪旧论断
  # framework: 综述 / 路线图 / 教科书章节
```

**超稳激光专题特殊规则（σ_y-first）**：
- 优先识别 σ_y(τ=1 s) 值
- 必须标注 Allan 变体类型（ADEV/MDEV/OADEV/Hadamard）
- 只有线宽则不能升 breakthrough

### 1.4 创建 YAML 文件

```bash
# 文件命名：{first_author_lower}{year}.yaml
# 位置：topics/<topic>/papers/

# 示例：
# topics/ultrastable-laser/papers/matei2017.yaml
# topics/optical-frequency-combs/papers/diddams2000.yaml
```

**最小结构**：

```yaml
# Schema版本：v4.5

meta:
  zotero_key: "XXXXXXXX"
  topic: "ultrastable-laser"
  source_type: "peer_reviewed_paper"
  contribution_type: "evidence"
  title: "论文标题"
  year: 2017
  first_author: "Matei"
  doi: "10.1103/PhysRevLett.118.263202"

entities:
  ent.example_system:
    name: "示例系统"
    tier: implementation
    level: 2
    note: "简要描述"

relations:
  - id: rel.M01
    type: CHARACTERIZED-BY
    subject: ent.example_system
    object: met.example_metric
    source:
      claim: "原文中的论断"
      zotero_key: "XXXXXXXX"
      page: 3
```

### 1.5 本地验证（必须全过）

```bash
# 1. 语法和完整性检查（权威）
python scripts/lint.py --summary

# 2. 统计指标检查（不倒退）
python scripts/stats.py

# 3. 重建索引
python scripts/build_index.py
```

### 1.6 更新运维文件

```bash
# 1. 追加已处理论文记录
echo "| First Author | Year | Title | Zotero Key | DOI | Topic | Status |" >> PROCESSED_PAPERS.md
# （填写实际信息）

# 2. 追加演化日志
cat >> LOG.md << EOF
## [$(date +%Y-%m-%d)] ingest | {author}{year}: {核心贡献一句话}
EOF

# 3. 检查 synthesis/ 页面是否需要更新
```

### 1.7 提交到 GitHub

```bash
# 添加文件
git add topics/<topic>/papers/{filename}.yaml
git add PROCESSED_PAPERS.md LOG.md
git add INDEX*.md topics/*/INDEX.md docs/CURRENT_NODES_REFERENCE.md

# 提交
git commit -m "add {author}{year}: {论文核心贡献一句话}"

# 推送（需要认证）
git push origin main
```

---

## 二、批量处理论文

### 2.1 使用队列文件

```bash
# 创建或编辑队列
cat > QUEUE.md << EOF
# 待处理论文队列

- [ ] Author1 (2020) - Zotero Key: ABC123 - Topic: ultrastable-laser
- [ ] Author2 (2021) - Zotero Key: DEF456 - Topic: optical-frequency-combs
EOF
```

### 2.2 GitHub Copilot 优先原则

根据 CLAUDE.md，优先使用 GitHub Copilot 完成：
- 代码生成（YAML 模板、脚本）
- 文档撰写
- 基于已有模式的重复性工作

仅在以下情况使用本地 Claude Code：
- 需要读取本地 PDF
- 需要调用本地工具
- 需要交互式探索和决策

---

## 三、专题管理

### 3.1 查看专题状态

```bash
# 查看所有专题
cat TOPICS.md

# 查看专题详细架构
cat topics/ultrastable-laser/_meta/architecture.md
cat topics/optical-frequency-combs/_meta/architecture.md

# 查看专题索引
cat topics/ultrastable-laser/INDEX.md
```

### 3.2 专题健康检查

```bash
# 运行统计脚本
python scripts/stats.py

# 查看孤立节点
grep -r "orphan" topics/*/papers/*.yaml

# 查看争议性论断
grep -r "contested_claims" topics/*/papers/*.yaml
```

---

## 四、日常维护

### 4.1 三个最常用命令

```bash
# 1. 质量检查
python scripts/lint.py --summary

# 2. 统计报告
python scripts/stats.py

# 3. 重建索引
python scripts/build_index.py
```

### 4.2 索引文件说明

**自动生成文件（不要手工编辑）**：
- `INDEX.md` - 全局导航
- `INDEX_metrics.md` - 指标快查
- `INDEX_principles.md` - 原理快查
- `docs/CURRENT_NODES_REFERENCE.md` - AI 摄入推荐入口
- `topics/*/INDEX.md` - 各专题索引

### 4.3 检查入库论文

```bash
# 使用入库论文参考索引
cat paper-inkb.md

# 或在已处理列表中查找
cat PROCESSED_PAPERS.md | grep "关键词"
```

---

## 五、故障排查

### 5.1 Git 操作失败

```bash
# 确认远程地址
git remote -v

# 重新设置远程地址
git remote set-url origin https://github.com/hjiang555-a11y/sci-logic-kb.git

# 配置认证（使用 token）
git config credential.helper store
```

### 5.2 Zotero 连接失败

```bash
# 检查 Windows IP
ip route | grep default | awk '{print $3}'

# 测试连接
curl -s "http://${WINDOWS_IP}:23119/api/users/19944378/items?limit=1"
```

### 5.3 脚本执行错误

```bash
# 检查 Python 环境
python --version

# 检查依赖
pip list | grep -E "(yaml|pyyaml)"

# 查看脚本帮助
python scripts/lint.py --help
python scripts/stats.py --help
```

---

## 六、最佳实践

### 6.1 提交前检查清单

- [ ] `python scripts/lint.py --summary` 零错误
- [ ] `python scripts/stats.py` 指标不倒退
- [ ] 所有 relation 有 `source.claim`
- [ ] 节点 ID 全局唯一
- [ ] 运维文件已更新（PROCESSED_PAPERS.md、LOG.md）

### 6.2 协作原则

1. **GitHub 优先**：完成后立即同步到 GitHub
2. **质量优先**：宁可少摄入，不要降低质量
3. **文档限定**：遵循专题的 scoping_principles.md
4. **问题先行**：不确定时先提 issue 或问专家

### 6.3 常见错误

❌ **不要**：
- 手工编辑自动生成的索引文件
- 把 PDF 存入知识库（通过 Zotero 查找）
- 把"方法"建为"实体"（PDH 是 meth，不是 ent）
- 盲目新建节点（先检查已有节点）

✅ **应该**：
- 先运行 `build_index.py` 查看已有节点
- 使用 `git pull` 保持同步
- 提交前运行三个验证命令
- Evidence 档论文允许产出 orphan 节点

---

## 七、角色分工

| 角色 | 职责 | 主要工作 |
|------|------|----------|
| **Domain Expert** | 策展与提问 | 选择论文、确认节点边界、审核争议、决定 Schema 方向 |
| **AI Agent** | 簿记与维护 | YAML 提取、交叉引用、INDEX 更新、一致性检查 |
| **GitHub Copilot** | 代码生成 | YAML 模板、脚本、文档撰写、重复性工作 |
| **Claude Code** | 本地处理 | PDF 阅读、本地工具调用、交互式探索 |

---

## 附录：快速参考

### 文件路径模板

```
topics/<topic>/papers/{first_author_lower}{year}.yaml
topics/<topic>/_meta/architecture.md
topics/<topic>/_meta/scoping_principles.md
topics/<topic>/synthesis/*.md
```

### 节点 ID 命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 实体 | `ent.{描述词}_{后缀}` | `ent.fp_cavity_system` |
| 原理 | `pri.{描述词}` | `pri.brownian_thermal_noise` |
| 方法 | `meth.{描述词}` | `meth.pdh_locking` |
| 指标 | `met.{描述词}_{后缀}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{首字母}{序号}` | `rel.M01` |

### 关系类型速查

- `PART-OF`: 部件-系统
- `CHARACTERIZED-BY`: 实体-指标
- `BOUNDED-BY`: 方法/指标-限制原理
- `ENABLED-BY`: 方法/指标-使能原理
- `OPERATIONALIZED-AS`: 原理-方法

---

*最后更新：2026-04-28*
*版本：v1.0*
