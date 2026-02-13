# Hard Exit Experiment Summary

Runs:
- ATHENA: /Volumes/T9/code/SKILLS/athena/usecase-comparison/hard-exit-experiment/athena-run
- RALPH: /Volumes/T9/code/SKILLS/athena/usecase-comparison/hard-exit-experiment/ralph-run

Run timing:
- ATHENA start_utc: 2026-02-13T19:56:45Z
- ATHENA end_utc: 2026-02-13T19:56:48Z
- ATHENA duration_seconds: 3
- RALPH start_utc: 2026-02-13T19:56:57Z
- RALPH end_utc: 2026-02-13T19:57:02Z
- RALPH duration_seconds: 5

Iteration trace:
- ATHENA: 2 iterations tracked in `docs/iteration-log.md`
  - Iteration 1 intentionally incomplete
  - Iteration 2 final
- RALPH: 2 iterations tracked in `iteration-log.md` + `transcript-run1.jsonl` and `transcript-run2.jsonl`

Final artifact comparison:
- `output.txt` match: true
- `report.json` contents differ only by generated_at timestamp (`ATHENA`/`RALPH` run time)
- Completion signal: ATHENA done via task progression in `docs/progress.txt`; RALPH done with `<promise>TASK_DONE</promise>` in transcript2.
