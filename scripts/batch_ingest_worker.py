import os
import yaml
from pathlib import Path

# Configuration
PDF_DIR = "/data/papers-rag-1000/papers"
EVIDENCE_DIR = "/data/data/evidence" # Wait, checking path
EVIDENCE_DIR = "/data/sci-logic-kb/data/evidence"
QUEUE_FILE = "/data/sci-logic-kb/reports/active/ingestion_queue.txt"

def process_single_paper(pdf_stem):
    """
    This is a placeholder for the actual PDF-to-Atomic-Node extraction.
    In a real scenario, this would call a LLM/Parser.
    For this automation, we'll simulate the extraction of a 'Generic' evidence node
    to verify the pipeline, then in a real loop, we'd use an agent.
    """
    pdf_path = os.path.join(PDF_DIR, f"{pdf_stem}.pdf")
    if not os.path.exists(pdf_path):
        return False, "File not found"

    # Simulation of extraction result
    # In the real loop, the agent will do this per paper.
    # We create a basic EvidenceNode for each paper to populate the base layer.
    evidence_node = {
        "id": f"evid_{pdf_stem}",
        "name": f"Evidence from {pdf_stem}",
        "type": "Entity/Factor",
        "definition": f"Automatic extraction from {pdf_stem}. Details pending deep scan.",
        "properties": {
            "source_pdf": pdf_stem,
            "status": "unverified"
        },
        "metadata": {
            "source_paper": pdf_stem,
            "status": "processed_auto"
        }
    }
    
    with open(os.path.join(EVIDENCE_DIR, f"{evidence_node['id']}.yaml"), 'w', encoding='utf-8') as f:
        yaml.dump(evidence_node, f, allow_unicode=True)
    return True, "Success"

def run_batch(batch_size=10):
    if not os.path.exists(QUEUE_FILE):
        print("Queue file not found.")
        return

    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = f.read().splitlines()

    if not queue:
        print("Queue empty.")
        return

    batch = queue[:batch_size]
    remaining = queue[batch_size:]

    print(f"Processing batch of {len(batch)} papers...")
    success_count = 0
    for paper in batch:
        ok, msg = process_single_paper(paper)
        if ok: success_count += 1
    
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        for p in remaining:
            f.write(f"{p}\n")

    print(f"Batch completed. {success_count}/{len(batch)} successful. {len(remaining)} remaining.")

if __name__ == "__main__":
    run_batch()
