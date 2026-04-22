#!/usr/bin/env python3
"""
lint.py — Advanced lint / health-check for the sci-logic-kb knowledge base.

Checks:
  1.  Orphan nodes          (WARNING)
  2.  Dangling references   (ERROR)
  3.  Duplicate definitions (ERROR)
  4.  Duplicate relation IDs (ERROR)
  5.  Reasoning chain gaps  (WARNING)  — BOUNDED-BY without breakthrough_paths
  6.  Missing evidence       (WARNING) — relations without source.claim
  7.  Missing conditions     (WARNING) — principles without conditions
  8.  Missing metric conds   (WARNING) — metrics with demonstrated_value but no conditions
  9.  Invalid predicates     (ERROR)   — deprecated predicates
  10. Invalid node ID prefix (ERROR)
  11. Missing meta fields    (WARNING)
  12. Breakthrough-missing-primary-metric (WARNING) — ultrastable-laser
      breakthrough papers must link a σ_y primary-role metric.

Exit code: 0 if no errors (warnings OK unless --strict), 1 if errors found.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


# ── Constants ────────────────────────────────────────────────────────────────

VALID_PREFIXES = ("ent.", "pri.", "meth.", "met.", "rel.")

VALID_PREDICATES = frozenset({
    "PART-OF",
    "CHARACTERIZED-BY",
    "OPERATIONALIZED-AS",
    "ENABLED-BY",
    "BOUNDED-BY",
    "DERIVED-FROM",
    "CONDITIONED-BY",
    "COMPETES-WITH",
    "SHARED-WITH",  # v4.5+ : cross-topic public mechanism anchoring
})

DEPRECATED_PREDICATES = frozenset({
    "GOVERNED-BY",
    "EQUIVALENT-IN-CONTEXT",
    "SUPPORTED-BY",
    "BREAKTHROUGH-VIA",
})

REQUIRED_META_FIELDS = ("zotero_key", "title", "year", "first_author")

NODE_SECTIONS = ("entities", "principles", "methods", "metrics")

# σ_y primary-metric heuristics for ultrastable-laser topic (v4.4+, Round 3).
# See topics/ultrastable-laser/_meta/scoping_principles.md v2.
PRIMARY_METRIC_PATTERNS = (
    "fractional_freq_instability",
    "fractional_frequency_instability",
    "allan_deviation",
    "mod_sigma_y",
    "mod_σ_y",
    "oadev",
    "hadamard",
)


# Allowed values for meta.primary_metric_exempt_reason
# (see docs/CONTRIBUTION_TIER_RULES.md §五)
VALID_EXEMPT_REASONS = frozenset({
    "new_principle",
    "new_method",
    "landmark_consensus",
    "psd_only",
})


def _is_primary_sigma_y_metric(metric: dict) -> bool:
    """Return True if a metric node is a σ_y primary-line metric.

    An explicit `role` field is authoritative: if set to any value other than
    'primary', heuristic inference is skipped.
    """
    role = metric.get("role")
    if isinstance(role, str) and role.strip():
        return role.strip().lower() == "primary"
    mid = (metric.get("id") or "").lower()
    name = (metric.get("name") or "").lower()
    haystack = f"{mid} {name}"
    return any(pat in haystack for pat in PRIMARY_METRIC_PATTERNS)


# ── Data collection helpers ──────────────────────────────────────────────────

class Issue:
    """A single lint issue."""

    __slots__ = ("level", "category", "file", "detail")

    def __init__(self, level: str, category: str, file: str, detail: str):
        self.level = level        # "ERROR" or "WARNING"
        self.category = category  # human-readable check name
        self.file = file          # relative path
        self.detail = detail

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "category": self.category,
            "file": self.file,
            "detail": self.detail,
        }

    def __str__(self) -> str:
        return f"[{self.level}] {self.file}: {self.detail}"


def _iter_items(section: Any) -> list[dict[str, Any]]:
    """Return a list of dicts from a YAML section that may be a list or a dict."""
    if section is None:
        return []
    if isinstance(section, list):
        return [item for item in section if isinstance(item, dict)]
    if isinstance(section, dict):
        return list(section.values()) if section else []
    return []


# ── Core scanning ────────────────────────────────────────────────────────────

def scan_files(yaml_paths: list[Path]) -> tuple[
    dict[str, list[str]],          # node_id -> [defining files]
    dict[str, list[str]],          # relation_id -> [defining files]
    dict[str, set[str]],           # relation refs: subject/object ids per file
    list[dict[str, Any]],          # all relations (with file info)
    list[dict[str, Any]],          # all nodes (with file, section info)
    dict[str, dict[str, Any]],     # file -> parsed meta
]:
    """Parse all YAML files and collect definitions and references."""

    node_defs: dict[str, list[str]] = {}          # id -> [files]
    rel_defs: dict[str, list[str]] = {}            # id -> [files]
    rel_refs: dict[str, set[str]] = {}             # file -> set of subject/object ids
    all_relations: list[dict[str, Any]] = []
    all_nodes: list[dict[str, Any]] = []
    file_metas: dict[str, dict[str, Any]] = {}

    for path in yaml_paths:
        rel_path = str(path)
        try:
            text = path.read_text(encoding="utf-8")
            doc = yaml.safe_load(text)
        except (yaml.YAMLError, OSError):
            # Silently skip unparseable files — caller handles this separately if needed
            continue

        if not isinstance(doc, dict):
            continue

        # Meta
        meta = doc.get("meta")
        if isinstance(meta, dict):
            file_metas[rel_path] = meta

        # Node definitions
        for section_key in NODE_SECTIONS:
            for item in _iter_items(doc.get(section_key)):
                node_id = item.get("id")
                if node_id is None:
                    continue
                node_defs.setdefault(node_id, []).append(rel_path)
                all_nodes.append({
                    "id": node_id,
                    "section": section_key,
                    "file": rel_path,
                    "data": item,
                })

        # Relations
        refs: set[str] = set()
        for item in _iter_items(doc.get("relations")):
            rid = item.get("id")
            if rid is not None:
                rel_defs.setdefault(rid, []).append(rel_path)
            subj = item.get("subject")
            obj = item.get("object")
            if subj:
                refs.add(subj)
            if obj:
                refs.add(obj)
            all_relations.append({**item, "_file": rel_path})

        rel_refs[rel_path] = refs

    return node_defs, rel_defs, rel_refs, all_relations, all_nodes, file_metas


# ── Individual checks ────────────────────────────────────────────────────────

def check_orphan_nodes(
    node_defs: dict[str, list[str]],
    all_relations: list[dict[str, Any]],
    file_metas: dict[str, dict[str, Any]] | None = None,
) -> list[Issue]:
    """1. Nodes never referenced by any relation subject or object.

    Tier-aware (v4.4 · Phase B): if all the files defining an orphan node are
    ``evidence`` or ``framework`` papers, the issue is demoted to ``INFO``
    (per docs/CONTRIBUTION_TIER_RULES.md §五). Only orphans from at least one
    ``breakthrough`` paper remain ``WARNING``.
    """
    referenced: set[str] = set()
    for rel in all_relations:
        subj = rel.get("subject")
        obj = rel.get("object")
        if subj:
            referenced.add(subj)
        if obj:
            referenced.add(obj)

    file_metas = file_metas or {}
    issues: list[Issue] = []
    for nid, files in sorted(node_defs.items()):
        # Relation IDs themselves are not expected as subjects/objects
        if nid.startswith("rel."):
            continue
        if nid not in referenced:
            for f in files:
                tier = str(
                    (file_metas.get(f) or {}).get("contribution_type", "")
                ).strip().lower()
                level = "WARNING" if tier == "breakthrough" else "INFO"
                detail = (
                    f"Node '{nid}' is defined but never referenced in any relation"
                )
                if level == "INFO":
                    detail += f" (tier={tier or 'unknown'}; orphan allowed per §9.1)"
                issues.append(Issue(level, "orphan-node", f, detail))
    return issues


def check_dangling_refs(
    node_defs: dict[str, list[str]],
    all_relations: list[dict[str, Any]],
) -> list[Issue]:
    """2. Relation subject/object referencing an undefined node."""
    defined_ids = set(node_defs.keys())
    issues: list[Issue] = []
    for rel in all_relations:
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        for role in ("subject", "object"):
            ref_id = rel.get(role)
            if ref_id and ref_id not in defined_ids:
                issues.append(Issue(
                    "ERROR", "dangling-ref", f,
                    f"Relation '{rid}' {role} references undefined node '{ref_id}'",
                ))
    return issues


def check_duplicate_defs(node_defs: dict[str, list[str]]) -> list[Issue]:
    """3. Same node ID defined in multiple files."""
    issues: list[Issue] = []
    for nid, files in sorted(node_defs.items()):
        if len(files) > 1:
            files_str = ", ".join(files)
            for f in files:
                issues.append(Issue(
                    "ERROR", "duplicate-def", f,
                    f"Node '{nid}' defined in multiple files: {files_str}",
                ))
    return issues


def check_duplicate_rel_ids(rel_defs: dict[str, list[str]]) -> list[Issue]:
    """4. Same relation ID used in multiple files."""
    issues: list[Issue] = []
    for rid, files in sorted(rel_defs.items()):
        if len(files) > 1:
            files_str = ", ".join(files)
            for f in files:
                issues.append(Issue(
                    "ERROR", "duplicate-rel-id", f,
                    f"Relation ID '{rid}' used in multiple files: {files_str}",
                ))
    return issues


def check_reasoning_chain_gaps(
    all_relations: list[dict[str, Any]],
    file_metas: dict[str, dict[str, Any]] | None = None,
) -> list[Issue]:
    """5. BOUNDED-BY relations without breakthrough_paths.

    Tier-aware (v4.4 · Phase B): BOUNDED-BY relations authored in ``evidence``
    or ``framework`` papers emit ``INFO`` instead of ``WARNING``
    (per docs/CONTRIBUTION_TIER_RULES.md §五 — evidence papers are not required
    to carry full breakthrough_paths). Only breakthrough-tier gaps stay WARNING.
    """
    file_metas = file_metas or {}
    issues: list[Issue] = []
    for rel in all_relations:
        if rel.get("predicate") != "BOUNDED-BY":
            continue
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        bp = rel.get("breakthrough_paths")
        if bp is None or (isinstance(bp, list) and len(bp) == 0):
            tier = str(
                (file_metas.get(f) or {}).get("contribution_type", "")
            ).strip().lower()
            level = "WARNING" if tier == "breakthrough" else "INFO"
            detail = f"BOUNDED-BY relation '{rid}' lacks breakthrough_paths"
            if level == "INFO":
                detail += f" (tier={tier or 'unknown'}; chain-gap allowed per §9.1)"
            issues.append(Issue(level, "reasoning-chain-gap", f, detail))
    return issues


def check_missing_evidence(all_relations: list[dict[str, Any]]) -> list[Issue]:
    """6. Relations without source.claim."""
    issues: list[Issue] = []
    for rel in all_relations:
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        source = rel.get("source")
        if source is None:
            issues.append(Issue(
                "WARNING", "missing-evidence", f,
                f"Relation '{rid}' has no 'source' field",
            ))
        elif isinstance(source, dict) and not source.get("claim"):
            issues.append(Issue(
                "WARNING", "missing-evidence", f,
                f"Relation '{rid}' has 'source' but no 'claim'",
            ))
    return issues


def check_missing_conditions(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """7. Principle nodes without conditions."""
    issues: list[Issue] = []
    for node in all_nodes:
        if node["section"] != "principles":
            continue
        data = node["data"]
        if not data.get("conditions"):
            issues.append(Issue(
                "WARNING", "missing-conditions", node["file"],
                f"Principle '{node['id']}' has no 'conditions' field",
            ))
    return issues


def check_missing_metric_conditions(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """8. Metrics with demonstrated_value but without conditions."""
    issues: list[Issue] = []
    for node in all_nodes:
        if node["section"] != "metrics":
            continue
        data = node["data"]
        dv = data.get("demonstrated_value")
        if not isinstance(dv, dict):
            continue
        if not dv.get("conditions"):
            issues.append(Issue(
                "WARNING", "missing-metric-conditions", node["file"],
                f"Metric '{node['id']}' has demonstrated_value without 'conditions'",
            ))
    return issues


def check_invalid_predicates(all_relations: list[dict[str, Any]]) -> list[Issue]:
    """9. Relations using deprecated predicates."""
    issues: list[Issue] = []
    for rel in all_relations:
        pred = rel.get("predicate", "")
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        if pred in DEPRECATED_PREDICATES:
            issues.append(Issue(
                "ERROR", "invalid-predicate", f,
                f"Relation '{rid}' uses deprecated predicate '{pred}'",
            ))
    return issues


def check_invalid_id_prefix(all_nodes: list[dict[str, Any]]) -> list[Issue]:
    """10. Node IDs that don't start with a valid prefix."""
    issues: list[Issue] = []
    for node in all_nodes:
        nid = node["id"]
        if not nid.startswith(VALID_PREFIXES):
            issues.append(Issue(
                "ERROR", "invalid-id-prefix", node["file"],
                f"Node ID '{nid}' does not start with a valid prefix ({', '.join(VALID_PREFIXES)})",
            ))
    return issues


