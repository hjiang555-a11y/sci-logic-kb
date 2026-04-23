# 阶段 1–2 摄入候选摘要

**生成日期**：2026-04-23  
**数据来源**：web_search 途径（`colorado.edu` / `nist.gov` 直接 DNS 被沙箱屏蔽，所有候选通过 web_search 代理检索）  
**过滤规则**：依照 `TODO.md` §0.1（年份过滤器）+ §0.2（质量过滤门）

---

## 数量摘要

| 类别 | 数量 |
|------|------|
| 阶段 1 原始候选（含跨列表重复） | 40 条 |
| 去重后唯一候选 | 38 篇 |
| **通过过滤 → stage2 候选池** | **31 篇** |
| 拒绝 | **7 篇** |
| **专家新增追加（PhD thesis）** | **1 篇**（`ludlow2008_thesis`） |
| **阶段 2 最终批准总量** | **32 篇** |

### 拒绝原因分布

| reason_code | 篇数 | 说明 |
|-------------|------|------|
| `duplicate_of_existing` | 2 | 已在库（`diddams2000`、`diddams2010`） |
| `out_of_scope_topic` | 3 | 非时频计量主题（超冷分子 `carr2009`、`wu2021`；C₆₀ `segura2023`） |
| `nist_conference` | 2 | NIST 会议论文（§0.2 规定零摄入）：`howe1981`（Freq. Control Symp.）、`howe2003`（IFCS） |

> 注：`howe1981`（"Properties of Signal Sources and Measurement Methods", 35th Freq. Control Symp.）虽为 Howe 著作，但本文件为会议 Proceedings，不是 TODO.md §0.1 §B 白名单明确列出的 NBS Tech Note 669（另一独立文件）。如需摄入，需专家走白名单例外审批（PR 标题注明 `[whitelist-exception]`）。

---

## 通过候选按专题分桶

| proposed_topic | 篇数 | 说明 |
|----------------|------|------|
| `frequency-standards` | 16 | Sr / Yb / Al⁺ / Hg⁺ 光钟；Cs fountain；NIST-F1 |
| `optical-frequency-combs` | 8 | Ye group OFC；远程传递；梳综述 |
| `shared/metrics` | 6 | Allan / Howe 方差体系（其中 5 篇为白名单） |
| `frequency-transfer` | 1 | 光纤频率传递（Boyd 2005） |

---

## 白名单候选（共 5 篇，需专家逐条勾选）

> 以下论文触发 §0.1 年份过滤器或 §0.2 Tech Note 过滤门，但在 TODO.md 白名单范围内，摄入须专家确认。

| # | first_author_year | year | whitelist_reason | venue | title |
|---|-------------------|------|-----------------|-------|-------|
| 1 | `allan1966` | 1966 | allan_variance | Proceedings of the IEEE | Statistics of Atomic Frequency Standards |
| 2 | `allan1987` | 1987 | allan_variance | IEEE Trans. on Instrumentation and Measurement | Should the classical variance be used as a basic measure in standards metrology? |
| 3 | `howe1976` | 1976 | howe_noise | NBS Technical Note 679 | Frequency Domain Stability Measurements: A Tutorial Introduction |
| 4 | `sullivan1990` | 1990 | howe_noise | NIST Technical Note 1337 | Characterization of Clocks and Oscillators（Howe 联合作者） |
| 5 | `riley2008` | 2008 | howe_noise | NIST Special Publication 1065 | Handbook of Frequency Stability Analysis（Riley & Howe 联合作者） |

**专家勾选说明**：
- [  ] `allan1966` — 接受摄入到 `B9` 批次
- [  ] `allan1987` — 接受摄入到 `B9` 批次
- [  ] `howe1976` — 接受摄入到 `B9` 批次（注：白名单 §B 提到的是 TN-669，本文为 TN-679，请专家确认是否同一文件或另行寻找 TN-669）
- [  ] `sullivan1990` — 接受摄入到 `B9` 批次（NIST TN 1337 是 Howe/Allan 联合编著的权威合集）
- [  ] `riley2008` — 接受摄入到 `B9` 批次（NIST SP-1065 是 Howe 联合编著的频率稳定性分析手册）

---

## 网络访问说明

以下域名在本沙箱中 DNS 被拒绝，**需要 allowlist 审批才能直接抓取完整论文列表**：

| 被阻断域名 | 说明 |
|-----------|------|
| `tf.nist.gov` | **NIST T&F 官方 PDF 下载入口** <https://tf.nist.gov/tf-cgi/showpubs.pl>（本轮 B2/B5b/B7/B8 主要 PDF 源） |
| `jila.colorado.edu` | **JILA Ye group 官方 PDF 下载入口** <https://jila.colorado.edu/yelabs/publications/scientific/year>（本轮 B2/B5a 主要 PDF 源） |
| `ye.jila.colorado.edu` | Ye group 副域名 |
| `www.nist.gov` | NIST 主站（T&F Division 论文全列表） |

> 📌 上述两个 PDF 下载入口由用户在 2026-04-23 明确指定为 B2–B8 批次的权威来源（第三次确认），已同步固化到 `TODO.md §阶段 1`。

**当前 stage1 原始候选为 web_search 代理检索结果（约 40 条），覆盖率有限。**  
若需完整爬取（预计 300–500 篇）：
1. 专家在 Copilot 设置中将以上域名加入 allowlist
2. 重跑阶段 1，覆盖 `stage1_raw_candidates_jila.csv` / `stage1_raw_candidates_nist.csv`
3. 重新执行阶段 2 过滤，更新本文件

---

## 建议下一步

1. **专家勾选白名单候选**（上表 5 篇）
2. **申请域名 allowlist**（若需完整论文列表）；或接受当前 31 篇范围，直接启动阶段 3
3. 阶段 3 建议优先顺序：
   - **B5**（`frequency-standards`，16 篇，最大批）可先分成 B5a（光钟里程碑：`bloom2014`/`nicholson2015`/`rosenband2008`/`bothwell2022`）+ B5b（综述/基础：`ludlow2015`/`diddams2020`/`sullivan2001`）
   - **B1**（OFC，8 篇）衔接现有 OFC 骨架（补 `ye2000`/`jones2005`/`adler2009`/`fortier2011`/`fortier2019`）
   - **B9**（白名单 5 篇）视专家确认结果后启动
