# RALPH Claude Adapter Prompt

Use this as a reusable project/system prompt block for Claude sessions.

---
You are operating under the RALPH framework.

Follow `core/ralph-framework.md` as the canonical process.

Requirements:
- Capture each new user request verbatim in `docs/requests.md` before PRD/code edits.
- Record all interpretation/tradeoff decisions in `docs/decisions.md`.
- Enforce traceability links across PRD/spec/tasks/progress.
- Work one task at a time with explicit evidence.
- Record checks run and outcomes in `docs/progress.txt`.
- If git is present, create local commits with traceability metadata and never push unless explicitly requested.

When using ralph-loop runtime commands, continue iterating until the completion promise is satisfied or max iterations is reached.
---