# ── SHARED-WITH checks (v4.5+) ──────────────────────────────────────────────

def _load_tier2_registry(repo: Path) -> set[str]:
    """Parse `topics/shared/registry.md` §3 Tier 2 and return the set of
    node IDs registered there.

    Tier 2 table has a pipe-delimited row whose first `|`-enclosed cell is a
    backticked node ID. We tolerate missing files by returning an empty set,
    which causes all SHARED-WITH usage to fail lint — the intended default
    for a misconfigured repo.
    """
    registry = repo / "topics" / "shared" / "registry.md"
    if not registry.is_file():
        return set()
    try:
        text = registry.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()

    ids: set[str] = set()
    in_tier2 = False
    for line in text.splitlines():
        stripped = line.strip()
        # Section boundaries: any "## " header toggles state
        if stripped.startswith("## "):
            # Robustly match "## 3." or lines containing "Tier 2"
            if "Tier 2" in stripped or stripped.startswith("## 3"):
                in_tier2 = True
            else:
                in_tier2 = False
            continue
        if not in_tier2:
            continue
        if not stripped.startswith("|"):
            continue
        # Table rows — first cell is the ID wrapped in backticks
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        # Skip header / separator rows
        if first.startswith("---") or first.startswith(":---"):
            continue
        if first.startswith("`") and first.endswith("`"):
            ids.add(first.strip("`"))
    return ids


