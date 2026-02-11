# RALPH Framework

RALPH is an agent-agnostic delivery framework for PRD-driven, traceable software execution.

This repository packages:
- the full Codex `ralph` skill (`SKILL.md`) for parity with local usage,
- a canonical core loop,
- Codex and Claude adapter materials,
- reusable templates,
- core helper scripts,
- and a clean `docs/` artifact trail scoped to this repo.

## Repository Layout

- `SKILL.md`: full Codex `ralph` skill definition (parity target)
- `core/ralph-framework.md`: canonical, agent-neutral RALPH loop
- `adapters/codex/SKILL.md`: Codex adapter
- `adapters/claude/CLAUDE_PROMPT.md`: Claude adapter prompt
- `adapters/claude/COMMANDS.md`: Claude `ralph-loop` command examples
- `templates/`: ready-to-copy traceability templates
- `scripts/`: helper automation (`commit_with_traceability.py`, `bootstrap_git_audit.py`, `print_resume_prompt.py`)
- `VERSION`: source-of-truth skill/repo version (SemVer)
- `docs/`: this repo's own RALPH artifacts (`requests`, `decisions`, `PRD`, `specs`, `progress`)
- `docs/examples/`: optional onboarding walkthroughs that demonstrate traceability flow

## Versioning

- Version source of truth: `VERSION`
- Scheme: Semantic Versioning (`MAJOR.MINOR.PATCH`)
- Git tag format: `v<MAJOR>.<MINOR>.<PATCH>`
- Bump guidance:
  - `PATCH`: docs fixes, clarifications, non-breaking script updates
  - `MINOR`: additive capabilities (new templates/scripts/adapters) without breaking behavior
  - `MAJOR`: breaking workflow or contract changes

## Compatibility Status

- Codex: parity target with local `~/.codex/skills/ralph/SKILL.md` (no intentional capability reductions).
- Claude: adapter materials are included, but parity with Codex behavior is treated as a later compatibility release.

## Compared to Claude `ralph-loop` Plugin

| Dimension | `ralph-traceability-loop` (this repo) | Claude original `ralph-loop` plugin |
|---|---|---|
| Primary orientation | Agent-agnostic framework for PRD-driven traceability | Claude-native plugin for interactive AI loops |
| Supported environments | Codex-first (`SKILL.md`) with Claude adapter docs staged | Claude Code plugin runtime |
| Installation approach | Clone/use repo files (`core/`, `adapters/`, `templates/`, `scripts/`) | `claude plugin install ralph-loop@claude-plugins-official` |
| Core operating model | `CR -> Decision -> PRD -> Spec -> Task -> Progress` artifacts under `docs/` | Iterative loop workflow inside Claude plugin UX |
| Governance package | Includes `LICENSE`, `SECURITY.md`, `CODEOWNERS`, Dependabot and security workflow | Not specified on the plugin page |
| Publisher/verification signal | Maintainer-owned open GitHub repository | Marked "Anthropic Verified" on plugin page |
| Best fit | Teams needing explicit audit trails and cross-agent portability | Users prioritizing Claude-native loop execution commands |

Reference:
- https://claude.com/plugins/ralph-loop

## Quick Start

### Codex
1. Load `SKILL.md`.
2. Keep `core/`, `templates/`, and `scripts/` available in the repo.
3. Optional activation: add `.codex/instruction.md` with `Use $ralph for PRD-driven, traceable delivery.`
4. Use bundled helpers:
   - `python3 scripts/commit_with_traceability.py ...`
   - `python3 scripts/bootstrap_git_audit.py --out docs/audit/git-history.md`
   - `python3 scripts/print_resume_prompt.py --repo .`
5. If you need additional Codex-only helpers not bundled here, install the full `ralph` skill via `$skill-installer` into `$CODEX_HOME/skills`.

### Claude
1. Use `adapters/claude/CLAUDE_PROMPT.md` and `adapters/claude/COMMANDS.md` as staged compatibility materials.
2. Treat Claude parity as a subsequent release track.

## Publishing

- GitHub as source of truth (tags/releases).
- LinkedIn for launch story and adoption examples.
- See `publishing/launch-checklist.md`.
