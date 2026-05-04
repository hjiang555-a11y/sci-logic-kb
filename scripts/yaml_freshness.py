#!/usr/bin/env python3
"""Paper YAML freshness checker — reports stale or schema-drifted YAML files.

Usage:
  python scripts/yaml_freshness.py               # list all papers with age > 6 months
  python scripts/yaml_freshness.py --months 12   # custom threshold
  python scripts/yaml_freshness.py --schema      # only check schema version drift
  python scripts/yaml_freshness.py --json        # machine-readable output
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _extract_extraction_date(yaml_text: str) -> str | None:
    """Extract extraction date from YAML header comment line: 提取日期：YYYY-MM-DD"""
    m = re.search(r"提取日期[：:]\s*(\d{4}-\d{2}-\d{2})", yaml_text)
    if m:
        return m.group(1)
    return None


def _extract_schema_version(yaml_text: str) -> str | None:
    """Extract schema version from YAML header comment: Schema版本：vX.Y"""
    m = re.search(r"Schema版本[：:]\s*(v?\d+\.\d+)", yaml_text)
    if m:
        return m.group(1)
    return None


def _current_schema_version() -> str:
    """Parse SCHEMA.md for the declared schema version."""
    schema_path = REPO / "SCHEMA.md"
    if not schema_path.exists():
        return "unknown"
    text = schema_path.read_text()
    m = re.search(r"S-ARK.*?v(\d+\.\d+)", text) or re.search(r"v(\d+\.\d+)", text)
    return f"v{m.group(1)}" if m else "unknown"


def _scan_yamls() -> list[dict]:
    """Scan all topics/*/papers/*.yaml and extract freshness metadata."""
    papers_dir = REPO / "topics"
    if not papers_dir.exists():
        return []

    results = []
    for yaml_path in sorted(papers_dir.glob("*/papers/*.yaml")):
        topic = yaml_path.parent.parent.name
        try:
            text = yaml_path.read_text()
        except Exception:
            continue

        ext_date = _extract_extraction_date(text)
        schema_ver = _extract_schema_version(text)

        # Fallback: use file mtime if no extraction date
        if ext_date:
            try:
                age_days = (datetime.now(timezone.utc) -
                           datetime.strptime(ext_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)).days
            except ValueError:
                age_days = None
        else:
            ext_date = None
            age_days = None

        results.append({
            "file": str(yaml_path.relative_to(REPO)),
            "topic": topic,
            "extraction_date": ext_date,
            "schema_version": schema_ver,
            "age_days": age_days,
        })

    return results


def _parse_args():
    p = argparse.ArgumentParser(description="Paper YAML freshness checker")
    p.add_argument("--months", type=int, default=6, help="Stale threshold in months (default 6)")
    p.add_argument("--schema", action="store_true", help="Only check schema version drift")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    return p.parse_args()


def main():
    args = _parse_args()
    papers = _scan_yamls()
    current_schema = _current_schema_version()

    if not papers:
        print("No YAML papers found.")
        return

    # Filter stale (by extraction date age)
    threshold_days = args.months * 30
    stale = [p for p in papers if p["age_days"] is not None and p["age_days"] > threshold_days]
    no_date = [p for p in papers if p["extraction_date"] is None]
    schema_drift = [p for p in papers if p["schema_version"] and p["schema_version"] != current_schema]

    if args.json:
        print(json.dumps({
            "total": len(papers),
            "current_schema": current_schema,
            "stale_gt_n_months": len(stale),
            "no_extraction_date": len(no_date),
            "schema_drifted": len(schema_drift),
            "stale": stale,
            "no_date": no_date,
            "schema_drift": schema_drift,
        }, indent=2))
        return

    print(f"── Paper YAML Freshness ──")
    print(f"  Total papers: {len(papers)}  |  Current schema: {current_schema}  "
          f"|  Stale threshold: >{args.months} months")
    print()

    if args.schema:
        if schema_drift:
            print(f"  ⚠️  {len(schema_drift)} files with schema drift (current: {current_schema}):")
            for p in schema_drift:
                print(f"      {p['file']}  [{p['schema_version']}]")
        else:
            print(f"  ✅ All files match current schema ({current_schema})")
        return

    if stale:
        print(f"  ⚠️  {len(stale)} papers extracted >{args.months} months ago:")
        for p in sorted(stale, key=lambda x: x["age_days"] or 0, reverse=True)[:20]:
            print(f"      {p['file']:<55}  {p['age_days']}d ago")
        if len(stale) > 20:
            print(f"      ... and {len(stale) - 20} more")
    else:
        print(f"  ✅ No papers older than {args.months} months")

    if no_date:
        print(f"  ⚠️  {len(no_date)} papers without extraction date (use file mtime instead)")
        for p in no_date[:10]:
            print(f"      {p['file']}")
        if len(no_date) > 10:
            print(f"      ... and {len(no_date) - 10} more")

    if schema_drift:
        print(f"  ⚠️  {len(schema_drift)} papers with schema drift from {current_schema}:")
        for p in schema_drift[:10]:
            print(f"      {p['file']:<55}  [{p['schema_version']}]")
        if len(schema_drift) > 10:
            print(f"      ... and {len(schema_drift) - 10} more")


if __name__ == "__main__":
    main()
