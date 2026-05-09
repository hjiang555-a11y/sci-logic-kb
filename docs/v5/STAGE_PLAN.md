# sci-logic-kb 知识库主体建设 — 阶段计划

> 日期: 2026-05-09
> 目标: 完成核心论文的结构化知识提取，建成分专题完整知识库主体
> 当前进度: 309/544 (57%)

---

## 一、范围界定

505 个 PDF 中，属于 6 个专题的约 544 篇（有些论文跨专题）。当前：

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 已入库（有内容） | **309** | 实体/原理/方法/指标/关系已提取 |
| 📋 占位壳（有PDF+专题，缺内容） | **235** | 批量摄入时只生成了元数据，待补结构化内容 |
| ❌ 未拟YAML的PDF | 待筛选 | 需先分类再决定是否入库 |
| **目标总计** | **~544** | 6专题范围内的全部论文 |

---

## 二、分阶段执行计划

### Stage 1: 占位壳填充（235篇，优先）

已有专题归属和 PDF 源文件，只需打开 PDF 提取结构化内容。

**策略**: 按专题从小到大批量并行处理，每个专题用多 agent 同时处理多篇。

| 批次 | 专题 | 数量 | 优先级 | 策略 |
|------|------|------|--------|------|
| 1 | shared | 11 | 🔴高 | 小专题快速收口，agent 并行 |
| 2 | time-frequency-transfer | 35 | 🔴高 | 中等专题，5 agent 并行 |
| 3 | frequency-standards | 29 | 🔴高 | 中等专题，5 agent 并行 |
| 4 | ultrastable-laser | 62 | 🟡中 | 大专题，分两轮，每轮 5 agent |
| 5 | optical-frequency-combs | 98 | 🟡中 | 最大专题，分三轮，每轮 5 agent |

**每篇流程**（CLAUDE.md Step 1-10，简化版）:
1. Agent 读 PDF → 提取标题/作者/年份/DOI（已有元数据可跳过）
2. Agent 识别核心贡献 → 确定 contribution_type
3. Agent 提取 entities, principles, methods, metrics, relations
4. Agent 写入 YAML（更新已有壳文件）
5. 主机验证: `lint.py` + `build_index.py`

**并行方案**: 每轮启动 5 个 `task(category="deep")` sub-agent，每个处理一篇论文。5 篇完成后主机验证，进入下一轮。

**成功标准**: 每批入库后 `lint.py --summary` 0 error，stats 不倒退。

### Stage 2: 剩余 PDF 分类与入库

Stage 1 完成后，评估剩余 PDF:
1. 快速关键词分类（排除明确出范围的）
2. 范围内论文按 Stage 1 相同流程处理
3. 边界模糊的论文标记为 `needs_review`

### Stage 3: 质量收口

- 全库 `lint.py` 0 error
- 补齐 `breakthrough_paths`（USL 专题优先）
- 推理链更新（新论文可能改变因果叙述）
- 重建 INDEX

---

## 三、时间估算

| Stage | 论文数 | 每轮并行 | 轮次 | 预计 |
|-------|--------|---------|------|------|
| Stage 1.1 shared | 11 | 5 agent | 3 轮 | ~30min |
| Stage 1.2 tft | 35 | 5 agent | 7 轮 | ~1h |
| Stage 1.3 fs | 29 | 5 agent | 6 轮 | ~1h |
| Stage 1.4 usl | 62 | 5 agent | 13 轮 | ~2h |
| Stage 1.5 ofc | 98 | 5 agent | 20 轮 | ~3h |
| Stage 2 分类+入库 | ~50-100 | 5 agent | 可变 | ~2-3h |
| Stage 3 收口 | — | — | — | ~1h |
| **总计** | **~470** | | | **~10h** |

---

## 四、Sub-Agent 调用规范

```python
# 每篇论文的 agent 调用
task(
    category="deep",
    load_skills=[],
    prompt="""
[CONTEXT] Processing paper for sci-logic-kb. Topic: {topic}. PDF: {pdf_path}. Existing YAML placeholder: {yaml_path}.

[GOAL] Extract structured knowledge following SCHEMA.md v4.5 YAML template.

[REQUIRED]
1. Read the PDF text
2. Identify: title, authors, year, DOI, core contribution
3. Extract entities (ent.*), principles (pri.*), methods (meth.*), metrics (met.*)
4. Create relations (PART-OF, BOUNDED-BY, ENABLED-BY, CHARACTERIZED-BY, etc.)
5. Determine contribution_type: breakthrough | evidence | framework
6. Write complete YAML to {yaml_path}

[MUST DO]
- Every relation MUST have source.claim from the paper
- Every demonstrated_value MUST have conditions
- Every principle MUST have conditions field
- Follow the EXACT SCHEMA.md v4.5 format
- Use existing node IDs when possible (check topics/{topic}/INDEX.md)

[MUST NOT DO]
- No placeholder/empty arrays
- No relations without source.claim
- No principles without conditions
- No invented data

[EXISTING YAML TO UPDATE]
{current_yaml_content}
""",
    run_in_background=False
)
```

---

## 五、风险与应对

| 风险 | 应对 |
|------|------|
| Agent 产出质量不稳定 | 每轮后运行 lint.py 验证，不合格的返回重做 |
| PDF 文本提取失败（中文/扫描版） | 标记 contribution_type: evidence, reliability: low |
| 5 agent 并行时节点 ID 冲突 | 每轮处理不同论文，避免 ID 重叠 |
| 新节点 ID 与已有节点重复 | 处理前先读 topics/{topic}/INDEX.md 检查已有节点 |
