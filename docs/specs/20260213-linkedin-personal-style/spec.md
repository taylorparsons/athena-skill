# Feature Spec: 20260213-linkedin-personal-style

## Metadata
- **Status:** Done
- **Created:** 2026-02-13 20:01
- **Inputs:** CR-20260213-1958
- **Decisions:** D-20260213-1959

## Summary
- Add one additional LinkedIn-ready ATHENA post draft that uses the maintainer's personal writing style: direct, structured, grounded, operator-focused, and low-hype, while preserving concrete setup and loop execution clarity.

## User Stories & Acceptance

### US1: Publish an honest, usable version in personal style (Priority: P1)
Narrative:
- As the maintainer, I want a personal-style variant that still reads like a practical execution guide, so readers get both honesty and usable instructions.

Acceptance scenarios:
1. Given the new personal-style draft, When reviewed, Then it reflects direct/no-fluff language and framework-oriented sections (problem, constraints, decision, evidence, confidence). (Verifies: FR-001, FR-002)
2. Given the same draft, When reviewed, Then it includes ATHENA invoke -> request -> loop -> check-in flow plus Codex/Claude copy/paste setup blocks. (Verifies: FR-003, FR-004)

## Requirements

Functional requirements:
- FR-001: Add one new LinkedIn-ready draft in `publishing/` distinct from v1 and v2. (Sources: CR-20260213-1958; D-20260213-1959)
- FR-002: Use personal-style traits from the request: direct language, structured reasoning, grounded reflection, operator mindset, and low-marketing tone. (Sources: CR-20260213-1958; D-20260213-1959)
- FR-003: Include ATHENA logical flow from invocation and request capture through loop execution to check-in completion. (Sources: CR-20260213-1958; D-20260213-1959)
- FR-004: Include Codex and Claude setup/install copy/paste blocks. (Sources: CR-20260213-1958; D-20260213-1959)

## Edge cases
- Keep style authentic without becoming vague; every claim should map to a concrete action or artifact. (Verifies: FR-002, FR-003)
