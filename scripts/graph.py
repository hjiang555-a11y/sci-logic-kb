#!/usr/bin/env python3
"""Export the sci-logic-kb knowledge graph and produce diagnostics.

Reads all YAML paper files under topics/*/papers/*.yaml, builds an
in-memory graph of nodes and edges, then exports as JSON or GraphML
and/or prints diagnostic statistics.

Usage examples:
    python scripts/graph.py --format json
    python scripts/graph.py --format graphml --output kb_graph.graphml
    python scripts/graph.py --diagnostics
    python scripts/graph.py --format json --diagnostics --output graph.json
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import yaml


# ── YAML loading ──────────────────────────────────────────────────────

def _iter_yaml_files(repo_path: Path):
    """Yield (topic, filepath) for every papers/*.yaml under topics/."""
    topics_dir = repo_path / "topics"
    if not topics_dir.is_dir():
        return
    for topic_dir in sorted(topics_dir.iterdir()):
        papers_dir = topic_dir / "papers"
        if not papers_dir.is_dir():
            continue
        topic = topic_dir.name
        for yf in sorted(papers_dir.glob("*.yaml")):
            yield topic, yf


def _load_yaml(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except Exception as exc:
        print(f"WARNING: cannot parse {path}: {exc}", file=sys.stderr)
        return None


# ── Section helpers (handle both list and dict styles) ────────────────

_NODE_SECTIONS = ("entities", "principles", "methods", "metrics")
_SECTION_TYPE = {
    "entities": "entity",
    "principles": "principle",
    "methods": "method",
    "metrics": "metric",
}


def _iter_items(section) -> list[dict]:
    """Yield dicts from a section that may be a list or a dict."""
    if section is None:
        return []
    if isinstance(section, list):
        return section
    if isinstance(section, dict):
        return list(section.values()) if section else []
    return []


# ── Graph building ────────────────────────────────────────────────────

def build_graph(repo_path: Path):
    """Return (nodes_dict, edges_list, file_topics).

    nodes_dict: {node_id: {id, type, name, topic, defining_file, ...}}
    edges_list: [{id, source, target, predicate, file, topic}, ...]
    file_topics: {filename: topic}
    """
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    file_topics: dict[str, str] = {}

    for topic, yf in _iter_yaml_files(repo_path):
        data = _load_yaml(yf)
        if not data or not isinstance(data, dict):
            continue
        filename = yf.name
        file_topics[filename] = topic

        # Nodes
        for section_key in _NODE_SECTIONS:
            section = data.get(section_key)
            for item in _iter_items(section):
                if not isinstance(item, dict):
                    continue
                node_id = item.get("id")
                if not node_id:
                    continue
                node_type = _SECTION_TYPE[section_key]
                # First file that defines the node wins as defining_file
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "type": node_type,
                        "name": item.get("name", ""),
                        "topic": topic,
                        "defining_file": filename,
                    }
                    hl = item.get("hierarchy_level")
                    if hl is not None:
                        nodes[node_id]["hierarchy_level"] = hl
                    tier = item.get("tier")
                    if tier is not None:
                        nodes[node_id]["tier"] = tier

        # Edges (relations section)
        relations = data.get("relations")
        for item in _iter_items(relations):
            if not isinstance(item, dict):
                continue
            edge_id = item.get("id", "")
            subject = item.get("subject", "")
            obj = item.get("object", "")
            predicate = item.get("predicate", "")
            if subject and obj and predicate:
                edges.append({
                    "id": edge_id,
                    "source": subject,
                    "target": obj,
                    "predicate": predicate,
                    "file": filename,
                    "topic": topic,
                })

    return nodes, edges, file_topics


# ── JSON export ───────────────────────────────────────────────────────

def export_json(nodes: dict, edges: list, output) -> None:
    topics = sorted({n["topic"] for n in nodes.values()})
    payload = {
        "nodes": list(nodes.values()),
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "topics": topics,
        },
    }
    json.dump(payload, output, ensure_ascii=False, indent=2)
    output.write("\n")


# ── GraphML export ────────────────────────────────────────────────────

def export_graphml(nodes: dict, edges: list, output) -> None:
    ns = "http://graphml.graphstruct.org/xmlns"
    ET.register_namespace("", ns)

    root = ET.Element("graphml", xmlns=ns)

    # Declare data keys
    key_defs = [
        ("d_type", "node", "type", "string"),
        ("d_name", "node", "name", "string"),
        ("d_topic", "node", "topic", "string"),
        ("d_file", "node", "defining_file", "string"),
        ("d_hlevel", "node", "hierarchy_level", "string"),
        ("d_tier", "node", "tier", "string"),
        ("d_predicate", "edge", "predicate", "string"),
        ("d_efile", "edge", "file", "string"),
        ("d_etopic", "edge", "topic", "string"),
    ]
    for kid, kfor, attr_name, attr_type in key_defs:
        ET.SubElement(root, "key", id=kid, attrib={
            "for": kfor, "attr.name": attr_name, "attr.type": attr_type,
        })

    graph = ET.SubElement(root, "graph", id="kb", edgedefault="directed")

    # Nodes
    for nid, ndata in nodes.items():
        n_el = ET.SubElement(graph, "node", id=nid)
        _gml_data(n_el, "d_type", ndata.get("type", ""))
        _gml_data(n_el, "d_name", ndata.get("name", ""))
        _gml_data(n_el, "d_topic", ndata.get("topic", ""))
        _gml_data(n_el, "d_file", ndata.get("defining_file", ""))
        if "hierarchy_level" in ndata:
            _gml_data(n_el, "d_hlevel", str(ndata["hierarchy_level"]))
        if "tier" in ndata:
            _gml_data(n_el, "d_tier", ndata["tier"])

    # Edges
    for i, e in enumerate(edges):
        e_el = ET.SubElement(graph, "edge", id=e.get("id") or f"e{i}",
                             source=e["source"], target=e["target"])
        _gml_data(e_el, "d_predicate", e.get("predicate", ""))
        _gml_data(e_el, "d_efile", e.get("file", ""))
        _gml_data(e_el, "d_etopic", e.get("topic", ""))

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(output, encoding="unicode", xml_declaration=True)
    output.write("\n")


def _gml_data(parent: ET.Element, key: str, text: str) -> None:
    d = ET.SubElement(parent, "data", key=key)
    d.text = text


# ── Graph algorithms (stdlib only, no networkx) ──────────────────────

def _build_adjacency(nodes: dict, edges: list):
    """Return (adj, in_deg, out_deg) dicts over all node IDs."""
    all_ids = set(nodes.keys())
    # Include edge endpoints that might reference nodes from other files
    for e in edges:
        all_ids.add(e["source"])
        all_ids.add(e["target"])

    adj: dict[str, set[str]] = {nid: set() for nid in all_ids}
    in_deg: dict[str, int] = collections.Counter()
    out_deg: dict[str, int] = collections.Counter()

    for e in edges:
        s, t = e["source"], e["target"]
        adj[s].add(t)
        adj[t].add(s)
        out_deg[s] += 1
        in_deg[t] += 1

    return adj, in_deg, out_deg


def _bfs_component(start: str, adj: dict[str, set[str]], visited: set[str]) -> set[str]:
    """BFS from start; return the connected component."""
    queue = collections.deque([start])
    comp: set[str] = {start}
    visited.add(start)
    while queue:
        cur = queue.popleft()
        for nb in adj[cur]:
            if nb not in visited:
                visited.add(nb)
                comp.add(nb)
                queue.append(nb)
    return comp


def _connected_components(adj: dict[str, set[str]]) -> list[set[str]]:
    visited: set[str] = set()
    components: list[set[str]] = []
    for nid in adj:
        if nid not in visited:
            components.append(_bfs_component(nid, adj, visited))
    return components


def _node_topic(nid: str, nodes: dict) -> str | None:
    n = nodes.get(nid)
    return n["topic"] if n else None


# ── Diagnostics ───────────────────────────────────────────────────────

def print_diagnostics(nodes: dict, edges: list) -> None:
    adj, in_deg, out_deg = _build_adjacency(nodes, edges)
    all_ids = set(adj.keys())

    # Total degree
    degree = {nid: in_deg.get(nid, 0) + out_deg.get(nid, 0) for nid in all_ids}

    # ── Hub nodes (top 20 by degree) ──
    hubs = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:20]
    print("=" * 72)
    print("HUB NODES (top 20 by total degree)")
    print("=" * 72)
    print(f"{'Rank':<5} {'ID':<50} {'In':>4} {'Out':>4} {'Tot':>4}")
    print("-" * 72)
    for rank, (nid, tot) in enumerate(hubs, 1):
        name = nodes[nid]["name"][:40] if nid in nodes else "(ref only)"
        print(f"{rank:<5} {nid:<50} {in_deg.get(nid,0):>4} "
              f"{out_deg.get(nid,0):>4} {tot:>4}  {name}")
    print()

    # ── Orphan islands (components of size 1) ──
    components = _connected_components(adj)
    orphans = sorted(nid for comp in components if len(comp) == 1
                     for nid in comp)
    print("=" * 72)
    print(f"ORPHAN ISLANDS ({len(orphans)} isolated nodes)")
    print("=" * 72)
    if orphans:
        for nid in orphans:
            name = nodes[nid]["name"][:50] if nid in nodes else "(ref only)"
            topic = _node_topic(nid, nodes) or "?"
            print(f"  {nid:<50} [{topic}] {name}")
    else:
        print("  (none)")
    print()

    # ── Bridge nodes: nodes connected to multiple topics ──
    # Approximate bridge detection: nodes that connect ≥2 distinct topics
    # through their immediate neighbours (including themselves).
    node_topics_map: dict[str, set[str]] = collections.defaultdict(set)
    for nid in all_ids:
        t = _node_topic(nid, nodes)
        if t:
            node_topics_map[nid].add(t)
    # Propagate neighbour topics
    for e in edges:
        s_topic = _node_topic(e["source"], nodes)
        t_topic = _node_topic(e["target"], nodes)
        if s_topic:
            node_topics_map[e["target"]].add(s_topic)
        if t_topic:
            node_topics_map[e["source"]].add(t_topic)

    bridges = [(nid, ts) for nid, ts in node_topics_map.items()
               if len(ts) >= 2]
    bridges.sort(key=lambda x: (-len(x[1]), x[0]))

    print("=" * 72)
    print(f"BRIDGE NODES ({len(bridges)} nodes connecting multiple topics)")
    print("=" * 72)
    if bridges:
        for nid, ts in bridges[:30]:
            name = nodes[nid]["name"][:40] if nid in nodes else "(ref only)"
            topics_str = ", ".join(sorted(ts))
            print(f"  {nid:<50} [{topics_str}] {name}")
    else:
        print("  (none)")
    print()

    # ── Topic connectivity matrix ──
    topic_set = sorted({n["topic"] for n in nodes.values()})
    cross: dict[tuple[str, str], int] = collections.Counter()
    for e in edges:
        st = _node_topic(e["source"], nodes)
        tt = _node_topic(e["target"], nodes)
        if st and tt and st != tt:
            pair = tuple(sorted([st, tt]))
            cross[pair] += 1

    print("=" * 72)
    print("TOPIC CONNECTIVITY (cross-topic edge counts)")
    print("=" * 72)
    if cross:
        for (t1, t2), cnt in sorted(cross.items(), key=lambda x: -x[1]):
            print(f"  {t1:<30} <-> {t2:<30} {cnt:>4} edges")
    else:
        print("  (no cross-topic edges)")
    print()

    # ── Summary ──
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Total nodes:       {len(nodes)}")
    print(f"  Total edges:       {len(edges)}")
    print(f"  Topics:            {len(topic_set)} ({', '.join(topic_set)})")
    print(f"  Components:        {len(components)}")
    print(f"  Largest component: {max(len(c) for c in components)} nodes")
    print(f"  Orphan nodes:      {len(orphans)}")
    print(f"  Bridge nodes:      {len(bridges)}")
    type_counts = collections.Counter(n["type"] for n in nodes.values())
    for t in ("entity", "principle", "method", "metric"):
        print(f"  {t + 's:':<19} {type_counts.get(t, 0)}")
    pred_counts = collections.Counter(e["predicate"] for e in edges)
    print(f"  Predicate distribution:")
    for p, c in pred_counts.most_common():
        print(f"    {p:<30} {c:>4}")
    print()


# ── CLI ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export sci-logic-kb knowledge graph and produce diagnostics.",
    )
    parser.add_argument(
        "--repo-path", type=Path, default=Path("."),
        help="Root of the sci-logic-kb repository (default: current directory)",
    )
    parser.add_argument(
        "--format", choices=["json", "graphml"], default=None,
        help="Export format (json or graphml)",
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (default: stdout for json, kb_graph.graphml for graphml)",
    )
    parser.add_argument(
        "--diagnostics", action="store_true",
        help="Print diagnostics to stdout",
    )
    args = parser.parse_args()

    if not args.format and not args.diagnostics:
        parser.error("Specify at least one of --format or --diagnostics")

    repo_path = args.repo_path.resolve()
    nodes, edges, _file_topics = build_graph(repo_path)

    if not nodes:
        print("WARNING: no nodes found. Check --repo-path.", file=sys.stderr)

    # Export
    if args.format == "json":
        if args.output:
            with open(args.output, "w", encoding="utf-8") as fh:
                export_json(nodes, edges, fh)
        else:
            export_json(nodes, edges, sys.stdout)

    elif args.format == "graphml":
        out_path = args.output or "kb_graph.graphml"
        with open(out_path, "w", encoding="utf-8") as fh:
            export_graphml(nodes, edges, fh)
        print(f"GraphML written to {out_path}", file=sys.stderr)

    # Diagnostics
    if args.diagnostics:
        print_diagnostics(nodes, edges)


if __name__ == "__main__":
    main()
