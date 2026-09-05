# ATHENA Core Framework (Agent-Agnostic)

## Canonical workflow

Follow [the root SKILL.md](../SKILL.md) for mode selection, permissions, retrieval, implementation and completion. The installable copy at `skills/athena/SKILL.md` is kept identical by regression checks. This file describes the artifact model, not a second execution loop.

## Core Artifacts

- `docs/requests.md`: append-only customer inputs
- `docs/decisions.md`: append-only interpretation/tradeoff log
- `docs/PRD.md`: source of truth requirements
- `docs/specs/<feature-id>/spec.md`: feature requirements + acceptance scenarios
- `docs/specs/<feature-id>/tasks.md`: implementation tasks linked to requirements
- `docs/specs/<feature-id>/notes.md`: append-only execution notes and recovery fields
- `docs/TRACEABILITY.md`: audit entry point

## Retrieval and legacy repositories

Use `./scripts/owl` for audit-log queries and writes as directed by the canonical workflow. `docs/progress.txt` is a legacy format; see [setup](../references/setup.md) for migration. Reviews do not authorize migration or other writes.
