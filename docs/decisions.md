# Decisions (append-only)

## D-20260603-1300

### Metadata
- **Date:** 2026-06-03 13:00
- **Inputs:** CR-20260603-1258
- **PRD:** ATHENA site follow-on redesign

### Decision:
Treat the existing static `site/` prototype as a completed baseline and define a follow-on design for a richer app-style ATHENA site: a launch-page hero plus deeper docs-oriented sections in a real frontend app structure, with hybrid first-screen framing and strong framework-launch tone.

### Rationale:
The repository already contains an untracked static prototype and a completed June 2 feature spec for a simple explanatory site. The current request is broader and should be framed as a redesign/expansion rather than overwriting the original intent.

### Alternatives considered:
- Reuse the static single-page site as-is (rejected: does not match the newly requested app-style structure and deeper docs scope).
- Skip design and implement immediately (rejected: conflicts with the active brainstorming workflow and increases rework risk).

### Acceptance / test:
- A new design doc exists under `docs/superpowers/specs/` for the richer ATHENA site.
- The follow-on ATHENA feature spec/tasks capture the redesign scope.
- The next step is explicit user review of the written design before implementation planning.

---

## D-20260602-2026

### Metadata
- **Date:** 2026-06-02 20:26
- **Inputs:** CR-20260602-2025
- **PRD:** ATHENA explanatory site

### Decision:
Create a static site under `site/` with no package-manager dependency, serve it locally with Python's built-in HTTP server, and use a bold product-launch visual direction that explains ATHENA's request-to-shipped-code loop before presenting install paths.

### Rationale:
The user wants to see the site immediately. A static site keeps the implementation lightweight for this repository, avoids adding a frontend toolchain, and can be published locally from the workspace with one command.

### Alternatives considered:
- Add a Vite/React app (rejected: unnecessary dependency and setup for a single explanatory page).
- Only update `README.md` (rejected: user asked to see a site).
- Make the page primarily install-focused (rejected: user chose explanation first, then install).

### Acceptance / test:
- `site/index.html`, `site/styles.css`, and `site/app.js` exist.
- The page explains ATHENA in plain language and shows the CR -> D -> PRD -> Spec -> Task -> Validation loop.
- The page includes Codex and Claude installation paths.
- A local HTTP server can serve the site and the browser can render it.

---

## D-20260602-1457

### Metadata
- **Date:** 2026-06-02 14:57
- **Inputs:** CR-20260602-1456
- **PRD:** Local repository sync with origin/main

### Decision:
Use `git pull --ff-only origin main` for this sync task after recording ATHENA traceability, so the local `main` branch advances only if the remote commits can be applied without creating a merge commit.

### Rationale:
The user asked to pull the two fetched remote commits into the current checkout. A fast-forward-only pull preserves the linear branch history already present in this repository and avoids introducing a local merge commit for a simple remote sync.

### Alternatives considered:
- `git pull origin main` with default merge behavior (rejected: could create an unnecessary merge commit).
- `git merge origin/main` after fetch (rejected: equivalent outcome with less explicit fast-forward protection).

### Acceptance / test:
- `git pull --ff-only origin main` succeeds.
- `git status --short --branch` no longer reports `behind`.
- `git log --oneline --decorate -n 3` includes the fetched remote tip on local `main`.

---

## D-20260416-1659

### Metadata
- **Date:** 2026-04-16 16:59
- **Inputs:** CR-20260416-1656
- **PRD:** Versioning and release publication summary

### Decision:
Supersede the earlier release-baseline assumption and treat the published GitHub release baseline as `v2.0.0`, not `v1.2.0`. Keep the requested `v2.0.0.1` version bump, but rewrite the release notes as a patch-level follow-up to the already-published `v2.0.0` release.

### Rationale:
The user provided the current GitHub release page content showing `v2.0.0: Owl of Athena, Fleet Management & Token Optimization` as the existing published release. That means `v2.0.0.1` should summarize only the follow-up changes after that release rather than repeating the entire `v2.0.0` feature set.

### Alternatives considered:
- Keep the cumulative `v1.2.0`-based notes (rejected: incorrect published baseline).
- Revert to `v2.0.0` and overwrite the existing release notes (rejected: conflicts with the explicit request to bump to `v2.0.0.1`).

### Acceptance / test:
- `CHANGELOG.md` `v2.0.0.1` entry is written as a patch release on top of published `v2.0.0`.
- ATHENA release spec and progress notes reference `v2.0.0` as the published baseline.

---

## D-20260416-1657

### Metadata
- **Date:** 2026-04-16 16:57
- **Inputs:** CR-20260416-1656
- **PRD:** Versioning and release publication summary

### Decision:
Treat `v2.0.0.1` as the next release tag for the current repository state without rewriting the existing local `v2.0.0` tag. Write the new `CHANGELOG.md` top entry as cumulative release notes intended for GitHub publication because the latest published release page still shows `v1.2.0` on 2026-04-16.

### Rationale:
The repository already has a local `v2.0.0` tag, but the GitHub releases page referenced by the user still presents `v1.2.0` as the latest published release. A patch-level `v2.0.0.1` tag preserves local history while providing one clean published summary that covers the post-`v1.2.0` changes now ready to ship.

### Alternatives considered:
- Reuse or move the existing `v2.0.0` tag (rejected: rewrites tag history and risks ambiguity).
- Write notes only for the delta from local `v2.0.0` (rejected: does not match the currently published release baseline on GitHub).

### Acceptance / test:
- `VERSION` reads `2.0.0.1`.
- `CHANGELOG.md` has a `v2.0.0.1` entry with `Summary` and `What's Changed` suitable for GitHub release publication.
- Local git tag `v2.0.0.1` exists after the release commit.

---

## D-20260416-1447

### Metadata
- **Date:** 2026-04-16 14:47
- **Inputs:** CR-20260416-1446
- **PRD:** README installation guidance clarity

### Decision:
Clarify the root `README.md` installation section by splitting the install flow into environment-first quick starts for Codex and Claude Code. Keep the current install mechanisms unchanged, explicitly say Codex only needs the ATHENA skill install, and label Owl setup as Claude Code only.

### Rationale:
The current README technically contains both installs, but the flow interleaves shared narrative with Claude-only Owl setup. That makes the correct path harder to scan, especially for Codex users who should stop after the packaged skill install.

### Alternatives considered:
- Rewrite broader Owl and bootstrap sections throughout the README (rejected: unnecessary scope for the request).
- Change install scripts or Claude hook behavior alongside the docs update (rejected: the request is for clearer instructions, not runtime changes).

