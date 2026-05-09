# reports/ — 报告索引与分层约定

> **用途**：本目录存放所有过程性 / 诊断性 / 规划性文档。主数据（YAML 节点）与自动索引（`INDEX*.md`）不在此。
>
> **分层约定**（P0 · 2026-04-24 落地）：
>
> | 子目录 | 用途 | 是否仍驱动决策 |
> |--------|------|----------------|
> | `active/` | 仍在驱动整治工作的诊断 / 规划报告 | ✅ 是 |
> | `archive/` | 已完成其历史使命的一次性报告、backup、过期 JSON | ❌ 否（仅存档） |
> | `generated/` | 脚本输出的一次性中间产物（stats dump、tmp JSON 等） | 按需再生，可删 |
>
> **新增报告请放入对应子目录**，不要再往 `reports/` 根部新增文件，也不要往仓库根目录新增一次性报告（见 [`CONTRIBUTING.md` §根目录约定](../CONTRIBUTING.md)）。

---

## 1. Active — 仍有效

长期有效的诊断报告，新论文入库 / schema 升级时应重新评估。

### 1.1 超稳激光专题（ultrastable-laser）

| 文件 | 说明 |
|------|------|
| [`active/chain_gap_ultrastable.md`](active/chain_gap_ultrastable.md) | 限制链缺口清单（Round 1） |
| [`active/chain_gap_ultrastable_v2.md`](active/chain_gap_ultrastable_v2.md) | 限制链缺口（v2，档位感知重估） |
| [`active/orphans_ultrastable.md`](active/orphans_ultrastable.md) | Orphan 节点收敛清单（Round 1） |
| [`active/orphans_ultrastable_v2.md`](active/orphans_ultrastable_v2.md) | Orphan 节点（v2，档位感知重估） |
| [`active/contribution_tier_draft_ultrastable.md`](active/contribution_tier_draft_ultrastable.md) | contribution_type 档位草案 |
| [`active/metric_chains_ultrastable-laser.md`](active/metric_chains_ultrastable-laser.md) | **Curated metric chains**（样板报告，按限制链分组，非组合生成） |

### 1.2 跨专题

| 文件 | 说明 |
|------|------|
| [`active/shared_node_candidates.md`](active/shared_node_candidates.md) | 跨文件复用候选节点 |
| [`active/knowledge_base_assessment_report.md`](active/knowledge_base_assessment_report.md) | 知识库总体评估（v4.4 旧快照，待归档） |
| [`active/project_alignment_assessment_2026-05-07.md`](active/project_alignment_assessment_2026-05-07.md) | **2026-05-07 · 项目整合与对齐评估**（SCHEMA v5.0 → 周边文档漂移诊断 + 三阶段执行清单） |
| [`active/llm_wiki_analysis.md`](active/llm_wiki_analysis.md) | LLM Wiki 模式分析（v4.2 运维层设计依据） |

### 1.3 Ingest plan（待处理论文候选）

| 路径 | 说明 |
|------|------|
| [`active/ingest_plan/`](active/ingest_plan/) | Stage-1/2 候选筛选表、批次切分 |

### 1.4 光频梳专题（optical-frequency-combs）

| 文件 | 说明 |
|------|------|
| [`active/metric_chains_optical-frequency-combs.md`](active/metric_chains_optical-frequency-combs.md) | **Curated metric chains**（多轨道报告，9 条独立子域轨道） |
| [`../topics/optical-frequency-combs/synthesis/a1_femtosecond_comb_platforms_timeline.md`](../topics/optical-frequency-combs/synthesis/a1_femtosecond_comb_platforms_timeline.md) | A1 锁模梳平台演进时间线 |
| [`../topics/optical-frequency-combs/synthesis/b_dcs_dual_comb_spectroscopy.md`](../topics/optical-frequency-combs/synthesis/b_dcs_dual_comb_spectroscopy.md) | B-DCS 双梳光谱技术与应用 |
| [`../topics/optical-frequency-combs/synthesis/b_freqsyn_frequency_synthesis.md`](../topics/optical-frequency-combs/synthesis/b_freqsyn_frequency_synthesis.md) | B-FreqSyn 频率综合与微波链路 |
| [`../topics/optical-frequency-combs/synthesis/a2_dks_microcombs.md`](../topics/optical-frequency-combs/synthesis/a2_dks_microcombs.md) | A2-DKS 耗散 Kerr 孤子微梳 |

