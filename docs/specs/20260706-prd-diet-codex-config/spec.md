# Feature Spec: 20260706-prd-diet-codex-config

Status: Done
Created: 2026-07-06 06:42
Inputs: CR-20260706-0642
Decisions: D-20260706-0642

## Summary
- Remove the remaining per-session token costs identified by the v2.1 A/B experiments: PRD full-read cost (new `owl prune-prd` + a never-full-read SKILL.md rule), Codex skills-listing overflow (move loose non-skill files out of ~/.codex/skills), and Codex reasoning spend (add a medium-effort `athena` profile to ~/.codex/config.toml).

## User Stories & Acceptance

### US1: PRD stays lean and is never read in full (Priority: P1)
Narrative:
- As an agent updating the PRD, I want the file bounded and the loop to forbid full reads, so that PRD cost stops growing with project age.

Acceptance scenarios:
1. Given a PRD with Metadata Inputs/Decisions link lists and shipped backlog lines, When `owl prune-prd` runs, Then those blocks move to docs/audit/prd-archive.md, pointer lines remain, and a second run is a no-op. (Verifies: FR-001)
2. Given the rewritten SKILL.md, When an agent needs the PRD, Then the instruction is to grep for the target section and read only that range, with `owl show FR-...` for single requirements. (Verifies: FR-002)

### US2: Codex session overhead reduced (Priority: P1)
Narrative:
- As the maintainer running Codex, I want the skills listing under budget and a cheaper reasoning tier for routine loop work.

Acceptance scenarios:
1. Given ~/.codex/skills contains loose non-skill files, When the cleanup runs, Then those files are moved (not deleted) to ~/.codex/skills-archive/ and an inventory is reported. (Verifies: FR-003)
2. Given ~/.codex/config.toml, When the profile is added, Then `[profiles.athena]` sets model_reasoning_effort to medium and existing config is otherwise unchanged. (Verifies: FR-004)

## Requirements

Functional requirements:
- FR-001: `owl prune-prd` archives the PRD Metadata `Inputs:`/`Decisions:` link lists and backlog lines beginning with Shipped/Implemented/Planned markers to docs/audit/prd-archive.md, leaving pointer lines; idempotent; unit-tested. (Sources: CR-20260706-0642; D-20260706-0642)
- FR-002: SKILL.md forbids full PRD reads: grep to locate the sections being changed, read only those ranges, `owl show FR-...` for single requirements; packaged and root copies stay in sync and both installs are refreshed. (Sources: CR-20260706-0642; D-20260706-0642)
- FR-003: Loose non-skill files in ~/.codex/skills are moved to ~/.codex/skills-archive/; skill directories without SKILL.md are reported for user review but not moved. (Sources: CR-20260706-0642; D-20260706-0642)
- FR-004: ~/.codex/config.toml gains `[profiles.athena]` with `model_reasoning_effort = "medium"`; plugin inventory reported to the user without disabling anything. (Sources: CR-20260706-0642; D-20260706-0642)
- FR-005: Version bumped to 2.2.0 with a CHANGELOG entry; package reinstalled to ~/.claude/skills/athena and ~/.codex/skills/athena. (Sources: CR-20260706-0642; D-20260706-0642)

## Edge cases
- PRD without Metadata link lists or shipped backlog lines: prune-prd reports nothing to prune, exits success. (Verifies: FR-001)
- Backlog line citing an active feature id: left in place. (Verifies: FR-001)
- config.toml already containing [profiles.athena]: profile write is skipped with a message. (Verifies: FR-004)