### Acceptance / test:
- README Installation section contains a clear Codex quick start and a clear Claude Code quick start.
- README explicitly states that Owl setup is Claude Code only and can be skipped for Codex.
- No install scripts or Claude files change as part of this feature.

---

## D-20260416-1425

### Metadata
- **Date:** 2026-04-16 14:25
- **Inputs:** CR-20260416-1424
- **PRD:** Packaged skill cross-agent compatibility

### Decision:
Update only the packaged ATHENA surface under `skills/athena/` to carry Codex-compatible Owl dispatch guidance, while leaving `.claude/*`, root README/agent docs, and Claude install or migration scripts unchanged. Merge the working local packaged changes into the source package without regressing the existing Claude memory-bridge guidance or the packaged Owl agent metadata copied into `.claude/agents/`.

### Rationale:
The local packaged install proved the Codex-facing wording gap, but the source repository's packaged skill is also consumed by Claude installs and migration tooling. A direct overwrite from the local copy would remove Claude memory-first instructions from `skills/athena/SKILL.md` and would change the packaged Owl agent model metadata that migration scripts copy into `.claude/agents/`.

### Alternatives considered:
- Copy the local packaged files wholesale (rejected: would regress Claude-oriented memory/write-memory guidance in the source package).
- Expand the change into `.claude/*`, README, install scripts, and migration scripts (rejected: unnecessary risk for this request).

### Acceptance / test:
- `skills/athena/SKILL.md` includes Codex Owl dispatch guidance without removing the existing Claude memory-bridge flow.
- `skills/athena/agents/owl-of-athena.md` uses cross-agent wording without changing the packaged model metadata.
- No `.claude/*`, root README, root agent docs, or install/migration scripts are modified in this pass.

---

## D-20260414-1100

### Metadata
- **Date:** 2026-04-14 11:00
- **Inputs:** CR-20260414-1100
- **PRD:** Rename INDEX.md to athena-index.md

### Decision:
Rename `docs/INDEX.md` to `docs/athena-index.md` (kebab-case) across all functional code, hooks, and documentation. Leave append-only logs (`requests.md`, `decisions.md`, `progress-archive.txt`) untouched. Leave `settings.json` hook commands unchanged (they call `./scripts/owl` by command name, not filename). Update `docs/progress.txt` (mutable active state) but not `docs/progress-archive.txt` (historical record). Add single-prompt fast path to README above the 5-step manual bootstrap.

### Rationale:
`INDEX.md` is a generic name that collides with existing documentation indexes in mature repos (confirmed collision in `agentic-browser`). `athena-index.md` is unambiguous, safe to install globally, and follows kebab-case conventions. No migration script needed — feature was never released publicly; only two projects had `docs/INDEX.md` (this repo and `my_LLC`, being reverted).

### Alternatives considered:
- `ATHENA_INDEX.md` (rejected: uppercase snake_case inconsistent with other filenames)
- `athena_index.md` (rejected: snake_case inconsistent with markdown file conventions)
- Auto-migrate old `INDEX.md` on first run (rejected: not needed, no public installs exist)

### Acceptance / test:
- `./scripts/owl update-index` creates `docs/athena-index.md`, not `docs/INDEX.md`
- `pre-commit` validates `docs/athena-index.md` sync
- `post-commit` stages `docs/athena-index.md` on feature completion
- No functional references to `docs/INDEX.md` remain in code or hooks

---

## D-20260413-1201

### Metadata
- **Date:** 2026-04-13 12:01
- **Inputs:** CR-20260413-1200
- **PRD:** Token optimization architecture

### Decision:
Use INDEX.md-based approach with Git hooks and Owl agent for archive management. Keep all features in docs/specs/ (no moving files). INDEX.md marks active vs archived. Owl agent (Python script) handles maintenance. Git hooks automate INDEX.md updates. Add progress.txt archival to reduce bloat.

**Rationale:**
- INDEX.md: Cross-platform, no symlinks, preserves all Git references
- Owl agent: Cheap model (Haiku) for archive ops, 99% cost savings
- Git hooks: Automatic enforcement, reduces manual errors
- progress.txt trim: Removes 1,000+ tokens of old session data
- Combined: ~9,500 tokens saved per session (88% reduction)

**Alternatives considered:**
- Move archives outside docs/: Breaks Git references
- Symlinks: Not cross-platform compatible
- No automation: Too much manual maintenance

## D-20260211-0940

### Metadata
- **Date:** 2026-02-11 09:40
- **Inputs:** CR-20260211-0939
- **PRD:** Scope boundary for public repo artifacts

### Decision:
Replace imported project-oriented docs with a clean, repo-scoped RALPH artifact set while preserving required traceability files (`requests`, `decisions`, `PRD`, `specs`, `progress`, `TRACEABILITY`).

### Rationale:
The user requested a public sharing repo that demonstrates RALPH itself, not historical artifacts from another project.

### Alternatives considered:
- Keep imported artifacts as examples (rejected: scope leakage and noise in public share).
- Remove docs artifacts entirely (rejected: conflicts with explicit request to include RALPH docs artifacts).

### Acceptance / test:
- `docs/` contains only this repo's RALPH artifacts.
- Imported report/spec files from other projects are removed.
- `git status` no longer includes generated local artifacts after ignore rules are added.

## D-20260211-1005

### Metadata
- **Date:** 2026-02-11 10:05
- **Inputs:** CR-20260211-1004
- **PRD:** Public share positioning and skill scope

### Decision:
Remove Daisy companion-skill references from the public RALPH repo content (`README.md`, `AVAILABLE_SKILLS.md`) and keep this shared version scoped strictly to RALPH.

### Rationale:
The user explicitly requested that this version of RALPH no longer include Daisy.

### Alternatives considered:
- Keep Daisy as optional companion text in docs (rejected: conflicts with explicit request).

### Acceptance / test:
- `README.md` and `AVAILABLE_SKILLS.md` contain no Daisy companion-skill references.
- README/skills listing describe only RALPH for this public version.

## D-20260211-1012

### Metadata
- **Date:** 2026-02-11 10:12
- **Inputs:** CR-20260211-1010
- **PRD:** Public release hardening and repository history policy

### Decision:
Perform a public-release hardening pass by adding `.gitignore` security patterns, adding `SECURITY.md`, adding MIT `LICENSE`, removing local absolute path strings from tracked docs, and rewriting git history to a single clean public baseline commit.

