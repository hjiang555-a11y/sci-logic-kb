# 超稳激光专题整治手册

> **目的**：把阶段 A–D 在 `topics/ultrastable-laser/` 上跑通的整治经验沉淀成可复用手册，供后续专题扩展时参考。
>
> **适用范围**：本手册总结的是"如何整治一个已入库专题"，不是单篇论文摄入流程。单篇论文摄入仍以 [`CONTRIBUTING.md`](../CONTRIBUTING.md) 为准；Schema 以 [`SCHEMA.md`](../SCHEMA.md) 为准。
>
> **当前基线（2026-04-21）**：
> - breakthrough-only reasoning chain closure：**100%**
> - σ_y Linkage（USL breakthrough）：**100%**
> - 全局 cross-file reuse：**8.8%**（仍待提升）
> - ultrastable-laser synthesis：已建 8 页，仍需数值复核

---

## 1. 整治目标

专题整治的目标不是"把所有论文都补得很满"，而是把专题内最关键的**问题 → 解决方案 → 结果**主链显式化，让知识库能够回答三类问题：

1. **当前性能极限在哪？**
2. **为什么卡在这里？**
3. **下一步怎样突破？**

在超稳激光专题中，这条主链被进一步锚定到 **σ_y(τ = 1 s)** 主线指标上。

---

## 2. 整治前提：先定专题主线，再做批量整治

超稳激光专题在 Round 2–3 的核心经验是：**必须先定义专题级主线指标与档位判据，再做 lint / graph / synthesis 整治。**

本专题的专题级规则已固化在：

- [`topics/ultrastable-laser/_meta/scoping_principles.md`](../topics/ultrastable-laser/_meta/scoping_principles.md)
- [`docs/CONTRIBUTION_TIER_RULES.md`](CONTRIBUTION_TIER_RULES.md)

### 2.1 本专题主线

- 唯一主线指标：**σ_y(1 s)**
- 次要指标：线宽、频噪 PSD、相干时间
- 工程指标：加速度灵敏度、漂移、损耗角、精细度、SWaP

### 2.2 整治前必须先回答的 3 个问题

1. 这个专题是否存在单一主线指标？如果没有，是否需要按子域拆分主线？
2. `breakthrough` 的判据是什么？是刷新纪录、提出新原理，还是建立共识？
3. `evidence` 是否允许 orphan / chain-gap？若允许，lint 是否要降级为 INFO？

若这三点未定，后续会产生大量"假缺口"。

---

## 3. 推荐整治流程（按阶段）

### 阶段 A：先完成档位规则落地

目标：把专题内论文统一归入 `breakthrough` / `evidence` / `framework` 三档。

动作：

- 批量检查 `meta.contribution_type`
- 对边界论文做专家裁决
- 默认不确定时归 `evidence`
- 把专题级 override 写入 `_meta/scoping_principles.md`

**验收标准**：

- 所有论文完成档位归一
- 档位规则能解释主要边界案例

### 阶段 B：让 lint / stats 对档位感知

目标：把"真实缺口"与"允许存在的缺口"分开。

动作：

- `reasoning-chain-gap`：仅对 `breakthrough` 保持 WARNING
- `orphan-node`：仅对 `breakthrough` 保持 WARNING
- 为专题主线指标补专题特有检查（本专题为 `σ_y Linkage`）

**验收标准**：

- 真实 WARNING 数显著下降
- evidence/framework 的正常稀疏性不再污染工作队列

### 阶段 C：清零 breakthrough 主链缺口

目标：只处理真正影响专题推理能力的缺口。

优先级：

1. `breakthrough` 论文的 `BOUNDED-BY` 缺 `breakthrough_paths`
2. `breakthrough` 论文的孤立 `pri.*` / `meth.*`
3. 影响主线指标链接的缺口（本专题为 σ_y）

**验收标准**：

- breakthrough-only reasoning chain closure 达标
- breakthrough-tier orphan 清零
- 主题主线指标链接闭环

### 阶段 D：沉淀手册，再扩展其他专题

目标：把专题经验抽象成跨专题可复用方法。

动作：

- 固化整治流程与验收标准
- 识别公共节点抽取候选
- 标注 synthesis 页面待复核项
- 明确下一专题启动前置条件

---

## 4. 实操规则：如何判断一个缺口是否值得修

### 4.1 必修项

以下缺口应优先修复：

