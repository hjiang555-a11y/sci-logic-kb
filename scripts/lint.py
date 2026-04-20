#!/usr/bin/env python3
"""
lint.py — Advanced lint / health-check for the sci-logic-kb knowledge base.

Checks:
  1.  Orphan nodes          (WARNING)
  2.  Dangling references   (ERROR)
  3.  Duplicate definitions (ERROR)
  4.  Duplicate relation IDs (ERROR)
  5.  Reasoning chain gaps  (WARNING)  — BOUNDED-BY without breakthrough_paths
  6.  Missing evidence       (WARNING) — relations without source.claim
  7.  Missing conditions     (WARNING) — principles without conditions
  8.  Missing metric conds   (WARNING) — metrics with demonstrated_value but no conditions
  9.  Invalid predicates     (ERROR)   — deprecated predicates
  10. Invalid node ID prefix (ERROR)
  11. Missing meta fields    (WARNING)

Exit code: 0 if no errors (warnings OK unless --strict), 1 if errors found.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


# ── Constants ────────────────────────────────────────────────────────────────

VALID_PREFIXES = ("ent.", "pri.", "meth.", "met.", "rel.")

VALID_PREDICATES = frozenset({
    "PART-OF",
    "CHARACTERIZED-BY",
    "OPERATIONALIZED-AS",
    "ENABLED-BY",
    "BOUNDED-BY",
    "DERIVED-FROM",
    "CONDITIONED-BY",
    "COMPETES-WITH",
})

DEPRECATED_PREDICATES = frozenset({
    "GOVERNED-BY",
    "EQUIVALENT-IN-CONTEXT",
    "SUPPORTED-BY",
    "BREAKTHROUGH-VIA",
})

REQUIRED_META_FIELDS = ("zotero_key", "title", "year", "first_author")

NODE_SECTIONS = ("entities", "principles", "methods", "metrics")


# ── Data collection helpers ──────────────────────────────────────────────────

class Issue:
    """A single lint issue."""

    __slots__ = ("level", "category", "file", "detail")

    def __init__(self, level: str, category: str, file: str, detail: str):
        self.level = level        # "ERROR" or "WARNING"
        self.category = category  # human-readable check name
        self.file = file          # relative path
        self.detail = detail

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "category": self.category,
            "file": self.file,
            "detail": self.detail,
        }

    def __str__(self) -> str:
        return f"[{self.level}] {self.file}: {self.detail}"


def _iter_items(section: Any) -> list[dict[str, Any]]:
    """Return a list of dicts from a YAML section that may be a list or a dict."""
    if section is None:
        return []
    if isinstance(section, list):
        return [item for item in section if isinstance(item, dict)]
    if isinstance(section, dict):
        return list(section.values()) if section else []
    return []


# ── Core scanning ────────────────────────────────────────────────────────────

def scan_files(yaml_paths: list[Path]) -> tuple[
    dict[str, list[str]],          # node_id -> [defining files]
    dict[str, list[str]],          # relation_id -> [defining files]
    dict[str, set[str]],           # relation refs: subject/object ids per file
    list[dict[str, Any]],          # all relations (with file info)
    list[dict[str, Any]],          # all nodes (with file, section info)
    dict[str, dict[str, Any]],     # file -> parsed meta
]:
    """Parse all YAML files and collect definitions and references."""

    node_defs: dict[str, list[str]] = {}          # id -> [files]
    rel_defs: dict[str, list[str]] = {}            # id -> [files]
    rel_refs: dict[str, set[str]] = {}             # file -> set of subject/object ids
    all_relations: list[dict[str, Any]] = []
    all_nodes: list[dict[str, Any]] = []
    file_metas: dict[str, dict[str, Any]] = {}

    for path in yaml_paths:
        rel_path = str(path)
        try:
            text = path.read_text(encoding="utf-8")
            doc = yaml.safe_load(text)
        except (yaml.YAMLError, OSError):
            # Silently skip unparseable files — caller handles this separately if needed
            continue

        if not isinstance(doc, dict):
            continue

        # Meta
        meta = doc.get("meta")
        if isinstance(meta, dict):
            file_metas[rel_path] = meta

        # Node definitions
        for section_key in NODE_SECTIONS:
            for item in _iter_items(doc.get(section_key)):
                node_id = item.get("id")
                if node_id is None:
                    continue
                node_defs.setdefault(node_id, []).append(rel_path)
                all_nodes.append({
                    "id": node_id,
                    "section": section_key,
                    "file": rel_path,
                    "data": item,
                })

        # Relations
        refs: set[str] = set()
        for item in _iter_items(doc.get("relations")):
            rid = item.get("id")
            if rid is not None:
                rel_defs.setdefault(rid, []).append(rel_path)
            subj = item.get("subject")
            obj = item.get("object")
            if subj:
                refs.add(subj)
            if obj:
                refs.add(obj)
            all_relations.append({**item, "_file": rel_path})

        rel_refs[rel_path] = refs

    return node_defs, rel_defs, rel_refs, all_relations, all_nodes, file_metas


# ── Individual checks ────────────────────────────────────────────────────────

def check_orphan_nodes(
    node_defs: dict[str, list[str]],
    all_relations: list[dict[str, Any]],
) -> list[Issue]:
    """1. Nodes never referenced by any relation subject or object."""
    referenced: set[str] = set()
    for rel in all_relations:
        subj = rel.get("subject")
        obj = rel.get("object")
        if subj:
            referenced.add(subj)
        if obj:
            referenced.add(obj)

    issues: list[Issue] = []
    for nid, files in sorted(node_defs.items()):
        # Relation IDs themselves are not expected as subjects/objects
        if nid.startswith("rel."):
            continue
        if nid not in referenced:
            for f in files:
                issues.append(Issue(
                    "WARNING", "orphan-node", f,
                    f"Node '{nid}' is defined but never referenced in any relation",
                ))
    return issues


def check_dangling_refs(
    node_defs: dict[str, list[str]],
    all_relations: list[dict[str, Any]],
) -> list[Issue]:
    """2. Relation subject/object referencing an undefined node."""
    defined_ids = set(node_defs.keys())
    issues: list[Issue] = []
    for rel in all_relations:
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        for role in ("subject", "object"):
            ref_id = rel.get(role)
            if ref_id and ref_id not in defined_ids:
                issues.append(Issue(
                    "ERROR", "dangling-ref", f,
                    f"Relation '{rid}' {role} references undefined node '{ref_id}'",
                ))
    return issues


def check_duplicate_defs(node_defs: dict[str, list[str]]) -> list[Issue]:
    """3. Same node ID defined in multiple files."""
    issues: list[Issue] = []
    for nid, files in sorted(node_defs.items()):
        if len(files) > 1:
            files_str = ", ".join(files)
            for f in files:
                issues.append(Issue(
                    "ERROR", "duplicate-def", f,
                    f"Node '{nid}' defined in multiple files: {files_str}",
                ))
    return issues


def check_duplicate_rel_ids(rel_defs: dict[str, list[str]]) -> list[Issue]:
    """4. Same relation ID used in multiple files."""
    issues: list[Issue] = []
    for rid, files in sorted(rel_defs.items()):
        if len(files) > 1:
            files_str = ", ".join(files)
            for f in files:
                issues.append(Issue(
                    "ERROR", "duplicate-rel-id", f,
                    f"Relation ID '{rid}' used in multiple files: {files_str}",
                ))
    return issues


def check_reasoning_chain_gaps(all_relations: list[dict[str, Any]]) -> list[Issue]:
    """5. BOUNDED-BY relations without breakthrough_paths."""
    issues: list[Issue] = []
    for rel in all_relations:
        if rel.get("predicate") != "BOUNDED-BY":
            continue
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        bp = rel.get("breakthrough_paths")
        if bp is None or (isinstance(bp, list) and len(bp) == 0):
            issues.append(Issue(
                "WARNING", "reasoning-chain-gap", f,
                f"BOUNDED-BY relation '{rid}' lacks breakthrough_paths",
            ))
    return issues


def check_missing_evidence(all_relations: list[dict[str, Any]]) -> list[Issue]:
    """6. Relations without source.claim."""
    issues: list[Issue] = []
    for rel in all_relations:
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        source = rel.get("source")
        if source is None:
            issues.append(Issue(
                "WARNING", "missing-evidence", f,
                f"Relation '{rid}' has no 'source' field",
            ))
        elif isinstance(source, dict) and not source.get("claim"):
            issues.append(Issue(
                "WARNING", "missing-evidence", f,
                f"Relation '{rid}' has 'source' but no 'claim'",
            ))
    return issues


def check_missing_conditions(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """7. Principle nodes without conditions."""
    issues: list[Issue] = []
    for node in all_nodes:
        if node["section"] != "principles":
            continue
        data = node["data"]
        if not data.get("conditions"):
            issues.append(Issue(
                "WARNING", "missing-conditions", node["file"],
                f"Principle '{node['id']}' has no 'conditions' field",
            ))
    return issues


def check_missing_metric_conditions(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """8. Metrics with demonstrated_value but without conditions."""
    issues: list[Issue] = []
    for node in all_nodes:
        if node["section"] != "metrics":
            continue
        data = node["data"]
        dv = data.get("demonstrated_value")
        if not isinstance(dv, dict):
            continue
        if not dv.get("conditions"):
            issues.append(Issue(
                "WARNING", "missing-metric-conditions", node["file"],
                f"Metric '{node['id']}' has demonstrated_value without 'conditions'",
            ))
    return issues


def check_invalid_predicates(all_relations: list[dict[str, Any]]) -> list[Issue]:
    """9. Relations using deprecated predicates."""
    issues: list[Issue] = []
    for rel in all_relations:
        pred = rel.get("predicate", "")
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        if pred in DEPRECATED_PREDICATES:
            issues.append(Issue(
                "ERROR", "invalid-predicate", f,
                f"Relation '{rid}' uses deprecated predicate '{pred}'",
            ))
    return issues


def check_invalid_id_prefix(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """10. Node IDs that don't start with a valid prefix."""
    issues: list[Issue] = []
    for node in all_nodes:
        nid = node["id"]
        if not nid.startswith(VALID_PREFIXES):
            issues.append(Issue(
                "ERROR", "invalid-id-prefix", node["file"],
                f"Node ID '{nid}' does not start with a valid prefix ({', '.join(VALID_PREFIXES)})",
            ))
    return issues


