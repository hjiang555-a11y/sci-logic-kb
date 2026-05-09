#!/usr/bin/env python3
"""discover_papers.py — Search arXiv for new papers, filter duplicates, generate review queue.

Primary: arXiv API (reliable, covers all physics)
Enrichment: CrossRef API (journal info for published versions)
Output: reports/active/paper_queue.md — human review queue

Usage:
  python scripts/discover_papers.py                    # All topics
  python scripts/discover_papers.py --topic ultrastable-laser
  python scripts/discover_papers.py --dry-run
"""
import os, sys, yaml, json, re, time, argparse, xml.etree.ElementTree as ET
import urllib.request, urllib.parse
from datetime import datetime
from collections import defaultdict

ARXIV_API = "http://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"

PRIORITY_JOURNALS = [
    'Nature', 'Nature Photonics', 'Nature Physics', 'Nature Communications',
    'Science', 'Science Advances', 'Physical Review Letters', 'Physical Review A',
    'Reviews of Modern Physics', 'Optica', 'Optics Letters', 'Optics Express',
    'Applied Physics Letters', 'Metrologia', 'Laser and Photonics Reviews',
    'Light: Science and Applications', 'New Journal of Physics',
]

TOPIC_QUERIES = {
    'ultrastable-laser': [
        'all:ultra-stable AND all:laser AND all:cavity AND (all:linewidth OR all:stability)',
        'all:optical AND all:reference AND all:cavity AND (all:thermal AND all:noise OR all:Brownian)',
        'all:crystalline AND all:coating AND (all:Brownian OR all:thermal)',
        'all:fiber AND all:delay AND all:laser AND all:frequency AND all:stabilization',
        'all:silicon AND all:cavity AND all:cryogenic AND all:frequency',
        'all:hollow AND all:core AND all:fiber AND all:thermal AND all:noise',
    ],
    'optical-frequency-combs': [
        'all:frequency AND all:comb AND (all:soliton OR all:Kerr OR all:microresonator)',
        'all:optical AND all:frequency AND all:division AND all:microwave',
        'all:dual-comb AND all:spectroscopy',
        'all:femtosecond AND all:comb AND (all:stabilization OR all:phase AND all:noise)',
        'all:electro-optic AND all:frequency AND all:comb',
    ],
    'frequency-standards': [
        'all:optical AND all:clock AND (all:uncertainty OR all:stability OR all:systematic)',
        'all:optical AND all:lattice AND all:clock AND (all:strontium OR all:ytterbium)',
        'all:nuclear AND all:clock AND all:thorium',
        'all:ion AND all:clock AND (all:aluminium OR all:ytterbium OR all:calcium)',
    ],
    'time-frequency-transfer': [
        'all:optical AND all:frequency AND all:transfer AND all:fiber AND (all:link OR all:dissemination)',
        'all:free-space AND all:optical AND (all:time OR all:frequency) AND all:transfer',
        'all:hollow AND all:core AND all:fiber AND all:frequency AND all:transfer',
        'all:optical AND all:clock AND all:network AND (all:comparison OR all:synchronization)',
    ],
}

def search_arxiv(query, max_results=15):
    url = f"{ARXIV_API}?search_query={urllib.parse.quote(query)}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read().decode()
        root = ET.fromstring(data)
        ns = '{http://www.w3.org/2005/Atom}'
        papers = []
        for entry in root.findall(f'{ns}entry'):
            title = entry.find(f'{ns}title').text.strip().replace('\n',' ')
            summary = entry.find(f'{ns}summary').text.strip().replace('\n',' ')
            published = entry.find(f'{ns}published').text[:10]
            arxiv_id = entry.find(f'{ns}id').text.strip().split('/abs/')[-1]
            doi = ''
            comment = entry.find(f'{ns}comment')
            comment_text = (comment.text or '') if comment is not None else ''
            for link in entry.findall(f'{ns}link'):
                if link.get('title') == 'doi':
                    doi = link.get('href','').replace('http://dx.doi.org/','')
            authors = [a.find(f'{ns}name').text.strip() for a in entry.findall(f'{ns}author')]
            papers.append({
                'title': title, 'abstract': summary[:500], 'published': published,
                'year': published[:4], 'arxiv_id': arxiv_id, 'doi': doi,
                'authors': authors[:5], 'comment': comment_text[:200],
                'journal': '', 'is_priority': False, 'url': f'https://arxiv.org/abs/{arxiv_id}',
            })
        return papers
    except Exception as e:
        print(f"  arXiv ERROR: {e}")
        return []

