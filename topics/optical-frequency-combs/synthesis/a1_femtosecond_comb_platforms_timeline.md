# A1 飞秒锁模光频梳技术平台 · 时间线

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。本页不替代 YAML 节点。
>
> **最后更新**：2026-04-24 · 首建（TODO.md P1-4）
> **涉及源文件**：bartels2009.yaml · meyer2013.yaml · wang2014.yaml · zhang2015.yaml · kuse2015.yaml · kuse2016.yaml · li2017b.yaml · ma2018.yaml · cai2020.yaml · washburn2004.yaml · newbury2005.yaml
> **专题架构**：[`../_meta/architecture.md`](../_meta/architecture.md) · 子域 A1（飞秒锁模激光器光频梳）
> **主线指标定义**：[`../_meta/scoping_principles.md`](../_meta/scoping_principles.md) v2 · §1.2 子域主线指标
> **状态**：🟢 当前（基于 Round 1 Batch 1 的 10 篇代表论文；后续摄入时刷新）

---

## 本页回答的问题

光频梳专题是 **multi-track** 结构（光频梳不同于超稳激光，不存在单一主线指标）。本页聚焦 **A1 飞秒锁模光频梳** 子域，沿三条独立子主线（A1-Rep / A1-Noise / A1-Robust）回答：

1. **A1-Rep**：基频 f_rep 从 MHz 提升到 10 GHz，关键瓶颈分别是什么？
2. **A1-Noise**：f_CEO 积分相噪从 ~rad 量级降到亚 rad 的路径上，哪些结构性创新起决定作用？
3. **A1-Robust**：从桌面原型走向全保偏 / 紧凑 / 工程化形态，哪些实现选择代表了关键进步？

> 📌 **本页不讨论** DKS 微腔梳（A2）、天文梳（A3）、双梳光谱（B-DCS）、频率综合链路（B-FreqSyn）等其他子域。各自的 synthesis 由独立页面承载。

---

## 一、A1-Rep 主线：基频 f_rep 的进步

**主线指标**：基频 f_rep（非谐波放大，基频直接锁定）+ 自参考可行性。详见 [`../_meta/scoping_principles.md` §1.2](../_meta/scoping_principles.md)。

### 1.1 时间线

| 年份 | 论文 | 平台 | f_rep（基频） | 自参考 | 位于主线位置 |
|------|------|------|-------------|--------|------------|
| 2009 | `bartels2009` | Ti:sapphire（KLM） | **10 GHz** | ✅ 首次基频 10 GHz + f-2f | 🏆 基频最高 |
| 2013 | `meyer2013` | Er:fiber | ~250 MHz（含 rep-rate 调谐） | ✅ | 代表宽调谐策略 |
| 2014 | `wang2014` | Yb:fiber（振荡器直出） | **500 MHz** | ✅（无放大直接 f-2f） | Yb 平台首次 >500 MHz 直接自参考 |
| 2018 | `ma2018` | Yb:fiber | **750 MHz** | ✅ | Yb 平台基频高端 |

### 1.2 核心物理约束

`pri.high_frep_bandwidth_power_tradeoff`（定义于 `bartels2009`）：
```
E_pulse = P_avg / f_rep
```
f_rep ↑ ⇒ 单脉冲能量 ↓ ⇒ 超连续阈值 `E_pulse ≥ E_th` 越来越难满足。10 GHz 是 Ti:sapph 平台目前达到自参考的最高基频，高于此基频则单齿功率或泵浦功率要求成为主要瓶颈。

### 1.3 下一步瓶颈（向 >10 GHz 基频推进）

- 泵浦耦合进紧腔的效率（腔长 ~1.5 cm 量级）
- 单齿功率 vs. HNLF 展宽阈值的协同优化
- 向 30–50 GHz 迈进需要光纤平台的 harmonic mode-locking 或微腔混合架构（归属 A2）

---

## 二、A1-Noise 主线：f_CEO 相噪 / 积分时延抖动

**主线指标**：f_CEO 积分相位噪声（rad，需标注积分区间）或等效积分时延抖动（as）。

### 2.1 关键台阶

| 年份 | 论文 | 结构 | f_CEO 积分相噪（或 timing jitter） | 关键创新 |
|------|------|------|----------------------------------|---------|
| 2015 | `kuse2015` | 全 PM Er:fiber（NALM 前身） | 铺垫 NALM 方向 | 全 PM 平台基础工作 |
| 2016 | `kuse2016` | 全 PM Er:fiber + **NALM** | **<40 as** 积分时延抖动 🏆（打破 NPR 路径限制） | NALM 替代 NPR |
| 2017 | `li2017b` | 全 PM Yb:fiber + NALM | **首次** Yb + PM + NALM f_CEO 自参考 | Yb 平台复制 NALM 优势 |
| 2018 | `ma2018` | Yb:fiber 750 MHz | **<1 rad** f_CEO 相噪 + in-loop σ_y ~10⁻¹⁸ | 高 f_rep 下的紧锁 |

