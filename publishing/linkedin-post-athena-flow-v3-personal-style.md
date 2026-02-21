# LinkedIn Post Draft V3: The Honest ATHENA Version

Most workflow posts are polished and vague.
This one is not.

## Problem

I wanted a way to ship work without losing the reasoning trail.
Not "we moved fast." Actual evidence:
- what request came in
- what I decided
- what changed
- what got validated
- what was checked in

## Constraint

If a process cannot survive audit later, it is not a process.
It is memory.
Memory fails.

## Decision

Use ATHENA as a strict loop:
1. Capture the request verbatim.
2. Record interpretation decisions.
3. Update PRD/spec/tasks with source links.
4. Execute one task at a time.
5. Validate.
6. Check in with traceability pointers.

## Evidence Path (invoke -> request -> loop -> check-in)

```text
$athena
"<customer request>"
```

Expected artifacts in order:
- `docs/requests.md` (raw input)
- `docs/decisions.md` (interpretation/tradeoffs)
- `docs/PRD.md` (requirements with Sources)
- `docs/specs/<feature-id>/spec.md` + `tasks.md`
- `docs/progress.txt` (commands, validation, outcomes)
- traceable local commit

## Install for Codex (copy/paste)

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo taylorparsons/athena-skill \
  --path skills/athena \
  --name athena
```

## Setup for Claude (copy/paste)

```bash
git clone https://github.com/taylorparsons/athena-skill.git
cd athena-skill
cat adapters/claude/CLAUDE_PROMPT.md
cat adapters/claude/COMMANDS.md
```

Use the prompt content in `adapters/claude/CLAUDE_PROMPT.md` as your project/system prompt.
Use commands from `adapters/claude/COMMANDS.md` (for example `/athena-loop ...`).

## Risk

The common failure mode is style over substance:
- good narrative
- no traceability
- no reproducibility

ATHENA is designed to reject that pattern.

## Confidence

High when all six artifacts exist and the commit references them.
Low if any link in the chain is missing.

That is the bar.
