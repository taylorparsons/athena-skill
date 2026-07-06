# Traceable Commits

Goal: every commit links back to the ATHENA artifacts (CR / D / FEATURE_ID / T-...).

Hard rules:
- Never run `git push` or open/submit PRs unless the user explicitly asks.
- Do not commit secrets. If found, remove them and record the incident via `owl add-note`.

## Staging modes (helper prechecks)

`scripts/commit_with_traceability.py` supports:
- **Default (broad stage with guardrails)**: blocks `.DS_Store`, common temp/cache paths, likely secret patterns, and large artifacts.
- `--paths <p1> <p2> ...` — explicit scope.
- `--docs-only` — stage only the ATHENA traceability docs (spec/tasks/notes/PRD/TRACEABILITY/requests/decisions).
- `--all-changes` — stage everything.
- `--skip-staging-precheck` — only when blocked files are intentionally included.

Review with `git diff --cached` before committing.

## Invocation

    python3 scripts/commit_with_traceability.py \
      --feature <FEATURE_ID> --task <T-001> \
      --summary "<what changed>" \
      --cr <CR-...> [--decisions <D-...,...>] \
      [--paths ... | --docs-only | --all-changes]

## Message format

- Subject: `T-001: <summary> (Feature: <FEATURE_ID>)`
- Body:
  - `Input: CR-...`
  - `Decisions: D-...`
  - `Spec: docs/specs/<FEATURE_ID>/spec.md`
  - `Tasks: docs/specs/<FEATURE_ID>/tasks.md`
  - `Notes: docs/specs/<FEATURE_ID>/notes.md`

After committing, record the hash via `owl add-note` so the audit trail links to Git history.
