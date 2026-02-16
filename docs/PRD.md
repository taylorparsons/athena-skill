# PRD: ATHENA Skill Repo

Status: Active
Updated: 2026-02-13 14:52
Inputs: CR-20260211-0908, CR-20260211-0939, CR-20260211-1004, CR-20260211-1010, CR-20260211-1019, CR-20260211-1325, CR-20260211-1358, CR-20260212-1646, CR-20260213-0912, CR-20260213-1958, CR-20260213-1434, CR-20260213-1435, CR-20260213-1436, CR-20260213-1448, CR-20260213-1452
Decisions: D-20260211-0940, D-20260211-1005, D-20260211-1012, D-20260211-1020, D-20260211-1326, D-20260211-1400, D-20260212-1647, D-20260212-1648, D-20260213-0913, D-20260213-1959, D-20260213-1437, D-20260213-1438, D-20260213-1448, D-20260213-1453

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
- Provide two LinkedIn-ready post variants that explain ATHENA flow (invoke -> request -> loops -> check-in) and include clear install instructions for both Codex and Claude. (Sources: CR-20260213-0912; D-20260213-0913)
- Provide one additional LinkedIn-ready variant in the maintainer's personal writing style while preserving ATHENA flow and installation clarity. (Sources: CR-20260213-1958; D-20260213-1959)
- Add a top-of-README fast visual for immediate ATHENA loop comprehension. (Sources: CR-20260213-1434, CR-20260213-1435; D-20260213-1437)
- Keep README prose in normal repo style for this update and limit scope to the top-image addition. (Sources: CR-20260213-1448; D-20260213-1448)
- Complete a traceable local check-in, merge with remote main, and push only intended changes for the README visual update. (Sources: CR-20260213-1452; D-20260213-1453)

## Functional requirements
- FR-ATHENA-001: Provide canonical core workflow in `core/athena-framework.md`. (Sources: CR-20260211-0908, CR-20260212-1646; D-20260212-1648)
- FR-ATHENA-002: Provide Codex and Claude adapters in `adapters/`. (Sources: CR-20260211-0908)
- FR-ATHENA-003: Provide reusable ATHENA templates. (Sources: CR-20260211-0908, CR-20260212-1646; D-20260212-1647)
- FR-ATHENA-004: Maintain repo-scoped docs artifacts (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`) under `docs/`. (Sources: CR-20260211-0939; D-20260211-0940)
- FR-ATHENA-005: Provide `docs/examples/` with one full CR -> D -> FR -> T walkthrough for onboarding. (Sources: CR-20260211-1325; D-20260211-1326)
- FR-ATHENA-006: Provide exactly one packaged install target at `skills/athena` and validate that target in CI/local checks. (Sources: CR-20260211-1358, CR-20260212-1646; D-20260211-1400, D-20260212-1647)
- FR-ATHENA-007: Ensure mutable repository code/documentation references use `athena`/`ATHENA` naming consistently. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-ATHENA-008: Ensure mutable repository identity references use `athena-skill`. (Sources: CR-20260212-1646; D-20260212-1647, D-20260212-1648)
- FR-ATHENA-009: Provide two LinkedIn-ready draft posts under `publishing/` that describe ATHENA invocation-to-checkin loop execution and include copy/paste installation instructions for both Codex and Claude usage. (Sources: CR-20260213-0912; D-20260213-0913)
- FR-ATHENA-010: Provide one additional LinkedIn-ready draft under `publishing/` using the maintainer's direct, structured, low-hype personal style while still documenting ATHENA loop flow and Codex/Claude setup blocks. (Sources: CR-20260213-1958; D-20260213-1959)
- FR-ATHENA-011: Place a fast visual image at the top of `README.md` using a new tracked asset path, and do not use `docs/athena-napkin-loop.svg`. (Sources: CR-20260213-1434, CR-20260213-1435; D-20260213-1437)
- FR-ATHENA-012: For the README fast-visual change, keep standard README prose and remove literal style labels while preserving executable command blocks and factual repository details. (Sources: CR-20260213-1448; D-20260213-1448)
- FR-ATHENA-013: Execute a scoped check-in and remote merge workflow that commits intended README/docs/image updates while excluding unrelated local file changes. (Sources: CR-20260213-1452; D-20260213-1453)

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
- Implemented in: `skills/athena/SKILL.md`, `core/athena-framework.md`, `README.md`, `AVAILABLE_SKILLS.md`, `adapters/codex/SKILL.md`, `adapters/claude/CLAUDE_PROMPT.md`, `scripts/validate_install_targets.py`, `publishing/linkedin-post-athena-flow-v1.md`, `publishing/linkedin-post-athena-flow-v2.md`, `publishing/linkedin-post-athena-flow-v3-personal-style.md`, `docs/images/athena-readme-fast-visual.svg`.
