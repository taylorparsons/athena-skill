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
| PRD-driven loop execution | Yes | Yes |
| CR -> Decision -> PRD -> Spec -> Task traceability | Yes | Yes |
| Local commit traceability guidance | Yes | Yes |
| Runtime loop controls (`max-iterations`, completion string) | Optional/manual | Native via `ralph-loop` |
| Cancel active loop | Manual stop + resume log | Native via `/cancel-ralph` |
| Template-driven docs initialization | Yes | Yes |

## Quick Start

### Codex
1. Load `adapters/codex/SKILL.md`.
2. Keep `core/` and `templates/` available in the repo.
3. Optional activation: add `.codex/instruction.md` with `Use $ralph for PRD-driven, traceable delivery.`

### Claude
1. Use `adapters/claude/CLAUDE_PROMPT.md` as your project/system scaffold.
2. Run examples from `adapters/claude/COMMANDS.md` with `ralph-loop`.

## Publishing

- GitHub as source of truth (tags/releases).
- LinkedIn for launch story and adoption examples.
- See `publishing/launch-checklist.md`.