def check_missing_meta(
    yaml_paths: list[Path],
    file_metas: dict[str, dict[str, Any]],
) -> list[Issue]:
    """11. YAML files missing required meta fields."""
    issues: list[Issue] = []
    for path in yaml_paths:
        rel_path = str(path)
        meta = file_metas.get(rel_path)
        if meta is None:
            issues.append(Issue(
                "WARNING", "missing-meta", rel_path,
                "File has no 'meta' section",
            ))
            continue
        for field in REQUIRED_META_FIELDS:
            if not meta.get(field):
                issues.append(Issue(
                    "WARNING", "missing-meta", rel_path,
                    f"Meta section missing required field '{field}'",
                ))
    return issues


# ── Orchestration ────────────────────────────────────────────────────────────

def collect_yaml_paths(repo: Path, topic: str | None) -> list[Path]:
    """Gather all topics/*/papers/*.yaml paths, optionally filtered to one topic."""
    pattern = f"topics/{topic}/papers/*.yaml" if topic else "topics/*/papers/*.yaml"
    paths = sorted(repo.glob(pattern))
    return paths


def run_all_checks(
    yaml_paths: list[Path],
) -> list[Issue]:
    """Run every check and return a flat list of issues."""
    node_defs, rel_defs, rel_refs, all_relations, all_nodes, file_metas = scan_files(yaml_paths)

    issues: list[Issue] = []
    issues.extend(check_orphan_nodes(node_defs, all_relations))
    issues.extend(check_dangling_refs(node_defs, all_relations))
    issues.extend(check_duplicate_defs(node_defs))
    issues.extend(check_duplicate_rel_ids(rel_defs))
    issues.extend(check_reasoning_chain_gaps(all_relations))
    issues.extend(check_missing_evidence(all_relations))
    issues.extend(check_missing_conditions(all_nodes))
    issues.extend(check_missing_metric_conditions(all_nodes))
    issues.extend(check_invalid_predicates(all_relations))
    issues.extend(check_invalid_id_prefix(all_nodes))
    issues.extend(check_missing_meta(yaml_paths, file_metas))
    return issues


