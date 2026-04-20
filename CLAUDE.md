# Claude Code 行为规范 — sci-logic-kb

本文件是 Claude Code 在此仓库中工作时的行为规范。

## 仓库用途

**时间频率计量科研知识库**（多专题，当前已建超稳激光专题）。
从 Zotero 管理的论文 PDF 中提取结构化知识，存储为 YAML 节点图。

详细 Schema 见 `SCHEMA.md`，专题体系见 `TOPICS.md`。

---

## GitHub Copilot 优先原则

**优先使用 GitHub Copilot 完成工作，仅在 GitHub Copilot 无法完成时才使用本地 Claude Code 处理。**

具体实施：
1. **GitHub Copilot 适用场景**：
   - 代码生成（YAML 模板、Python 脚本、bash 脚本）
   - 文档撰写（README、注释、说明）
   - 代码审查和问题修复
   - 基于已有模式的重复性工作

2. **本地 Claude Code 适用场景**：
   - 需要读取本地 PDF 文件（Zotero 存储）
   - 需要调用本地工具（Read、Edit、Bash 等）
   - 需要交互式探索和决策（如关系提取、节点识别）
   - GitHub Copilot 无法直接处理的复杂逻辑推理

3. **工作流整合**：
   - 尽可能将任务分解为可 GitHub Copilot 完成的子任务
   - 使用 GitHub PR 流程管理所有更改
   - 本地处理结果必须通过 GitHub PR 提交

## 单篇论文处理流程

### 步骤 1：确定目标论文

从 `QUEUE.md` 中选取下一篇 `[ ]` 状态的论文，记录其 `ZOTERO_KEY`。

### 步骤 2：获取论文 PDF

```bash
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
ZOTERO_KEY="替换为实际KEY"

# 获取论文元数据
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(d.get('title','')); print(d.get('DOI',''))"

# 获取附件 PDF 路径
curl -s -H "Host: 127.0.0.1:23119" \
  "http://${WINDOWS_IP}:23119/api/users/19944378/items/${ZOTERO_KEY}/children" \
  | python3 -c "
import json, sys
items = json.load(sys.stdin)
for i in items:
    d = i.get('data', {})
    if d.get('itemType') == 'attachment':
        key = d.get('key', '')
        fn = d.get('filename', d.get('path', '').split('/')[-1])
        print(f'/mnt/d/Users/hjian/Zotero/storage/{key}/{fn}')
"
```

### 步骤 3：阅读 PDF

使用 `Read` 工具读取 PDF 文件（最多 20 页/次，大论文分批读取）。

### 步骤 4：提取 YAML

按 `SCHEMA.md` 中的模板提取：
- 识别该论文的**核心贡献**（方法创新/原理解析/实验结果，或专题框架定义）
- 提取节点（entities/principles/methods/metrics）
- 建立关系（relations）
- 检查是否有跨文件引用的已有节点

若该论文是综述/路线图，且主要贡献在于建立专题顶层架构而非提供新的具体技术演示：
- 使用 `meta.contribution_type: framework`
- 优先定义 Level 0/1 顶层实体、tier: meta/domain 原理、跨专题 `CONDITIONED-BY` 接口
- 不把具体实验系统的 Level 2 参数实例作为该文件的主职责

### 步骤 5：写入文件

写入 `topics/<topic>/papers/{first_author_lower}{year}.yaml`，例如 `topics/ultrastable-laser/papers/matei2017.yaml`。

当前默认专题为 `ultrastable-laser`。

### 步骤 6：更新运维文件

- 在 `PROCESSED_PAPERS.md` 中补充论文记录
- 更新 `INDEX.md`（新节点、新指标最佳值、论文计数）
- 追加 `LOG.md` 条目（格式：`## [YYYY-MM-DD] ingest | description`）
- 若新数据与已有声明矛盾，更新相关节点的 `contested_claims` 并在 LOG.md 记录 `contradiction`
- 若存在相关综合页面（`synthesis/`），检查是否需要标注为"需要更新"

### 步骤 7：提交

```bash
git add topics/<topic>/papers/{filename}.yaml PROCESSED_PAPERS.md INDEX.md LOG.md
git commit -m "add {author}{year}: {论文核心贡献一句话}"
git push
```

---

## 质量检查清单

提交前确认：

