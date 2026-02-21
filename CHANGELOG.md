# Changelog

All notable changes to this project are documented in this file.

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
