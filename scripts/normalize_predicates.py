#!/usr/bin/env python3
"""One-time migration: replace non-canonical predicates with canonical equivalents.

Usage:
  python scripts/normalize_predicates.py --dry-run    # report changes only
  python scripts/normalize_predicates.py               # apply changes
"""

import os
import sys
import argparse
import re
from pathlib import Path

MERGE_MAP: dict[str, str] = {
    # Inverse normalization
    "ENABLES": "ENABLED-BY",
    "REALIZED-BY": "REALIZES",
    "IMPLEMENTED-BY": "REALIZES",
    "DEMONSTRATED-BY": "DEMONSTRATES",
    # Semantic merges
    "USES-METHOD": "IMPLEMENTS",
    "DEPENDS-ON": "ENABLED-BY",
    "APPRAISES": "CHARACTERIZES",
    "RESOLVED-BY": "BOUNDED-BY",
    "PRODUCES": "ENABLED-BY",
    "IMPROVES-ON": "DERIVED-FROM",
    "USES": "ENABLED-BY",
    "MEASURES": "CHARACTERIZED-BY",
    "APPLIED-TO": "CONDITIONED-BY",
    "VALIDATES": "DEMONSTRATES",
    "UNDERLIES": "ENABLED-BY",
    "SUBSUMED-BY": "PART-OF",
    "MITIGATES": "BOUNDED-BY",
    "MANIFESTS-AS": "CHARACTERIZED-BY",
    "IS-LIMITED-BY": "BOUNDED-BY",
    "INTERROGATES": "CHARACTERIZES",
    "HAS-SUBSYSTEM": "PART-OF",
    "GOVERNS": "CONDITIONED-BY",
    "ENHANCED-BY": "ENABLED-BY",
    "ENABLED": "ENABLED-BY",
    "CONSTRAINS": "BOUNDED-BY",
    "CONSTRAINED-BY": "BOUNDED-BY",
    "CONNECTED-BY": "PART-OF",
    "COMPARED-WITH": "COMPETES-WITH",
    "CALIBRATES": "CHARACTERIZED-BY",
    "BROADENED-BY": "ENABLED-BY",
    "BASED_ON": "DERIVED-FROM",
}

PREDICATE_RE = re.compile(r"^(\s+predicate:\s*)(\S[\S ]*)$", re.MULTILINE)


def normalize_file(path: Path, dry_run: bool) -> list[tuple[str, str]]:
    """Replace non-canonical predicates in a YAML file.

    Returns list of (old, new) changes made.
    """
    original = path.read_text()
    changes: list[tuple[str, str]] = []

    def replace(match: re.Match) -> str:
        indent = match.group(1)
        pred = match.group(2).strip()
        if pred in MERGE_MAP:
            new_pred = MERGE_MAP[pred]
            changes.append((pred, new_pred))
            return f"{indent}{new_pred}"
        return match.group(0)

    new_content = PREDICATE_RE.sub(replace, original)

    if changes and not dry_run:
        path.write_text(new_content)

    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize relation predicates")
    parser.add_argument("--dry-run", action="store_true", help="Report only, no writes")
    args = parser.parse_args()

    papers_dir = Path("topics")
    yaml_files = sorted(papers_dir.rglob("papers/*.yaml"))

    total_files = 0
    total_changes = 0
    pred_counts: dict[tuple[str, str], int] = {}

    for yf in yaml_files:
        changes = normalize_file(yf, dry_run=args.dry_run)
        if changes:
            total_files += 1
            total_changes += len(changes)
            for old, new in changes:
                key = (old, new)
                pred_counts[key] = pred_counts.get(key, 0) + 1
            if args.dry_run:
                rel_path = yf.relative_to(Path("."))
                for old, new in changes:
                    print(f"  {rel_path}: {old} → {new}")

    print(f"\n{'Would modify' if args.dry_run else 'Modified'} "
          f"{total_files} files, {total_changes} predicate changes")
    print("\nChange summary:")
    for (old, new), cnt in sorted(pred_counts.items()):
        print(f"  {old:25s} → {new:25s}  x{cnt}")

    if args.dry_run and total_files > 0:
        print("\nRe-run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
