# Changelog

All notable changes to this project are documented in this file.

## v2.1.0 - 2026-07-05

## Summary

**Token diet.** Per-session token cost drops ~85% (measured ~26-32K → ~4-5K in a mature repo). The audit trail keeps full queryability, but the KB is now **script-gated**: agents never read the `docs/` logs — all access goes through `./scripts/owl`, which is deterministic and costs zero tokens. Full Claude Code / Codex parity via scripts.

## What's Changed
### Script-gated KB (owl.py)
- New `owl context` — compact session-open block (active feature, goal, IN PROGRESS/NEXT, recent CR/D IDs, latest request verbatim). Replaces reading five docs files; works identically on Claude Code and Codex.
- New append commands `owl add-request`, `owl add-decision`, `owl add-note` — write audit entries with generated collision-safe IDs, never loading the logs.
- New query commands `owl show <CR-|D-|FR-ID>` (one entry) and `owl why <FR-ID>` (requirement → sources → tasks → commits).
- `write-memory` now sources from `tasks.md`/`notes.md`; `prune-done` is a graceful no-op on migrated repos.
- 20 unit tests added (`scripts/tests/test_owl.py`).

### progress.txt retired
- Task truth: per-feature `tasks.md`. Session notes: per-feature `notes.md` (new template). Session-open summary: `owl context`.
- New `owl migrate` converts existing repos losslessly (per-feature blocks → `notes.md`; unattributable blocks → `docs/audit/progress-legacy.txt`), then removes `progress.txt`. All commands fall back to `progress.txt` on unmigrated repos.
- `validate_progress_log.py` / `print_resume_prompt.py` handle the retired layout; `templates/progress.txt` removed; `templates/notes.md` added.

### Instruction layer diet
- `SKILL.md` rewritten: 338 → 86 lines (~3.9K → ~1.3K tokens); detailed procedures moved to `references/` (setup, commits, recovery), loaded only when needed; frontmatter description cut to one sentence.
- Codex `AGENTS.md` guidance reduced to trigger + stop-gates (≤ 15 lines) — the loop lives only in SKILL.md; Codex adapter rewritten accordingly.
- Root `SKILL.md`/`templates/` kept as synced copies of the `skills/athena/` package.

## Verification
- `python3 -m unittest discover -s scripts/tests` — 20/20 pass
- `node --test site/site.test.mjs` — pass
- `owl migrate` + `context` + `write-memory` + `prune-done` verified on this repo

## v2.0.0.1 - 2026-04-16

## Summary

Patch release on top of **published `v2.0.0`**. This release focuses on install-path clarity, Codex vs. Claude onboarding improvements, and packaged ATHENA wording updates that make Codex Owl dispatch clearer without changing Claude runtime behavior.

## What's Changed
### Installation and README Clarity
- Moved installation guidance higher in `README.md` and kept Codex-first ordering easier to scan.
- Added a clearer environment split in the Installation section:
  - dedicated **Codex quick start**
  - dedicated **Claude Code quick start**
  - explicit note that Owl setup is **Claude Code only**
- Clarified the Codex packaged-skill install command and verification path.
- Corrected Owl setup guidance to point at the root-repo installer workflow from a full `athena-skill` checkout.

### Packaged Skill Compatibility
- Updated the packaged `skills/athena/SKILL.md` Owl section with Codex-safe dispatch wording while preserving the existing Claude memory-first and `write-memory` guidance.
- Updated the packaged `skills/athena/agents/owl-of-athena.md` wording to be cross-agent friendly without changing the model metadata used by Claude migration flows.

## Verification

- GitHub release page baseline: published release `v2.0.0: Owl of Athena, Fleet Management & Token Optimization`.
- `VERSION` now reads `2.0.0.1`.
- Local git tag target for this release: `v2.0.0.1`.

## v2.0.0 - 2026-04-15

