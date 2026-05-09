# sci-logic-kb 网站部署方案

> 状态：需求确认中
> 架构：混合 — GitHub Pages 静态站 + 结构化查询层

---

## 一、用户与场景

| 角色 | 核心需求 | 页面 |
|------|----------|------|
| **科研人员** | 查指标值、看推理链、浏览论文 | Topics, Chains, Consensus, Search |
| **专题专家** | 审核 consensus 值、补 breakthrough_paths | Dashboard(质量报告), Consensus |
| **维护者** | 看 ingest 进度、lint 报告、更新状态 | Dashboard(运维), Diff |

---

## 二、站点地图

```
sci-logic-kb/
├── index.html              Dashboard — 知识库全景
│   ├── 统计卡片 (papers/nodes/relations/chains)
│   ├── 健康指示器 (lint errors, coverage %, warnings)
│   ├── 专题卡片 (6 topics, 论文数/指标数/限制数)
│   └── 最近更新 (latest ingest, chain changes)
│
├── topics/<topic>/         Topic 详情页 (×6)
│   ├── 指标表 (key metrics, 按年份排序)
│   ├── 论文表 (title, author, year, type, content status)
│   ├── 限制原理 (BOUNDED-BY summary)
│   └── 突破路径 (breakthrough_paths summary)
│
├── chains/                 Reasoning Chain 浏览器 (×12)
│   ├── 按专题分组
│   ├── 每条链: question → limiting_principle → edges → evidence
│   └── 因果边可视化 (ASCII图 or simple SVG)
│
├── consensus/              Consensus 时间线 (×7)
│   ├── 按专题分组
│   ├── 垂直时间线 (year, value, system, significance)
│   └── 趋势标注 (solved/active/emerging)
│
├── dashboard/              维护仪表盘 (公开)
│   ├── lint summary (errors/warnings/info by category)
│   ├── coverage (papers by topic, content %)
│   ├── chain validation status
│   ├── ingest progress (placeholder counters)
│   └── freshness (last updated timestamps)
│
├── graph/                  交互式知识图谱 (已有)
│   └── Cytoscape.js 可视化
│
├── search/                 全文搜索
│   └── 静态 JSON 索引 + 客户端搜索
│
└── api/
    └── data.json           全量结构化数据 (供查询/下载)
```

---

## 三、数据流

```
topics/*/papers/*.yaml  (事实真源)
        │
        ├──→ build_index.py      → INDEX*.md (已有)
        ├──→ build_site.py       → docs/site/ (静态HTML)
        │       ├── 读取所有 YAML
        │       ├── 读取 chains/*.yaml
        │       ├── 读取 consensus/*.yaml
        │       ├── 运行 lint.py --json (内嵌)
        │       ├── 运行 stats.py --json (内嵌)
        │       └── 生成 HTML + CSS + JSON
        │
        └──→ lint.py + stats.py  → dashboard 数据
```

---

## 四、技术选择

| 层 | 方案 | 理由 |
|----|------|------|
| **静态站点** | Python 生成纯 HTML + CSS | 零依赖，GitHub Pages 原生支持 |
| **样式** | 手写 CSS (无框架) | 页面简单，不需要 Bootstrap/Tailwind |
| **图表** | 纯 CSS 时间线 + 表格 | 内容为王，不需要 JS 图表库 |
| **搜索** | JSON 索引 + 客户端 fetch | 静态站可用的搜索方案 |
| **动态查询** | 预留 `/api/data.json` | 后续可接 FastAPI 或 Cloudflare Worker |
| **CI** | GitHub Actions weekly | 定时重建 + push 触发 |

---

## 五、页面详细设计

### 5.1 Dashboard (index.html)

```
┌─────────────────────────────────────────────┐
│  sci-logic-kb v5.0                          │
│  Time-frequency metrology knowledge base    │
├──────────┬──────────┬──────────┬────────────┤
│  530     │  1904    │  12      │  7         │
│  Papers  │  Nodes   │  Chains  │  Consensus │
├──────────┴──────────┴──────────┴────────────┤
│  Health: ✅ 0 errors · 95 warnings           │
│  Coverage: 99% papers · 100% evidence       │
├─────────────────────────────────────────────┤
│  Topics                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │   USL   │ │   OFC   │ │    FS   │  ...  │
│  │ 143 ppr │ │ 213 ppr │ │  73 ppr │       │
│  │ 55 lim  │ │ 97 lim  │ │  7 lim  │       │
│  └─────────┘ └─────────┘ └─────────┘       │
│                                             │
│  Recent Chains · Consensus · Updates        │
└─────────────────────────────────────────────┘
```

### 5.2 Topic Page (topics/ultrastable-laser/)

- Key metrics table (sorted by year, filtered by σ_y/instability)
- Paper table (with content status badges)
- BOUNDED-BY summary (limits by principle)
- Breakthrough paths list

### 5.3 Consensus Timeline

```
1966 ─── Allen variance defined
  │
1983 ─── PDH technique (Drever)
  │
1999 ─── Sub-Hz linewidth (Young)  ─ σ_y ≈ 3×10⁻¹⁶
  │
2012 ─── Si cavity @124K (Kessler) ─ σ_y ≈ 1×10⁻¹⁶
  │
2017 ─── Si3 @124K (Matei)         ─ σ_y = 4×10⁻¹⁷
  │
2026 ─── Si + AlGaAs @17K (Lee)    ─ σ_y = 2.5×10⁻¹⁷ ★ WORLD RECORD
```

### 5.4 Dashboard 指标

| 指标 | 来源 | 展示方式 |
|------|------|----------|
| Papers with content | stats.py | 进度条 |
| Lint errors/warnings | lint.py --json | 红/黄/绿 指示灯 |
| BOUNDED-BY closure rate | stats.py | 百分比 |
| Evidence coverage | stats.py | 百分比 |
| Chain validation | validate_chains.py | 通过/失败 |
| Consensus reports | count | 覆盖度 1/6→6/6 |
| Last rebuild | datetime | 时间戳 |

---

## 六、实施计划

| 阶段 | 内容 | 产出 |
|------|------|------|
| **P1** | `build_site.py` 核心生成器 | index + topics + chains + consensus |
| **P2** | Dashboard 页面 | lint/stats 集成 |
| **P3** | 搜索 + data.json API | 全文搜索 + 结构化数据下载 |
| **P4** | CI 定时重建 | weekly workflow |
| **P5** | 动态查询层 | 后续评估是否需要 |

---

## 七、待确认

1. 是否需要每个 paper 的独立详情页？（目前设计只到 topic 级聚合）
2. 搜索需要多深？（标题+作者 vs 全文指标值）
3. 时间线需要交互吗？（点击展开 vs 静态展示）
4. 需要中英文双语吗？
