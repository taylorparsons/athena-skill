# Changelog

All notable changes to this project are documented in this file.

## v2.0.0 - 2026-04-15

### Added
- **Owl of Athena** sub-agent: handles archive management, `athena-index.md` maintenance, archived feature retrieval, and `write-memory` for Claude Code auto-memory.
- **athena-index.md**: token-optimized index replacing `INDEX.md` — reduces session startup token overhead by 80–90% for mature repos.
- **Owl memory bridge**: `owl write-memory` writes `project_athena_active.md` to Claude Code auto-memory at `SessionStart`, so Athena skips re-reading `progress.txt` and `athena-index.md` each session.
- **Fleet management**: `scripts/migrate-all-projects.py` scans all local Athena projects and migrates them to the current version (hooks, Owl agent, settings).
- **Weekly sweeper**: `scripts/sweep-projects.py` audits token overhead across all projects and auto-fixes stale indexes, unarchived done specs, and large progress files. Scheduled via OS crontab.
- **Runtime-agnostic `owl` wrapper**: `scripts/owl` works in both Codex CLI and Claude Code environments.

### Changed
- SessionStart hook now runs `prune-done` and `update-index` via `scripts/owl` before Athena loads each session.
- README updated with fleet management scripts, Codex compatibility notes, and corrected hook format.

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

## v1.2.0 - 2026-02-20

### Added
- Improved scanability across ATHENA documentation by applying stronger heading structure and **bold metadata labels** in root docs and spec files.

### Changed
- Updated feature `20260220-docs-readability-format` PRD links so all numbered references are inline markdown links to document anchors.
- Normalized PRD link targets away from absolute filesystem paths and `/docs/...` route forms to reader-compatible `*.md#anchor` form.

### Fixed
- Resolved local markdown reader navigation failures/404s for reference IDs by making documentation cross-links portable and in-reader compatible.