### Rationale:
The user explicitly requested a truly clean public repo and asked for these hardening artifacts.

### Alternatives considered:
- Keep existing multi-commit history with prior imported content (rejected: not truly clean).
- Keep raw local path strings for strict verbatim logs (rejected: conflicts with public-sharing hygiene request).

### Acceptance / test:
- No local absolute path strings remain in tracked files.
- `.gitignore` includes `.env`, `__pycache__/`, and `*.pyc`.
- `SECURITY.md` and `LICENSE` exist.
- Repository history is rewritten to a clean public baseline.

## D-20260211-1020

### Metadata
- **Date:** 2026-02-11 10:20
- **Inputs:** CR-20260211-1019
- **PRD:** Low-priority hardening controls for public repository governance

### Decision:
Complete the low-priority hardening findings by adding a single-owner `CODEOWNERS`, adding `.github/dependabot.yml`, adding `.github/workflows/security.yml`, and enabling repo-level `commit.gpgsign`.

### Rationale:
The user explicitly approved finishing the low-priority hardening items and confirmed there is one code owner.

### Alternatives considered:
- Skip low-priority items before publish (rejected: user explicitly requested completion).
- Use multiple owners in `CODEOWNERS` (rejected: conflicts with single-owner direction).

### Acceptance / test:
- Security audit no longer reports missing `CODEOWNERS`, Dependabot config, workflow, or GPG signing configuration.

## D-20260211-1326

### Metadata
- **Date:** 2026-02-11 13:26
- **Inputs:** CR-20260211-1325
- **PRD:** Resume execution handling and onboarding example backlog

### Decision:
Interpret the resume command as instruction to continue from the existing `docs/progress.txt` NEXT backlog item and implement an onboarding walkthrough under `docs/examples/` as a new traceable feature.

### Rationale:
No local artifact matched the provided resume UUID, and the safest deterministic continuation path is the explicit pending task already recorded in repo state.

### Alternatives considered:
- Pause and ask for an external session export keyed to the UUID (rejected: unnecessary because a concrete pending task was already queued locally).
- Resume by selecting an arbitrary new task (rejected: breaks ordered execution from tracked backlog).

### Acceptance / test:
- A new feature spec/task pair exists for the walkthrough deliverable.
- `docs/examples/` includes one end-to-end CR -> D -> FR -> T walkthrough.
- `docs/progress.txt` marks the walkthrough task as done with validation notes.

## D-20260211-1400

### Metadata
- **Date:** 2026-02-11 14:00
- **Inputs:** CR-20260211-1358
- **PRD:** Skill install packaging and single-skill install guardrails

### Decision:
Keep this share repo's install contract focused on one installable skill target (`skills/ralph`) and remove the `skills/ralph-codex` packaged install target from the repo.

### Rationale:
The user explicitly asked to keep install guidance and available skills scoped to `ralph` only and requested a checked-in update.

### Alternatives considered:
- Keep `skills/ralph-codex` as an optional install target (rejected: conflicts with explicit scope request).
- Revert to root installs with `--path .` (rejected: installs entire repo and caused prior confusion).

### Acceptance / test:
- `AVAILABLE_SKILLS.md` lists only `ralph`.
- `README.md` install section lists only `ralph` installation command.
- `scripts/validate_install_targets.py` validates only `skills/ralph`.
- `skills/ralph-codex/` does not exist.

## D-20260212-1647

### Metadata
- **Date:** 2026-02-12 16:47
- **Inputs:** CR-20260212-1646
- **PRD:** Product/skill naming and repository identity

### Decision:
Treat `athena` as the canonical replacement name for this repository and skill references, and treat `athen` in request item 1 as a typo.

### Rationale:
The same request explicitly uses `athena` in items 2 and 3 and asks for all code/documentation references to be updated to that name.

### Alternatives considered:
- Preserve `athen` literally for skill name while using `athena` elsewhere (rejected: inconsistent naming and conflicts with item 3 global replacement intent).
- Pause execution to ask for clarification (rejected: request is actionable and interpretation is low risk).

### Acceptance / test:
- Repository/docs/code references are updated from `ralph` to `athena` where this repo defines its own naming.
- Project identity references use `athena-skill`.

## D-20260212-1648

### Metadata
- **Date:** 2026-02-12 16:48
- **Inputs:** CR-20260212-1646
- **PRD:** Rename execution scope and audit-log immutability

### Decision:
Apply rename changes across mutable repository code/docs/configuration, including path renames (`skills/ralph` -> `skills/athena`, `core/ralph-framework.md` -> `core/athena-framework.md`), and preserve append-only historical logs in `docs/requests.md` and `docs/decisions.md` as factual records.

### Rationale:
The request requires broad replacement to `athena`, while RALPH audit rules require historical request/decision entries to stay append-only and customer-verbatim.

### Alternatives considered:
- Edit historical request/decision entries to fully eliminate legacy naming (rejected: breaks append-only/verbatim audit contract).
- Limit rename only to README and skill metadata (rejected: does not satisfy global code/documentation update intent).

### Acceptance / test:
- Mutable files reference `athena`/`ATHENA` and project name `athena-skill`.
- Any remaining `ralph` references are limited to append-only historical entries or backward-compatibility notes explicitly documented.

## D-20260213-0913

### Metadata
- **Date:** 2026-02-13 09:13
- **Inputs:** CR-20260213-0912
- **PRD:** Publishing collateral for onboarding and installation

### Decision:
Interpret "two more versions" as two new LinkedIn-ready post drafts under `publishing/`, each covering the ATHENA request-to-checkin loop and including explicit install instructions for both Codex and Claude with copy/paste blocks.

### Rationale:
The request explicitly asks for two versions and asks for logical flow plus clear install instructions in LinkedIn-compatible format.

### Alternatives considered:
- Update only one existing file (`publishing/launch-checklist.md`) (rejected: does not satisfy "two more versions").
- Put content only in README (rejected: request is for post-ready content, not repository setup docs).

### Acceptance / test:
- Two new files exist in `publishing/` with distinct post drafts.
- Each draft includes: ATHENA flow from invocation to check-in, Codex install instructions, Claude install instructions, and copy/paste code blocks.

## D-20260213-1959

### Metadata
- **Date:** 2026-02-13 19:59
- **Inputs:** CR-20260213-1958
- **PRD:** Publishing tone/style requirements for additional personal-style variant

### Decision:
Create one additional LinkedIn-ready draft that preserves ATHENA invoke-to-checkin flow and installation sections while adopting the provided personal style traits: direct language, framework structure, grounded reflection, operator evidence orientation, and low-marketing tone.

