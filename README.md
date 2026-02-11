# RALPH Framework

RALPH is an agent-agnostic delivery framework for PRD-driven, traceable software execution.

This repository packages:
- a canonical core loop,
- Codex and Claude adapters,
- reusable templates,
- and a clean `docs/` artifact trail scoped to this repo.

## Repository Layout

- `core/ralph-framework.md`: canonical, agent-neutral RALPH loop
- `adapters/codex/SKILL.md`: Codex adapter
- `adapters/claude/CLAUDE_PROMPT.md`: Claude adapter prompt
- `adapters/claude/COMMANDS.md`: Claude `ralph-loop` command examples
- `templates/`: ready-to-copy traceability templates
- `docs/`: this repo's own RALPH artifacts (`requests`, `decisions`, `PRD`, `specs`, `progress`)

## Compatibility Matrix

| Capability | Codex Adapter | Claude Adapter |
|---|---|---|
| Canonical RALPH loop parity (`core/ralph-framework.md`) | Yes | Yes |
| PRD-driven loop execution | Yes | Yes |
| Capture request before PRD/code edits | Yes | Yes |
| Decision log for scope/tradeoff interpretation | Yes | Yes |
| CR -> Decision -> PRD -> Spec -> Task traceability | Yes | Yes |
| Enforce single `IN PROGRESS` task discipline | Yes | Yes |
| Record command/check outcomes in progress log | Yes | Yes |
| Evidence-based completion criteria | Yes | Yes |
| Template-driven docs initialization | Yes | Yes |
| Local commit traceability guidance | Yes | Yes |
| Push protection (`never push unless explicitly requested`) | Yes | Yes |
| Runtime loop controls (`--max-iterations`, completion promise) | Optional/manual | Native via `ralph-loop` command pattern |
| Cancel active loop | Manual stop + resume from docs/progress | Native via `/cancel-ralph` |
| Adapter activation mechanism | Load `adapters/codex/SKILL.md` (optionally via `.codex/instruction.md`) | Use `adapters/claude/CLAUDE_PROMPT.md` + `adapters/claude/COMMANDS.md` |

## Quick Start

### Codex
1. Load `adapters/codex/SKILL.md`.
2. Keep `core/` and `templates/` available in the repo.
3. Optional activation: add `.codex/instruction.md` with `Use $ralph for PRD-driven, traceable delivery.`
4. This public repo is framework/docs only. If you need Codex helper Python scripts (for example traceable commit/audit helpers), install the full `ralph` skill via `$skill-installer` into `$CODEX_HOME/skills`.

### Claude
1. Use `adapters/claude/CLAUDE_PROMPT.md` as your project/system scaffold.
2. Run examples from `adapters/claude/COMMANDS.md` with `ralph-loop`.

## Publishing

- GitHub as source of truth (tags/releases).
- LinkedIn for launch story and adoption examples.
- See `publishing/launch-checklist.md`.