- [ ] 每个节点 ID 全局唯一（不与同专题 papers/ 目录及其他专题的文件冲突）
- [ ] 所有 relation 有 `source.claim`（原文论断）
- [ ] 所有 metric 的 `demonstrated_value` 有 `conditions`
- [ ] 原理节点有 `conditions` 或 `applicable_when`
- [ ] 跨文件引用的节点在 `note` 中注明来源文件
- [ ] 没有把"方法"建为"实体"（PDH 是 `meth`，不是 `ent`）

---

## 节点 ID 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 实体 | `ent.{描述词}_{可选后缀}` | `ent.fp_cavity_system` |
| 原理 | `pri.{描述词}` | `pri.brownian_thermal_noise_fdt` |
| 方法 | `meth.{描述词}` | `meth.pdh_locking` |
| 指标 | `met.{描述词}_{可选后缀}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{文件首字母缩写}{两位序号}` | `rel.N01`（N=Numata） |

---

## 已有节点参考（超稳激光专题，跨文件引用时使用）

> 以下节点均位于 `topics/ultrastable-laser/papers/` 目录下。

### 来自 drever1983.yaml

**Level 2 硬件**（PDH误差探测，配套 ent.fp_cavity_system）
- `ent.rf_phase_modulator` — 射频相位调制器（EOM，产生±fm边带）

**原理**（全局，本文提出）
- `pri.pdh_heterodyne_detection` — PDH 射频边带光学外差探测原理
- `pri.pdh_high_speed_regime` — PDH 高速相位检测域（伺服带宽不受腔响应时间限制）
- `pri.shot_noise_frequency_limit` — 散粒噪声频率稳定度极限

**方法**
- `meth.pdh_locking` — PDH 锁频方法（超稳激光标准误差探测手段）

**指标**
- `met.laser_linewidth` — 激光线宽（通用，<100 Hz @ 1983年）
- `met.freq_spectral_density` — 激光频率噪声谱密度

### 来自 young1999.yaml

> `ent.fp_cavity_system` 定义于 numata2004.yaml，young1999 通过跨文件关系引用，无需重复定义。

**Level 1 实体**
- `ent.dye_laser_563nm` — 563 nm 染料激光器

**Level 2 子单元**（PART-OF ent.fp_cavity_system）
- `ent.vibration_isolation` — 被动弹性悬挂隔振系统（手术管悬挂，f₀ ≈ 0.3 Hz）
- `ent.two_stage_pdh_lock_young99` — 两级级联 PDH 锁频系统

**外围条件（ext）**
- `ent.vibration_environment` — 环境振动条件（CONDITIONED-BY 接口节点）

**原理**（全局，本文提出）
- `pri.ule_zero_cte` — ULE 玻璃零热膨胀系数原理
- `pri.mirror_heating_cavity_shift` — 腔镜加热导致谐振频率漂移（≈1 Hz/mW）
- `pri.vibration_isolation_pendulum` — 低频弹性悬挂隔振原理

**指标**
- `met.laser_linewidth_563nm` — 0.6 Hz 线宽（Young 1999，已在热噪声极限）
- `met.fractional_freq_instability_y99` — 3×10⁻¹⁶ @ 1 s
- `met.acceleration_sensitivity_y99` — 腔加速度灵敏度 ≈100 kHz/(m/s²)
- `met.freq_noise_from_vibration` — 振动引起的频率噪声（接口指标）

**方法**
- `meth.two_stage_pdh_visible` — 两级级联 PDH 锁频（可见光）

### 来自 shaddock1999.yaml

**Level 2 硬件**（Tilt Locking误差探测，配套 ent.fp_cavity_system）
- `ent.split_photodetector` — 分割光电探测器（替代PDH的RF探测+解调电路）
- `ent.tilting_mirror` — 倾斜反射镜（激励腔TEM10横模）

**原理**（全局）
- `pri.off_resonance_reference_light` — **元原理**（tier: meta）：非谐振参考光（PDH 和 Tilt Locking 共有）
- `pri.gouy_phase_discrimination` — Gouy 相位横模鉴别原理（Tilt Locking 物理基础）
- `pri.spatial_homodyne_detection` — 空间零差探测原理（分割探测器差分）

**方法**
- `meth.tilt_locking` — Tilt Locking（倾斜锁定）方法

**指标**
- `met.servo_bandwidth` — 伺服带宽（通用指标，Tilt Locking典型值 ~230 Hz）

### 来自 numata2004.yaml

**Level 1 实体**（主节点，跨文件引用请用此 ID）
- `ent.fp_cavity_system` — 刚性 F-P 参考腔系统

