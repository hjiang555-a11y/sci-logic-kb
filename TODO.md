# TODO — 批量摄入计划（JILA / NIST 时频论文扩库）

> **定位**：本轮主任务是将 JILA（Jun Ye group 为主）与 NIST 时间频率部门的代表性论文系统性纳入知识库。
> **更新日期**：2026-04-23
> **当前阶段**：✅ 阶段 0（元规则与过滤器）已固化 · ⏳ 阶段 1（源爬取）待启动
>
> **维护原则**：
> - 阶段推进后更新本文件状态；完成项打勾但保留条目，直到整轮结束再归档到 LOG.md
> - 每个阶段的产物放在 `reports/ingest_plan/` 下，文件名前缀 `stageN_*`
> - 每批 PR 合并后同步勾选对应阶段 checkbox

---

## 阶段 0 · 元规则与过滤器（✅ 已固化）

> 本节一经固化即作为后续所有阶段的硬约束。任何豁免必须在 PR 描述中显式说明并链接到此节。

### 0.1 年份过滤器

| 论文出版年 | 处理规则 |
|-----------|---------|
| `year ≥ 1999` | 按常规技术/实验论文流程摄入（走 `CONTRIBUTING.md` Step 1–10） |
| `year < 1999` | **白名单制**：仅接受下列两类奠基性贡献，其他一律拒绝 |

**< 1999 白名单（两类奠基）**

- **A. Allan 方差体系**
  - Allan 1966 *Proc. IEEE* 54(2): 221 — σ_y(τ) 原始定义
  - Allan 1987 *IEEE TUFFC* 34(6): 647 — "Should the classical variance be used as a basic measure…"
  - Barnes / Allan / Sullivan 等 1990s 的派生方差（Modified / Hadamard / Total）奠基期刊/NBS Tech Note
- **B. David A. Howe 噪声测量体系**（注：用户口述"David Hown"经核实为 NIST 频率稳定性分析奠基人 **David A. Howe**）
  - Howe 1981 NBS Tech Note 669 — 频率稳定性测量方法
  - Howe 1995 / 1999 — TheoH / Theo1 方差
  - Howe 在 1990s 末的频率稳定性测量综述（*Metrologia* / *IEEE TUFFC* 期刊版本优先）

白名单外的 < 1999 年论文**一律进入 `rejected.csv`**，`reason_code = pre_1999_out_of_whitelist`。

> PDH（Drever 1983）等已在库的 < 1999 奠基原理节点无需重复摄入。若本轮发现 Pound 1946 等与 PDH 推导直接相关的论文确有新增必要，单独走白名单例外审批。

### 0.2 质量过滤门

| 论文类型 | 判定 | 备注 |
|---------|------|------|
| **Peer-reviewed 期刊** | ✅ 接受 | Nature / Science / PRL / PRA / PRX / PR Applied / Metrologia / *IEEE TUFFC* (Regular Paper) / *IEEE JQE* / APL / OL / Opt. Express / Optica / Nat. Photon. / Nat. Commun. / Rev. Sci. Instrum. / JOSA B 等 |
| **NIST 会议论文** | ❌ **一律拒绝** | CPEM / IFCS (Int. Frequency Control Symposium) / EFTF / PTTI / FCS 等 proceedings 一律拒。用户明确指示 |
| **其他会议论文** | ❌ 默认拒 | 同上 |
| **NBS / NIST Tech Note / Technical Monograph** | ⚠️ 白名单制 | 仅 0.1 §B 的 Allan / Howe 奠基技术报告接受；其他拒绝 |
| **PhD thesis** | ✅ 接受 | 仅 Ye group / 其他一线组的代表性学位论文，定位为 `framework` 档 |
| **arXiv preprint 无期刊版本** | ❌ 拒绝 | 若同文后续发表期刊版本，以期刊版本为准；记录 preprint DOI 备查 |
| **Review / Roadmap** | ✅ 接受 | 定位为 `framework` 档 |

**例外通道**：若某"IFCS proceedings"论文是 Allan/Howe 奠基算法定义的**唯一来源**，走 0.1 §B 白名单单独审批，PR 标题注明 `[whitelist-exception]`。

### 0.3 拒绝记录规范

所有被过滤掉的候选论文必须记入 `reports/ingest_plan/rejected.csv`，字段：

| 列 | 说明 |
|----|------|
| `doi` | 论文 DOI（无 DOI 时填 URL 或 ISBN） |
| `title` | 论文标题 |
| `first_author_year` | 作者年份（如 `allan1966`） |
| `venue` | 期刊 / 会议 / 报告编号原文 |
| `venue_type` | `journal` / `conference` / `tech_note` / `thesis` / `preprint` |
| `year` | 出版年 |
| `reason_code` | `nist_conference` / `other_conference` / `pre_1999_out_of_whitelist` / `preprint_only` / `duplicate_of_existing` / `out_of_scope_topic` |
| `source_url` | 原始候选来源（JILA 列表页 / NIST 列表页 / 引文） |

### 0.4 候选清单新增字段

`reports/ingest_plan/candidates_final.csv` 必含下列列（在常规书目字段之外）：

- `venue_type`：`journal` / `conference` / `tech_note` / `thesis` / `preprint`
- `quality_pass`：`yes` / `no` / `whitelist`
- `whitelist_reason`：`allan_variance` / `howe_noise` / `foundational_other` / `null`
- `proposed_topic`：预判归属的 `topics/<topic>/`
- `proposed_tier`：`breakthrough` / `evidence` / `framework`（默认 `evidence`）

### 0.5 阶段产物目录约定

