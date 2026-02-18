# PRD: ATHENA Skill Repo

Status: Active
Updated: 2026-02-18 09:04
Inputs: CR-20260211-0908, CR-20260211-0939, CR-20260211-1004, CR-20260211-1010, CR-20260211-1019, CR-20260211-1325, CR-20260211-1358, CR-20260212-1646, CR-20260213-0912, CR-20260213-1958, CR-20260213-1434, CR-20260213-1435, CR-20260213-1436, CR-20260213-1448, CR-20260213-1452, CR-20260216-1317, CR-20260217-0846, CR-20260217-1417, CR-20260217-1451, CR-20260217-1535, CR-20260217-1550, CR-20260218-0902
Decisions: D-20260211-0940, D-20260211-1005, D-20260211-1012, D-20260211-1020, D-20260211-1326, D-20260211-1400, D-20260212-1647, D-20260212-1648, D-20260213-0913, D-20260213-1959, D-20260213-1437, D-20260213-1438, D-20260213-1448, D-20260213-1453, D-20260216-1318, D-20260217-0847, D-20260217-1419, D-20260217-1452, D-20260217-1536, D-20260217-1551, D-20260218-0903

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
- Remediate findings 1-5 from the review with scoped fixes in docs/workflows/scripts and reconcile stale traceability state. (Sources: CR-20260216-1317; D-20260216-1318)
- Add a warrior-themed SVG icon asset to the installable ATHENA skill package. (Sources: CR-20260217-0846; D-20260217-0847)
- Ensure ATHENA install metadata binds the packaged warrior icon path and is covered by install-target validation. (Sources: CR-20260217-1417; D-20260217-1419)
- Remediate follow-up absolute-path residues in tracked docs so repository security audit no longer reports a `HIGH` path finding. (Sources: CR-20260217-1451; D-20260217-1452)
- Document and sequence the next ATHENA hardening workstreams (traceability linting, merge-sync checklist consolidation, path-scoped staging defaults, and `docs/progress.txt` schema validation) with explicit task traceability and agentic workflow output. (Sources: CR-20260217-1535; D-20260217-1536)
- Complete implementation of all queued ATHENA hardening workstreams in the current feature execution cycle. (Sources: CR-20260217-1550; D-20260217-1551)
- Update ATHENA repository version marker to `1.1.0`. (Sources: CR-20260218-0902; D-20260218-0903)

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
- FR-ATHENA-014: Resolve review findings 1-5 by reconciling stale feature status, hardening helper scripts, expanding markdown secret scanning, and removing remaining local absolute path residue from tracked docs. (Sources: CR-20260216-1317; D-20260216-1318)
- FR-ATHENA-015: Provide a warrior-themed SVG icon asset at `skills/athena/assets/athena-warrior-icon.svg` for ATHENA skill packaging and reuse. (Sources: CR-20260217-0846; D-20260217-0847)
- FR-ATHENA-016: Ensure installable ATHENA metadata (`skills/athena/agents/openai.yaml`) sets `icon_small`/`icon_large` to `./assets/athena-warrior-icon.svg` and validate this contract in `scripts/validate_install_targets.py`. (Sources: CR-20260217-1417; D-20260217-1419)
- FR-ATHENA-017: Remove remaining absolute-path residues from tracked docs and verify remediation using repository security audit checks. (Sources: CR-20260217-1451; D-20260217-1452)
- FR-ATHENA-018: Produce ATHENA hardening planning artifacts in `docs/specs/20260217-athena-hardening-plan/` and `artifacts/agentic_workflow/20260217-1535-athena-hardening-plan.json`, and define implementation backlog tasks for the four hardening items. (Sources: CR-20260217-1535; D-20260217-1536)
- FR-ATHENA-019: Implement the four ATHENA hardening workstreams in repo scripts/docs: traceability linter, canonical merge/check-in checklist, path-scoped staging default, and progress schema validation integrated with resume flow. (Sources: CR-20260217-1550; D-20260217-1551)
- FR-ATHENA-020: Update the root `VERSION` file value to `1.1.0`. (Sources: CR-20260218-0902; D-20260218-0903)

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
- Implemented in: `VERSION`, `docs/specs/20260218-version-bump-1-1-0/spec.md`, `docs/specs/20260218-version-bump-1-1-0/tasks.md`, `docs/progress.txt`.
- Implemented in: `docs/specs/20260217-athena-hardening-plan/spec.md`, `docs/specs/20260217-athena-hardening-plan/tasks.md`, `artifacts/agentic_workflow/20260217-1535-athena-hardening-plan.json`, `scripts/validate_traceability_links.py`, `skills/athena/scripts/validate_traceability_links.py`, `scripts/commit_with_traceability.py`, `skills/athena/scripts/commit_with_traceability.py`, `scripts/progress_schema.py`, `skills/athena/scripts/progress_schema.py`, `scripts/validate_progress_log.py`, `skills/athena/scripts/validate_progress_log.py`, `scripts/print_resume_prompt.py`, `skills/athena/scripts/print_resume_prompt.py`, `SKILL.md`, `skills/athena/SKILL.md`.
- Implemented in: `skills/athena/SKILL.md`, `core/athena-framework.md`, `README.md`, `AVAILABLE_SKILLS.md`, `adapters/codex/SKILL.md`, `adapters/claude/CLAUDE_PROMPT.md`, `scripts/validate_install_targets.py`, `publishing/linkedin-post-athena-flow-v1.md`, `publishing/linkedin-post-athena-flow-v2.md`, `publishing/linkedin-post-athena-flow-v3-personal-style.md`, `docs/images/athena-readme-fast-visual.svg`.
- Implemented in: `docs/specs/20260213-checkin-merge-remote/spec.md`, `docs/specs/20260213-checkin-merge-remote/tasks.md`, `scripts/print_resume_prompt.py`, `skills/athena/scripts/print_resume_prompt.py`, `scripts/bootstrap_git_audit.py`, `skills/athena/scripts/bootstrap_git_audit.py`, `.github/workflows/security.yml`, `docs/progress.txt`, `docs/specs/20260216-review-findings-remediation/spec.md`, `docs/specs/20260216-review-findings-remediation/tasks.md`.
- Implemented in: `skills/athena/assets/athena-warrior-icon.svg`, `docs/specs/20260217-athena-warrior-icon/spec.md`, `docs/specs/20260217-athena-warrior-icon/tasks.md`.
- Implemented in: `skills/athena/agents/openai.yaml`, `scripts/validate_install_targets.py`, `docs/specs/20260217-athena-install-icon-metadata/spec.md`, `docs/specs/20260217-athena-install-icon-metadata/tasks.md`.
- Implemented in: `docs/specs/20260217-absolute-path-hygiene/spec.md`, `docs/specs/20260217-absolute-path-hygiene/tasks.md`, `docs/specs/20260216-review-findings-remediation/spec.md`, `docs/progress.txt`.
