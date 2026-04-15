# GitHub PR 分批处理计划 — sci-logic-kb

**制定日期**: 2026-04-14（更新: 2026-04-15 Cleanup Pass）  
**当前状态**: 27 篇论文已入库（papers/ 目录），约 58 篇待处理（QUEUE.md 含少量重复条目）  
**Schema 版本**: v3.1（以 `SCHEMA.md` 为准）  
**项目定位补充**: 知识库需能回答技术能力边界、限制链（BOUNDED-BY）问题

---

## 项目定位更新

基于用户要求，知识库设计需增强以下能力：

1. **限制链（BOUNDED-BY）**: 节点需标注限制性原理、当前是否为活跃瓶颈、突破路径
2. **边界条件与前提**: 原理节点使用 `conditions`/`preconditions`/`invalidated_when` 描述适用范围
3. **争议与开放问题**: 使用 `contested_claims`/`open_questions` 显式记录

体现在提取策略（对齐 SCHEMA.md v3.1）：
- 原理节点 (`pri.*`): 强化 `conditions`、`preconditions`、`invalidated_when`、`open_questions` 字段
- 指标节点 (`met.*`): 记录 `demonstrated_value` 配合 `conditions`，标注 `historical_landmarks`（首次/最佳）
- 关系 (`rel.*`): BOUNDED-BY 必填 `is_system_limit` + `verification_status` + `source.claim`；CONDITIONED-BY 必填接口契约

---

## 分批原则

1. **主题集中**: 每批围绕一个技术分支，保持上下文连贯
2. **规模适中**: 每批5–10篇论文，适合GitHub Copilot单次处理
3. **优先级排序**: 按CLAUDE.md建议的优先级顺序
4. **质量检查**: 每批完成后执行项目标准检查，修正明显问题
5. **GitHub Copilot优先**: 尽可能使用Copilot，仅在需要本地PDF读取/复杂推理时用Claude Code

---

## 各批详细列表

### Batch 1: 低温硅腔与镀层技术 (6篇) — **已完成 3 篇，剩余 3 篇**
> 目标: 完善低温硅腔技术链，明确晶体镀层的性能边界

| Zotero Key | 作者年份 | 标题 | 状态 |
|------------|----------|------|------|
| `8YK6EH22` | Kedar 2023 | Frequency stability of cryogenic silicon cavities with semiconductor crystalline coatings | ✅ `kedar2023.yaml` |
| `N6HILT6B` | Chen 2025 | A laser with instability reaching 4×10⁻¹⁷ based on a 10-cm-long silicon cavity | ✅ `chen2025.yaml` |
| `4GUXEM2C` | Cole 2016 | High-performance near- and mid-infrared crystalline coatings | ✅ `cole2016.yaml` |
| `LCMWCIWB` | Marchio 202x | Optical performance of large-area crystalline coatings | 待处理 |
| `L6KKLLSR` | Steinlechner 201x | Development of mirror coatings for gravitational-wave detectors | 待处理 |
| `N9AGEQ8S` | Zhang 201x | Ultrastable Silicon Cavity in a Continuously Operating Closed-Cycle | 待处理 |

**技术焦点**: 硅腔CTE零点、晶体镀层损耗角、低温机械Q增强、热噪声极限（BOUNDED-BY 链完善）

---

### Batch 2: FP腔防振改进 (7篇) — **已完成 4 篇，剩余 3 篇**
> 目标: 系统化振动不敏感腔设计，明确加速度灵敏度改善路径