def _file_topic(file_path: str) -> str | None:
    """Extract the topic directory from a `topics/<topic>/papers/...` path."""
    norm = file_path.replace("\\", "/")
    parts = norm.split("/")
    if "topics" in parts:
        idx = parts.index("topics")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def check_shared_with(
    all_relations: list[dict[str, Any]],
    all_nodes: list[dict[str, Any]],
    node_defs: dict[str, list[str]],
    repo: Path,
) -> list[Issue]:
    """13. SHARED-WITH usage rules (v4.5+).

    Three rules:
      a. object must be registered in `topics/shared/registry.md` §3 Tier 2
      b. subject and object must belong to different topics
      c. subject and object must both be `pri.*` or `meth.*`
    """
    issues: list[Issue] = []
    tier2 = _load_tier2_registry(repo)

    # Map node_id -> topic of its first defining file (if any)
    node_topic: dict[str, str | None] = {}
    for nid, files in node_defs.items():
        if files:
            node_topic[nid] = _file_topic(files[0])

    for rel in all_relations:
        if rel.get("predicate") != "SHARED-WITH":
            continue
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        subj = rel.get("subject", "") or ""
        obj = rel.get("object", "") or ""

        # Rule c: prefix must be pri./meth. on both ends
        for role, ref in (("subject", subj), ("object", obj)):
            if not ref.startswith(("pri.", "meth.")):
                issues.append(Issue(
                    "ERROR", "shared-with-invalid-type", f,
                    f"SHARED-WITH relation '{rid}' {role} '{ref}' is not a "
                    f"pri.* or meth.* node (SHARED-WITH is only for principles/methods)",
                ))

        # Rule a: object must be in Tier 2 registry
        if obj and obj not in tier2:
            issues.append(Issue(
                "ERROR", "shared-with-object-not-in-registry", f,
                f"SHARED-WITH relation '{rid}' object '{obj}' is not "
                f"registered in topics/shared/registry.md §3 Tier 2",
            ))

        # Rule b: cross-topic requirement
        subj_topic = node_topic.get(subj) or _file_topic(f)
        obj_topic = node_topic.get(obj)
        if subj_topic and obj_topic and subj_topic == obj_topic:
            issues.append(Issue(
                "WARNING", "shared-with-same-topic", f,
                f"SHARED-WITH relation '{rid}' subject and object are both in "
                f"topic '{subj_topic}'; same-topic reuse should stay implicit "
                f"(Tier 1), SHARED-WITH is for cross-topic anchoring",
            ))

    return issues


