# 超稳激光专题 · `contribution_type` 档位建议草案（Phase A2 · Round 2）

> **生成方式**：全局规则 [`docs/CONTRIBUTION_TIER_RULES.md`](../docs/CONTRIBUTION_TIER_RULES.md)
> ＋ 专题原则 [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md) 的 **稳定度 > 线宽** 仲裁
> **生成日期**：2026-04-21（Round 2）  ·  **涉及论文**：78 篇  ·  **Round 1 的 🟧 breakthrough? 17 条已全部落定**
>
> **本轮变更**（相对 Round 1）：
>
> - Round 1 的 🟧 breakthrough? 17 条已用 “稳定度 > 线宽” 原则仲裁完毕（8 条升 🟥 / 9 条降 🟩）
> - 🟥 breakthrough 从 16 升到 **24**（详见下方"升格/降格"表）
> - 🟩 evidence 从 42 升到 **51**（Round 1 剩余 🟧 下沉）
> - 🟧 breakthrough? 档位已清空（0 条）
>
> **性质**：仍是 **AI 草稿 · 待专家裁决**，零 YAML 改动。专家使用方式与 Round 1 相同（`决定` 列 accept / override / ❓）。

---

## ⚡ 阶段 A3 操作说明（专家必读）

> 这是整条流水线的关键节点：A3 完成后，AI 可批量回写 78 篇 YAML 的 `meta.contribution_type`（阶段 A4），随后 lint/stats 的档位感知指标才能激活（阶段 B）。

### 操作方式

在下方逐篇清单的 **`决定`** 列填写：

| 填写内容 | 含义 |
|---------|------|
| `accept` | 同意 AI 建议，不做更改 |
| `override: breakthrough` | 降档或升档为 breakthrough |
| `override: evidence` | 降档或升档为 evidence |
| `override: framework` | 改判为 framework |
| `skip` | 暂不处理（此论文推到下轮） |

### 批量操作技巧

- 如果对某个分组（如所有 🟩 evidence）没有异议，可在分组标题旁一次性写 `批量 accept`
- 只需标注**有异议的条目**，其余视为 accept
- 专家确认完毕后，AI 将执行阶段 A4（批量回写 YAML），无需手工逐一修改文件

### 当前建议分布

| 档位 | 数量 | 是否有异议？ |
|------|-----:|-------------|
| 🟥 breakthrough | 24 | 请逐条核查（见下方清单） |
| 🟦 framework | 3 | 可直接 accept |
| 🟩 evidence | 51 | 如无异议可批量 accept |

---

## 新分布

| 档位 | 数量 | 占比 | 说明 |
|------|-----:|-----:|------|
| 🟥 breakthrough | 24 | 30.8% | landmark 论文 + 稳定度/长期/子分支纪录 + 可复用新机制 |
| 🟦 framework | 3 | 3.8% | 综述 / 教科书 / 路线图 |
| 🟩 evidence | 51 | 65.4% | 默认档位：新数据点 / 工程复现 / 线宽纪录（但 σ_y 未刷新）|
| **合计** | **78** | 100% | — |

> **相对 SCHEMA §9.1 预期（15–22 篇 breakthrough）**：当前 🟥 24 条（30.8%）略高于预期上沿；此偏高源于专题原则 “稳定度 > 线宽” 把一批子分支稳定度纪录（SHB、光纤、HC-fiber 等）升格所致，符合超稳激光突破史密度高于通用领域的实情。若专家认为仍偏高，可把子分支 landmark 再做一次下沉。

---

## 逐篇清单（按档位分组，组内按年份升序）

