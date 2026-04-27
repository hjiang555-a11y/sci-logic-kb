#!/usr/bin/env python3
"""
Graph-aware knowledge base query engine.

Unlike Dify's flat RAG, this script:
1. Parses the YAML knowledge graph (reusing graph.py's build_graph)
2. Does BFS graph traversal to retrieve ALL relevant context for a question
3. Assembles a structured context block with quantitative comparisons
4. Calls any OpenAI-compatible LLM API to answer

Usage:
    python scripts/kb_query.py "超稳激光最高指标是多少？"
    python scripts/kb_query.py --model gpt-4o "光纤干涉仪能否追上FP腔？"
    python scripts/kb_query.py --dry-run "空心光纤的天花板在哪？"

Environment variables:
    OPENAI_API_KEY  - your API key
    OPENAI_BASE_URL - optional, defaults to https://api.openai.com/v1
    LLM_MODEL       - optional, defaults to gpt-4o

Requirements:
    pip install pyyaml openai
"""

from __future__ import annotations

import json
import os
import sys
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import yaml

# ── Graph builder (same logic as graph.py, self-contained) ──

_NODE_SECTIONS = ("entities", "principles", "methods", "metrics")
_SECTION_TYPE = {
    "entities": "entity", "principles": "principle",
    "methods": "method", "metrics": "metric",
}


def _iter_yaml_files(repo_path: Path):
    topics_dir = repo_path / "topics"
    if not topics_dir.is_dir():
        return
    for topic_dir in sorted(topics_dir.iterdir()):
        papers_dir = topic_dir / "papers"
        if not papers_dir.is_dir():
            continue
        for yf in sorted(papers_dir.glob("*.yaml")):
            yield topic_dir.name, yf


def _iter_items(section):
    if section is None:
        return []
    if isinstance(section, list):
        return section
    if isinstance(section, dict):
        return list(section.values()) if section else []
    return []


