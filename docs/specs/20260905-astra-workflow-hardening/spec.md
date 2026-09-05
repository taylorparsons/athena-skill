# Feature Spec: 20260905-astra-workflow-hardening

Status: Done
Created: 2026-09-05 11:01
Inputs: CR-20260905-1100
Decisions: D-20260905-1101

## Summary
- Apply the review recommendations while retaining traceability and permission boundaries. No remote publication or model benchmark is included.

## User Stories & Acceptance

### US1: Resume authorized work without instruction conflicts (Priority: P1)

Acceptance scenarios:
1. Given a review request, the skill routes to read-only inspection without requesting audit writes or implementation. (Verifies: FR-ATHENA-037)
2. Given authorized implementation, tasks proceed sequentially until complete or genuinely blocked, with explicit commit paths and no unrequested push. (Verifies: FR-ATHENA-037)
3. Given interrupted work, context includes live Git state and the latest recorded operational fields, labels missing fields unknown, and does not treat history as permission. (Verifies: FR-ATHENA-038)
4. Given missing Git, a non-repository directory, stale notes or oversized output, recovery remains read-only and reports uncertainty or truncation. (Verifies: FR-ATHENA-038)
5. Given drift between root and install resources, the parity regression fails; behavioral evaluation instructions distinguish measured results from unrun cases. (Verifies: FR-ATHENA-039)

## Requirements

- FR-ATHENA-037: Maintain one canonical workflow, a read-only route, scoped continuation and explicit commit paths. (Sources: CR-20260905-1100; D-20260905-1101)
- FR-ATHENA-038: Recover live Git state and latest-note operational fields with unknown defaults and permission boundaries. (Sources: CR-20260905-1100; D-20260905-1101)
- FR-ATHENA-039: Add regression coverage, package parity checks and a behavioral evaluation protocol. (Sources: CR-20260905-1100; D-20260905-1101)
