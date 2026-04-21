# 光纤稳频分支全景

> **综合页面（synthesis）**：跨论文综合视图，YAML 是 source of truth。
>
> **最后更新**：2026-04-21 · 🟡 初稿（draft，需要专家补充证据细节）
> **涉及源文件**：jiang2010, kefelian2009, dong2015, li2019, michaudbelleau2021, michaudbelleau2022, belardi2015, ding2025, huang2023, huangjc2019, huangjc2019b, shi2021, shi2022, gao2025, grabielle2025, jeon2025, zuba2023
> **关联综合页**：[stability_record_timeline.md](stability_record_timeline.md)

---

## 一、问题定位

**光纤干涉仪**（`ent.fiber_interferometer`，Level 1）是与 FP 腔（`ent.fp_cavity_system`）并列的**非谐振**频率参考方案，核心差异：

| 维度 | FP 腔 | 光纤延迟线 |
|------|-------|-----------|
| 工作原理 | 谐振峰锁定 | 延迟相位比较（非谐振） |
| 调谐自由度 | 有限（PZT 拉伸） | 大范围 AOM / 光路温度 |
| 主要限制 | 布朗热噪声（镜镀层） | 光纤热相噪声 + Rayleigh 背散射 |
| 体积 | 10–68 cm 腔体 + 真空 | 盘绕光纤盘 |
| 技术成熟度 | 高（1983 起） | 中（2009 Kefelian 起） |

`COMPETES-WITH` 关系在两类 Level 1 节点之间已显式成立。

---

## 二、限制原理家族

| 限制 | 节点 | 主导体制 | 代表论文 |
|------|------|---------|---------|
| 光纤热相噪声（Wanser 模型） | `pri.fiber_thermal_noise_wanser` | 光纤折射率温度涨落驱动 | Dong 2015, Jeon 2025 |
| Rayleigh 背散射 | `pri.rayleigh_backscattering_noise` | 分布式瑞利散射→干涉斑纹 | Jiang 2010, Michaud-Belleau 2021 |
| 空心光纤低热噪声 | `pri.hollow_core_fiber_thermal_noise` | 反谐振/空芯导光降低模场-玻璃重叠 | Michaud-Belleau 2022 |
| FDL 锁定白噪声 | `pri.fdl_locking_noise_nonlinearity` | 锁定伺服底噪非线性耦合 | Grabielle 2025 |
| 巨型 IFOG 热相噪声 | `pri.fiber_thermal_phase_noise_giant_ifog` | 长光纤温度漂移 | Li 2019 |

> 跨分支隔离原则（SCHEMA §1.3）：光纤热噪声与 FP 腔热噪声虽都叫"热噪声"，但模型、主导变量、工程突破路径完全不同，保持独立节点。

---

## 三、三条主突破路径

### 路径 A · **热噪声降低**

1. 空心光纤（`ent.antiresonant_hollow_core_fiber` / `ent.ule_hollow_core_fiber_d25`）—  
   模场主要在空气/真空中，玻璃温度耦合小 → Belardi 2015 / Michaud-Belleau 2022 / Ding 2025
2. 差分 / 双缠绕抵消振动和温度（`pri.double_winding_vibration_cancellation_hjc19`） — Huang JC 2019b
3. 盘绕与温控一体化（Hu 2015 `ent.ultralow_accel_fiber_spool_h15`）

### 路径 B · **背散射抑制**

1. 更短延迟线（牺牲 Q 但降背散射，Jiang 2010 讨论）
2. 隔离器链路 + AOM 频移区分前后向（`pri.aom_heterodyne_fiber_detection`）
3. 空心光纤天然低背散射（`pri.hollow_core_fiber_low_backscattering`，Michaud-Belleau 2021）

### 路径 C · **锁定伺服优化**

1. 全光纤循环干涉仪（Gao 2025 `ent.recirculating_fiber_interferometer_g25`）— 光学等效增长延迟
2. 数字化伺服 + AI 辅助伺服整形（开放方向）

---

## 四、关键性能里程碑

| 年份 | 成果 | σ_y (1 s) | 代表 | 核心使能 |
|------|------|----------|------|---------|
| 2009 | 光纤延迟线稳频原型 | — | Kefelian 2009 | FDL 概念验证 |
| 2010 | 光纤 MZI + 法拉第反射镜 | ~10⁻¹⁴ | Jiang 2010 | AOM 外差 + FRM |
| 2015 | 热噪声模型验证 | — | Dong 2015 | Wanser 热噪声对齐 |
| 2019 | 双缠绕抗振 | — | Huang JC 2019b | 振动抵消 |
| 2022 | 空心光纤低热噪声 | — | Michaud-Belleau 2022 | HC-ARF 导光 |
| 2023 | 200 mHz 全光纤稳频 | 线宽 200 mHz | Huang 2023 | 全光纤集成 |
| 2025 | 循环光纤干涉仪 | — | Gao 2025 | 光学等效增长延迟 |

---

## 五、与 FP 腔的分工图景

```
                 超稳激光场景
                      │
          ┌───────────┴───────────┐
          │                       │
    追求最高稳定度           追求大调谐/可搬运/集成
    (< 10⁻¹⁷)                (10⁻¹⁵ 量级足够)
          │                       │
       FP 腔                  光纤延迟线
     (低温 Si + 晶体镀层)   (空心光纤 / 双缠绕)
```

光纤稳频不与 FP 腔争"绝对稳定度"，而是在**可集成、大调谐带宽、真空/低温约束弱**的场景形成互补。

---

## 六、开放问题

- 光纤延迟线绝对极限：空心光纤 + 循环结构 + 双缠绕全部叠加后理论下限？
- 与超稳激光传递（time-frequency-transfer 专题）的直接耦合路线
- 波长扩展（可见、中红外）时光纤非线性与色散的限制

---

> 本综合页由 AI 基于 YAML + INDEX 草稿而成，需要专家逐条复核数值与时间线。
