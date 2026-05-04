# B-DCS 双梳光谱 · 技术与应用时间线

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。本页不替代 YAML 节点。
>
> **最后更新**：2026-05-02 · 首建（B-2 OFC 样板区）
> **涉及源文件**：coddington2010.yaml · coddington2016.yaml · ideguchi2016.yaml · cossel2017.yaml · carlson2018.yaml · coburn2018.yaml · ycas2019.yaml · lesko2020.yaml · probster2021.yaml · han2024.yaml
> **专题架构**：[`../_meta/architecture.md`](../_meta/architecture.md) · 子域 B-DCS（双梳光谱）
> **主线指标定义**：[`../_meta/scoping_principles.md`](../_meta/scoping_principles.md) v2 · §1.2 B-DCS
> **状态**：🟢 当前（基于已摄入论文；后续摄入时刷新）

---

## 本页回答的问题

双梳光谱（Dual-Comb Spectroscopy, DCS）是光频梳的核心应用子域。利用两台互相干光频梳的微小 f_rep 差实现多外差下转换，将光学频谱映射到 RF 域，实现高分辨率、高速、无机械扫描的光谱测量。本页回答：

1. **DCS 的物理基础**：互相干 + 多外差检测如何实现光学→RF 的频率映射？
2. **相干时间 vs 光谱覆盖带宽**如何协同进步？
3. **DCS 从实验室走向野外**的关键工程节点是什么？
4. **开放路径 DCS** 的长程探测物理极限在哪里？

> 📌 **本页不讨论** 飞秒锁模技术（A1）、频率综合链路（B-FreqSyn）、中红外单独探测器（B-MIR 子域合成页独立承载）。

---

## 一、DCS 物理基础

### 1.1 核心原理链

```
pri.dual_comb_multiheterodyne_detection (domain, coddington2016)
  └── 两台 comb（f_rep1, f_rep2 = f_rep1 + Δf_rep）
      └── 多外差拍频 → 每对梳齿映射到 RF 频率
          └── RF 频谱 = 光学频谱 × (Δf_rep / f_rep) 缩放
              └── 无需机械扫描，全电子读出
```

**关键约束**：`pri.mutual_coherence_requirement` (coddington2016)
- 两台梳必须在整个采集窗口内保持互相干（mutual coherence）
- 失去互相干 ⇒ 梳齿拍频展宽 ⇒ 光谱分辨率退化
- 互相干时间直接决定**有效分辨率 × 带宽积**

### 1.2 早期奠基

| 年份 | 论文 | 贡献 |
|------|------|------|
| 2010 | `coddington2010` | **首台相干双梳光谱仪**：两台锁模 Er:fiber 梳，互相干锁定，多外差检测演示 |
| 2016 | `coddington2016` | 双梳光谱综述：建立 multiheterodyne 理论框架 + 互相干要求 + SNR 标度律 |

---

## 二、主线演进：互相干时间 × 光谱覆盖带宽

**主线指标**：互相干时间（mutual coherence time）+ 光谱覆盖带宽。详见 [`../_meta/scoping_principles.md` §1.2](../_meta/scoping_principles.md)。

### 2.1 关键台阶

| 年份 | 论文 | 系统 | 互相干时间 | 覆盖带宽/波长 | 关键创新 |
|------|------|------|-----------|-------------|---------|
| 2010 | `coddington2010` | 相干 DCS（NIST） | ~ms 级（锁定下） | NIR（~1.5 μm） | 🏆 首台相干 DCS |
| 2016 | `ideguchi2016` | KLM 单腔双向 DCS | 被动互相干（单腔共享噪声） | NIR | 单腔双向：无需主动锁定 |
| 2017 | `cossel2017` | 机载开放路径 DCS（NIST） | 飞行中保持 | NIR | 🏆 首次机载 DCS |
| 2018 | `coburn2018` | 野外部署 DCS | 连续数日野外操作 | NIR–SWIR | 🏆 首次野外连续部署 |
| 2018 | `carlson2018` | PHIRE 单梳/双梳 | 灵活切换 | NIR | 单梳 DCS 简化架构 |
| 2019 | `ycas2019` | 中红外 DCS（VOC 探测） | 公里级开放路径 | MIR（3–5 μm） | MIR 长程大气探测 |
| 2020 | `lesko2020` | 1 GHz 交钥匙 Er:fiber DCS | 高 f_rep 加速采集 | NIR（1.56 μm） | `pri.high_frep_dcs_speed_advantage` 采集速率 ↑ |
| 2021 | `probster2021` | FOKUS II 空间 DCS | 空间环境 | NIR | 🏆 空间级双梳 |
| 2024 | `han2024` | 113 km 双站双向 DCS | 长程大气 | NIR | 🏆 最长距离开放路径 DCS |