### 🟥 breakthrough（24 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `drever1983.yaml` | 1983 | 🟥 breakthrough | ❓ | Laser phase and frequency stabilization using an optical resonator | 领域共识级 landmark 论文（手工标注） |
| 2 | `shaddock1999.yaml` | 1999 | 🟥 breakthrough | ❓ | Frequency locking a laser to an optical cavity by use of spatial mode interference | 领域共识级 landmark 论文（手工标注） |
| 3 | `young1999.yaml` | 1999 | 🟥 breakthrough | ❓ | Visible Lasers with Subhertz Linewidths | 领域共识级 landmark 论文（手工标注） |
| 4 | `numata2004.yaml` | 2004 | 🟥 breakthrough | ❓ | Thermal-Noise Limit in the Frequency Stabilization of Lasers with Rigid Cavities | 领域共识级 landmark 论文（手工标注） |
| 5 | `webster2007.yaml` | 2007 | 🟥 breakthrough | ❓ | Vibration insensitive optical cavity | 领域共识级 landmark 论文（手工标注） |
| 6 | `kim2008.yaml` | 2008 | 🟥 breakthrough | ❓ | Drift-free femtosecond timing synchronization of remote optical and microwave sources | 🧭 专题原则（稳定度>线宽）：10 h sub-10 fs 长期稳定度纪录（长期漂移自由） |
| 7 | `webster2008.yaml` | 2008 | 🟥 breakthrough | ❓ | Thermal-noise-limited optical cavity | 🧭 专题原则（稳定度>线宽）：首次直接实验验证 FP 腔达到热噪声极限（Numata 2004 理论闭环） |
| 8 | `kefelian2009.yaml` | 2009 | 🟥 breakthrough | ❓ | Ultralow-frequency-noise stabilization of a laser by locking to an optical fiber-delay lin | 🧭 专题原则（稳定度>线宽）：光纤干涉仪子分支首次 40 dB 级降噪高性能演示（新机制分支） |
| 9 | `jiang2010.yaml` | 2010 | 🟥 breakthrough | ❓ | An agile laser with ultra-low frequency noise and high sweep linearity | 领域共识级 landmark 论文（手工标注） |
| 10 | `thorpe2011.yaml` | 2011 | 🟥 breakthrough | ❓ | Frequency stabilization to 6×10⁻¹⁶ via spectral-hole burning | 🧭 专题原则（稳定度>线宽）：SHB 稳频子分支首次 10^-16 级 σ_y（子分支稳定度纪录） |
| 11 | `kessler2012.yaml` | 2012 | 🟥 breakthrough | ❓ | A sub-40-mHz-linewidth laser based on a silicon single-crystal optical cavity | 领域共识级 landmark 论文（手工标注） |
| 12 | `aasi2013.yaml` | 2013 | 🟥 breakthrough | ❓ | Enhanced sensitivity of the LIGO gravitational wave detector by using squeezed states of l | note 含 world-record/打破极限 |
| 13 | `cole2013.yaml` | 2013 | 🟥 breakthrough | ❓ | Tenfold reduction of Brownian noise in high-reflectivity optical coatings | 领域共识级 landmark 论文（手工标注） |
| 14 | `zhang2014_ram.yaml` | 2014 | 🟥 breakthrough | ❓ | Reduction of residual amplitude modulation to 1×10⁻⁶ for frequency modulation and laser st | 🧭 专题原则（稳定度>线宽）：RAM 抑制至 1 ppm 使 σ_y 接近热噪声极限（可复用机制 + 稳定度） |
| 15 | `hafner2015.yaml` | 2015 | 🟥 breakthrough | ❓ | 8×10⁻¹⁷ fractional laser frequency instability with a long room-temperature cavity | 领域共识级 landmark 论文（手工标注） |
| 16 | `matei2017.yaml` | 2017 | 🟥 breakthrough | ❓ | 1.5 μm Lasers with Sub-10 mHz Linewidth | 领域共识级 landmark 论文（手工标注） |
| 17 | `zhang2017.yaml` | 2017 | 🟥 breakthrough | ❓ | Ultrastable Silicon Cavity in a Continuously Operating Closed-Cycle Cryostat at 4 K | note 含 world-record/打破极限 |
| 18 | `robinson2019.yaml` | 2019 | 🟥 breakthrough | ❓ | Crystalline optical cavity at 4 K with thermal-noise-limited instability and ultralow drif | 领域共识级 landmark 论文（手工标注） |
| 19 | `michaudbelleau2022.yaml` | 2022 | 🟥 breakthrough | ❓ | Fundamental thermal noise in antiresonant hollow-core fibers | 🧭 专题原则（稳定度>线宽）：首次评估 HC-fiber 基础热噪声（新 pri.* 级机制；跨分支原理隔离） |
| 20 | `huang2023.yaml` | 2023 | 🟥 breakthrough | ❓ | All-fiber-based ultrastable laser with long-term frequency stability of 1.1×10⁻¹⁴ | 🧭 专题原则（稳定度>线宽）：全光纤长期稳定度 1.1×10^-14 @1000s（子分支长期纪录） |
| 21 | `kedar2023.yaml` | 2023 | 🟥 breakthrough | ❓ | Frequency stability of cryogenic silicon cavities with semiconductor crystalline coatings | 🧭 专题原则（稳定度>线宽）：发现双折射噪声新机制 + 晶体镀层低温硅腔 σ_y 3.5–5.5×10^-17（首次表征） |
| 22 | `chen2025.yaml` | 2025 | 🟥 breakthrough | ❓ | A laser with instability reaching 10⁻¹⁷ based on a 10-cm-long silicon cavity at sub-5-K te | 领域共识级 landmark 论文（手工标注） |
| 23 | `parke2025.yaml` | 2025 | 🟥 breakthrough | ❓ | Three hundred microsecond optical cavity storage time and 10⁻⁷ active RAM cancellation for | 领域共识级 landmark 论文（手工标注） |
| 24 | `lee2026.yaml` | 2026 | 🟥 breakthrough | ❓ | Frequency Stability of 2.5×10⁻¹⁷ from a Si Cavity with AlGaAs Crystalline Mirrors | 领域共识级 landmark 论文（手工标注） |

