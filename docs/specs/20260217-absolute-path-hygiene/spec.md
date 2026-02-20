# Feature Spec: 20260217-absolute-path-hygiene

## Metadata
- **Status:** Done
- **Created:** 2026-02-17 14:52
- **Inputs:** CR-20260217-1451
- **Decisions:** D-20260217-1452

## Summary
- Remove remaining absolute-path residues from tracked ATHENA docs so repository security audit no longer reports `HIGH` path findings.

## User Stories & Acceptance

### US1: Keep tracked docs path-hygienic (Priority: P1)
Narrative:
- As a maintainer, I want audit-facing docs free of local absolute path tokens, so security audits stay green for path hygiene.

Acceptance scenarios:
1. Given tracked ATHENA docs, When searching for user-home absolute path tokens, Then no literal local home-directory path tokens remain. (Verifies: FR-001)
2. Given repository security audit, When it runs after remediation, Then no `HIGH` absolute-path finding is reported. (Verifies: FR-002)

## Requirements

Functional requirements:
- FR-001: Remove literal local absolute-path tokens from tracked docs that trigger path hygiene checks. (Sources: CR-20260217-1451; D-20260217-1452)
- FR-002: Verify path-hygiene remediation using `audit_repository_security.py`. (Sources: CR-20260217-1451; D-20260217-1452)