| Zotero Key | 作者年份 | 标题 | 状态 |
|------------|----------|------|------|
| `VU2V2PTX` | Webster 2008 | Thermal-noise-limited optical cavity | ✅ `webster2008.yaml` |
| `MW3RDB68` | Legero 2010 | Tuning the thermal expansion properties of optical reference cavities | ✅ `legero2010.yaml` |
| `GLXHEIPV` | Millo 2009 | Ultrastable lasers based on vibration insensitive cavities | ✅ `millo2009.yaml` |
| `H5MYBTXH` | Leibrandt 2013 | Cavity-stabilized laser with acceleration sensitivity below 10⁻¹² | ✅ `leibrandt2013.yaml` |
| `U4Z95559` | Tao 201x | A vibration-insensitive-cavity design holds impact of higher than 100g | 待处理 |
| `KH82PQJ2` | Hu 2015 | Optical fiber spool for laser stabilization with reduced acceleration sensitivity | 待处理（重复条目，见光纤分支） |
| `5DCNFGX4` | 黄军超 2019 | Vibration-insensitive fiber spool for laser stabilization | 待处理 |

**技术焦点**: 四点对称支撑、自平衡安装、加速度灵敏度补偿（CONDITIONED-BY 接口）、惯性力前馈

---

### Batch 3: 光纤稳频系列 A (9篇) — **已完成 2 篇，剩余 7 篇**
> 目标: 建立光纤延迟线稳频技术链，明确背向散射噪声等限制（BOUNDED-BY 链）

| Zotero Key | 作者年份 | 标题 | 状态 |
|------------|----------|------|------|
| `MN54T4F3` | Kéfélian 2009 | Ultralow-frequency-noise stabilization of a laser by locking to a fiber | ✅ `kefelian2009.yaml`（早期批次完成） |
| `W8K5GLK6` | Dong 2015 | Subhertz linewidth laser by locking to a fiber delay line | ✅ `dong2015.yaml`（早期批次完成） |
| `F2GG2N6W` | Huang 202x | All-fiber-based laser with 200 mHz linewidth | 待处理 |
| `JYGVFJBN` | Huang 2023 | All-fiber-based ultrastable laser with long-term frequency stability | ✅ `huang2023.yaml`（早期批次完成） |
| `RENEQVU9` | Wei 202x | Support-Free Thermally Insensitive Hollow Core Fiber Coil | 待处理 |
| `QLXRP462` | Shi 202x | Thinly coated hollow core fiber for improved thermal phase-stability | 待处理 |
| `UKBFZLXG` | Shi 202x | Temperature Insensitive Delay-Line Fiber Interferometer | 待处理 |
| `DD6SE43C` | Michaud-Belleau 2021 | Backscattering in antiresonant hollow-core fibers: over 40 dB lower | ✅ `michaudbelleau2021.yaml` |
| `4GT5VD54` | Michaud-Belleau 2022 | Fundamental thermal noise in antiresonant hollow-core fibers | ✅ `michaudbelleau2022.yaml` |

**技术焦点**: Rayleigh 背向散射噪声（BOUNDED-BY 链）、光纤热相位噪声、空心光纤性能边界、跨分支原理隔离

---

### Batch 4: 光纤稳频系列 B (10篇) — **中高优先级**
> 目标: 完善空心光纤技术链，明确耦合效率等工程限制

| Zotero Key | 作者年份 | 标题 | 关键提取点 |
|------------|----------|------|------------|
| `QGLVTMB7` | Ding 202x | Hollow-core fiber made of ultralow expansion glass | ULE玻璃空心光纤的热性能边界 |
| `GIUQZ2EE` | Zuba 202x | Limits of Coupling Efficiency Into Hollow-Core Antiresonant Fibers | 反谐振空心光纤耦合效率极限 |
| `SBPRDKPV` | Jeon 202x | 10⁻¹⁵-level laser stabilization down to fiber thermal noise limit | 光纤热噪声极限下的10⁻¹⁵稳频 |
| `XSMPRNT3` | Grabielle 2025 | Locking noise in laser frequency stabilization to an optical fiber | 光纤锁频的锁定噪声机制与限制 |
| `JAW66GYL` | J. Gao 2025 | Ultra-Low Frequency Noise Laser Based on All-Fiber Integrated Interferometer | 全光纤集成干涉仪的超低频率噪声边界 |
| `ULMQ3IXP` | Winful 1985 | SELF-INDUCED POLARIZATION CHANGES IN BIREFRINGENT OPTICAL FIBERS | 双折射光纤偏振变化的基础限制 |
| `2F3PD62T` | Belardi 201x | Design and Properties of Hollow Antiresonant Fibers | 反谐振空心光纤设计属性与限制 |
| `ELKHJ5GL` | Li 2019 | Thermal phase noise in giant interferometric fiber optic gyro | 巨型干涉光纤陀螺热相位噪声边界 |
| `HJZ6BVYE` | Dixneuf 202x | Ultra-low intensity noise all-fiber laser | 全光纤激光器的超低强度噪声极限 |
| `KH82PQJ2` | Hu 2015 | An optical fiber spool for laser stabilization with reduced acceleration sensitivity | (重复，检查后决定是否处理) |