# ── limit_status checks (v4.5+, BOUNDED-BY) ─────────────────────────────────

VALID_LIMIT_STATUS = frozenset({"active", "conditional", "resolved", "refuted"})


def check_limit_status(
    all_relations: list[dict[str, Any]],
    node_defs: dict[str, list[str]],
) -> list[Issue]:
    """14. BOUNDED-BY `limit_status` field (v4.5+).

    Rules:
      - If `limit_status` present, value must be one of VALID_LIMIT_STATUS
      - If `limit_status == 'resolved'`, `resolved_by` MUST be a non-empty list
        of pri.* / meth.* node IDs
      - If any `breakthrough_paths[].status == 'demonstrated'`, the parent
        BOUNDED-BY relation SHOULD carry `limit_status: resolved` (INFO nudge)
    """
    issues: list[Issue] = []
    defined = set(node_defs.keys())

    for rel in all_relations:
        if rel.get("predicate") != "BOUNDED-BY":
            continue
        f = rel.get("_file", "?")
        rid = rel.get("id", "?")
        ls = rel.get("limit_status")
        if ls is not None:
            ls_norm = str(ls).strip().lower()
            if ls_norm not in VALID_LIMIT_STATUS:
                issues.append(Issue(
                    "ERROR", "invalid-limit-status", f,
                    f"BOUNDED-BY '{rid}' limit_status='{ls}' not in "
                    f"{sorted(VALID_LIMIT_STATUS)}",
                ))
            elif ls_norm == "resolved":
                rb = rel.get("resolved_by")
                if not isinstance(rb, list) or not rb:
                    issues.append(Issue(
                        "ERROR", "limit-status-resolved-missing-resolved-by", f,
                        f"BOUNDED-BY '{rid}' limit_status='resolved' requires "
                        f"non-empty 'resolved_by' list of pri.*/meth.* node IDs",
                    ))
                else:
                    for item in rb:
                        if not isinstance(item, str):
                            continue
                        if not item.startswith(("pri.", "meth.")):
                            issues.append(Issue(
                                "ERROR", "limit-status-resolved-by-bad-ref", f,
                                f"BOUNDED-BY '{rid}' resolved_by entry '{item}' "
                                f"must be pri.* or meth.*",
                            ))
                        elif item not in defined:
                            issues.append(Issue(
                                "ERROR", "limit-status-resolved-by-dangling", f,
                                f"BOUNDED-BY '{rid}' resolved_by '{item}' is "
                                f"not defined in any YAML",
                            ))
        # Nudge: demonstrated breakthrough_path without resolved status
        bp = rel.get("breakthrough_paths")
        if isinstance(bp, list) and bp:
            has_demonstrated = any(
                isinstance(p, dict)
                and str(p.get("status", "")).strip().lower() == "demonstrated"
                for p in bp
            )
            if has_demonstrated:
                ls_norm = str(rel.get("limit_status") or "").strip().lower()
                if ls_norm not in ("resolved", "refuted"):
                    issues.append(Issue(
                        "INFO", "limit-status-missing-resolved-nudge", f,
                        f"BOUNDED-BY '{rid}' has a breakthrough_path with "
                        f"status='demonstrated' but limit_status is not "
                        f"'resolved'; consider updating (SCHEMA §4.2, v4.5+)",
                    ))
    return issues


