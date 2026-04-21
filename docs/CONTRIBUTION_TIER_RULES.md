# 论文贡献档位（`contribution_type`）操作规则书

> **版本**：v1（2026-04-21） · **归属**：v4.4 schema 机制落地的配套规范
> **范围**：本规则书用于决定一篇论文 YAML 头部 `meta.contribution_type` 应填 `breakthrough` / `evidence` / `framework` 中的哪一档。
> **上位规范**：[`SCHEMA.md` §9.1–9.2](../SCHEMA.md)；本文件与 SCHEMA 冲突时以 SCHEMA 为准。
>
> **使用场景**：
> - AI（Copilot / Claude）在处理新论文或既有 YAML 档位迁移时，按本规则产出建议
> - 专家在审阅分级建议表时，按本规则判断 accept / override
> - 目标是**把同类边界案例的裁决一次性写死**，避免每篇都重新讨论

---

## 一、三档的判定次序（先 framework → 再 breakthrough → 兜底 evidence）

**Step 1 — 是否是 `framework`？**

> 判据：论文主要贡献在于**建立专题顶层架构、梳理现有工作**，而非提供具体的新技术演示。

命中任一条即判为 `framework`：

1. `meta.source_type` ∈ {`review_paper`, `textbook`, `chapter`, `book_chapter`}
2. 题目或摘要明确含 `review / roadmap / tutorial / handbook / perspective / 综述 / 路线图 / 教科书`
3. 论文贡献主要是"定义 Level 0/1 顶层实体 + `tier: meta/domain` 原理 + 跨专题 `CONDITIONED-BY` 接口"，而**没有**具体 Level 2 参数实例

> ⚠ 注意："某个技术方向的首篇系统性工作"属于 `breakthrough`，不是 `framework`。框架型论文不引入 `pri.*` 新机制，仅做架构与共识梳理。

**Step 2 — 是否是 `breakthrough`？**

> 判据：论文显著推动了该分支的技术前沿。命中任一条即判 `breakthrough`。

1. **指标纪录**：在某个量化指标上打破已知最佳值（如 σ_y、linewidth、accuracy、coating loss angle）。须有可引用的原文数值与 `source.claim`
2. **新原理**：提出一个可被后续论文复用的新 `pri.*` 节点（不是"从已有原理派生一个条件变量"）
3. **证伪**：给出实证数据推翻某个既有论断（需写入 `contested_claims`）
4. **方法原创**：提出新的 `meth.*`（如 PDH、Tilt Locking、AOM 光纤外差这种级别）
5. **领域共识 landmark**：被综述 / 教科书 / 路线图反复引用的奠基性工作

> ⚠ 注意：
> - "在已有 `pri.brownian_thermal_noise_fdt` 上复现/工程化/换材料" ≠ `breakthrough`，这是 `evidence`
> - "首次在某个波长/某个温度/某个腔长上实现 X"，需要进一步看是否跨越了物理或工程 regime 才算 `breakthrough`；单纯"首次在 1064 nm 做了同样的事"属 `evidence`

**Step 3 — 兜底 `evidence`（默认档位）**

> 不满足 framework 与 breakthrough 的论文，全部归为 `evidence`。这是大多数论文的合法归宿，**不是缺陷**。

Evidence 档位论文的典型形态：
- 在已有 `ent.*` / `pri.*` / `meth.*` 上新增一个 `demonstrated_value`
- 做一次工程复现或参数扫描
- 提供跨 regime 的佐证数据点
- 进行系统集成演示（整机性能数据）

> Evidence 档位**允许** orphan 节点 / chain-gap 存在，不强求补 `breakthrough_paths`。详见 SCHEMA §9.1 与 CONTRIBUTING.md。

---

## 二、10 条边界案例裁决（一次写死，不再反复讨论）

> 格式：`案例 → 裁决 → 理由`

1. **"世界上第一台空间级超稳腔原型" (argence2012 类)** → `breakthrough?` 候选，专家确认是否打破 SWaP 指标；若仅是工程封装复现已有腔设计则 `evidence`
2. **"某团队首次复现了 Kessler 2012 结果"** → `evidence`。复现不是 breakthrough
3. **"在 1064 nm 做了 1550 nm 早已演示的 PDH 锁定"** → `evidence`。换工作波长通常不构成 regime 跨越
4. **"首次把腔长从 10 cm 加到 30 cm"** → `evidence`。参数扫描（走 condition_variables）。只有当加到某个量级首次让新限制成为主导（如 Häfner 2015 的 48 cm、Parke 2025 的 68 cm）才算 `breakthrough`
5. **"提出某 RAM 修正方案并给出实验验证"** → `breakthrough`，当该方案带来了可被后续复用的新机制 `pri.*`；否则 `evidence`
6. **"综述 + 一段作者自己的新实验"** → 按主要贡献判：若综述占主体 → `framework`；若实验是论文主干 → `breakthrough` 或 `evidence`
7. **"博士论文 / 学位论文"** → 按主要贡献判；通常是 `evidence`（工程复现 + 测量），除非明确有新原理/世界纪录
8. **"光学频率梳/光纤干涉仪在超稳激光专题下的边界论文"** → 如果该论文的主贡献是**作为超稳激光的参考或比对工具**而不是梳/光纤本身的突破 → `evidence`；如果是为超稳激光提供新的稳频原理 → 按原理判
9. **"引力波探测器相关论文（LIGO/Virgo）"** → 与超稳激光共享 FP 腔/量子噪声技术，但主贡献通常在引力波灵敏度而非腔技术，多数判 `evidence`；若引入全新激光稳频原理（如首次 squeezed light injection）则 `breakthrough`
10. **"同一作者群的系列论文（如 Webster 2007 / 2008 / 2011）"** → 只有系列首篇提出新机制时判 `breakthrough`，后续迭代（微改、外推、长期稳定性报告）判 `evidence`

---

## 三、关键互检问题（分档前先问自己 3 个问题）

1. **复用性**：这篇论文新增的 `pri.*` 会不会被后续论文引用？如果不会 → 降到 `evidence` 或并入父节点字段
2. **纪录性**：这篇论文的最佳 `demonstrated_value` 是不是在它发表时打破了公认纪录？如果没有 → 通常 `evidence`
3. **独立意义**：如果这篇论文不存在，专题架构会不会缺一块？如果答案是"没什么缺失" → `evidence`

全部否 → `evidence`。只要有一个明确的"是"，就考虑 `breakthrough`。

---

## 四、与 lint / stats 的交互（B 阶段生效，提前公示）

- `breakthrough` 档：`reasoning-chain-gap`、`orphan-node` 按现行规则 **强制**（必须补 `breakthrough_paths`、必须挂到父节点）
- `evidence` 档：`reasoning-chain-gap`、`orphan-node` **降级为 info**（不计入 TODO 缺口）
- `framework` 档：按 §9.5 规则豁免具体参数节点的约束

详细规则升级计划见 TODO.md「阶段 B」条目。

---

*本文件随专家反馈迭代。每轮修改请在顶部"版本"字段升号，并在 LOG.md 追加 `schema` 类型条目。*
