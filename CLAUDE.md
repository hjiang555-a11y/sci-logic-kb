# Claude Code 行为规范 — sci-logic-kb

本文件是 Claude Code 在此仓库中工作时的行为规范。

## 仓库用途

**时间频率计量科研知识库**（超稳激光专题）。
从 Zotero 管理的论文 PDF 中提取结构化知识，存储为 YAML 节点图。

详细 Schema 见 `SCHEMA.md`，待处理论文见 `QUEUE.md`。

---

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
- 识别该论文的**核心贡献**（方法创新/原理解析/实验结果）
- 提取节点（entities/principles/methods/metrics）
- 建立关系（relations）
- 检查是否有跨文件引用的已有节点

### 步骤 5：写入文件

写入 `papers/{first_author_lower}{year}.yaml`，例如 `papers/matei2017.yaml`。

### 步骤 6：更新队列

将 `QUEUE.md` 中该论文的 `[ ]` 改为 `[x]`，并在 `SCHEMA.md` 的"已处理论文"表中补充记录。

### 步骤 7：提交

```bash
git add papers/{filename}.yaml QUEUE.md SCHEMA.md
git commit -m "add {author}{year}: {论文核心贡献一句话}"
git push
```

---

## 质量检查清单

提交前确认：

- [ ] 每个节点 ID 全局唯一（不与 papers/ 目录其他文件冲突）
- [ ] 所有 relation 有 `source.claim`（原文论断）
- [ ] 所有 metric 的 `demonstrated_value` 有 `conditions`
- [ ] 原理节点有 `conditions` 或 `applicable_when`
- [ ] 跨文件引用的节点在 `note` 中注明来源文件
- [ ] 没有把"方法"建为"实体"（PDH 是 `meth`，不是 `ent`）

---

## 节点 ID 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 实体 | `ent.{描述词}_{可选后缀}` | `ent.ule_fp_cavity_young99` |
| 原理 | `pri.{描述词}` | `pri.brownian_thermal_noise_fdt` |
| 方法 | `meth.{描述词}` | `meth.pdh_locking` |
| 指标 | `met.{描述词}_{可选后缀}` | `met.laser_linewidth_563nm` |
| 关系 | `rel.{文件首字母缩写}{两位序号}` | `rel.N01`（N=Numata） |

---

## 已有节点参考（跨文件引用时使用）

### 来自 drever1983.yaml

- `ent.fp_cavity_reference` — F-P 参考腔
- `ent.rf_phase_modulator` — 射频相位调制器
- `pri.pdh_heterodyne_detection` — PDH 射频边带光学外差探测原理
- `pri.pdh_high_speed_regime` — PDH 高速相位检测域
- `pri.shot_noise_frequency_limit` — 散粒噪声频率稳定度极限
- `meth.pdh_locking` — PDH 锁频方法
- `met.laser_linewidth` — 激光线宽（通用）
- `met.freq_spectral_density` — 激光频率噪声谱密度

### 来自 young1999.yaml

- `ent.ule_fp_cavity_young99` — ULE F-P 参考腔（Young 1999）
- `ent.vibration_isolated_table_young99` — 隔振光学平台
- `pri.ule_zero_cte` — ULE 玻璃零热膨胀系数原理
- `pri.mirror_heating_cavity_shift` — 腔镜加热导致谐振频率漂移
- `pri.vibration_isolation_pendulum` — 低频弹性悬挂隔振原理
- `met.laser_linewidth_563nm` — 0.6 Hz 线宽（Young 1999）
- `met.fractional_freq_instability_y99` — 3×10⁻¹⁶ @ 1s

### 来自 shaddock1999.yaml

- `ent.split_photodetector` — 分割光电探测器
- `ent.tilting_mirror` — 倾斜反射镜
- `pri.off_resonance_reference_light` — **元原理**：非谐振参考光（PDH 和 Tilt Locking 共有）
- `pri.gouy_phase_discrimination` — Gouy 相位横模鉴别原理
- `pri.spatial_homodyne_detection` — 空间零差探测（分割探测器）
- `meth.tilt_locking` — Tilt Locking 方法
- `met.servo_bandwidth` — 伺服带宽

### 来自 numata2004.yaml

- `ent.rigid_fp_cavity` — 刚性 F-P 参考腔（通用）
- `ent.mirror_coating` — 腔镜高反射镀层
- `ent.mirror_substrate` — 腔镜基底
- `ent.spacer_ule` — 腔间隔物
- `pri.brownian_thermal_noise_fdt` — 布朗热噪声——涨落耗散定理
- `pri.mirror_substrate_noise_dominance` — 镜底物热噪声主导（84%）
- `met.thermal_noise_freq_psd` — 热噪声频率噪声谱密度

### 来自 webster2007.yaml

- `ent.vibration_insensitive_fp_cavity_w07` — 水平方向振动不敏感 FP 腔（Webster 2007）
- `pri.cavity_deformation_compensation` — 腔镜中心位移补偿原理（四点对称支撑）
- `pri.ule_cte_zero_crossing` — ULE 零膨胀点工作原理
- `met.vibration_sensitivity_w07` — 加速度灵敏度（< 1 kHz/(m/s²)）
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

- `ent.self_balancing_long_cavity_h15` — 自平衡安装 48 cm ULE 腔（Level 2，< 2×10⁻¹⁰/g 全向）
- `pri.long_cavity_thermal_noise_reduction` — 增长腔长降低热噪声分数贡献（σ_y ∝ 1/L）
- `met.fractional_freq_instability_h15` — <1×10⁻¹⁶（1–1000 s，Häfner 2015，室温 48 cm 腔）
- `met.acceleration_sensitivity_h15` — κ < 2×10⁻¹⁰/g 全向（自平衡安装）

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

*本文件由 Claude Code 生成，更新日期：2026-04-14*
