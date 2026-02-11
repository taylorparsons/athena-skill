# Skills In This Repo

## Installable Skills

1. `ralph`
- Path: `skills/ralph`
- Install:
  ```bash
  python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
    --repo taylorparsons/ralph-traceability-loop \
    --path skills/ralph \
    --name ralph
  ```

## Guardrail

Do not use `--path .` when installing from this repository. It copies the entire repo.
