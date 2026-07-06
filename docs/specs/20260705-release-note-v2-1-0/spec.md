# Feature Spec: 20260705-release-note-v2-1-0

Status: Done
Created: 2026-07-05 21:23
Inputs: CR-20260705-2123
Decisions: D-20260705-2123

## Summary
- Publish a release note for ATHENA v2.1.0 that states the token-usage improvement per surface with measured before/after numbers and % reductions, in Taylor style, at docs/releases/v2.1.0.md.

## User Stories & Acceptance

### US1: Shareable token-improvement release note (Priority: P1)
Narrative:
- As the maintainer, I want a release note with concrete token numbers and % reductions, so that I can announce v2.1.0 without readers needing the CHANGELOG or spec.

Acceptance scenarios:
1. Given the v2.1.0 measurements, When the note is read, Then every claimed reduction shows a before value, an after value, and a % figure, plus the measurement basis. (Verifies: FR-001)
2. Given the Taylor style profile, When scripts/validate_style.py runs on the note, Then it passes. (Verifies: FR-002)

## Requirements

Functional requirements:
- FR-001: docs/releases/v2.1.0.md states per-surface token costs before and after (session-open reads, SKILL.md, skill description, Codex AGENTS.md, fixed session overhead) with % reductions and the chars/4 measurement basis. (Sources: CR-20260705-2123; D-20260705-2123)
- FR-002: The note follows Taylor style (direct, specific, no promotional adjectives) and passes scripts/validate_style.py from the taylor-style-voice skill. (Sources: CR-20260705-2123; D-20260705-2123)

## Edge cases
- Numbers are approximations: the note must say how they were measured so they are reproducible. (Verifies: FR-001)
