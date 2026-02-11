# Decisions (append-only)

## D-20260211-0940
Date: 2026-02-11 09:40
Inputs: CR-20260211-0939
PRD: Scope boundary for public repo artifacts

Decision:
Replace imported project-oriented docs with a clean, repo-scoped RALPH artifact set while preserving required traceability files (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`).

Rationale:
The user requested a public sharing repo that demonstrates RALPH itself, not historical artifacts from another project.

Alternatives considered:
- Keep imported artifacts as examples (rejected: scope leakage and noise in public share).
- Remove docs artifacts entirely (rejected: conflicts with explicit request to include RALPH docs artifacts).

Acceptance / test:
- `docs/` contains only this repo's RALPH artifacts.
- Imported report/spec files from other projects are removed.
- `git status` no longer includes generated local artifacts after ignore rules are added.

## D-20260211-1005
Date: 2026-02-11 10:05
Inputs: CR-20260211-1004
PRD: Public share positioning and skill scope

Decision:
Remove Daisy companion-skill references from the public RALPH repo content (`README.md`, `AVAILABLE_SKILLS.md`) and keep this shared version scoped strictly to RALPH.

Rationale:
The user explicitly requested that this version of RALPH no longer include Daisy.

Alternatives considered:
- Keep Daisy as optional companion text in docs (rejected: conflicts with explicit request).

Acceptance / test:
- `README.md` and `AVAILABLE_SKILLS.md` contain no Daisy companion-skill references.
- README/skills listing describe only RALPH for this public version.

## D-20260211-1012
Date: 2026-02-11 10:12
Inputs: CR-20260211-1010
PRD: Public release hardening and repository history policy

Decision:
Perform a public-release hardening pass by adding `.gitignore` security patterns, adding `SECURITY.md`, adding MIT `LICENSE`, removing local absolute path strings from tracked docs, and rewriting git history to a single clean public baseline commit.

Rationale:
The user explicitly requested a truly clean public repo and asked for these hardening artifacts.

Alternatives considered:
- Keep existing multi-commit history with prior imported content (rejected: not truly clean).
- Keep raw local path strings for strict verbatim logs (rejected: conflicts with public-sharing hygiene request).

Acceptance / test:
- No local absolute path strings remain in tracked files.
- `.gitignore` includes `.env`, `__pycache__/`, and `*.pyc`.
- `SECURITY.md` and `LICENSE` exist.
- Repository history is rewritten to a clean public baseline.

## D-20260211-1020
Date: 2026-02-11 10:20
Inputs: CR-20260211-1019
PRD: Low-priority hardening controls for public repository governance

Decision:
Complete the low-priority hardening findings by adding a single-owner `CODEOWNERS`, adding `.github/dependabot.yml`, adding `.github/workflows/security.yml`, and enabling repo-level `commit.gpgsign`.

Rationale:
The user explicitly approved finishing the low-priority hardening items and confirmed there is one code owner.

Alternatives considered:
- Skip low-priority items before publish (rejected: user explicitly requested completion).
- Use multiple owners in `CODEOWNERS` (rejected: conflicts with single-owner direction).

Acceptance / test:
- Security audit no longer reports missing `CODEOWNERS`, Dependabot config, workflow, or GPG signing configuration.

## D-20260211-1326
Date: 2026-02-11 13:26
Inputs: CR-20260211-1325
PRD: Resume execution handling and onboarding example backlog

Decision:
Interpret the resume command as instruction to continue from the existing `docs/progress.txt` NEXT backlog item and implement an onboarding walkthrough under `docs/examples/` as a new traceable feature.

Rationale:
No local artifact matched the provided resume UUID, and the safest deterministic continuation path is the explicit pending task already recorded in repo state.

Alternatives considered:
- Pause and ask for an external session export keyed to the UUID (rejected: unnecessary because a concrete pending task was already queued locally).
- Resume by selecting an arbitrary new task (rejected: breaks ordered execution from tracked backlog).

Acceptance / test:
- A new feature spec/task pair exists for the walkthrough deliverable.
- `docs/examples/` includes one end-to-end CR -> D -> FR -> T walkthrough.
- `docs/progress.txt` marks the walkthrough task as done with validation notes.
