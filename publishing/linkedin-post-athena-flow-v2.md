# LinkedIn Post Draft V2: From "Can you build this?" to Traceable Check-In

A lot of teams can ship fast.
Fewer teams can explain exactly how a request became a requirement, then code, then a validated check-in.

ATHENA is the operating loop I use for that.

## What happens when ATHENA is called

- You call `$athena`.
- The request is captured exactly as given.
- Any interpretation is explicitly recorded as a decision.
- Requirements are updated with source links.
- Tasks are selected one-by-one.
- Work is implemented and validated.
- Check-in is created with references back to request/decision/spec/task/progress evidence.

It is a straight line from ask -> execution -> proof.

## Codex install (copy/paste)

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo taylorparsons/athena-skill \
  --path skills/athena \
  --name athena
```

## Claude setup (copy/paste)

```bash
git clone https://github.com/taylorparsons/athena-skill.git
cd athena-skill
cp adapters/claude/CLAUDE_PROMPT.md /tmp/ATHENA_CLAUDE_PROMPT.md
cp adapters/claude/COMMANDS.md /tmp/ATHENA_CLAUDE_COMMANDS.md
```

Use `/tmp/ATHENA_CLAUDE_PROMPT.md` as your Claude project/system prompt, then run commands from `/tmp/ATHENA_CLAUDE_COMMANDS.md` (for example `/athena-loop ...`).

## Request-to-checkin example

```text
$athena
"Create two LinkedIn-ready post variants with install instructions for Codex and Claude, then check in changes."
```

Loop completion criteria:
- artifacts updated (`requests`, `decisions`, `PRD`, `spec`, `tasks`, `progress`)
- validations executed and logged
- task moved to DONE
- traceable commit written

If you care about explainable delivery, this pattern is a practical baseline.