### Rationale:
The request explicitly asks for one more version in the user's personal writing style and provides concrete style guardrails.

### Alternatives considered:
- Reuse an existing version with minor wording tweaks (rejected: does not meaningfully reflect the provided style profile).
- Write a purely personal narrative with no setup blocks (rejected: inconsistent with prior request context requiring install clarity and flow).

### Acceptance / test:
- A new `publishing/` draft exists and is distinct from v1/v2.
- Draft includes direct, structured sections (problem/constraint/decision/evidence style), ATHENA loop narrative, and Codex/Claude copy/paste setup blocks.

## D-20260213-1437

### Metadata
- **Date:** 2026-02-13 14:35
- **Inputs:** CR-20260213-1434, CR-20260213-1435
- **PRD:** README onboarding visual placement and asset source constraint

### Decision:
Add a new tracked visual asset at `docs/images/athena-readme-fast-visual.svg` and place it at the top of `README.md`, while explicitly not using `docs/athena-napkin-loop.svg`.

### Rationale:
The user requested a top README visual from the provided image and explicitly excluded the existing untracked SVG path.

### Alternatives considered:
- Use `docs/athena-napkin-loop.svg` directly (rejected: explicitly disallowed by user).
- Keep README text-only (rejected: conflicts with fast-visual request).

### Acceptance / test:
- `README.md` references `docs/images/athena-readme-fast-visual.svg`.
- `README.md` does not reference `docs/athena-napkin-loop.svg`.

## D-20260213-1438

### Metadata
- **Date:** 2026-02-13 14:36
- **Inputs:** CR-20260213-1436
- **PRD:** README voice and documentation tone

### Decision:
Rewrite `README.md` in Taylor-style voice using direct, structured sections (context, tension, decision, execution, outcome, reflection) while preserving existing install and validation facts.

### Rationale:
The user explicitly asked for Taylor-style voice in README text, and the style skill defines concrete wording and structure constraints.

### Alternatives considered:
- Keep current README wording with only the image insertion (rejected: does not satisfy explicit style request).
- Apply heavy marketing framing to emphasize launch messaging (rejected: conflicts with provided style profile).

### Acceptance / test:
- README headings and prose are direct, concrete, and structured.
- Install commands and repository facts remain intact and executable.

## D-20260213-1448

### Metadata
- **Date:** 2026-02-13 14:48
- **Inputs:** CR-20260213-1448
- **PRD:** README update scope correction

### Decision:
Narrow the README change to image-only: keep the new top visual and restore normal README prose structure by removing literal style labels such as `context:`/`decision:`/`execution:`.

### Rationale:
The user explicitly corrected the prior wording and asked to leave only the new image change.

### Alternatives considered:
- Keep the Taylor-style labeled sections (rejected: conflicts with explicit user correction).
- Remove both image and style edits (rejected: conflicts with "just add the image").

### Acceptance / test:
- `README.md` retains `docs/images/athena-readme-fast-visual.svg` at the top.
- `README.md` does not contain literal labels like `context:` `tension:` `decision:` `execution:` `outcome:` `reflection:`.

## D-20260213-1453

### Metadata
- **Date:** 2026-02-13 14:52
- **Inputs:** CR-20260213-1452
- **PRD:** Check-in and remote merge execution policy

### Decision:
Interpret "checkin a marge to remote" as a request to commit current intended ATHENA changes, merge with `origin/main`, and push to the remote repository. Stage only the intended README/docs/image changes and leave unrelated local modifications untouched.

### Rationale:
The request explicitly asks for check-in and remote merge, and the working tree contains unrelated modified files that should not be included without explicit user direction.

### Alternatives considered:
- Stage all modified files with `git add -A` (rejected: would include unrelated local changes).
- Defer push and only make a local commit (rejected: conflicts with explicit remote merge request).

### Acceptance / test:
- Local commit exists containing only intended README/docs/image updates.
- Local `main` is merged with `origin/main` and pushed successfully.

## D-20260216-1318

### Metadata
- **Date:** 2026-02-16 13:18
- **Inputs:** CR-20260216-1317
- **PRD:** Review remediation for findings 1-5

### Decision:
Interpret `on on 1-5` as approval to implement all five findings from the prior review in one scoped remediation feature.

### Rationale:
The immediate prior message presented findings numbered 1 through 5 and asked whether to fix them; the user response references that exact set.

### Alternatives considered:
- Ask for clarification before editing (rejected: likely unnecessary delay with clear local context).
- Implement only finding #1 first (rejected: user referenced the full 1-5 set).

### Acceptance / test:
- Findings 1-5 are remediated in code/docs and captured in PRD/spec/tasks/progress artifacts.

## D-20260217-0847

### Metadata
- **Date:** 2026-02-17 08:47
- **Inputs:** CR-20260217-0846
- **PRD:** ATHENA skill visual asset packaging

### Decision:
Create a new SVG icon asset at `skills/athena/assets/athena-warrior-icon.svg` to represent a warrior motif for the ATHENA skill package.

### Rationale:
The request is specifically for an SVG skill icon invoking a warrior concept. Adding the asset under the installable skill path keeps it packaged with the `athena` skill.

### Alternatives considered:
- Store the icon only under `docs/images/` (rejected: not part of the installable skill path).
- Add raster image instead of SVG (rejected: request explicitly asks for SVG).

### Acceptance / test:
- `skills/athena/assets/athena-warrior-icon.svg` exists and renders as a valid SVG icon.
- ATHENA docs reflect the new request/decision/spec/task/progress trail for this change.

## D-20260217-1419

### Metadata
- **Date:** 2026-02-17 14:19
- **Inputs:** CR-20260217-1417
- **PRD:** ATHENA install metadata for warrior icon asset

### Decision:
Add explicit icon metadata in `skills/athena/agents/openai.yaml` (`icon_small` and `icon_large` -> `./assets/athena-warrior-icon.svg`) and extend install-target validation to require the icon asset and those metadata bindings.

### Rationale:
The request specifically targets the `.codex` ATHENA install to include the warrior icon asset path. Declaring icon fields in installable skill metadata and enforcing them in validation provides deterministic packaging behavior.

### Alternatives considered:
- Keep only the asset file without metadata bindings (rejected: install UI/config would not explicitly reference the icon).
- Update only local `~/.codex/skills/athena` without repo guardrails (rejected: not durable for future installs).