# ── instance_of checks (v4.5+, Level 2 entities) ────────────────────────────

def check_instance_of(
    all_nodes: list[dict[str, Any]],
    all_relations: list[dict[str, Any]],
) -> list[Issue]:
    """15. Optional `instance_of` field on entity nodes (v4.5+).

    If an entity node declares `instance_of: <parent_ent_id>`, a matching
    `PART-OF <parent_ent_id>` relation with the entity as subject MUST also
    exist. This keeps the instance relationship first-class in the relation
    graph without introducing a new predicate.
    """
    issues: list[Issue] = []

    # Build set of (subject, object) pairs for PART-OF relations
    part_of_pairs: set[tuple[str, str]] = set()
    for rel in all_relations:
        if rel.get("predicate") != "PART-OF":
            continue
        s = rel.get("subject")
        o = rel.get("object")
        if isinstance(s, str) and isinstance(o, str):
            part_of_pairs.add((s, o))

    for node in all_nodes:
        if node["section"] != "entities":
            continue
        data = node["data"]
        parent = data.get("instance_of")
        if not parent:
            continue
        if not isinstance(parent, str) or not parent.startswith("ent."):
            issues.append(Issue(
                "ERROR", "instance-of-invalid", node["file"],
                f"Entity '{node['id']}' has instance_of='{parent}' which is "
                f"not an ent.* node ID",
            ))
            continue
        nid = node["id"]
        if (nid, parent) not in part_of_pairs:
            issues.append(Issue(
                "WARNING", "instance-of-missing-part-of", node["file"],
                f"Entity '{nid}' declares instance_of: {parent} but no "
                f"matching 'PART-OF {parent}' relation exists",
            ))
    return issues


