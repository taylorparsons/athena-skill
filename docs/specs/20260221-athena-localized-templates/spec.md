# Feature Spec: 20260221-athena-localized-templates

Status: Done
Created: 2026-02-21 12:52
Inputs: CR-20260221-1252
Decisions: D-20260221-1255

## Summary
- Keep ATHENA reusable templates inside the `skills/athena` package so the installed skill is self-contained and always references local template assets.

## User Stories & Acceptance

### US1: Template packaging (Priority: P1)
Narrative:
- As an operator, I want ATHENA workflow templates to live under `skills/athena`, so that a packaged installation uses local templates without repo-root assumptions.

Acceptance scenarios:
1. Given `skills/athena` is used as the active package, When I open `skills/athena/SKILL.md`, Then it should reference only files under `skills/athena/templates/*` for request/decision/progress/spec/task/traceability templates. (Verifies: FR-001)

## Requirements

Functional requirements:
- FR-001: ATHENA templates for this packaged skill are stored under `skills/athena/templates/` and include `requests.md`, `decisions.md`, `progress.txt`, `spec.md`, `tasks.md`, and `traceability.md`. (Sources: CR-20260221-1252; D-20260221-1255)