### 🟦 framework（3 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `kogelnik1966.yaml` | 1966 | 🟦 framework | ❓ | Laser Beams and Resonators | source_type=review_paper（综述/教材） |
| 2 | `adhikari2014.yaml` | 2014 | 🟦 framework | ❓ | Gravitational radiation detection with laser interferometry | source_type=review_paper（综述/教材） |
| 3 | `steinlechner2018.yaml` | 2018 | 🟦 framework | ❓ | Development of mirror coatings for gravitational-wave detectors | title/note 指示综述/roadmap/tutorial |

### 🟩 evidence（51 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `braun1995.yaml` | 1995 | 🟩 evidence | ❓ | Continuous-wave mode-locked solid-state lasers with enhanced spatial hole burning, Part I: | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 2 | `kartner1995.yaml` | 1995 | 🟩 evidence | ❓ | Continuous-wave mode-locked solid-state lasers with enhanced spatial hole burning, Part II | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 3 | `konz2003.yaml` | 2003 | 🟩 evidence | ❓ | Temperature and concentration dependence of optical dephasing, spectral-hole lifetime, and | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 4 | `nelson2008.yaml` | 2008 | 🟩 evidence | ❓ | Relative Intensity Noise Suppression for RF Photonic Links | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 5 | `meiser2009.yaml` | 2009 | 🟩 evidence | ❓ | Prospects for a Millihertz-Linewidth Laser | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 6 | `millo2009.yaml` | 2009 | 🟩 evidence | ❓ | Ultra-stable lasers based on vibration insensitive cavities | 🧭 专题原则（稳定度>线宽）：FS 镜热噪声降 ~2× 属工程复现；σ_y 5.6×10^-16 未破 Young 1999 纪录 |
| 7 | `legero2010.yaml` | 2010 | 🟩 evidence | ❓ | Tuning the thermal expansion properties of optical reference cavities with fused silica mi | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 8 | `jiang2011.yaml` | 2011 | 🟩 evidence | ❓ | Making optical atomic clocks more stable with 10⁻¹⁶-level laser stabilization | 🧭 专题原则（稳定度>线宽）：σ_y 2×10^-16 为 Yb 光钟应用里程碑而非超稳激光自身突破 |
| 9 | `webster2011.yaml` | 2011 | 🟩 evidence | ❓ | Force-insensitive optical cavity | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 10 | `argence2012.yaml` | 2012 | 🟩 evidence | ❓ | Prototype of an ultra-stable optical cavity for space applications | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 11 | `leibrandt2013.yaml` | 2013 | 🟩 evidence | ❓ | Absolute and Relative Stability of an Optical Frequency Reference Based on Spectral Hole B | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 12 | `mohle2013.yaml` | 2013 | 🟩 evidence | ❓ | Highly stable piezoelectrically tunable optical cavities | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 13 | `chen2014.yaml` | 2014 | 🟩 evidence | ❓ | A compact, robust, and transportable ultra-stable laser with a fractional frequency instab | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 14 | `belardi2015.yaml` | 2015 | 🟩 evidence | ❓ | Design and Properties of Hollow Antiresonant Fibers for the Visible and Near Infrared Spec | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 15 | `cook2015.yaml` | 2015 | 🟩 evidence | ❓ | Laser-Frequency Stabilization Based on Steady-State Spectral-Hole Burning in Eu³⁺:Y₂SiO₅ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 16 | `dong2015.yaml` | 2015 | 🟩 evidence | ❓ | Subhertz linewidth laser by locking to a fiber delay line | 🧭 专题原则（稳定度>线宽）：亚赫兹线宽 0.67 Hz 为 Kéfélian 2009 机制的工程延伸（线宽纪录不升级） |
| 17 | `hu2015.yaml` | 2015 | 🟩 evidence | ❓ | An optical fiber spool for laser stabilization with reduced acceleration sensitivity to 10 | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 18 | `cole2016.yaml` | 2016 | 🟩 evidence | ❓ | High-performance near- and mid-infrared crystalline coatings | 🧭 专题原则（稳定度>线宽）：AlGaAs 镀层工程性能延伸（Cole 2013 extension），无新原理 |
| 19 | `grote2016.yaml` | 2016 | 🟩 evidence | ❓ | High power and ultra-low-noise photodetector for squeezed-light enhanced gravitational wav | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 20 | `potnis2016.yaml` | 2016 | 🟩 evidence | ❓ | Note: Broadband low-noise photodetector for Pound-Drever-Hall laser stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 21 | `tai2016.yaml` | 2016 | 🟩 evidence | ❓ | Electro-optic modulator with ultra-low residual amplitude modulation for frequency modulat | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 22 | `wu2016.yaml` | 2016 | 🟩 evidence | ❓ | 0.26-Hz-linewidth ultrastable lasers at 1557 nm | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 23 | `gobron2017.yaml` | 2017 | 🟩 evidence | ❓ | Dispersive heterodyne probing method for laser frequency stabilization based on spectral h | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 24 | `tai2017.yaml` | 2017 | 🟩 evidence | ❓ | Transportable 1555-nm Ultra-Stable Laser with Sub-0.185-Hz Linewidth | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 25 | `didier2018.yaml` | 2018 | 🟩 evidence | ❓ | Ultracompact reference ultralow expansion glass cavity | 🧭 专题原则（稳定度>线宽）：ultracompact SWaP 探索，σ_y 7.5×10^-15 不破纪录 |
| 26 | `jin2018.yaml` | 2018 | 🟩 evidence | ❓ | Laser frequency instability of 2×10⁻¹⁶ by stabilizing to 30-cm-long Fabry-Pérot cavities a | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 27 | `li2018.yaml` | 2018 | 🟩 evidence | ❓ | An improved strontium lattice clock with 10⁻¹⁶ level laser frequency stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 28 | `marchio2018.yaml` | 2018 | 🟩 evidence | ❓ | Optical performance of large-area crystalline coatings | 🧭 专题原则（稳定度>线宽）：大面积晶体镀层工程表征，属 characterization |
| 29 | `tao2018.yaml` | 2018 | 🟩 evidence | ❓ | A vibration-insensitive-cavity design holds impact of higher than 100g | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 30 | `yan2018.yaml` | 2018 | 🟩 evidence | ❓ | Multi-cavity-stabilized ultrastable laser | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 31 | `didier2019.yaml` | 2019 | 🟩 evidence | ❓ | 946-nm Nd:YAG digital-locked laser at 1.1×10⁻¹⁶ in 1 s and transfer-locked to a cryogenic  | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 32 | `herbers2019.yaml` | 2019 | 🟩 evidence | ❓ | Phase noise of frequency doublers in optical clock lasers | 🧭 专题原则（稳定度>线宽）：证明 PPLN SHG 不是限制因素（negative characterization） |
| 33 | `huangjc2019.yaml` | 2019 | 🟩 evidence | ❓ | All-fiber-based laser with 200 mHz linewidth | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 34 | `huangjc2019b.yaml` | 2019 | 🟩 evidence | ❓ | Vibration-insensitive fiber spool for laser stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 35 | `li2019.yaml` | 2019 | 🟩 evidence | ❓ | Thermal phase noise in giant interferometric fiber optic gyroscopes | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 36 | `loh2019.yaml` | 2019 | 🟩 evidence | ❓ | Ultra-narrow linewidth Brillouin laser with nanokelvin temperature self-referencing | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 37 | `olson2019.yaml` | 2019 | 🟩 evidence | ❓ | Ramsey-Bordé Matter-Wave Interferometry for Laser Frequency Stabilization at 10⁻¹⁶ Frequen | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 38 | `sanjuan2019.yaml` | 2019 | 🟩 evidence | ❓ | Long-term stable optical cavity for special relativity tests in space | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 39 | `chen2020.yaml` | 2020 | 🟩 evidence | ❓ | Laser frequency instability of 6×10⁻¹⁶ using 10-cm-long cavities on a cubic spacer | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 40 | `dixneuf2020.yaml` | 2020 | 🟩 evidence | ❓ | Ultra-low intensity noise, all fiber 365 W linearly polarized single frequency laser at 10 | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 41 | `galland2020.yaml` | 2020 | 🟩 evidence | ❓ | Double-heterodyne probing for an ultra-stable laser based on spectral hole burning in a ra | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 42 | `hafner2020.yaml` | 2020 | 🟩 evidence | ❓ | Transportable interrogation laser system with an instability of mod σ_y = 3×10⁻¹⁶ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 43 | `michaudbelleau2021.yaml` | 2021 | 🟩 evidence | ❓ | Backscattering in antiresonant hollow-core fibers: over 40 dB lower than in standard optic | 🧭 专题原则（稳定度>线宽）：HC-fiber 背向散射 −40 dB 测量属子机制 characterization，未刷新稳定度 |
| 44 | `shi2021.yaml` | 2021 | 🟩 evidence | ❓ | Thinly coated hollow core fiber for improved thermal phase-stability performance | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 45 | `herbers2022.yaml` | 2022 | 🟩 evidence | ❓ | Transportable clock laser system with an instability of 1.6×10⁻¹⁶ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 46 | `shi2022.yaml` | 2022 | 🟩 evidence | ❓ | Temperature Insensitive Delay-Line Fiber Interferometer Operating at Room Temperature | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 47 | `zuba2023.yaml` | 2023 | 🟩 evidence | ❓ | Limits of Coupling Efficiency Into Hollow-Core Antiresonant Fibres | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 48 | `ding2025.yaml` | 2025 | 🟩 evidence | ❓ | Hollow-core fiber made of ultralow expansion glass: Toward the ultimate stability for room | 🧭 专题原则（稳定度>线宽）：ULE-HCF 材料创新但无稳定度数据；暂入 evidence 待后续验证 |
| 49 | `gao2025.yaml` | 2025 | 🟩 evidence | ❓ | An Ultra-Low Frequency Noise Laser Based on All-Fiber Integrated Recirculating Interferome | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 50 | `grabielle2025.yaml` | 2025 | 🟩 evidence | ❓ | Locking noise in laser frequency stabilization to an optical fiber delay line | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 51 | `jeon2025.yaml` | 2025 | 🟩 evidence | ❓ | 10⁻¹⁵-level laser stabilization down to fiber thermal noise limit using self-homodyne dete | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |

