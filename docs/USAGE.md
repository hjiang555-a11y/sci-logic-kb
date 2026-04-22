# 使用指南 — How to Query sci-logic-kb as a Researcher

> 这份文档解决一个问题：**作为时间频率计量领域的研究者，我要怎么"用"这个知识库？**
>
> 它不是 Schema（→ [SCHEMA.md](../SCHEMA.md)），也不是建设规范（→ [CONTRIBUTING.md](../CONTRIBUTING.md)），更不是审核入口（→ [REVIEW_GUIDE.md](REVIEW_GUIDE.md)），而是**读者视角的导航手册**。

---

## 三种典型使用场景

### 场景 A · 我要设计一套新的超稳激光装置，需要选择技术路线

**三跳查询路径**：

1. **从限制出发**（第 1 跳）  
   打开 [`topics/ultrastable-laser/_meta/architecture.md`](../topics/ultrastable-laser/_meta/architecture.md) 的"限制↔路径↔论文"三栏对照表，找到你的目标稳定度对应的**主导限制**（如 10⁻¹⁷ 量级 → 布朗热噪声）

2. **展开路径**（第 2 跳）  
   打开 [`synthesis/breakthrough_paths_matrix.md`](../topics/ultrastable-laser/synthesis/breakthrough_paths_matrix.md)，沿"限制 × 条件"矩阵定位已演示的路径组合，评估工程代价与收益

3. **对齐到论文**（第 3 跳）  
   对感兴趣的单元格（如 "Si 17 K + AlGaAs 镀层"），追溯到代表论文（如 Lee 2026），打开 `topics/ultrastable-laser/papers/lee2026.yaml` 查看细节、参数、限制、后续空间

**示例查询**："我想设计 10 cm ULE 腔，室温，目标 σ_y(1s) < 5×10⁻¹⁶，从哪里开始？"  
→ 三栏表 → 热噪声限制 + 晶体镀层路径 → Cole 2013 的 `ent.algaas_crystalline_mirror_c13` + 相关振动不敏感几何（Webster 2011 / Chen 2020）

---

### 场景 B · 我的实验 σ_y 卡在某个数值，需要诊断瓶颈

**三跳查询路径**：

1. **从指标出发**（第 1 跳）  
   打开根目录 [`INDEX_metrics.md`](../INDEX_metrics.md)，按指标类型（线宽 / 分数频稳 / 加速度灵敏度 / …）找到已知的最佳值与典型值，评估你的数值处在什么分位

2. **反向追溯限制**（第 2 跳）  
   每个 YAML 文件的 `metrics` 条目包含 `BOUNDED-BY` 或相关 `sources`；或打开对应 synthesis 页面的"误差预算"表格（如 [`ram_and_pdh_error_budget.md`](../topics/ultrastable-laser/synthesis/ram_and_pdh_error_budget.md)）

3. **读开放问题**（第 3 跳）  
   每篇论文 YAML 的 `open_questions` 与 `contested_claims` 字段是你诊断时的"候选嫌疑人列表"——它们记录了领域内还未解决或有争议的点

**示例查询**："我的 FP 腔系统 σ_y 卡在 1×10⁻¹⁶，无法下降，是不是 RAM？"  
→ `synthesis/ram_and_pdh_error_budget.md` 的误差预算表 → Zhang 2014 的 RAM 分数频稳公式 σ_y = σ_RAM · κ / ν → 估算你的 RAM 贡献

---

### 场景 C · 我在写综述或申请书，需要历史演化脉络

**三跳查询路径**：

1. **从时间线出发**（第 1 跳）  
   打开 [`synthesis/stability_record_timeline.md`](../topics/ultrastable-laser/synthesis/stability_record_timeline.md) 或相应专题的 `synthesis/*_roadmap.md`

2. **按分支分主题**（第 2 跳）  
   根据综述重点选择对应 synthesis 页：
   - 低温 → `cryogenic_roadmap.md`
   - 光纤稳频 → `fiber_stabilization_landscape.md`
   - 振动设计 → `vibration_insensitivity_landscape.md`
   - SHB 旁路 → `spectral_hole_burning_track.md`

3. **引用标准节点**（第 3 跳）  
   所有 synthesis 页引用的 `ent.*` / `pri.*` / `meth.*` / `met.*` ID 都可通过全文 grep 定位 YAML 源文件，从而拿到论文引用、年份、DOI 等

---

## 其他常用入口

| 我想… | 入口文件 |
|-------|---------|
| 看专题总览 | [`TOPICS.md`](../TOPICS.md) |
| 看所有节点/关系（按类型） | [`INDEX.md`](../INDEX.md)、[`INDEX_metrics.md`](../INDEX_metrics.md)、[`INDEX_principles.md`](../INDEX_principles.md) |
| 看知识库演化日志 | [`LOG.md`](../LOG.md) |
| 看已处理论文清单 | [`PROCESSED_PAPERS.md`](../PROCESSED_PAPERS.md) |
| 看尚未修复的问题 | [`TODO.md`](../TODO.md) |
| 跑统计/健康检查 | `python scripts/stats.py` / `python scripts/lint.py` |

---

## 查询小技巧

- **按节点 ID 找来源论文**：`grep -r "ent.fp_cavity_system" topics/` → 列出所有定义或引用该节点的 YAML
- **按物理关键词定位 synthesis 页**：所有 synthesis 页的 header 都列出了涉及的源文件，反查快
- **按年份排序**：INDEX 文件自动按 ID 排序；若要按年份，用 YAML 的 `meta.year` 字段 `grep -l "year: 201" topics/<topic>/papers/`
- **矛盾/争议定位**：`grep -r "contested_claims\|open_questions" topics/` → 直接定位领域内未解问题

---

## Synthesis 页新鲜度机制（v4.5+）

Synthesis 页依赖的 paper YAML 更新后，Synthesis 页可能需要随之刷新。仓库的自动化会**在 PR 上自动提示**：

- 触发：任意 PR 修改 `topics/**/*.yaml` 或 `topics/**/*.md`
- 检查：`scripts/freshness.py --check --json` 基于 **git log 提交时间戳**（非 `mtime`）对比 YAML 和 synthesis 页的新旧
- 提示方式：
  - 若某 synthesis 页有更新的 YAML，但本 PR **未同时修改该 synthesis 页** → PR 自动获得 `needs-refresh` 标签，并收到一条 sticky comment 列出受影响页面和触发 YAML
  - 若同一 PR 已经在修改该 synthesis 页，则视为"已响应"，不加标签
- 标签不会阻塞合并；由维护者决定合并前修复还是合并后跟进。

本地预览：`python scripts/freshness.py --check` 或 `python scripts/freshness.py --list`（结构化：`--json`）。

---

## 本指南的定位

- 这是**读者视角**文档，不规定如何摄入论文（→ CONTRIBUTING.md）
- Synthesis 页可能过时（见每页 header 的"最后更新"），以 YAML 为准
- 如发现查询路径缺失（例如你想做的查询没有对应的 synthesis 页），欢迎提 issue 请求新建
