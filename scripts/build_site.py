#!/usr/bin/env python3
"""build_site.py — Generate static website from sci-logic-kb data.

Output: docs/site/
  index.html    — Dashboard with stats, health, topic cards
  topics/<t>/   — Papers, metrics, limits per topic
  chains/       — Reasoning chain browser
  consensus/    — Consensus timeline viewer
  api/data.json — Full structured dataset
"""
import os, sys, yaml, json, argparse, subprocess, glob
from collections import defaultdict, Counter
from datetime import datetime
from html import escape

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font:14px/1.6 system-ui,-apple-system, sans-serif;color:#1a1a2e;background:#f8f9fa;max-width:1100px;margin:0 auto;padding:0 20px}
nav{display:flex;gap:24px;padding:16px 0;border-bottom:2px solid #2563eb;margin-bottom:24px;flex-wrap:wrap}
nav a{color:#2563eb;text-decoration:none;font-weight:600;font-size:15px}
nav a:hover,a:hover{color:#1d4ed8}
main{min-height:70vh}
footer{text-align:center;color:#94a3b8;padding:24px 0;margin-top:48px;border-top:1px solid #e2e8f0;font-size:12px}
h1{font-size:24px;margin:24px 0 8px}
h2{font-size:18px;margin:20px 0 8px;border-bottom:1px solid #e2e8f0;padding-bottom:4px}
h3{font-size:15px;margin:16px 0 4px;color:#334155}
.card{background:#fff;border-radius:8px;padding:16px;margin:12px 0;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin:16px 0}
.stat{text-align:center;padding:12px}
.stat-val{font-size:28px;font-weight:700;color:#2563eb}
.stat-lbl{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:11px;margin:2px;font-weight:600}
.badge-ok{background:#d1fae5;color:#065f46}.badge-warn{background:#fef3c7;color:#92400e}.badge-err{background:#fee2e2;color:#991b1b}
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13px}
th{background:#f1f5f9;text-align:left;padding:8px;border-bottom:2px solid #cbd5e1;font-weight:600}
td{padding:6px 8px;border-bottom:1px solid #e2e8f0;vertical-align:top}
tr:hover{background:#f8fafc}
.timeline{position:relative;padding-left:20px;border-left:3px solid #2563eb;margin:16px 0}
.tl-item{margin:10px 0;padding:8px 12px;background:#f8fafc;border-radius:4px}
.tl-year{color:#2563eb;font-weight:700;font-size:14px}
.tl-val{color:#0f172a;font-size:13px}
.tl-sys{color:#64748b;font-size:12px}
.tl-sig{color:#94a3b8;font-size:11px;margin-top:2px}
.chain-q{font-style:italic;color:#475569;margin:8px 0}
code{background:#f1f5f9;padding:1px 4px;border-radius:2px;font-size:12px}
a{color:#2563eb;text-decoration:none}
.good{color:#059669}.warn{color:#d97706}.err{color:#dc2626}
.dim{color:#94a3b8}
pre{background:#f1f5f9;padding:12px;border-radius:4px;overflow-x:auto;font-size:12px}
"""

class SiteBuilder:
    def __init__(self, repo_path, output_dir):
        self.repo = repo_path
        self.out = output_dir
        self.now = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        self.topics = defaultdict(lambda: defaultdict(list))
        self.all_papers = []
        self.chains = []
        self.consensus = []
        self.lint_data = {}
        self.stats_data = {}
        self.topic_order = ['ultrastable-laser','optical-frequency-combs','frequency-standards','time-frequency-transfer','timescales','shared']

    def nav(self, depth):
        home = '../' * depth if depth > 0 else ''
        css = home + 'style.css'
        home_link = home + 'index.html'
        return f"""<nav><a href="{home_link}">sci-logic-kb</a>
<a href="{home}topics/">Topics</a> <a href="{home}chains/">Chains</a>
<a href="{home}consensus/">Consensus</a> <a href="{home}dashboard/">Dashboard</a></nav>
<main>"""

    def page(self, title, depth, body):
        css = '../' * depth + 'style.css' if depth > 0 else 'style.css'
        return f"""<!DOCTYPE html><html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} · sci-logic-kb</title><link rel="stylesheet" href="{css}"></head>
<body>{self.nav(depth)}{body}</main><footer>sci-logic-kb v5.0 · Generated {self.now}</footer></body></html>"""

    def collect(self):
        topics_dir = os.path.join(self.repo, "topics")
        for topic in os.listdir(topics_dir):
            tp = os.path.join(topics_dir, topic)
            if not os.path.isdir(tp): continue
            pd = os.path.join(tp, "papers")
            if not os.path.isdir(pd): continue
            for f in sorted(os.listdir(pd)):
                if not f.endswith('.yaml'): continue
                try:
                    with open(os.path.join(pd, f)) as fh: data = yaml.safe_load(fh)
                except: continue
                if not data: continue
                meta = data.get('meta',{})
                paper = {
                    'file':f,'title':str(meta.get('title','')),'year':str(meta.get('year','')),
                    'author':str(meta.get('first_author','')),'ct':str(meta.get('contribution_type','')),
                    'topic':topic,'has_content':False,
                }
                for sec in ['entities','principles','methods','metrics']:
                    items = data.get(sec)
                    if items is not None and len(items)>0: paper['has_content']=True;break
                self.topics[topic]['papers'].append(paper)
                self.all_papers.append(paper)
                for m in data.get('metrics') or []:
                    dv = m.get('demonstrated_value',{})
                    v = dv.get('value','') if isinstance(dv,dict) else ''
                    if v and v!='see paper':
                        self.topics[topic]['metrics'].append({'name':m.get('name',''),'value':str(v)[:200],'year':paper['year'],'author':paper['author']})
                for p in data.get('principles') or []:
                    self.topics[topic]['principles'].append({'id':p.get('id',''),'name':p.get('name',''),'tier':p.get('tier','')})
                for rel in data.get('relations') or []:
                    if rel.get('predicate')=='BOUNDED-BY':
                        self.topics[topic]['bounded_by'].append({'subject':str(rel.get('subject','')),'object':str(rel.get('object','')),'has_bt':bool(rel.get('breakthrough_paths')),'is_limit':rel.get('is_system_limit')})
                        for bp in rel.get('breakthrough_paths') or []:
                            self.topics[topic]['bt_paths'].append({'direction':bp.get('direction',''),'status':bp.get('status','')})
        for cf in glob.glob(os.path.join(self.repo,"logic/chains/*.yaml")):
            try:
                with open(cf) as f: c=yaml.safe_load(f)
                if c: self.chains.append({'id':c.get('chain_id',''),'q':c.get('question',''),'domain':c.get('domain',''),'conf':c.get('confidence',''),'lp':(c.get('limiting_principle',{})or{}).get('name',''),'best':(c.get('current_best',{})or{}).get('value',''),'edges':c.get('edges',[])or[],'ev':c.get('evidence',[])or[],'timeline':c.get('timeline',[])or[],'narrative':c.get('breakthrough_narrative','')[:300]})
            except: pass
        for cf in glob.glob(os.path.join(self.repo,"consensus/*.yaml")):
            try:
                with open(cf) as f: cs=yaml.safe_load(f)
                if cs: self.consensus.append({'metric':cs.get('metric',''),'name':cs.get('metric_name',''),'domain':cs.get('domain',''),'conf':cs.get('confidence',''),'best':(cs.get('consensus',{})or{}).get('best_demonstrated_value',''),'timeline':cs.get('timeline',[])or[],'trend':cs.get('trend','')})
            except: pass
        try:
            r=subprocess.run(['python3',os.path.join(self.repo,'scripts/lint.py'),'--repo-path',self.repo,'--json'],capture_output=True,text=True,cwd=self.repo)
            self.lint_data=json.loads(r.stdout) if r.stdout else {}
        except: pass
        try:
            r=subprocess.run(['python3',os.path.join(self.repo,'scripts/stats.py'),'--repo-path',self.repo,'--json'],capture_output=True,text=True,cwd=self.repo)
            if r.stdout:
                for line in r.stdout.strip().split('\n'):
                    try: self.stats_data.update(json.loads(line))
                    except: pass
        except: pass

    def build_index(self):
        total=len(self.all_papers)
        wc=sum(1 for p in self.all_papers if p['has_content'])
        bt=sum(len(self.topics[t]['bounded_by']) for t in self.topic_order)
        btp=sum(len(self.topics[t]['bt_paths']) for t in self.topic_order)
        le=self.lint_data.get('errors',0)
        lw=self.lint_data.get('warnings',0)

        b=''
        b+='<h1>sci-logic-kb v5.0</h1><p style="color:#64748b">Time-frequency metrology knowledge base</p>'
        b+='<div class="grid">'
        b+=f'<div class="card stat"><div class="stat-val">{total}</div><div class="stat-lbl">Papers</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{wc}<span class="dim">/{total}</span></div><div class="stat-lbl">With Content</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{len(self.chains)}</div><div class="stat-lbl">Reasoning Chains</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{len(self.consensus)}</div><div class="stat-lbl">Consensus Reports</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{bt}</div><div class="stat-lbl">BOUNDED-BY</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{btp}</div><div class="stat-lbl">Breakthrough Paths</div></div>'
        b+='</div>'

        health=f'<span class="badge badge-{"ok" if le==0 else "err"}">Lint: {le} errors</span> '
        health+=f'<span class="badge badge-{"ok" if lw<150 else "warn"}">{lw} warnings</span> '
        ev_cov=100
        try:
            for line in (subprocess.run(['python3',os.path.join(self.repo,'scripts/stats.py'),'--repo-path',self.repo],capture_output=True,text=True,cwd=self.repo).stdout or '').split('\n'):
                if 'Evidence Coverage' in line:
                    import re; m=re.search(r'(\d+\.?\d*)%',line)
                    if m: ev_cov=float(m.group(1))
        except: pass
        health+=f'<span class="badge badge-{"ok" if ev_cov>=95 else "warn"}">Evidence: {ev_cov:.0f}%</span>'
        b+=f'<div class="card"><h3>Health</h3><p>{health}</p></div>'

        b+='<h2>Topics</h2><div class="grid">'
        for t in self.topic_order:
            td=self.topics.get(t,{})
            pc=sum(1 for p in td.get('papers',[]) if p['has_content'])
            b+=f'<a href="topics/{t}/"><div class="card"><h3>{t}</h3>'
            b+=f'<p>{pc} papers · {len(td.get("metrics",[]))} metrics · {len(td.get("bounded_by",[]))} limits</p></div></a>'
        b+='</div>'

        b+='<h2>Reasoning Chains</h2><div class="grid">'
        for c in sorted(self.chains,key=lambda x:x['domain']):
            b+=f'<a href="chains/#{c["id"]}"><div class="card"><h3>{c["domain"]}</h3><p class="chain-q">{escape(c["q"][:100])}</p><p>{len(c["ev"])} evidence · {len(c["edges"])} edges</p></div></a>'
        b+='</div>'

        b+='<h2>Consensus Reports</h2><div class="grid">'
        for c in sorted(self.consensus,key=lambda x:x['domain']):
            b+=f'<a href="consensus/#{c["metric"]}"><div class="card"><h3>{c["domain"]}</h3><p>{escape(c.get("name","")[:100])}</p><p>{len(c["timeline"])} entries</p></div></a>'
        b+='</div>'

        with open(os.path.join(self.out,'index.html'),'w') as f: f.write(self.page('Knowledge Base',0,b))

    def build_topics(self):
        os.makedirs(os.path.join(self.out,'topics'),exist_ok=True)
        for topic in self.topic_order:
            td=self.topics.get(topic,{})
            os.makedirs(os.path.join(self.out,'topics',topic),exist_ok=True)
            papers=sorted(td.get('papers',[]),key=lambda x:(-int(x['year']) if x['year'].isdigit() else 0))
            pc=sum(1 for p in papers if p['has_content'])
            b=f'<h1>{topic}</h1><p>{pc}/{len(papers)} papers · {len(td.get("metrics",[]))} metrics · {len(td.get("bounded_by",[]))} limits · {len(td.get("bt_paths",[]))} paths</p>'
            mt=sorted(td.get('metrics',[]),key=lambda x:-int(x['year']) if x['year'].isdigit() else 0)[:30]
            if mt:
                b+='<h2>Key Metrics</h2><table><tr><th>Year</th><th>Author</th><th>Metric</th><th>Value</th></tr>'
                for m in mt:b+=f'<tr><td>{m["year"]}</td><td>{m["author"]}</td><td>{escape(m["name"][:60])}</td><td><code>{escape(m["value"][:100])}</code></td></tr>'
                b+='</table>'
            b+='<h2>Papers</h2><table><tr><th>Year</th><th>Author</th><th>Title</th><th>Type</th><th>Content</th></tr>'
            for p in papers[:60]:
                ct_badge='breakthrough' if p['ct']=='breakthrough' else 'framework' if p['ct']=='framework' else 'evidence'
                cs='<span class="badge badge-ok">'+str(sum(1 for s in ['entities','principles','methods','metrics'] if len((p.get(s,[])or[]))>0))+' sections</span>' if p['has_content'] else '<span class="badge badge-warn">placeholder</span>'
                b+=f'<tr><td>{p["year"]}</td><td>{p["author"]}</td><td>{escape(p["title"][:100])}</td><td><span class="badge badge-{ct_badge}">{p["ct"]}</span></td><td>{cs}</td></tr>'
            b+='</table>'
            if td.get('bounded_by'):
                b+='<h2>Limits (BOUNDED-BY)</h2><ul>'
                for lb in td['bounded_by'][:15]:
                    bt_mark='✅' if lb['has_bt'] else '❌'
                    b+=f'<li>{bt_mark} {escape(lb["subject"])} → {escape(lb["object"])}</li>'
                b+='</ul>'
            with open(os.path.join(self.out,'topics',topic,'index.html'),'w') as f: f.write(self.page(topic,2,b))

    def build_chains(self):
        b='<h1>Reasoning Chains</h1><p>12 chains — causal reasoning from limiting principles to breakthrough paths.</p>'
        for c in sorted(self.chains,key=lambda x:x['domain']):
            b+=f'<div class="card" id="{c["id"]}"><h2>{c["domain"]} · <span class="badge badge-{"ok" if c["conf"]=="established" else "warn"}">{c["conf"]}</span></h2>'
            b+=f'<p class="chain-q">{escape(c["q"])}</p>'
            if c['lp']:b+=f'<p><strong>Limit:</strong> {escape(c["lp"])}</p>'
            if c['best']:b+=f'<p><strong>Best:</strong> <code>{escape(c["best"][:120])}</code></p>'
            if c['narrative']:b+=f'<p style="font-size:13px;color:#475569">{escape(c["narrative"][:400])}</p>'
            if c['edges']:
                b+='<h3>Edges</h3><ul>'
                for e in c['edges'][:8]:b+=f'<li>{escape(e["from"])} → <strong>{e["relation"]}</strong> → {escape(e["to"])}</li>'
                b+='</ul>'
            if c['timeline']:
                b+='<div class="timeline">'
                for tl in c['timeline'][:8]:
                    b+=f'<div class="tl-item"><span class="tl-year">{tl.get("year","")}</span> <span class="tl-val">{escape(str(tl.get("value",""))[:80])}</span><br><span class="tl-sys">{escape(str(tl.get("system",""))[:80])}</span></div>'
                b+='</div>'
            b+=f'<p><strong>Evidence:</strong> {len(c["ev"])} v4.5 relation references</p></div>'
        with open(os.path.join(self.out,'chains','index.html'),'w') as f: f.write(self.page('Chains',1,b))

    def build_consensus(self):
        b='<h1>Consensus Reports</h1><p>7 reports — best demonstrated values with historical timelines.</p>'
        for cs in sorted(self.consensus,key=lambda x:x['domain']):
            b+=f'<div class="card" id="{cs["metric"]}"><h2>{cs["domain"]} · <span class="badge badge-{"ok" if cs["conf"]=="established" else "warn"}">{cs["conf"]}</span></h2>'
            b+=f'<p>{escape(cs.get("name","")[:150])}</p>'
            if cs['best']:b+=f'<p><strong>Best:</strong> <code>{escape(str(cs["best"])[:150])}</code></p>'
            if cs.get('trend'):b+=f'<p style="color:#64748b">{escape(cs["trend"][:200])}</p>'
            if cs['timeline']:
                b+='<div class="timeline">'
                for tl in cs['timeline']:
                    b+=f'<div class="tl-item"><span class="tl-year">{tl.get("year","")}</span> '
                    b+=f'<span class="tl-val">{escape(str(tl.get("value",""))[:100])}</span><br>'
                    b+=f'<span class="tl-sys">{escape(str(tl.get("system",""))[:80])}</span>'
                    if tl.get('significance'):b+=f'<div class="tl-sig">{escape(str(tl["significance"])[:120])}</div>'
                    b+='</div>'
                b+='</div>'
            b+='</div>'
        with open(os.path.join(self.out,'consensus','index.html'),'w') as f: f.write(self.page('Consensus',1,b))

    def build_dashboard(self):
        le=self.lint_data.get('errors',0)
        lw=self.lint_data.get('warnings',0)
        li=self.lint_data.get('info',0)
        issues=self.lint_data.get('issues',[])
        by_cat=Counter(i.get('category','?') for i in issues)
        by_level=Counter(i.get('level','?') for i in issues)

        total=len(self.all_papers)
        wc=sum(1 for p in self.all_papers if p['has_content'])
        bt=sum(len(self.topics[t]['bounded_by']) for t in self.topic_order)
        btp=sum(len(self.topics[t]['bt_paths']) for t in self.topic_order)
        bt_with=sum(1 for t in self.topic_order for lb in self.topics[t].get('bounded_by',[]) if lb['has_bt'])

        b='<h1>Dashboard</h1>'

        b+='<div class="grid">'
        b+=f'<div class="card stat"><div class="stat-val {"good" if le==0 else "err"}">{le}</div><div class="stat-lbl">Lint Errors</div></div>'
        b+=f'<div class="card stat"><div class="stat-val warn">{lw}</div><div class="stat-lbl">Lint Warnings</div></div>'
        b+=f'<div class="card stat"><div class="stat-val dim">{li}</div><div class="stat-lbl">Lint Info</div></div>'
        b+=f'<div class="card stat"><div class="stat-val good">{wc}/{total}</div><div class="stat-lbl">Content Coverage</div></div>'
        b+=f'<div class="card stat"><div class="stat-val good">{bt_with}/{bt}</div><div class="stat-lbl">Chain Closure</div></div>'
        b+=f'<div class="card stat"><div class="stat-val">{len(self.chains)}</div><div class="stat-lbl">Chains</div></div>'
        b+='</div>'

        b+='<h2>Lint by Category</h2><table><tr><th>Category</th><th>Count</th></tr>'
        for cat,cnt in by_cat.most_common():
            lvl=Counter(i.get('level','?') for i in issues if i.get('category')==cat)
            lvl_str=' '.join(f'<span class="badge badge-{"err" if k=="ERROR" else "warn" if k=="WARNING" else "ok"}">{k}:{v}</span>' for k,v in lvl.items())
            b+=f'<tr><td>{cat}</td><td>{cnt} {lvl_str}</td></tr>'
        b+='</table>'

        b+='<h2>Topic Coverage</h2><table><tr><th>Topic</th><th>Papers</th><th>Content</th><th>Metrics</th><th>BOUNDED-BY</th><th>BT Paths</th><th>Chains</th><th>Consensus</th></tr>'
        for t in self.topic_order:
            td=self.topics.get(t,{})
            pc=sum(1 for p in td.get('papers',[]) if p['has_content'])
            tp=len(td.get('papers',[]))
            nc=sum(1 for c in self.chains if c['domain']==t)
            cs_c=sum(1 for c in self.consensus if c['domain']==t)
            b+=f'<tr><td><strong>{t}</strong></td><td>{tp}</td><td><span class="{"good" if pc==tp else "warn"}">{pc}</span></td><td>{len(td.get("metrics",[]))}</td><td>{len(td.get("bounded_by",[]))}</td><td>{len(td.get("bt_paths",[]))}</td><td>{nc}</td><td>{cs_c}</td></tr>'
        b+='</table>'

        b+=f'<p class="dim">Last rebuild: {self.now}</p>'
        with open(os.path.join(self.out,'dashboard','index.html'),'w') as f: f.write(self.page('Dashboard',1,b))

    def build(self):
        print("Collecting data...")
        self.collect()
        os.makedirs(self.out,exist_ok=True)
        for sub in ['topics','chains','consensus','dashboard','api']:
            os.makedirs(os.path.join(self.out,sub),exist_ok=True)
        with open(os.path.join(self.out,'style.css'),'w') as f: f.write(CSS)

        print("Building pages...")
        self.build_index()
        self.build_topics()
        self.build_chains()
        self.build_consensus()
        self.build_dashboard()

        # JSON data export
        export={'papers':self.all_papers,'chains':[{'id':c['id'],'q':c['q'],'domain':c['domain']} for c in self.chains],'consensus':[{'metric':c['metric'],'domain':c['domain'],'best':c['best']} for c in self.consensus]}
        with open(os.path.join(self.out,'api','data.json'),'w') as f: json.dump(export,f,ensure_ascii=False)

        # Symlink graph viewer
        gs=os.path.join(self.repo,'docs/graph')
        gd=os.path.join(self.out,'graph')
        if os.path.exists(gs) and not os.path.exists(gd): os.symlink(gs,gd)

        print(f"\nSite generated: {self.out}")
        print(f"  index.html · topics/ · chains/ · consensus/ · dashboard/")
        print(f"  api/data.json · graph/ (symlink)")
        return 0

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo-path',default='/data/sci-logic-kb')
    p.add_argument('--output',default=None)
    a=p.parse_args()
    out=a.output or os.path.join(a.repo_path,'docs/site')
    return SiteBuilder(a.repo_path,out).build()

if __name__=='__main__': sys.exit(main())
