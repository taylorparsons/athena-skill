---
name: ralph-codex
description: Use the RALPH framework in Codex for PRD-driven, traceable delivery. Trigger when the user wants iterative execution with auditable CR/Decision/Spec/Task/Progress artifacts and disciplined one-task-at-a-time implementation.
---

# RALPH Codex Adapter

Use `../../core/ralph-framework.md` as the canonical process.

## Codex-specific operating notes

- Prefer direct repository execution over discussion-only responses.
- Keep diffs small and reviewable.
- Use local tooling to validate implementation changes.
- Record commands and outcomes in `docs/progress.txt`.
- If `.git/` exists, create local traceable commits and do not push unless asked.

## Required file set

Initialize these files using templates from `../../templates/` when missing:
- `docs/requests.md`
- `docs/decisions.md`
- `docs/TRACEABILITY.md`
- `docs/PRD.md`
- `docs/progress.txt`
- `docs/specs/<feature-id>/spec.md`
- `docs/specs/<feature-id>/tasks.md`

## Optional Codex helper scripts

This repository intentionally focuses on the public RALPH framework and templates.
If you need the helper Python scripts commonly used in Codex workflows, use `$skill-installer` to install the full `ralph` skill package into `$CODEX_HOME/skills`, then run those scripts from `$CODEX_HOME/skills/ralph/scripts/`.
