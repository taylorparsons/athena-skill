# Traceable Commits

Goal: every commit links back to the ATHENA artifacts (CR / D / FEATURE_ID / T-...).

Hard rules:
- Never run `git push` or open/submit PRs unless the user explicitly asks.
- Do not commit secrets. If found, remove them and record the incident via `owl add-note`.

## Staging modes (helper prechecks)

`scripts/commit_with_traceability.py` supports:
- Default without explicit scope is rejected unless broad staging has operator confirmation. Prefer `--paths`; checks block `.DS_Store`, common temp/cache paths, likely secrets, and large artifacts.
- `--paths <p1> <p2> ...` — explicit scope.
- `--docs-only` — stage only the ATHENA traceability docs (spec/tasks/notes/PRD/TRACEABILITY/requests/decisions).
- `--all-changes` requests broad staging; the current helper also requires `--strong-operator`. Use only with explicit authorization for all changes, never as an automatic retry.
- `--skip-staging-precheck` — only when blocked files are intentionally included.

Inspect `git status --short`, `git diff`, and `git diff --cached` before invoking the helper: it stages and commits in one operation. `--paths` limits new staging but does not exclude already-staged files from the commit. If unrelated changes are staged, stop and ask the user to resolve ownership; do not unstage their work without permission.

## Invocation

    python3 scripts/commit_with_traceability.py \
      --feature <FEATURE_ID> --task <T-001> \
      --summary "<what changed>" \
      --cr <CR-...> [--decisions <D-...,...>] \
      --paths <task-owned-paths...>

## Message format

- Subject: `T-001: <summary> (Feature: <FEATURE_ID>)`
- Body:
  - `Input: CR-...`
  - `Decisions: D-...`
  - `Spec: docs/specs/<FEATURE_ID>/spec.md`
  - `Tasks: docs/specs/<FEATURE_ID>/tasks.md`
  - `Notes: docs/specs/<FEATURE_ID>/notes.md`

After committing, record the hash via `owl add-note` so the audit trail links to Git history.
