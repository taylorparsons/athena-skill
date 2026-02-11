# RALPH Walkthrough: CR -> D -> FR -> T

This example shows one completed chain in this repository so new contributors can follow the audit trail end-to-end.

## 1) Customer request (`CR`)
- ID: `CR-20260211-1019`
- File: `docs/requests.md`
- Request summary: complete low-priority hardening and use one code owner.

## 2) Decision (`D`)
- ID: `D-20260211-1020`
- File: `docs/decisions.md`
- Interpretation: implement single-owner governance and baseline automation hardening items.

## 3) PRD requirements
- File: `docs/PRD.md`
- Requirement links:
  - `NFR-RALPH-007` (single-owner `CODEOWNERS`)
  - `NFR-RALPH-008` (`.github/dependabot.yml` + `.github/workflows/security.yml`)
  - `NFR-RALPH-009` (repo-level `commit.gpgsign`)
- Each requirement includes `Sources: CR-20260211-1019; D-20260211-1020`.

## 4) Feature spec requirements (`FR`)
- File: `docs/specs/20260211-public-release-hardening/spec.md`
- Requirement links:
  - `FR-006` -> single-owner `CODEOWNERS`
  - `FR-007` -> Dependabot and security workflow config
  - `FR-008` -> repo-level signing configuration
- Acceptance section includes `Verifies: FR-...` links.

## 5) Task execution (`T`)
- File: `docs/specs/20260211-public-release-hardening/tasks.md`
- Task links:
  - `T-006` implements `FR-006`
  - `T-007` implements `FR-007`
  - `T-008` implements `FR-008`

## 6) Progress evidence
- File: `docs/progress.txt`
- Evidence links:
  - DONE entries for `T-006`, `T-007`, and `T-008`
  - Notes describing audit/validation outcomes

## 7) Delivered repository artifacts
- `CODEOWNERS`
- `.github/dependabot.yml`
- `.github/workflows/security.yml`

## 8) Repeat this method for any new feature
1. Append a verbatim `CR-...` entry in `docs/requests.md`.
2. Add `D-...` only when interpretation/tradeoffs are required.
3. Update `docs/PRD.md` with `Sources: CR-...` and `D-...` as applicable.
4. Define `FR-...` requirements + acceptance scenarios in `docs/specs/<feature>/spec.md`.
5. Define `T-...` tasks mapped by `Implements: FR-...` in `docs/specs/<feature>/tasks.md`.
6. Execute one task at a time and record validation in `docs/progress.txt`.
