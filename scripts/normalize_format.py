#!/usr/bin/env python3
"""Normalize YAML paper files to canonical format (v4.6).

Fixes applied:
  1. Add missing header comment (derived from meta fields)
  2. Normalize meta field ordering
  3. Normalize quoting (unquoted: zotero_key, doi, source_type, etc.)
  4. Ensure topic: field present (from directory)
  5. Normalize note: to folded block scalar (>)
  6. Ensure yaml dump style

Usage:
  python scripts/normalize_format.py --dry-run
  python scripts/normalize_format.py
"""

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import date

import yaml

# Canonical meta field order
META_ORDER = [
    "zotero_key", "topic", "source_type", "contribution_type",
    "reliability", "title", "year", "first_author", "authors",
    "journal", "volume", "pages", "doi", "note",
]

# Fields that should NOT be quoted in YAML output
UNQUOTED_FIELDS = {
    "zotero_key", "topic", "source_type", "contribution_type",
    "reliability", "doi", "volume", "pages", "year",
}

# Fields that keep their original quoting (rich text)
QUOTED_FIELDS = {"title", "journal", "first_author", "note"}

# Section boundaries after meta
SECTION_HEADERS = ("entities:", "principles:", "methods:", "metrics:", "relations:")

# Maps topic directory names to use for missing topic fields
DIR_TO_TOPIC = {
    "ultrastable-laser": "ultrastable-laser",
    "optical-frequency-combs": "optical-frequency-combs",
    "time-frequency-transfer": "time-frequency-transfer",
    "frequency-standards": "frequency-standards",
    "timescales": "timescales",
    "shared": "shared",
}

TODAY = date.today().isoformat()


def extract_meta_and_body(content: str) -> tuple[str, str, str]:
    """Split file into header_comment, meta_block, body."""
    lines = content.split("\n")
    header_lines = []
    meta_start = None
    body_start = None

    for i, line in enumerate(lines):
        if line.startswith("#"):
            header_lines.append(line)
        elif line.startswith("meta:"):
            meta_start = i
            break
        elif line.startswith("---"):
            # Old format with YAML document separator
            header_lines.append(line)
        elif any(line.startswith(sh) for sh in SECTION_HEADERS):
            body_start = i
            meta_start = i  # no meta block
            break

    if meta_start is None:
        # No meta block and no sections found — whole file
        return "\n".join(header_lines), "", content

    if body_start is None:
        # Find where meta ends and body begins
        for i in range(meta_start + 1, len(lines)):
            if any(lines[i].startswith(sh) for sh in SECTION_HEADERS):
                body_start = i
                break
        if body_start is None:
            body_start = len(lines)

    header = "\n".join(header_lines)
    meta = "\n".join(lines[meta_start:body_start])
    body = "\n".join(lines[body_start:])
    return header, meta, body


def parse_meta_block(meta_text: str) -> dict:
    """Parse the meta: YAML block into a dict."""
    if not meta_text.strip():
        return {}
    try:
        parsed = yaml.safe_load(meta_text)
        if isinstance(parsed, dict) and "meta" in parsed:
            return parsed["meta"] or {}
        return parsed or {}
    except yaml.YAMLError:
        return {}


def yaml_scalar(value, field_name: str) -> str:
    """Format a YAML scalar value with appropriate quoting."""
    if value is None:
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    if isinstance(value, (int, float)):
        return str(value)

    s = str(value)

    if field_name in UNQUOTED_FIELDS:
        return s.strip('"').strip("'")

    # For string fields, check if quoting is needed
    if field_name in QUOTED_FIELDS:
        # Always use single-line format for simple titles
        if "\n" not in s:
            # Escape internal double quotes
            escaped = s.replace('"', '\\"')
            return f'"{escaped}"'
        # Multi-line: use folded scalar
        return f">\n    {s}"

    # Default: quote if contains special chars
    if any(c in s for c in (':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`')):
        return f'"{s}"'
    return s


