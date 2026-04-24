# 知识库部署方案评估（DEPLOYMENT_PLAN）

> **产出背景**：TODO.md P2-1 · 评估 GitHub Pages 只读发布方案
> **产出日期**：2026-04-24
> **当前默认部署**：GitHub 原生网页浏览（零配置）
> **目标**：为第二阶段的静态只读发布提供方案选型与落地清单

---

## 1. 现状：GitHub 原生浏览足以覆盖第一阶段

**结论：当前阶段不必迁移到 GitHub Pages，保持 GitHub 原生浏览即可。**

理由：

| 能力 | GitHub 原生 | 评估 |
|------|-----------|------|
| Markdown 渲染 | ✅ 自动 | 满足 |
| 表格 / Mermaid | ✅ 自动 | 满足（`docs/graph/index.html` 是 HTML，GitHub 不渲染但可下载） |
| 仓库内链接跳转 | ✅ 自动 | 满足 |
| YAML 高亮 | ✅ 自动 | 满足 |
| 可视化图谱（交互 HTML） | ⚠ 仅作为原始文件 | `docs/graph/index.html` 在 GitHub 上只能看源码，不能交互运行 |

**唯一真正的触发条件**：`docs/graph/index.html` 的交互式图谱只有上 Pages 后才能跑起来。

---

## 2. 第二阶段候选方案

### 方案 A：最小化 GitHub Pages（只发布 `docs/` 与选定子树）

**范围**：
- `docs/graph/`（交互式图谱）
- `docs/USAGE.md` / `docs/REVIEW_GUIDE.md` / `docs/CURRENT_NODES_REFERENCE.md`
- 根目录 `INDEX*.md`、`README.md`
- `reports/README.md`（报告索引）

**配置成本**：
- 在 `Settings → Pages` 启用，source 选 `main` branch `/docs` 目录 —— **但**当前根目录索引不在 `docs/` 下，需要加一层发布桥接。
- 方案 A-1（推荐）：启用 `branch: main, folder: /`，使用 Pages 默认 Jekyll 处理；`.nojekyll` 关闭 Jekyll 即可把仓库整体原样发布。
- 方案 A-2：加一个简单的 GitHub Actions 把需要发布的文件组装进 `gh-pages` 分支。

**优点**：零前端代码投入，保留当前仓库结构。
**缺点**：发布面较大（YAML 源文件也会被发布出去）——对只读知识库不是问题。

### 方案 B：静态站点生成器（MkDocs Material / VitePress / Docusaurus）

**范围**：生成一个导航式站点，含搜索、主题、侧边栏。

**适用时机**：当读者量增大，且 README / INDEX 结构不再能满足"检索 + 主题浏览"的诉求时再考虑。

**优点**：读者体验显著好于 GitHub 原生；支持全站搜索。
**缺点**：引入新工具链 + 每次 PR 需要重新构建；维护者角色增加。

### 方案 C：按需发布子集（docs/graph + README 摘要）

**范围**：只发布对外入口，源 YAML 不对外。

**优点**：最小披露面。
**缺点**：对本知识库意义不大——YAML 即知识源，遮蔽反而损害价值。

---

## 3. 推荐路径

| 时间 | 动作 | 触发条件 |
|------|------|----------|
| 当前 | 保持 GitHub 原生浏览 | — |
| 近期（本季度） | 方案 A-1：启用 Pages + `.nojekyll`，发布 `docs/graph/` 交互式图谱 | 若审阅者 / 读者要求图谱可交互 |
| 中期 | 方案 B：MkDocs Material | 若外部读者数 >10，或内部协作者反馈 GitHub 原生导航吃力 |
| 长期 | 不建议走方案 C | 本库的核心价值就是 YAML 源 |

---

## 4. 近期最小动作清单（方案 A-1 预备）

以下清单只在决定启用 Pages 时再执行，本 PR 不实施：

- [ ] 在仓库根添加空 `.nojekyll` 文件（禁止 Jekyll 二次处理，防止 `_` 开头目录被隐藏）
- [ ] `Settings → Pages` 选 `branch: main, folder: /`
- [ ] 在 `README.md` 顶部加 "🌐 在线阅读：<url>" 链接
- [ ] 确认 `docs/graph/index.html` 使用相对路径加载 `graph.json`（避免 Pages 路由问题）
- [ ] 首次发布后人工检查：（a）Mermaid 图是否可渲染（Pages 默认不渲染，需嵌入 JS）；（b）内部相对链接跳转是否正常

---

## 5. 维护者本地工作流不变

无论部署方式如何演进，**YAML 仍是 source of truth**。本地维护继续以脚本为核心：

```bash
python scripts/lint.py --summary
python scripts/stats.py
python scripts/build_index.py
```

呈现层（Pages / MkDocs）仅作"壳"，不改变知识的产生与审核流程。

---

## 6. P2-2 "查询者单页总入口"的状态

TODO.md P2-2 为条件式任务："若后续读者增多，再考虑"。

**当前判定**：不新建。理由：

- 目前根目录已有 `README.md` + `INDEX.md` + `docs/USAGE.md` 三层入口，不必叠加。
- 若将来上 Pages 后需要一个对外单页，优先由 Pages 主页承担，而非再向根目录增加文件。
- 触发条件（将来重新评估时采用）：外部读者反馈"找不到入口"，且反馈出现 ≥3 次。

---

*首建：2026-04-24（TODO.md P2-1 · 部署方案评估）*
