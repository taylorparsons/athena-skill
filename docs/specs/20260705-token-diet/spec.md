# Feature Spec: 20260705-token-diet

Status: Active
Created: 2026-07-05 20:25
Inputs: CR-20260705-2015
Decisions: D-20260705-2025, D-20260705-2026, D-20260705-2027, D-20260705-2028

## Summary
- Cut ATHENA per-session token cost ~85% (measured ~26-32K in this repo, target ~4-5K) while keeping full audit-trail queryability, by gating all KB access through the deterministic `owl` script, retiring `docs/progress.txt` in favor of per-feature `tasks.md` + `notes.md` + a generated `owl context` block, and shrinking the instruction layer (SKILL.md core + references/, one-sentence frontmatter, minimal Codex AGENTS.md). Full Claude/Codex parity via scripts.

## User Stories & Acceptance

### US1: Cheap session open (Priority: P1)
Narrative:
- As an agent starting an ATHENA session, I want one command that gives me the active feature, goal, task state, and recent request/decision IDs, so that I never read the full logs.

Acceptance scenarios:
1. Given a migrated repo, When `./scripts/owl context` runs, Then it prints active feature, goal, IN PROGRESS/NEXT from tasks.md, other active features, last 3 CR and D IDs, and the latest CR verbatim, in ≤ ~60 lines. (Verifies: FR-001)
2. Given an unmigrated repo (progress.txt present), When `owl context` runs, Then it derives the same block from progress.txt without error. (Verifies: FR-001, FR-008)

### US2: Append without reading (Priority: P1)
Narrative:
- As an agent capturing audit entries, I want script-mediated appends with generated IDs, so that logs are written but never loaded into context.

Acceptance scenarios:
1. Given any repo, When text is piped to `owl add-request`, Then a well-formed CR entry with a unique generated ID is appended to docs/requests.md and the ID is returned as JSON. (Verifies: FR-002)
2. Given a CR ID, When text is piped to `owl add-decision --cr <ID>`, Then a well-formed D entry is appended to docs/decisions.md. (Verifies: FR-003)
3. Given an active feature, When text is piped to `owl add-note --feature <id>`, Then a timestamped session block is appended to docs/specs/<id>/notes.md (file created from template if missing). (Verifies: FR-004)

### US3: Targeted retrieval (Priority: P1)
Narrative:
- As an agent or user asking about history, I want single-entry and chain retrieval, so that queries cost tokens proportional to the answer, not the archive.

Acceptance scenarios:
1. Given an existing CR/D/FR ID, When `owl show <ID>` runs, Then exactly that entry is printed. (Verifies: FR-005)
2. Given an FR ID, When `owl why <FR-ID>` runs, Then the chain FR → Sources (CR/D entries) → implementing tasks → matching commits is printed. (Verifies: FR-006)

### US4: progress.txt retirement (Priority: P1)
Narrative:
- As a maintainer, I want progress.txt converted losslessly and all tooling to survive both layouts, so that existing repos migrate safely.

Acceptance scenarios:
1. Given a repo with progress.txt, When `owl migrate` runs, Then per-feature session blocks land in each feature's notes.md, unresolvable blocks land in docs/audit/progress-legacy.txt, progress.txt is removed, and a second run is a no-op. (Verifies: FR-007)
2. Given a migrated repo, When `owl write-memory` or `owl prune-done` runs, Then write-memory sources from tasks.md/notes.md and prune-done reports a graceful no-op. (Verifies: FR-008)

### US5: Slim instruction layer (Priority: P1)
Narrative:
- As a user paying per token, I want the always-loaded instruction surface minimal on both harnesses.

