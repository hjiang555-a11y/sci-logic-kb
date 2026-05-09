#!/usr/bin/env python3
"""kb-query-server.py — LLM-assisted knowledge base query API.
Uses Ollama for answer generation, local JSON index for retrieval.
POST /query  {"question": "..."}
"""

import json, os, sys, re
from http.server import HTTPServer, BaseHTTPRequestHandler

KB_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(KB_DIR, "data", "structured_data.json")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:7b"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def search(query, data, top_n=8):
    tokens = query.lower().replace('?','').split()
    tokens = [t for t in tokens if len(t) > 1]
    results = []

    for c in data.get('consensus', []):
        text = (c.get('name','') + ' ' + c.get('best','') + ' ' + c.get('trend','')).lower()
        score = sum(2 for t in tokens if t in text)
        if score > 0: results.append(('consensus', c, score))

    for c in data.get('chains', []):
        text = (c.get('question','') + ' ' + c.get('limit','') + ' ' + c.get('best','') + ' ' + c.get('narrative','')).lower()
        score = sum(2 for t in tokens if t in text)
        if score > 0: results.append(('chain', c, score))

    for tname, papers in data.get('topics', {}).items():
        if tname not in ('shared',): continue
        for p in papers:
            text = (p.get('title','') + ' ' + p.get('author','')).lower()
            score = sum(1 for t in tokens if t in text)
            if score > 1: results.append(('paper', {**p, 'topic': tname}, score))

    for m in data.get('metrics', []):
        text = (m.get('metric','') + ' ' + m.get('value','') + ' ' + m.get('paper','')).lower()
        score = sum(2 for t in tokens if t in text)
        if score > 1: results.append(('metric', m, score))

    results.sort(key=lambda x: -x[2])
    return results[:top_n]

def build_context(results):
    ctx = []
    for typ, item, score in results:
        if typ == 'consensus':
            ctx.append(f"[共识] {item.get('name','')}: 最佳值={item.get('best','')}. {item.get('trend','')}")
        elif typ == 'chain':
            ctx.append(f"[推理链] 问题: {item.get('question','')}. 限制: {item.get('limit','')}. 当前最佳: {item.get('best','')}")
        elif typ == 'paper':
            ctx.append(f"[论文] {item.get('year','')} {item.get('author','')}: {item.get('title','')}")
        elif typ == 'metric':
            ctx.append(f"[指标] {item.get('metric','')} = {item.get('value','')}")
    return '\n'.join(ctx[:6])

def ask_ollama(question, context):
    prompt = f"""你是一个时间频率计量知识库助手。只基于以下知识库内容回答问题。不知道就说不知道。回答要简洁准确，引用来源。

知识库内容:
{context}

用户问题: {question}

回答:"""
    try:
        import urllib.request
        data = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(OLLAMA_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get('response', '').strip()
    except:
        return None

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/query':
            self.send_response(404); self.end_headers(); return
        try:
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length))
            question = body.get('question', '')
        except:
            self.send_response(400); self.end_headers(); return

        data = load_data()
        results = search(question, data)
        context = build_context(results)

        ollama_answer = ask_ollama(question, context)

        sources = []
        for typ, item, _ in results[:5]:
            if typ == 'consensus': sources.append(f"共识: {item.get('name','')}")
            elif typ == 'chain': sources.append(f"推理链: {item.get('question','')[:80]}")
            elif typ == 'paper': sources.append(f"{item.get('year','')} {item.get('author','')}: {item.get('title','')[:80]}")
            elif typ == 'metric': sources.append(f"{item.get('metric','')[:80]}")

        if ollama_answer:
            answer = ollama_answer
        else:
            answer = "基于知识库数据：\n" + '\n'.join(sources[:5])
            answer += "\n\n⚠️ Ollama 未连接，显示原始检索结果。"

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({
            'answer': answer,
            'sources': sources,
            'context_used': len(context),
        }, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args): pass

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8910
    print(f"kb-query-server on :{port}")
    print(f"Data: {DATA_FILE}")
    print(f"Ollama: {OLLAMA_URL} (model: {OLLAMA_MODEL})")
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

if __name__ == '__main__':
    main()
