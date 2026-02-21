# Feature Spec: 20260213-terminal-snake

Status: Active
Created: 2026-02-13 15:30
Inputs: CR-20260213-1530, CR-20260213-1231
Decisions: D-20260213-1530, D-20260213-1231

## Summary
Terminal snake implementation with deterministic replay and review artifacts.

## User Stories & Acceptance

### US1: Deterministic terminal game run
Narrative:
- As a reviewer, I want deterministic replay, so I can validate behavior repeatably.

Acceptance:
1. Given a seed and move script, when run, then final score, snake length, and collisions are reproducible. (Verifies: FR-SNAKE-001)

### US2: Evidence-first review
Narrative:
- As an evaluator, I want metrics and a visual artifact, so I can review end-to-end outcomes.

Acceptance:
1. When a run completes, `game-metrics.json` and `video.mp4` exist and show a coherent sequence. (Verifies: FR-SNAKE-002, FR-SNAKE-003)

### US3: One-command local execution
Narrative:
- As an implementer, I want a one-command entrypoint from `athena-run` so I can regenerate all artifacts reliably.

Acceptance:
1. Given I am in the `athena-run` directory, when I run `bash run.sh`, then `game-metrics.json`, `validation-report.json`, and `artifacts/video.mp4` are produced and `docs/run-metadata.md` is updated. (Verifies: FR-SNAKE-005)

## Requirements

- FR-SNAKE-001: terminal run consumes `moves.json` with direction values (`U|D|L|R` or `W|S|A|D`). (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-002: include deterministic random seeds for food spawn. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-003: emit per-step frame + metric trace in JSON and video artifact. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-005: `athena-run/run.sh` must run replay, validation, and rendering in one command path and emit run metadata. (Sources: CR-20260213-1231; D-20260213-1231)