### Acceptance / test:
- `skills/athena/agents/openai.yaml` contains `icon_small` and `icon_large` set to `./assets/athena-warrior-icon.svg`.
- `scripts/validate_install_targets.py` fails if required install asset/metadata bindings are missing and passes in current repo state.

## D-20260217-1452

### Metadata
- **Date:** 2026-02-17 14:52
- **Inputs:** CR-20260217-1451
- **PRD:** Absolute-path hygiene follow-up remediation

### Decision:
Patch tracked docs that still include local absolute-path tokens and verify resolution by rerunning the repository security audit.

### Rationale:
The user requested absolute-path remediation, and the current audit reports a `HIGH` finding limited to two documentation lines.

### Alternatives considered:
- Suppress the audit rule instead of fixing docs (rejected: hides a hygiene issue instead of resolving it).
- Leave legacy user-home absolute path examples in completed artifacts (rejected: continues to trigger `HIGH` findings).

### Acceptance / test:
- `rg -n 'user-home absolute path' docs/` returns only policy wording and no literal local home-directory path tokens.
- `audit_repository_security.py` no longer reports a `HIGH` absolute-path finding.

## D-20260217-1536

### Metadata
- **Date:** 2026-02-17 15:36
- **Inputs:** CR-20260217-1535
- **PRD:** ATHENA hardening documentation planning

### Decision:
Treat this request as a documentation/planning feature in the ATHENA repository: define traceable requirements/tasks for the four hardening items and generate an `aipm-agentic-workflow` JSON artifact, without implementing script/code behavior changes in this session.

### Rationale:
The user asked to create documents and explicitly clarified the target repository path for documentation placement.

### Alternatives considered:
- Implement all four hardening changes immediately (rejected: request is to create docs; implementation should run as follow-up tasks).

### Acceptance / test:
- `docs/specs/20260217-athena-hardening-plan/spec.md` and `docs/specs/20260217-athena-hardening-plan/tasks.md` exist with traceability links.
- `artifacts/agentic_workflow/20260217-1535-athena-hardening-plan.json` exists with `task_graph`, `agents`, and `interventions`.

## D-20260217-1551

### Metadata
- **Date:** 2026-02-17 15:51
- **Inputs:** CR-20260217-1550
- **PRD:** ATHENA hardening execution

### Decision:
Execute all remaining implementation tasks for `20260217-athena-hardening-plan` (`T-002` through `T-005`) in this session and reconcile PRD/spec/tasks/progress to a shipped state.

### Rationale:
The user explicitly requested completion of all remaining work after the planning-only phase.

### Alternatives considered:
- Implement only one task this session and defer others (rejected: conflicts with explicit "complete all of the work").

### Acceptance / test:
- Traceability linter exists and validates `Sources`, `Verifies`, `Implements` references.
- ATHENA guidance contains one canonical merge/check-in checklist section.
- Commit helper defaults to path-scoped staging unless explicitly overridden.
- `docs/progress.txt` schema validation is implemented and integrated with resume prompt flow.

## D-20260218-0903

### Metadata
- **Date:** 2026-02-18 09:03
- **Inputs:** CR-20260218-0902
- **PRD:** ATHENA release versioning

### Decision:
Implement the request as a repository version bump by updating `VERSION` from `1.0.1` to `1.1.0`, with ATHENA traceability docs for this change.

### Rationale:
The user requested only a version update; the minimal correct change is updating the canonical version file.

### Alternatives considered:
- Update additional release artifacts without request (rejected: unnecessary scope expansion).

### Acceptance / test:
- `VERSION` equals `1.1.0`.
- ATHENA spec/tasks/progress records show the version bump task completed.

## D-20260218-1100

### Metadata
- **Date:** 2026-02-18 11:00
- **Inputs:** CR-20260218-1059
- **PRD:** ATHENA traceable staging guardrails

### Decision:
Change `commit_with_traceability.py` default staging back to broad staging (`git add -A`) but enforce pre-stage guardrails that block `.DS_Store`, common temp/cache paths, likely secret patterns, and large artifacts before staging. Keep scoped alternatives via `--paths` and add `--docs-only` for legacy path-scoped behavior.

### Rationale:
The user wants broad staging behavior for clean working flow while preventing accidental inclusion of risky files.

### Alternatives considered:
- Keep path-scoped default and require `--all-changes` each time (rejected: does not restore desired user workflow).
- Restore broad staging with no checks (rejected: reintroduces accidental staging risk).

### Acceptance / test:
- Helper defaults to broad staging when no `--paths`/`--docs-only` is provided.
- Pre-stage checks fail with actionable errors when blocked patterns, secret markers, or large files are detected.
- `--docs-only` preserves the prior scoped ATHENA docs staging option.

## D-20260219-1643

### Metadata
- **Date:** 2026-02-19 16:43
- **Inputs:** CR-20260219-1638, CR-20260219-1639, CR-20260219-1640, CR-20260219-1641, CR-20260219-1642
- **PRD:** Docs readability formatting for root markdown and feature specs

### Decision:
Apply readability improvements only in `/Volumes/T9/code/SKILLS/athena/docs` moving forward, with ATHENA-managed traceability. Improve scanability by adding clearer heading hierarchy and bold metadata labels in root markdown docs and `docs/specs/*/spec.md`, while preserving existing requirement/task semantics.

### Rationale:
This directly satisfies the user scope correction and readability request without reverting unrelated prior edits outside this source repo.

### Alternatives considered:
- Roll back prior `.codex`-path edits first (rejected: user explicitly said to leave the wrong path as-is for now).
- Limit changes only to one root file (rejected: user requested root docs plus spec readability improvements).

### Acceptance / test:
- Root docs in `docs/*.md` show stronger heading structure and bold metadata labels.
- Spec files in `docs/specs/*/spec.md` use consistent bold metadata labels and readable section labels.
- ATHENA validation scripts pass after updates.

## D-20260219-1658

### Metadata
- **Date:** 2026-02-19 16:58
- **Inputs:** CR-20260219-1658
- **PRD:** PRD traceability readability

### Decision:
Link references in `docs/PRD.md` by ID type to concrete, navigable destinations: `CR-...` to `docs/requests.md` entries, `D-...` to `docs/decisions.md` entries, and `FR-ATHENA-...` / `NFR-ATHENA-...` to their own numbered lines in `docs/PRD.md`.

### Rationale:
The request is for easier human auditing and skimming. Mapping each numbered reference to a stable in-repo location provides direct navigation without changing requirement semantics.

