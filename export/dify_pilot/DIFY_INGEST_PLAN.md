# ultrastable-laser 知识库 → Dify 接入方案

> 编制日期：2026-04-26
> 数据来源：三轮 Claude Code 策划（Qwen3 32B ×2 + DeepSeek V4 Pro 尝试）综合

---

## 一、实际数据

| 指标 | 值 |
|------|-----|
| 论文总数 | 89 篇 YAML |
| 总数据量 | 683 KB（YAML），平均每篇 7.7 KB |
| 最大文件 | 25 KB（numata2004.yaml） |
| 最小文件 | 2.2 KB |
| synthesis 页面 | 8 个，共 62 KB |
| contribution_type | evidence: 62 / breakthrough: 24 / framework: 3 |

**结论**：数据量很小（89 篇一共 683 KB），Dify 导入无压力。

---

## 二、YAML → Dify 映射策略

### Dify 知识库的能力边界
Dify 1.13.3 的知识库是**文档分段 + 向量检索**模式，不支持原生图数据库/三元组。

### 推荐方案：每篇 YAML → 一个 Markdown 文档

将结构化关系**嵌入文档正文**而非依赖 Dify 的原生关系支持。
查询时通过向量检索 + 关系文本共同实现推理。

### Markdown 格式示例
```
# {author}{year} — {标题}

## 元数据
- contribution_type: breakthrough/evidence/framework
- 核心指标: σ_y = xxx

## 实体
- ent.fp_cavity_system — 刚性 F-P 参考腔系统

## 原理
- pri.brownian_thermal_noise_fdt — 布朗热噪声

## 方法
- meth.pdh_locking — PDH 锁频

## 指标
- met.laser_linewidth — 激光线宽: xxx Hz

## 关系
- BOUNDED-BY: ent.xxx → pri.xxx
- COMPETES-WITH: ent.xxx → ent.xxx
- PART-OF: ent.xxx → ent.xxx
- ENABLED-BY: ent.xxx → meth.xxx
```

### Synthesis 页面
直接作为独立文档导入，每个 6-10 KB。作为"综合视图"知识库。

---

## 三、导入流程

### 工作量估算
- 89 篇 YAML → Markdown：脚本自动处理，< 1 分钟
- 导入 Dify：89 个文档 + 8 synthesis = 97 个，预计 < 30 秒
- 分段索引：Dify 自动处理，3-5 分钟

### 分批方案
| 批次 | 内容 | 数量 |
|------|------|------|
| 试点 | breakthrough×1 + evidence×1 + framework×1 | 3 篇 |
| 第一批 | breakthrough 论文 | 24 篇 |
| 第二批 | evidence 论文 | 62 篇 |
| 第三批 | framework + synthesis | 11 篇 |

---

## 四、执行方式

详见 `/data/sci-logic-kb/docs/DIFY_INGEST_WORKFLOW.md`

该文件是写给 Claude Code 的可执行任务序列，按步骤 1-4 顺序推进即可。

---

## 五、风险评估

| 风险 | 影响 | 缓解 |
|------|------|------|
| 关系链在向量检索中丢失 | 中 | 关系嵌入文档正文，通过文本检索弥补 |
| Dify 分段破坏结构 | 中 | 自定义分段策略（按标题分段） |
| 向量召回效果不理想 | 高 | 试点导入后评估，不行调策略 |
