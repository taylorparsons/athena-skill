# Feature Spec: 20260216-review-findings-remediation

## Metadata
- **Status:** Done
- **Created:** 2026-02-16 13:17
- **Inputs:** CR-20260216-1317
- **Decisions:** D-20260216-1318

## Summary
- Remediate findings 1-5 from the project review: traceability state drift, resume prompt placeholder parsing, markdown secret-scan coverage, local path hygiene, and git-audit output path anchoring.

## User Stories & Acceptance

### US1: Keep ATHENA state internally consistent (Priority: P1)
Narrative:
- As a maintainer, I want feature status artifacts to align with progress logs so resume/reconciliation behavior is reliable.

Acceptance scenarios:
1. Given feature `20260213-checkin-merge-remote`, When status is reconciled, Then spec/tasks reflect completion state consistent with `docs/progress.txt`. (Verifies: FR-001)

### US2: Keep helper scripts reliable for session recovery and repo adoption (Priority: P1)
Narrative:
- As a maintainer, I want helper scripts to handle placeholders and relative paths safely in normal usage.

Acceptance scenarios:
1. Given `docs/progress.txt` contains `- (none)`, When `print_resume_prompt.py` selects a task, Then it skips placeholders. (Verifies: FR-002)
2. Given `bootstrap_git_audit.py` is run from a subdirectory with a relative `--out`, When output is resolved, Then path anchoring uses the repository root. (Verifies: FR-005)

### US3: Preserve security and publication hygiene (Priority: P1)
Narrative:
- As a maintainer, I want CI scanning and tracked docs to match repository hardening requirements.

Acceptance scenarios:
1. Given markdown-heavy audit docs, When the security workflow runs, Then markdown files are included in secret-pattern scanning. (Verifies: FR-003)
2. Given tracked docs, When path hygiene is checked, Then no local absolute user-home path token remains in `docs/progress.txt`. (Verifies: FR-004)

## Requirements

Functional requirements:
- FR-001: Reconcile `docs/specs/20260213-checkin-merge-remote/spec.md` and `docs/specs/20260213-checkin-merge-remote/tasks.md` to a completed state aligned with `docs/progress.txt`. (Sources: CR-20260216-1317; D-20260216-1318)
- FR-002: Update `scripts/print_resume_prompt.py` and `skills/athena/scripts/print_resume_prompt.py` to ignore placeholder bullets like `- (none)` when selecting an active task. (Sources: CR-20260216-1317; D-20260216-1318)
- FR-003: Update `.github/workflows/security.yml` to include markdown files in secret-pattern scanning. (Sources: CR-20260216-1317; D-20260216-1318)
- FR-004: Remove remaining local absolute path residue from tracked progress notes in `docs/progress.txt`. (Sources: CR-20260216-1317; D-20260216-1318)
- FR-005: Update `scripts/bootstrap_git_audit.py` and `skills/athena/scripts/bootstrap_git_audit.py` so relative `--out` paths are resolved from repository root, not invocation subdirectories. (Sources: CR-20260216-1317; D-20260216-1318)

## Edge cases
- Progress files that use `- none` or `- (none)` placeholders should not be interpreted as actionable tasks. (Verifies: FR-002)
- Running git-audit generation from nested paths must not produce output under nested `docs/` folders by accident. (Verifies: FR-005)
