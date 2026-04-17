# Packaged Codex Surface Sync

## Metadata
- **Status:** Done
- **Sources:** CR-20260416-1424; D-20260416-1425

## User Story
As an ATHENA maintainer, I want the packaged `skills/athena` surface to reflect the working Codex Owl dispatch guidance without changing Claude-facing repo files, so the source package stays cross-agent compatible and low-risk.

## Functional Requirements
- FR-001: `skills/athena/SKILL.md` must keep the existing Claude memory-bridge/session-start guidance while adding packaged Owl dispatch wording that is valid for Codex sessions. (Sources: CR-20260416-1424; D-20260416-1425)
- FR-002: `skills/athena/agents/owl-of-athena.md` must use cross-agent dispatch wording for `write-memory` and invocation style without changing the packaged model metadata copied by Claude migration tooling. (Sources: CR-20260416-1424; D-20260416-1425)
- FR-003: This change must not modify `.claude/*`, root `README.md`, root Owl docs, or install/migration scripts. (Sources: CR-20260416-1424; D-20260416-1425)

## Acceptance Scenarios
- Given a maintainer reads the packaged `skills/athena/SKILL.md`, when they review the Owl section, then it describes the packaged Owl location and includes a Codex dispatch note without removing Claude memory-first behavior. (Verifies: FR-001)
- Given a maintainer reads the packaged Owl agent file, when they review the command list and dispatch instructions, then the wording is environment-agnostic while the `model:` line remains unchanged. (Verifies: FR-002)
- Given the tracked diff for this feature, when changed files are listed, then `.claude/*`, root `README.md`, root Owl docs, and install/migration scripts are absent from the change set. (Verifies: FR-003)

## Safety Constraints
- Do not copy the local packaged files wholesale into the source repo.
- Do not edit `.claude/*`, `README.md`, `agents/OWL-IMPLEMENTATION.md`, `scripts/migrate-all-projects.py`, or `skills/athena/scripts/install-owl.sh`.
- Treat existing validator failures in unrelated legacy docs as baseline unless this feature directly changes those files.
