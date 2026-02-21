# PRD: Slug Utility Side-by-Side Use Case

Status: Active
Updated: 2026-02-13 11:00
Inputs: CR-20260213-1100
Decisions: D-20260213-1100

## Goals
- Build a deterministic slug utility using ATHENA workflow. (Sources: CR-20260213-1100)
- Produce evidence logs for output comparison against a RALPH-run folder. (Sources: CR-20260213-1100)

## Functional requirements
- FR-SLUG-001: Add `src/slugify.py` that reads `input.txt`, normalizes each line to kebab-case slugs, deduplicates, sorts, and writes to `output.txt`. (Sources: CR-20260213-1100; D-20260213-1100)
