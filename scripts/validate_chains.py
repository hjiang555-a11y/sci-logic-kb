#!/usr/bin/env python3
"""validate_chains.py — Verify v5.0 reasoning chain integrity against v4.5 data.

Checks:
1. All evidence relation_ids in chains exist in v4.5 YAML
2. All consensus paper references resolve to actual YAML files
3. All limiting principles in chains are defined in v4.5
4. Chain edges reference valid principles
5. Data freshness (chain date vs YAML modification dates)
"""
import os, sys, yaml, argparse, glob
from datetime import datetime

def parse_args():
    p = argparse.ArgumentParser(description="Validate v5.0 reasoning chains")
    p.add_argument("--repo-path", default=".", help="Repository root")
    p.add_argument("--chain", default=None, help="Validate specific chain file")
    p.add_argument("--strict", action="store_true", help="Warnings are errors")
    return p.parse_args()

def collect_v4_relations(repo_path):
    """Collect all relation IDs from v4.5 YAML files."""
    relations = {}
    papers_dir = os.path.join(repo_path, "topics")
    for root, dirs, files in os.walk(papers_dir):
        for f in files:
            if not f.endswith('.yaml'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    data = yaml.safe_load(fh)
            except Exception:
                continue
            if not data:
                continue
            for rel in data.get('relations', []):
                rid = rel.get('id', '')
                if rid:
                    relations[rid] = path
    return relations

def collect_v4_nodes(repo_path):
    """Collect all node IDs from v4.5 YAML files."""
    nodes = {}
    papers_dir = os.path.join(repo_path, "topics")
    for root, dirs, files in os.walk(papers_dir):
        for f in files:
            if not f.endswith('.yaml'):
                continue
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    data = yaml.safe_load(fh)
            except Exception:
                continue
            if not data:
                continue
            for section in ['entities', 'principles', 'methods', 'metrics']:
                items = data.get(section) or []
                for node in items:
                    nid = node.get('id', '')
                    if nid:
                        nodes[nid] = path
    return nodes

def collect_paper_files(repo_path):
    """Collect all paper YAML files."""
    papers = {}
    papers_dir = os.path.join(repo_path, "topics")
    for root, dirs, files in os.walk(papers_dir):
        for f in files:
            if not f.endswith('.yaml'):
                continue
            papers[f] = os.path.join(root, f)
    return papers

def validate_chain(chain_path, relations, nodes, papers):
    """Validate a single chain file."""
    results = {'file': chain_path, 'errors': [], 'warnings': []}
    
    try:
        with open(chain_path) as f:
            chain = yaml.safe_load(f)
    except Exception as e:
        results['errors'].append(f"Cannot parse chain file: {e}")
        return results
    
    if not chain:
        results['errors'].append("Empty chain file")
        return results
    
    chain_id = chain.get('chain_id', os.path.basename(chain_path))

    for field in ['chain_id', 'question', 'limiting_principle', 'evidence']:
        if not chain.get(field):
            results['errors'].append(f"Missing required field: {field}")

    lp = chain.get('limiting_principle', {})
    if isinstance(lp, dict):
        lp_id = lp.get('id', '')
        if lp_id and lp_id.startswith('pri.') and lp_id not in nodes:
                results['errors'].append(f"Limiting principle '{lp_id}' not found in v4.5 nodes")

    for ev in chain.get('evidence', []):
        rid = ev.get('relation_id', '')
        if not rid:
            results['errors'].append(f"Evidence entry missing relation_id")
        elif rid not in relations:
                results['errors'].append(f"Evidence reference '{rid}' not found in any v4.5 YAML")

    for edge in chain.get('edges', []):
        for key in ['from', 'to']:
            node_ref = edge.get(key, '')
            if node_ref.startswith('pri.') and node_ref not in nodes:
                results['warnings'].append(f"Edge reference '{node_ref}' not found in v4.5 (may be descriptive)")

    last_updated = chain.get('last_updated', '')
    if last_updated:
        try:
            if isinstance(last_updated, str):
                chain_date = datetime.strptime(last_updated, '%Y-%m-%d').date()
            elif hasattr(last_updated, 'date'):
                chain_date = last_updated.date() if hasattr(last_updated, 'date') else last_updated
            else:
                chain_date = last_updated
            for ev in chain.get('evidence', []):
                rid = ev.get('relation_id', '')
                if rid in relations:
                    yaml_date = datetime.fromtimestamp(os.path.getmtime(relations[rid])).date()
                    if isinstance(chain_date, type(yaml_date)) and yaml_date > chain_date:
                        results['warnings'].append(
                            f"Evidence {rid} modified ({yaml_date.date()}) after chain update ({chain_date.date()})"
                        )
        except ValueError:
            pass
    
    return results

def validate_consensus(consensus_path, papers):
    """Validate a consensus report."""
    results = {'file': consensus_path, 'errors': [], 'warnings': []}
    
    try:
        with open(consensus_path) as f:
            cs = yaml.safe_load(f)
    except Exception as e:
        results['errors'].append(f"Cannot parse consensus file: {e}")
        return results
    
    if not cs:
        results['errors'].append("Empty consensus file")
        return results
    
    for field in ['metric', 'consensus', 'timeline']:
        if not cs.get(field):
            results['errors'].append(f"Missing required field: {field}")
    
    for entry in cs.get('timeline', []):
        paper = entry.get('paper', '')
        if paper:
            yaml_name = f"{paper}.yaml"
            if yaml_name not in papers:
                yaml_name_alt = f"{paper}"
                found = any(yaml_name_alt in p for p in papers)
                if not found:
                    results['warnings'].append(f"Timeline paper '{paper}' not found as YAML file")
    
    return results

def main():
    args = parse_args()
    repo = os.path.abspath(args.repo_path)
    
    print("Collecting v4.5 data...")
    relations = collect_v4_relations(repo)
    nodes = collect_v4_nodes(repo)
    papers = collect_paper_files(repo)
    print(f"  Relations: {len(relations)}")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Papers: {len(papers)}")
    
    all_results = []
    total_errors = 0
    total_warnings = 0
    
    chains_dir = os.path.join(repo, "logic", "chains")
    chain_files = [args.chain] if args.chain else glob.glob(os.path.join(chains_dir, "*.yaml"))
    
    for cf in chain_files:
        if not cf or not os.path.exists(cf):
            continue
        print(f"\nValidating chain: {os.path.basename(cf)}")
        r = validate_chain(cf, relations, nodes, papers)
        all_results.append(r)
        for e in r['errors']:
            print(f"  ❌ ERROR: {e}")
            total_errors += 1
        for w in r['warnings']:
            print(f"  ⚠  WARNING: {w}")
            total_warnings += 1
        if not r['errors'] and not r['warnings']:
            print(f"  ✅ All checks passed")
    
    # Validate consensus
    consensus_dir = os.path.join(repo, "consensus")
    for cf in glob.glob(os.path.join(consensus_dir, "*.yaml")):
        print(f"\nValidating consensus: {os.path.basename(cf)}")
        r = validate_consensus(cf, papers)
        all_results.append(r)
        for e in r['errors']:
            print(f"  ❌ ERROR: {e}")
            total_errors += 1
        for w in r['warnings']:
            print(f"  ⚠  WARNING: {w}")
            total_warnings += 1
        if not r['errors'] and not r['warnings']:
            print(f"  ✅ All checks passed")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: {total_errors} errors, {total_warnings} warnings ({len(all_results)} files)")
    
    if args.strict and total_warnings > 0:
        print("❌ FAIL (strict mode)")
        return 1
    
    if total_errors > 0:
        print("❌ FAIL")
        return 1
    
    print("✅ PASS")
    return 0

if __name__ == '__main__':
    sys.exit(main())
