# Tasks: 20260706-prd-diet-codex-config

Spec: docs/specs/20260706-prd-diet-codex-config/spec.md

## NEXT

## IN PROGRESS
- (none)

## DONE
- [2026-07-06 06:44] T-001: `owl prune-prd` implemented in owl.py (metadata link lists + closed backlog lines → docs/audit/prd-archive.md, active-feature lines kept, idempotent). (Implements: FR-001; Skills: athena)
- [2026-07-06 06:45] T-002: 3 unit tests added (archive+pointers, idempotency, missing/lean PRD) — 23/23 pass. (Implements: FR-001; Skills: athena)
- [2026-07-06 06:46] T-003: SKILL.md — never-full-read PRD rule + prune-prd in command table; root copy and package synced. (Implements: FR-002; Skills: athena)
- [2026-07-06 06:47] T-004: prune-prd run on this repo: 14 lines / ~6.2KB archived, PRD 26.9KB → 20.9KB; second run no-op; linter unchanged. (Implements: FR-001; Skills: athena)
- [2026-07-06 06:48] T-005: 7 loose files moved from ~/.codex/skills to ~/.codex/skills-archive/ (jd_*.txt ×3, tailored_*.md ×3, tmp_cloudflare_jd.html); 3 dirs without SKILL.md reported (ai_pm_agent_level4, codex-primary-runtime, outputs), not moved. (Implements: FR-003; Skills: athena)
- [2026-07-06 06:49] T-006: `[profiles.athena]` (model_reasoning_effort=medium) appended to ~/.codex/config.toml; TOML validated; 14 plugins inventoried for user review. (Implements: FR-004; Skills: athena)
- [2026-07-06 06:52] T-007: VERSION 2.2.0, CHANGELOG entry, package reinstalled to both installs. (Implements: FR-005; Skills: athena)
