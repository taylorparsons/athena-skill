# Session Notes: 20260705-token-diet (append-only)

## S-20260705-2041
Agent: Claude Code
Model: claude-fable-5
Skills: athena, superpowers:brainstorming
Goal: Cut ATHENA per-session token cost ~85% via script-gated KB

- Commands run: python3 -m unittest discover -s scripts/tests -> 20/20 pass; node --test site/site.test.mjs -> pass; ./scripts/owl migrate -> 4 blocks to notes.md, 5 to docs/audit/progress-legacy.txt
- Decisions: D-20260705-2025, D-20260705-2026, D-20260705-2027, D-20260705-2028
- Deletions: docs/progress.txt (migrated via owl migrate), templates/progress.txt + skills/athena/templates/progress.txt (template retired per FR-011)
- External config updated: ~/.codex/AGENTS.md reduced to 8-line trigger+gates block
- Risks / open questions: site/ dir remains untracked (belongs to 20260603-athena-site-app feature); local main is 1 commit ahead of origin — push not requested

## S-20260705-2044
Skills: athena

- Commit: bca8599 (T-010 implementation). Release commit follows as T-011.
- Reinstalled package to ~/.claude/skills/athena and ~/.codex/skills/athena via rsync --delete (sweep-projects.py preserved in installs).
- Legacy install extras removed by reinstall: install-owl.sh, migrate-all-projects.py, validate_install_targets.py, core/ (claude), stale Codex word-swap SKILL.md (codex).

## S-20260705-2153
Skills: athena

- A/B experiment (CR-20260705-2139): identical feature request ("--quiet flag for validate_progress_log.py") run by two fresh agents on clones of this repo — control at 67b43bb (v2.0 layout) vs HEAD (v2.1 layout).
- Tokens: v2.0 = 161,349; v2.1 = 59,942 (63% reduction end-to-end). Duration: 740s vs 476s (36% faster). Tool uses: 47 vs 40.
- Files read: v2.0 = 18 incl. full requests.md/decisions.md/PRD.md/progress.txt/athena-index.md + owl.py spelunking; v2.1 = 7, zero log reads, PRD read by section via grep/sed.
- Outcome equivalence: both produced verbatim CR, D entries, PRD FR + shipped line, spec/tasks with valid traceability links, session evidence with commit hashes, 2 traceable commits, clean tree, nothing pushed. v2.1 evidence in notes.md; v2.0 in progress.txt/progress-archive.txt.
- Bonus: control agent independently found the v2.0 owl archive progress-rewrite data-loss bug (its D-20260705-2156) and had to work around it; the v2.1 layout removes that failure class with progress.txt.
- Scratch repos: scratchpad/athena-v20 and athena-v21 (session-temporary).

## S-20260705-2253
Skills: athena

- Codex A/B experiment (CR-20260705-2205): same request, cold gpt-5.5 codex exec runs, clones athena-v20-codex (67b43bb) vs athena-v21-codex (HEAD).
- Tokens (Codex-reported): v2.0 = 225,195; v2.1 = 194,730 -> 13.5% reduction; absolute delta 30,465 ~= the doc-stack overhead the redesign removes (~28-30K).
- v2.1 compliance on Codex: zero direct reads of requests.md/decisions.md/athena-index.md (transcript-verified); owl used for context/add-request/add-decision/add-note x4/why/retrieve/archive/write-memory; full PRD cat'd (allowed but loose - PRD pruning backlog item).
- v2.0 control read the full stack (index, requests, decisions, TRACEABILITY, PRD, progress) plus owl.py spelunking.
- Outcome equivalence: both Codex arms produced valid trails, 2 traceable commits each, working --quiet flag (success suppressed, errors still print, correct exit codes).
- Caveat: control session was mildly contaminated by the new ~/.codex/AGENTS.md (tried `owl context`, failed on old owl.py, then followed old SKILL.md full reads) - bias small and toward the control.
- Cross-model note: Claude delta was 63% because subagent accounting re-carries context per turn; Codex accounting surfaces the overhead ~once. Same mechanism, different amplification.