**Level 2 子单元**（PART-OF ent.fp_cavity_system）
- `ent.mirror_substrate` — 腔镜基底（热噪声 84%，首要改善目标）
- `ent.mirror_coating` — 腔镜高反射镀层（热噪声 15%）
- `ent.spacer_ule` — 腔间隔物（热噪声 1%，可忽略）

**原理**（全局，本文提出）
- `pri.brownian_thermal_noise_fdt` — 布朗热噪声——涨落耗散定理
  - 内含 condition_variables：φ（损耗角）/ w₀（光斑半径）/ T（温度）/ L（腔长）
  - ⚠ `pri.beam_radius_scaling` 和 `pri.low_loss_substrate_improvement` 不是独立节点，是该原理的 condition_variables 优化方向字段
- `pri.mirror_substrate_noise_dominance` — 镜底物 84% 主导（engineering 推论）

**指标**
- `met.thermal_noise_freq_psd` — 热噪声频率噪声谱密度（~0.13 Hz/√Hz @ 1 Hz）

### 来自 webster2007.yaml

- `ent.cutout_cavity_mount_w07` — 切口腔体安装设计（Level 2，PART-OF fp_cavity_system，COMPETES-WITH vibration_isolation）
- `pri.cavity_deformation_compensation` — 腔镜中心位移补偿原理（四点对称支撑）
- `pri.ule_cte_zero_crossing` — ULE 零膨胀点工作原理
- `met.acceleration_sensitivity_vertical_w07` — 竖直加速度灵敏度 < 0.1 kHz/ms⁻²（Webster 2007）
- `ent.vibration_environment` — 环境振动噪声（外围条件节点，ext）

### 来自 kessler2012.yaml

- `ent.si_crystal_fp_cavity_k12` — Si 单晶低温 FP 腔（Level 1，124 K，~1×10⁻¹⁶）
- `pri.silicon_cte_zero_crossing_124k` — Si 单晶 CTE 零点（124.2 K，dα/dT=1.71×10⁻⁸ K⁻²）
- `pri.cryogenic_mechanical_q_enhancement` — 低温机械 Q 增强（Si Q > 10⁷ at 124 K）
- `met.fractional_freq_instability_k12` — ~1×10⁻¹⁶（Kessler 2012，Si 腔）
- `met.laser_linewidth_k12` — <35 mHz 单激光线宽（Kessler 2012）
- `met.vibration_sensitivity_k12` — κ < 10⁻¹⁰/g（Si 腔全向）

### 来自 cole2013.yaml

- `ent.algaas_crystalline_mirror_c13` — AlGaAs/GaAs 晶体镀层腔镜（Level 2，φ≤2.5×10⁻⁵，室温）
- `pri.crystalline_coating_low_brownian_noise` — 单晶镀层低布朗热噪声原理（φ_AlGaAs/φ_IBS ≈ 1/16）
- `met.algaas_coating_loss_angle_c13` — 晶体镀层损耗角 φ≤2.5×10⁻⁵（室温上限）

### 来自 matei2017.yaml

- `pri.flicker_noise_linewidth_divergence` — 闪变频率噪声线宽发散问题与实用线宽定义
- `met.fractional_freq_instability_m17` — mod σ_y = 4×10⁻¹⁷（Matei 2017，Si 腔镀层极限）
- `met.laser_linewidth_m17` — 5–10 mHz 个体线宽（Matei 2017，Si2–Si3 拍频）
- `met.optical_coherence_time_m17` — 11 s (Ramsey) 至 55 s (回溯)（Matei 2017）

### 来自 hafner2015.yaml

- `ent.self_balancing_long_cavity_h15` — 自平衡安装 48 cm ULE 腔（**Level 1**，COMPETES-WITH fp_cavity_system 和 si_crystal_fp_cavity_k12）
- `pri.long_cavity_thermal_noise_reduction` — 增长腔长降低热噪声分数贡献（σ_y ∝ 1/L）
- `met.fractional_freq_instability_h15` — <1×10⁻¹⁶（1–1000 s，Häfner 2015，室温 48 cm 腔）
- `met.acceleration_sensitivity_h15` — κ < 2×10⁻¹⁰/g 全向（自平衡安装）

### 来自 webster2007.yaml

