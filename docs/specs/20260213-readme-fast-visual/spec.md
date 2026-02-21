# Feature Spec: 20260213-readme-fast-visual

## Metadata
- **Status:** Done
- **Created:** 2026-02-13 14:34
- **Inputs:** CR-20260213-1434, CR-20260213-1435, CR-20260213-1436, CR-20260213-1448
- **Decisions:** D-20260213-1437, D-20260213-1438, D-20260213-1448

## Summary
- Add a fast visual at the top of `README.md` using a new tracked diagram asset derived from the customer-provided image, explicitly avoiding the untracked `docs/athena-napkin-loop.svg` file.
- Scope correction: keep the new image and restore normal README prose structure (no literal style labels).

## User Stories & Acceptance

### US1: Show the ATHENA loop at first glance (Priority: P1)
Narrative:
- As a reader, I want an immediate visual at the top of the README so I can understand ATHENA flow quickly before reading detailed instructions.

Acceptance scenarios:
1. Given the README, When opened, Then a workflow image appears before or immediately under the title for quick orientation. (Verifies: FR-001)
2. Given the repo status, When checking tracked files, Then the README visual references a new tracked asset and does not reference `docs/athena-napkin-loop.svg`. (Verifies: FR-002)
3. Given the README body text, When reviewed, Then it uses standard README structure and does not include literal labels such as `context:` `tension:` `decision:` `execution:` `outcome:` `reflection:`. (Verifies: FR-003)

## Requirements

Functional requirements:
- FR-001: Add a fast visual image block at the top of `README.md`. (Sources: CR-20260213-1434; D-20260213-1437)
- FR-002: Use a new tracked README visual asset path and do not use the untracked `docs/athena-napkin-loop.svg` file. (Sources: CR-20260213-1435; D-20260213-1437)
- FR-003: Keep README body text in normal repository style for this change and remove literal style labels, while preserving existing technical accuracy and commands. (Sources: CR-20260213-1448; D-20260213-1448)

## Edge cases
- The visual must remain readable in GitHub Markdown rendering with no external dependencies. (Verifies: FR-001)
- Text cleanup must not change install commands or required file paths. (Verifies: FR-003)