```
reports/ingest_plan/
  stage1_raw_candidates_jila.csv       # 阶段 1 · JILA 原始抓取
  stage1_raw_candidates_nist.csv       # 阶段 1 · NIST 原始抓取
  stage2_candidates_final.csv          # 阶段 2 · 经 0.1/0.2 过滤后的最终候选池
  rejected.csv                         # 全阶段共享的拒绝清单
  summary.md                           # 阶段 2 人读摘要（含拒绝统计 + 白名单候选逐条列出）
  batches/                             # 阶段 3 起每批的摄入清单
    B1_*.md
    ...
```

---

## 阶段 1 · 源爬取（✅ 完成，2026-04-23）

> ⚠️ 沙箱 DNS 屏蔽：`colorado.edu` / `nist.gov` 均 DNS REFUSED，已通过 web_search 代理检索代替直接爬取。
> 若需完整列表（预计 300–500 篇），需专家将这两个域名加入 Copilot allowlist 后重跑。

- [x] 抓取 JILA Jun Ye group 论文（web_search 代理），落盘 `stage1_raw_candidates_jila.csv`（20 条）
- [x] 抓取 NIST Time & Frequency Division 论文（web_search 代理），落盘 `stage1_raw_candidates_nist.csv`（20 条）
- [x] 导出 `nist_techreports_howe_allan.csv`（9 条 Allan / Howe 相关技术报告）供白名单核验
- [x] 沙箱被阻断域名已记录：`jila.colorado.edu`、`www.nist.gov`、`tf.nist.gov`（见 `summary.md §网络访问说明`）

---

## 阶段 2 · 过滤与人读摘要（✅ 完成，2026-04-23）

> 38 篇去重 → 31 接受 / 7 拒绝；白名单候选 5 篇待专家勾选；详见 [`reports/ingest_plan/summary.md`](reports/ingest_plan/summary.md)

- [x] 应用 0.1 年份过滤器 + 0.2 质量过滤门，生成 `stage2_candidates_final.csv`（31 篇）
- [x] 所有被拒候选写入 `rejected.csv`（7 篇：2 重复 / 3 超出主题 / 2 NIST 会议）
- [x] 生成 `summary.md`（候选总数 / 分桶 / 白名单逐条列出）
- [ ] **专家勾选白名单 5 篇**（`allan1966` / `allan1987` / `howe1976` / `sullivan1990` / `riley2008`）——见 `summary.md §白名单候选`
- [ ] **专家审批最终候选池**（31 篇）→ 批准后触发阶段 3

---

## 阶段 3 · 分批摄入（⏳ 待启动，阶段 2 通过后触发）

批次编号规则：`B1` ~ `B9`，每批目标 8–15 篇，按子域聚类：

| 批次 | 子域 | 目标篇数 | 说明 |
|------|------|---------|------|
| B1 | OFC · 自参考与频率综合 | 8–12 | 衔接现有 OFC 骨架 |
| B2 | OFC · 双梳光谱 | 8–12 | |
| B3 | OFC · 微梳平台 | 8–12 | |
| B4 | 超稳激光 · JILA/NIST 分支补全 | 6–10 | 合并到已有 78 篇 |
| B5 | 光钟 · Sr / Yb / Al⁺ / Hg | 10–15 | 激活 `topics/frequency-standards/` |
| B6 | 时间标尺 · UTC/TAI · Kalman 合成 | 6–10 | 激活 `topics/timescales/` |
| B7 | 时频传递 · 光纤相干 / TWSTFT / GNSS | 8–12 | 激活 `topics/frequency-transfer/` |
| B8 | 时频计量数学基础 · 非奠基期刊论文 | 4–8 | 归属 `topics/shared/metrics/` 待阶段 2 定 |
| **B9** | **Allan–Howe 奠基白名单** | **3–5** | **< 1999 白名单专用批次；PR 标题注明 `[foundational-whitelist]`** |

**每批 PR 必做事项**：
- PR 描述中列出 `Rejected from this batch: N 篇会议 / M 篇 preprint`，透明化质量过滤动作
- 按 `CONTRIBUTING.md` Step 1–10 逐篇摄入
- 运行 `python scripts/lint.py` 必须 0 error 通过
- 同批 YAML 文件内的跨文件节点复用率在 PR 描述中汇报

---

## 阶段 4 · 索引与统计刷新（每批合并后）

- [ ] 运行 `python scripts/build_index.py` 刷新 `INDEX.md` / `INDEX_metrics.md` / `INDEX_principles.md` / `docs/CURRENT_NODES_REFERENCE.md`
- [ ] 运行 `python scripts/stats.py` 记录增量指标（库存 / chain-closure / reuse / σ_y linkage）
- [ ] `LOG.md` 追加 `ingest` 条目

---

## 阶段 5 · Synthesis 页面启动（阶段 3 完成 ≥ 2 批后）

- [ ] OFC 首批 synthesis 最小集（4 页）：频率综合 / 双梳光谱 / 微梳平台 / 光谱应用
- [ ] 频率标准 / 时间标尺激活后，各起 1 个骨架 synthesis 页
- [ ] 更新 freshness 报表

---

## 阶段 6 · 专家验收与归档

- [ ] 全阶段合并后生成 `reports/ingest_plan/final_report.md`
- [ ] 本 TODO 归档到 `LOG.md`，TODO.md 退回到维护性清单

---

## 硬约束速查（开发者请勿跳过）

1. **NIST 会议论文 = 零摄入**（0.2 质量过滤门，用户明确指示）
2. **< 1999 论文除 Allan / Howe 白名单外 = 零摄入**（0.1 年份过滤器）
3. **拒绝必留痕**：全部进 `rejected.csv`，可追溯
4. **默认档位 `evidence`**：不确定时归 evidence，等专家升档
5. **不手工修改自动生成的 INDEX / CURRENT_NODES_REFERENCE**
