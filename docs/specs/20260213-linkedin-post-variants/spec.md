# Feature Spec: 20260213-linkedin-post-variants

## Metadata
- **Status:** Done
- **Created:** 2026-02-13 09:15
- **Inputs:** CR-20260213-0912
- **Decisions:** D-20260213-0913

## Summary
- Create two LinkedIn-ready post variants that explain ATHENA end-to-end flow from invocation/request through loop execution to check-in completion, with clear install instructions for both Codex and Claude using copy/paste-friendly code blocks.

## User Stories & Acceptance

### US1: Explain the ATHENA loop in a post-ready format (Priority: P1)
Narrative:
- As a maintainer sharing ATHENA publicly, I want post-ready content that clearly explains the workflow and setup, so readers can understand and adopt it quickly.

Acceptance scenarios:
1. Given post draft version 1, When reviewed, Then it includes a clear invoke -> request -> loop -> check-in narrative and codex/claude install blocks. (Verifies: FR-001, FR-002, FR-003)
2. Given post draft version 2, When reviewed, Then it presents the same core content with a distinct framing/style and codex/claude install blocks. (Verifies: FR-001, FR-002, FR-003)

## Requirements

Functional requirements:
- FR-001: Provide two distinct LinkedIn-ready post draft files under `publishing/`. (Sources: CR-20260213-0912; D-20260213-0913)
- FR-002: Each draft MUST include ATHENA logical flow from invocation and customer request through loop steps to local check-in completion. (Sources: CR-20260213-0912; D-20260213-0913)
- FR-003: Each draft MUST include clear copy/paste code blocks for installation guidance covering both Codex and Claude usage. (Sources: CR-20260213-0912; D-20260213-0913)

## Edge cases
- Keep instructions concise enough for LinkedIn while preserving runnable command blocks. (Verifies: FR-003)
