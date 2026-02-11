# Feature Spec: 20260211-public-release-hardening

Status: Done
Created: 2026-02-11 10:15
Inputs: CR-20260211-1010, CR-20260211-1019
Decisions: D-20260211-1012, D-20260211-1020

## Summary
- Harden this public-share repository for publication by cleaning local strings, adding governance/security artifacts, and rewriting history to a clean baseline.

## User Stories & Acceptance

### US1: Publish-ready hygiene (Priority: P1)
Narrative:
- As repo maintainer, I want a clean and hardened public repository, so external users get a trustworthy baseline.

Acceptance scenarios:
1. Given tracked files, When searching for local absolute paths, Then none are present. (Verifies: FR-001)
2. Given root policy files, When checking repository root, Then `.gitignore`, `SECURITY.md`, and `LICENSE` meet publication requirements. (Verifies: FR-002, FR-003, FR-004)
3. Given git history, When reviewing the branch graph, Then only the clean public baseline remains. (Verifies: FR-005)
4. Given repository governance configuration, When running the hardening audit, Then low-priority missing-items findings are resolved. (Verifies: FR-006, FR-007, FR-008)

## Requirements

Functional requirements:
- FR-001: Remove local absolute path strings from tracked docs. (Sources: CR-20260211-1010; D-20260211-1012)
- FR-002: Extend `.gitignore` with `.env`, `__pycache__/`, and `*.pyc`. (Sources: CR-20260211-1010; D-20260211-1012)
- FR-003: Add `SECURITY.md` for vulnerability reporting policy. (Sources: CR-20260211-1010; D-20260211-1012)
- FR-004: Add open-source MIT `LICENSE`. (Sources: CR-20260211-1010; D-20260211-1012)
- FR-005: Rewrite history to a truly clean public baseline. (Sources: CR-20260211-1010; D-20260211-1012)
- FR-006: Add single-owner `CODEOWNERS` policy for repository ownership. (Sources: CR-20260211-1019; D-20260211-1020)
- FR-007: Add `.github/dependabot.yml` and `.github/workflows/security.yml` for baseline automation hardening. (Sources: CR-20260211-1019; D-20260211-1020)
- FR-008: Enable repository-level `commit.gpgsign` in git config. (Sources: CR-20260211-1019; D-20260211-1020)

## Edge cases
- If the request log originally included local paths, retain intent while sanitizing path details for public exposure. (Verifies: FR-001)
