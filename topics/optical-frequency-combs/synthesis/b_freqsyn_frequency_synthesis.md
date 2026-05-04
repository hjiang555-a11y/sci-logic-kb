# B-FreqSyn 频率综合与微波链路 · 技术时间线

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。本页不替代 YAML 节点。
>
> **最后更新**：2026-05-02 · 首建（B-2 OFC 样板区）
> **涉及源文件**：lecoq2010.yaml · fortier2011.yaml · quinlan2011.yaml · fortier2012.yaml · hati2013.yaml · portuondo-campa2015.yaml · giunta2019.yaml · giunta2020.yaml · kalubovilage2022.yaml · leopardi2017.yaml
> **专题架构**：[`../_meta/architecture.md`](../_meta/architecture.md) · 子域 B-FreqSyn（频率综合 / 计量链路）
> **主线指标定义**：[`../_meta/scoping_principles.md`](../_meta/scoping_principles.md) v2 · §1.2 B-FreqSyn
> **状态**：🟢 当前（基于已摄入论文；后续摄入时刷新）

---

## 本页回答的问题

光频梳的核心计量功能是将超稳光学参考的精度**相干传递**至微波域或其他光学频段。本页回答：

1. **光频除法（OFD）** 如何将光学稳定度以 N² 相位噪声降低因子转移至微波？
2. **微波相位噪声与 σ_y 转移残差**如何从 10⁻¹⁵ 级演进至 10⁻¹⁸ 级？
3. **混合振荡器**如何用互补噪声特性突破 OFD 散粒噪声底？
4. **宽带光学频率综合**如何实现跨频段 10⁻²⁰ 量级频率比值测量？

> 📌 **本页不讨论** 飞秒锁模技术（A1）、超稳激光腔噪声（USL topic）、DCS 多外差架构（B-DCS 合成页）。

---

## 一、OFD 物理基础

### 1.1 核心原理链

```
pri.optical_frequency_division_microwave (domain, giunta2019)
  └── 飞秒梳锁定至超稳光学参考（ν_opt ~ 282–500 THz）
      └── 光电探测 f_rep 谐波 → 提取微波信号（~10 GHz）
          └── 相位噪声功率降低 N² = (ν_opt / f_mw)² ≈ 2.5×10⁹
              └── 光学 Q ~ 10¹¹ 的稳定度"转写"至微波域
```

**关键约束**：`pri.ofd_optical_stability_transfer` (fortier2011)
- 光频处相位噪声 S_φ(opt) 以 1/N² 因子降低至微波域 S_φ(mw)
- 最终微波相位噪声由光学参考和光电探测散粒噪声共同决定
- 散粒噪声底 ∝ 1/(P_avg × f_rep²)，是 OFD 高偏移频率的基本限制

### 1.2 信号链

```
超稳 FP 腔 → CW 参考激光 → 飞秒梳 f-2f 自参考锁定
  → f_rep 谐波光电探测 → 微波输出（~10 GHz）
  → 双梳比对 / 混合振荡器规训 → 独立噪声表征
```

---

## 二、主线演进：σ_y 转移残差 × 微波相位噪声

**主线指标**：光-微波 σ_y 转移残差（τ = 1 s）+ 10 GHz 绝对相位噪声 @ 1 Hz offset。详见 [`../_meta/scoping_principles.md` §1.2](../_meta/scoping_principles.md)。

### 2.1 关键台阶

| 年份 | 论文 | 系统 | σ_y(1 s) 残差 | 10 GHz PN @ 1 Hz | 关键创新 |
|------|------|------|-------------|-----------------|---------|
| 2010 | `lecoq2010` | Er:fiber OFD（LNE-SYRTE） | ~1.6×10⁻¹⁶ | −111 dBc/Hz | 双梳比对法表征残余噪声 |
| 2011 | `fortier2011` | Ti:sapphire OFD（NIST） | ≤8×10⁻¹⁶ | −104 dBc/Hz | 🏆 首次光分频微波 < 10⁻¹⁵；760 as 时序抖动 |
| 2011 | `quinlan2011` | Er:fiber OFD 200 MHz（NIST） | — | ≤−100 dBc/Hz | 高 f_rep 降散粒噪声底：−145 dBc/Hz |
| 2012 | `fortier2012` | 混合光子-微波振荡器（NIST） | — | — | 🏆 OFD + SLCO 噪声互补：420 as 时序抖动 |
| 2013 | `hati2013` | OFD 光子微波源（NIST） | — | SOTA（见 paper） | 绝对时序抖动测量方法 |
| 2015 | `portuondo-campa2015` | DPSSL + PM 交织器 | — | −100 dBc/Hz @ 1 Hz | 紧凑 DPSSL 9.6 GHz 生成 |
| 2017 | `leopardi2017` | Er:fiber 梳合成（NIST） | ~3×10⁻¹⁸ | — | 🏆 梳合成稳定度进入 10⁻¹⁸ |
| 2019 | `giunta2019` | 光子微波合成（NPL） | ~6.5×10⁻¹⁸ | −171 dBc/Hz | 🏆 最低微波相噪记录 |
| 2020 | `giunta2020` | 宽带光学频率合成（NPL） | ≤2×10⁻¹⁹ (35 h) | — | 🏆 宽带合成准确度 10⁻²⁰ 量级 |
| 2022 | `kalubovilage2022` | 自由运行单片梳微波 | — | <−180 dBc/Hz @ 1 MHz | 单片集成路径 |

