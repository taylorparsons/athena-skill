# Tasks: 20261113-plugin-submission-prep

Spec: docs/specs/20261113-plugin-submission-prep/spec.md

Status legend: TODO | IN PROGRESS | DONE

- [2026-11-13] T-001: Create submission-prep branch; capture CR and decisions. (Implements: FR-006) — DONE
- [2026-11-13] T-002: Add .claude-plugin/plugin.json (name athena, version 2.2.0, MIT, author Taylor Parsons, repository URL; no email). Icon set to .claude-plugin/icon.png. (Implements: FR-001) — DONE
- [2026-11-13] T-003: Move agents/OWL-IMPLEMENTATION.md to docs/agents/ via git mv (only archived/history references existed). (Implements: FR-005) — DONE
- [2026-11-13] T-004: Render .claude-plugin/icon.png (1024×1024) from skills/athena/assets/athena-warrior-icon.svg with rsvg-convert; checked visually. (Implements: FR-005) — DONE
- [2026-11-13] T-005: Add .claude-plugin/marketplace.json (name athena-skill, plugin athena with source ./) for the README install path. (Implements: FR-003) — DONE
- [2026-11-13] T-006: Add Claude Code plugin, Requirements, and License sections to README.md; existing content unchanged. (Implements: FR-003) — DONE
- [2026-11-13] T-007: Write SUBMISSION_NOTES.md (draft answers; TODOs listed; repo grep for secrets, personal identifiers, egress). (Implements: FR-004) — DONE
- [2026-11-13] T-008: Run claude plugin validate --strict --profile directory on ./athena-skill (passes); run validate_install_targets.py (OK), unittest (23 OK). Traceability validator flags pre-existing older specs; this feature's Spec pointer fixed. (Implements: FR-005) — DONE
- [2026-11-13] T-009: Commit locally on submission-prep with traceability trailers. No push, no merge, no submission. (Implements: FR-006) — DONE
