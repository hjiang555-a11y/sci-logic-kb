# Shared / Cross-Topic Nodes — Architecture

> This directory holds nodes referenced by ≥2 topics.
> Shared nodes have no topic namespace prefix.

## Purpose

When a principle, method, or metric is referenced by multiple topics, it should be
defined once in `topics/shared/` and referenced via `SHARED-WITH` relations from
each topic.

## Candidates for Shared Nodes

### Mathematical Foundations
- Allan deviation family (ADEV, MDEV, TDEV, Hadamard)
- Phase noise spectral density models
- Noise type classification (white PM, flicker PM, white FM, flicker FM, random walk FM)

### Common Methods
- PDH locking (currently in ultrastable-laser, also used in frequency-standards)
- Phase-locked loop techniques
- Heterodyne beat note measurement

### Common Principles
- Shot noise limit
- Thermal noise (Fluctuation-Dissipation Theorem) — generic form
- Quantum projection noise limit

## Status: Not yet populated

Shared nodes will be migrated when ≥2 topics reference the same concept.
