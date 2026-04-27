#!/usr/bin/env python3
"""Export all YAML knowledge nodes to Dify-compatible JSONL format.
Read-only: never modifies YAML files.
Output: /data/sci-logic-kb/export/knowledge_base.jsonl
"""
import os, sys, json, yaml, glob

KB_PATH = "/data/sci-logic-kb/topics"
OUTPUT_DIR = "/data/sci-logic-kb/export"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "knowledge_base.jsonl")
NODE_SECTIONS = ["entities", "principles", "methods", "metrics"]

def extract_paper_info(data):
    meta = data.get("meta", {}) or {}
    author = meta.get("first_author", "unknown")
    year = meta.get("year", "unknown")
    title = meta.get("title", "")
    return author, year, title

def get_node_text(node, section):
    parts = []
    for key in ["name", "description", "statement", "key_insight", "domain", "formula"]:
        val = node.get(key, "")
        if val:
            parts.append(str(val))
    return "\n".join(parts)

def get_relations_summary(data, node_id):
    related = []
    for rel in (data.get("relations", []) or []):
        if not isinstance(rel, dict):
            continue
        if isinstance(rel.get("subject"), dict):
            subj = str(rel["subject"].get("node_id", ""))
        else:
            subj = str(rel.get("subject", rel.get("source", "")))
        if isinstance(rel.get("object"), dict):
            obj = str(rel["object"].get("node_id", ""))
        else:
            obj = str(rel.get("object", rel.get("target", "")))
        pred = str(rel.get("predicate", rel.get("type", "")))
        if subj == node_id:
            related.append(f"{pred} -> {obj}")
        if obj == node_id:
            related.append(f"<- {pred} from {subj}")
    return "; ".join(related)

def export():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lines = 0
    errors = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for topic_dir in sorted(os.listdir(KB_PATH)):
            pattern = os.path.join(KB_PATH, topic_dir, "papers", "*.yaml")
            for pf in sorted(glob.glob(pattern)):
                try:
                    with open(pf, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    if not data:
                        continue
                    author, year, title = extract_paper_info(data)
                    source_paper = f"{author}{year}"
                    for section in NODE_SECTIONS:
                        for node in (data.get(section, []) or []):
                            if not isinstance(node, dict):
                                continue
                            node_id = node.get("id", "")
                            if not node_id:
                                continue
                            name = node.get("name", "")
                            content = get_node_text(node, section)
                            relations = get_relations_summary(data, node_id)
                            record = {
                                "id": node_id,
                                "type": section,
                                "topic": topic_dir,
                                "source_paper": source_paper,
                                "name": name,
                                "content": content,
                                "relations_summary": relations,
                                "paper_title": title,
                            }
                            out.write(json.dumps(record, ensure_ascii=False) + "\n")
                            lines += 1
                except Exception as e:
                    errors += 1
                    print(f"ERROR: {pf}: {e}", file=sys.stderr)
    return lines, errors

if __name__ == "__main__":
    lines, errors = export()
    print(f"DONE: {lines} nodes exported to {OUTPUT_FILE}")
    print(f"Errors: {errors}")
