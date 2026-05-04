#!/usr/bin/env python3
"""Unified KB health check — runs lint + stats + freshness in one pass.

Usage:
  python scripts/health.py              # full check
  python scripts/health.py --quick      # skip slow freshness git-log checks
  python scripts/health.py --json       # machine-readable output
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _import_lint():
    sys.path.insert(0, str(REPO / "scripts"))
    import lint
    return lint


def _import_stats():
    sys.path.insert(0, str(REPO / "scripts"))
    import stats as st
    return st


def _run_lint(yaml_paths, repo):
    lint = _import_lint()
    issues = lint.run_all_checks(yaml_paths, repo)
    by_level = Counter(i.level for i in issues)
    return by_level.get("ERROR", 0), by_level.get("WARNING", 0), by_level.get("INFO", 0)


def _run_stats(repo):
    st = _import_stats()
    data = st.analyse(repo)
    rr = data["reasoning_readiness"]
    return {
        "chain_closure": round(rr["reasoning_chain_closure"]["rate"] * 100, 1),
        "chain_closure_target": round(rr["reasoning_chain_closure"]["target"] * 100, 1),
        "chain_closure_pass": rr["reasoning_chain_closure"]["rate"] >= rr["reasoning_chain_closure"]["target"],
        "evidence_coverage": round(rr["evidence_coverage"]["rate"] * 100, 1),
        "evidence_coverage_pass": rr["evidence_coverage"]["rate"] >= rr["evidence_coverage"]["target"],
        "condition_completeness": round(rr["condition_completeness"]["rate"] * 100, 1),
        "condition_completeness_pass": rr["condition_completeness"]["rate"] >= rr["condition_completeness"]["target"],
        "synthesis_coverage": f"{rr['synthesis_coverage']['topics_with_synthesis']}/{rr['synthesis_coverage']['topics_with_papers']}",
        "synthesis_pass": rr["synthesis_coverage"]["topics_with_synthesis"] == rr["synthesis_coverage"]["topics_with_papers"],
        "total_papers": data["inventory"]["total_papers"],
        "total_nodes": data["inventory"]["total_nodes"],
        "total_relations": data["inventory"]["total_relations"],
    }


def _run_freshness(repo):
    import subprocess
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "freshness.py"), "check"],
        capture_output=True, text=True, cwd=str(repo)
    )
    output = result.stdout + result.stderr
    stale_count = output.count("STALE")
    fresh_count = output.count("fresh")
    return {"stale": stale_count, "fresh": fresh_count, "total": stale_count + fresh_count}


def _parse_args():
    p = argparse.ArgumentParser(description="Unified KB health check")
    p.add_argument("--quick", action="store_true", help="Skip freshness check (slow)")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    return p.parse_args()


def main():
    args = _parse_args()
    repo = REPO

    yaml_paths_raw = _import_lint().collect_yaml_paths(repo, None)
    lint_errors, lint_warnings, lint_infos = _run_lint(yaml_paths_raw, repo)
    stats = _run_stats(repo)

    if args.quick:
        fresh = None
    else:
        try:
            fresh = _run_freshness(repo)
        except Exception:
            fresh = None

    checks = {}
    checks["lint_errors"] = {"value": lint_errors, "pass": lint_errors == 0, "label": "Lint errors"}
    checks["lint_warnings"] = {"value": lint_warnings, "pass": True, "label": "Lint warnings"}  # always informational
    checks["chain_closure"] = {"value": f"{stats['chain_closure']}%", "pass": stats["chain_closure_pass"],
                                "label": f"Chain closure (target ≥{stats['chain_closure_target']}%)"}
    checks["evidence_coverage"] = {"value": f"{stats['evidence_coverage']}%", "pass": stats["evidence_coverage_pass"],
                                    "label": "Evidence coverage"}
    checks["condition_completeness"] = {"value": f"{stats['condition_completeness']}%",
                                         "pass": stats["condition_completeness_pass"], "label": "Condition completeness"}
    checks["synthesis_coverage"] = {"value": stats["synthesis_coverage"], "pass": stats["synthesis_pass"],
                                     "label": "Synthesis coverage"}
    if fresh is not None:
        checks["freshness"] = {"value": f"{fresh['stale']}/{fresh['total']} stale",
                                "pass": fresh["stale"] == 0, "label": "Synthesis freshness"}

    passed = sum(1 for c in checks.values() if c["pass"])
    total = len(checks)

    if args.json:
        print(json.dumps({"passed": passed, "total": total, "checks": checks}, indent=2))
    else:
        print(f"kb health: {passed}/{total} checks passed")
        for key, c in checks.items():
            icon = "✅" if c["pass"] else "❌"
            print(f"  {icon} {c['label']}: {c['value']}")
        print()
        print(f"  inventory: {stats['total_papers']} papers, {stats['total_nodes']} nodes, {stats['total_relations']} relations")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
