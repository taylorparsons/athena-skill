# Feature Spec: 20260217-athena-install-icon-metadata

## Metadata
- **Status:** Done
- **Created:** 2026-02-17 14:19
- **Inputs:** CR-20260217-1417
- **Decisions:** D-20260217-1419

## Summary
- Ensure ATHENA installs expose the warrior icon asset through skill metadata and keep that contract enforced by install-target validation.

## User Stories & Acceptance

### US1: Expose icon path in installed ATHENA metadata (Priority: P1)
Narrative:
- As a maintainer, I want the installed ATHENA skill metadata to point to `assets/athena-warrior-icon.svg`, so `.codex` installations can consume the icon deterministically.

Acceptance scenarios:
1. Given the installable skill package, When opening `skills/athena/agents/openai.yaml`, Then `icon_small` and `icon_large` both reference `./assets/athena-warrior-icon.svg`. (Verifies: FR-001)
2. Given install-target validation, When required icon bindings or files are missing, Then validation fails with actionable errors. (Verifies: FR-002)

## Requirements

Functional requirements:
- FR-001: Set `icon_small` and `icon_large` in `skills/athena/agents/openai.yaml` to `./assets/athena-warrior-icon.svg`. (Sources: CR-20260217-1417; D-20260217-1419)
- FR-002: Extend `scripts/validate_install_targets.py` to validate required icon asset/metadata bindings for `skills/athena`. (Sources: CR-20260217-1417; D-20260217-1419)

## Edge cases
- Validation must parse quoted YAML values and reject mismatched icon paths. (Verifies: FR-002)
