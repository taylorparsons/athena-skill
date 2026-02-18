# Decisions (append-only)

## D-20260211-0940
Date: 2026-02-11 09:40
Inputs: CR-20260211-0939
PRD: Scope boundary for public repo artifacts

Decision:
Replace imported project-oriented docs with a clean, repo-scoped RALPH artifact set while preserving required traceability files (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`).

Rationale:
The user requested a public sharing repo that demonstrates RALPH itself, not historical artifacts from another project.

Alternatives considered:
- Keep imported artifacts as examples (rejected: scope leakage and noise in public share).
- Remove docs artifacts entirely (rejected: conflicts with explicit request to include RALPH docs artifacts).

Acceptance / test:
- `docs/` contains only this repo's RALPH artifacts.
- Imported report/spec files from other projects are removed.
- `git status` no longer includes generated local artifacts after ignore rules are added.

## D-20260211-1005
Date: 2026-02-11 10:05
Inputs: CR-20260211-1004
PRD: Public share positioning and skill scope

Decision:
Remove Daisy companion-skill references from the public RALPH repo content (`README.md`, `AVAILABLE_SKILLS.md`) and keep this shared version scoped strictly to RALPH.

Rationale:
The user explicitly requested that this version of RALPH no longer include Daisy.

Alternatives considered:
- Keep Daisy as optional companion text in docs (rejected: conflicts with explicit request).

Acceptance / test:
- `README.md` and `AVAILABLE_SKILLS.md` contain no Daisy companion-skill references.
- README/skills listing describe only RALPH for this public version.

## D-20260211-1012
Date: 2026-02-11 10:12
Inputs: CR-20260211-1010
PRD: Public release hardening and repository history policy

Decision:
Perform a public-release hardening pass by adding `.gitignore` security patterns, adding `SECURITY.md`, adding MIT `LICENSE`, removing local absolute path strings from tracked docs, and rewriting git history to a single clean public baseline commit.

Rationale:
The user explicitly requested a truly clean public repo and asked for these hardening artifacts.

Alternatives considered:
- Keep existing multi-commit history with prior imported content (rejected: not truly clean).
- Keep raw local path strings for strict verbatim logs (rejected: conflicts with public-sharing hygiene request).

Acceptance / test:
- No local absolute path strings remain in tracked files.
- `.gitignore` includes `.env`, `__pycache__/`, and `*.pyc`.
- `SECURITY.md` and `LICENSE` exist.
- Repository history is rewritten to a clean public baseline.

## D-20260211-1020
Date: 2026-02-11 10:20
Inputs: CR-20260211-1019
PRD: Low-priority hardening controls for public repository governance

Decision:
Complete the low-priority hardening findings by adding a single-owner `CODEOWNERS`, adding `.github/dependabot.yml`, adding `.github/workflows/security.yml`, and enabling repo-level `commit.gpgsign`.

Rationale:
The user explicitly approved finishing the low-priority hardening items and confirmed there is one code owner.

Alternatives considered:
- Skip low-priority items before publish (rejected: user explicitly requested completion).
- Use multiple owners in `CODEOWNERS` (rejected: conflicts with single-owner direction).

Acceptance / test:
- Security audit no longer reports missing `CODEOWNERS`, Dependabot config, workflow, or GPG signing configuration.

## D-20260211-1326
Date: 2026-02-11 13:26
Inputs: CR-20260211-1325
PRD: Resume execution handling and onboarding example backlog

Decision:
Interpret the resume command as instruction to continue from the existing `docs/progress.txt` NEXT backlog item and implement an onboarding walkthrough under `docs/examples/` as a new traceable feature.

Rationale:
No local artifact matched the provided resume UUID, and the safest deterministic continuation path is the explicit pending task already recorded in repo state.

Alternatives considered:
- Pause and ask for an external session export keyed to the UUID (rejected: unnecessary because a concrete pending task was already queued locally).
- Resume by selecting an arbitrary new task (rejected: breaks ordered execution from tracked backlog).

Acceptance / test:
- A new feature spec/task pair exists for the walkthrough deliverable.
- `docs/examples/` includes one end-to-end CR -> D -> FR -> T walkthrough.
- `docs/progress.txt` marks the walkthrough task as done with validation notes.

## D-20260211-1400
Date: 2026-02-11 14:00
Inputs: CR-20260211-1358
PRD: Skill install packaging and single-skill install guardrails

Decision:
Keep this share repo's install contract focused on one installable skill target (`skills/ralph`) and remove the `skills/ralph-codex` packaged install target from the repo.

Rationale:
The user explicitly asked to keep install guidance and available skills scoped to `ralph` only and requested a checked-in update.

Alternatives considered:
- Keep `skills/ralph-codex` as an optional install target (rejected: conflicts with explicit scope request).
- Revert to root installs with `--path .` (rejected: installs entire repo and caused prior confusion).

Acceptance / test:
- `AVAILABLE_SKILLS.md` lists only `ralph`.
- `README.md` install section lists only `ralph` installation command.
- `scripts/validate_install_targets.py` validates only `skills/ralph`.
- `skills/ralph-codex/` does not exist.

## D-20260212-1647
Date: 2026-02-12 16:47
Inputs: CR-20260212-1646
PRD: Product/skill naming and repository identity

Decision:
Treat `athena` as the canonical replacement name for this repository and skill references, and treat `athen` in request item 1 as a typo.

Rationale:
The same request explicitly uses `athena` in items 2 and 3 and asks for all code/documentation references to be updated to that name.

Alternatives considered:
- Preserve `athen` literally for skill name while using `athena` elsewhere (rejected: inconsistent naming and conflicts with item 3 global replacement intent).
- Pause execution to ask for clarification (rejected: request is actionable and interpretation is low risk).

Acceptance / test:
- Repository/docs/code references are updated from `ralph` to `athena` where this repo defines its own naming.
- Project identity references use `athena-skill`.

## D-20260212-1648
Date: 2026-02-12 16:48
Inputs: CR-20260212-1646
PRD: Rename execution scope and audit-log immutability

Decision:
Apply rename changes across mutable repository code/docs/configuration, including path renames (`skills/ralph` -> `skills/athena`, `core/ralph-framework.md` -> `core/athena-framework.md`), and preserve append-only historical logs in `docs/requests.md` and `docs/decisions.md` as factual records.

Rationale:
The request requires broad replacement to `athena`, while RALPH audit rules require historical request/decision entries to stay append-only and customer-verbatim.

Alternatives considered:
- Edit historical request/decision entries to fully eliminate legacy naming (rejected: breaks append-only/verbatim audit contract).
- Limit rename only to README and skill metadata (rejected: does not satisfy global code/documentation update intent).

Acceptance / test:
- Mutable files reference `athena`/`ATHENA` and project name `athena-skill`.
- Any remaining `ralph` references are limited to append-only historical entries or backward-compatibility notes explicitly documented.

## D-20260213-0913
Date: 2026-02-13 09:13
Inputs: CR-20260213-0912
PRD: Publishing collateral for onboarding and installation

Decision:
Interpret "two more versions" as two new LinkedIn-ready post drafts under `publishing/`, each covering the ATHENA request-to-checkin loop and including explicit install instructions for both Codex and Claude with copy/paste blocks.

Rationale:
The request explicitly asks for two versions and asks for logical flow plus clear install instructions in LinkedIn-compatible format.

Alternatives considered:
- Update only one existing file (`publishing/launch-checklist.md`) (rejected: does not satisfy "two more versions").
- Put content only in README (rejected: request is for post-ready content, not repository setup docs).

Acceptance / test:
- Two new files exist in `publishing/` with distinct post drafts.
- Each draft includes: ATHENA flow from invocation to check-in, Codex install instructions, Claude install instructions, and copy/paste code blocks.

## D-20260213-1959
Date: 2026-02-13 19:59
Inputs: CR-20260213-1958
PRD: Publishing tone/style requirements for additional personal-style variant

Decision:
Create one additional LinkedIn-ready draft that preserves ATHENA invoke-to-checkin flow and installation sections while adopting the provided personal style traits: direct language, framework structure, grounded reflection, operator evidence orientation, and low-marketing tone.

Rationale:
The request explicitly asks for one more version in the user's personal writing style and provides concrete style guardrails.

Alternatives considered:
- Reuse an existing version with minor wording tweaks (rejected: does not meaningfully reflect the provided style profile).
- Write a purely personal narrative with no setup blocks (rejected: inconsistent with prior request context requiring install clarity and flow).

Acceptance / test:
- A new `publishing/` draft exists and is distinct from v1/v2.
- Draft includes direct, structured sections (problem/constraint/decision/evidence style), ATHENA loop narrative, and Codex/Claude copy/paste setup blocks.

## D-20260213-1437
Date: 2026-02-13 14:35
Inputs: CR-20260213-1434, CR-20260213-1435
PRD: README onboarding visual placement and asset source constraint

Decision:
Add a new tracked visual asset at `docs/images/athena-readme-fast-visual.svg` and place it at the top of `README.md`, while explicitly not using `docs/athena-napkin-loop.svg`.

Rationale:
The user requested a top README visual from the provided image and explicitly excluded the existing untracked SVG path.

Alternatives considered:
- Use `docs/athena-napkin-loop.svg` directly (rejected: explicitly disallowed by user).
- Keep README text-only (rejected: conflicts with fast-visual request).

Acceptance / test:
- `README.md` references `docs/images/athena-readme-fast-visual.svg`.
- `README.md` does not reference `docs/athena-napkin-loop.svg`.

## D-20260213-1438
Date: 2026-02-13 14:36
Inputs: CR-20260213-1436
PRD: README voice and documentation tone

Decision:
Rewrite `README.md` in Taylor-style voice using direct, structured sections (context, tension, decision, execution, outcome, reflection) while preserving existing install and validation facts.

Rationale:
The user explicitly asked for Taylor-style voice in README text, and the style skill defines concrete wording and structure constraints.

Alternatives considered:
- Keep current README wording with only the image insertion (rejected: does not satisfy explicit style request).
- Apply heavy marketing framing to emphasize launch messaging (rejected: conflicts with provided style profile).

Acceptance / test:
- README headings and prose are direct, concrete, and structured.
- Install commands and repository facts remain intact and executable.

## D-20260213-1448
Date: 2026-02-13 14:48
Inputs: CR-20260213-1448
PRD: README update scope correction

Decision:
Narrow the README change to image-only: keep the new top visual and restore normal README prose structure by removing literal style labels such as `context:`/`decision:`/`execution:`.

Rationale:
The user explicitly corrected the prior wording and asked to leave only the new image change.

Alternatives considered:
- Keep the Taylor-style labeled sections (rejected: conflicts with explicit user correction).
- Remove both image and style edits (rejected: conflicts with "just add the image").

Acceptance / test:
- `README.md` retains `docs/images/athena-readme-fast-visual.svg` at the top.
- `README.md` does not contain literal labels like `context:` `tension:` `decision:` `execution:` `outcome:` `reflection:`.

## D-20260213-1453
Date: 2026-02-13 14:52
Inputs: CR-20260213-1452
PRD: Check-in and remote merge execution policy

Decision:
Interpret "checkin a marge to remote" as a request to commit current intended ATHENA changes, merge with `origin/main`, and push to the remote repository. Stage only the intended README/docs/image changes and leave unrelated local modifications untouched.

Rationale:
The request explicitly asks for check-in and remote merge, and the working tree contains unrelated modified files that should not be included without explicit user direction.

Alternatives considered:
- Stage all modified files with `git add -A` (rejected: would include unrelated local changes).
- Defer push and only make a local commit (rejected: conflicts with explicit remote merge request).

Acceptance / test:
- Local commit exists containing only intended README/docs/image updates.
- Local `main` is merged with `origin/main` and pushed successfully.

## D-20260216-1318
Date: 2026-02-16 13:18
Inputs: CR-20260216-1317
PRD: Review remediation for findings 1-5

Decision:
Interpret `on on 1-5` as approval to implement all five findings from the prior review in one scoped remediation feature.

Rationale:
The immediate prior message presented findings numbered 1 through 5 and asked whether to fix them; the user response references that exact set.

Alternatives considered:
- Ask for clarification before editing (rejected: likely unnecessary delay with clear local context).
- Implement only finding #1 first (rejected: user referenced the full 1-5 set).

Acceptance / test:
- Findings 1-5 are remediated in code/docs and captured in PRD/spec/tasks/progress artifacts.

## D-20260217-0847
Date: 2026-02-17 08:47
Inputs: CR-20260217-0846
PRD: ATHENA skill visual asset packaging

Decision:
Create a new SVG icon asset at `skills/athena/assets/athena-warrior-icon.svg` to represent a warrior motif for the ATHENA skill package.

Rationale:
The request is specifically for an SVG skill icon invoking a warrior concept. Adding the asset under the installable skill path keeps it packaged with the `athena` skill.

Alternatives considered:
- Store the icon only under `docs/images/` (rejected: not part of the installable skill path).
- Add raster image instead of SVG (rejected: request explicitly asks for SVG).

Acceptance / test:
- `skills/athena/assets/athena-warrior-icon.svg` exists and renders as a valid SVG icon.
- ATHENA docs reflect the new request/decision/spec/task/progress trail for this change.

## D-20260217-1419
Date: 2026-02-17 14:19
Inputs: CR-20260217-1417
PRD: ATHENA install metadata for warrior icon asset

Decision:
Add explicit icon metadata in `skills/athena/agents/openai.yaml` (`icon_small` and `icon_large` -> `./assets/athena-warrior-icon.svg`) and extend install-target validation to require the icon asset and those metadata bindings.

Rationale:
The request specifically targets the `.codex` ATHENA install to include the warrior icon asset path. Declaring icon fields in installable skill metadata and enforcing them in validation provides deterministic packaging behavior.

Alternatives considered:
- Keep only the asset file without metadata bindings (rejected: install UI/config would not explicitly reference the icon).
- Update only local `~/.codex/skills/athena` without repo guardrails (rejected: not durable for future installs).

Acceptance / test:
- `skills/athena/agents/openai.yaml` contains `icon_small` and `icon_large` set to `./assets/athena-warrior-icon.svg`.
- `scripts/validate_install_targets.py` fails if required install asset/metadata bindings are missing and passes in current repo state.

## D-20260217-1452
Date: 2026-02-17 14:52
Inputs: CR-20260217-1451
PRD: Absolute-path hygiene follow-up remediation

Decision:
Patch tracked docs that still include local absolute-path tokens and verify resolution by rerunning the repository security audit.

Rationale:
The user requested absolute-path remediation, and the current audit reports a `HIGH` finding limited to two documentation lines.

Alternatives considered:
- Suppress the audit rule instead of fixing docs (rejected: hides a hygiene issue instead of resolving it).
- Leave legacy user-home absolute path examples in completed artifacts (rejected: continues to trigger `HIGH` findings).

Acceptance / test:
- `rg -n 'user-home absolute path' docs/` returns only policy wording and no literal local home-directory path tokens.
- `audit_repository_security.py` no longer reports a `HIGH` absolute-path finding.

## D-20260217-1536
Date: 2026-02-17 15:36
Inputs: CR-20260217-1535
PRD: ATHENA hardening documentation planning

Decision:
Treat this request as a documentation/planning feature in the ATHENA repository: define traceable requirements/tasks for the four hardening items and generate an `aipm-agentic-workflow` JSON artifact, without implementing script/code behavior changes in this session.

Rationale:
The user asked to create documents and explicitly clarified the target repository path for documentation placement.

Alternatives considered:
- Implement all four hardening changes immediately (rejected: request is to create docs; implementation should run as follow-up tasks).

Acceptance / test:
- `docs/specs/20260217-athena-hardening-plan/spec.md` and `docs/specs/20260217-athena-hardening-plan/tasks.md` exist with traceability links.
- `artifacts/agentic_workflow/20260217-1535-athena-hardening-plan.json` exists with `task_graph`, `agents`, and `interventions`.

## D-20260217-1551
Date: 2026-02-17 15:51
Inputs: CR-20260217-1550
PRD: ATHENA hardening execution

Decision:
Execute all remaining implementation tasks for `20260217-athena-hardening-plan` (`T-002` through `T-005`) in this session and reconcile PRD/spec/tasks/progress to a shipped state.

Rationale:
The user explicitly requested completion of all remaining work after the planning-only phase.

Alternatives considered:
- Implement only one task this session and defer others (rejected: conflicts with explicit "complete all of the work").

Acceptance / test:
- Traceability linter exists and validates `Sources`, `Verifies`, `Implements` references.
- ATHENA guidance contains one canonical merge/check-in checklist section.
- Commit helper defaults to path-scoped staging unless explicitly overridden.
- `docs/progress.txt` schema validation is implemented and integrated with resume prompt flow.
