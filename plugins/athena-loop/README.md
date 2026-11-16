# Athena Loop

A Claude Code plugin for ATHENA, a PRD-driven delivery loop with a token-lean audit trail: requests, decisions, specs, tasks, and commits.

It adds the `athena` skill and the Owl of Athena sub-agent. The skill walks Claude through capturing each request verbatim, recording decisions, keeping a feature spec and task list, and linking commits back to them.

## Who it is for

Developers who use Claude Code and want every change tied to a written request, decision, requirement, and task.

## Install

```
/plugin install athena-loop --marketplace taylorparsons/athena-skill
```

Requires Claude Code 2.1.275 or later.

## What it does not include

This plugin ships Markdown only: the skill, its references and templates, and the Owl agent. It includes no scripts or programs. The skill refers to `./scripts/owl` in your project. To set that up, follow the "Bootstrap ATHENA docs" steps in the main repository README: https://github.com/taylorparsons/athena-skill

## Usage

Ask Claude to start work on a feature in a project that uses ATHENA docs, for example: "Use ATHENA to add input validation to the signup form." Claude follows the loop in `skills/athena/SKILL.md`.

## Privacy

Athena Loop collects and transmits nothing. It has no network calls, no telemetry, and no connectors. Anything it writes goes to your own project's `docs/` folder. See the Privacy section of the main README: https://github.com/taylorparsons/athena-skill#privacy

## License

MIT. See LICENSE. Contact: taylor.parsons@gmail.com

Source of truth: https://github.com/taylorparsons/athena-skill (this folder is copied from `skills/athena`; keep them in sync).
