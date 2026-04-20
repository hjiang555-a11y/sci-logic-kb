#!/usr/bin/env python3
"""Synthesis page freshness tracker for sci-logic-kb.

Detects when synthesis pages become stale due to newer paper YAML files,
and optionally marks them with frontmatter metadata for CI or human review.

Usage:
    python scripts/freshness.py --check          # default: report freshness
    python scripts/freshness.py --mark           # add/update frontmatter on stale pages
    python scripts/freshness.py --clear          # remove needs_update marks
    python scripts/freshness.py --list           # list all synthesis pages with status
    python scripts/freshness.py --repo-path /path/to/repo --check
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

NODE_ID_RE = re.compile(r"\b(ent|pri|meth|met|rel)\.[a-z][a-z0-9_]*\b")
YAML_REF_RE = re.compile(r"\b([a-z][a-z0-9_]*\d{4}[a-z]?)\.yaml\b")
FRONTMATTER_FENCE = "---"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def find_repo_root(explicit: str | None) -> Path:
    """Return the repository root directory."""
    if explicit:
        return Path(explicit).resolve()
    # Walk up from this script's location
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "SCHEMA.md").exists():
        return candidate
    return Path.cwd()


def discover_topics(repo: Path) -> list[Path]:
    """Return topic directories that contain a synthesis/ subfolder."""
    topics_dir = repo / "topics"
    if not topics_dir.is_dir():
        return []
    return sorted(
        t for t in topics_dir.iterdir()
        if t.is_dir() and (t / "synthesis").is_dir()
    )


def discover_synthesis_pages(topic_dir: Path) -> list[Path]:
    """Return all .md files under <topic>/synthesis/."""
    synth_dir = topic_dir / "synthesis"
    if not synth_dir.is_dir():
        return []
    return sorted(synth_dir.glob("*.md"))


def discover_paper_yamls(topic_dir: Path) -> list[Path]:
    """Return all .yaml files under <topic>/papers/."""
    papers_dir = topic_dir / "papers"
    if not papers_dir.is_dir():
        return []
    return sorted(papers_dir.glob("*.yaml"))


def file_mtime(path: Path) -> float:
    """Return modification time as a POSIX timestamp."""
    return path.stat().st_mtime


def extract_node_ids(text: str) -> set[str]:
    """Extract all node IDs (ent.xxx, pri.xxx, …) from markdown text."""
    return set(NODE_ID_RE.findall(text))


def extract_yaml_refs(text: str) -> set[str]:
    """Extract referenced YAML filenames (e.g. 'lee2026.yaml') from text."""
    return set(YAML_REF_RE.findall(text))


def mtime_to_datestr(ts: float) -> str:
    """Convert a POSIX timestamp to YYYY-MM-DD."""
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Frontmatter manipulation
# ---------------------------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Parse YAML frontmatter delimited by '---' fences.

    Returns (frontmatter_dict_or_None, body_without_frontmatter).
    Only simple key: value pairs are handled (no nested YAML).
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return None, text

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == FRONTMATTER_FENCE:
            end_idx = i
            break

    if end_idx is None:
        return None, text

    fm: dict[str, str] = {}
    for line in lines[1:end_idx]:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    body = "\n".join(lines[end_idx + 1:])
    return fm, body


def render_frontmatter(fm: dict[str, str]) -> str:
    """Render a simple frontmatter block."""
    lines = [FRONTMATTER_FENCE]
    for k, v in fm.items():
        if " " in v or "," in v or ":" in v:
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append(FRONTMATTER_FENCE)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Core freshness logic
# ---------------------------------------------------------------------------


class SynthesisStatus:
    """Freshness status of a single synthesis page."""

    def __init__(self, path: Path, topic_dir: Path):
        self.path = path
        self.topic_dir = topic_dir
        self.topic_name = topic_dir.name
        self.is_stale = False
        self.newer_yamls: list[str] = []
        self.node_ids_referenced: set[str] = set()
        self.yaml_refs: set[str] = set()
        self.frontmatter: dict[str, str] | None = None

    @property
    def rel_path(self) -> str:
        """Path relative to repo root (best-effort)."""
        try:
            return str(self.path.relative_to(self.topic_dir.parent.parent))
        except ValueError:
            return str(self.path)


def check_freshness(synth_path: Path, topic_dir: Path,
                    paper_yamls: list[Path]) -> SynthesisStatus:
    """Determine whether a synthesis page is stale."""
    status = SynthesisStatus(synth_path, topic_dir)
    synth_mtime = file_mtime(synth_path)

    text = synth_path.read_text(encoding="utf-8", errors="replace")
    status.frontmatter, _ = parse_frontmatter(text)

    # Extract references from the page content
    status.node_ids_referenced = {m.group(0) for m in NODE_ID_RE.finditer(text)}
    status.yaml_refs = extract_yaml_refs(text)

    # Build a lookup: node_id -> set of YAML paths that define it
    node_to_yamls: dict[str, set[Path]] = {}
    for yp in paper_yamls:
        try:
            ytxt = yp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for match in NODE_ID_RE.finditer(ytxt):
            nid = match.group(0)
            node_to_yamls.setdefault(nid, set()).add(yp)

    # Check 1: any paper YAML modified more recently than the synthesis page
    newer = []
    for yp in paper_yamls:
        if file_mtime(yp) > synth_mtime:
            newer.append(yp.name)

    # Check 2: referenced node IDs whose defining YAML is newer
    for nid in status.node_ids_referenced:
        for yp in node_to_yamls.get(nid, set()):
            if file_mtime(yp) > synth_mtime and yp.name not in newer:
                newer.append(yp.name)

    # Check 3: explicitly referenced YAML files that are newer
    for ref in status.yaml_refs:
        fname = ref if ref.endswith(".yaml") else ref + ".yaml"
        yp = topic_dir / "papers" / fname
        if yp.exists() and file_mtime(yp) > synth_mtime and yp.name not in newer:
            newer.append(yp.name)

    status.newer_yamls = sorted(set(newer))
    status.is_stale = len(status.newer_yamls) > 0

    # Also respect existing frontmatter mark
    if status.frontmatter and status.frontmatter.get("needs_update") == "true":
        status.is_stale = True

    return status


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def action_check(repo: Path) -> list[SynthesisStatus]:
    """Check freshness of all synthesis pages and report."""
    results: list[SynthesisStatus] = []
    for topic_dir in discover_topics(repo):
        yamls = discover_paper_yamls(topic_dir)
        for sp in discover_synthesis_pages(topic_dir):
            st = check_freshness(sp, topic_dir, yamls)
            results.append(st)

    for st in results:
        icon = "⚠️ " if st.is_stale else "✅"
        label = "STALE" if st.is_stale else "fresh"
        print(f"  {icon} {st.rel_path}  [{label}]")
        if st.newer_yamls:
            print(f"      newer papers: {', '.join(st.newer_yamls)}")

    stale_count = sum(1 for s in results if s.is_stale)
    total = len(results)
    print()
    if stale_count:
        print(f"⚠️  {stale_count}/{total} synthesis page(s) need updating.")
    else:
        print(f"✅ All {total} synthesis page(s) are fresh.")

    return results


def action_mark(repo: Path) -> list[SynthesisStatus]:
    """Mark stale synthesis pages with frontmatter metadata."""
    results: list[SynthesisStatus] = []
    today = date.today().isoformat()

    for topic_dir in discover_topics(repo):
        yamls = discover_paper_yamls(topic_dir)
        for sp in discover_synthesis_pages(topic_dir):
            st = check_freshness(sp, topic_dir, yamls)
            results.append(st)

            if not st.is_stale:
                print(f"  ✅ {st.rel_path}  [fresh — no changes]")
                continue

            text = sp.read_text(encoding="utf-8", errors="replace")
            existing_fm, body = parse_frontmatter(text)

            fm = existing_fm if existing_fm else {}
            fm["needs_update"] = "true"
            fm["stale_since"] = fm.get("stale_since", today)
            reason = f"New papers ingested: {', '.join(st.newer_yamls)}"
            fm["reason"] = reason

            new_text = render_frontmatter(fm) + "\n" + body
            sp.write_text(new_text, encoding="utf-8")
            print(f"  ⚠️  {st.rel_path}  [marked stale — {reason}]")

    return results


def action_clear(repo: Path) -> None:
    """Remove needs_update marks from all synthesis pages."""
    for topic_dir in discover_topics(repo):
        for sp in discover_synthesis_pages(topic_dir):
            text = sp.read_text(encoding="utf-8", errors="replace")
            fm, body = parse_frontmatter(text)

            if fm is None:
                print(f"  ✅ {sp.name}  [no frontmatter — skip]")
                continue

            changed = False
            for key in ("needs_update", "stale_since", "reason"):
                if key in fm:
                    del fm[key]
                    changed = True

            if not changed:
                print(f"  ✅ {sp.name}  [already clear]")
                continue

            if fm:
                new_text = render_frontmatter(fm) + "\n" + body
            else:
                # Remove empty frontmatter entirely
                new_text = body.lstrip("\n")

            sp.write_text(new_text, encoding="utf-8")
            print(f"  🧹 {sp.name}  [cleared]")


def action_list(repo: Path) -> list[SynthesisStatus]:
    """List all synthesis pages with their freshness status."""
    results: list[SynthesisStatus] = []
    for topic_dir in discover_topics(repo):
        yamls = discover_paper_yamls(topic_dir)
        print(f"\n📂 {topic_dir.name}/synthesis/")
        for sp in discover_synthesis_pages(topic_dir):
            st = check_freshness(sp, topic_dir, yamls)
            results.append(st)

            icon = "⚠️ " if st.is_stale else "✅"
            mtime = mtime_to_datestr(file_mtime(sp))
            fm_mark = ""
            if st.frontmatter and st.frontmatter.get("needs_update") == "true":
                fm_mark = " [frontmatter: needs_update]"

            print(f"  {icon} {sp.name}  (mtime: {mtime}){fm_mark}")
            print(f"      node refs: {len(st.node_ids_referenced)}  "
                  f"yaml refs: {len(st.yaml_refs)}  "
                  f"newer papers: {len(st.newer_yamls)}")
            if st.newer_yamls:
                print(f"      → {', '.join(st.newer_yamls[:10])}"
                      f"{'…' if len(st.newer_yamls) > 10 else ''}")

    print()
    stale = sum(1 for s in results if s.is_stale)
    print(f"Total: {len(results)} page(s), {stale} stale")
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Track synthesis page freshness in sci-logic-kb.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--repo-path", type=str, default=None,
        help="Path to repository root (auto-detected if omitted).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--check", action="store_true", default=False,
        help="Report freshness status (default action).",
    )
    group.add_argument(
        "--mark", action="store_true", default=False,
        help="Add/update needs_update frontmatter on stale pages.",
    )
    group.add_argument(
        "--clear", action="store_true", default=False,
        help="Remove needs_update marks from all synthesis pages.",
    )
    group.add_argument(
        "--list", action="store_true", default=False,
        help="List all synthesis pages with detailed status.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo = find_repo_root(args.repo_path)
    if not (repo / "topics").is_dir():
        print(f"Error: {repo}/topics not found. Use --repo-path.", file=sys.stderr)
        return 1

    # Default action is --check
    if not any([args.check, args.mark, args.clear, args.list]):
        args.check = True

    if args.mark:
        results = action_mark(repo)
    elif args.clear:
        action_clear(repo)
        return 0
    elif args.list:
        results = action_list(repo)
    else:
        results = action_check(repo)

    # Exit code: 1 if any stale
    return 1 if any(s.is_stale for s in results) else 0


if __name__ == "__main__":
    sys.exit(main())