def build_graph(repo_path: Path):
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    papers: dict[str, dict] = {}

    for topic, yf in _iter_yaml_files(repo_path):
        try:
            with open(yf, encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue

        filename = yf.name
        papers[filename] = {"data": data, "topic": topic, "path": str(yf)}

        for section_key in _NODE_SECTIONS:
            for item in _iter_items(data.get(section_key)):
                if not isinstance(item, dict):
                    continue
                node_id = item.get("id")
                if not node_id:
                    continue
                node_type = _SECTION_TYPE[section_key]
                if node_id not in nodes:
                    # Attach paper metadata for better search
                    meta = data.get("meta", {}) or {}
                    nodes[node_id] = {
                        "id": node_id,
                        "type": node_type,
                        "name": item.get("name", ""),
                        "topic": topic,
                        "defining_file": filename,
                        "full_node": item,
                        "paper_title": meta.get("title", ""),
                        "paper_year": meta.get("year", ""),
                        "paper_contribution": meta.get("contribution_type", ""),
                        "paper_first_author": meta.get("first_author", ""),
                        "paper_note": meta.get("note", ""),
                    }

        for item in _iter_items(data.get("relations")):
            if not isinstance(item, dict):
                continue
            subject = item.get("subject", "")
            obj = item.get("object", "")
            predicate = item.get("predicate", "")
            if subject and obj and predicate:
                edges.append({
                    "id": item.get("id", ""),
                    "source": subject, "target": obj,
                    "predicate": predicate,
                    "file": filename, "topic": topic,
                    "full_relation": item,
                })

    return nodes, edges, papers


# ── Keyword-based entry node selection ──

# Semantic keyword mapping: question keywords → node ID patterns
TOPIC_KEYWORDS = {
    "超稳激光": ["ultrastable-laser"],
    "光梳": ["optical-frequency-combs"],
    "频率标准": ["frequency-standards"],
    "时频传递": ["time-frequency-transfer"],
    "光纤": ["fiber", "FDL", "hollow_core"],
    "FP腔": ["fp_cavity", "brownian_thermal"],
    "SHB": ["shb", "spectral_hole"],
    "布里渊": ["brillouin", "sbs"],
    "超辐射": ["superradiant"],
    "原子干涉": ["ramsey_borde", "atom_interferometer"],
    "晶体镀层": ["crystalline_coating", "algaas", "coating_loss"],
    "低温": ["cryogenic", "silicon_cte", "17k", "124k", "4k"],
    "热噪声": ["thermal_noise", "brownian"],
    "振动": ["vibration", "acceleration_sensitivity"],
    "RAM": ["ram_pdh"],
    "线宽": ["linewidth"],
    "稳定度": ["instability", "allan", "sigma_y"],
}


def _score_node_for_question(nid: str, node: dict, question: str) -> float:
    """Score a node against a question. Uses keyword overlap + semantic mapping."""
    # Build rich search text: node fields + paper metadata
    search_text = (
        (node.get("name", "") + " " + nid + " " +
         node.get("paper_title", "") + " " +
         str(node.get("paper_note", "")) + " " +
         node.get("paper_first_author", ""))
    ).lower()
    keywords = re.findall(r"[一-鿿]+|[a-zA-Z0-9_]+", question.lower())

    score = 0.0
    for kw in keywords:
        if len(kw) >= 2 and kw in search_text:
            score += 1.2
        if len(kw) >= 3 and kw in nid:
            score += 3.0  # ID match is strong signal
        # Paper title match
        if len(kw) >= 2 and kw in node.get("paper_title", "").lower():
            score += 1.0

    # Semantic topic mapping
    for cn_kw, id_pats in TOPIC_KEYWORDS.items():
        if cn_kw in question:
            for pat in id_pats:
                if pat in nid.lower() or pat in node.get("name", "").lower():
                    score += 2.0

    # "最高/纪录/best/record/SOTA" query → boost breakthru + world-record nodes
    record_pats = ["最高", "纪录", "最佳", "记录", "best", "record", "SOTA", "sota", "极限", "世界"]
    is_record_q = any(p in question for p in record_pats)
    if is_record_q:
        contrib = node.get("paper_contribution", "")
        if contrib == "breakthrough":
            score += 5.0
        note = node.get("paper_note", "")
        if note and ("世界纪录" in note or "world record" in note.lower() or
                     "当前" in note or "里程碑" in note):
            score += 8.0
        # Boost metrics that are role=primary (σ_y主线)
        fn = node.get("full_node", {})
        if fn.get("role") == "primary":
            score += 4.0
        # Boost 2026 papers (most recent)
        year = node.get("paper_year", "")
        if str(year) == "2026":
            score += 3.0

    # Node type boost
    boosts = {"metric": 2.5, "principle": 1.5, "entity": 1.0, "method": 0.5}
    score += boosts.get(node.get("type", ""))

    # Topic boost
    topic = node.get("topic", "")
    laser_kw = ["激光", "超稳", "laser", "ultrastable"]
    if any(k in question.lower() for k in laser_kw) and topic == "ultrastable-laser":
        score *= 1.8

    return score


def find_entry_nodes(nodes: dict, question: str, top_k: int = 15) -> list[str]:
    scored = []
    for nid, node in nodes.items():
        s = _score_node_for_question(nid, node, question)
        if s > 0:
            scored.append((s, nid))
    scored.sort(key=lambda x: -x[0])
    return [nid for _, nid in scored[:top_k]]


# ── Graph traversal ──

def _build_adjacency(edges: list[dict]) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        adj[e["source"]].add(e["target"])
        adj[e["target"]].add(e["source"])
    return adj


def bfs_context(
    seed_ids: list[str],
    nodes: dict,
    edges: list[dict],
    max_depth: int = 2,
    max_nodes: int = 60,
) -> dict[str, dict]:
    adj = _build_adjacency(edges)
    edge_index: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        edge_index[e["source"]].append(e)
        edge_index[e["target"]].append(e)

    visited: set[str] = set()
    queue: deque = deque()
    for nid in seed_ids:
        if nid in nodes:
            queue.append((nid, 0))
            visited.add(nid)

    collected: dict[str, dict] = {}

    while queue and len(collected) < max_nodes:
        current, depth = queue.popleft()
        if current in nodes:
            collected[current] = nodes[current]

        if depth >= max_depth:
            continue

        neighbors = adj.get(current, set())
        prioritized = []
        for nb in neighbors:
            if nb in visited:
                continue
            priority = 0
            for e in edge_index.get(current, []):
                other = e["target"] if e["source"] == current else e["source"]
                if other == nb:
                    pred = e.get("predicate", "")
                    if pred in ("BOUNDED-BY", "CHARACTERIZED-BY"):
                        priority = 3
                    elif pred in ("COMPETES-WITH", "ENABLED-BY"):
                        priority = 2
                    elif pred in ("PART-OF", "DERIVED-FROM"):
                        priority = 1
            prioritized.append((priority, nb))

        prioritized.sort(key=lambda x: -x[0])
        for _, nb in prioritized:
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, depth + 1))

    return collected


