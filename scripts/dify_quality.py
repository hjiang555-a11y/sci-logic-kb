#!/usr/bin/env python3
"""Dify export quality checker — validates knowledge_base.jsonl and dify_pilot md exports.

Usage:
  python scripts/dify_quality.py            # check JSONL and pilot md files
  python scripts/dify_quality.py --json     # machine-readable output
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
JSONL_PATH = REPO / "export" / "knowledge_base.jsonl"
PILOT_DIR = REPO / "export" / "dify_pilot"


def _check_jsonl():
    """Analyze the JSONL Dify export."""
    if not JSONL_PATH.exists():
        return {"error": f"JSONL file not found: {JSONL_PATH}"}

    chunks = []
    with open(JSONL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    chunks.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not chunks:
        return {"error": "No valid JSON chunks found"}

    content_lengths = [len(c.get("content", "")) for c in chunks]
    short_chunks = [c["id"] for c in chunks if len(c.get("content", "")) < 50]
    missing_relations = [c["id"] for c in chunks if not c.get("relations_summary")]
    topics = Counter(c.get("topic", "unknown") for c in chunks)
    types = Counter(c.get("type", "unknown") for c in chunks)

    return {
        "total_chunks": len(chunks),
        "total_chars": sum(content_lengths),
        "avg_chunk_size": round(sum(content_lengths) / len(content_lengths), 1),
        "min_chunk_size": min(content_lengths),
        "max_chunk_size": max(content_lengths),
        "short_chunks": short_chunks,
        "missing_relations": missing_relations,
        "topics": dict(topics),
        "types": dict(types),
    }


def _check_pilot():
    """Check the dify_pilot markdown exports."""
    if not PILOT_DIR.exists():
        return {"error": f"Pilot dir not found: {PILOT_DIR}"}

    md_files = sorted(PILOT_DIR.glob("*.md"))
    if not md_files:
        return {"files": [], "total_size_bytes": 0, "note": "No markdown files in pilot dir"}

    files_info = []
    for f in md_files:
        size = f.stat().st_size
        # Check for corresponding YAML source
        yaml_name = f.stem + ".yaml"
        yaml_exists = False
        for topic_dir in (REPO / "topics").iterdir():
            if topic_dir.is_dir() and (topic_dir / "papers" / yaml_name).exists():
                yaml_exists = True
                break

        files_info.append({
            "name": f.name,
            "size_bytes": size,
            "has_yaml_source": yaml_exists,
        })

    return {
        "files": files_info,
        "total_files": len(files_info),
        "total_size_bytes": sum(fi["size_bytes"] for fi in files_info),
        "missing_yaml_source": [fi["name"] for fi in files_info if not fi["has_yaml_source"]],
    }


def _parse_args():
    p = argparse.ArgumentParser(description="Dify export quality checker")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    return p.parse_args()


def main():
    args = _parse_args()

    jsonl = _check_jsonl()
    pilot = _check_pilot()

    if args.json:
        print(json.dumps({"jsonl": jsonl, "pilot": pilot}, indent=2))
        return

    # -- JSONL section --
    if "error" in jsonl:
        print(f"❌ JSONL: {jsonl['error']}")
    else:
        print("── Dify JSONL Export ──")
        print(f"  Chunks: {jsonl['total_chunks']}  |  "
              f"Total size: {jsonl['total_chars']:,} chars  |  "
              f"Avg chunk: {jsonl['avg_chunk_size']} chars")
        print(f"  Size range: {jsonl['min_chunk_size']}–{jsonl['max_chunk_size']} chars")
        if jsonl["short_chunks"]:
            print(f"  ⚠️  {len(jsonl['short_chunks'])} chunks with content <50 chars: "
                  f"{', '.join(jsonl['short_chunks'][:5])}"
                  + (f" ... (+{len(jsonl['short_chunks']) - 5} more)" if len(jsonl['short_chunks']) > 5 else ""))
        else:
            print(f"  ✅ No chunks with content <50 chars")
        if jsonl["missing_relations"]:
            print(f"  ⚠️  {len(jsonl['missing_relations'])} chunks missing relations_summary")
        else:
            print(f"  ✅ All chunks have relations_summary")
        print(f"  Topics: {jsonl['topics']}")
        print(f"  Types:  {jsonl['types']}")

    # -- Pilot section --
    print()
    if "error" in pilot:
        print(f"❌ Pilot: {pilot['error']}")
    else:
        print("── Dify Pilot MD Exports ──")
        print(f"  Files: {pilot['total_files']}  |  Total size: {pilot['total_size_bytes']:,} bytes")
        for fi in pilot["files"]:
            yaml_icon = "✅" if fi["has_yaml_source"] else "⚠️ "
            print(f"    {yaml_icon} {fi['name']}  ({fi['size_bytes']:,} bytes)")
        if pilot["missing_yaml_source"]:
            print(f"  ⚠️  {len(pilot['missing_yaml_source'])} files without YAML source: "
                  f"{', '.join(pilot['missing_yaml_source'])}")


if __name__ == "__main__":
    main()
