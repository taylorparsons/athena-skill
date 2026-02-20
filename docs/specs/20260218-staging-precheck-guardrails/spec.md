# Feature Spec: 20260218-staging-precheck-guardrails

## Metadata
- **Status:** Done
- **Created:** 2026-02-18 11:00
- **Inputs:** CR-20260218-1059
- **Decisions:** D-20260218-1100

## Summary
- Restore broad staging workflow in traceable commits while adding pre-stage guardrails for risky files.

## User Stories & Acceptance

### US1: Keep broad staging without accidental risky files (Priority: P1)
Narrative:
- As a maintainer, I want broad staging to stay convenient while blocking risky files, so I can keep commits clean without manually curating every run.

Acceptance scenarios:
1. Given commit helper invocation without `--paths`/`--docs-only`, When staging runs, Then helper stages all changes only after pre-stage checks pass. (Verifies: FR-001)
2. Given staged candidates that include `.DS_Store`, temp/cache files, likely secrets, or large artifacts, When helper runs, Then it exits with actionable errors before staging. (Verifies: FR-002)
3. Given user needs scoped behavior, When `--docs-only` is passed, Then helper stages only ATHENA docs defaults. (Verifies: FR-003)

## Requirements

Functional requirements:
- FR-001: Default commit helper staging mode must be broad staging (`git add -A`) when no explicit path mode is selected. (Sources: CR-20260218-1059; D-20260218-1100)
- FR-002: Commit helper must run pre-stage checks that block `.DS_Store`, common temp/cache patterns, likely secret markers, and large artifacts before staging. (Sources: CR-20260218-1059; D-20260218-1100)
- FR-003: Commit helper must support scoped alternatives with explicit paths (`--paths`) and legacy docs-only mode (`--docs-only`). (Sources: CR-20260218-1059; D-20260218-1100)

## Edge cases
- Pre-stage checks must evaluate both modified tracked files and untracked files before broad staging. (Verifies: FR-002)
- Deleted files should not trigger false positives during pre-stage checks. (Verifies: FR-002)