# ── Context assembly ──

def _fmt_metric(m: dict) -> str:
    fn = m.get("full_node", {})
    lines = [f"### [指标] {m.get('name', m['id'])}"]
    lines.append(f"ID: `{m['id']}` | 专题: {m.get('topic','?')} | 论文: {m.get('defining_file','?')}")

    dv = fn.get("demonstrated_value", {})
    if isinstance(dv, dict):
        val = dv.get("value", "?")
        cond = dv.get("conditions", "")
        lines.append(f"**实测值**: {val}")
        if cond:
            lines.append(f"条件: {cond}")

    tf = fn.get("theoretical_floor", {})
    if isinstance(tf, dict):
        lines.append(f"**理论下限**: {tf.get('value','?')}")
        gap = tf.get("gap_note", "")
        if gap:
            lines.append(f"差距注释: {gap}")

    comp = fn.get("comparison", {})
    if isinstance(comp, dict):
        for k, v in comp.items():
            if v:
                lines.append(f"- 对比({k}): {v}")

    desc = fn.get("description", "")
    if desc:
        lines.append(f"\n{str(desc)[:300]}")
    return "\n".join(lines)


def _fmt_principle(p: dict) -> str:
    fn = p.get("full_node", {})
    lines = [f"### [原理] {p.get('name', p['id'])}"]
    lines.append(f"ID: `{p['id']}` | tier: {fn.get('tier','?')} | 专题: {p.get('topic','?')}")
    if fn.get("formula"):
        lines.append(f"公式: {fn['formula']}")
    ki = fn.get("key_insight", "")
    if ki:
        lines.append(f"洞见: {str(ki)[:250]}")
    return "\n".join(lines)


def _fmt_entity(e: dict) -> str:
    fn = e.get("full_node", {})
    lines = [f"### [实体] {e.get('name', e['id'])}"]
    lines.append(f"ID: `{e['id']}` | 专题: {e.get('topic','?')}")
    params = fn.get("key_parameters", {})
    if isinstance(params, dict):
        for k, v in params.items():
            lines.append(f"- {k}: {v}")
    return "\n".join(lines)


def _fmt_method(m: dict) -> str:
    fn = m.get("full_node", {})
    lines = [f"### [方法] {m.get('name', m['id'])}"]
    lines.append(f"ID: `{m['id']}` | 专题: {m.get('topic','?')}")
    adv = fn.get("advantages", [])
    if adv:
        lines.append("优势: " + "; ".join(str(a) for a in adv[:3]))
    return "\n".join(lines)


