# PRD: ATHENA Skill Repo

Status: Active
Updated: 2026-02-12 17:00
Inputs: CR-20260211-0908, CR-20260211-0939, CR-20260211-1004, CR-20260211-1010, CR-20260211-1019, CR-20260211-1325, CR-20260211-1358, CR-20260212-1646
Decisions: D-20260211-0940, D-20260211-1005, D-20260211-1012, D-20260211-1020, D-20260211-1326, D-20260211-1400, D-20260212-1647, D-20260212-1648

## Summary
Public, clean ATHENA framework repository for cross-agent usage (Codex + Claude) with scoped traceability artifacts for this repo only. (Sources: CR-20260211-0908, CR-20260211-0939, CR-20260212-1646; D-20260211-0940, D-20260212-1647)

## Goals
- Publish ATHENA as an agent-agnostic framework with adapter-specific guidance. (Sources: CR-20260211-0908, CR-20260212-1646; D-20260212-1647)
- Keep repo artifacts clean and scoped only to this public share. (Sources: CR-20260211-0939; D-20260211-0940)
- Harden the repo for open-source publication readiness. (Sources: CR-20260211-1010; D-20260211-1012)
- Complete low-priority governance controls before public push. (Sources: CR-20260211-1019; D-20260211-1020)
- Provide an onboarding walkthrough under `docs/examples/` that demonstrates end-to-end traceability. (Sources: CR-20260211-1325; D-20260211-1326)
- Ensure public install guidance stays single-skill (`athena`) with deterministic path-based packaging. (Sources: CR-20260211-1358, CR-20260212-1646; D-20260211-1400, D-20260212-1647)
- Ensure mutable repository identity references use `athena-skill`. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)

## Functional requirements
- FR-ATHENA-001: Provide canonical core workflow in `core/athena-framework.md`. (Sources: CR-20260211-0908, CR-20260212-1646; D-20260212-1648)
- FR-ATHENA-002: Provide Codex and Claude adapters in `adapters/`. (Sources: CR-20260211-0908)
- FR-ATHENA-003: Provide reusable ATHENA templates. (Sources: CR-20260211-0908, CR-20260212-1646; D-20260212-1647)
- FR-ATHENA-004: Maintain repo-scoped docs artifacts (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`) under `docs/`. (Sources: CR-20260211-0939; D-20260211-0940)
- FR-ATHENA-005: Provide `docs/examples/` with one full CR -> D -> FR -> T walkthrough for onboarding. (Sources: CR-20260211-1325; D-20260211-1326)
- FR-ATHENA-006: Provide exactly one packaged install target at `skills/athena` and validate that target in CI/local checks. (Sources: CR-20260211-1358, CR-20260212-1646; D-20260211-1400, D-20260212-1647)
- FR-ATHENA-007: Ensure mutable repository code/documentation references use `athena`/`ATHENA` naming consistently. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-ATHENA-008: Ensure mutable repository identity references use `athena-skill`. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)

## Non-functional requirements
- NFR-ATHENA-001: Exclude local/generated artifacts from commits via `.gitignore`. (Sources: CR-20260211-0939, CR-20260211-1010; D-20260211-0940, D-20260211-1012)
- NFR-ATHENA-002: Keep README focused on public share and cross-agent compatibility. (Sources: CR-20260211-0908, CR-20260211-0939)
- NFR-ATHENA-003: Keep this public-share version scoped to ATHENA only with no Daisy companion-skill references. (Sources: CR-20260211-1004, CR-20260212-1646; D-20260211-1005, D-20260212-1647)
- NFR-ATHENA-004: Remove local absolute path strings from tracked docs before public release. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-ATHENA-005: Include public-facing `SECURITY.md` and MIT `LICENSE` files. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-ATHENA-006: Publish from a rewritten clean baseline history. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-ATHENA-007: Include single-owner repository `CODEOWNERS` policy. (Sources: CR-20260211-1019; D-20260211-1020)
- NFR-ATHENA-008: Include `.github/dependabot.yml` and `.github/workflows/security.yml` hardening automation. (Sources: CR-20260211-1019; D-20260211-1020)
- NFR-ATHENA-009: Enable repository-level `commit.gpgsign` in local git configuration. (Sources: CR-20260211-1019; D-20260211-1020)
- NFR-ATHENA-010: Keep install docs explicit about avoiding `--path .` to prevent whole-repo skill installs. (Sources: CR-20260211-1358; D-20260211-1400)
- NFR-ATHENA-011: Preserve append-only historical request/decision records as factual audit evidence. (Sources: CR-20260212-1646; D-20260212-1648)

## Out of scope
- Editing historical verbatim request/decision text for cosmetic renaming. (Sources: CR-20260212-1646; D-20260212-1648)
- Shipping imported historical docs from unrelated product repos as canonical artifacts in this share repo. (Sources: CR-20260211-0939; D-20260211-0940)

## Next / backlog
- (none currently)
- Implemented in: `skills/athena/SKILL.md`, `core/athena-framework.md`, `README.md`, `AVAILABLE_SKILLS.md`, `adapters/codex/SKILL.md`, `adapters/claude/CLAUDE_PROMPT.md`, `scripts/validate_install_targets.py`.