# ── Output formatting ────────────────────────────────────────────────────────

def format_grouped(issues: list[Issue], summary_only: bool) -> str:
    """Pretty-print issues grouped by category."""
    if not issues:
        return "✅  No issues found."

    by_cat: dict[str, list[Issue]] = {}
    for issue in issues:
        by_cat.setdefault(issue.category, []).append(issue)

    lines: list[str] = []
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")

    for cat in sorted(by_cat):
        group = by_cat[cat]
        levels = {i.level for i in group}
        level_tag = "ERROR" if "ERROR" in levels else "WARNING"
        lines.append(f"\n── {cat} ({len(group)} issues, {level_tag}) ──")
        if not summary_only:
            for issue in group:
                lines.append(f"  [{issue.level}] {issue.file}: {issue.detail}")

    lines.append(f"\nSummary: {errors} error(s), {warnings} warning(s) across {len(by_cat)} categories")
    return "\n".join(lines)


def format_json(issues: list[Issue]) -> str:
    """JSON output."""
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")
    return json.dumps({
        "errors": errors,
        "warnings": warnings,
        "issues": [i.to_dict() for i in issues],
    }, indent=2, ensure_ascii=False)


# ── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lint / health-check for sci-logic-kb YAML knowledge base.",
    )
    p.add_argument(
        "--repo-path", type=Path, default=Path("."),
        help="Root of the sci-logic-kb repository (default: current dir)",
    )
    p.add_argument(
        "--topic", type=str, default=None,
        help="Lint only one topic (e.g. 'ultrastable-laser')",
    )
    p.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors (non-zero exit code)",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results as JSON",
    )
    p.add_argument(
        "--summary", action="store_true",
        help="Only show summary counts, not individual issues",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo: Path = args.repo_path.resolve()
    yaml_paths = collect_yaml_paths(repo, args.topic)

    if not yaml_paths:
        msg = f"No YAML files found under {repo / 'topics'}"
        if args.topic:
            msg += f" for topic '{args.topic}'"
        print(msg, file=sys.stderr)
        return 1

    issues = run_all_checks(yaml_paths)

    # Output
    if args.json_output:
        print(format_json(issues))
    else:
        print(format_grouped(issues, summary_only=args.summary))

    # Exit code
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")
    if errors > 0:
        return 1
    if args.strict and warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
