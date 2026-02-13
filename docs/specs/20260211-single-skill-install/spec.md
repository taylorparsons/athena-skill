# Feature Spec: 20260211-single-skill-install

Status: Done
Created: 2026-02-11 14:00
Inputs: CR-20260211-1358
Decisions: D-20260211-1400

## Summary
- Keep public installation deterministic by exposing only one installable skill target (`skills/athena`) and documenting only that path.

## User Stories & Acceptance

### US1: Install only the intended skill package (Priority: P1)
Narrative:
- As a user installing from GitHub, I want one explicit install target for `athena`, so the installer does not pull unintended content.

Acceptance scenarios:
1. Given the repository docs, When a user follows install instructions, Then only `skills/athena` is referenced. (Verifies: FR-001, FR-002)
2. Given install-target validation, When run locally or in CI, Then only `skills/athena` is required and validated. (Verifies: FR-003)

## Requirements

Functional requirements:
- FR-001: Keep only `skills/athena` as the packaged install target in the repository. (Sources: CR-20260211-1358; D-20260211-1400)
- FR-002: Document only `athena` install instructions in `README.md` and `AVAILABLE_SKILLS.md`. (Sources: CR-20260211-1358; D-20260211-1400)
- FR-003: Validate only `skills/athena` via `scripts/validate_install_targets.py` and CI workflow. (Sources: CR-20260211-1358; D-20260211-1400)

## Edge cases
- Explicitly warn against `--path .` in docs to prevent whole-repo installs. (Verifies: FR-002)