### Alternatives considered:
- Link only `CR-...` and `D-...` IDs (rejected: incomplete user expectation for all numbered references).
- Link `FR-ATHENA...` and `NFR-ATHENA...` to a separate index only (rejected: less direct than section-line navigation in PRD).

### Acceptance / test:
- Every `CR-...`, `D-...`, `FR-ATHENA-...`, and `NFR-ATHENA-...` reference in `docs/PRD.md` is wrapped as a markdown link.
- Clicking each link opens the matching document and anchored location.

## D-20260219-1700

### Metadata
- **Date:** 2026-02-19 17:00
- **Inputs:** CR-20260219-1700
- **PRD:** PRD linkability correctness

### Decision:
Adjust PRD link targets from path-prefixed absolute-in-repo links (`docs/...`) to file-relative links (`./...`) so links render correctly from markdown pages and local file viewers where `docs/PRD.md` is in the `docs/` directory.

### Rationale:
The request reported 404s in a local docs server (`http://localhost:8765/docs/PRD.md`) because links with `docs/...` were resolving to `/docs/docs/...`.

### Alternatives considered:
- Keep existing `docs/...` links and require users to adjust base URL handling manually (rejected: still produces broken first-run behavior).
- Convert to root-relative links (`/docs/requests.md`) (rejected: not portable across local file preview and some markdown renderers).

### Acceptance / test:
- `docs/PRD.md` contains `./requests.md`, `./decisions.md`, and `./PRD.md` link targets only.
- The first linked request now resolves correctly in local preview and repository rendering contexts.

## D-20260219-1702

### Metadata
- **Date:** 2026-02-19 17:02
- **Inputs:** CR-20260219-1702
- **PRD:** PRD linkability correction (local preview compatibility)

### Decision:
Keep `docs/PRD.md` links on the local preview API route (`/api/file?path=...`) and avoid `/docs/...` document routes for clickable source-of-truth links.

### Rationale:
The user reported a 404 on `/docs/requests.md`; current local preview does not serve direct `/docs/...` file routes, while `/api/file?path=...` returns rendered markdown content.

### Alternatives considered:
- Add external server-side redirect support from `/docs/...` to `/api/file?...` (rejected: outside repository control in current scope).
- Keep prior route style and document manual remapping in user workflow (rejected: reintroduced fragile one-off behavior).

### Acceptance / test:
- `curl` against `http://localhost:8765/api/file?path=/Volumes/T9/code/SKILLS/athena/docs/requests.md` returns HTTP 200 and rendered markdown JSON.
- All `docs/PRD.md` cross-document references remain `/api/file?path=...` style and include anchor IDs.
- Local check confirms no remaining `/docs/requests.md` links are emitted from PRD link targets.

## D-20260220-1707

### Metadata
- **Date:** 2026-02-20 17:07
- **Inputs:** CR-20260220-1707
- **PRD:** PRD markdown link portability in local reader

### Decision:
Remove the absolute filesystem prefix from `docs/PRD.md` `/api/file?path=...` links and normalize to `requests.md`, `decisions.md`, and `PRD.md` targets with existing anchor fragments.

### Rationale:
User-reported failures showed absolute-file and `/docs/...` routes breaking in the local markdown reader, while file names with anchor fragments are still the only portable form accepted consistently in this repo.

### Alternatives considered:
- Keep the absolute path prefixes (rejected: host-dependent and not portable in reader links).
- Switch to root-relative document routes like `/docs/requests.md` (rejected: previously returned 404 in this local reader).
- Keep `/api/file?...` but trim to file names only (accepted: minimal change and reader-compatible target shape).

### Acceptance / test:
- No `/Volumes/T9/code/SKILLS/athena/docs/` prefixes remain in `docs/PRD.md` link targets.
- All `CR-...`, `D-...`, `FR-...`, and `NFR-...` references in PRD still use valid anchors and remain clickable.
- `curl -s -w '%{http_code}' 'http://localhost:8765/api/file?path=requests.md#cr-20260211-0939'` returns `200`.
- `curl -s -w '%{http_code}' 'http://localhost:8765/docs/requests.md#cr-20260211-0939'` returns `404`.

## D-20260219-1710

### Metadata
- **Date:** 2026-02-19 17:10
- **Inputs:** CR-20260219-1710
- **PRD:** PRD markdown link portability in local reader

### Decision:
Update `docs/PRD.md` links to document-relative markdown paths and ensure the markdown reader resolves those links through `/api/open-link` so navigation stays inside the preview with section anchors intact.

### Rationale:
The `/api/file?...` link pattern exposed raw JSON and direct-doc failures in the reader workflow for the reported paths. Using compact file+anchor links plus client-side open-link handling provides portable links and in-reader rendering without host-dependent endpoints.

### Alternatives considered:
- Keep `/api/file?...` links only and rely on browser navigation (rejected: raw JSON responses are rendered instead of markdown preview).
- Use absolute filesystem paths in every link (rejected: host-dependent and non-portable).

### Acceptance / test:
- PRD numbered references use markdown file routes with anchor fragments.
- Local reader click flow routes `.md` references through `/api/open-link`.
- Hash fragments (for example `#cr-...`) are applied after loading the linked file.

## D-20260221-1255

### Metadata
- **Date:** 2026-02-21 12:55
- **Inputs:** CR-20260221-1252
- **PRD:** Template delivery and SKILL.md integration (local skill package)

### Decision:
Move ATHENA workflow templates into `skills/athena/templates` and reference those local files directly from `skills/athena/SKILL.md` so packaged skill behavior stays self-contained.

### Rationale:
The request is for local template usage within the installed skill package, so template resolution should not depend on repo-root templates once the skill is executed in this package.

### Alternatives considered:
- Keep using root-level `templates/` entries only (rejected: introduces external dependency and requires users to mirror files outside the skill package).
- Duplicate template content inline in `SKILL.md` (rejected: increases prompt bloat and makes future updates harder).

### Acceptance / test:
- `skills/athena/SKILL.md` points to `skills/athena/templates/*` for template lookups.
- `skills/athena/templates/` contains `requests.md`, `decisions.md`, `progress.txt`, `spec.md`, `tasks.md`, and `traceability.md`.
- Changes are recorded in `docs/specs/20260221-athena-localized-templates` and `docs/progress.txt` with traceable IDs.

## D-20260414-1327

### Metadata
- **Date:** 2026-04-14 13:27
- **Inputs:** CR-20260414-1327
- **PRD:** Owl of Athena — session start token optimization

