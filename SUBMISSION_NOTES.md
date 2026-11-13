# Submission Notes: ATHENA Claude plugin

**DRAFT answers for the owner to confirm.** Nothing here has been submitted. Prepared on branch `submission-prep` from a code audit on 2026-11-13. Items marked **TODO** need an owner answer. Nothing in this file was invented.

## Plugin identity

| Field | Value | Source |
|---|---|---|
| Name | `athena` | `.claude-plugin/plugin.json`; matches skill name |
| Version | `2.2.0` | `VERSION`; matches git tag `v2.2.0` |
| License | MIT | `LICENSE` (Copyright 2026 Taylor Parsons) |
| Author | Taylor Parsons | `LICENSE` copyright line |
| Repository | https://github.com/taylorparsons/athena-skill (public) | `git remote`; `gh repo view` |
| Icon | `.claude-plugin/icon.png`, 1024×1024 PNG | rendered from `skills/athena/assets/athena-warrior-icon.svg` |

The request named the repo `atheha-skill`. The actual repo is `athena-skill`, and all files use that name.

## TODO: owner must answer before submitting

- **Contact email for Anthropic:** taylor.parsons@gmail.com (supplied by the owner; set as `author.email` in `plugin.json`).
- **Author website:** TODO. None found in the repo beyond the GitHub account.
- **License:** confirm MIT. It is taken from `LICENSE`, not chosen here.
- **Branch or tag to track:** TODO. Options: `main` (default branch) or tag `v2.2.0` (latest tag, matches `VERSION`).
- **Icon approval:** the directory locks the icon the first time the plugin is saved or submitted. Confirm `.claude-plugin/icon.png` is the one to lock.
- **Shipped internal logs:** the plugin is the whole repo (see "Content the plugin ships" below). Decide whether to keep these or exclude them before submitting. Nothing was deleted.
- **Duplicate Owl agent file:** `agents/owl-of-athena.md` (shipped) and `.claude/agents/owl-of-athena.md` (local) differ by 21 diff lines. The shipped copy matches `skills/athena/agents/owl-of-athena.md`. Confirm the shipped copy is the current one.

## Data handling (draft answers)

**Does the plugin read or store personal data?**
Draft: The plugin's code reads and writes files on the user's machine. It does not collect data from the user. Its audit logs (`docs/requests.md`, `docs/decisions.md`, specs, tasks) hold the text the user types into Claude Code, verbatim, so any personal information the user types ends up in those files. The owner should confirm this description.

**What is stored, and where?**
- Project `docs/` files in the user's repo (requests, decisions, specs, tasks, `athena-index.md`).
- `owl write-memory` writes the active feature, goal, and task state to `~/.claude/projects/<encoded-repo-path>/memory/`. The bash fallback in `scripts/owl` and `scripts/install-owl.sh` also copy up to 100 lines of active request text from `docs/requests.md` into that memory directory.
- `scripts/patch-claude-settings.py` edits `~/.claude/settings.json` and `~/.claude/CLAUDE.md`. It runs only when the user runs it.
- `scripts/sweep-projects.py` writes `~/.claude/logs/athena-sweep.log`. It runs only when the user schedules or runs it. By default it scans `$HOME` and `/Volumes` for `docs/requests.md` files and reads spec status lines. It sends nothing.

**How long is data kept?**
Draft: The code has no retention or deletion policy. Logs are append-only and persist until the user deletes them. `owl archive` moves the feature entry in `athena-index.md` and its progress lines into `progress-archive.txt`. Spec files stay in place.

**Does it send data to any service other than the ones it declares?**
Draft: No. The scripts make no network calls. The only subprocesses are local `git`, `find`, `owl`, and `python3` calls. Checked by grepping all tracked `.py`, `.sh`, `.js`, `.ts`, and `.yml` files for `curl`, `wget`, `urllib`, `requests.*`, `httpx`, `urlopen`, `socket`, and `fetch(`. No matches in code. Matches appear only in historical docs and logs (see below).

**Declared services.** The plugin declares none. Claude Code and the model host receive whatever the user types, as in any Claude Code session. That is platform behavior, not plugin behavior.

**Does it run git push or GitHub CLI?**
Only when the user or an agent asks. The docs say `git push` and PR creation need explicit user approval (`references/commits.md`).

## Security scan: items that may flag

- **No secrets found.** Grepped all tracked files for GitHub tokens, OpenAI-style keys, AWS keys, Slack tokens, private key blocks, and `password`/`token`/`api_key` assignments. No matches.
- **No personal identifiers in code.** No `/Users/taylorparsons` path and no personal email in code. One `notes.md` match for "gmail" is a plugin name in an inventory list.
- **Hard-coded machine paths in logs and docs.** `/Volumes/T9/code/SKILLS/athena` appears in historical docs and logs (`docs/requests.md`, `docs/decisions.md`, `docs/progress-archive.txt`, `docs/audit/progress-legacy.txt`, `usecase-comparison/**`). Not in code.
- **`curl | bash` text in logs.** `docs/requests.md` (line 142) and `docs/audit/progress-legacy.txt` (line 109) contain `curl -fsSL https://claude.ai/install.sh | bash`. Recorded text, not run by the plugin. A scanner may flag it.
- **localhost URLs in logs.** `http://localhost:8765` and `http://127.0.0.1:8766` appear in historical logs and specs. These are local dev servers, not external destinations.
- **Shell hooks.** `scripts/install-owl.sh` writes project `.claude/settings.json` with SessionStart and Stop hooks that run shell commands. The plugin does not include `hooks/`, so it does not install these. They are a manual step (README Step 2b).

## Content the plugin ships

The plugin source is the repo root, so an install copies everything tracked. That includes:

- `docs/requests.md` (894 lines of the author's verbatim requests) and `docs/decisions.md` (1060 lines)
- `docs/progress-archive.txt`, `docs/audit/*`, `docs/specs/*` (historical feature specs)
- `usecase-comparison/**`, including two `transcript-run*.jsonl` files in `usecase-comparison/hard-exit-experiment/ralph-run/.claude/`
- `publishing/*` drafts and two LinkedIn PDFs
- `CHANGELOG.md`, `CODEOWNERS`, `SECURITY.md`

Owner decision: keep these in the listing, or move internal logs out of the repo before submitting. Nothing was moved or deleted in this change.

## Not verified

- Whether the directory's safety scan and policy review pass. `claude plugin validate` does not run them (its output says so).
- Whether the installed plugin, copied from the marketplace, loads `agents/owl-of-athena.md` as expected. Validation confirms the file loads. It does not confirm runtime behavior.
