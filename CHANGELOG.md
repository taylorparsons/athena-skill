# Changelog

All notable changes to this project are documented in this file.

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
