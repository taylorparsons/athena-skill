# Skills In This Repo

## Installable Skills

1. `athena`
- Path: `skills/athena`
- Install:
  ```bash
  python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
    --repo taylorparsons/athena-skill \
    --path skills/athena \
    --name athena
  ```

## Guardrail

Do not use `--path .` when installing from this repository. It copies the entire repo.
