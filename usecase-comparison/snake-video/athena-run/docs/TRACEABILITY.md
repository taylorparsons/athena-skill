# Traceability (How to follow this use case)

## ID Index
- Customer request ID: `CR-20260213-1530`
- Customer request ID: `CR-20260213-1231`
- Decision ID: `D-20260213-1530`
- Decision ID: `D-20260213-1231`
- Feature ID: `20260213-terminal-snake`
- Requirement IDs:
  - `FR-SNAKE-001`
  - `FR-SNAKE-002`
  - `FR-SNAKE-003`
  - `FR-SNAKE-005`
- Task ID:
  - `T-001`

## Decision Tree (with IDs)

- `docs/requests.md` (`CR-20260213-1530`, `CR-20260213-1231`)
  - `docs/decisions.md` (`D-20260213-1530`, `D-20260213-1231`)
    - `docs/PRD.md` (`inputs: CR-20260213-1530`, `CR-20260213-1231`; `decisions: D-20260213-1530`, `D-20260213-1231`)
      - `docs/specs/20260213-terminal-snake/spec.md`
        - `FR-SNAKE-001`
        - `FR-SNAKE-002`
        - `FR-SNAKE-003`
        - `FR-SNAKE-005`
      - `docs/specs/20260213-terminal-snake/tasks.md`
        - `T-001` (implements `FR-SNAKE-001`, `FR-SNAKE-002`, `FR-SNAKE-003`, `FR-SNAKE-005`)
      - `docs/progress.txt` (tracks task state for `T-001`)
      - `docs/run-metadata.md` (captures run timing)
      - output artifacts (`game-metrics.json`, `validation-report.json`, `artifacts/video.mp4`)
