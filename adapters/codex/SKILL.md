---
name: athena-codex
description: Use the ATHENA framework in Codex for PRD-driven, traceable delivery. Trigger when the user wants iterative execution with auditable CR/Decision/Spec/Task artifacts and disciplined one-task-at-a-time implementation.
---

# ATHENA Codex Adapter

The loop is identical on every harness — follow `../../skills/athena/SKILL.md`. This adapter only covers Codex wiring.

## Codex wiring

- Session open: run `./scripts/owl context` regardless of optional harness memory or hooks. Reconcile recorded context with live state and the current request.
- Keep `~/.codex/AGENTS.md` minimal (trigger + stop-gates only, ≤ 15 lines). Do not duplicate loop steps there — the loop lives in SKILL.md. Recommended block:

      ## ATHENA for repositories using its audit trail
      - Invoke athena and select the requested mode before work.
      - Review, explanation and diagnosis are read-only unless changes are requested.
      - Session open: ./scripts/owl context
      - Never Read docs/requests.md, docs/decisions.md, or docs/athena-index.md —
        use ./scripts/owl (add-request, add-decision, add-note, show, why).
      - No code changes until the current request is captured (owl add-request)
        and reflected in docs/PRD.md.
      - If a gate was missed, reconcile the missing traceability before further changes.
      - Preserve completed work; ask if reconciliation requires new scope or permission.

- Install the full package with `$skill-installer` into `$CODEX_HOME/skills/athena`, then run scripts from `$CODEX_HOME/skills/athena/scripts/` (or a local `./scripts/owl` wrapper).

## Versioning

Use Semantic Versioning from `../../VERSION`. Breaking process changes require a major bump.