### 2.2 结构性洞察

- **单腔双向** (`ideguchi2016`) 是一次架构简化：一台激光器双向锁模产生两个互相干的脉冲序列（`pri.kerr_asymmetry_induced_frep_difference_i16`），省去主动互相干锁定。代价是 Δf_rep 调节范围受限。
- **从实验室到野外**的跃迁（Coburn 2018）标志 DCS 从"原理演示"进入"实用传感工具"阶段。
- **长程开放路径**的物理极限由 `pri.photon_starved_open_path_dcs_limit` (han2024) 定义：散粒噪声 + 大气信道损耗（湍流、衰减、退相干）共同决定 SNR 地板。

---

## 三、相干平均 SNR 标度律

`pri.dual_comb_coherent_averaging_snr_scaling` (coddington2010)：

```
SNR ∝ √(N_coherent) × (per-tooth power) / (detector noise floor)
```

- 互相干 ⇒ 干涉图相干叠加 ⇒ SNR ∝ √N（N 为相干平均次数）
- 失去互相干 ⇒ 干涉图随机相位 ⇒ 非相干平均 ⇒ SNR 不再 ∝ √N
- 因此**互相干时间是 DCS 灵敏度的第一性约束**

长程 DCS 中附加约束（`pri.coherent_averaging_background_noise_suppression`, han2024）：
- 长时相干平均可抑制散粒/探测器背景噪声
- 但大气湍流引入的相位扰动限制了有效相干积分时间
- `pri.bistatic_two_way_dcs_geometry` (han2024)：双站双向几何降低单程大气穿越的共模噪声

---

## 四、DCS 变体架构谱系

| 架构 | 论文 | 核心特征 | 适用场景 |
|------|------|---------|---------|
| 双梳主动锁定 | coddington2010 | 两台独立梳 + 互相干锁相环 | 最高 SNR，实验室 |
| 单腔双向 | ideguchi2016 | 一台激光器双向输出 | 简化架构，中 SNR |
| 单梳 DCS (PHIRE) | carlson2018 | 单梳 + 延迟扫描 | 最低复杂度 |
| 野外部署 | coburn2018 | 加固双梳 + 太阳能 | 环境监测 |
| 机载 DCS | cossel2017 | 飞行器平台 + 开放路径 | 大气遥感 |
| 空间 DCS | probster2021 | 空间级加固双梳 | 星载光谱 |
| 长程双向 DCS | han2024 | 双站望远镜 + 信标对准 | 113 km 大气 |

---

## 五、与超稳激光 / 频率标准的接口

- `CONDITIONED-BY ent.fp_cavity_system`：双梳的互相干锁定依赖窄线宽 CW 参考激光
- DCS 的绝对频率精度由梳齿锁定链向上游追溯到频率标准

---

## 六、下一步整治建议

- [ ] 高重频 DCS 的 SNR × 采集速率乘积模型（与 A1-Rep 轨道协同）
- [ ] MIR DCS 子页（当 B-MIR paper count ≥ 5 时独立）
- [ ] 本页在新 DCS 论文入库时刷新时间线

---

*首建：2026-05-02（B-2 OFC 样板区 · synthesis gap fill）*
*维护规范：新 B-DCS 论文入库时，若刷新主线纪录 → 在 §2.1 表补一行 · 更新"状态"时间戳*
