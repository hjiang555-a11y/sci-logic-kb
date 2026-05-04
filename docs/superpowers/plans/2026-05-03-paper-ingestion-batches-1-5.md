# Paper Ingestion Pipeline: Batches 1–5 (188 papers across 5 topics)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan batch-by-batch. Each batch is one topic; each task is one paper.

**Goal:** Ingest 188 pending papers (YAML extraction from PDFs) into the sci-logic-kb knowledge graph following CLAUDE.md Step 1-7 workflow.

**Architecture:** Sequential per-topic batches, smallest-first (shared 3 done → timescales 7 → time-frequency-transfer 23 → ultrastable-laser 26 → frequency-standards 64 → optical-frequency-combs 68). Each paper: read PDF via pdftotext, extract structured YAML per SCHEMA.md, write to `topics/<topic>/papers/`, run `lint.py`, update `PROCESSED_PAPERS.md`/`LOG.md`/`ingestion_status.json`, rebuild index, commit.

**Tech Stack:** bash/pdftotext for PDF extraction, Python for lint/index/status updates, git for versioning.

---

## Pre-Flight Checks (every session)

- [ ] Verify `python scripts/lint.py --summary` shows 0 errors before starting
- [ ] Verify `/data/papers-rag-1000/papers/<key>.pdf` exists for target paper
- [ ] Read `topics/<topic>/INDEX.md` for existing nodes to avoid ID collisions
- [ ] Read one existing paper YAML in the topic for style reference

---

## Per-Paper Workflow (CLAUDE.md Step 1-7, reusable template)

For each paper `<KEY>` in topic `<TOPIC>`:

### Step 1-3: Extract PDF text

```bash
pdftotext /data/papers-rag-1000/papers/<KEY>.pdf /tmp/<key>.txt
```

Read the text (typically 300–1000 lines). Identify: title, authors, year, journal/venue, DOI if present, core contribution, key metrics, methods used.

### Step 4: Determine contribution_type

Per SCHEMA.md §9.1:
- **breakthrough**: breaks a metric record, proposes new principle, or falsifies prior claim
- **evidence**: provides new data points on existing nodes, replication, engineering improvement (**default for most papers**)
- **framework**: review/roadmap/textbook chapter establishing topic architecture

### Step 5: Extract YAML nodes

Write `topics/<topic>/papers/<first_author_lower><year>.yaml`. Required sections:
- `meta:` — zotero_key, topic, source_type, contribution_type, reliability, title, year, first_author, authors, journal, doi, note
- `entities:` — system-level hardware/configurations (if any)
- `principles:` — physical/mathematical principles with `statement`, `domain`, `key_insight`, `conditions`, `source.claim`
- `methods:` — experimental/analytical methods with `purpose`, `description`, `key_steps`, `applicable_conditions`, `source.claim`
- `metrics:` — measured values with `demonstrated_value.value`, `demonstrated_value.conditions`, `source.claim`
- `relations:` — at least 3–4 relations connecting nodes with `predicate`, `source.claim`

**Node ID uniqueness check:** grep the topic's INDEX.md for any node IDs before using them.

**Cross-topic references:** Use existing shared nodes where applicable (e.g., `meth.allan_deviation_adev` from allan1966).

### Step 6: Quality gate — lint

```bash
cd /data/sci-logic-kb && python scripts/lint.py --summary
```

Must show **0 errors** before commit. Warnings should not increase. If errors appear, fix them before proceeding.

### Step 7: Update tracking files and commit

```bash
# Rebuild indexes
python scripts/build_index.py

# Update PROCESSED_PAPERS.md — add one line to the topic's table:
# | `<file>.yaml` | <KEY> | <FirstAuthor> <Year> — <one-line contribution> (<Journal>) | ✅ v4.5 <contribution_type> |

# Update LOG.md — prepend entry:
# ## [2026-05-03] ingest | <FirstAuthor> <Year> — <one-line summary> (<topic>)

# Update ingestion_status.json:
python3 -c "
import json
with open('/data/sci-logic-kb/data/ingestion_status.json') as f:
    d = json.load(f)
d['<KEY>'] = 'done'
with open('/data/sci-logic-kb/data/ingestion_status.json', 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
"

# Stage and commit
git add topics/<topic>/papers/<file>.yaml PROCESSED_PAPERS.md LOG.md data/ingestion_status.json \
       topics/<topic>/INDEX.md INDEX.md INDEX_metrics.md INDEX_principles.md docs/CURRENT_NODES_REFERENCE.md
git commit -m "add <first_author><year>: <one-line contribution>"
```

