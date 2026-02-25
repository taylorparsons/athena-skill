# ATHENA Framework

![How the ATHENA Skill Works](docs/images/athena-readme-fast-visual.svg)

ATHENA is an agent-agnostic delivery framework for PRD-driven, traceable software execution.

## What ATHENA Does

ATHENA creates a **complete audit trail from customer request to shipped code**:

- **Captures customer requests verbatim** in `docs/requests.md` (CR-... IDs)
- **Documents design decisions** in `docs/decisions.md` (D-... IDs)
- **Maintains a living PRD** in `docs/PRD.md` with full traceability
- **Specs features** in `docs/specs/<FEATURE_ID>/spec.md` with functional requirements (FR-...)
- **Lists tasks** in `docs/specs/<FEATURE_ID>/tasks.md` linked to requirements (Implements: FR-...)
- **Tracks execution** in `docs/progress.txt` with validation evidence
- **Creates traceable Git commits** referencing CR/D/FEATURE_ID/T-... IDs
- **Enables auditing** via `docs/TRACEABILITY.md` to follow any request through to code

## Installation

### Option A: Codex with `skill-installer`

When running in Codex with `skill-installer` available:

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo taylorparsons/athena-skill \
  --path skills/athena \
  --name athena
```

This installs `skills/athena/SKILL.md` into Codex's skill registry.

### Option B: Claude Code CLI

In an active Claude Code session, paste this prompt:

```
Install the athena skill from https://github.com/taylorparsons/athena-skill — copy skills/athena/SKILL.md into ~/.claude/skills/athena/SKILL.md
```

Claude will fetch the file and write it to `~/.claude/skills/athena/SKILL.md`. Once installed, the skill is available in all future Claude Code sessions.

**Verify:** Check that `~/.claude/skills/athena/SKILL.md` exists, or run `/skills` in Claude Code to confirm `athena` appears in the list.

### Option C: Bootstrap ATHENA docs in a project

To set up the ATHENA docs structure (`docs/requests.md`, `docs/decisions.md`, `docs/PRD.md`, `docs/specs/`, etc.) inside an existing project, open Claude Code in that project and paste:

```
Setup ATHENA docs in this project from https://github.com/taylorparsons/athena-skill
```

Claude will create the full docs scaffold. This is separate from skill installation — you can do both, or just one depending on your workflow.

## Install Target

- `skills/athena/`: canonical full `athena` skill for Codex/Claude Code
- Contains exactly one `SKILL.md` with required frontmatter (`name`, `description`)

## Quick Start (5 minutes)

1. **Review the framework**: Read `core/athena-framework.md` (10-step ATHENA loop)
2. **Understand the structure**: Check `docs/TRACEABILITY.md` (audit trail entry point)
3. **Add your first request**: Edit `docs/requests.md`, add a CR-... entry with your requirement
4. **Create a feature spec**: Copy template from `templates/spec.md` to `docs/specs/<FEATURE_ID>/spec.md`
5. **Make decisions**: Add to `docs/decisions.md` if you need to interpret the request
6. **Start executing**: Create `docs/specs/<FEATURE_ID>/tasks.md` from template and tackle one task at a time

## Repository Layout

- `skills/athena/`: installable `athena` package
- `core/athena-framework.md`: canonical, agent-neutral ATHENA loop
- `adapters/`: framework adapter source materials
- `templates/`: traceability templates
- `scripts/`: helper automation (`commit_with_traceability.py`, `bootstrap_git_audit.py`, `print_resume_prompt.py`)
- `VERSION`: source-of-truth framework version (SemVer)
- `docs/`: this repo's own ATHENA artifacts and examples (walkthrough examples in `docs/examples/`)

## Key Files & What They Do

| File | Purpose |
|------|---------|
| `core/athena-framework.md` | Complete ATHENA methodology and 10-step loop |
| `docs/TRACEABILITY.md` | Entry point: navigate from request to code |
| `docs/requests.md` | Customer inputs (append-only log) |
| `docs/decisions.md` | Design decisions (append-only log) |
| `docs/PRD.md` | Living requirements document |
| `docs/specs/*/spec.md` | Feature specifications with acceptance criteria |
| `docs/specs/*/tasks.md` | Implementation tasks (Implements: FR-...) |
| `docs/progress.txt` | Execution log with evidence and session notes |
| `templates/` | Ready-to-use templates for specs, tasks, requests, decisions, progress |
| `scripts/` | Helper utilities (`commit_with_traceability.py`, `bootstrap_git_audit.py`, etc.) |
| `adapters/claude/` | Claude-specific guidance (`COMMANDS.md`, `CLAUDE_PROMPT.md`) |
| `adapters/codex/` | Codex skill adapter |

## Non-Negotiable Rules

1. **Capture verbatim**: Record customer requests exactly as stated before changing anything.
2. **Append-only logs**: Never delete or edit `docs/requests.md` or `docs/decisions.md` entries.
3. **Full traceability**: Link sources (CR/D) to requirements (FR) to tasks (T).
4. **Single focus**: Only one task `IN PROGRESS` at a time.
5. **Evidence required**: Every task needs test/check results.
6. **Git integration**: Commit messages reference CR/D/FEATURE_ID/T-... IDs.
7. **Never auto-push**: Only push to remote when explicitly requested.

## Validation

Run install-target validation locally:

```bash
python3 scripts/validate_install_targets.py
```

This checks:
- each declared install target exists,
- each target has exactly one `SKILL.md`,
- frontmatter includes required `name` and `description`.

## Versioning

- Version source of truth: `VERSION`
- Scheme: Semantic Versioning (`MAJOR.MINOR.PATCH`)
- Git tag format: `v<MAJOR>.<MINOR>.<PATCH>`

## Help & Resources

- **Examples**: `docs/examples/01-cr-to-task-walkthrough.md` (step-by-step example)
- **Claude Adapter**: `adapters/claude/CLAUDE_PROMPT.md` and `adapters/claude/COMMANDS.md`
- **Codex Skill**: `adapters/codex/SKILL.md` (Codex skill definition)

## Publishing

- GitHub as source of truth (tags/releases)
- LinkedIn for launch/adoption examples
- `publishing/launch-checklist.md`
