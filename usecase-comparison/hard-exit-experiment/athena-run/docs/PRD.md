# PRD: Harder Slug Utility Side-by-Side

Status: Active
Updated: 2026-02-13 14:00
Inputs: CR-20260213-1400
Decisions: D-20260213-1400

## Goals
- Demonstrate process persistence in a task that requires correction.
- Ensure both ATHENA and RALPH complete only after deterministic canonicalization, dedupe, sort, and report generation.

## Functional requirements
- FR-SLUG-H-001: `src/slugify.py` reads `input.txt`, slugifies each line to kebab-case, removes invalid lines, deduplicates, sorts deterministically, and writes `output.txt`. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-002: Unicode inputs are normalized before slugification. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-003: `report.json` is written with canonical summary fields and invalid-line inventory. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-004: Run metadata includes UTC start and end timestamps and runtime seconds. (Sources: CR-20260213-1400; D-20260213-1400)
