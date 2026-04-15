---
Feature: 20260415-version-bump-2-0-0
Status: Done
---

# Version Bump to 2.0.0

## Summary

Bump the Athena framework version from 1.2.1 to 2.0.0 to reflect the major changes shipped since the last release (Owl of Athena agent, athena-index.md token optimization, memory bridge, sweeper, fleet migration).

## Functional Requirements

### FR-001 — VERSION file updated
Update `VERSION` to `2.0.0`.
(Sources: CR-20260415-0900)

### FR-002 — CHANGELOG entry added
Add a `v2.0.0` section to `CHANGELOG.md` summarizing major features since v1.2.1.
(Sources: CR-20260415-0900)

## Acceptance Scenarios

### Scenario 1 — VERSION reads 2.0.0
**Given** the repository root  
**When** I read `VERSION`  
**Then** the content is `2.0.0`  
(Verifies: FR-001)

### Scenario 2 — CHANGELOG has v2.0.0 section
**Given** `CHANGELOG.md`  
**When** I search for `v2.0.0`  
**Then** an entry exists with at least one bullet  
(Verifies: FR-002)