---

## Batch 1: timescales (7 papers) — target: 1→2 hours

**Current state:** 1 paper (dimarcq2024), 6 nodes, 6 relations
**Topic focus:** time scale generation, clock ensembles, steering algorithms, UTC realization

| # | Key | Likely First Author/Year | Notes |
|---|-----|--------------------------|-------|
| 1 | `1.2195297` | TBD (IEEE/DOI key) | Read PDF to identify |
| 2 | `1302.5927` | arXiv:1302.5927 | Read PDF to identify |
| 3 | `1630.full (1)` | TBD (journal full text) | Read PDF to identify |
| 4 | `ICOLS09 Amy et al` | Amy et al. 2009 (ICOLS conf) | Conference paper |
| 5 | `LZ01024172` | TBD (Chinese journal key) | Read PDF to identify |
| 6 | `Syrte 2012` | SYRTE group 2012 | Read PDF to identify |
| 7 | `oe-28-19-28563` | Optics Express 28(19), 28563 (2020) | Read PDF to identify |

### Batch 1 quality checkpoints:
- [ ] All 7 papers have `first_author` + `year` identified from PDF content (not guessed from key)
- [ ] Each YAML has ≥ 3 relations with `source.claim`
- [ ] No node ID collisions with existing dimarcq2024 nodes (check `topics/timescales/INDEX.md`)
- [ ] `lint.py --summary` shows 0 errors after all 7
- [ ] `ingestion_status.json` shows all 7 keys as `done`
- [ ] Timescales INDEX.md shows 8 papers (1 existing + 7 new)

---

## Batch 2: time-frequency-transfer (23 papers)

**Current state:** ~31 papers already ingested (needs exact count from stats.py)
**Topic focus:** optical fiber links, free-space transfer, two-way time transfer, atmospheric turbulence compensation

Quality checkpoints same pattern as Batch 1. Process in alphabetical key order or group by sub-topic if obvious from titles.

---

## Batch 3: ultrastable-laser (26 papers)

**Current state:** ~89 papers already ingested
**Topic focus:** Fabry-Perot cavities, thermal noise limits, vibration sensitivity, coating optimization

Special rule (CLAUDE.md): σ_y-first rule — identify and quantify σ_y(τ=1s) as primary metric; note Allan variant type (ADEV/MDEV/OADEV/Hadamard).

---

## Batch 4: frequency-standards (64 papers)

**Current state:** ~18 papers already ingested
**Topic focus:** optical atomic clocks, microwave standards, ion traps, lattice clocks, accuracy evaluation

Largest batch — consider sub-batching by clock species (Yb/Sr/Al+/Hg+/Yb+ ion/Th nuclear) if PDF titles allow grouping.

---

## Batch 5: optical-frequency-combs (68 papers)

**Current state:** ~114 papers already ingested
**Topic focus:** frequency comb generation, stabilization, dual-comb spectroscopy, microcombs, supercontinuum

Largest batch — consider sub-batching by comb type (fiber/MLL, microresonator/DKS, QCL, EO comb) if PDF titles allow.

---

## Global Quality Gates

After each batch:
- [ ] `python scripts/lint.py --summary` → 0 errors
- [ ] `python scripts/health.py` → all checks pass
- [ ] `python scripts/stats.py` → counts match expectations
- [ ] `git log --oneline -<N>` shows one commit per paper with descriptive messages

After all 5 batches:
- [ ] `python scripts/lint.py --summary` → 0 errors, warnings ≤ current baseline (31)
- [ ] `ingestion_status.json` → 0 `pending_*` entries for the 5 topics (only `needs_review`/`needs_zotero_db`/`out_of_scope` remain)
- [ ] `INDEX.md` shows paper count = 335 + 188 = 523 (approximate, verify with stats.py)
- [ ] All synthesis pages in `topics/*/synthesis/` checked for staleness against new ingestions

---

## Error Recovery

If `lint.py` reports errors after a paper:
1. Read the specific error messages
2. Fix the YAML file (most common: duplicate node ID, missing `source.claim`, malformed `demonstrated_value`)
3. Re-run lint until 0 errors
4. If error is in another topic's file (pre-existing), note it but don't block — fix only what the new paper introduced

If PDF text extraction produces garbled output (scanned PDF, bad encoding):
1. Try `pdftotext -layout` for table-heavy papers
2. If still unreadable, mark as `needs_review` in ingestion_status.json and skip
3. Log the skip in LOG.md
