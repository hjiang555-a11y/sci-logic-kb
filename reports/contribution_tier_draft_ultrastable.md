# 超稳激光专题 · `contribution_type` 档位建议草案（Phase A2）

> **生成方式**：`scripts/_phase_a2/`（一次性脚本）+ AI 启发式 + 领域共识 landmark 白名单
> **生成日期**：2026-04-21  ·  **涉及论文**：78 篇（全专题覆盖）  ·  **规则依据**：[`docs/CONTRIBUTION_TIER_RULES.md`](../docs/CONTRIBUTION_TIER_RULES.md)
>
> **性质**：**AI 草稿 · 待专家裁决**。本文件不直接用于自动化流程；零 YAML 改动。
>
> **专家使用方式**：
>
> - **Accept**：在 `决定` 列勾选 ✅，表示采纳建议档位
> - **Override**：在 `决定` 列写出实际档位（例如 `→ evidence`、`→ breakthrough`），并在 `专家备注` 列给一句理由
> - **存疑**：在 `决定` 列保留 ❓，留给下一轮处理（阶段 A3 之外）
>
> **下一步**（需专家触发）：
>
> 1. 专家勾选完成后提交 PR 或评论，AI 会根据 `决定` 列的最终档位批量回写 78 个 YAML 文件的 `meta.contribution_type`（阶段 A4，机械改动）
> 2. 回写完成后进入阶段 B：lint / stats 引入档位感知，重估 chain-gap / orphan 真实基线

---

## 汇总分布（AI 建议）

| 档位 | 数量 | 占比 | 说明 |
|------|-----:|-----:|------|
| 🟥 breakthrough | 16 | 20.5% | AI 高置信：领域共识 landmark 或明确打破纪录 / 提出新原理 |
| 🟧 breakthrough? | 17 | 21.8% | AI 低置信：含 首次/best/多原理 等弱信号，**需专家确认是否真正跨 regime** |
| 🟦 framework | 3 | 3.8% | 综述 / 教科书 / 路线图 |
| 🟩 evidence | 42 | 53.8% | 默认档位：在已有坐标轴上提供新数据点或工程复现（大多数论文的合法归宿） |
| **合计** | **78** | 100% | — |

> **预期分布调整方向**：`breakthrough?` 17 条需专家在 breakthrough / evidence 间裁决；结合 SCHEMA §9.2 映射与领域直觉，最终 `breakthrough` 总数期望收敛在 **15–22 篇** 范围（占比 ~20%–28%）。若最终比例显著偏离，说明规则书需要调整，并按 TODO.md「风险与对策」第 3 条处理。

---

## 逐篇清单（按档位分组，组内按年份升序）

### 🟥 breakthrough（16 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `drever1983.yaml` | 1983 | 🟥 breakthrough | ❓ | Laser phase and frequency stabilization using an optical resonator | 领域共识级 landmark 论文（手工标注） |
| 2 | `shaddock1999.yaml` | 1999 | 🟥 breakthrough | ❓ | Frequency locking a laser to an optical cavity by use of spatial mode interference | 领域共识级 landmark 论文（手工标注） |
| 3 | `young1999.yaml` | 1999 | 🟥 breakthrough | ❓ | Visible Lasers with Subhertz Linewidths | 领域共识级 landmark 论文（手工标注） |
| 4 | `numata2004.yaml` | 2004 | 🟥 breakthrough | ❓ | Thermal-Noise Limit in the Frequency Stabilization of Lasers with Rigid Cavities | 领域共识级 landmark 论文（手工标注） |
| 5 | `webster2007.yaml` | 2007 | 🟥 breakthrough | ❓ | Vibration insensitive optical cavity | 领域共识级 landmark 论文（手工标注） |
| 6 | `jiang2010.yaml` | 2010 | 🟥 breakthrough | ❓ | An agile laser with ultra-low frequency noise and high sweep linearity | 领域共识级 landmark 论文（手工标注） |
| 7 | `kessler2012.yaml` | 2012 | 🟥 breakthrough | ❓ | A sub-40-mHz-linewidth laser based on a silicon single-crystal optical cavity | 领域共识级 landmark 论文（手工标注） |
| 8 | `aasi2013.yaml` | 2013 | 🟥 breakthrough | ❓ | Enhanced sensitivity of the LIGO gravitational wave detector by using squeezed states of l | note 含 world-record/打破极限 |
| 9 | `cole2013.yaml` | 2013 | 🟥 breakthrough | ❓ | Tenfold reduction of Brownian noise in high-reflectivity optical coatings | 领域共识级 landmark 论文（手工标注） |
| 10 | `hafner2015.yaml` | 2015 | 🟥 breakthrough | ❓ | 8×10⁻¹⁷ fractional laser frequency instability with a long room-temperature cavity | 领域共识级 landmark 论文（手工标注） |
| 11 | `matei2017.yaml` | 2017 | 🟥 breakthrough | ❓ | 1.5 μm Lasers with Sub-10 mHz Linewidth | 领域共识级 landmark 论文（手工标注） |
| 12 | `zhang2017.yaml` | 2017 | 🟥 breakthrough | ❓ | Ultrastable Silicon Cavity in a Continuously Operating Closed-Cycle Cryostat at 4 K | note 含 world-record/打破极限 |
| 13 | `robinson2019.yaml` | 2019 | 🟥 breakthrough | ❓ | Crystalline optical cavity at 4 K with thermal-noise-limited instability and ultralow drif | 领域共识级 landmark 论文（手工标注） |
| 14 | `chen2025.yaml` | 2025 | 🟥 breakthrough | ❓ | A laser with instability reaching 10⁻¹⁷ based on a 10-cm-long silicon cavity at sub-5-K te | 领域共识级 landmark 论文（手工标注） |
| 15 | `parke2025.yaml` | 2025 | 🟥 breakthrough | ❓ | Three hundred microsecond optical cavity storage time and 10⁻⁷ active RAM cancellation for | 领域共识级 landmark 论文（手工标注） |
| 16 | `lee2026.yaml` | 2026 | 🟥 breakthrough | ❓ | Frequency Stability of 2.5×10⁻¹⁷ from a Si Cavity with AlGaAs Crystalline Mirrors | 领域共识级 landmark 论文（手工标注） |

