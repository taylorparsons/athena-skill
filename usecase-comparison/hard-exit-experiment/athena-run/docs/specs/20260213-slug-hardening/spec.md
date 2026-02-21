# Feature Spec: 20260213-slug-hardening

Status: Active
Created: 2026-02-13 14:00
Inputs: CR-20260213-1400
Decisions: D-20260213-1400

## Summary
This feature hardens slug generation and proof artifacts for a persistence comparison.

## User Stories & Acceptance

### US1: Deterministic slug file output (Priority: P1)
Narrative:
- As a reviewer, I want deterministic canonical slugs so comparisons across iterations are meaningful.

Acceptance scenario:
1. Given noisy and Unicode-heavy input, when the script runs, then `output.txt` is deduplicated and sorted. (Verifies: FR-SLUG-H-001)

### US2: Validation report (Priority: P1)
Narrative:
- As a reviewer, I want a machine-readable artifact showing what was valid/invalid.

Acceptance scenario:
1. Given a run, when it completes, then `report.json` includes line totals and unicode normalization count. (Verifies: FR-SLUG-H-003)

## Requirements

- FR-SLUG-H-001: read input, normalize non-alnum to dash, dedupe, sort, write output. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-002: preserve deterministic output for Unicode and punctuation noise. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-003: emit summary report fields: generated_at, source_file, total_lines, valid_lines, invalid_lines, output_count, unique_count, duplicates_removed, unicode_normalized_count. (Sources: CR-20260213-1400; D-20260213-1400)
- FR-SLUG-H-004: emit run timing in metadata. (Sources: CR-20260213-1400; D-20260213-1400)
