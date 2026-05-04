import os
import json
from pathlib import Path

STATUS_FILE = "/data/sci-logic-kb/data/ingestion_status.json"
PDF_DIR = "/data/papers-rag-1000/papers"

def init_tracker():
    if not os.path.exists(STATUS_FILE):
        pdfs = sorted([p.stem for p in Path(PDF_DIR).glob("*.pdf")])
        status = {p: "pending" for p in pdfs}
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
        print(f"Tracker initialized with {len(pdfs)} papers.")

def get_next_paper():
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        status = json.load(f)
    for p, s in status.items():
        if s == "pending":
            return p
    return None

def mark_completed(paper_id):
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        status = json.load(f)
    status[paper_id] = "completed"
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        init_tracker()
    elif len(sys.argv) > 1 and sys.argv[1] == "--next":
        print(get_next_paper())
    elif len(sys.argv) > 2 and sys.argv[1] == "--done":
        mark_completed(sys.argv[2])
