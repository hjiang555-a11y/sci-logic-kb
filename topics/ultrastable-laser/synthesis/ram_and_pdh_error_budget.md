# RAM 与 PDH 误差预算全景

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，需要专家补充证据细节）
> **涉及源文件**：drever1983, zhang2014_ram, tai2016, tai2017, shaddock1999 (对比), 其余 PDH 实现论文
> **关联综合页**：[stability_record_timeline.md](stability_record_timeline.md)

---

## 一、问题

PDH 锁频（`meth.pdh_locking`）是超稳激光的主流误差探测手段。当系统稳定度进入 10⁻¹⁶ 量级后，**残余幅度调制（Residual Amplitude Modulation, RAM）** 取代散粒噪声成为 PDH 路径的主要系统性限制。

核心原理：
- `pri.pdh_heterodyne_detection`（基础原理，Drever 1983）
- `pri.ram_pdh_frequency_offset`（RAM → 错锁点偏移 → 频率偏置噪声）

转换公式：
```
Δν_RAM = σ_RAM · κ / ν   （Zhang 2014）
例：κ = 28 kHz/(m/s²)、σ_RAM = 1 ppm → σ_y ≈ 1×10⁻¹⁶
```

---

## 二、RAM 的来源与三条抑制路径

| 来源 | 物理机制 | 代表节点 |
|------|---------|---------|
| EOM 本身 | 相位调制器晶体的走离/双折射/温漂 | `ent.eom` |
| 残余反射 | EOM 端面反射形成标准具 | 同上 |
| 光路对准 | 偏振失配、空间模式失配 | 工程层 |

### 路径 1 · **被动几何抑制** — Brewster 角 EOM
- 代表：Tai 2016 (`ent.brewster_eom_t16`) + 原理 `pri.brewster_angle_ram_suppression`
- 关键：让 EOM 端面工作在布儒斯特角，消除端面反射形成的 etalon
- 效果：室温下 σ_RAM 降至 ppm 量级

### 路径 2 · **主动伺服抑制** — Active RAM Servo
- 代表：Zhang 2014 (`zhang2014_ram.yaml`)
- 方法：用独立 PD 监测 RAM 幅度，反馈到 EOM 温度 / 偏压 / 压电
- 效果：演示 σ_RAM < 1 ppm 长时；可叠加于被动路径之上

### 路径 3 · **波导 EOM / 低 RAM 器件**
- 候选原理：`pri.waveguide_eom_low_ram`（SCHEMA 曾出现，待落地）
- 思路：集成光波导 EOM 消除空间模式问题，改善长期 RAM 稳定性

---

## 三、PDH 误差预算（概念分解）

| 分量 | 物理机制 | 当前典型贡献（顶级系统） | 主要对策 |
|------|---------|-------------------------|---------|
| 腔热噪声 | 布朗热噪声（FDT） | 10⁻¹⁷ 量级 | 见 [thermal_noise_landscape.md](thermal_noise_landscape.md) |
| RAM | EOM 残余幅度调制 | 10⁻¹⁶ – 10⁻¹⁷ | 本页 |
| 散粒噪声 | 光强涨落 | < 10⁻¹⁷（光功率充足时） | 提高光功率 / 精度设计 (Drever) |
| 电子学噪声 | 混频器、伺服环路 | < 10⁻¹⁷ | 低噪声混频 + 高增益伺服 |
| 振动耦合 | 腔形变 | 10⁻¹⁶（未优化）→ 10⁻¹⁷（力不敏感几何）| 见 [vibration_insensitivity_landscape.md](vibration_insensitivity_landscape.md) |

---

## 四、与替代误差探测方法的关系

| 方法 | 节点 | 相对 PDH 的优势 | 相对 PDH 的劣势 | RAM 问题 |
|------|------|-----------------|----------------|---------|
| Tilt Locking | `meth.tilt_locking` (Shaddock 1999) | 无需 RF 调制、无 RAM | 需要模式匹配、横模鉴别稳定性 | 无 RAM |
| 光纤延迟线 | `meth.fiber_delay_locking` | 无腔，支持大带宽调谐 | 热噪声、Rayleigh 背散射 | 不适用 |

RAM 是 PDH 方案的**内在**问题，不是可以通过调参消除的；进入 < 10⁻¹⁷ 区间后可能推动**非 PDH 方案**复兴，是重要开放方向。

---

## 五、开放问题

- RAM 在低温 Si 腔系统中的长期表现尚未系统研究（低温环境下 EOM 温控是否更稳？）
- 波导 EOM 是否能在同等 RAM 抑制下显著降低伺服复杂度？
- RAM 抑制技术在可搬运系统（无温控暗箱）中的极限是多少？

---

> 本综合页由 AI 基于 YAML + INDEX 草稿而成，需要专家逐条复核 RAM 数值与路径分类。
