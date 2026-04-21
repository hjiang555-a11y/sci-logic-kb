#!/usr/bin/env python3
"""Comprehensive statistics for the sci-logic-kb knowledge base.

Computes 6 key "reasoning readiness" metrics plus standard inventory counts.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


# σ_y primary-metric heuristics (ultrastable-laser, Round 3, scoping_principles.md v2)
PRIMARY_METRIC_PATTERNS = (
    "fractional_freq_instability",
    "fractional_frequency_instability",
    "allan_deviation",
    "mod_sigma_y",
    "mod_σ_y",
    "oadev",
    "hadamard",
)


def _is_primary_sigma_y_id(node_id: str) -> bool:
    """Return True if a metric ID matches the σ_y primary-line heuristic."""
    if not node_id:
        return False
    lid = node_id.lower()
    return lid.startswith("met.") and any(pat in lid for pat in PRIMARY_METRIC_PATTERNS)


def _is_primary_sigma_y_metric(metric: dict) -> bool:
    """Return True if a metric node is a σ_y primary-line metric
    (explicit role: primary, or ID/name heuristic)."""
    role = metric.get("role")
    if isinstance(role, str) and role.strip().lower() == "primary":
        return True
    mid = (metric.get("id") or "").lower()
    name = (metric.get("name") or "").lower()
    haystack = f"{mid} {name}"
    return any(pat in haystack for pat in PRIMARY_METRIC_PATTERNS)


# ── helpers ──────────────────────────────────────────────────────────────

def _as_list(section):
    """Normalize a YAML section to a list of dicts (handles list / dict / None)."""
    if section is None:
        return []
    if isinstance(section, list):
        return [item for item in section if isinstance(item, dict)]
    if isinstance(section, dict):
        return list(section.values()) if section else []
    return []


def _count_items(node, field_name):
    """Count items in a list-valued field, tolerating missing / non-list values."""
    val = node.get(field_name)
    if isinstance(val, list):
        return len(val)
    return 0


# ── YAML loading ────────────────────────────────────────────────────────

def load_yaml_files(repo: Path):
    """Yield (topic, filepath, parsed_doc) for every papers/*.yaml file."""
    topics_dir = repo / "topics"
    if not topics_dir.is_dir():
        return
    for topic_dir in sorted(topics_dir.iterdir()):
        if not topic_dir.is_dir():
            continue
        papers_dir = topic_dir / "papers"
        if not papers_dir.is_dir():
            continue
        topic = topic_dir.name
        for yf in sorted(papers_dir.glob("*.yaml")):
            try:
                with open(yf, encoding="utf-8") as fh:
                    doc = yaml.safe_load(fh)
            except Exception as exc:
                print(f"WARNING: failed to parse {yf}: {exc}", file=sys.stderr)
                continue
            if not isinstance(doc, dict):
                continue
            yield topic, yf, doc


# ── core analysis ───────────────────────────────────────────────────────

def analyse(repo: Path):
    """Return a dict with all computed statistics."""

    # per-topic bookkeeping
    papers_per_topic = Counter()
    nodes_per_type = Counter()  # prefix → count
    relations_per_predicate = Counter()
    topic_paper_files = defaultdict(list)

    # node ID → set of files that reference it
    node_files = defaultdict(set)

    # reasoning-readiness accumulators
    bounded_by_total = 0
    bounded_by_with_bp = 0
    relations_total = 0
    relations_with_claim = 0
    principle_total = 0
    principle_with_cond = 0
    contested_total = 0
    open_q_total = 0

    # σ_y-linkage (ultrastable-laser only): do breakthrough papers actually
    # carry a σ_y primary-line metric? Round-3 scoping principle v2.
    usl_breakthrough_total = 0
    usl_breakthrough_with_sy = 0
    usl_breakthrough_missing_sy: list[str] = []

    for topic, filepath, doc in load_yaml_files(repo):
        fname = filepath.name
        papers_per_topic[topic] += 1
        topic_paper_files[topic].append(fname)

        meta = doc.get("meta") if isinstance(doc.get("meta"), dict) else {}
        contrib = str(meta.get("contribution_type", "")).strip().lower()
        is_usl_breakthrough = (topic == "ultrastable-laser" and contrib == "breakthrough")
        if is_usl_breakthrough:
            usl_breakthrough_total += 1
            has_primary_sy = False
            for met in _as_list(doc.get("metrics")):
                if _is_primary_sigma_y_metric(met):
                    has_primary_sy = True
                    break
            if not has_primary_sy:
                for rel in _as_list(doc.get("relations")):
                    for field in ("subject", "object"):
                        if _is_primary_sigma_y_id(rel.get(field, "") or ""):
                            has_primary_sy = True
                            break
                    if has_primary_sy:
                        break
            if has_primary_sy:
                usl_breakthrough_with_sy += 1
            else:
                usl_breakthrough_missing_sy.append(fname)

        # ── nodes ──
        for section_key, prefix in [
            ("entities", "ent"),
            ("principles", "pri"),
            ("methods", "meth"),
            ("metrics", "met"),
        ]:
            items = _as_list(doc.get(section_key))
            for node in items:
                nid = node.get("id", "")
                if nid:
                    nodes_per_type[prefix] += 1
                    node_files[nid].add(fname)

                # condition completeness (principles only)
                if prefix == "pri":
                    principle_total += 1
                    has_cond = any(
                        node.get(f) not in (None, "", [])
                        for f in ("conditions", "preconditions", "invalidated_when")
                    )
                    if has_cond:
                        principle_with_cond += 1

                # contradiction visibility (any node type)
                contested_total += _count_items(node, "contested_claims")
                open_q_total += _count_items(node, "open_questions")

        # ── relations ──
        rels = _as_list(doc.get("relations"))
        for rel in rels:
            predicate = rel.get("predicate", "UNKNOWN")
            relations_per_predicate[predicate] += 1
            relations_total += 1

            # track node IDs referenced in relations
            for ref_field in ("subject", "object"):
                ref_id = rel.get(ref_field, "")
                if ref_id:
                    node_files[ref_id].add(fname)

            # source claim coverage
            src = rel.get("source")
            if isinstance(src, dict) and src.get("claim"):
                relations_with_claim += 1

            # reasoning chain closure (BOUNDED-BY with breakthrough_paths)
            if predicate == "BOUNDED-BY":
                bounded_by_total += 1
                bp = rel.get("breakthrough_paths")
                if isinstance(bp, list) and len(bp) > 0:
                    bounded_by_with_bp += 1

    # ── cross-file reuse ──
    total_unique_ids = len(node_files)
    reused_ids = sum(1 for fset in node_files.values() if len(fset) >= 2)

    # ── synthesis coverage ──
    synthesis_per_topic = {}
    topics_dir = repo / "topics"
    topics_with_papers = set(papers_per_topic.keys())
    if topics_dir.is_dir():
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            syn_dir = topic_dir / "synthesis"
            md_files = sorted(syn_dir.glob("*.md")) if syn_dir.is_dir() else []
            synthesis_per_topic[topic_dir.name] = [f.name for f in md_files]

    topics_with_synthesis = sum(
        1 for t in topics_with_papers if len(synthesis_per_topic.get(t, [])) > 0
    )

    # ── build result dict ──
    def _rate(num, den):
        return round(num / den, 4) if den else 0.0

    return {
        "reasoning_readiness": {
            "reasoning_chain_closure": {
                "bounded_by_total": bounded_by_total,
                "bounded_by_with_breakthrough_paths": bounded_by_with_bp,
                "rate": _rate(bounded_by_with_bp, bounded_by_total),
                "target": 0.70,
            },
            "evidence_coverage": {
                "relations_total": relations_total,
                "relations_with_source_claim": relations_with_claim,
                "rate": _rate(relations_with_claim, relations_total),
                "target": 0.90,
            },
            "condition_completeness": {
                "principle_total": principle_total,
                "principle_with_conditions": principle_with_cond,
                "rate": _rate(principle_with_cond, principle_total),
                "target": 0.80,
            },
            "cross_file_reuse": {
                "total_unique_ids": total_unique_ids,
                "ids_in_2_plus_files": reused_ids,
                "rate": _rate(reused_ids, total_unique_ids),
            },
            "synthesis_coverage": {
                "topics_with_papers": len(topics_with_papers),
                "topics_with_synthesis": topics_with_synthesis,
                "details": {
                    t: synthesis_per_topic.get(t, []) for t in sorted(topics_with_papers)
                },
            },
            "contradiction_visibility": {
                "contested_claims_total": contested_total,
                "open_questions_total": open_q_total,
                "combined_total": contested_total + open_q_total,
            },
            "sigma_y_linkage": {
                "scope": "ultrastable-laser · contribution_type == breakthrough",
                "breakthrough_papers": usl_breakthrough_total,
                "breakthrough_with_sigma_y": usl_breakthrough_with_sy,
                "rate": _rate(usl_breakthrough_with_sy, usl_breakthrough_total),
                "target": 1.00,
                "missing_files": sorted(usl_breakthrough_missing_sy),
            },
        },
        "inventory": {
            "papers_per_topic": dict(papers_per_topic.most_common()),
            "total_papers": sum(papers_per_topic.values()),
            "nodes_per_type": dict(sorted(nodes_per_type.items())),
            "total_nodes": sum(nodes_per_type.values()),
            "relations_per_predicate": dict(
                sorted(relations_per_predicate.items(), key=lambda x: -x[1])
            ),
            "total_relations": relations_total,
        },
    }


# ── output formatters ──────────────────────────────────────────────────

def _pass_fail(rate, target):
    return "✅ PASS" if rate >= target else "❌ FAIL"


def _pct(rate):
    return f"{rate * 100:.1f}%"


def format_text(stats):
    rr = stats["reasoning_readiness"]
    inv = stats["inventory"]
    lines = []

    lines.append("=" * 62)
    lines.append("  sci-logic-kb  ·  Knowledge Base Statistics")
    lines.append("=" * 62)

    # ── reasoning readiness ──
    lines.append("")
    lines.append("── Reasoning Readiness Metrics ──")
    lines.append("")

    rc = rr["reasoning_chain_closure"]
    lines.append(
        f"  1. Reasoning Chain Closure  {_pct(rc['rate']):>7}  "
        f"(target ≥{_pct(rc['target'])})  "
        f"{_pass_fail(rc['rate'], rc['target'])}  "
        f"[{rc['bounded_by_with_breakthrough_paths']}/{rc['bounded_by_total']} BOUNDED-BY]"
    )

    ec = rr["evidence_coverage"]
    lines.append(
        f"  2. Evidence Coverage        {_pct(ec['rate']):>7}  "
        f"(target ≥{_pct(ec['target'])})  "
        f"{_pass_fail(ec['rate'], ec['target'])}  "
        f"[{ec['relations_with_source_claim']}/{ec['relations_total']} relations]"
    )

    cc = rr["condition_completeness"]
    lines.append(
        f"  3. Condition Completeness   {_pct(cc['rate']):>7}  "
        f"(target ≥{_pct(cc['target'])})  "
        f"{_pass_fail(cc['rate'], cc['target'])}  "
        f"[{cc['principle_with_conditions']}/{cc['principle_total']} principles]"
    )

    cr = rr["cross_file_reuse"]
    lines.append(
        f"  4. Cross-file Reuse         {_pct(cr['rate']):>7}  "
        f"(higher is better)          "
        f"[{cr['ids_in_2_plus_files']}/{cr['total_unique_ids']} IDs]"
    )

    sc = rr["synthesis_coverage"]
    lines.append(
        f"  5. Synthesis Coverage        "
        f"{sc['topics_with_synthesis']}/{sc['topics_with_papers']} topics  "
        f"{'✅ PASS' if sc['topics_with_synthesis'] == sc['topics_with_papers'] else '⚠️  INCOMPLETE'}"
    )
    for t, files in sorted(sc["details"].items()):
        mark = "✓" if files else "✗"
        detail = ", ".join(files) if files else "(none)"
        lines.append(f"       {mark} {t}: {detail}")

    cv = rr["contradiction_visibility"]
    lines.append(
        f"  6. Contradiction Visibility  "
        f"{cv['combined_total']} entries  "
        f"(contested: {cv['contested_claims_total']}, open_q: {cv['open_questions_total']})"
    )

    sy = rr["sigma_y_linkage"]
    if sy["breakthrough_papers"] > 0:
        lines.append(
            f"  7. σ_y Linkage (USL)      {_pct(sy['rate']):>7}  "
            f"(target ={_pct(sy['target'])})  "
            f"{_pass_fail(sy['rate'], sy['target'])}  "
            f"[{sy['breakthrough_with_sigma_y']}/{sy['breakthrough_papers']} USL breakthroughs]"
        )
        if sy["missing_files"]:
            lines.append(f"       ⚠  missing σ_y primary metric: {', '.join(sy['missing_files'][:5])}"
                         + (f" ... (+{len(sy['missing_files']) - 5} more)" if len(sy['missing_files']) > 5 else ""))
    else:
        lines.append("  7. σ_y Linkage (USL)      n/a    (no ultrastable-laser breakthrough papers)")

    # ── inventory ──
    lines.append("")
    lines.append("── Inventory ──")
    lines.append("")
    lines.append(f"  Total papers: {inv['total_papers']}")
    for t, c in inv["papers_per_topic"].items():
        lines.append(f"    {t}: {c}")

    lines.append(f"  Total nodes:  {inv['total_nodes']}")
    for prefix, c in inv["nodes_per_type"].items():
        lines.append(f"    {prefix}.*: {c}")

    lines.append(f"  Total relations: {inv['total_relations']}")
    for pred, c in inv["relations_per_predicate"].items():
        lines.append(f"    {pred}: {c}")

    lines.append("")
    return "\n".join(lines)


def format_markdown(stats):
    rr = stats["reasoning_readiness"]
    inv = stats["inventory"]
    lines = []

    lines.append("# sci-logic-kb — Knowledge Base Statistics")
    lines.append("")

    lines.append("## Reasoning Readiness Metrics")
    lines.append("")
    lines.append("| # | Metric | Value | Target | Status | Detail |")
    lines.append("|---|--------|-------|--------|--------|--------|")

    rc = rr["reasoning_chain_closure"]
    lines.append(
        f"| 1 | Reasoning Chain Closure | {_pct(rc['rate'])} | ≥{_pct(rc['target'])} "
        f"| {_pass_fail(rc['rate'], rc['target'])} "
        f"| {rc['bounded_by_with_breakthrough_paths']}/{rc['bounded_by_total']} BOUNDED-BY |"
    )

    ec = rr["evidence_coverage"]
    lines.append(
        f"| 2 | Evidence Coverage | {_pct(ec['rate'])} | ≥{_pct(ec['target'])} "
        f"| {_pass_fail(ec['rate'], ec['target'])} "
        f"| {ec['relations_with_source_claim']}/{ec['relations_total']} relations |"
    )

    cc = rr["condition_completeness"]
    lines.append(
        f"| 3 | Condition Completeness | {_pct(cc['rate'])} | ≥{_pct(cc['target'])} "
        f"| {_pass_fail(cc['rate'], cc['target'])} "
        f"| {cc['principle_with_conditions']}/{cc['principle_total']} principles |"
    )

    cr = rr["cross_file_reuse"]
    lines.append(
        f"| 4 | Cross-file Reuse | {_pct(cr['rate'])} | higher=better "
        f"| — "
        f"| {cr['ids_in_2_plus_files']}/{cr['total_unique_ids']} IDs |"
    )

    sc = rr["synthesis_coverage"]
    sc_status = (
        "✅ PASS"
        if sc["topics_with_synthesis"] == sc["topics_with_papers"]
        else "⚠️ INCOMPLETE"
    )
    lines.append(
        f"| 5 | Synthesis Coverage | "
        f"{sc['topics_with_synthesis']}/{sc['topics_with_papers']} | all topics | {sc_status} | see below |"
    )

    cv = rr["contradiction_visibility"]
    lines.append(
        f"| 6 | Contradiction Visibility | {cv['combined_total']} | more=better "
        f"| — "
        f"| contested: {cv['contested_claims_total']}, open_q: {cv['open_questions_total']} |"
    )

    sy = rr["sigma_y_linkage"]
    if sy["breakthrough_papers"] > 0:
        sy_status = _pass_fail(sy["rate"], sy["target"])
        lines.append(
            f"| 7 | σ_y Linkage (USL breakthrough) | {_pct(sy['rate'])} | ={_pct(sy['target'])} "
            f"| {sy_status} "
            f"| {sy['breakthrough_with_sigma_y']}/{sy['breakthrough_papers']} USL breakthroughs |"
        )
    else:
        lines.append(
            f"| 7 | σ_y Linkage (USL breakthrough) | n/a | ={_pct(sy['target'])} | — "
            "| no USL breakthrough papers |"
        )

    lines.append("")
    lines.append("### Synthesis details")
    lines.append("")
    for t, files in sorted(sc["details"].items()):
        mark = "✅" if files else "❌"
        detail = ", ".join(f"`{f}`" for f in files) if files else "*(none)*"
        lines.append(f"- {mark} **{t}**: {detail}")

    lines.append("")
    lines.append("## Inventory")
    lines.append("")
    lines.append(f"**Total papers: {inv['total_papers']}**")
    lines.append("")
    lines.append("| Topic | Papers |")
    lines.append("|-------|--------|")
    for t, c in inv["papers_per_topic"].items():
        lines.append(f"| {t} | {c} |")

    lines.append("")
    lines.append(f"**Total nodes: {inv['total_nodes']}**")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for prefix, c in inv["nodes_per_type"].items():
        lines.append(f"| `{prefix}.*` | {c} |")

    lines.append("")
    lines.append(f"**Total relations: {inv['total_relations']}**")
    lines.append("")
    lines.append("| Predicate | Count |")
    lines.append("|-----------|-------|")
    for pred, c in inv["relations_per_predicate"].items():
        lines.append(f"| {pred} | {c} |")

    lines.append("")
    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Compute statistics and reasoning-readiness metrics for sci-logic-kb."
    )
    parser.add_argument(
        "--repo-path",
        type=Path,
        default=Path("."),
        help="Root of the sci-logic-kb repository (default: current directory).",
    )
    fmt = parser.add_mutually_exclusive_group()
    fmt.add_argument("--json", action="store_true", help="Output as JSON.")
    fmt.add_argument("--markdown", action="store_true", help="Output as Markdown report.")
    args = parser.parse_args()

    repo = args.repo_path.resolve()
    if not (repo / "topics").is_dir():
        print(f"ERROR: {repo}/topics not found. Use --repo-path.", file=sys.stderr)
        sys.exit(1)

    stats = analyse(repo)

    if args.json:
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    elif args.markdown:
        print(format_markdown(stats))
    else:
        print(format_text(stats))


if __name__ == "__main__":
    main()