Acceptance scenarios:
1. Given the rewritten skill, When SKILL.md is counted, Then it is ≤ ~130 lines with detailed procedures in references/*.md, and the frontmatter description is one sentence. (Verifies: FR-009)
2. Given the Codex config, When AGENTS.md is inspected, Then it contains only trigger + stop-gates (≤ 15 lines) and no loop steps. (Verifies: FR-010)

## Requirements

Functional requirements:
- FR-001: `owl context` prints a compact session-open block (current feature, goal, IN PROGRESS/NEXT, active features, last 3 CR/D IDs with dates, latest CR verbatim, doc paths), working in both migrated and legacy layouts. (Sources: CR-20260705-2015; D-20260705-2025, D-20260705-2026)
- FR-002: `owl add-request [--source <s>]` appends a standardized CR entry from stdin with generated collision-safe ID; returns JSON with the ID. (Sources: CR-20260705-2015; D-20260705-2028)
- FR-003: `owl add-decision --cr <CR-...[,CR-...]> [--prd <section>]` appends a standardized D entry from stdin; returns JSON with the ID. (Sources: CR-20260705-2015; D-20260705-2028)
- FR-004: `owl add-note --feature <id> [--goal g] [--agent a] [--model m] [--skills s]` appends a timestamped session block to the feature's notes.md, creating it from template if missing. (Sources: CR-20260705-2015; D-20260705-2026)
- FR-005: `owl show <CR-...|D-...|FR-...>` prints exactly one entry (logs for CR/D; spec files for FR). (Sources: CR-20260705-2015; D-20260705-2025)
- FR-006: `owl why <FR-...>` prints the traceability chain: requirement line, its Sources entries, tasks whose Implements references it, and commits found via `git log --grep`. (Sources: CR-20260705-2015; D-20260705-2025)
- FR-007: `owl migrate` losslessly converts progress.txt to per-feature notes.md + docs/audit/progress-legacy.txt, deletes progress.txt, and is idempotent. (Sources: CR-20260705-2015; D-20260705-2026)
- FR-008: `write-memory` sources from tasks.md/notes.md in migrated repos (progress.txt fallback otherwise); `prune-done` is a graceful no-op without progress.txt. (Sources: CR-20260705-2015; D-20260705-2026)
- FR-009: SKILL.md rewritten to ≤ ~130 lines enforcing script-gated access; detailed procedures moved to references/ (commits.md, setup.md, recovery.md); frontmatter description one sentence; root SKILL.md kept identical to skills/athena/SKILL.md. (Sources: CR-20260705-2015; D-20260705-2025, D-20260705-2028)
- FR-010: Codex adapter and ~/.codex/AGENTS.md reduced to trigger + stop-gates; session open via `./scripts/owl context`. (Sources: CR-20260705-2015; D-20260705-2027)
- FR-011: Templates updated — notes.md added, progress.txt removed from the package, TRACEABILITY.md template describes the new trail; both template copies (root and skills/athena) stay identical. (Sources: CR-20260705-2015; D-20260705-2026, D-20260705-2028)
- FR-012: Downstream tooling survives both layouts: validate_progress_log.py passes on migrated repos, print_resume_prompt.py uses the context builder, sweep-projects.py notes legacy status, site copy updated and site tests pass. (Sources: CR-20260705-2015; D-20260705-2026, D-20260705-2028)
- FR-013: Version bumped, CHANGELOG updated, skill reinstalled to ~/.claude/skills/athena and ~/.codex/skills/athena matching the repo package. (Sources: CR-20260705-2015)

## Edge cases
- Multiple active features: `owl context` picks the one with the newest notes.md session timestamp (tie-break: tasks.md mtime) and lists the others. (Verifies: FR-001)
- ID collision within the same minute: add-request/add-decision increment the minute until unique. (Verifies: FR-002, FR-003)
- add-note for a feature with no spec dir: command errors with a clear message, no partial writes. (Verifies: FR-004)
- `owl why` on an FR with no commits yet: prints the doc chain and "no commits found". (Verifies: FR-006)
- Migration block with Feature: id whose spec dir is gone: block goes to docs/audit/progress-legacy.txt. (Verifies: FR-007)
