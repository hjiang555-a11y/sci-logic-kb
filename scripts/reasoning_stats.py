#!/usr/bin/env python3
"""reasoning_stats.py — v5.0 reasoning readiness metrics for the three-layer architecture.

Extends stats.py with v5.0-specific metrics:
1. Chain coverage per topic
2. Evidence freshness
3. Consensus completeness
4. Cross-chain connectivity
5. Evidence-to-chain link density
"""
import os, sys, yaml, argparse, glob
from collections import defaultdict
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="v5.0 reasoning readiness metrics")
    p.add_argument("--repo-path", default=".", help="Repository root")
    p.add_argument("--json", action="store_true", help="JSON output")
    return p.parse_args()

def count_chains(repo_path):
    chains_dir = os.path.join(repo_path, "logic", "chains")
    chains = {}
    for cf in glob.glob(os.path.join(chains_dir, "*.yaml")):
        try:
            with open(cf) as f:
                chain = yaml.safe_load(f)
            if chain:
                cid = chain.get('chain_id', os.path.basename(cf))
                domain = chain.get('domain', 'unknown')
                ev_count = len(chain.get('evidence', []))
                edge_count = len(chain.get('edges', []))
                confidence = chain.get('confidence', 'unknown')
                chains[cid] = {
                    'domain': domain,
                    'evidence_count': ev_count,
                    'edge_count': edge_count,
                    'confidence': confidence,
                    'file': os.path.basename(cf),
                }
        except Exception:
            pass
    return chains

def count_evidence_registries(repo_path):
    ev_dir = os.path.join(repo_path, "evidence")
    registries = {}
    for rf in glob.glob(os.path.join(ev_dir, "registry_*.yaml")):
        try:
            with open(rf) as f:
                reg = yaml.safe_load(f)
            if reg:
                topic = reg.get('topic', 'unknown')
                summary = reg.get('summary', {})
                registries[topic] = {
                    'evidence_units': summary.get('total_evidence_units', 0),
                    'limiting_principles': summary.get('unique_limiting_principles', 0),
                    'with_breakthrough_paths': summary.get('with_breakthrough_paths', 0),
                }
        except Exception:
            pass
    return registries

def count_consensus(repo_path):
    cs_dir = os.path.join(repo_path, "consensus")
    reports = []
    for cf in glob.glob(os.path.join(cs_dir, "*.yaml")):
        try:
            with open(cf) as f:
                cs = yaml.safe_load(f)
            if cs:
                reports.append({
                    'metric': cs.get('metric', 'unknown'),
                    'domain': cs.get('domain', 'unknown'),
                    'confidence': cs.get('confidence', 'unknown'),
                    'timeline_entries': len(cs.get('timeline', [])),
                })
        except Exception:
            pass
    return reports

def check_references(repo_path):
    topics_dir = os.path.join(repo_path, "topics")
    topics = [d for d in os.listdir(topics_dir) if os.path.isdir(os.path.join(topics_dir, d)) and d != 'shared']

    v4_stats = {}
    for topic in topics:
        papers_dir = os.path.join(topics_dir, topic, "papers")
        paper_count = len([f for f in os.listdir(papers_dir) if f.endswith('.yaml')])
        v4_stats[topic] = {'papers': paper_count}

    chains = count_chains(repo_path)
    registries = count_evidence_registries(repo_path)

    chain_by_domain = defaultdict(list)
    for cid, info in chains.items():
        chain_by_domain[info['domain']].append(cid)

    return v4_stats, chains, chain_by_domain, registries

def main():
    args = parse_args()
    repo = os.path.abspath(args.repo_path)

    v4_stats, chains, chain_by_domain, registries = check_references(repo)
    consensus_reports = count_consensus(repo)

    if args.json:
        import json
        result = {
            'chains': {k: v for k, v in chains.items()},
            'consensus_reports': consensus_reports,
            'registries': registries,
            'metrics': {
                'total_chains': len(chains),
                'total_consensus': len(consensus_reports),
                'total_registries': len(registries),
            }
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print("=" * 60)
    print("  sci-logic-kb v5.0  ·  Reasoning Readiness Metrics")
    print("=" * 60)

    print(f"\n  Chain Coverage")
    print(f"    Total chains: {len(chains)}")
    for domain, cids in sorted(chain_by_domain.items()):
        print(f"    {domain}: {len(cids)} chains — {', '.join(cids)}")

    print(f"\n  Evidence Registries")
    print(f"    Total registries: {len(registries)}")
    for topic, info in sorted(registries.items()):
        print(f"    {topic}: {info['evidence_units']} units, {info['limiting_principles']} principles, {info['with_breakthrough_paths']} with bt_paths")

    print(f"\n  Consensus Reports")
    print(f"    Total reports: {len(consensus_reports)}")
    for r in consensus_reports:
        print(f"    {r['metric']}: {r['timeline_entries']} timeline entries ({r['confidence']})")

    total_evidence = sum(r['evidence_count'] for r in chains.values())
    total_bt = sum(r['with_breakthrough_paths'] for r in registries.values())
    total_units = sum(r['evidence_units'] for r in registries.values())

    print(f"\n  Cross-Layer Metrics")
    print(f"    Chain-to-evidence link density: {total_evidence}/{total_units} ({100*total_evidence//max(1,total_units)}%)")
    print(f"    Breakthrough path ratio: {total_bt}/{total_units} ({100*total_bt//max(1,total_units)}%)")
    print(f"    Consensus coverage: {len(consensus_reports)}/{len(chain_by_domain)} domains")

    return 0

if __name__ == '__main__':
    sys.exit(main())