def check_missing_meta(
    yaml_paths: list[Path],
    file_metas: dict[str, dict[str, Any]],
) -> list[Issue]:
    """11. YAML files missing required meta fields."""
    issues: list[Issue] = []
    for path in yaml_paths:
        rel_path = str(path)
        meta = file_metas.get(rel_path)
        if meta is None:
            issues.append(Issue(
                "WARNING", "missing-meta", rel_path,
                "File has no 'meta' section",
            ))
            continue
        for field in REQUIRED_META_FIELDS:
            if not meta.get(field):
                issues.append(Issue(
                    "WARNING", "missing-meta", rel_path,
                    f"Meta section missing required field '{field}'",
                ))
    return issues


def check_breakthrough_primary_metric(
    yaml_paths: list[Path],
    file_metas: dict[str, dict[str, Any]],
) -> list[Issue]:
    """12. ultrastable-laser breakthrough papers must link at least one σ_y primary metric.

    Rationale (Round 3, scoping_principles.md v2): the σ_y-first principle says
    a paper can only be tagged `breakthrough` if it refreshes σ_y(τ=1 s) —
    therefore it MUST define (or reference) a primary-role σ_y metric.

    A paper passes the check if it satisfies either:
      (a) defines a metric node with role: primary (or matching heuristic), OR
      (b) its relations reference an external metric whose ID matches the
          primary-metric heuristic (cross-file reuse of an existing σ_y metric).
    """
    issues: list[Issue] = []

    for path in yaml_paths:
        rel_path = str(path)
        # Only apply to ultrastable-laser topic
        if "ultrastable-laser" not in rel_path.replace("\\", "/"):
            continue

        meta = file_metas.get(rel_path)
        if not meta:
            continue
        if str(meta.get("contribution_type", "")).strip().lower() != "breakthrough":
            continue

        # Tier-aware exemption: explicit meta.primary_metric_exempt_reason
        # declares why this breakthrough does not carry a σ_y primary metric
        # (e.g. new_principle / new_method / landmark_consensus / psd_only).
        # Allowed values are documented in docs/CONTRIBUTION_TIER_RULES.md §五.
        exempt = str(meta.get("primary_metric_exempt_reason") or "").strip()
        if exempt:
            if exempt.lower() not in VALID_EXEMPT_REASONS:
                issues.append(Issue(
                    "WARNING", "invalid-exempt-reason", rel_path,
                    f"meta.primary_metric_exempt_reason='{exempt}' is not one of "
                    f"{sorted(VALID_EXEMPT_REASONS)}; see CONTRIBUTION_TIER_RULES.md §五",
                ))
            continue

        # Re-load doc to inspect metrics + relations
        try:
            doc = yaml.safe_load(Path(rel_path).read_text(encoding="utf-8"))
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(doc, dict):
            continue

        has_primary = False
        for met in _iter_items(doc.get("metrics")):
            if _is_primary_sigma_y_metric(met):
                has_primary = True
                break

        if not has_primary:
            # Check if relations reference an external primary-looking metric ID
            for rel in _iter_items(doc.get("relations")):
                for field in ("subject", "object"):
                    ref = (rel.get(field) or "").lower()
                    if ref.startswith("met.") and any(
                        pat in ref for pat in PRIMARY_METRIC_PATTERNS
                    ):
                        has_primary = True
                        break
                if has_primary:
                    break

        if not has_primary:
            issues.append(Issue(
                "WARNING", "breakthrough-missing-primary-metric", rel_path,
                "ultrastable-laser 'breakthrough' paper has no σ_y primary-role metric "
                "(neither defined locally with role: primary nor referenced via relations). "
                "See topics/ultrastable-laser/_meta/scoping_principles.md v2.",
            ))

    return issues


