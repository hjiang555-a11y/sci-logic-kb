#!/usr/bin/env python3
"""
Process a paper PDF using GitHub Models API (claude-sonnet-4-6) → generate YAML.
Also supports reprocessing existing YAMLs to SCHEMA v2.0.

Uses OpenAI-compatible GitHub Models endpoint with GITHUB_TOKEN.
No separate Anthropic API key needed — Copilot Pro+ subscription covers this.

Environment variables (set by GitHub Actions):
  GITHUB_TOKEN        - Auto-injected by Actions (no extra secret needed)
  TASK                - 'process' | 'reprocess-v2'
  AUTHOR_YEAR         - e.g. matei2017
  PDF_FILENAME        - e.g. TVY7T59A_matei2017.pdf  (only for process task)
  ZOTERO_KEY          - e.g. TVY7T59A
"""

import os
import sys
from pathlib import Path

from openai import OpenAI

GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
MODEL = "claude-sonnet-4-6"


def get_client() -> OpenAI:
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("ERROR: GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    return OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=token)


def load_context() -> tuple[str, str, str]:
    """Load SCHEMA, copilot instructions, and existing papers as context."""
    schema = Path("SCHEMA.md").read_text(encoding="utf-8")
    instructions = Path(".github/copilot-instructions.md").read_text(encoding="utf-8")

    existing = []
    for f in sorted(Path("papers").glob("*.yaml")):
        existing.append(f"### {f.name}\n```yaml\n{f.read_text(encoding='utf-8')}\n```")
    existing_str = "\n\n".join(existing) if existing else "(none yet)"

    return schema, instructions, existing_str


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader  # type: ignore[no-redef]

    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def process_new_paper(client: OpenAI, author_year: str,
                      zotero_key: str, pdf_filename: str,
                      schema: str, instructions: str, existing: str) -> str:
    """Extract knowledge from a new PDF."""
    pdf_path = Path(f"pdfs/{pdf_filename}")
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    pdf_text = extract_pdf_text(pdf_path)
    print(f"PDF extracted: {len(pdf_text)} chars")

    system_prompt = f"""You are a knowledge extraction expert for ultra-stable laser physics research.

Extract structured YAML knowledge nodes from the provided research paper.
Follow SCHEMA v2.0 strictly. Output ONLY the complete YAML file — no explanation,
no markdown code fences. Start directly with the comment line.

=== SCHEMA v2.0 ===
{schema}

=== EXISTING NODES (cross-reference, do NOT redefine) ===
{existing}

=== DETAILED TASK INSTRUCTIONS ===
{instructions}
"""

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Process this paper (Zotero key: {zotero_key}).\n"
                    f"Generate the complete YAML file for papers/{author_year}.yaml "
                    f"following SCHEMA v2.0.\n"
                    f"This is a NEW paper — extract all entities, principles, "
                    f"methods, metrics, and relations.\n\n"
                    f"=== PAPER TEXT ===\n{pdf_text}"
                )
            }
        ]
    )

    return response.choices[0].message.content


def reprocess_v2(client: OpenAI, author_year: str,
                 schema: str, existing: str) -> str:
    """Update an existing YAML file to comply with SCHEMA v2.0."""
    existing_yaml_path = Path(f"papers/{author_year}.yaml")
    if not existing_yaml_path.exists():
        raise FileNotFoundError(f"Existing YAML not found: {existing_yaml_path}")

    existing_yaml = existing_yaml_path.read_text(encoding="utf-8")

    system_prompt = f"""You are a knowledge graph schema migration expert.

Migrate the provided YAML file from SCHEMA v1.0 to SCHEMA v2.0.
Output ONLY the complete migrated YAML — no explanation, no markdown fences.

=== SCHEMA v2.0 (target) ===
{schema}

=== OTHER EXISTING FILES (for cross-reference) ===
{existing}
"""

    migration_instructions = """
Specific changes required for v2.0 migration:

1. RELATION TYPES — replace all GOVERNED-BY:
   - If the principle explains WHY the method works → ENABLED-BY
   - If the principle sets a PERFORMANCE LIMIT → BOUNDED-BY

2. BOUNDED-BY must include these fields:
   is_system_limit: true/false
   dominated_by: null  (or the ID of the principle that dominates it)
   quantitative_contribution: "X%"  (if known)
   regime: all | short-term | long-term | during-sweep
   verification_status: observed | calculated | inferred
   temporal_role: proposes | validates | refutes | extends
   breakthrough_paths:
     - direction: pri.xxx
       expected_gain: "description"
       status: demonstrated | theoretical | speculative
       source: {zotero_key: "KEY"}

3. ENTITY NODES — add:
   hierarchy_level: 1  (Level 1=main branch entity, 2=sub-unit, ext=external condition)
   status: demonstrated | theoretical | obsolete

4. PRINCIPLE NODES — add:
   tier: meta | domain | engineering
   verification_status: observed | calculated | inferred

5. DERIVED-FROM — add relations from engineering-tier principles to their parent:
   e.g. pri.beam_radius_scaling DERIVED-FROM pri.brownian_thermal_noise_fdt

6. COMPETES-WITH — add at Level 1 if applicable (e.g. FP cavity vs fiber interferometer)

7. CONDITIONED-BY — add for external conditions (vibration, temperature) with interface fields

8. Remove deprecated relations: GOVERNED-BY, EQUIVALENT-IN-CONTEXT, SUPPORTED-BY

9. Update header comment to include: # Schema版本：v2.0
"""

    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=8192,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Migrate this file to SCHEMA v2.0:\n\n"
                    f"```yaml\n{existing_yaml}\n```\n\n"
                    f"{migration_instructions}"
                )
            }
        ]
    )

    return response.choices[0].message.content


def main():
    task = os.environ.get("TASK", "process")
    author_year = os.environ.get("AUTHOR_YEAR", "")
    zotero_key = os.environ.get("ZOTERO_KEY", "")
    pdf_filename = os.environ.get("PDF_FILENAME", "")

    if not author_year:
        print("ERROR: AUTHOR_YEAR not set", file=sys.stderr)
        sys.exit(1)

    client = get_client()
    schema, instructions, existing = load_context()

    print(f"Task: {task} | Paper: {author_year} | Model: {MODEL}")

    if task == "reprocess-v2":
        yaml_content = reprocess_v2(client, author_year, schema, existing)
    else:
        if not pdf_filename:
            matches = list(Path("pdfs").glob(f"*_{author_year}.pdf"))
            if matches:
                pdf_filename = matches[0].name
                print(f"Found PDF: {pdf_filename}")
            else:
                print(f"ERROR: PDF_FILENAME not set and no match found for {author_year}",
                      file=sys.stderr)
                sys.exit(1)

        yaml_content = process_new_paper(
            client, author_year, zotero_key, pdf_filename,
            schema, instructions, existing
        )

    output_path = Path(f"papers/{author_year}.yaml")
    output_path.write_text(yaml_content, encoding="utf-8")
    print(f"Written: {output_path} ({len(yaml_content)} chars)")

    with open(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/null"), "a") as f:
        f.write(f"## Paper processed: `{author_year}.yaml`\n")
        f.write(f"- Task: `{task}`\n")
        f.write(f"- Model: `{MODEL}`\n")
        f.write(f"- Output: `{output_path}` ({len(yaml_content)} chars)\n")


if __name__ == "__main__":
    main()
