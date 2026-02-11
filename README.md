# RALPH Framework

RALPH is an agent-agnostic delivery framework for PRD-driven, traceable software execution.

## Install (Recommended)

Install from explicit skill paths so `skill-installer` copies only the intended skill package.

### Install `ralph`

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo taylorparsons/ralph-traceability-loop \
  --path skills/ralph \
  --name ralph
```

### Important

Do **not** install with `--path .`.

Why: `skill-installer` copies the entire selected directory. Using repo root (`.`) pulls the whole repository into your installed skill folder and can expose multiple `SKILL.md` files.

## Install Target

- `skills/ralph`: canonical full `ralph` skill for Codex

This install target is designed to contain exactly one `SKILL.md`.

## Repository Layout

- `skills/ralph/`: installable `ralph` package
- `core/ralph-framework.md`: canonical, agent-neutral RALPH loop
- `adapters/`: framework adapter source materials
- `templates/`: traceability templates
- `scripts/`: helper automation (`commit_with_traceability.py`, `bootstrap_git_audit.py`, `print_resume_prompt.py`)
- `VERSION`: source-of-truth framework version (SemVer)
- `docs/`: this repo's own RALPH artifacts and examples

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

## Publishing

- GitHub as source of truth (tags/releases)
- LinkedIn for launch/adoption examples
- `publishing/launch-checklist.md`
