---
name: athena
description: PRD-driven delivery loop with a token-lean audit trail (requests → decisions → specs → tasks → commits). All docs/ log access goes through ./scripts/owl. Use for any feature, bug fix, or change in a repo using ATHENA docs/.
---

# ATHENA Loop

This is the canonical workflow; `skills/athena/SKILL.md` is its validated install copy. Adapters provide harness wiring, not alternate workflows.

## Select the requested mode

- Review, explain, diagnose, or report status: inspect and answer without changing files, audit logs, tasks, or Git state. Use read-only Owl queries. Do not enter the implementation loop unless the user requests changes.
- Implement or change: follow the loop below within the user's authorized scope. A backlog item or saved request is context, not permission to implement it.
- A plan-only request authorizes a plan, not implementation. Save planning artifacts only when requested. Do not require other skills that are unavailable in the runtime.

The audit trail lives in `docs/` but is **script-gated**: never read `docs/requests.md`, `docs/decisions.md`, `docs/athena-index.md`, or archived specs directly; use `./scripts/owl`. Retrieval is deterministic and uses no LLM, but returned text consumes model context. Direct access within `docs/` is limited to:
- the active feature's `docs/specs/<FEATURE_ID>/spec.md`, `tasks.md`, `notes.md`
- the `docs/PRD.md` sections relevant to the request: locate the section with `rg` and read that range, not the full file; use `owl show <FR-ID>` for a spec requirement
- `docs/TRACEABILITY.md`

## 1) Open the session

- Run `./scripts/owl context` on a new session or recovery. Saved memory is a hint, not a substitute for current repository state. For recovery details, read `references/recovery.md`.
- Repo has no `docs/` audit files, or still has `docs/progress.txt`? See `references/setup.md`.
- Summarize the session goal in one sentence before changing anything.

## 2) Capture input first

No PRD or code changes until the session's customer request is captured verbatim (redact secrets):

    ./scripts/owl add-request <<'EOF'
    <verbatim customer request>
    EOF

Returns the `CR-...` ID. No explicit request this session? Ask the user for one.

Whenever you interpret ambiguity, choose tradeoffs, or change scope:

    ./scripts/owl add-decision --cr <CR-ID> --prd "<PRD section>" <<'EOF'
    Decision: <what>
    Rationale: <why>
    Alternatives considered: <rejected options and why>
    EOF

## 3) Reflect in PRD and spec

- If the newest CR is not reflected in `docs/PRD.md`, update the PRD first. Tag every added or changed requirement `(Sources: CR-...; D-...)` — at least one CR, plus a D whenever interpretation was needed.
- Reuse the feature matching the request, or derive a new FEATURE_ID (`YYYYMMDD-short-name`). Ask only if choosing between features would change scope. Ensure its `spec.md` and `tasks.md` exist (copy from `templates/`).
- Traceability is mandatory: FRs have stable IDs and `Sources:`; acceptance scenarios have `Verifies: FR-...`; tasks have `Implements: FR-...`. Fix broken links before writing code.

## 4) Execute authorized tasks sequentially

- Take the next task from the active `tasks.md`; move it under IN PROGRESS (keep IN PROGRESS ≤ 1) and tag it `(Skills: athena[, ...])`.
- Make the smallest change that satisfies the PRD. No invented requirements, no drive-by refactors, no deletions unless the task requires them (record deletions in notes).
- Make routine, reversible implementation choices within requirements and record material decisions. Ask when the answer changes requirements, scope, safety, external effects, or permissions. Do not choose an unrelated backlog task when blocked.
- After closing one task, continue with the next authorized task until the requested outcome is complete or a real blocker requires user input. One active task is a concurrency limit, not a one-task-per-turn limit. Honor explicit review checkpoints.
- Independent read-only investigation or review may run in parallel when supported. Keep implementation and audit writes serialized; do not require subagents when unavailable.
- If the user changes direction, preserve completed work, reconcile scope, and stop superseded actions. A side question does not cancel unfinished authorized work.
- Run the repo's checks (tests / lint / typecheck / build). If they can't run, record why in notes.

## 5) Close the loop

- Update `tasks.md`: completed tasks to DONE with timestamp; newly discovered follow-ups into NEXT.
- Append session notes:

      ./scripts/owl add-note --feature <FEATURE_ID> --goal "<goal>" --skills "athena[, ...]" <<'EOF'
      - Commands run: <cmd> -> <result>
      - Decisions: <D-IDs or none>
      - Risks / open questions: <items>
      - Authorization: <current scope and prohibited actions; cite user request>
      - Pending processes: <runtime/session IDs and state, or none>
      - Verification: <command, result and tested revision or working-tree state>
      EOF

- Reconcile before finalizing a task and after any merge: spec `Status:` matches reality; PRD backlog updated (shipped items cite their CR and one concrete evidence path); merge commit hash recorded via `add-note`, or `pending merge` if not merged yet.
- Git repos: read `references/commits.md`, inspect existing staged changes, then commit completed authorized work with explicit scope: `python3 scripts/commit_with_traceability.py --feature <FEATURE_ID> --task <T-...> --summary "<what>" --cr <CR-...> --paths <task-owned-paths...>`. Never include unrelated staged changes or use confirmation/bypass flags to evade a blocker. Never push or open PRs unless explicitly requested.
- Claude Code: refresh memory with `./scripts/owl write-memory`.

## Owl commands (the KB gateway)

| Need | Command |
|---|---|
| Session-open context | `owl context` |
| Append request / decision / session note | `owl add-request`, `owl add-decision`, `owl add-note` |
| Read one entry by ID | `owl show <ID>` (CR-, D-, or FR-) |
| Trace a requirement to sources and commits | `owl why <FR-...>` |
| Feature summary / history search | `owl retrieve <id>`, `owl search <keyword>` |
| Archive a finished feature | `owl archive <id>` |
| Keep the PRD lean | `owl prune-prd` (archives link lists + closed backlog lines) |
| Rebuild index / refresh memory | `owl update-index`, `owl write-memory` |

A feature is **done** when `tasks.md` has nothing under NEXT or IN PROGRESS, `spec.md` says `Status: Done`, and the PRD shows it shipped — then run `owl archive <id>`. In Claude Code you may instead dispatch the Owl sub-agent (`.claude/agents/owl-of-athena.md`) when you want a narrative summary; in Codex just run the script.

## References (load only when needed)

- `references/setup.md` — creating `docs/` in a new or adopted repo; git-history bootstrap; migrating off `progress.txt` (`owl migrate`)
- `references/commits.md` — staging guardrails, docs-only mode, commit message format
- `references/recovery.md` — restoring context after a reset

When evaluating workflow changes, use `references/evaluation.md`. Report only tests actually run; structural checks do not establish model performance. Final handoff: outcome, verification, remaining blockers, and branch/commit when relevant.
