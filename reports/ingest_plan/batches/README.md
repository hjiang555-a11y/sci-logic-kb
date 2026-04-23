# 阶段 3 · 批次分配清单

**生成日期**：2026-04-23
**候选池总量**：**32 篇**（原 31 篇 + Ludlow 博士论文 1 篇）
**审批状态**：✅ 全部已批准（含 5 篇白名单 + 1 篇 PhD thesis）

> 阶段 3 遵循 TODO.md §阶段 3 的批次规则（每批 8–15 篇）。每批走**独立 PR**，按 `CONTRIBUTING.md` Step 1–10 摄入，合并前必须 `python scripts/lint.py` 0 error 通过。

---

## 批次分配总览

| 批次 | 子域 / 主题 | 篇数 | 候选 `first_author_year` | 状态 |
|------|-----------|------|------|------|
| **B1** | OFC · 早期综述与原理奠基 | 4 | `cundiff2003`, `fortier2019`, `diddams2020b`, `diddams2016` | **✅ 已完成 2026-04-23**（lint 0 error；5 条跨文件节点复用，0 重复定义） |
| **B2** | OFC · 直接光谱与频率综合 | 5 | `ye2000`, `marian2004`, `jones2005`, `adler2009`, `fortier2011` | ⏳ 待启动 |
| **B5a** | 光钟 · Sr lattice 主干（JILA 分支） | 8 | `ludlow2008`, `bloom2014`, `nicholson2015`, `ludlow2015`, `bothwell2019`, `oelker2019`, `bothwell2022`, `kim2023` | ⏳ 待启动 |
| **B5b** | 光钟 · NIST 与离子钟 · 基石综述 | 7 | `sullivan2001`, `heavner2005`, `oskay2006`, `rosenband2008`, `diddams2020`, `bacon2021`, `aeppli2022` | ⏳ 待启动 |
| **B5c** | 光钟 · Ludlow PhD thesis | 1 | `ludlow2008_thesis` ⭐ | **✅ 已完成 2026-04-23**（`meth.sr_optical_lattice_clock_stack_l08` 建立供 B5a 后续论文复用） |
| **B7** | 频率传递 | 1 | `boyd2005` | ⏳ 待启动 |
| **B8** | 时频数学基础 · 非奠基期刊 | 1 | `allan2016` | ⏳ 待启动 |
| **B9** | Allan–Howe 奠基白名单（< 1999） | 5 | `allan1966`, `allan1987`, `howe1976`, `sullivan1990`, `riley2008` | **✅ 已完成 2026-04-23**（lint 0 error，8 个权威 `meth.*` 节点入库） |
| **合计** | — | **32** | — | |

> 注：批次 B3/B4/B6 原计划的子域（微梳、超稳激光 JILA/NIST 分支、时间标尺）在本轮爬取未命中候选，留空等后续源扩充（需 `jila.colorado.edu` / `www.nist.gov` allowlist 开通后重跑阶段 1）。

---

## 批次摄入顺序建议

1. **B9**（先摄入 Allan–Howe 奠基）—— 为后续实验论文提供指标/方法节点复用基础
2. **B1**（OFC 综述 + 原理）—— 衔接现有 OFC 骨架
3. **B5c**（Ludlow PhD thesis）—— 作为 Sr lattice 专题的 framework 总纲
4. **B5a / B5b**（Sr / NIST 光钟）—— 实验突破主体
5. **B2**（OFC 直接应用）
6. **B7 / B8**（补齐时频传递 / 数学基础）

---

## 档位分布（v4.4 contribution_type）

| 档位 | 篇数 | 比例 | 代表 |
|------|------|------|------|
| `breakthrough` | 6 | 19% | `bloom2014`, `nicholson2015`, `rosenband2008`, `bothwell2022`, `fortier2011`, 另 1 保留待专家定档 |
| `framework` | 11 | 34% | 所有 review/thesis/奠基（`cundiff2003` / `ludlow2015` / `diddams2020` / `diddams2020b` / `fortier2019` / `ludlow2008_thesis` / 5 篇 B9 白名单） |
| `evidence` | 15 | 47% | 绝大多数实验改进与工程演示 |

---

## 每批 PR 约束（重申 TODO.md §阶段 3）

1. PR 描述列出 `Rejected from this batch: N 篇` —— 透明化质量过滤
2. `scripts/lint.py` 0 error
3. 跨文件节点复用率写入 PR 描述
4. B9 批次 PR 标题追加 `[foundational-whitelist]` 标签
5. B5c 批次 PR 标题追加 `[phd-thesis]` 标签

---

## PDF 可用性备忘（阶段 3 阻塞点）

- **权威 PDF 下载入口**（用户 2026-04-23 三次确认）：
  - NIST T&F：<https://tf.nist.gov/tf-cgi/showpubs.pl>
  - JILA Ye group：<https://jila.colorado.edu/yelabs/publications/scientific/year>
- **可直接做 metadata 级摄入**：`framework` 档 11 篇（综述/路线图/thesis 摘要通常可得）
- **需 PDF 全文才能摄入**：`breakthrough` + `evidence` 21 篇 —— 需上述两站（`tf.nist.gov` / `jila.colorado.edu`）或 `journals.aps.org` / `nature.com` / `science.org` / `iopscience.iop.org` allowlist，或本地 Zotero 投递
- **网络限制域**：见 `summary.md §网络访问说明`
