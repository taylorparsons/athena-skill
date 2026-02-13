# Claude `athena-loop` Command Examples

## Basic run

```bash
/athena-loop "Implement FR-001 and update traceability docs" --max-iterations 8 --completion-promise "DONE"
```

## Tight loop for small changes

```bash
/athena-loop "Fix failing tests for T-003 and update progress log" --max-iterations 4 --completion-promise "DONE"
```

## Cancel current run

```bash
/cancel-athena
```

## Recommended usage pattern

1. Start with a bounded `--max-iterations`.
2. Set a concrete completion promise (for example: `DONE` or `ALL_TESTS_PASS`).
3. Keep traceability artifacts updated between iterations.