def assemble_context(collected: dict, edges: list, question: str) -> str:
    parts = [f"# 知识库检索上下文\n问题: {question}\n"]

    metrics, principles, entities, methods = [], [], [], []
    for nid, node in collected.items():
        t = node.get("type", "")
        (metrics if t == "metric" else principles if t == "principle"
         else entities if t == "entity" else methods).append(node)

    if metrics:
        parts.append("## 📊 指标\n")
        for m in metrics:
            parts.append(_fmt_metric(m) + "\n")

    if principles:
        parts.append("## 🔬 原理\n")
        for p in principles[:10]:
            parts.append(_fmt_principle(p) + "\n")

    if entities:
        parts.append("## 🏗️ 实体\n")
        for e in entities[:8]:
            parts.append(_fmt_entity(e) + "\n")

    if methods:
        parts.append("## 🔧 方法\n")
        for m in methods[:5]:
            parts.append(_fmt_method(m) + "\n")

    # Key relations between collected nodes
    nids = set(collected.keys())
    rels = [e for e in edges if e["source"] in nids and e["target"] in nids
            and e.get("predicate") in ("BOUNDED-BY","COMPETES-WITH","CHARACTERIZED-BY","ENABLED-BY")]
    if rels:
        parts.append("## 🔗 关键关系\n")
        seen = set()
        for e in rels[:20]:
            k = (e["source"], e["target"], e["predicate"])
            if k not in seen:
                seen.add(k)
                parts.append(f"- `{e['source']}` --[{e['predicate']}]--> `{e['target']}`")

    return "\n".join(parts)


# ── LLM ──

SYSTEM_PROMPT = """你是科学知识库问答助手。你的回答必须基于下面提供的"知识库检索上下文"。
知识库包含科学论文的结构化数据：指标、原理、实体、方法及它们之间的关系。

规则:
1. 优先用数值数据支撑回答，引用实测值和论文来源
2. 如果上下文中有对比数据，给出定量对比
3. 区分"已验证的实测值"和"理论预期"
4. 数据不充分时，明确说"知识库中未找到该数据"而不是猜测
5. 回答用中文，保持简洁，关键数字加粗
"""


def query_llm(context: str, question: str, model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        return "[错误: 请 pip install openai]"

    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        return "[错误: 请设置 OPENAI_API_KEY 环境变量]"

    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n\n---\n请回答问题: {question}"},
        ],
        temperature=0.1,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# ── CLI ──

def main():
    import argparse
    parser = argparse.ArgumentParser(description="KB Graph Query")
    parser.add_argument("question", nargs="+", help="问题")
    parser.add_argument("--model", default=os.environ.get("LLM_MODEL","gpt-4o"))
    parser.add_argument("--repo-path", default="/data/sci-logic-kb")
    parser.add_argument("--dry-run", action="store_true", help="只显示检索结果，不调LLM")
    parser.add_argument("--max-nodes", type=int, default=60)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    question = " ".join(args.question)
    repo_path = Path(args.repo_path)

    print(f"加载知识图谱: {repo_path}", file=sys.stderr)
    nodes, edges, papers = build_graph(repo_path)
    print(f"节点: {len(nodes)}  边: {len(edges)}  论文: {len(papers)}", file=sys.stderr)

    seeds = find_entry_nodes(nodes, question)
    if not seeds:
        print("未找到匹配节点", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        for sid in seeds:
            n = nodes.get(sid, {})
            print(f"  [{n.get('type','?')}] {sid}  {n.get('name','')[:60]}", file=sys.stderr)

    collected = bfs_context(seeds, nodes, edges, args.depth, args.max_nodes)
    context = assemble_context(collected, edges, question)
    print(f"检索 {len(collected)} 个节点, ~{len(context)//3} tokens", file=sys.stderr)

    if args.dry_run:
        print("\n" + "="*70)
        print(context)
        print("="*70)
        print("\n[--dry-run: 未调用 LLM]")
        return

    print(f"调用 {args.model}...", file=sys.stderr)
    answer = query_llm(context, question, args.model)
    print("\n" + answer)


if __name__ == "__main__":
    main()