### Decision:
Add `write-memory` command to owl.py. Run it at SessionStart after update-index. It writes `project_athena_active.md` to `~/.claude/projects/<encoded-repo>/memory/` with active feature, goal, and task state. Athena checks memory at step 2 and skips reading athena-index.md and progress.txt when memory is present. Athena calls `write-memory` at end of session (step 6) to keep memory current.

### Rationale:
Owl already has all needed data at SessionStart (progress.txt, athena-index.md) when prune-done and update-index run. Writing it to Claude Code memory requires zero extra file reads. Athena saves 2 file reads per session (athena-index.md + progress.txt) and gets active context immediately without parsing.

### Alternatives considered:
- Athena writes memory herself during step 2 (rejected: requires Athena to read files first anyway, no savings).
- Add a Stop hook for write-memory (rejected: Stop hook adds complexity; end-of-session call from Athena step 6 is sufficient and more explicit).
- Cache all docs/ files in memory (rejected: docs/ content changes frequently and memory would go stale; only the active-context summary is stable enough to cache).

### Acceptance / test:
- `./scripts/owl write-memory` creates `~/.claude/projects/-Volumes-T9-code-SKILLS-athena/memory/project_athena_active.md` with correct frontmatter.
- Running twice with no intervening progress.txt change → second run returns "no update needed".
- MEMORY.md index updated with entry (no duplicates on re-run).

## D-20260415-1221

### Metadata
- **Date:** 2026-04-15 12:21
- **Inputs:** CR-20260415-1221
- **PRD:** README-only Owl installer correction

### Decision:
Supersede the earlier Option A packaging direction for Phase 1. Treat `install-owl.sh` as root repo setup tooling, not packaged skill runtime, and update README guidance to use `/path/to/athena-skill/scripts/install-owl.sh` from the target ATHENA project root.

### Rationale:
The installer is a one-time operational setup helper that writes project-local `scripts/owl` and `.claude/settings.json`; it is not required for the `skills/athena` agent runtime. README should not imply that a skill-only install includes operational setup tooling.

### Alternatives considered:
- Package `install-owl.sh` inside `skills/athena/scripts/` (rejected for Phase 1: broader operational tooling packaging policy should be handled separately).
- Clean up untracked rejected Option A artifacts now (rejected: Phase 1 is README-only and explicitly avoids deletion).

### Acceptance / test:
- README no longer points `install-owl.sh` setup to `~/.claude/skills/athena/scripts/install-owl.sh`.
- README says setup requires access to a full `athena-skill` checkout and runs that checkout's script from the target project root.
- `CHANGELOG.md`, migration scripts, sweeper scripts, packaged skill scripts, hook installers, and validation rules are not changed by this Phase 1 correction.

## D-20260705-2025
Date: 2026-07-05 20:25
Inputs: CR-20260705-2015
PRD: Token efficiency / KB access model

Decision:
Adopt a script-gated KB (Approach C). The main agent never reads docs/requests.md, docs/decisions.md, or archived specs directly; all KB access goes through ./scripts/owl (deterministic, zero-token). The Owl agent is dispatched only for judgment/synthesis tasks. Optimization priority: main-session context first, total billing second.

Rationale:
Measured per-session overhead in this repo was ~26-32K tokens, dominated by full reads of append-only logs (decisions.md 44KB, requests.md 20KB, PRD 26KB). Scripts remove reads at zero token cost; sub-agents would only relocate the cost.

Alternatives considered:
- Read-discipline only (Approach A) (rejected because files keep growing and discipline is instruction-based; ~8-10K floor)
- Git-native ledger, decisions in commit messages (Approach B) (rejected because commit messages are immutable, decisions can precede commits, and blast radius includes validators/site/migration for all repos)

Acceptance / test:
- A session opens with `owl context` (~300 tokens) instead of reading 5 docs files.

## D-20260705-2026
Date: 2026-07-05 20:26
Inputs: CR-20260705-2015
PRD: Artifacts

Decision:
Retire docs/progress.txt as derived state. Task truth stays in docs/specs/<id>/tasks.md; session notes move to per-feature docs/specs/<id>/notes.md (append-only via `owl add-note`); the session-open summary is generated by `owl context`. `owl migrate` converts existing repos losslessly (per-feature blocks into notes.md, unresolvable blocks into docs/audit/progress-legacy.txt). All owl commands fall back to progress.txt when a repo is unmigrated.

Rationale:
progress.txt duplicated tasks.md and grew without bound; it was read every session. Per-feature notes are naturally pruned by archiving (archived spec dirs are never loaded).

Alternatives considered:
- Keep progress.txt with harder pruning (rejected because it remains a global ever-growing file read at session open)

Acceptance / test:
- After `owl migrate`, progress.txt is gone, notes.md files exist per feature, and `owl context` + `write-memory` still produce correct output.

## D-20260705-2027
Date: 2026-07-05 20:27
Inputs: CR-20260705-2015
PRD: Codex parity

Decision:
Full Claude/Codex parity via scripts: session open is `./scripts/owl context` in both harnesses. On Claude Code, the SessionStart hook pre-writes the same block into auto-memory (write-memory wraps the context builder). Codex AGENTS.md shrinks to trigger + stop-gates (~12 lines); the loop lives only in SKILL.md.

Rationale:
Codex has no hooks or auto-memory; a script-first design makes the hook a convenience layer, not the mechanism, and removes the duplicated (and drifted) loop text from AGENTS.md (~860 tokens per Codex session).

Alternatives considered:
- Claude-first with degraded Codex (rejected by user: full parity chosen)

Acceptance / test:
- Same artifacts and same token profile on both harnesses; AGENTS.md contains no loop steps.

## D-20260705-2028
Date: 2026-07-05 20:28
Inputs: CR-20260705-2015
PRD: Compatibility

Decision:
Keep docs/requests.md and docs/decisions.md filenames and entry formats unchanged; appends go through `owl add-request` / `owl add-decision` (script assigns IDs and timestamps). SKILL.md is rewritten to a ~120-line core with detailed procedures moved to references/ (commits, setup/bootstrap, recovery), and the frontmatter description is cut to one sentence. Root SKILL.md remains a synced identical copy of skills/athena/SKILL.md.

Rationale:
site/ and validate_traceability_links.py parse these files; keeping formats avoids blast radius. Script-assigned IDs eliminate ID-format drift. SKILL.md is loaded on every task, so its size is a per-task tax.

Alternatives considered:
- Single ledger file replacing both logs (rejected: breaks site/validators for no additional token savings, since logs are no longer read wholesale)

