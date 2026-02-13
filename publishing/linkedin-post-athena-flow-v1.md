# LinkedIn Post Draft V1: ATHENA Loop in 60 Seconds

I wanted a repeatable way to move from a raw request to a clean check-in without losing auditability.

That is what ATHENA does.

## The logical flow

1. Invoke ATHENA in the session.
2. Capture the customer request verbatim in `docs/requests.md`.
3. Record interpretation decisions in `docs/decisions.md`.
4. Translate request -> requirements in `docs/PRD.md`.
5. Map requirements to `docs/specs/<feature-id>/spec.md` and `tasks.md`.
6. Work one task at a time and log commands/outcomes in `docs/progress.txt`.
7. Validate, reconcile docs, then check in with traceability pointers.

Result: request -> decision -> requirement -> task -> evidence -> commit.

## Install for Codex (copy/paste)

```bash
python3 "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo taylorparsons/athena-skill \
  --path skills/athena \
  --name athena
```

## Install / setup for Claude (copy/paste)

```bash
git clone https://github.com/taylorparsons/athena-skill.git
cd athena-skill
cat adapters/claude/CLAUDE_PROMPT.md
cat adapters/claude/COMMANDS.md
```

Then paste the prompt content from `adapters/claude/CLAUDE_PROMPT.md` into your Claude project/system instructions.

## Example invocation + request + loop execution

```text
$athena
"Implement feature X, update docs, and check in with traceability."
```

Expected loop behavior:
- request captured
- decisions logged
- PRD/spec/tasks updated
- one task moved to IN PROGRESS
- implementation + validation
- progress reconciled
- local check-in created

## Why this matters

ATHENA keeps delivery fast, but evidence-first.
You can always reconstruct why a change was made and how it was validated.
