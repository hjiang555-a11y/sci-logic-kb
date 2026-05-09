#!/usr/bin/env python3
"""build_evidence_index.py — Extract atomic evidence from v4.5 YAML relations.

Reads paper YAML files from a topic, extracts BOUNDED-BY relations as atomic
evidence units, groups by limiting principle, and writes evidence/registry_{topic}.yaml.
"""
import os, sys, yaml, argparse
from collections import defaultdict
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="Build v5.0 evidence index from v4.5 YAML")
    p.add_argument("--repo-path", default=".", help="Repository root")
    p.add_argument("--topic", required=True, help="Topic name (e.g., ultrastable-laser)")
    p.add_argument("--output-dir", default=None, help="Output directory (default: evidence/)")
    return p.parse_args()

def load_yaml(path):
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception:
        return None

def extract_evidence(topic_dir):
    """Scan topic YAML files and extract atomic evidence from relations."""
    papers_dir = os.path.join(topic_dir, "papers")
    stats = {
        'total_papers': 0,
        'papers_with_relations': 0,
        'total_relations': 0,
        'bounded_by_count': 0,
        'with_breakthrough_paths': 0,
        'with_limit_status': 0,
    }
    if not os.path.isdir(papers_dir):
        print(f"ERROR: papers directory not found at {papers_dir}")
        return [], {}, stats

    yaml_files = sorted([f for f in os.listdir(papers_dir) if f.endswith('.yaml')])

    evidence_list = []
    stats['total_papers'] = len(yaml_files)
    by_principle = defaultdict(list)

    for fname in yaml_files:
        path = os.path.join(papers_dir, fname)
        data = load_yaml(path)
        if not data:
            continue

        meta = data.get('meta', {})
        relations = data.get('relations', [])
        if not relations:
            continue

        stats['papers_with_relations'] += 1

        for rel in relations:
            stats['total_relations'] += 1
            pred = rel.get('predicate', '')

            if pred != 'BOUNDED-BY':
                continue

            stats['bounded_by_count'] += 1
            src = rel.get('source', {})
            bt_paths = rel.get('breakthrough_paths', [])

            if bt_paths:
                stats['with_breakthrough_paths'] += 1
            if rel.get('limit_status'):
                stats['with_limit_status'] += 1

            ev = {
                'relation_id': rel.get('id'),
                'paper_file': fname,
                'paper_title': meta.get('title', ''),
                'first_author': meta.get('first_author', ''),
                'year': meta.get('year', ''),
                'zotero_key': meta.get('zotero_key', ''),
                'contribution_type': meta.get('contribution_type', 'evidence'),
                'subject': rel.get('subject', ''),
                'object': rel.get('object', ''),
                'claim': src.get('claim', ''),
                'is_system_limit': rel.get('is_system_limit'),
                'limit_status': rel.get('limit_status'),
                'regime': rel.get('regime', ''),
                'quantitative_contribution': rel.get('quantitative_contribution', ''),
                'verification_status': rel.get('verification_status', ''),
                'confidence': rel.get('confidence', ''),
                'breakthrough_paths': [],
            }

            for bp in bt_paths:
                ev['breakthrough_paths'].append({
                    'direction': bp.get('direction', ''),
                    'expected_gain': bp.get('expected_gain', ''),
                    'status': bp.get('status', ''),
                    'source': bp.get('source', {}),
                })

            evidence_list.append(ev)
            by_principle[ev['object']].append(ev)

    return evidence_list, by_principle, stats

def build_registry(evidence_list, by_principle, topic):
    """Build the evidence registry by grouping evidence by limiting principle."""
    registry = {
        'topic': topic,
        'generated': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
        'schema_version': 'v5.0-evidence',
        'summary': {},
        'evidence_groups': [],
    }

    total_ev = len(evidence_list)
    total_bt = sum(1 for e in evidence_list if e['breakthrough_paths'])
    total_resolved = sum(1 for e in evidence_list if e['limit_status'] == 'resolved')
    total_active = sum(1 for e in evidence_list if e['limit_status'] == 'active')

    registry['summary'] = {
        'total_evidence_units': total_ev,
        'unique_limiting_principles': len(by_principle),
        'with_breakthrough_paths': total_bt,
        'with_resolved_limits': total_resolved,
        'with_active_limits': total_active,
    }

    for principle_id, ev_list in sorted(by_principle.items(), key=lambda x: -len(x[1])):
        papers = sorted(set(e['paper_file'] for e in ev_list))
        years = sorted(set(str(e['year']) for e in ev_list if e['year']))
        authors = sorted(set(e['first_author'] for e in ev_list if e['first_author']))

        best = None
        for e in ev_list:
            if e['contribution_type'] == 'breakthrough' and e['is_system_limit']:
                best = e
                break
        if not best:
            for e in ev_list:
                if e['is_system_limit']:
                    best = e
                    break
        if not best:
            best = ev_list[0]

        all_bt = []
        for e in ev_list:
            for bp in e['breakthrough_paths']:
                if bp['direction'] not in [b['direction'] for b in all_bt]:
                    all_bt.append(bp)

        group = {
            'limiting_principle': principle_id,
            'supporting_papers': len(papers),
            'paper_list': papers,
            'year_range': f"{min(years)}-{max(years)}" if years else '',
            'first_authors': authors,
            'best_evidence': {
                'paper': best['paper_file'],
                'author': best['first_author'],
                'year': best['year'],
                'claim': best['claim'][:200],
                'is_system_limit': best['is_system_limit'],
                'limit_status': best['limit_status'],
            },
            'breakthrough_paths': all_bt,
            'evidence_units': [
                {
                    'relation_id': e['relation_id'],
                    'paper': e['paper_file'],
                    'author': e['first_author'],
                    'year': e['year'],
                    'is_system_limit': e['is_system_limit'],
                    'limit_status': e['limit_status'],
                    'verification': e['verification_status'],
                    'claim': e['claim'][:200],
                }
                for e in ev_list
            ],
        }
        registry['evidence_groups'].append(group)

    return registry

def main():
    args = parse_args()
    repo_path = os.path.abspath(args.repo_path)
    topic_dir = os.path.join(repo_path, "topics", args.topic)
    output_dir = args.output_dir or os.path.join(repo_path, "evidence")

    print(f"Scanning: {topic_dir}")
    evidence_list, by_principle, stats = extract_evidence(topic_dir)

    print(f"\n=== Scan Results ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    if not evidence_list:
        print("\nNo BOUNDED-BY relations found. Nothing to index.")
        return 1 if stats['total_papers'] == 0 else 0

    registry = build_registry(evidence_list, by_principle, args.topic)

    os.makedirs(output_dir, exist_ok=True)
    outpath = os.path.join(output_dir, f"registry_{args.topic}.yaml")
    with open(outpath, 'w') as f:
        yaml.dump(registry, f, allow_unicode=True, sort_keys=False, width=200,
                  default_flow_style=False)

    print(f"\nEvidence registry written to: {outpath}")
    print(f"  Evidence groups: {len(registry['evidence_groups'])}")
    print(f"  Total evidence units: {registry['summary']['total_evidence_units']}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
