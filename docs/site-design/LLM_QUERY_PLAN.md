# sci-logic-kb LLM 查询架构方案

> 原则：LLM 永远用知识库数据回答，不依赖自身知识。杜绝幻觉。

---

## 一、架构：Context-First Query

```
用户问题
    │
    ▼
关键词检索 ──→ 结构化数据 (JSON)
    │              │
    │         papers / metrics / chains / consensus
    │              │
    ▼              ▼
LLM 组装 ──→ 打包为 context ──→ LLM 仅基于 context 回答
    │
    ▼
结构化答案 + 引用来源 (paper, chain, consensus)
```

**LLM 只做两件事**：
1. 理解用户意图 → 转换检索关键词
2. 基于检索结果 → 用自然语言回答

**LLM 不做的事**：凭空回答、编造数值、推测物理机制。

---

## 二、数据层

已有结构化 JSON（`docs/site/api/`）：

| 文件 | 内容 | 大小 |
|------|------|------|
| `structured_data.json` | 全量：papers, metrics, principles, chains, consensus | ~500KB |
| `search_index.json` | 轻量检索索引 | ~135KB |

每条数据自带引用：`topic, paper, year, author, claim`。

---

## 三、查询 Pipeline

```python
def query(question: str) -> Answer:
    # Step 1: 关键词提取 (LLM 或 rule-based)
    keywords = extract_keywords(question)
    
    # Step 2: 结构化检索
    papers  = search_papers(keywords)
    metrics = search_metrics(keywords)
    chains  = search_chains(keywords)
    consensus = search_consensus(keywords)
    
    # Step 3: 组装 context (限制 token)
    context = build_context(papers[:3], metrics[:5], chains[:2], consensus[:1])
    
    # Step 4: LLM 回答
    answer = llm.generate(
        system="你是时间频率计量知识库助手。只基于提供的 context 回答。不知道就说不知道。",
        context=context,
        question=question
    )
    
    # Step 5: 附加引用
    return Answer(text=answer, sources=[...])
```

---

## 四、接口形态

### 4.1 命令行（快速验证）

```bash
python scripts/query.py "FP 腔 σ_y(1s) 的当前世界纪录是多少？"
```

输出：
```
答案: FP 腔稳频激光的 σ_y(1s) 当前世界纪录是 mod σ_y = 2.5×10⁻¹⁷，
由 Lee 2026 实现（17K Si 腔 + AlGaAs 晶体镀层，JILA/PTB）。
理论极限约 10⁻¹⁸，剩余差距约 8×。

来源:
  - consensus/sigma_y_1s_fp_cavity (共识报告, 12 个数据点)
  - lee2026.yaml (Lee 2026, breakthrough)
  - logic/chains/sigma_y_cavity (推理链)
```

### 4.2 HTTP API（后续接网页）

```bash
curl -X POST http://localhost:8091/query \
  -d '{"question": "What limits fiber link instability?"}'
```

### 4.3 网页嵌入（最终形态）

Query 页面内嵌一个真实的对话组件，每个回答带引用。

---

## 五、分步实施

| 步骤 | 内容 | 产出 |
|------|------|------|
| **S1** | `scripts/query.py` — CLI 查询脚本，LLM 后端可插拔 | 命令行可查 |
| **S2** | 验证答案质量（10 个典型问题，人工判断） | 质量报告 |
| **S3** | HTTP API（FastAPI） | 网页可调 |
| **S4** | 网页对话组件 | 最终形态 |

---

## 六、LLM 后端选择

| 后端 | 部署 | 费用 | 适用 |
|------|------|------|------|
| Dify + OpenAI API | 已有 Docker | API 按量 | 质量最好，需要 key |
| Ollama + qwen2.5 | 本地安装 | 免费 | 完全本地，离线可用 |
| DeepSeek API | 无需部署 | 极低 | 中文最优，性价比最高 |

**推荐**：S1 先用 DeepSeek API（便宜、中文好、联网可用），后续可切换到本地 Ollama。