---

## 专题原则对本轮的 8 个升格 + 9 个降格（集中展示）

> 见 [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md) §1.2 判据表。

### 升格到 🟥 breakthrough（8 条）

| 文件 | 关键信号 |
|------|----------|
| `kim2008.yaml` | 10 h sub-10 fs 长期稳定度纪录（长期漂移自由） |
| `webster2008.yaml` | 首次直接实验验证 FP 腔达到热噪声极限（Numata 2004 理论闭环） |
| `kefelian2009.yaml` | 光纤干涉仪子分支首次 40 dB 级降噪高性能演示（新机制分支） |
| `thorpe2011.yaml` | SHB 稳频子分支首次 10^-16 级 σ_y（子分支稳定度纪录） |
| `zhang2014_ram.yaml` | RAM 抑制至 1 ppm 使 σ_y 接近热噪声极限（可复用机制 + 稳定度） |
| `kedar2023.yaml` | 发现双折射噪声新机制 + 晶体镀层低温硅腔 σ_y 3.5–5.5×10^-17（首次表征） |
| `huang2023.yaml` | 全光纤长期稳定度 1.1×10^-14 @1000s（子分支长期纪录） |
| `michaudbelleau2022.yaml` | 首次评估 HC-fiber 基础热噪声（新 pri.* 级机制；跨分支原理隔离） |

