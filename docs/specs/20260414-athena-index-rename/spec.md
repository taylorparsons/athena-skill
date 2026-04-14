# Feature Spec: 20260414-athena-index-rename

**Status:** Active  
**Created:** 2026-04-14 11:00  
**Inputs:** CR-20260414-1100  
**Decisions:** D-20260414-1100

## Summary

Rename `docs/INDEX.md` to `docs/athena-index.md` across all functional code, git hooks, and documentation to prevent filename collisions in mature repos that already use `index.md` for their own purposes. The change is a targeted rename with no logic changes — one constant in `owl.py` drives all downstream behavior.

## User Stories & Acceptance

### US1: Safe global install (Priority: P1)
Narrative:
- As an ATHENA user with a mature repo, I want Owl to use `docs/athena-index.md` so that it never collides with my project's existing `docs/index.md`.

Acceptance scenarios:
1. Given a project with an existing `docs/index.md`, When `./scripts/owl update-index` runs, Then it creates `docs/athena-index.md` and leaves `docs/index.md` untouched. (Verifies: FR-001)
2. Given `docs/athena-index.md` exists, When the `pre-commit` hook runs, Then it validates `docs/athena-index.md` sync — not `docs/INDEX.md`. (Verifies: FR-002)
3. Given a completed feature commit, When the `post-commit` hook fires, Then it stages `docs/athena-index.md` — not `docs/INDEX.md`. (Verifies: FR-002)

### US2: Clean documentation (Priority: P2)
Narrative:
- As a new ATHENA installer, I want README and SKILL.md to reference `athena-index.md` consistently so that I copy the correct filename without confusion.

Acceptance scenarios:
1. Given the README install instructions, When I follow them, Then every reference to the index file uses `athena-index.md`. (Verifies: FR-003)
2. Given `docs/progress-archive.txt`, When I read it, Then it still contains original `INDEX.md` references as historical record. (Verifies: FR-004)

## Requirements

**Functional requirements:**
- FR-001: `owl.py` uses `docs/athena-index.md` as the index path for all operations (update-index, prune-done, archive, retrieve, search). (Sources: CR-20260414-1100; D-20260414-1100)
- FR-002: Git hook scripts (`pre-commit`, `post-commit`) reference `docs/athena-index.md` in all functional path variables and `git add` / `git diff` calls. (Sources: CR-20260414-1100; D-20260414-1100)
- FR-003: All documentation files (README.md, SKILL.md x2, agent files, OWL-IMPLEMENTATION.md, INDEX-TEST-RESULTS.md, install-hooks.sh, patch-claude-settings.py) reference `athena-index.md`. (Sources: CR-20260414-1100; D-20260414-1100)
- FR-004: Append-only logs (`requests.md`, `decisions.md`) and historical archive (`progress-archive.txt`) are not modified. (Sources: CR-20260414-1100; D-20260414-1100)
- FR-005: `docs/progress.txt` active session references updated to `athena-index.md`. (Sources: CR-20260414-1100; D-20260414-1100)
- FR-006: README "existing project bootstrap" section presents single-prompt fast path first, followed by 5-step manual path. (Sources: CR-20260414-1100; D-20260414-1100)

## Edge Cases
- `settings.json` hook commands call `./scripts/owl` by name — no filename reference, no change needed. (Verifies: FR-001)
- `docs/progress-archive.txt` retains `INDEX.md` references intentionally as historical record. (Verifies: FR-004)
