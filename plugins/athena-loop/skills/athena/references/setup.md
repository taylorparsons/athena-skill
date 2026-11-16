# ATHENA Setup & Migration

## New or adopted repo — create the audit files

Required set (create any that are missing before other work):
- `docs/requests.md` — created automatically by the first `owl add-request`
- `docs/decisions.md` — created automatically by the first `owl add-decision`
- `docs/PRD.md` — keep minimal and factual; do not invent requirements
- `docs/TRACEABILITY.md` — copy `templates/traceability.md`
- `docs/specs/<FEATURE_ID>/spec.md` + `tasks.md` — copy `templates/spec.md` / `templates/tasks.md`

Session notes (`docs/specs/<FEATURE_ID>/notes.md`) are created automatically by the first `owl add-note` for that feature.

`docs/athena-index.md` is generated — run `./scripts/owl update-index`; never edit or read it directly.

## Adopted repo with existing Git history

Create a derived "before ATHENA" record (never fabricate customer requests — Git history is not verbatim customer input):

    python3 scripts/bootstrap_git_audit.py --out docs/audit/git-history.md

Then add a pointer to `docs/audit/git-history.md` in `docs/TRACEABILITY.md`. Verbatim requests start from the current session forward.

## Migrating a repo that still has docs/progress.txt

`progress.txt` is retired: task truth lives in each feature's `tasks.md`, session notes in each feature's `notes.md`, and the session-open summary comes from `owl context`. Convert once:

    ./scripts/owl migrate

This moves each session block into the matching feature's `notes.md`, parks unresolvable blocks in `docs/audit/progress-legacy.txt`, and deletes `progress.txt`. It is idempotent. All owl commands fall back to `progress.txt` automatically until you migrate, so migration can happen at any convenient moment — but do it before relying on `add-note`.

## Harness wiring

- **Claude Code**: a `SessionStart` hook should run `./scripts/owl prune-done`, `update-index`, and `write-memory` (see `scripts/patch-claude-settings.py`). The memory file then replaces `owl context` at session open.
- **Codex**: no hooks — the loop's step 1 (`./scripts/owl context`) does the same job. Keep `~/.codex/AGENTS.md` to trigger + stop-gates only; the loop lives in SKILL.md.