- `ent.cutout_cavity_mount_w07` — 切口腔体安装设计（Level 2，PART-OF fp_cavity_system，COMPETES-WITH vibration_isolation）
- `pri.cavity_deformation_compensation` — 腔镜中心位移补偿原理（四点对称支撑）
- `pri.ule_cte_zero_crossing` — ULE 零膨胀点工作原理
- `met.acceleration_sensitivity_vertical_w07` — 竖直加速度灵敏度 < 0.1 kHz/ms⁻²（Webster 2007）
- `met.acceleration_sensitivity_horizontal_w07` — 水平加速度灵敏度 3.7 kHz/ms⁻²（Webster 2007）
- `ent.vibration_environment` — 环境振动噪声（外围条件节点，ext）

### 来自 lee2026.yaml

- `ent.si_crystal_17k_fp_cavity_l26` — Si 单晶 17 K FP 腔（Level 1，AlGaAs 晶体镀层，mod σ_y=2.5×10⁻¹⁷）
- `pri.silicon_cte_zero_crossing_17k` — Si CTE 第二零点（17 K）
- `pri.optical_frequency_averaging` — 多腔光学频率平均（双腔平均 √2 提升）
- `met.fractional_freq_instability_l26` — mod σ_y = 2.5×10⁻¹⁷（Lee 2026，世界纪录）
- `met.algaas_coating_loss_angle_17k_l26` — AlGaAs 镀层损耗角 φ < 2.3×10⁻⁵（17 K）

### 来自 jiang2010.yaml

- `ent.fiber_interferometer` — 光纤迈克尔逊干涉仪（频率参考）
- `ent.faraday_rotation_mirror` — 法拉第旋转镜
- `pri.fiber_delay_line_frequency_ref` — 光纤延迟线频率参考原理
- `pri.rayleigh_backscattering_noise` — Rayleigh 背向散射噪声原理
- `pri.aom_heterodyne_fiber_detection` — AOM 外差检测（光纤）
- `meth.fiber_delay_locking` — 光纤延迟线锁频方法
- `met.freq_noise_psd_fiber` — 光纤锁定频率噪声谱密度
- `met.allan_deviation_fiber` — 光纤锁定 Allan 偏差 ~10⁻¹⁴

---

## 处理顺序建议

按照超稳激光三分支架构，优先处理填充"缺口"最大的方向：

1. **低温硅腔系列**：Robinson 2019（JIZCUZLY，4 K Si 腔）、Kedar 202x（8YK6EH22，晶体镀层+低温）
2. **FP 腔防振改进**：Webster 2011（A96XGR82，force-insensitive）、Legero 2010（MW3RDB68，热膨胀调谐）
3. **前沿记录**：Chen 2025（N6HILT6B，4×10⁻¹⁷）、Parke 2025（U2LXSU62，300 μs 存储时间）
4. **光纤稳频**：Huang 2023（JYGVFJBN，全光纤 200 mHz）
5. **其余论文**：按 QUEUE.md 顺序

---

*本文件由 Claude Code 生成，更新日期：2026-04-20*
*多专题架构升级：v4.0*
*运维层引入：v4.2（Karpathy LLM Wiki 思想整合）*

---

## 人机协作原则（v4.2 新增，inspired by Karpathy LLM Wiki）

> **核心理念**：人做策展与提问，AI 做簿记与维护。知识库的价值在于**持久复合知识**的增量构建，而非每次查询时重新发现。

### 人类角色（Domain Expert）
- **选择论文**（sourcing）：决定下一篇处理的论文
- **确认节点边界**：判断"这是新实体还是参数变体？"
- **审核争议性论断**：决定 `contested_claims` 的最终判定
- **提出探索性问题**：如"为什么 17K 比 4K 的镀层损耗更低？"
- **审核综合页面**：确认 `synthesis/` 目录下页面的准确性
- **决定 Schema 方向**：Schema 升级由人类主导

### AI 角色（Knowledge Engineer）
- **Ingest**：YAML 节点提取与维护
- **Cross-referencing**：跨文件交叉引用维护
- **Bookkeeping**：INDEX.md / LOG.md / PROCESSED_PAPERS.md 自动更新
- **Synthesis**：综合页面生成与更新
- **Lint**：健康检查与修复建议
- **Consistency check**：新论文与已有知识的矛盾检测
- **Freshness tracking**：新论文入库后标记受影响的综合页面为"需要更新"

### 运维文件导航
- **全局导航索引**：[`INDEX.md`](INDEX.md)
- **演化日志**：[`LOG.md`](LOG.md)
- **已处理论文列表**：[`PROCESSED_PAPERS.md`](PROCESSED_PAPERS.md)
- **综合分析页面**：`topics/<topic>/synthesis/`
- **完整 Schema 规范**：[`SCHEMA.md`](SCHEMA.md)（第十节定义运维操作）