Acceptance / test:
- node --test site/ passes; validate_traceability_links.py passes; SKILL.md <= ~130 lines.

## D-20260705-2123
Date: 2026-07-05 21:23
Inputs: CR-20260705-2123
PRD: Next / backlog

Decision:
Publish the v2.1.0 token-improvement release note as docs/releases/v2.1.0.md (new docs/releases/ directory), written in Taylor style, with a measured before/after token table and % reductions sourced from the 20260705-token-diet session measurements (chars/4 token approximation, athena-skill repo as the reference project).

Rationale:
CHANGELOG.md already carries the technical change list; the release note is the shareable announcement. docs/releases/ keeps release communications versioned next to the audit trail; publishing/ is reserved for social posts.

Alternatives considered:
- GitHub release page only (rejected: requires push, which the user has not requested)
- Extend CHANGELOG.md (rejected: different audience and format)

Acceptance / test:
- docs/releases/v2.1.0.md exists, passes scripts/validate_style.py, and states per-surface token numbers with % reductions.

## D-20260706-0642
Date: 2026-07-06 06:42
Inputs: CR-20260706-0642
PRD: Functional requirements

Decision:
Implement the three approved optimizations: (1) PRD diet — new `owl prune-prd` command archives the PRD Metadata Inputs/Decisions link lists and shipped/implemented backlog lines to docs/audit/prd-archive.md (idempotent, pointer lines left behind), plus a hardened SKILL.md rule: never read docs/PRD.md in full — grep for the sections being changed and read only those ranges, `owl show FR-...` for single requirements. (2) Codex skills cleanup — move the 7 loose non-skill files out of ~/.codex/skills into ~/.codex/skills-archive/ (move, not delete); directories without SKILL.md are reported for user review, not touched. (3) Codex reasoning profile — add [profiles.athena] with model_reasoning_effort "medium" to ~/.codex/config.toml for routine loop work; plugins are inventoried and reported, not disabled.

Rationale:
Codex A/B showed thinking tokens and full-PRD reads dominate post-v2.1 cost. Goals and FR history stay in the PRD (they are the requirements source of truth); only derived link ceremony and closed backlog lines move to the audit archive. Config moves are reversible (file moves, additive TOML profile).

Alternatives considered:
- Semantic FR pruning by feature status (rejected: CR-to-feature mapping is not deterministic; risks archiving live requirements)
- Disabling Codex plugins outright (rejected: may break non-athena workflows; user decides from the inventory)

Acceptance / test:
- prune-prd unit-tested, idempotent, PRD shrinks with pointers intact; SKILL.md rule present; loose files moved with inventory reported; profile present in config.toml and codex accepts --profile athena.

## D-20260706-0652
Date: 2026-07-06 06:52
Inputs: CR-20260706-0651
PRD: Next / backlog

Decision:
Release v2.1.0 and v2.2.0 as two separate GitHub releases (tag v2.1.0 at commit 104bd2c, tag v2.2.0 at the README-accuracy commit), with release bodies stating measured per-harness value: Claude -63% end-to-end / -94% fixed overhead, Codex -13.5% end-to-end (delta ~= removed doc-stack). README is updated in place (same structure, corrected content) rather than rewritten; the retired migrate-all-projects.py fleet section is removed; sweep-projects.py stays documented.

Rationale:
Two releases match the two CHANGELOG entries and published-tag history (v2.0.0.1 is the current latest). Measured numbers come from the recorded A/B experiments (docs/specs/20260705-token-diet/notes.md S-20260705-2153).

Alternatives considered:
- Single combined v2.2.0 release (rejected: hides the v2.1.0 milestone that carries the architecture change)

Acceptance / test:
- gh release list shows v2.1.0 and v2.2.0; README greps clean for stale terms; git status clean; origin/main == main.

## D-20261113-1035
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Plugin folder is the repo root (no copied subfolder). skills/athena/SKILL.md is already the expected skills/<name>/SKILL.md layout, so adding .claude-plugin/plugin.json at the root avoids a third copy of scripts and agents. Root SKILL.md is kept (single-skill install path).

## D-20261113-1036
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Plugin name is "athena" (matches the skill name). Recheck against the validator's repository-name note before submission; the GitHub repo is athena-skill.

## D-20261113-1037
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Plugin version is 2.2.0, taken from VERSION and matching existing git tag v2.2.0. Not the 0.1.0 example in the request.

## D-20261113-1038
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: License is MIT, stated in LICENSE (Copyright 2026 Taylor Parsons). Author name "Taylor Parsons" comes from that copyright line. No author email, no contact address: left out, listed as an owner question.

## D-20261113-1039
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Move agents/OWL-IMPLEMENTATION.md out of agents/ (to docs/agents/ or similar, after grep for references). It has no frontmatter, so the plugin would load it as an agent. Adding frontmatter would turn an implementation doc into a live agent, so it is moved, not edited.

## D-20261113-1040
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Plugin icon is a PNG rendered from skills/athena/assets/athena-warrior-icon.svg (512 to 2048 px, square). The directory accepts only PNG/JPEG for the icon, and the icon is locked on first submit, so the owner must approve it.

## D-20261113-1041
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Add .claude-plugin/marketplace.json so /plugin marketplace add taylorparsons/athena-skill works as the README will describe. Without it, the install command in the README has no target.

## D-20261113-1042
Date: 2026-11-13 10:35
Inputs: CR-20261113-1034
PRD: (n/a)

D: Work stays local on branch submission-prep. Nothing is pushed, merged, or submitted. docs/athena-index.md is dirty from the SessionStart hook and is excluded from commits.

## D-20261113-1228
Date: 2026-11-13 12:28
Inputs: CR-20261113-1228
PRD: (n/a)

D: Branch submission-prep-contact is cut from submission-prep so the plugin files are included. Owner-supplied email added as author.email in plugin.json and owner.email in marketplace.json; SUBMISSION_NOTES.md contact TODO resolved.

## D-20261113-1302
Date: 2026-11-13 13:02
Inputs: CR-20261113-1302
PRD: (n/a)

D: Copy the installed ~/.claude/skills/athena changes (SKILL.md, agents/owl-of-athena.md, scripts/owl.py, validate_traceability_links.py, tests/test_owl.py) into skills/athena and the root mirrors (SKILL.md, agents/, scripts/). sweep-projects.py already matched. Installed copy scanned first: no personal paths or secrets. Version not bumped; owner to decide.