### 2.2 结构性洞察

- **NPR（非线性偏振旋转）→ NALM（非线性放大环镜）** 的范式转换是本主线的决定性跃迁：PM 兼容 + 环境鲁棒 + 更低时延抖动同时获得。`meth.nalm_locking` 类节点从 `kuse2016` 起成为 A1-Noise 主线的核心方法。
- **高 f_rep + 低相噪** 是冲突的目标（单齿能量 ↓ 导致 f-2f SNR ↓）；`ma2018` 首次同时满足两条主线达到 `breakthrough` 档。

---

## 三、A1-Robust 主线：工程化 / 全保偏 / 紧凑化

**主线指标**：连续稳定时长 + SWaP（足迹 / 功耗）+ 单驱动器锁定带宽。

### 3.1 代表演进

| 年份 | 论文 | 结构 | 工程化突破 |
|------|------|------|-----------|
| 2015 | `zhang2015` | Er:fiber 腔内 EOM | 腔内 EOM 替代外部执行器，锁定带宽 ↑ |
| 2016 | `kuse2016` | 全 PM Er:fiber + NALM | 全保偏光路 = 工厂化可制造 |
| 2017 | `li2017b` | 全 PM Yb:fiber + NALM | Yb 平台全保偏首次落地 |
| 2020 | `cai2020` | 全 PM Er:fiber，**单光纤机械执行器** | 单驱动器紧凑工程化样机 · H-maser 1 s Allan 330 μHz |

### 3.2 结构性洞察

- 工程化主线的关键词是**单**：单驱动器、单光纤、单腔——降低自由度 = 降低装配复杂度 + 提高长时稳定性。
- `cai2020` 的 330 μHz @ 1 s Allan 不是打破记录（不是 `breakthrough`），但在工程紧凑化维度上刷新了"可搬运 comb + 高稳定"的同时存在性，档位 `evidence`。

---

## 四、早期基础：超连续与 f-2f 基础建立

早期基础论文定义了所有后续 A1 主线的起点：

| 年份 | 论文 | 贡献 |
|------|------|------|
| 2004 | `washburn2004` | Er:fiber + HNLF 超连续展宽获得倍频程谱 → Er 平台 f-2f 可行性奠基 |
| 2005 | `newbury2005` | 超连续相干性理论与实验表征 → 奠定相干展宽可用区间 |

---

## 五、三条主线的同时刷新矩阵

| 论文 | A1-Rep | A1-Noise | A1-Robust | 整体档位 |
|------|--------|----------|-----------|----------|
| bartels2009 | 🏆 | — | — | breakthrough |
| wang2014 | ✅ | — | — | evidence |
| kuse2016 | — | 🏆 | ✅ | breakthrough |
| li2017b | — | ✅ | 🏆 (Yb PM NALM 首次) | breakthrough |
| ma2018 | ✅ | 🏆 | — | breakthrough |
| cai2020 | — | — | ✅ | evidence |

> 🏆 = 刷新该主线纪录；✅ = 显著进步但未破纪录。
> 若一篇论文只在某一条主线 ✅ 而无 🏆，按 `evidence` 档；任一主线 🏆 即可升 `breakthrough`（详见 `scoping_principles.md` §1.3）。

---

## 六、与超稳激光 / 频率标准专题的接口

A1 子域作为**技术源头**，向上下游接口：

- **CONDITIONED-BY** `ent.fp_cavity_system`（超稳激光）：f_rep 紧锁要求窄线宽 CW 参考
- **向下游提供**：
  - → B-FreqSyn 子域：光-微波分频基础（见 bartels2009 / 后续 fortier2011 等）
  - → 频率标准专题：时钟齿分频到 RF 的载体

---

## 七、下一步整治建议

- [ ] 首个微腔梳（A2）synthesis 页：泵浦-梳光转换效率 + 相噪 @ offset + 集成 SWaP
- [ ] 频率综合链路（B-FreqSyn）σ_y 传递残差 synthesis 页（10⁻¹⁸/3× 纪录线）
- [ ] 天文梳（A3）和双梳光谱（B-DCS）待论文数 ≥ 5 时再独立建页
- [ ] 本页随新 Batch 的 A1 论文入库时刷新"时间线"节

---

*首建：2026-04-24（TODO.md P1-4 · 解决 1/6 topics synthesis coverage 缺口）*
*维护规范：新 A1 论文入库时，若刷新任一子主线纪录 → 在本页对应表补一行 · 更新"状态"时间戳*
