# Decisions (append-only)

## D-20260213-1530
Date: 2026-02-13 15:30
Inputs: CR-20260213-1530
PRD: Snake terminal game + metrics

Decision:
Use one deterministic CLI snake engine with optional move replay and JSON frame capture, then generate a local MP4 from frame renders for review.

Rationale:
This gives objective, reviewable evidence across runtime and terminal behavior without external assumptions.

Alternatives considered:
- Pure interactive-only game (rejected because hard to automate reproducible review)
- No replay seed mode (rejected because it prevents deterministic validation)

Acceptance / test:
- Both ATHENA and RALPH runs must produce `game-metrics.json` and `video.mp4`.
- Play/pause/quit workflow is deterministic from replay moves.

## D-20260213-1231
Date: 2026-02-13 12:31
Inputs: CR-20260213-1231
PRD: Terminal Snake Playable Demo + Video Metrics

Decision:
Add a local executable entrypoint (`run.sh`) under `athena-run` so the use case can be run end-to-end from that directory without manually chaining scripts.

Rationale:
This satisfies the request for location-specific execution while keeping game logic unchanged and minimizing operational complexity.

Alternatives considered:
- Create a new orchestration language (rejected because this use case only needs one stable command).
- Add manual documented commands in `docs` only (rejected because it still invites human error and missing-step runs).

Acceptance / test:
- Running `bash run.sh` from `athena-run` produces/rebuilds `game-metrics.json`, `validation-report.json`, `artifacts/video.mp4`, and updates `docs/run-metadata.md`.