def enrich_with_crossref(papers):
    for p in papers:
        if p['doi']: continue
        try:
            title_q = urllib.parse.quote(p['title'][:200])
            url = f"{CROSSREF_API}?query.title={title_q}&rows=1"
            req = urllib.request.Request(url, headers={"User-Agent": "sci-logic-kb/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
            items = data.get('message',{}).get('items',[])
            if items:
                p['doi'] = items[0].get('DOI','')
                p['journal'] = items[0].get('container-title',[''])[0] if items[0].get('container-title') else ''
        except: pass
        time.sleep(0.3)

def load_existing(repo_path):
    existing = {'titles': set(), 'dois': set()}
    for root, dirs, files in os.walk(os.path.join(repo_path, "topics")):
        for f in files:
            if not f.endswith('.yaml'): continue
            try:
                with open(os.path.join(root, f)) as fh: data = yaml.safe_load(fh)
            except: continue
            if not data: continue
            meta = data.get('meta',{})
            title = str(meta.get('title','')).lower().strip()
            doi = str(meta.get('doi','')).lower().strip()
            if title and title != 'untitled': existing['titles'].add(title[:80])
            if doi and len(doi)>10: existing['dois'].add(doi)
    return existing

def is_duplicate(paper, existing):
    title = paper['title'].lower().strip()[:80]
    if title in existing['titles']: return True
    if paper['doi'] and paper['doi'].lower() in existing['dois']: return True
    for et in existing['titles']:
        if len(title) > 40 and len(et) > 40 and (title[:50] in et or et[:50] in title): return True
    return False

def discover(repo_path, topic_filter=None):
    existing = load_existing(repo_path)
    print(f"Existing: {len(existing['titles'])} titles, {len(existing['dois'])} DOIs\n")
    
    all_candidates = defaultdict(list)
    topics = [topic_filter] if topic_filter else list(TOPIC_QUERIES.keys())
    
    for topic in topics:
        print(f"=== {topic} ===")
        seen = set()
        for q in TOPIC_QUERIES[topic][:4]:
            papers = search_arxiv(q)
            for p in papers:
                key = p['arxiv_id']
                if key in seen: continue
                seen.add(key)
                if is_duplicate(p, existing): continue
                all_candidates[topic].append(p)
            time.sleep(1.5)
        
        if all_candidates[topic]:
            print(f"  Enriching with CrossRef...")
            enrich_with_crossref(all_candidates[topic])
        
        for p in all_candidates[topic]:
            journal = p.get('journal','')
            p['is_priority'] = any(j in journal for j in PRIORITY_JOURNALS)
        
        all_candidates[topic].sort(key=lambda p: (-p['is_priority'], -int(p['year'])))
        priority = sum(1 for p in all_candidates[topic] if p['is_priority'])
        print(f"  Found: {len(all_candidates[topic])} ({priority} priority journals)")
    
    total = sum(len(v) for v in all_candidates.values())
    priority = sum(1 for v in all_candidates.values() for p in v if p['is_priority'])
    print(f"\nTotal: {total} candidates ({priority} from priority journals)")
    return all_candidates

def write_queue(candidates, repo_path, dry_run=False):
    now = datetime.utcnow().strftime('%Y-%m-%d')
    total = sum(len(v) for v in candidates.values())
    priority = sum(1 for v in candidates.values() for p in v if p['is_priority'])
    
    md = f"# Paper Review Queue\n\n"
    md += f"> Generated: {now} · Source: arXiv + CrossRef enrichment\n"
    md += f"> **{total} candidates** ({priority} from priority journals)\n\n"
    md += f"## Summary\n\n"
    for topic in sorted(candidates):
        c = len(candidates[topic])
        p = sum(1 for x in candidates[topic] if x['is_priority'])
        md += f"- **{topic}**: {c} ({p} priority)\n"
    
    for topic, papers in sorted(candidates.items()):
        if not papers: continue
        md += f"\n## {topic} ({len(papers)})\n\n"
        for p in papers:
            badge = '⭐' if p['is_priority'] else '📄'
            authors = ', '.join(p['authors'][:3])
            if len(p['authors']) > 3: authors += ' et al.'
            journal_str = f" · *{p['journal']}*" if p.get('journal') else f" (arXiv: {p['arxiv_id']})"
            md += f"### {badge} {p['title']}\n\n"
            md += f"- **{p['year']}**{journal_str}\n"
            md += f"- **Authors**: {authors}\n"
            if p['doi']: md += f"- **DOI**: [{p['doi']}](https://doi.org/{p['doi']})\n"
            md += f"- **arXiv**: [{p['arxiv_id']}](https://arxiv.org/abs/{p['arxiv_id']})\n"
            md += f"- **Status**: [ ] ✅ ingest / [ ] ❌ skip / [ ] ❓ unsure\n\n"
            md += f"> {p['abstract'][:300]}\n\n"
            md += "---\n\n"
    
    if dry_run:
        print(f"\n[DRY RUN] {len(md)} chars")
        print(md[:3000])
        return
    
    out = os.path.join(repo_path, "reports/active/paper_queue.md")
    with open(out, 'w') as f: f.write(md)
    print(f"\nQueue written: {out}")

def main():
    p = argparse.ArgumentParser(description='Discover new papers')
    p.add_argument('--repo-path', default='/data/sci-logic-kb')
    p.add_argument('--topic', default=None)
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    candidates = discover(a.repo_path, a.topic)
    if not candidates: print("No new candidates."); return 0
    write_queue(candidates, a.repo_path, a.dry_run)
    return 0

if __name__ == '__main__':
    sys.exit(main())