### 降格到 🟩 evidence（9 条）

| 文件 | 降格理由 |
|------|----------|
| `millo2009.yaml` | FS 镜热噪声降 ~2× 属工程复现；σ_y 5.6×10^-16 未破 Young 1999 纪录 |
| `jiang2011.yaml` | σ_y 2×10^-16 为 Yb 光钟应用里程碑而非超稳激光自身突破 |
| `dong2015.yaml` | 亚赫兹线宽 0.67 Hz 为 Kéfélian 2009 机制的工程延伸（线宽纪录不升级） |
| `cole2016.yaml` | AlGaAs 镀层工程性能延伸（Cole 2013 extension），无新原理 |
| `didier2018.yaml` | ultracompact SWaP 探索，σ_y 7.5×10^-15 不破纪录 |
| `marchio2018.yaml` | 大面积晶体镀层工程表征，属 characterization |
| `herbers2019.yaml` | 证明 PPLN SHG 不是限制因素（negative characterization） |
| `michaudbelleau2021.yaml` | HC-fiber 背向散射 −40 dB 测量属子机制 characterization，未刷新稳定度 |
| `ding2025.yaml` | ULE-HCF 材料创新但无稳定度数据；暂入 evidence 待后续验证 |

---

## 附：规则速查

- 全局三档判据 → [`docs/CONTRIBUTION_TIER_RULES.md`](../docs/CONTRIBUTION_TIER_RULES.md)
- 超稳激光专题偏好（稳定度 > 线宽）→ [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md)
