# 知识库演化日志

> **格式约定**：每条日志以 `## [YYYY-MM-DD] type | description` 开头。
> 支持的类型：`ingest`（摄入）、`restructure`（重组）、`lint`（健康检查）、`query`（查询反哺）、`contradiction`（矛盾发现）、`schema`（Schema 升级）、`synthesis`（综合页面）
>
> **使用方法**：`grep "^## \[" LOG.md | grep "contradiction"` 可快速定位矛盾点。

---

## [2026-04-20] restructure | P0 整固——自动化基础设施与度量体系

- **新增脚本**（5 个）：
  - `scripts/stats.py` — 6 项推理就绪度量（限制链闭环率、证据覆盖率、条件完备率、跨文件复用度、综合覆盖、矛盾可见度）
  - `scripts/lint.py` — 11 项健康检查（孤立节点、悬空引用、重复定义、推理链缺口等）
  - `scripts/build_index.py` — 从 YAML 自动生成分层 INDEX（替代手工维护）
  - `scripts/graph.py` — 知识图谱导出（JSON/GraphML）+ hub/orphan/bridge 诊断
  - `scripts/freshness.py` — 综合页面新鲜度追踪
- **分层索引**：INDEX.md 改为脚本自动生成 + 新增 INDEX_metrics.md、INDEX_principles.md、各专题 INDEX.md
- **专题元数据**：每个专题新增 `_meta/architecture.md`（架构图、限制链、路线图）
- **CI 集成**：新增 `.github/workflows/kb-lint-stats.yml`（PR 时自动运行 lint + stats）
- **Baseline 度量**（2026-04-20，141 篇论文 / 869 节点 / 957 关系）：

| 度量 | 当前值 | 目标 | 状态 |
|------|--------|------|------|
| 限制链闭环率 | 71.3% (87/122) | ≥70% | ✅ |
| 证据覆盖率 | 86.9% (832/957) | ≥90% | ❌ |
| 条件完备率 | 94.8% (220/232) | ≥80% | ✅ |
| 跨文件复用度 | 8.8% (76/862) | higher | — |
| 综合页面覆盖 | 1/4 专题 | 全覆盖 | ⚠️ |
| 矛盾可见度 | 119 (6 contested + 113 open_q) | more | — |

- **Lint baseline**：198 errors (5 dangling-ref + 21 duplicate-def + 172 duplicate-rel-id), 294 warnings
- **图谱诊断**：113 孤立节点，hub 节点前3: ent.fp_cavity_system (75度), ent.optical_frequency_comb (56度), ent.microresonator_frequency_comb (37度)

## [2026-04-20] restructure | 引入 Karpathy LLM Wiki 运维层

- 新增 `INDEX.md`（全局导航索引）、`LOG.md`（本文件）、`PROCESSED_PAPERS.md`（论文详细列表）
- 新增 `topics/ultrastable-laser/synthesis/` 综合分析页面目录（首批 2 个页面）
- SCHEMA.md 新增第十节「知识库运维操作」（Ingest/Query/Lint 工作流形式化）
- SCHEMA.md 第八节精简（详细论文列表迁移至 PROCESSED_PAPERS.md）
- CLAUDE.md 新增「人机协作原则」（Karpathy 人机分工思想）
- README.md 更新反映新文件和运维流程
- **设计理念**：在保持 YAML 符号主义架构核心优势的基础上，叠加面向人类可读性和 AI 可维护性的运维基础设施

## [2026-04-19] ingest | OFC 批量提取（~40 篇技术论文）

- 光学频率梳专题新增约 40 篇技术论文 YAML（v4.1 格式）
- 覆盖：飞秒激光器梳、微腔梳、电光梳、天文光梳、双梳光谱、中红外梳
- 关键新增节点：ent.battery_operated_microcomb_s18、ent.cep_hhg_comb_system_l22 等
- OFC 专题论文总数达到 61 篇，节点总数 ~456

## [2026-04-19] ingest | OFC 框架型综述（3 篇）

- `picque2020.yaml`：Picqué/Diddams/Vahala/Udem 2020 Science — 光频梳 20 年回顾
- `droste2016.yaml`：Droste & Newbury 2016 — Er:fiber 梳综述
- `endo2018.yaml`：Endo 2018 — 超低噪声光频梳综述

## [2026-04-18] schema | Schema v4.1

- 合并"光钟"+"微波频率标准"为"频率标准"专题
- 光学频率梳重组为应用-技术-原理三层架构
- 新增天文光梳子分支
- 新增"时频计量数学基础"跨专题模块
- 目录 `topics/optical-clocks/` 迁移为 `topics/frequency-standards/`

## [2026-04-17] restructure | 超稳激光 78 篇全量升级至 v4.1

- 所有 78 篇超稳激光论文 YAML 补充 principles/methods/metrics/relations 推理链条
- 补充 `breakthrough_paths`、`open_questions`、`contested_claims`
- 关系结构全面合规（direction 字段从 ent.* → pri.*/meth.*）

## [2026-04-16] restructure | Schema v4.0 多专题架构

- 从单专题（超稳激光）扩展为六专题体系
- 新增框架型论文处理规范（第九节）
- 首批框架文档：`fortier2026.yaml`（频率标准）、`giunta2019.yaml`（光学频率梳）、`dimarcq2024.yaml`（时间标尺）

## [2026-04-16] ingest | lee2026.yaml — 世界纪录

- 新世界纪录：mod σ_y = 2.5×10⁻¹⁷（17K Si 腔 + AlGaAs 晶体镀层）
- 确认 `pri.silicon_cte_zero_crossing_17k`（Si CTE 第二零点）
- 确认 `pri.optical_frequency_averaging`（多腔光学频率平均）

## [2026-04-10] schema | Schema v3.0 — 实例节点降级

- 4 个 FP 腔"独立方案"从 Level 1 降为 Level 2
- 取消 8 条 COMPETES-WITH 关系
- 6 个工程推理并入父原理 condition_variables
- 新增"稳频策略"分支

## [2026-04-06] ingest | 首批超稳激光论文（~15 篇核心文献）

- 建立超稳激光专题基础架构
- 核心节点：ent.fp_cavity_system、pri.brownian_thermal_noise_fdt、meth.pdh_locking
- 首批文献：Drever 1983、Young 1999、Numata 2004、Kessler 2012、Matei 2017 等

---

*本日志由 AI 自动维护。每次 Ingest/Restructure/Lint 后追加条目。*