- `breakthrough` 论文的 `BOUNDED-BY` 缺 `breakthrough_paths`
- `breakthrough` 论文新增的 `pri.*` / `meth.*` 未挂关系
- 主线指标缺失或未与论文核心贡献建立连接
- synthesis 页面中的主线记录、代表论文、关键数值明显失配

### 4.2 可暂缓项

以下缺口可先保留：

- `evidence` 论文的 orphan / chain-gap
- 仅提供局部工程参数、但不改变主线判断的节点
- 仍未形成跨文件复用价值的单篇指标节点

### 4.3 不要做的事

- 不要为了清零 warning 人为抬升论文档位
- 不要把所有 evidence 节点都强行挂到父节点上
- 不要在主线判据未明确前大量制作 synthesis 页面

---

## 5. 推荐工作顺序

每轮专题整治建议遵循以下顺序：

1. **看规则**：`SCHEMA.md` → 专题 `_meta/scoping_principles.md`
2. **看统计**：`python scripts/stats.py`
3. **看缺口**：`python scripts/lint.py` 与 `python scripts/graph.py --diagnostics`
4. **只修真实缺口**：先 breakthrough，再 evidence
5. **回写综合视图**：必要时更新 `_meta/architecture.md` 与 `synthesis/`
6. **复跑验证**：再次运行 lint / stats

---

## 6. 超稳激光专题的特定经验

### 6.1 σ_y-first 比"线宽-first"更稳定

超稳激光专题最关键的经验是：若不把主线统一到 σ_y(1 s)，则会出现以下问题：

- 世界纪录定义在"线宽 / PSD / 相干时间 / 漂移"之间来回切换
- breakthrough 判据失真
- synthesis 页面无法统一排序
- reasoning chain 无法汇聚到同一坐标轴

因此本专题把：

- **σ_y(1 s)** 设为唯一主线
- 其余刷新默认只记为 `evidence`

### 6.2 breakthrough_paths 应优先记录"可复用方向"

`breakthrough_paths[*].direction` 应优先指向可复用的 `pri.*` / `meth.*`，而不是一次性实体实例。

优先写法：

- 晶体镀层
- 低温机械 Q 增强
- 长腔热噪声稀释
- 光学频率平均
- RAM 主动抑制

避免写法：

- 某个单一实验装置型号
- 某篇论文独有但无法被复用的参数组合

### 6.3 synthesis 页面要围绕主线，不要围绕论文列表

优先的 synthesis 结构应是：

- 限制原理
- 突破路径
- 主线指标改善
- 代表论文

而不是简单按年份堆论文摘要。

---

## 7. 推广到其他专题时的启动条件

建议满足以下条件后再启动下一个专题整治：

- 已有专题的整治规则已文档化
- 新专题已有至少一个 `_meta/scoping_principles.md`
- 专家已确认该专题的主线指标或子域拆分方式
- 已有足够论文规模支撑综合页（通常 ≥ 10 篇，或某子域 ≥ 3 篇）

### 7.1 光学频率梳专题

建议先完成：

- 补齐低成本 lint warning
- 明确至少 2 个子域的主线指标
- 再决定是否做 breakthrough-only 整治

### 7.2 频率标准 / 时间频率传递 / 时间标尺

建议先完成：

- 代表论文摄入达到最小规模
- 激活 Level 1 实体节点
- 明确跨专题接口节点（如超稳激光、频梳、SI 秒定义）

---

## 8. 阶段 D 之后的优先事项

超稳激光专题进入阶段 D 后，建议按以下顺序继续推进：

1. **数值复核**：优先复核 `breakthrough_paths_matrix.md`、`cryogenic_roadmap.md`
2. **公共节点抽取**：提升 cross-file reuse
3. **修补 OPERATIONALIZED-AS**：增强"限制 ↔ 指标 ↔ 实体"的推理桥梁
4. **再启动新专题整治**

---

## 9. 一页式检查清单

- [ ] 专题主线指标已定义
- [ ] `contribution_type` 已批量归一
- [ ] lint / stats 已档位感知
- [ ] breakthrough-tier chain-gap 已清零
- [ ] breakthrough-tier orphan 已清零
- [ ] 主线指标链接已闭环
- [ ] synthesis 页面已建立最小集合
- [ ] 整治经验已沉淀为专题手册
- [ ] 已识别跨文件公共节点候选

---

*本手册是阶段 D 的整治沉淀文档；后续若推广到其他专题，应先复制方法，再按专题特性改写主线判据。*
