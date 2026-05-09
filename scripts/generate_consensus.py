#!/usr/bin/env python3
"""generate_consensus.py — Generate consensus report drafts from v4.5 data and v5.0 evidence registry.

Reads topic YAML files, extracts metrics with demonstrated_values across papers,
constructs timelines, identifies best values, and outputs consensus report drafts.
"""
import os, sys, yaml, argparse, glob
from collections import defaultdict
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="Generate v5.0 consensus reports from v4.5 data")
    p.add_argument("--repo-path", default=".", help="Repository root")
    p.add_argument("--topic", required=True, help="Topic name")
    p.add_argument("--output-dir", default=None, help="Output directory (default: consensus/)")
    p.add_argument("--dry-run", action="store_true", help="Preview only, don't write files")
    return p.parse_args()

def load_evidence_registry(repo_path, topic):
    path = os.path.join(repo_path, "evidence", f"registry_{topic}.yaml")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f)

def extract_metric_timeline(repo_path, topic):
    topic_dir = os.path.join(repo_path, "topics", topic, "papers")
    if not os.path.isdir(topic_dir):
        return {}

    metrics = defaultdict(list)

    for fname in sorted(os.listdir(topic_dir)):
        if not fname.endswith('.yaml'):
            continue
        path = os.path.join(topic_dir, fname)
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not data:
            continue

        meta = data.get('meta', {})
        year = meta.get('year', '')
        author = meta.get('first_author', '')
        title = meta.get('title', '')

        for m in data.get('metrics', []):
            mid = m.get('id', '')
            name = m.get('name', '')
            unit = m.get('unit', '')
            role = m.get('role', '')

            dv = m.get('demonstrated_value', {})
            if not isinstance(dv, dict):
                continue
            value = dv.get('value', '')
            conditions = dv.get('conditions', '')
            verification = dv.get('verification_status', '')
            confidence = dv.get('confidence', '')
            src = dv.get('source', {})

            if not value:
                continue

            entry = {
                'metric_id': mid,
                'metric_name': name,
                'unit': unit,
                'value': str(value)[:200],
                'conditions': str(conditions)[:200] if conditions else '',
                'year': year,
                'author': author,
                'paper': fname,
                'paper_title': str(title)[:200],
                'role': role,
                'verification': verification,
                'confidence': confidence,
                'claim': str(src.get('claim', ''))[:200] if isinstance(src, dict) else '',
            }
            metrics[mid].append(entry)

    return dict(metrics)

def select_key_metrics(metrics, registry, topic):
    selected = {}

    is_primary = lambda m: m.get('role') == 'primary'
    is_stability_related = lambda m: any(kw in str(m.get('metric_name', '')).lower() + str(m.get('metric_id', '')).lower()
        for kw in ['σ_y', 'allan', 'instability', 'stability', 'fractional',
                   'uncertainty', 'accuracy', 'linewidth', 'phase_noise',
                   'frequency_noise', 'transfer', 'link', 'drift',
                   'noise', 'loss_angle', 'sensitivity', 'bandwidth',
                   'coherence', 'jitter', 'clock'])

    for mid, entries in metrics.items():
        entries_with_year = sorted([e for e in entries if e['year']], key=lambda e: e['year'])

        if len(entries_with_year) < 2:
            continue

        has_primary = any(is_primary(e) for e in entries)
        is_interesting = is_stability_related(entries[0])

        if has_primary or is_interesting:
            selected[mid] = entries_with_year

    if len(selected) < 3:
        by_count = sorted(metrics.items(), key=lambda x: -len(x[1]))
        for mid, entries in by_count:
            if mid not in selected:
                entries_with_year = sorted([e for e in entries if e['year']], key=lambda e: e['year'])
                if len(entries_with_year) >= 2:
                    selected[mid] = entries_with_year
            if len(selected) >= 5:
                break

    return selected

def build_consensus_report(metric_id, entries, topic):
    newest = max(entries, key=lambda e: e['year'])
    best_value = newest['value']
    best_system = f"{newest.get('author','?')} {newest.get('year','')}"

    timeline = []
    for e in sorted(entries, key=lambda e: e['year']):
        timeline.append({
            'year': e['year'],
            'value': e['value'][:120],
            'system': f"{e.get('author','?')} {e.get('year','')}",
            'paper': e['paper'],
            'note': e.get('conditions', '')[:120],
        })

    report = {
        'metric': metric_id,
        'metric_name': entries[0].get('metric_name', ''),
        'context': f"{entries[0].get('metric_name','')} — auto-generated consensus draft",
        'domain': topic,
        'updated': datetime.utcnow().strftime('%Y-%m-%d'),
        'confidence': 'draft',
        'consensus': {
            'best_demonstrated_value': best_value,
            'best_demonstrated_system': best_system,
            'best_demonstrated_paper': newest['paper'],
            'best_demonstrated_conditions': newest.get('conditions', ''),
            'data_points': len(entries),
            'year_range': f"{entries[0]['year']}-{entries[-1]['year']}",
        },
        'timeline': timeline,
    }

    return report

def main():
    args = parse_args()
    repo = args.repo_path
    topic = args.topic
    output_dir = args.output_dir or os.path.join(repo, "consensus")

    print(f"Scanning topic: {topic}")
    metrics = extract_metric_timeline(repo, topic)
    print(f"  Found {len(metrics)} metrics with demonstrated values")

    registry = load_evidence_registry(repo, topic)

    selected = select_key_metrics(metrics, registry, topic)
    print(f"  Selected {len(selected)} key metrics for consensus reports")

    os.makedirs(output_dir, exist_ok=True)

    generated = 0
    for mid, entries in sorted(selected.items()):
        report = build_consensus_report(mid, entries, topic)

        safe_name = mid.replace('.', '_').replace(' ', '_')
        outpath = os.path.join(output_dir, f"{safe_name}.yaml")

        if not args.dry_run:
            with open(outpath, 'w') as f:
                yaml.dump(report, f, allow_unicode=True, sort_keys=False, width=200,
                          default_flow_style=False)
            print(f"  Wrote: {os.path.basename(outpath)} ({len(entries)} data points, {report['consensus']['year_range']})")
        else:
            print(f"  [DRY RUN] {safe_name}: {len(entries)} data points, {report['consensus']['year_range']}")

        generated += 1

    print(f"\nGenerated {generated} consensus report drafts for {topic}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