# ── Orchestration ────────────────────────────────────────────────────────────

def collect_yaml_paths(repo: Path, topic: str | None) -> list[Path]:
    """Gather all topics/*/papers/*.yaml paths, optionally filtered to one topic."""
    pattern = f"topics/{topic}/papers/*.yaml" if topic else "topics/*/papers/*.yaml"
    paths = sorted(repo.glob(pattern))
    return paths


def run_all_checks(
    yaml_paths: list[Path],
    repo: Path | None = None,
) -> list[Issue]:
    """Run every check and return a flat list of issues."""
    node_defs, rel_defs, rel_refs, all_relations, all_nodes, file_metas = scan_files(yaml_paths)

    issues: list[Issue] = []
    issues.extend(check_orphan_nodes(node_defs, all_relations, file_metas))
    issues.extend(check_dangling_refs(node_defs, all_relations))
    issues.extend(check_duplicate_defs(node_defs))
    issues.extend(check_duplicate_rel_ids(rel_defs))
    issues.extend(check_reasoning_chain_gaps(all_relations, file_metas))
    issues.extend(check_missing_evidence(all_relations))
    issues.extend(check_missing_conditions(all_nodes))
    issues.extend(check_missing_metric_conditions(all_nodes))
    issues.extend(check_invalid_predicates(all_relations))
    issues.extend(check_invalid_id_prefix(all_nodes))
    issues.extend(check_missing_meta(yaml_paths, file_metas))
    issues.extend(check_breakthrough_primary_metric(yaml_paths, file_metas))
    if repo is not None:
        issues.extend(check_shared_with(all_relations, all_nodes, node_defs, repo))
        issues.extend(check_limit_status(all_relations, node_defs))
        issues.extend(check_instance_of(all_nodes, all_relations))
    return issues