**技术焦点**: 空心光纤耦合损耗、热噪声极限、偏振稳定性、集成干涉仪性能边界

---

### Batch 5: 空间/可搬运应用 (7篇) — **已完成 1 篇，剩余 6 篇**
> 目标: 梳理空间与可搬运腔设计，明确环境适应性（CONDITIONED-BY 接口）

| Zotero Key | 作者年份 | 标题 | 状态 |
|------------|----------|------|------|
| `RP8Q44RZ` | Argence 201x | Prototype of an ultra-stable optical cavity for space applications | 待处理 |
| `PHRXF4IL` | Didier 201x | Ultracompact reference ultralow expansion glass cavity | 待处理 |
| `H3HYK5D3` | Sanjuan 201x | Long-term stable optical cavity for special relativity tests in space | 待处理 |
| `X7XXKXDZ` | Hafner 201x | Transportable interrogation laser system with an instability of m×10⁻¹⁶ | 待处理 |
| `NU79W75P` | Herbers 202x | Transportable clock laser system with an instability of 1.6×10⁻¹⁶ | 待处理 |
| `AHUZI4A7` | Tai 2017 | Transportable 1555-nm Ultra-Stable Laser with Sub-0.185-Hz Linewidth | ✅ `tai2017.yaml` |
| `WTUHUAQ7` | Qun-Feng 201x | A compact, robust, and transportable ultra-stable laser | 待处理 |

**技术焦点**: 空间环境 CONDITIONED-BY 接口、紧凑化与热噪声权衡、可搬运性-稳定度折中、长期稳定性

---

### Batch 6: 时钟应用与器件技术 (8篇) — **中低优先级**
> 目标: 连接超稳激光与原子钟应用，明确器件技术限制

| Zotero Key | 作者年份 | 标题 | 关键提取点 |
|------------|----------|------|------------|
| `WP8FMS5N` | Herbers 201x | Phase noise of frequency doublers on optical clock lasers | 光钟激光频率倍频器的相位噪声边界 |
| `RAC23NZV` | Jiang 201x | Making optical atomic clocks more stable with 10⁻¹⁶-level laser | 10⁻¹⁶激光提升光钟稳定度的限制 |
| `AFFU5KGB` | Li 201x | An improved strontium lattice clock with 10⁻¹⁶ level laser frequency | 锶晶格钟的激光频率要求边界 |
| `FIJXUVZV` | Tai 2016 | Electro-optic modulator with ultra-low residual amplitude modulation | 超低剩余振幅调制EOM的技术极限 |
| `WDGF2B36` | Potnis 201x | Broadband low-noise photodetector for PDH | PDH宽带低噪声光电探测器性能边界 |
| `VM5MJ9B3` | Grote 2016 | High power and ultra-low-noise photodetector for squeezed-light | 压缩光高功率超低噪声探测器的限制 |
| `8MNIBZEW` | Möhle 2013 | Highly stable piezoelectrically tunable optical cavities | 压电可调腔的稳定性与调谐范围权衡 |
| `XAKCIXKT` | Nelson 200x | Relative Intensity Noise Suppression for RF Photonic Links | RF光子链路的相对强度噪声抑制极限 |

