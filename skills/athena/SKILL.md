---
name: athena
description: PRD-driven delivery loop with a token-lean audit trail (requests → decisions → specs → tasks → commits). All docs/ log access goes through ./scripts/owl. Use for any feature, bug fix, or change in a repo using ATHENA docs/.
---

# ATHENA Loop

The audit trail lives in `docs/` but is **script-gated**: never Read `docs/requests.md`, `docs/decisions.md`, `docs/athena-index.md`, or archived specs — all access goes through `./scripts/owl` (deterministic, zero-token). You may Read/Edit directly only:
- the active feature's `docs/specs/<FEATURE_ID>/spec.md`, `tasks.md`, `notes.md`
- the `docs/PRD.md` sections you are changing — never the full file: locate the section with grep, read only that line range; one requirement → `owl show <FR-ID>`
- `docs/TRACEABILITY.md`

## 1) Open the session

- Claude Code: if the `Athena Active Context` memory is present, use it and skip the next step.
- Otherwise run `./scripts/owl context` — prints active feature, goal, IN PROGRESS/NEXT, recent CR/D IDs, and the latest request.
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
- Establish a FEATURE_ID (`YYYYMMDD-short-name`; ask if unclear). Ensure `docs/specs/<FEATURE_ID>/spec.md` and `tasks.md` exist (copy from `templates/`).
- Traceability is mandatory: FRs have stable IDs and `Sources:`; acceptance scenarios have `Verifies: FR-...`; tasks have `Implements: FR-...`. Fix broken links before writing code.

## 4) Execute one small task

- Take the next task from the active `tasks.md`; move it under IN PROGRESS (keep IN PROGRESS ≤ 1) and tag it `(Skills: athena[, ...])`.
- Make the smallest change that satisfies the PRD. No invented requirements, no drive-by refactors, no deletions unless the task requires them (record deletions in notes).
- PRD unclear? Don't guess — record the question via `owl add-note`, then pick the smallest unambiguous task or stop and ask.
- Run the repo's checks (tests / lint / typecheck / build). If they can't run, record why in notes.

## 5) Close the loop

- Update `tasks.md`: completed tasks to DONE with timestamp; newly discovered follow-ups into NEXT.
- Append session notes:

      ./scripts/owl add-note --feature <FEATURE_ID> --goal "<goal>" --skills "athena[, ...]" <<'EOF'
      - Commands run: <cmd> -> <result>
      - Decisions: <D-IDs or none>
      - Risks / open questions: <items>
      EOF

- Reconcile before finalizing a task and after any merge: spec `Status:` matches reality; PRD backlog updated (shipped items cite their CR and one concrete evidence path); merge commit hash recorded via `add-note`, or `pending merge` if not merged yet.
- Git repos: commit when a task reaches DONE — `python3 scripts/commit_with_traceability.py --feature <FEATURE_ID> --task <T-...> --summary "<what>" --cr <CR-...> [--decisions <D-...>]`. Staging modes and message format: `references/commits.md`. **Never push or open PRs unless the user explicitly asks.**
- Claude Code: refresh memory with `./scripts/owl write-memory`.

## Owl commands (the KB gateway)

| Need | Command |
|---|---|
| Session-open context | `owl context` |
| Append request / decision / session note | `owl add-request`, `owl add-decision`, `owl add-note` |
| Read one entry by ID | `owl show <ID>` (CR-, D-, or FR-) |
| Trace a requirement to sources and commits | `owl why <FR-...>` |
| Feature summary / history search | `owl retrieve <id>`, `owl search <keyword>` |
| Archive a finished feature | `owl archive <id>` (also condenses its spec.md; `--keep-spec` opts out) |
| Keep the PRD lean | `owl prune-prd` (archives link lists + closed backlog lines) |
| Keep requests.md / decisions.md lean | `owl archive-logs [--keep-days 30] [--keep-last 20] [--dry-run]` — old entries move to `docs/audit/<log>-YYYY-MM.md`; `owl show <ID>` still finds them |
| Keep Done specs lean | `owl archive-specs [--dry-run]` — spec.md shrinks to title/Status/Summary/FR/AS/Sources lines, full text in `docs/audit/specs/<id>.md`; `owl restore-spec <id>` undoes it |
| Both at once | `owl trim [--dry-run]` — run `--dry-run` first |
| Rebuild index / refresh memory | `owl update-index`, `owl write-memory` |

A feature is **done** when `tasks.md` has nothing under NEXT or IN PROGRESS, `spec.md` says `Status: Done`, and the PRD shows it shipped — then run `owl archive <id>`. In Claude Code you may instead dispatch the Owl sub-agent (`.claude/agents/owl-of-athena.md`) when you want a narrative summary; in Codex just run the script.

## References (load only when needed)

- `references/setup.md` — creating `docs/` in a new or adopted repo; git-history bootstrap; migrating off `progress.txt` (`owl migrate`)
- `references/commits.md` — staging guardrails, docs-only mode, commit message format
- `references/recovery.md` — restoring context after a reset

UI/UX work in a feature? Offer the `daisy` skill. Explicit plan requests → `create-plan` skill, then resume this loop.
