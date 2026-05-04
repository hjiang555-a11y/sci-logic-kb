#!/usr/bin/env python3
"""Historical trend tracking for KB quality metrics.

Records snapshots of lint/stats outputs and shows deltas over time.

Usage:
  python scripts/trend.py --record       # append current snapshot
  python scripts/trend.py --show -n 5    # show last 5 snapshots with deltas
  python scripts/trend.py --json         # machine-readable output
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = REPO / "reports" / "active" / "trend_snapshots.json"


def _take_snapshot() -> dict:
    """Run lint + stats and return a snapshot dict."""
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "lint.py"), "--summary"],
        capture_output=True, text=True, cwd=str(REPO)
    )
    output = result.stdout + result.stderr
    # Parse lint summary line: "Summary: N error(s), M warning(s), I info across C categories"
    lint_errs, lint_warns, lint_infos = 0, 0, 0
    for line in output.splitlines():
        if "Summary:" in line and "error" in line:
            import re
            m = re.search(r"(\d+) error\(s\), (\d+) warning\(s\), (\d+) info", line)
            if m:
                lint_errs, lint_warns, lint_infos = int(m.group(1)), int(m.group(2)), int(m.group(3))

    # Run stats
    sys.path.insert(0, str(REPO / "scripts"))
    import stats as st
    data = st.analyse(REPO)
    rr = data["reasoning_readiness"]

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lint_errors": lint_errs,
        "lint_warnings": lint_warns,
        "lint_infos": lint_infos,
        "chain_closure_pct": round(rr["reasoning_chain_closure"]["rate"] * 100, 1),
        "evidence_coverage_pct": round(rr["evidence_coverage"]["rate"] * 100, 1),
        "condition_completeness_pct": round(rr["condition_completeness"]["rate"] * 100, 1),
        "synthesis_topics": f"{rr['synthesis_coverage']['topics_with_synthesis']}/{rr['synthesis_coverage']['topics_with_papers']}",
        "total_papers": data["inventory"]["total_papers"],
        "total_nodes": data["inventory"]["total_nodes"],
        "total_relations": data["inventory"]["total_relations"],
    }


def _load_snapshots() -> list[dict]:
    if not SNAPSHOT_FILE.exists():
        return []
    with open(SNAPSHOT_FILE) as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def _save_snapshots(snapshots: list[dict]):
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshots, f, indent=2)


def _delta(a_val, b_val):
    """Return string representation of delta between two numeric values."""
    if isinstance(a_val, str) or isinstance(b_val, str):
        return ""
    try:
        diff = b_val - a_val
    except (TypeError, ValueError):
        return ""
    if diff == 0:
        return "= "
    arrow = "↑" if diff > 0 else "↓"
    return f"{arrow}{abs(diff)}"


def _show_trend(snapshots: list[dict], n: int):
    """Display the last N snapshots with deltas from the first in the window."""
    if not snapshots:
        print("No snapshots recorded yet. Run `trend.py --record` first.")
        return
    window = snapshots[-n:] if n > 0 else snapshots
    if len(window) < 2:
        for s in window:
            print(f"  [{s['timestamp'][:19]}]  errors={s['lint_errors']}  chain_closure={s['chain_closure_pct']}%  "
                  f"papers={s['total_papers']}")
        print("\n(Only 1 snapshot — no deltas to show.)")
        return

    base = window[0]
    print(f"{'Date':<12} {'Errors':>7} {'Warns':>7} {'Chain%':>7} {'Evid%':>6} {'Synth':>6} {'Papers':>7}")
    print("-" * 58)
    for s in window:
        ts = s["timestamp"][:10]
        errs = f"{s['lint_errors']} {_delta(base['lint_errors'], s['lint_errors']):>4}"
        warns = f"{s['lint_warnings']} {_delta(base['lint_warnings'], s['lint_warnings']):>4}"
        chain = f"{s['chain_closure_pct']} {_delta(base['chain_closure_pct'], s['chain_closure_pct']):>4}"
        evid = f"{s['evidence_coverage_pct']} {_delta(base['evidence_coverage_pct'], s['evidence_coverage_pct']):>4}"
        synth = f"{s['synthesis_topics']}"
        papers = f"{s['total_papers']} {_delta(base['total_papers'], s['total_papers']):>4}"
        print(f"{ts:<12} {errs:>7} {warns:>7} {chain:>7} {evid:>6} {synth:>6} {papers:>7}")


def _parse_args():
    p = argparse.ArgumentParser(description="KB quality trend tracking")
    p.add_argument("--record", action="store_true", help="Append a new snapshot")
    p.add_argument("--show", action="store_true", help="Display recent trend")
    p.add_argument("-n", type=int, default=10, help="Number of recent snapshots to show (default 10)")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    return p.parse_args()


def main():
    args = _parse_args()

    if args.record:
        snapshots = _load_snapshots()
        snap = _take_snapshot()
        snapshots.append(snap)
        _save_snapshots(snapshots)
        if args.json:
            print(json.dumps({"recorded": snap}, indent=2))
        else:
            print(f"Recorded snapshot: {snap['timestamp'][:19]}  "
                  f"errors={snap['lint_errors']}  chain_closure={snap['chain_closure_pct']}%  "
                  f"papers={snap['total_papers']}")
        return

    if args.show or args.json:
        snapshots = _load_snapshots()
        if args.json:
            print(json.dumps(snapshots[-args.n:] if args.n > 0 else snapshots, indent=2))
        else:
            _show_trend(snapshots, args.n)
        return

    # Default: show if no flags
    snapshots = _load_snapshots()
    _show_trend(snapshots, args.n)


if __name__ == "__main__":
    main()
