import os
from pathlib import Path

PDF_DIR = "/data/papers-rag-1000/papers"
EVIDENCE_DIR = "/data/sci-logic-kb/data/evidence"

def get_all_pdfs():
    return {p.stem for p in Path(PDF_DIR).glob("*.pdf")}

def get_processed_pdfs():
    # We look at the evidence layer. If a paper has any evidence node, it's "processed"
    # Evidence nodes are usually named la_... or evid_...
    # But the most reliable way is to check if the PDF stem is in the metadata of any evidence node.
    processed = set()
    for p in Path(EVIDENCE_DIR).glob("*.yaml"):
        with open(p, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if data and 'metadata' in data:
                    source = data['metadata'].get('source_paper', '')
                    # We'll store the filename stem in source_paper
                    processed.add(source)
            except:
                continue
    return processed

if __name__ == "__main__":
    all_pdfs = get_all_pdfs()
    processed = get_processed_pdfs()
    
    # Papers that are in PDF dir but NOT in the processed set
    missing = sorted([p for p in all_pdfs if p not in processed])
    
    print(f"Total PDFs: {len(all_pdfs)}")
    print(f"Processed: {len(processed)}")
    print(f"Missing: {len(missing)}")
    for m in missing:
        print(m)