**技术焦点**: 频率倍频器相位噪声、EOM剩余振幅调制、光电探测器噪声边界、压电调谐稳定性

---

### Batch 7: 前沿方法与基础理论 (10篇) — **低优先级**
> 目标: 补充谱孔燃烧等替代方法，完善基础理论覆盖

| Zotero Key | 作者年份 | 标题 | 关键提取点 |
|------------|----------|------|------------|
| `Q2MRB267` | Thorpe 201x | Frequency stabilization to 6×10⁻¹⁶ via spectral-hole burning | 谱孔燃烧稳频到6×10⁻¹⁶的技术边界 |
| `KZJHGH3N` | Cook 201x | Laser-Frequency Stabilization Based on Steady-State Spectral-Hole | 稳态谱孔燃烧稳频的限制因素 |
| `U2LXSU62` | Parke 2025 | Three hundred microsecond optical cavity storage time and 10⁻⁷ acceleration insensitivity | 300 μs腔存储时间与加速度不敏感性的极限 |
| `ZDF94KK5` | Matei 2017 (v2?) | 1.5 μm Lasers with Sub-10 mHz Linewidth (重复检查) | 重复论文，验证后决定处理 |
| `PZGR9S7S` | Wu 201x | 0.26-Hz-linewidth ultrastable lasers at 1557 nm | 1557 nm 0.26 Hz线宽激光的性能边界 |
| `6R3RCHPT` | Jin 2018 | Laser frequency instability of 2×10⁻¹⁶ | 2×10⁻¹⁶激光频率不稳定的技术条件 |
| `MIAVJSIK` | Didier 201x | 946-nm Nd:YAG digital-locked laser at 1.1×10⁻¹⁶ | 946 nm Nd:YAG数字锁频激光的限制 |
| `HKYLIW8U` | Gobron 2017 | Dispersive heterodyne probing method for laser frequency stabilization | 色散外差探测方法的技术边界 |
| `MPWLNUIH` | Galland 202x | Double-heterodyne probing for an ultra-stable laser based on spectral hole | 基于谱孔的双外差探测限制 |
| `UQL6FYN7` | Kogelnik 1966 | LASER BEAMS AND RESONATORS (基础教材) | 高斯光束与谐振腔基础理论边界 |

**技术焦点**: 谱孔燃烧稳频极限、腔存储时间边界、数字锁频技术、外差探测方法限制

---

## 质量检查标准（每批完成后执行，对齐 SCHEMA.md v3.1）

