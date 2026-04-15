# Design: Rename INDEX.md to athena-index.md

**Date:** 2026-04-14  
**Input:** CR-20260414-1100  
**Status:** Approved

## Problem

`docs/INDEX.md` collides with existing `index.md` files in mature repos (confirmed: `agentic-browser` already has a `docs/index.md` for its own documentation). The name `INDEX.md` is too generic to safely install globally.

## Decision

Rename to `docs/athena-index.md` (kebab-case, matches repo conventions).

## Scope

### Files changed (functional)
| File | Change |
|---|---|
| `docs/INDEX.md` | Renamed to `docs/athena-index.md` |
| `scripts/owl.py` | Line 19: `self.index_path = self.docs_dir / "athena-index.md"` |
| `scripts/hooks/pre-commit` | `INDEX_FILE` variable + messages + `git add` path |
| `scripts/hooks/post-commit` | `git diff` + `git add` paths + messages |

### Files changed (documentation + strings)
| File | Change |
|---|---|
| `README.md` | All 22 references; existing-project section gets single-prompt fast path |
| `SKILL.md` | Load instruction references |
| `skills/athena/SKILL.md` | Load instruction references |
| `agents/owl-of-athena.md` | All references |
| `.claude/agents/owl-of-athena.md` | All references |
| `agents/OWL-IMPLEMENTATION.md` | All references |
| `docs/INDEX-TEST-RESULTS.md` | All references |
| `scripts/install-hooks.sh` | Output message references |
| `scripts/patch-claude-settings.py` | CLAUDE.md trigger string references |
| `docs/progress.txt` | Active session references only |

### Files untouched
- `docs/requests.md` — append-only
- `docs/progress-archive.txt` — historical record, intentionally preserved with old name
- `docs/decisions.md` — append-only
- `settings.json` hook commands — call `./scripts/owl` by command name, not filename

## Key Design Decisions

**No migration script.** Feature was never released publicly. Only two projects had `docs/INDEX.md`: this repo and `my_LLC` (which is being reverted). Clean rename with no backward-compat shim.

**`settings.json` hook commands unchanged.** Both `SessionStart` and `Stop` hooks call `./scripts/owl prune-done` and `./scripts/owl update-index` — they reference the command, not the file. No change needed.

**`progress-archive.txt` untouched.** Historical session logs preserve original filenames as written. Only `progress.txt` (active multi-session state) gets updated references.

## README: Existing Project Bootstrap

The current 5-step manual process gets a single-prompt fast path added above it:

```
Bootstrap Owl of Athena in this project. Run ./scripts/owl update-index to generate docs/athena-index.md, run ./scripts/install-hooks.sh to install git hooks, run ./scripts/owl prune-done to clean progress.txt, then commit the results.
```

The 5 manual steps remain below as the explicit path for users who want control over each decision point.

## Acceptance Criteria

- `./scripts/owl update-index` creates `docs/athena-index.md`, not `docs/INDEX.md`
- `./scripts/owl prune-done` reads and writes correctly
- `pre-commit` hook validates `docs/athena-index.md` sync
- `post-commit` hook stages `docs/athena-index.md` on feature completion
- No references to `docs/INDEX.md` remain in functional code or current docs
- `docs/progress-archive.txt` still contains original `INDEX.md` references (intentional)
