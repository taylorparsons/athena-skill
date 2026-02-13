# Feature Spec: 20260212-athena-rename

Status: Done
Created: 2026-02-12 16:50
Inputs: CR-20260212-1646
Decisions: D-20260212-1647, D-20260212-1648

## Summary
- Migrate this repository's mutable skill/project identity to `athena`, including path names, install metadata, and code/documentation references, while preserving append-only historical request/decision logs.

## User Stories & Acceptance

### US1: Use ATHENA as the canonical skill name (Priority: P1)
Narrative:
- As a repository user, I want the installable skill and framework naming to use `athena`, so the repo presents one consistent identity.

Acceptance scenarios:
1. Given repository paths, When reviewed, Then install/core paths use `athena` naming. (Verifies: FR-001, FR-002)
2. Given mutable docs/code, When searched, Then references use consistent `athena` naming. (Verifies: FR-003, FR-004)
3. Given append-only audit logs, When reviewed, Then prior verbatim customer/decision text remains unchanged. (Verifies: FR-005)

## Requirements

Functional requirements:
- FR-001: Ensure mutable skill/core paths use `athena` naming. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-002: Ensure mutable project identity references use `athena-skill`. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-003: Ensure mutable code references use `athena`/`ATHENA` naming. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-004: Ensure mutable documentation references use `athena`/`ATHENA` naming. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-005: Preserve append-only historical entries in `docs/requests.md` and `docs/decisions.md`. (Sources: CR-20260212-1646; D-20260212-1648)

## Edge cases
- Legacy naming inside historical verbatim entries remains intentionally unchanged. (Verifies: FR-005)
