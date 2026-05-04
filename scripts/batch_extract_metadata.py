#!/usr/bin/env python3
"""Batch extract metadata from PDFs and generate minimal YAML paper nodes.

Sources (tried in order):
  1. pdfinfo — basic PDF metadata (title, author)
  2. pdftotext -f 1 -l 1 — first page text for DOI extraction
  3. CrossRef API — structured metadata from DOI (most reliable)
  4. Fallback — placeholder from zotero_key

Usage:
  python scripts/batch_extract_metadata.py --dry-run
  python scripts/batch_extract_metadata.py
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

TODAY = date.today().isoformat()
PDF_DIR = Path("/data/papers-rag-1000/papers")
STATUS_FILE = Path("data/ingestion_status.json")

# Topic → contribution_type default (most common per topic from existing YAML)
DEFAULT_CONTRIBUTION = {
    "optical-frequency-combs": "evidence",
    "ultrastable-laser": "evidence",
    "time-frequency-transfer": "evidence",
    "frequency-standards": "evidence",
    "timescales": "evidence",
    "shared": "framework",
}

DOI_RE = re.compile(r"\b(10\.\d{4,}/[^\s\"]+)\b", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def pdfinfo(path: Path) -> dict[str, str]:
    """Extract basic PDF metadata."""
    r = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, timeout=15)
    info = {}
    for line in r.stdout.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            info[key.strip()] = val.strip()
    return info


def pdftotext_first_page(path: Path) -> str:
    """Extract first page as plain text."""
    r = subprocess.run(
        ["pdftotext", "-f", "1", "-l", "1", str(path), "-"],
        capture_output=True, text=True, timeout=30,
    )
    return r.stdout


def extract_doi(text: str) -> str | None:
    """Try to find a DOI in text."""
    m = DOI_RE.search(text)
    return m.group(1).rstrip(".") if m else None


def extract_year(text: str) -> int | None:
    """Try to find a publication year near the top of the first page."""
    years = YEAR_RE.findall(text[:2000])
    for y in years:
        yi = int(y)
        if 1960 <= yi <= 2027:
            return yi
    return None


def crossref_lookup(doi: str) -> dict | None:
    """Fetch structured metadata from CrossRef API."""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "sci-logic-kb/1.0 (mailto:kb@example.com)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        msg = data.get("message", {})
        authors = []
        for a in msg.get("author", []):
            family = a.get("family", "")
            given = a.get("given", "")
            if family:
                name = f"{given} {family}" if given else family
                authors.append(name)
        title_list = msg.get("title", [])
        title = title_list[0] if title_list else ""
        journal_list = msg.get("container-title", [])
        journal = journal_list[0] if journal_list else ""
        year = msg.get("created", {}).get("date-parts", [[None]])[0][0]
        if not year:
            year = msg.get("published-print", {}).get("date-parts", [[None]])[0][0]
        volume = msg.get("volume", "")
        pages = msg.get("page", "")
        return {
            "title": title,
            "authors": authors,
            "first_author": authors[0].split()[-1] if authors else "",
            "journal": journal,
            "year": int(year) if year else None,
            "volume": volume,
            "pages": pages,
            "doi": doi,
        }
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError) as e:
        print(f"  CrossRef lookup failed for {doi}: {e}")
        return None


def build_metadata(pdf_path: Path, zotero_key: str, topic: str) -> dict:
    """Extract best available metadata for a paper."""
    # Level 1: pdfinfo
    info = pdfinfo(pdf_path)
    pdf_title = info.get("Title", "").strip()
    pdf_author = info.get("Author", "").strip()

    # Level 2: pdftotext first page
    text = pdftotext_first_page(pdf_path)
    doi = extract_doi(text)
    year = extract_year(text)

    # If no DOI in first page, try pdfinfo Subject (sometimes has DOI)
    if not doi:
        subject = info.get("Subject", "")
        doi_match = DOI_RE.search(subject)
        if doi_match:
            doi = doi_match.group(1).rstrip(".")

    # Level 3: CrossRef (if DOI found)
    cr = crossref_lookup(doi) if doi else None

    # Build final metadata
    meta = {
        "zotero_key": zotero_key,
        "topic": topic,
        "source_type": "journal_paper",
        "contribution_type": DEFAULT_CONTRIBUTION.get(topic, "evidence"),
        "reliability": "high",
        "title": "",
        "year": None,
        "first_author": "",
        "authors": [],
        "journal": "",
        "volume": None,
        "pages": "",
        "doi": doi or None,
        "note": "",
    }

    metadata_source = "placeholder"

    if cr:
        # CrossRef data is most reliable
        meta["title"] = cr["title"] or pdf_title
        meta["authors"] = cr["authors"]
        meta["first_author"] = cr["first_author"]
        meta["journal"] = cr["journal"] or ""
        meta["year"] = cr["year"] or year
        meta["volume"] = cr["volume"] or None
        meta["pages"] = cr["pages"] or ""
        meta["reliability"] = "high"
        metadata_source = "CrossRef"
    elif pdf_title:
        meta["title"] = pdf_title
        meta["first_author"] = pdf_author.split(",")[0].split()[-1] if pdf_author else ""
        meta["authors"] = [pdf_author] if pdf_author else []
        meta["year"] = year
        meta["reliability"] = "medium"
        metadata_source = "PDF metadata"
    else:
        meta["title"] = zotero_key
        meta["year"] = year
        meta["reliability"] = "low"
        metadata_source = "placeholder (needs expert review)"

    # Clean up author list
    if isinstance(meta["authors"], str):
        meta["authors"] = [meta["authors"]]

    meta["note"] = f"[批量提取] 元数据来源：{metadata_source}。内容待专家提取。"

    return meta


def generate_yaml(meta: dict) -> str:
    """Generate canonical YAML string from meta dict."""
    lines = [
        f"# {meta['first_author']} {meta['year'] or '????'} — {meta['title'][:80]} [{meta['contribution_type']}]",
        "# 提取者：AI 批量提取（待专家确认）",
        f"# 提取日期：{TODAY}",
        "meta:",
    ]

    def val(name: str, v):
        if v is None:
            return "null"
        if isinstance(v, bool):
            return str(v).lower()
        if isinstance(v, int):
            return str(v)
        if isinstance(v, float):
            return str(v)
        s = str(v)
        if name in ("zotero_key", "topic", "source_type", "contribution_type",
                     "reliability", "doi", "volume", "pages", "year"):
            return s.strip('"').strip("'")
        if name in ("title", "journal", "first_author"):
            escaped = s.replace('"', '\\"')
            return f'"{escaped}"'
        return s

    for field in ["zotero_key", "topic", "source_type", "contribution_type",
                   "reliability", "title", "year", "first_author"]:
        if field in meta and meta[field] is not None:
            lines.append(f"  {field}: {val(field, meta[field])}")

    if meta.get("authors"):
        author_strs = [f'"{a}"' for a in meta["authors"]]
        lines.append(f"  authors: [{', '.join(author_strs)}]")

    for field in ["journal", "volume", "pages", "doi"]:
        if field in meta and meta[field] is not None and meta[field] != "":
            lines.append(f"  {field}: {val(field, meta[field])}")

    # note
    note = meta.get("note", "")
    lines.append(f"  note: >")
    for nline in note.split("\n"):
        lines.append(f"    {nline.strip()}")

    # Stub sections
    lines.extend(["", "entities: []", "principles: []", "methods: []",
                   "metrics: []", "relations: []", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch metadata extraction")
    parser.add_argument("--dry-run", action="store_true", help="Extract but don't write YAML")
    args = parser.parse_args()

    # Load status
    with open(STATUS_FILE) as f:
        status = json.load(f)

    # Find done papers with topic assignments
    done_keys = {k for k, v in status.items() if v == "done" and not k.startswith("_")}
    papers = []
    for k in done_keys:
        t = status.get(f"_topic_{k}")
        if t:
            pdf = PDF_DIR / f"{k}.pdf"
            if pdf.exists():
                papers.append((k, t, pdf))

    print(f"Papers to extract: {len(papers)}")

    tiers = {"CrossRef": 0, "PDF metadata": 0, "placeholder": 0}
    written = 0

    for i, (zotero_key, topic, pdf_path) in enumerate(papers):
        print(f"[{i+1}/{len(papers)}] {zotero_key} [{topic}]")

        try:
            meta = build_metadata(pdf_path, zotero_key, topic)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        # Determine tier
        if "CrossRef" in meta.get("note", ""):
            tiers["CrossRef"] += 1
        elif "PDF metadata" in meta.get("note", ""):
            tiers["PDF metadata"] += 1
        else:
            tiers["placeholder"] += 1

        print(f"  → {meta['title'][:70]}... [{meta['reliability']}]")

        if not args.dry_run:
            out_dir = Path(f"topics/{topic}/papers")
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{zotero_key}.yaml"
            yaml_content = generate_yaml(meta)
            out_path.write_text(yaml_content)
            written += 1

        # Polite delay for CrossRef
        if "CrossRef" in meta.get("note", ""):
            time.sleep(0.2)

    print(f"\n--- Results ---")
    print(f"CrossRef:     {tiers['CrossRef']}")
    print(f"PDF metadata: {tiers['PDF metadata']}")
    print(f"Placeholder:  {tiers['placeholder']}")
    if not args.dry_run:
        print(f"\nWrote {written} YAML files")


if __name__ == "__main__":
    main()
