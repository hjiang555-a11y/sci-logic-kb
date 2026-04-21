# TODO — 知识库待处理工作登记

> **定位**：集中登记各专题尚未完成的结构化工作，避免分散遗忘。
>
> **维护原则**：
> - 本文件是"导航器"，具体细节链接到 `reports/` 或 issue
> - 每完成一项更新对应状态 / 同步 LOG.md
> - 新增待办请加到对应专题段落，严重缺口请同时在 TOPICS.md 降级对应专题优先级

---

## 📌 当前优先级：阶段 A（机制落地闭环）进行中 — A1+A2 已交付，等待专家裁决触发 A3/A4

> **v4.4 机制落地进度（2026-04-21）**：按"先形成工作机制再扩展规模"迭代计划：
>
> - ✅ **阶段 A1**：档位分级操作规则书 → [`docs/CONTRIBUTION_TIER_RULES.md`](docs/CONTRIBUTION_TIER_RULES.md)（含"专题级偏好"索引节）
> - ✅ **阶段 A2 · Round 1**：78 篇档位建议草案（🟥 16 / 🟧 17 / 🟦 3 / 🟩 42）
> - ✅ **阶段 A2 · Round 2**：专家增补**专题原则"稳定度 > 线宽"**（见 [`topics/ultrastable-laser/_meta/scoping_principles.md`](topics/ultrastable-laser/_meta/scoping_principles.md)），清空 🟧 档——8 升 🟥 / 9 降 🟩。新分布 🟥 24 / 🟦 3 / 🟩 51 → [`reports/contribution_tier_draft_ultrastable.md`](reports/contribution_tier_draft_ultrastable.md)
> - ⏳ **阶段 A3**：等待专家批量 accept / override（Round 2 表）
> - ⏳ **阶段 A4**：AI 回写 78 篇 YAML 的 `meta.contribution_type`（机械改动，依赖 A3）
> - ⏳ **阶段 B**：lint / stats 引入档位感知 → 重跑 chain-gap / orphan 报告（依赖 A4）
> - ⏳ **阶段 C**：针对真缺口做精准收敛（依赖 B）
> - ⏳ **阶段 D**：沉淀专题整治手册，再启动其他专题扩展
>
> **重要提示**：本节后续 chain-gap / orphan / 复用度数字是在"所有论文都需补限制链"旧预设下统计的；阶段 B 完成后，真实缺口大概率显著低于当前数字，届时以 B 的重估结果为准。

### 超稳激光（重点整治专题）

#### P0 · Chain-gap 闭环（21 条 → 目标 ≤ 3）
- 详见 [`reports/chain_gap_ultrastable.md`](reports/chain_gap_ultrastable.md)
- 🟢 批量可补（~14 条）：由 AI 按 P0 模板批量提 PR，专家审核合并
- 🟡 精修（4 条）：RAM 相关 + 父节点（legero2010 / tai2017 / webster2008）
- 🟣 专家裁决（3 条）：didier2018 / grabielle2025 / li2019

#### P1 · Orphan 收敛（90 → 目标 ≤ 30）
- 详见 [`reports/orphans_ultrastable.md`](reports/orphans_ultrastable.md)
- 优先文件：chen2020 / chen2025 / hafner2020 / jin2018 / kedar2023 / lee2026
- 需要专家在桶 A / B / C 间做归属决策

#### P2 · 跨文件复用度提升（8.8% → 15%+）
- 待抽取：10~15 个公共 pri.* / meth.*（如 `pri.brownian_thermal_noise_fdt`、`meth.pdh_locking`、`pri.cavity_deformation_compensation`）
- 需要专家确认哪些节点应提升为"公共节点"（可留在专题内，也可上提到 `topics/shared/`）

#### P3 · Synthesis 页面数值复核（已完成 8 篇，全部标 🟡 draft）
- [ ] `vibration_insensitivity_landscape.md` — 需核对 κ 数值
- [ ] `ram_and_pdh_error_budget.md` — 需核对 RAM 分数频稳典型贡献
- [ ] `fiber_stabilization_landscape.md` — 需核对光纤稳频最佳值时间线
- [ ] `cryogenic_roadmap.md` — 需核对 Si 腔最佳 σ_y 对应论文
- [ ] `spectral_hole_burning_track.md` — SHB 分支整体结构化最弱，需专家深度参与
- [ ] `breakthrough_paths_matrix.md` — 待 chain-gap 修复后刷新单元格状态

---

### 光学频率梳（已入库待深化）

- [ ] 修 36 条低成本 lint warnings（主要是 `missing-conditions`）
- [ ] 其他整固（orphan、chain-gap）延后到未来轮次
- [ ] 无综合页面（`synthesis/`），未来可参考超稳激光专题模式补建

---

### 频率标准（骨架）

> **状态**：仅接受新摄入，不投入整治资源
- [ ] 摄入 ≥ 3 篇代表论文（光钟类：Sr、Yb、Hg、Al⁺；微波类：Cs fountain、H-maser）
- [ ] 激活 Level 1 实体节点

---

### 时间标尺与钟组（骨架）

> **状态**：仅接受新摄入
- [ ] 摄入 UTC/TAI 综述、本地 UTC(k) 实现、Kalman 合成算法论文

---

### 时间频率传递（骨架空壳）

> **状态**：0 论文，仅架构占位
- [ ] 摄入 ≥ 3 篇代表论文：光纤相干链路 + TWSTFT + GNSS 载波相位比对
- [ ] 激活 Level 1 实体节点

---

### 时频计量数学基础（未建）

> **状态**：架构未启动
- [ ] 确定是作为独立专题还是放在 `topics/shared/metrics/`
- [ ] 摄入基础方差体系论文（Allan, Hadamard, Mod-σ, Dynamic Allan, …）

---

## 🛠️ 开发 / 工具 / CI

### Round 4 延后项
- [ ] CI 集成 freshness 检查：synthesis 页面依赖的 yaml 更新时自动标 `needs-refresh` 标签
- [ ] 探索 graph.py 输出的交互式可视化（d3 / cytoscape）

---

## 📋 Schema / 架构层面

- [ ] 评估是否需要新增"`status: resolved`"字段到 BOUNDED-BY 关系（当限制已被工程超越时）
- [ ] 评估 `INSTANCE-OF` 是否作为正式谓词（或继续用 `PART-OF` 表示 Level 2 参数变体）
- [ ] 评估 `SHARED-WITH` 关系的使用规范（当前零使用，需要实际案例触发规则定稿）

---

> 本文件随工作推进持续更新；每次 PR 合并后请检查并勾选 / 删减对应条目，保持 TODO 长度收敛。