### 1. 节点唯一性检查
- [ ] 所有节点ID全局唯一（不与已有papers/*.yaml冲突）
- [ ] 节点ID符合命名规范：`ent.*`, `pri.*`, `meth.*`, `met.*`
- [ ] 跨文件引用的节点在`note`字段注明来源文件

### 2. 关系完整性检查（八种关系类型）
- [ ] 每个关系有`source.claim`字段，指向原文具体论断
- [ ] 关系包含`confidence`（established/likely/contested）
- [ ] BOUNDED-BY 必填：`is_system_limit` + `verification_status` + `source.claim`
- [ ] CONDITIONED-BY 必填：`interface_metric` + `coupling_formula` + `is_system_limit`
- [ ] `breakthrough_paths.direction` 仅引用 `pri.*` 或 `meth.*`（不得引用 `ent.*`）

### 3. 限制链与前提条件检查
- [ ] 原理节点有`conditions`，鼓励补充 `preconditions` / `invalidated_when`
- [ ] 指标节点有`demonstrated_value.conditions`（必填）
- [ ] 若论文有争议，使用 `contested_claims`（非 note）
- [ ] 若论文有未解问题，使用 `open_questions`（非 note）
- [ ] 时间演化优先填写 `historical_landmarks.first_demonstration` / `best_demonstration`

### 4. 元数据一致性
- [ ] Zotero Key正确
- [ ] 节点文件包含完整 meta（zotero_key, title, year, first_author, journal, doi）

### 5. 架构符合性
- [ ] 没有把"方法"建为"实体"（如PDH是`meth`，不是`ent`）
- [ ] 关系类型在八种之内（PART-OF, CHARACTERIZED-BY, OPERATIONALIZED-AS, ENABLED-BY, BOUNDED-BY, DERIVED-FROM, CONDITIONED-BY, COMPETES-WITH）
- [ ] 未使用废弃关系（GOVERNED-BY, EQUIVALENT-IN-CONTEXT, SUPPORTED-BY, BREAKTHROUGH-VIA）
- [ ] Level 2 实例节点不使用 COMPETES-WITH

---

## 执行建议

### GitHub Copilot工作流
1. **批量任务创建**: 每批创建一个GitHub Issue，标题"Batch N: [主题]处理"
2. **Copilot指令**: 在Issue中粘贴本计划的批次表格和质量检查清单
3. **PR提交**: 每批完成后创建一个PR，包含所有新增的YAML文件和更新的QUEUE.md、SCHEMA.md
4. **审查要点**: 重点审查技术边界标注和限制因素提取

### 本地Claude Code辅助场景
- PDF文件在Zotero中但未上传至GitHub（需本地读取）
- 复杂逻辑推理（如判断方法vs实体分类）
- 跨批次节点引用一致性检查
- Obsidian节点文件同步

### 时间估计
- 每批处理时间：2-4小时（GitHub Copilot为主）
- 质量检查时间：1小时/批
- 总预计时间：7批 × 3-5小时 ≈ 25-35小时

---

## 下一步行动

### 推荐的下一轮优先方向

**优先继续 FP 腔主线**（Batch 1/2 剩余）：
- 理由：当前已建立较完整的 FP 腔 BOUNDED-BY 链（brownian_thermal_noise_fdt → 多实例验证），
  剩余 Batch 1 的 3 篇（Marchio, Steinlechner, Zhang-Si）和 Batch 2 的 3 篇（Tao, Hu, 黄军超）
  可继续补全镀层和防振两条线，投入产出比高。
- 其中 `N9AGEQ8S`（Zhang Si 闭循环）和 `U4Z95559`（Tao 抗冲击）知识贡献明确。
- `LCMWCIWB`（Marchio）和 `L6KKLLSR`（Steinlechner）偏引力波应用，可暂缓至下下轮。

**光纤分支暂缓大规模处理**：
- 光纤分支已有 7 篇入库（jiang2010, kefelian2009, dong2015, huang2023, michaudbelleau2021, michaudbelleau2022）
  + 若干跨文件引用，当前架构（pri.fiber_delay_line_frequency_ref, pri.rayleigh_backscattering_noise,
  pri.hollow_core_fiber_low_backscattering, pri.hollow_core_fiber_thermal_noise）已可支撑。
- 剩余光纤论文（Batch 3 余 4 篇 + Batch 4 全部）多为工程实现细节，优先级可降。

### 暂缓处理的条目

1. `ZDF94KK5`（疑似 Matei 2017 重复条目）：待确认后决定删除或合并
2. `KH82PQJ2`（Hu 2015）：在 QUEUE.md 中出现两次（FP 腔 + 光纤），待确认归属后处理一次
3. `SBPRDKPV`（Jeon 202x）：在 QUEUE.md 中出现两次（时钟应用 + 光纤），待确认归属后处理一次
4. 56 篇无 PDF 论文：不在本轮处理范围

> **注意**: 本计划遵循"GitHub Copilot优先"原则，最大限度利用Copilot处理结构化提取任务，仅在必要时使用本地Claude Code。
> **Schema 依据**: 以 `SCHEMA.md` v3.1 为准。本文档中的术语应与 SCHEMA.md 保持一致。