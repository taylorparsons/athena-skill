# Feature Spec: 20260414-owl-memory-bridge

Status: Active
Created: 2026-04-14 13:27
Inputs: CR-20260414-1327
Decisions: D-20260414-1327

## Summary

Add `write-memory` command to owl.py. At SessionStart, after `prune-done` and `update-index`, Owl writes a Claude Code auto-memory file (`project_athena_active.md`) containing the active feature, goal, and task state. Athena reads this from memory at session start instead of re-reading `athena-index.md` and `progress.txt`. Athena calls `write-memory` at end of session to keep memory current.

## User Stories & Acceptance

### US1: Fast session start via memory (Priority: P1)
Narrative:
- As Athena, I want active project context pre-loaded in memory so I can skip reading athena-index.md and progress.txt and go directly to the active spec.

Acceptance scenarios:
1. Given a project with memory initialized and progress.txt present, When `./scripts/owl write-memory` runs, Then `project_athena_active.md` is created in the correct memory dir with valid frontmatter and active context. (Verifies: FR-001, FR-002)
2. Given memory file already newer than progress.txt, When `./scripts/owl write-memory` runs again, Then it returns "no update needed" and does not rewrite the file. (Verifies: FR-003)
3. Given a project with no memory dir initialized, When `./scripts/owl write-memory` runs, Then it returns success with "memory not initialized — skipping" and creates no files. (Verifies: FR-004)

### US2: Memory stays current through session (Priority: P1)
Narrative:
- As Athena, I want to refresh the memory file at end of session so the next session opens with accurate task state.

Acceptance scenarios:
1. Given Athena has updated progress.txt with new DONE/IN PROGRESS state, When Athena calls `./scripts/owl write-memory`, Then the memory file is rewritten with current task state. (Verifies: FR-005)

### US3: SessionStart hook includes write-memory (Priority: P1)
Narrative:
- As a user, I want write-memory to run automatically at session start so memory is always fresh without manual intervention.

Acceptance scenarios:
1. Given the updated SessionStart hook command, When a session starts, Then prune-done → update-index → write-memory all run before Claude starts. (Verifies: FR-006)

## Requirements

Functional requirements:
- FR-001: `owl.py` exposes a `write-memory` CLI command that invokes `write_memory()`. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-002: `write_memory()` writes `project_athena_active.md` to `~/.claude/projects/<encoded-repo>/memory/` with frontmatter `type: project` and body containing: active feature ID, goal, active features list, IN PROGRESS tasks, NEXT tasks, timestamp. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-003: `write_memory()` is idempotent — if memory file is newer than `progress.txt`, returns skip result without writing. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-004: `write_memory()` silently skips if the memory directory does not exist, returning success. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-005: `SKILL.md` step 6 instructs Athena to run `./scripts/owl write-memory` after updating `progress.txt` at end of session. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-006: `scripts/patch-claude-settings.py` `CORRECT_COMMAND` constant updated to include `&& ./scripts/owl write-memory` so new and patched installs get the updated SessionStart hook. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-007: `SKILL.md` step 2 updated to check memory first and skip `athena-index.md` + `progress.txt` reads when `Athena Active Context` memory is present. (Sources: CR-20260414-1327; D-20260414-1327)
- FR-008: Agent docs (`owl-of-athena.md`, `OWL-IMPLEMENTATION.md`) updated to document the `write-memory` command. (Sources: CR-20260414-1327; D-20260414-1327)