### 🟧 breakthrough?（17 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `kim2008.yaml` | 2008 | 🟧 breakthrough? | ❓ | Drift-free femtosecond timing synchronization of remote optical and microwave sources | note 含 首次/first（待核对范围） |
| 2 | `webster2008.yaml` | 2008 | 🟧 breakthrough? | ❓ | Thermal-noise-limited optical cavity | note 含 首次/first（待核对范围） |
| 3 | `kefelian2009.yaml` | 2009 | 🟧 breakthrough? | ❓ | Ultralow-frequency-noise stabilization of a laser by locking to an optical fiber-delay lin | note 含 首次/first（待核对范围） |
| 4 | `millo2009.yaml` | 2009 | 🟧 breakthrough? | ❓ | Ultra-stable lasers based on vibration insensitive cavities | note 含 首次/first（待核对范围）；note 含 最佳/best（可能是阶段性纪录） |
| 5 | `jiang2011.yaml` | 2011 | 🟧 breakthrough? | ❓ | Making optical atomic clocks more stable with 10⁻¹⁶-level laser stabilization | note 含 首次/first（待核对范围） |
| 6 | `thorpe2011.yaml` | 2011 | 🟧 breakthrough? | ❓ | Frequency stabilization to 6×10⁻¹⁶ via spectral-hole burning | note 含 首次/first（待核对范围） |
| 7 | `zhang2014_ram.yaml` | 2014 | 🟧 breakthrough? | ❓ | Reduction of residual amplitude modulation to 1×10⁻⁶ for frequency modulation and laser st | note 含 首次/first（待核对范围） |
| 8 | `dong2015.yaml` | 2015 | 🟧 breakthrough? | ❓ | Subhertz linewidth laser by locking to a fiber delay line | note 含 首次/first（待核对范围） |
| 9 | `cole2016.yaml` | 2016 | 🟧 breakthrough? | ❓ | High-performance near- and mid-infrared crystalline coatings | note 含 首次/first（待核对范围） |
| 10 | `didier2018.yaml` | 2018 | 🟧 breakthrough? | ❓ | Ultracompact reference ultralow expansion glass cavity | note 含 首次/first（待核对范围） |
| 11 | `marchio2018.yaml` | 2018 | 🟧 breakthrough? | ❓ | Optical performance of large-area crystalline coatings | note 含 首次/first（待核对范围） |
| 12 | `herbers2019.yaml` | 2019 | 🟧 breakthrough? | ❓ | Phase noise of frequency doublers in optical clock lasers | note 含 最佳/best（可能是阶段性纪录） |
| 13 | `michaudbelleau2021.yaml` | 2021 | 🟧 breakthrough? | ❓ | Backscattering in antiresonant hollow-core fibers: over 40 dB lower than in standard optic | note 含 首次/first（待核对范围） |
| 14 | `michaudbelleau2022.yaml` | 2022 | 🟧 breakthrough? | ❓ | Fundamental thermal noise in antiresonant hollow-core fibers | note 含 首次/first（待核对范围） |
| 15 | `huang2023.yaml` | 2023 | 🟧 breakthrough? | ❓ | All-fiber-based ultrastable laser with long-term frequency stability of 1.1×10⁻¹⁴ | note 含 最佳/best（可能是阶段性纪录） |
| 16 | `kedar2023.yaml` | 2023 | 🟧 breakthrough? | ❓ | Frequency stability of cryogenic silicon cavities with semiconductor crystalline coatings | note 含 首次/first（待核对范围） |
| 17 | `ding2025.yaml` | 2025 | 🟧 breakthrough? | ❓ | Hollow-core fiber made of ultralow expansion glass: Toward the ultimate stability for room | note 含 首次/first（待核对范围） |

