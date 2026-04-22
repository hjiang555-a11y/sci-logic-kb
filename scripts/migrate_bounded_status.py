#!/usr/bin/env python3
"""migrate_bounded_status.py — one-shot helper to suggest `limit_status`
values for existing BOUNDED-BY relations (v4.5+).

Emits a YAML-free textual proposal to stdout. Does **NOT** modify any files.
Reviewers manually transcribe approved suggestions into the source YAMLs.

Inference heuristic:
  * any breakthrough_paths[].status == 'demonstrated'  → resolved
  * is_system_limit == false  &&  dominated_by present → conditional
  * is_system_limit == false                           → conditional
  * is_system_limit == true (or unset)                 → active

``resolved_by`` candidates are collected from the demonstrated
breakthrough_paths' ``direction`` fields (pri.* / meth.* nodes).

Usage:
    python scripts/migrate_bounded_status.py [--topic ultrastable-laser]
    python scripts/migrate_bounded_status.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def _iter_items(section):
    if section is None:
        return []
    if isinstance(section, list):
        return [i for i in section if isinstance(i, dict)]
    if isinstance(section, dict):
        return list(section.values())
    return []


def infer(rel: dict) -> tuple[str, list[str]]:
    """Return (suggested_limit_status, candidate_resolved_by)."""
    bp = rel.get("breakthrough_paths") or []
    directions: list[str] = []
    demonstrated = False
    for p in bp:
        if not isinstance(p, dict):
            continue
        status = str(p.get("status", "")).strip().lower()
        if status == "demonstrated":
            demonstrated = True
            d = p.get("direction")
            if isinstance(d, str) and d.startswith(("pri.", "meth.")):
                directions.append(d)
    if demonstrated:
        # Deduplicate while preserving order
        seen: set[str] = set()
        uniq = [d for d in directions if not (d in seen or seen.add(d))]
        return "resolved", uniq
    is_limit = rel.get("is_system_limit")
    if is_limit is False:
        return "conditional", []
    return "active", []


def analyze(repo: Path, topic: str | None = None) -> list[dict]:
    pattern = (
        f"topics/{topic}/papers/*.yaml" if topic else "topics/*/papers/*.yaml"
    )
    out: list[dict] = []
    for yf in sorted(repo.glob(pattern)):
        try:
            doc = yaml.safe_load(yf.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict):
            continue
        for rel in _iter_items(doc.get("relations")):
            if rel.get("predicate") != "BOUNDED-BY":
                continue
            current = rel.get("limit_status")
            suggested, resolved_by = infer(rel)
            if current is None or str(current).strip().lower() != suggested:
                out.append({
                    "file": str(yf.relative_to(repo)),
                    "rel_id": rel.get("id"),
                    "subject": rel.get("subject"),
                    "object": rel.get("object"),
                    "current_limit_status": current,
                    "suggested_limit_status": suggested,
                    "suggested_resolved_by": resolved_by,
                })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-path", type=Path, default=Path("."))
    ap.add_argument("--topic", type=str, default=None)
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args(argv)
    repo = args.repo_path.resolve()

    proposals = analyze(repo, args.topic)
    if args.as_json:
        print(json.dumps(proposals, ensure_ascii=False, indent=2))
        return 0

    if not proposals:
        print("No BOUNDED-BY relations need migration.")
        return 0

    print(f"# {len(proposals)} BOUNDED-BY relation(s) have proposed "
          f"`limit_status` changes\n")
    for p in proposals:
        print(f"- {p['file']}  ·  rel `{p['rel_id']}`")
        print(f"    subject: {p['subject']}  → object: {p['object']}")
        cur = p['current_limit_status'] or "(unset)"
        print(f"    current: {cur}   →   suggested: {p['suggested_limit_status']}")
        if p['suggested_resolved_by']:
            rb = ", ".join(p['suggested_resolved_by'])
            print(f"    resolved_by (from demonstrated breakthrough_paths): {rb}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