def build_meta_block(meta: dict) -> str:
    """Build canonical meta: block from dict."""
    lines = ["meta:"]
    for field in META_ORDER:
        if field not in meta or meta[field] is None:
            continue
        value = meta[field]

        if field == "authors":
            if isinstance(value, list) and value:
                author_strs = [f'"{a}"' if isinstance(a, str) else str(a) for a in value]
                lines.append(f"  authors: [{', '.join(author_strs)}]")
        elif field == "note":
            note_str = str(value).strip()
            if "\n" in note_str:
                lines.append("  note: >")
                for nline in note_str.split("\n"):
                    lines.append(f"    {nline.strip()}")
            else:
                lines.append(f'  note: >')
                lines.append(f"    {note_str}")
        else:
            val_str = yaml_scalar(value, field)
            lines.append(f"  {field}: {val_str}")

    return "\n".join(lines)


def build_header(meta: dict) -> str:
    """Build canonical header comment."""
    first_author = meta.get("first_author", "")
    if not first_author and meta.get("authors"):
        authors = meta["authors"]
        if isinstance(authors, list) and authors:
            first_author = authors[0].split()[-1] if " " in str(authors[0]) else str(authors[0])

    year = meta.get("year", "????")
    title = meta.get("title", "Unknown Title")
    # Shorten title for header
    short_title = title if len(str(title)) <= 80 else str(title)[:77] + "..."

    ctype = meta.get("contribution_type", "unknown")

    return f"# {first_author} {year} — {short_title} [{ctype}]\n# 提取者：AI（待专家确认）\n# 提取日期：{TODAY}"


def normalize_file(path: Path, dry_run: bool) -> list[str]:
    """Normalize a single YAML file. Returns list of change descriptions."""
    original = path.read_text()
    header, meta_text, body = extract_meta_and_body(original)
    meta = parse_meta_block(meta_text)

    changes = []

    # Check for missing meta block
    if not meta:
        changes.append("MISSING meta block — skipping (needs manual fix)")
        return changes

    # Add topic from directory if missing
    if "topic" not in meta or meta["topic"] is None:
        for dname, topic_name in DIR_TO_TOPIC.items():
            if dname in str(path):
                meta["topic"] = topic_name
                changes.append(f"topic: (missing) → {topic_name}")
                break

    # Normalize DOI quoting
    doi = meta.get("doi")
    if doi and isinstance(doi, str) and (doi.startswith('"') or " " in doi):
        clean_doi = doi.strip('"').strip("'")
        if clean_doi != doi:
            meta["doi"] = clean_doi
            changes.append(f"doi: unquoted")

    # Build new header + meta
    new_header = build_header(meta)
    new_meta = build_meta_block(meta)

    # Only report if header is missing
    if not header.strip() or header.strip() == "---":
        changes.append("header: added")

    new_content = new_header + "\n" + new_meta + "\n" + body.lstrip("\n")

    if new_content != original:
        if not dry_run:
            path.write_text(new_content)

    if not changes and new_content != original:
        changes.append("field ordering normalized")

    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize YAML paper format")
    parser.add_argument("--dry-run", action="store_true", help="Report only")
    args = parser.parse_args()

    papers_dir = Path("topics")
    yaml_files = sorted(papers_dir.rglob("papers/*.yaml"))

    total = 0
    skipped = 0
    for yf in yaml_files:
        changes = normalize_file(yf, dry_run=args.dry_run)
        if changes:
            total += 1
            rel = yf.relative_to(Path("."))
            if any("MISSING" in c for c in changes):
                skipped += 1
                print(f"  SKIP {rel}: {', '.join(changes)}")
            elif args.dry_run:
                print(f"  {rel}: {', '.join(changes)}")

    action = "Would modify" if args.dry_run else "Normalized"
    print(f"\n{action} {total} files" + (f" (skipped {skipped})" if skipped else ""))
    if args.dry_run and total > 0:
        print("Re-run without --dry-run to apply.")


if __name__ == "__main__":
    main()