# ── Output formatting ────────────────────────────────────────────────────────

def format_grouped(issues: list[Issue], summary_only: bool) -> str:
    """Pretty-print issues grouped by category."""
    if not issues:
        return "✅  No issues found."

    by_cat: dict[str, list[Issue]] = {}
    for issue in issues:
        by_cat.setdefault(issue.category, []).append(issue)

    lines: list[str] = []
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")
    infos = sum(1 for i in issues if i.level == "INFO")

    for cat in sorted(by_cat):
        group = by_cat[cat]
        levels = {i.level for i in group}
        if "ERROR" in levels:
            level_tag = "ERROR"
        elif "WARNING" in levels:
            level_tag = "WARNING"
        else:
            level_tag = "INFO"
        n_err = sum(1 for i in group if i.level == "ERROR")
        n_warn = sum(1 for i in group if i.level == "WARNING")
        n_info = sum(1 for i in group if i.level == "INFO")
        breakdown_parts = []
        if n_err:
            breakdown_parts.append(f"{n_err} error")
        if n_warn:
            breakdown_parts.append(f"{n_warn} warn")
        if n_info:
            breakdown_parts.append(f"{n_info} info")
        breakdown = ", ".join(breakdown_parts) if breakdown_parts else str(len(group))
        lines.append(
            f"\n── {cat} ({len(group)} issues; {breakdown}, primary={level_tag}) ──"
        )
        if not summary_only:
            for issue in group:
                lines.append(f"  [{issue.level}] {issue.file}: {issue.detail}")

    lines.append(
        f"\nSummary: {errors} error(s), {warnings} warning(s), {infos} info "
        f"across {len(by_cat)} categories"
    )
    return "\n".join(lines)


def format_json(issues: list[Issue]) -> str:
    """JSON output."""
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")
    infos = sum(1 for i in issues if i.level == "INFO")
    return json.dumps({
        "errors": errors,
        "warnings": warnings,
        "info": infos,
        "issues": [i.to_dict() for i in issues],
    }, indent=2, ensure_ascii=False)


# ── CLI ──────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lint / health-check for sci-logic-kb YAML knowledge base.",
    )
    p.add_argument(
        "--repo-path", type=Path, default=Path("."),
        help="Root of the sci-logic-kb repository (default: current dir)",
    )
    p.add_argument(
        "--topic", type=str, default=None,
        help="Lint only one topic (e.g. 'ultrastable-laser')",
    )
    p.add_argument(
        "--files", nargs="+", type=Path, default=None,
        help=(
            "Lint specific files only (overrides --repo-path and --topic scanning). "
            "Accepts one or more paths to topics/*/papers/*.yaml files."
        ),
    )
    p.add_argument(
        "--strict", action="store_true",
        help="Treat warnings as errors (non-zero exit code)",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_output",
        help="Output results as JSON",
    )
    p.add_argument(
        "--summary", action="store_true",
        help="Only show summary counts, not individual issues",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.files:
        # Lint specific files provided on the command line
        yaml_paths = sorted(
            p.resolve() for p in args.files if p.exists()
        )
        if not yaml_paths:
            print(
                "No accessible YAML files found in the provided --files list.",
                file=sys.stderr,
            )
            return 1
    else:
        yaml_paths = collect_yaml_paths(args.repo_path.resolve(), args.topic)
        if not yaml_paths:
            msg = f"No YAML files found under {args.repo_path.resolve() / 'topics'}"
            if args.topic:
                msg += f" for topic '{args.topic}'"
            print(msg, file=sys.stderr)
            return 1

    repo = args.repo_path.resolve()
    issues = run_all_checks(yaml_paths, repo=repo)

    # Output
    if args.json_output:
        print(format_json(issues))
    else:
        print(format_grouped(issues, summary_only=args.summary))

    # Exit code
    errors = sum(1 for i in issues if i.level == "ERROR")
    warnings = sum(1 for i in issues if i.level == "WARNING")
    if errors > 0:
        return 1
    if args.strict and warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
