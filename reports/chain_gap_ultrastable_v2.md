# 超稳激光专题 · 限制链缺口（Chain-Gap）· v2（阶段 B 档位感知重估）

> **生成方式**：`python scripts/lint.py --topic ultrastable-laser --json`（2026-04-21，阶段 B 完成后）
>
> **变更说明**：v1（2026-04-21）假设所有 BOUNDED-BY 关系都必须补 `breakthrough_paths`，统计出 21 条缺口。阶段 B（v4.4 档位感知）按 `meta.contribution_type` 归并：只有 **breakthrough** 档位论文的链缺口计为真实工作项（WARNING），`evidence` / `framework` 档位的链缺口降级为 `INFO`（符合 SCHEMA §9.1 — evidence 档位允许留开链）。
>
> **v2 真实缺口：7 条（WARNING）+ 14 条 INFO**（总 21 条未变，但性质重新归类）
>
> v1 报告保留于 [`chain_gap_ultrastable.md`](chain_gap_ultrastable.md) 作为历史存档，本文件为当前工作底稿。

---

## 一、真实缺口（breakthrough-tier · 7 条 WARNING）

| 文件 | contribution_type | rel_id | 受限实体 / 方法 | 原文论断摘录 | 建议动作 |
|------|-------------------|--------|---------------|-------------|---------|
| `chen2025.yaml` | breakthrough | `rel.Che02` | `ent.si_crystal_fp_cavity_sub5k_c25` | fundamentally limited by Brownian thermal noise | 🟢 已是低温 Si，补 path 1 (AlGaAs 镀层未用) · 标 path 2 status: demonstrated |
| `kedar2023.yaml` | breakthrough | `rel.Ked03` | `ent.si_crystal_fp_cavity_k12` | Brownian noise from mirror dissipation | 🟢 path 1 (AlGaAs 晶体镀层，Kedar 2023 本身演示) status: demonstrated |
| `numata2004.yaml` | breakthrough | `rel.N04` | `ent.mirror_coating` | coating contributes ~15% | 🟢 path 1 (晶体镀层直接针对镀层贡献) |
| `numata2004.yaml` | breakthrough | `rel.N05` | `ent.spacer_ule` | spacer contributes ~1% | 🟡 spacer 贡献已次要，建议 status: resolved (not active bottleneck) |
| `webster2008.yaml` | breakthrough | `rel.We08_01` | `ent.fp_cavity_system` | Brownian motion of substrate + coating | 🟢 父节点级，引用 Numata 分解作为起点 |
| `zhang2014_ram.yaml` | breakthrough | `rel.Z14_01` | `meth.pdh_locking` | RAM 诱导 PDH 频偏 | 🟢 path 1 (Tai 2016 Brewster) · path 2 (本文主动抑制) · path 3 (波导 EOM) |
| `zhang2014_ram.yaml` | breakthrough | `rel.Z14_05` | `met.ram_fractional_instability` | 同上 | 🟢 同上（指标层共享） |

**按限制原理归纳**：

| 限制原理 | 真实缺口数 | 说明 |
|---------|-----------|------|
| `pri.brownian_thermal_noise_fdt` | 5 | Numata 基础分解 + Webster 父节点 + 低温 Si 腔双例 |
| `pri.ram_pdh_frequency_offset` | 2 | zhang2014_ram 自身（方法+指标双挂） |
| **合计** | **7** | 全部集中在两条主线，可一轮 PR 批量修复 |

---

## 二、降级为 INFO 的缺口（evidence-tier · 14 条）

> 这些关系的 BOUNDED-BY 来自 `contribution_type: evidence` 的论文。按 SCHEMA §9.1，evidence 档位**允许**链缺口存在，不计入工作缺口。如有余力可在后续精修阶段处理。

| 文件 | rel_id | 说明 |
|------|--------|------|
| `argence2012.yaml` | rel.A03 | 空间级紧凑化，evidence |
| `chen2014.yaml` | rel.CHF03 | 可搬运紧凑腔，evidence |
| `chen2020.yaml` | rel.CH02 | 立方双腔，evidence |
| `didier2018.yaml` | rel.DD02 | 超紧凑金字塔腔，evidence |
| `grabielle2025.yaml` | rel.GR01 | FDL 白噪声，evidence |
| `hafner2020.yaml` | rel.HF20_03 | 可搬运 12cm 腔，evidence |
| `jiang2011.yaml` | rel.JI02 | 低热噪声腔，evidence |
| `jin2018.yaml` | rel.JN02 | ULE 30cm 腔（578 nm），evidence |
| `legero2010.yaml` | rel.Leg02 | 10cm 腔 flicker 底，evidence |
| `li2018.yaml` | rel.LI02 | ULE 30cm 腔（Sr），evidence |
| `li2019.yaml` | rel.LIG01 | 巨型 IFOG，evidence |
| `millo2009.yaml` | rel.Mil01 | 早期 FP 系统，evidence |
| `tai2017.yaml` | rel.Tai01 | FP 父节点，evidence |
| `tao2018.yaml` | rel.T05 | 紧凑长方体腔，evidence |

> lint 输出示例：`[INFO] tai2017.yaml: BOUNDED-BY relation 'rel.Tai01' lacks breakthrough_paths (tier=evidence; chain-gap allowed per §9.1)`

---

## 三、修复优先级（v2 重估）

| 级别 | 条目数 | 说明 |
|------|-------|------|
| P0（可批量补 breakthrough_paths） | 6 | 7 条 WARNING 中除 `rel.N05`（建议 resolved）外均可按三大路径模板补齐 |
| P0 特判 | 1 | `numata2004.yaml::rel.N05`：spacer 贡献 1%，标 `status: resolved` |

> **重大变化**：原 v1 报告列出的 `didier2018` / `grabielle2025` / `li2019` "专家裁决"三条因 tier=evidence 均降为 INFO，不再是阶段 B 的必修项；如确有需求可后续补，但不阻塞阶段 B 关闭。

---

## 四、执行后预期收益

- 推理链闭环率（breakthrough-only）：73.1% → 预计 ≥ 95%（剩余 7 条补齐后）
- 超稳激光 lint chain-gap WARNINGS：7 → 0–1（仅 N05 保留为 resolved 样例）
- 阶段 B 收尾条件：WARNING 清零；INFO 保留，后续按专家节奏处理

---

## 五、操作建议

1. 按 P0 补 `breakthrough_paths`，每条含 `direction` / `expected_gain` / `status` / `source.claim`
2. 每次编辑后运行：`python scripts/lint.py --topic ultrastable-laser --summary`，关注 WARNING 数
3. 全部修复完成后重建 INDEX：`python scripts/build_index.py`
4. 在 `LOG.md` 追加 `## [YYYY-MM-DD] lint | 阶段 B 后续 · breakthrough chain-gap 清零`

---

*v2 报告生成于 2026-04-21 阶段 B 完成后；lint / stats 档位感知已合入 `scripts/lint.py` 与 `scripts/stats.py`。*