### Added
- **Owl of Athena** sub-agent (`scripts/owl.py`, `skills/athena/agents/owl-of-athena.md`): handles archive management, `athena-index.md` maintenance (`update-index`, `prune-done`), archived feature retrieval, and `write-memory` for Claude Code auto-memory.
- **athena-index.md**: token-optimized index replacing `INDEX.md` — reduces session startup token overhead by 80–90% for mature repos by loading only active feature summaries instead of full spec files.
- **Owl memory bridge**: `owl write-memory` writes `project_athena_active.md` to Claude Code auto-memory at `SessionStart`, so Athena skips re-reading `progress.txt` and `athena-index.md` each session.
- **Git hooks**: automatic `athena-index.md` management via pre-commit and post-commit hooks installed by `scripts/install-hooks.sh`.
- **progress.txt archival**: `owl trim-progress` archives completed session blocks to `docs/progress-archive.txt`, keeping active `progress.txt` small and fast to load.
- **install-owl.sh**: one-command fleet deployment script to install the `scripts/owl` delegation wrapper in any existing Athena project.
- **Fleet management**: `scripts/migrate-all-projects.py` scans all local Athena projects and migrates them to the current version (hooks, Owl agent, `settings.json`).
- **Weekly sweeper**: `scripts/sweep-projects.py` audits token overhead across all projects and auto-fixes stale indexes, unarchived done specs, and large progress files. Scheduled via OS crontab.
- **Runtime-agnostic `owl` wrapper**: `scripts/owl` detects whether it is running in Codex CLI or Claude Code and dispatches accordingly — no environment config required.
- **Localized skill templates**: ATHENA spec/tasks templates are now co-located in the repo (`docs/specs/`) rather than requiring a global install path.

### Changed
- Renamed `INDEX.md` → `athena-index.md` to avoid collisions with existing `docs/index.md` files in mature repos.
- `SessionStart` hook now runs `prune-done` and `update-index` via `scripts/owl` before Athena loads each session.
- README updated with fleet management scripts, Codex compatibility notes, corrected hook format, and clearer Claude Code vs. Codex install paths (Option A / Option B).

### Fixed
- `patch-claude-settings`: auto-detects outdated `settings.json` hook format (missing `write-memory` step) and patches it non-destructively.
- `_is_fully_closed`: returns `True` when a feature is not listed in `PRD.md` — trusts `tasks.md` + `spec.md` completion state instead of requiring PRD presence.
- Progress archive entries now write to `docs/` path, not the spec folder.

## v1.2.1 - 2026-02-21

### Added
- Staging precheck guardrails in `scripts/commit_with_traceability.py`: blocks `.DS_Store`, common temp/cache paths, likely secret patterns, and large binary artifacts before broad `git add`.
- Localized ATHENA traceability templates (`docs(athena): add localized skill templates and traceability`).

### Changed
- Hardened staging workflow — path-scoped staging is now the documented default.

## v1.2.0 - 2026-02-20

### Added
- Improved scanability across ATHENA documentation by applying stronger heading structure and **bold metadata labels** in root docs and spec files.

### Changed
- Updated feature `20260220-docs-readability-format` PRD links so all numbered references are inline markdown links to document anchors.
- Normalized PRD link targets away from absolute filesystem paths and `/docs/...` route forms to reader-compatible `*.md#anchor` form.
- Clarified Installation section for Claude Code users (PRs #3, #4).

### Fixed
- Resolved local markdown reader navigation failures/404s for reference IDs by making documentation cross-links portable and in-reader compatible.

## v1.1.0 - 2026-02-18

### Added
- Traceability linter that validates `Sources:`, `Verifies:`, and `Implements:` references across spec and task files.
- Schema validation for `docs/progress.txt` to reduce context-restore failures.

### Changed
- Consolidated overlapping merge-sync sections into one canonical merge/check-in reconciliation checklist.
- Path-scoped staging (`--docs-only`) is now the default in traceable commit helper usage.

## v1.0.3 - 2026-02-13

### Changed
- Renamed the skill identity from `ralph` to `athena` to avoid potential naming and copyright/IP confusion with established TV character names.
- Reframed the system from a generic loop to a **traceable loop**, emphasizing ATHENA's end-to-end audit trail from request to decision to requirement to task to shipped code.
- Updated Claude and Codex installation guidance to consistently use the `athena` skill name and repository identity.
- Strengthened ATHENA positioning: reliable, deliberate, and documentation-first execution designed for high trust, clear accountability, and easier team adoption.

## v1.0.2 - 2026-02-13

### Changed
- Bumped release for the install-command name change to use `skill-installer`.
- Retagged the latest release as `v1.0.2`.

## v1.0.1 - 2026-02-12

### Changed
- Updated installation instructions in `README.md` to use `skill-installer` with the repository URL:
  - `$skill-installer https://github.com/taylorparsons/ralph-traceability-loop/`
