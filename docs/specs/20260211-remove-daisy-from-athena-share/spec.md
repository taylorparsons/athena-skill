# Feature Spec: 20260211-remove-daisy-from-athena-share

Status: Done
Created: 2026-02-11 10:06
Inputs: CR-20260211-1004
Decisions: D-20260211-1005

## Summary
- Remove Daisy companion-skill references from this public ATHENA share repo so the published version is scoped only to ATHENA.

## User Stories & Acceptance

### US1: Share ATHENA-only version (Priority: P1)
Narrative:
- As the repo owner, I want this public share version to describe only ATHENA, so there is no confusion about bundled companion skills.

Acceptance scenarios:
1. Given the root docs, When a reviewer reads README and skill listing, Then only ATHENA is presented for this public version. (Verifies: FR-001, FR-002)
2. Given the public-facing docs, When searching `README.md` and `AVAILABLE_SKILLS.md`, Then no Daisy references remain. (Verifies: FR-003)

## Requirements

Functional requirements:
- FR-001: Remove Daisy companion section from `README.md`. (Sources: CR-20260211-1004; D-20260211-1005)
- FR-002: Remove Daisy optional companion entry from `AVAILABLE_SKILLS.md`. (Sources: CR-20260211-1004; D-20260211-1005)
- FR-003: Ensure no Daisy references remain in public-facing share docs (`README.md`, `AVAILABLE_SKILLS.md`). (Sources: CR-20260211-1004; D-20260211-1005)

## Edge cases
- If future users want Daisy guidance, keep it out of public-facing share docs and publish separately as an optional companion repo/doc. (Verifies: FR-003)
