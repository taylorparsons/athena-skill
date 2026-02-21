# PRD: Terminal Snake Playable Demo + Video Metrics

Status: Active
Updated: 2026-02-13 15:30
Inputs: CR-20260213-1530, CR-20260213-1231
Decisions: D-20260213-1530, D-20260213-1231

## Goals
- Build a terminal Snake implementation that can run deterministically from CLI.
- Produce reproducible run logs and an MP4-like visual artifact for review.

## Functional requirements
- FR-SNAKE-001: `src/snake_game.py` reads an input move script and runs game from terminal. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-002: `src/validate_snake_game.py` validates movement, collision handling, food consumption, growth, and deterministic seed behavior. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-003: `src/render_snake_video.py` creates `artifacts/video.mp4` from frame capture. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-004: Final artifacts include `game-metrics.json` and run metadata with UTC start/end. (Sources: CR-20260213-1530; D-20260213-1530)
- FR-SNAKE-005: `run.sh` in `athena-run` runs deterministic replay, validation, and video render from that directory. (Sources: CR-20260213-1231; D-20260213-1231)
