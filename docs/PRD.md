# PRD: RALPH Public Share Repo

Status: Active
Updated: 2026-02-11 10:20
Inputs: CR-20260211-0908, CR-20260211-0939, CR-20260211-1004, CR-20260211-1010, CR-20260211-1019
Decisions: D-20260211-0940, D-20260211-1005, D-20260211-1012, D-20260211-1020

## Summary
Public, clean RALPH framework repository for cross-agent usage (Codex + Claude) with scoped traceability artifacts for this repo only. (Sources: CR-20260211-0908, CR-20260211-0939; D-20260211-0940)

## Goals
- Publish RALPH as an agent-agnostic framework with adapter-specific guidance. (Sources: CR-20260211-0908)
- Keep repo artifacts clean and scoped only to this public share. (Sources: CR-20260211-0939; D-20260211-0940)
- Harden the repo for open-source publication readiness. (Sources: CR-20260211-1010; D-20260211-1012)
- Complete low-priority governance controls before public push. (Sources: CR-20260211-1019; D-20260211-1020)

## Functional requirements (shipped)
- FR-RALPH-001: Provide canonical core workflow in `core/ralph-framework.md`. (Sources: CR-20260211-0908)
- FR-RALPH-002: Provide Codex and Claude adapters in `adapters/`. (Sources: CR-20260211-0908)
- FR-RALPH-003: Provide reusable RALPH templates in `templates/`. (Sources: CR-20260211-0908)
- FR-RALPH-004: Maintain repo-scoped docs artifacts (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`) under `docs/`. (Sources: CR-20260211-0939; D-20260211-0940)

## Non-functional requirements (shipped)
- NFR-RALPH-001: Exclude local/generated artifacts from commits via `.gitignore`. (Sources: CR-20260211-0939, CR-20260211-1010; D-20260211-0940, D-20260211-1012)
- NFR-RALPH-002: Keep README focused on public share and cross-agent compatibility. (Sources: CR-20260211-0908, CR-20260211-0939)
- NFR-RALPH-003: Keep this public-share version scoped to RALPH only with no Daisy companion-skill references. (Sources: CR-20260211-1004; D-20260211-1005)
- NFR-RALPH-004: Remove local absolute path strings from tracked docs before public release. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-RALPH-005: Include public-facing `SECURITY.md` and MIT `LICENSE` files. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-RALPH-006: Publish from a rewritten clean baseline history. (Sources: CR-20260211-1010; D-20260211-1012)
- NFR-RALPH-007: Include single-owner repository `CODEOWNERS` policy. (Sources: CR-20260211-1019; D-20260211-1020)
- NFR-RALPH-008: Include `.github/dependabot.yml` and `.github/workflows/security.yml` hardening automation. (Sources: CR-20260211-1019; D-20260211-1020)
- NFR-RALPH-009: Enable repository-level `commit.gpgsign` in local git configuration. (Sources: CR-20260211-1019; D-20260211-1020)

## Out of scope
- Shipping imported historical docs from unrelated product repos as canonical artifacts in this share repo. (Sources: CR-20260211-0939; D-20260211-0940)

## Next / backlog
- Add `docs/examples/` with one full CR -> D -> FR -> T walkthrough for onboarding.