### 🟦 framework（3 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `kogelnik1966.yaml` | 1966 | 🟦 framework | ❓ | Laser Beams and Resonators | source_type=review_paper（综述/教材） |
| 2 | `adhikari2014.yaml` | 2014 | 🟦 framework | ❓ | Gravitational radiation detection with laser interferometry | source_type=review_paper（综述/教材） |
| 3 | `steinlechner2018.yaml` | 2018 | 🟦 framework | ❓ | Development of mirror coatings for gravitational-wave detectors | title/note 指示综述/roadmap/tutorial |

### 🟩 evidence（42 篇）

| # | 文件 | 年份 | AI 建议 | 决定 | 标题（截断） | 一句依据 |
|---|------|------|---------|------|-------------|----------|
| 1 | `braun1995.yaml` | 1995 | 🟩 evidence | ❓ | Continuous-wave mode-locked solid-state lasers with enhanced spatial hole burning, Part I: | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 2 | `kartner1995.yaml` | 1995 | 🟩 evidence | ❓ | Continuous-wave mode-locked solid-state lasers with enhanced spatial hole burning, Part II | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 3 | `konz2003.yaml` | 2003 | 🟩 evidence | ❓ | Temperature and concentration dependence of optical dephasing, spectral-hole lifetime, and | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 4 | `nelson2008.yaml` | 2008 | 🟩 evidence | ❓ | Relative Intensity Noise Suppression for RF Photonic Links | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 5 | `meiser2009.yaml` | 2009 | 🟩 evidence | ❓ | Prospects for a Millihertz-Linewidth Laser | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 6 | `legero2010.yaml` | 2010 | 🟩 evidence | ❓ | Tuning the thermal expansion properties of optical reference cavities with fused silica mi | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 7 | `webster2011.yaml` | 2011 | 🟩 evidence | ❓ | Force-insensitive optical cavity | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 8 | `argence2012.yaml` | 2012 | 🟩 evidence | ❓ | Prototype of an ultra-stable optical cavity for space applications | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 9 | `leibrandt2013.yaml` | 2013 | 🟩 evidence | ❓ | Absolute and Relative Stability of an Optical Frequency Reference Based on Spectral Hole B | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 10 | `mohle2013.yaml` | 2013 | 🟩 evidence | ❓ | Highly stable piezoelectrically tunable optical cavities | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 11 | `chen2014.yaml` | 2014 | 🟩 evidence | ❓ | A compact, robust, and transportable ultra-stable laser with a fractional frequency instab | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 12 | `belardi2015.yaml` | 2015 | 🟩 evidence | ❓ | Design and Properties of Hollow Antiresonant Fibers for the Visible and Near Infrared Spec | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 13 | `cook2015.yaml` | 2015 | 🟩 evidence | ❓ | Laser-Frequency Stabilization Based on Steady-State Spectral-Hole Burning in Eu³⁺:Y₂SiO₅ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 14 | `hu2015.yaml` | 2015 | 🟩 evidence | ❓ | An optical fiber spool for laser stabilization with reduced acceleration sensitivity to 10 | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 15 | `grote2016.yaml` | 2016 | 🟩 evidence | ❓ | High power and ultra-low-noise photodetector for squeezed-light enhanced gravitational wav | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 16 | `potnis2016.yaml` | 2016 | 🟩 evidence | ❓ | Note: Broadband low-noise photodetector for Pound-Drever-Hall laser stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 17 | `tai2016.yaml` | 2016 | 🟩 evidence | ❓ | Electro-optic modulator with ultra-low residual amplitude modulation for frequency modulat | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 18 | `wu2016.yaml` | 2016 | 🟩 evidence | ❓ | 0.26-Hz-linewidth ultrastable lasers at 1557 nm | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 19 | `gobron2017.yaml` | 2017 | 🟩 evidence | ❓ | Dispersive heterodyne probing method for laser frequency stabilization based on spectral h | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 20 | `tai2017.yaml` | 2017 | 🟩 evidence | ❓ | Transportable 1555-nm Ultra-Stable Laser with Sub-0.185-Hz Linewidth | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 21 | `jin2018.yaml` | 2018 | 🟩 evidence | ❓ | Laser frequency instability of 2×10⁻¹⁶ by stabilizing to 30-cm-long Fabry-Pérot cavities a | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 22 | `li2018.yaml` | 2018 | 🟩 evidence | ❓ | An improved strontium lattice clock with 10⁻¹⁶ level laser frequency stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 23 | `tao2018.yaml` | 2018 | 🟩 evidence | ❓ | A vibration-insensitive-cavity design holds impact of higher than 100g | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 24 | `yan2018.yaml` | 2018 | 🟩 evidence | ❓ | Multi-cavity-stabilized ultrastable laser | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 25 | `didier2019.yaml` | 2019 | 🟩 evidence | ❓ | 946-nm Nd:YAG digital-locked laser at 1.1×10⁻¹⁶ in 1 s and transfer-locked to a cryogenic  | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 26 | `huangjc2019.yaml` | 2019 | 🟩 evidence | ❓ | All-fiber-based laser with 200 mHz linewidth | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 27 | `huangjc2019b.yaml` | 2019 | 🟩 evidence | ❓ | Vibration-insensitive fiber spool for laser stabilization | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 28 | `li2019.yaml` | 2019 | 🟩 evidence | ❓ | Thermal phase noise in giant interferometric fiber optic gyroscopes | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 29 | `loh2019.yaml` | 2019 | 🟩 evidence | ❓ | Ultra-narrow linewidth Brillouin laser with nanokelvin temperature self-referencing | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 30 | `olson2019.yaml` | 2019 | 🟩 evidence | ❓ | Ramsey-Bordé Matter-Wave Interferometry for Laser Frequency Stabilization at 10⁻¹⁶ Frequen | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 31 | `sanjuan2019.yaml` | 2019 | 🟩 evidence | ❓ | Long-term stable optical cavity for special relativity tests in space | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 32 | `chen2020.yaml` | 2020 | 🟩 evidence | ❓ | Laser frequency instability of 6×10⁻¹⁶ using 10-cm-long cavities on a cubic spacer | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 33 | `dixneuf2020.yaml` | 2020 | 🟩 evidence | ❓ | Ultra-low intensity noise, all fiber 365 W linearly polarized single frequency laser at 10 | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 34 | `galland2020.yaml` | 2020 | 🟩 evidence | ❓ | Double-heterodyne probing for an ultra-stable laser based on spectral hole burning in a ra | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 35 | `hafner2020.yaml` | 2020 | 🟩 evidence | ❓ | Transportable interrogation laser system with an instability of mod σ_y = 3×10⁻¹⁶ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 36 | `shi2021.yaml` | 2021 | 🟩 evidence | ❓ | Thinly coated hollow core fiber for improved thermal phase-stability performance | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 37 | `herbers2022.yaml` | 2022 | 🟩 evidence | ❓ | Transportable clock laser system with an instability of 1.6×10⁻¹⁶ | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 38 | `shi2022.yaml` | 2022 | 🟩 evidence | ❓ | Temperature Insensitive Delay-Line Fiber Interferometer Operating at Room Temperature | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 39 | `zuba2023.yaml` | 2023 | 🟩 evidence | ❓ | Limits of Coupling Efficiency Into Hollow-Core Antiresonant Fibres | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 40 | `gao2025.yaml` | 2025 | 🟩 evidence | ❓ | An Ultra-Low Frequency Noise Laser Based on All-Fiber Integrated Recirculating Interferome | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 41 | `grabielle2025.yaml` | 2025 | 🟩 evidence | ❓ | Locking noise in laser frequency stabilization to an optical fiber delay line | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |
| 42 | `jeon2025.yaml` | 2025 | 🟩 evidence | ❓ | 10⁻¹⁵-level laser stabilization down to fiber thermal noise limit using self-homodyne dete | 在已有坐标轴上提供新数据点 / 工程复现 / 参数变体 |

---

## 附：规则书速查

| 档位 | 判据要点 | 最低入库门槛 |
|------|---------|-------------|
| `breakthrough` | 打破纪录 / 新 `pri.*` / 证伪 / 新 `meth.*` / 领域 landmark | 完整限制链 + `breakthrough_paths` + `historical_landmarks.best_demonstration` |
| `evidence` | 默认档位；在已有节点上加数据点 / 复现 / 参数扫描 | 1 条关系挂已有节点 + 1 个 `demonstrated_value`（带 `conditions`） + `source.claim` |
| `framework` | 综述 / 路线图 / 教材 | 只定义 Level 0/1 + tier: meta/domain 原理；不定义 Level 2 实例 |

完整版见 [`docs/CONTRIBUTION_TIER_RULES.md`](../docs/CONTRIBUTION_TIER_RULES.md)。