### 2.2 结构性洞察

- **OFD 范式确立** (fortier2011)：光频分法产生的微波，1 s 不稳定度首次低于 10⁻¹⁵，且无需深冷。这证明光学 Q 因子（~10¹¹）是微波振荡器噪声突破的关键杠杆。
- **Er:fiber 路线** (quinlan2011) 证明光纤梳可达到与 Ti:sapphire 相当的 OFD 性能，为便携化铺路。关键瓶颈是散粒噪声底由 f_rep² 和探测功率共同决定。
- **混合振荡器** (fortier2012) 是一次架构精妙化：OFD 提供接近载波低噪声（来自光学腔），SLCO 提供远端低热噪声底（~−190 dBc/Hz），二者互补实现全谱最优——420 as 单台时序抖动。
- **10⁻¹⁸ 时代** (leopardi2017 → giunta2019 → giunta2020)：光纤梳合成稳定度进入 10⁻¹⁸ 级，宽带合成准确度达 10⁻²⁰ 量级（5.4×10⁻²¹ 单次测量）。

---

## 三、限制链概览

### 3.1 散粒噪声底限制

`pri.high_rep_rate_ofd_low_shot_noise` (quinlan2011)：

```
散粒噪声相噪底 ∝ 1 / (I_avg × f_rep²)
→ 高 f_rep 降低散粒噪声（200 → 1000 MHz 改善 ~14 dB）
→ 高探测功率（mUTC 光电探测器 >100 mW 线性）进一步压低
```

### 3.2 微波参考相噪天花板

`pri.microwave_reference_noise_limit` (diddams2000) / `pri.microwave_reference_transfer_to_optical_comb` (rao2019)：

```
微波参考 → f_rep/f_ceo 锁定 → 梳齿相噪
→ 参考源相噪直接转写至光域
→ 破解路径：超稳激光作主参考（替代微波参考），梳只做光-光/光-微波齿轮
```

### 3.3 光学参考腔热噪声终极限制

OFD 的微波输出最终受限于锁定所用超稳光学腔的热噪声底（~10⁻¹⁶ 量级）。突破路径指向：
- 低温单晶硅腔（→ USL topic）
- 多腔平均或光学钟直接参考

---

## 四、架构谱系

| 架构 | 论文 | 核心特征 | 适用场景 |
|------|------|---------|---------|
| Ti:sapphire OFD | fortier2011 | 1 GHz f_rep，最高性能，−157 dBc/Hz 散粒噪声底 | 国家计量院基准 |
| Er:fiber OFD | quinlan2011, lecoq2010 | 200 MHz f_rep，−145 dBc/Hz 散粒噪声底，1550 nm 兼容 | 可搬运 / 光纤网络 |
| 混合 OFD + SLCO | fortier2012 | 噪声互补，420 as 时序抖动 | 需要全谱最优噪声 |
| DPSSL + 交织器 | portuondo-campa2015 | 紧凑固体激光 + PM 交织 | 紧凑化微波源 |
| 宽带合成器 | giunta2020 | 多分支梳 + 色散外差检测，10⁻²⁰ 准确度 | 光钟比对 / 频率比值测量 |
| 自由运行单片 | kalubovilage2022 | 无锁定链，< −180 dBc/Hz 远端本底 | 单片集成微波源 |

---

## 五、与频率标准 / 超稳激光的接口

- `CONDITIONED-BY ent.fp_cavity_system`：OFD 的绝对性能由上游超稳光学参考（腔热噪声底 ~10⁻¹⁶）设定天花板
- `ENABLES optical clock comparison`：梳作为"光-微波齿轮箱"（`pri.optical_microwave_coherent_gearbox`），使光学钟比值测量成为可能
- 双向接口：梳既从光学参考获取稳定度，又以 OFD 输出回馈微波域标准

---

## 六、下一步整治建议

- [ ] 光-光频率比值的转移残差独立追踪（与 USL topic 的接口量化）
- [ ] 片上集成 OFD（Spencer 2018 等）的 Phase II 更新
- [ ] 新 FreqSyn 论文入库时刷新时间线

---

*首建：2026-05-02（B-2 OFC 样板区 · synthesis gap fill）*
*维护规范：新 B-FreqSyn 论文入库时，若刷新主线纪录 → 在 §2.1 表补一行 · 更新"状态"时间戳*
