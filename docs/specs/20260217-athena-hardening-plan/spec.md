# Feature Spec: 20260217-athena-hardening-plan

Status: Active
Created: 2026-02-17 15:36
Inputs: CR-20260217-1535, CR-20260217-1550
Decisions: D-20260217-1536, D-20260217-1551

## Summary
- Implement all remaining ATHENA hardening workstreams after the planning phase: traceability linting, canonical merge/check-in checklist consolidation, path-scoped staging defaults, and progress-log schema validation integrated with resume flow.

## User Stories & Acceptance

### US1: Enforce traceability integrity automatically (Priority: P1)
Narrative:
- As a maintainer, I want automated checks for `Sources`, `Verifies`, and `Implements`, so broken traceability links are caught before task closeout.

Acceptance scenarios:
1. Given PRD/spec/task docs, When traceability lint runs, Then it fails on missing/mismatched references and passes on valid links. (Verifies: FR-001)

### US2: Remove merge-sync ambiguity (Priority: P1)
Narrative:
- As a maintainer, I want one canonical merge/check-in reconciliation checklist, so operators do not execute overlapping sections inconsistently.

Acceptance scenarios:
1. Given ATHENA guidance, When merge/check-in reconciliation is reviewed, Then only one canonical checklist exists for this control point. (Verifies: FR-002)

### US3: Make safer staging the default (Priority: P1)
Narrative:
- As a maintainer, I want traceable commits to default to path-scoped staging, so unrelated files are not accidentally included.

Acceptance scenarios:
1. Given commit helper usage without explicit overrides, When staging runs, Then it stages scoped paths by default and requires explicit opt-in for broad staging. (Verifies: FR-003)

### US4: Prevent restore failures from malformed progress logs (Priority: P1)
Narrative:
- As a maintainer, I want progress-log schema validation in restore flow, so malformed `docs/progress.txt` is surfaced early.

Acceptance scenarios:
1. Given malformed progress logs, When resume prompt generation runs, Then schema errors are reported and execution stops (unless explicitly overridden). (Verifies: FR-004)
2. Given valid logs, When resume prompt generation runs, Then resume output remains available and task selection works. (Verifies: FR-004)

## Requirements

Functional requirements:
- FR-001: Add a traceability linter script that validates `Sources`, `Verifies`, and `Implements` references across `docs/PRD.md`, `docs/specs/*/spec.md`, and `docs/specs/*/tasks.md`. (Sources: CR-20260217-1535, CR-20260217-1550; D-20260217-1551)
- FR-002: Consolidate overlapping merge-sync guidance in ATHENA skill docs into one canonical merge/check-in reconciliation checklist. (Sources: CR-20260217-1535, CR-20260217-1550; D-20260217-1551)
- FR-003: Update traceable commit helper behavior to default to path-scoped staging, with explicit override for staging all changes. (Sources: CR-20260217-1535, CR-20260217-1550; D-20260217-1551)
- FR-004: Add schema validation for `docs/progress.txt` and integrate it with `print_resume_prompt.py` execution flow. (Sources: CR-20260217-1535, CR-20260217-1550; D-20260217-1551)
- FR-005: Preserve the structured hardening planning artifact at `artifacts/agentic_workflow/20260217-1535-athena-hardening-plan.json`. (Sources: CR-20260217-1535; D-20260217-1536)
- FR-006: Preserve audit-traceable planning completion history for `T-001` in feature tasks/progress artifacts. (Sources: CR-20260217-1535; D-20260217-1536)

## Edge cases
- Progress schema validation allows placeholders such as `- (none)` while still enforcing required headers and section order. (Verifies: FR-004)
- Path-scoped staging defaults do not silently skip missing paths and provide actionable errors. (Verifies: FR-003)
