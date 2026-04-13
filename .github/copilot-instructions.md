# GitHub Copilot 任务说明 — sci-logic-kb 超稳激光知识提取

## 你的任务

将 `pdfs/` 目录中的论文 PDF 提取为结构化 YAML 知识节点，存入 `papers/` 目录。

**每篇论文生成一个 YAML 文件**，格式严格遵守 `SCHEMA.md` 中的规范。

---

## 处理顺序

按以下顺序处理 `pdfs/` 中的论文（文件名含 Zotero Key）：

| 优先级 | PDF 文件 | 说明 |
|--------|---------|------|
| 1 | `TVY7T59A_matei2017.pdf` | Matei 2017 — 1.5μm 10mHz 线宽（当前最窄） |
| 2 | `YKPFKDD9_kessler2012.pdf` | Kessler 2012 — Si 单晶腔 sub-40mHz |
| 3 | `CWIHQRJD_cole2013.pdf` | Cole 2013 — 晶体镀层降低热噪声10倍 |
| 4 | `UCNS7EM7_webster2007.pdf` | Webster 2007 — 防振 FP 腔 |
| 5 | `VU2V2PTX_webster2004.pdf` | Webster 2004 — 热噪声极限实验验证 |
| 6 | `A96XGR82_webster2011.pdf` | Webster 2011 — 力不敏感腔 |
| 7 | `MW3RDB68_legero2010.pdf` | Legero 2010 — 热膨胀系数调谐 |
| 8 | `UV6S5FFL_hafner2015.pdf` | Häfner 2015 — 8×10⁻¹⁷ 不稳定度 |
| 9 | `GLXHEIPV_millo2009.pdf` | Millo 2009 — 防振腔超稳激光 |
| 10 | `H5MYBTXH_leibrandt2011.pdf` | Leibrandt 2011 — 加速度灵敏度 <10⁻¹² |
| 11 | `JIZCUZLY_robinson2019.pdf` | Robinson 2019 — 4K 晶体腔热噪声极限 |
| 12 | `8YK6EH22_kedar2023.pdf` | Kedar 2023 — 低温 Si 腔 + 晶体镀层 |
| 13 | `4GUXEM2C_cole2016.pdf` | Cole 2016 — 高性能晶体镀层 |
| 14 | `N6HILT6B_chen2025.pdf` | Chen 2025 — 4×10⁻¹⁷（最新记录） |
| 15 | `MN54T4F3_kefelian2009.pdf` | Kefelian 2009 — 光纤延迟线锁频 |
| 16 | `W8K5GLK6_dong2015.pdf` | Dong 2015 — 光纤延迟亚赫兹线宽 |
| 17 | `JYGVFJBN_huang2023.pdf` | Huang 2023 — 全光纤超稳激光 |
| 18 | `4GT5VD54_michaudbelleau2022a.pdf` | Michaud-Belleau 2022 — 空心光纤热噪声 |
| 19 | `DD6SE43C_michaudbelleau2021.pdf` | Michaud-Belleau 2021 — 空心光纤 RBS |
| 20 | `AHUZI4A7_tai2017.pdf` | Tai 2017 — 可搬运超稳激光 |

---

## 处理每篇论文的步骤

### 1. 阅读 PDF

完整阅读论文，重点关注：
- **摘要**：核心贡献一句话
- **引言**：与已有工作的关系，问题定义
- **实验/理论方法**：技术路线，核心装置
- **结果**：关键数值（线宽、Allan偏差、噪声谱密度等）+测量条件
- **讨论/结论**：适用范围、局限性、改进方向

### 2. 参考已有节点

**先查看 `CLAUDE.md` 中"已有节点参考"部分**，若论文中出现的概念已有节点，直接引用已有 ID，不重复定义。

常见跨文件引用：
- FP 腔相关 → `ent.fp_cavity_reference`（drever1983）或 `ent.rigid_fp_cavity`（numata2004）
- PDH 原理 → `pri.pdh_heterodyne_detection`（drever1983）
- 热噪声原理 → `pri.brownian_thermal_noise_fdt`（numata2004）
- 激光线宽指标 → `met.laser_linewidth`（drever1983）

### 3. 生成 YAML 文件

文件命名：`papers/{first_author_lowercase}{year}.yaml`

**严格按照 `SCHEMA.md` 中的模板格式**，包含：
- `meta`：完整文献元数据
- `entities`：新出现的技术实体（勿重复已有节点）
- `principles`：新原理（勿重复）
- `methods`：新方法
- `metrics`：新指标（含数值+条件+置信度）
- `relations`：所有语义关系（必须有 `source.claim`）

### 4. 更新队列

在 `QUEUE.md` 中将对应论文的 `[ ]` 改为 `[x]`。

在 `SCHEMA.md` 的"已处理论文"表中补充记录。

### 5. 提交

```
git add papers/{filename}.yaml QUEUE.md SCHEMA.md
git commit -m "add {author}{year}: {核心贡献一句话}"
```

---

## 质量要求（必须满足）

1. **节点 ID 全局唯一**：检查 `papers/` 目录所有已有文件，避免 ID 冲突
2. **关系有原文支撑**：每条 `relation` 的 `source.claim` 必须是原文中的真实论断
3. **数值有条件**：`demonstrated_value.value` 必须配有 `conditions`（测量条件、腔参数等）
4. **跨文件引用**：已有节点直接引用 ID，不重建
5. **不创建孤立节点**：每个节点至少有一条 relation 连接到其他节点
6. **方法≠实体**：PDH/Tilt/Fiber Delay 是 `meth.`，不是 `ent.`

---

## 领域背景知识

**超稳激光的核心指标**（重要性递减）：
1. 分数频率不稳定度 σ_y(τ)（Allan 偏差）— 最重要
2. 激光线宽（Hz）
3. 频率噪声谱密度 S_ν(f)（Hz²/Hz 或 Hz/√Hz）

**三分支架构**（所有论文都对应其中某个分支）：
```
超稳激光
├── 分支1：频率参考部件（FP 腔 OR 光纤干涉仪）
├── 分支2：误差探测方法（PDH / Tilt Locking / 光纤延迟锁频）
└── 分支3：反馈执行部件（EOM / AOM / PZT）
```

**关键物理概念**：
- **热噪声**（Brownian noise）：f^(-1/2) 谱，由涨落耗散定理决定
- **振动噪声**：腔长随加速度变化，需防振设计（< 10⁻¹¹ /g）
- **ULE/Zerodur**：低膨胀玻璃，有零膨胀系数温度点（CTE zero-crossing）
- **精细度**（Finesse）：腔品质因子，越高线宽越窄，热噪声越低

---

## 特别说明：Webster 系列论文的知识脉络

Webster 系列（2004/2007/2011）和 Millo 2009 解决"振动噪声"问题：
- Webster 2004：测量热噪声极限（配合 Numata 2004 理论）
- Webster 2007：设计防振腔（加速度不敏感结构）
- Webster 2011：力不敏感腔（进一步改进）
- Millo 2009：应用防振腔实现超稳激光

这些论文共享以下原理节点（已在 numata2004.yaml 中定义）：
- `pri.brownian_thermal_noise_fdt`
- `pri.vibration_isolation_pendulum`（young1999.yaml 中定义）

---

## 输出示例

参考 `papers/numata2004.yaml` 的格式（最完整的示例）。

每篇论文提取约：
- 2-5 个新实体节点
- 2-4 个新原理节点
- 1-2 个新方法节点（如有）
- 2-5 个新指标节点
- 5-15 条关系

---

*此说明由知识库负责人生成，最后更新：2026-04-14*
