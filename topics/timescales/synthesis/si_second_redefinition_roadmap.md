# SI 秒重定义路线图

> 基于 `dimarcq2024.yaml` — CCTF 官方路线图 (Metrologia 61, 012001, 2024)
> 专题: timescales | 最后更新: 2026-05-03

---

## 当前状态

- **SI 秒定义**: ¹³³Cs 基态超精细跃迁 (1967 年至今)，实现精度 ~1-2×10⁻¹⁶
- **光学频率标准**: 最佳系统不确定度已达 9.4×10⁻¹⁹ (²⁷Al⁺ 量子逻辑钟, NIST)
- **差距**: 光学标准已超越铯定义 2 个数量级，但尚未被采纳为 SI 定义基础

---

## CCTF 重定义强制性标准 (15 条)

### 核心技术标准
| 标准编号 | 要求 | 当前状态 |
|---------|------|---------|
| I.1 | 多种光学频率标准系统不确定度达 10⁻¹⁸ | ✅ 已满足 (Al⁺, Sr, Yb) |
| I.2 | 独立光钟频率比测量一致性达 5×10⁻¹⁸ | ⚠️ 部分满足，洲际比较进行中 |
| I.3 | 与当前铯定义连续性 | ✅ 已满足 |
| I.4 | 光学频率标准定期向 TAI 提供校准数据 | ⚠️ 进行中 |

### 基础设施标准
| 标准编号 | 要求 | 当前状态 |
|---------|------|---------|
| II.1 | 可持续光钟比较技术 (本地+远程) | ⚠️ 光纤链路成熟，卫星链路待改进 |
| II.2 | 重力位知识精度达 10⁻¹⁸ (~0.1 m²/s²) | ⚠️ 局部满足，全球覆盖不足 |

---

## 次级表示 (SRS) 过渡机制

当前 10 个光学跃迁 + 1 个微波跃迁 (⁸⁷Rb) 已被 CCTF 采纳为秒的次级表示。
SRS 是铯定义到光学定义的过渡桥梁：光学标准在重定义前通过 SRS 参与 TAI 校准。

---

## 待解决关键问题

1. **单一跃迁 vs 多跃迁平均**: 社区仍未达成共识 (Option 1: 单跃迁简洁, Option 2: 多跃迁平均灵活)
2. **洲际比较**: 5×10⁻¹⁸ 一致性目标需依赖超稳光纤链路和先进卫星双向传递
3. **UTC/TAI 算法**: 光钟是否需连续运行，还是间歇校准即可？

---

## 关联专题

- `frequency-standards`: 光钟技术 (`ent.optical_frequency_standard` → `fortier2026.yaml`)
- `time-frequency-transfer`: 远程比对基础设施 (`global_dissemination.md`)
- `optical-frequency-combs`: 频率梳桥接 (`ent.optical_frequency_comb` → `giunta2019.yaml`)

---

## 参考节点

- `ent.si_second_definition` — Level 0 系统级实体, 定义于 `dimarcq2024.yaml`
- `pri.redefinition_criteria_second` — 15 条强制性标准体系
- `pri.secondary_representation_si_second` — 秒次级表示机制
- `met.optical_clock_systematic_uncertainty` — 当前最佳: 9.4×10⁻¹⁹
