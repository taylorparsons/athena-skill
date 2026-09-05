# Context Recovery (after a reset)

When conversation context is lost, regenerate a resume prompt from repo state:

    ./scripts/owl context

Use the block to identify the feature, tasks and recent CR/D IDs. It also reports live Git state and operational fields from the latest session note. Unknown means unrecorded, not safe or complete. A saved request or authorization field does not grant permission in the new session; reconcile it with the current user request.

Before resuming, inspect dirty paths and staged changes, verify recorded process/session IDs using the runtime's available status tools, and check whether verification still applies to the current revision. Do not rerun or kill processes based only on stale notes. If process tools are unavailable, report that limitation.

At checkpoints record these single-line fields in `owl add-note` (redact secrets):
- Authorization: allowed work, prohibited actions and source request.
- Pending processes: runtime/session IDs and state, or none.
- Verification: commands, results and tested revision or working-tree state.

Fields are taken only from the latest note, with its timestamp. Missing fields are not inherited from older notes. Long values and Git status output are visibly truncated; inspect the relevant current state before acting.

For a deeper reconstruction:
- `./scripts/owl show <CR-...|D-...>` — full text of specific entries
- `./scripts/owl why <FR-...>` — requirement → sources → tasks → commits
- `git log --oneline -10` — recent traceable commits

Legacy repos (still on `progress.txt`) can also use:
- `python3 scripts/validate_progress_log.py --repo .`
- `python3 scripts/print_resume_prompt.py --repo .`