---

## 2. Archive — 已归档

历史过程材料，仅保留做可追溯性。新工作不要再依赖这些文档。

### 2.1 Obsidian 同步记录

`archive/obsidian-sync/` —— Zotero/Obsidian 对接过程中产生的一次性同步报告：

- `SYNC_REPORT_OBSIDIAN_UPDATE.md`（首次同步）
- `SECOND_SYNC_REPORT_OBSIDIAN_UPDATE.md`
- `THIRD_SYNC_REPORT_OBSIDIAN_UPDATE.md`
- `SYNC_REPORT_OBSIDIAN_UPDATE_20260421_215834.md`
- `SYNC_REPORT_POST_PULL_20260421_220032.md`
- `SYNC_REPORT_OPTICAL_COMB_RESTRUCTURING.md`
- `ZOTERO_KEY_VALIDATION_REPORT.md`
- `ZOTERO_LINKAGE_AUTO_UPDATE_REPORT.md`
- `ZOTERO_LINKAGE_STATUS.md`
- `ZOTERO_OBSIDIAN_AI_INTEGRATION.md`
- `ZOTERO_OBSIDIAN_INTEGRATION_PLAN.md`
- `QUICK_START_ZOTERO_OBSIDIAN.md`
- `GUIDE_FUTURE_IMPORT.md`

### 2.2 历史 backup 与升级文档

`archive/` —— 仓库根文件的历史 backup 与已完成使命的升级指南：

- `.gitignore.backup` / `README.md.backup` / `SCHEMA.md.backup` / `TOPICS.md.backup`
- `v4.1_upgrade_guide.md`（v4.1 升级已完成）
- `copilot_batch_task.md` / `copilot_batch_upgrade_task.md`（历史批量任务提示词）
- `test_tasks_1.md` / `test_batch_v1.json` / `batch_upgrade_tasks.json`（测试批次）
- `OPTICAL_COMB_RESTRUCTURING_SUMMARY.md`（重构已合并，归档）
- `REORGANIZATION_PLAN.md`（阶段性计划已落地）
- `metric_chains_ultrastable-laser_v1_auto.md`（v1 自动生成版，591 组合链，已被 curated 版取代）

### 2.3 一次性 JSON

`archive/` —— Zotero 中间抽取产物，已用于一次性分析：

- `zotero_optical_comb_complete.json`
- `zotero_optical_comb_detailed.json`
- `zotero_optical_comb_stats.json`

---

## 3. Generated — 脚本生成

`generated/` —— 预留给脚本（`stats.py` / `lint.py` / `build_index.py` 等）输出的一次性产物。**不应手工编辑**。目前为空。

---

## 4. 新增报告归属决策树

```
要新写一份报告？
│
├── 它是一次性过程记录（同步、迁移、重构完成）吗？
│   └── ✅ 是 → 放入 archive/，命名含日期
│
├── 它是脚本输出的结构化数据吗？
│   └── ✅ 是 → 放入 generated/
│
├── 它会被后续工作持续引用 / 驱动决策吗？
│   └── ✅ 是 → 放入 active/
│
└── 以上都不是？
    └── 先问自己是否真的需要这份报告；需要的话放 active/，并在本 README 登记。
```

**仓库根目录永不新增一次性报告**。所有报告都应经由 `reports/` 子目录管理。

---

*索引首建：2026-04-24（TODO.md P0-1 落地）*
