# Context Recovery (after a reset)

When conversation context is lost, regenerate a resume prompt from repo state:

    ./scripts/owl context

Paste the output into the new session together with one line: "Use the athena skill and continue the active feature." That is sufficient — the block contains the active feature, goal, task state, and recent CR/D IDs.

For a deeper reconstruction:
- `./scripts/owl show <CR-...|D-...>` — full text of specific entries
- `./scripts/owl why <FR-...>` — requirement → sources → tasks → commits
- `git log --oneline -10` — recent traceable commits

Legacy repos (still on `progress.txt`) can also use:
- `python3 scripts/validate_progress_log.py --repo .`
- `python3 scripts/print_resume_prompt.py --repo .`
