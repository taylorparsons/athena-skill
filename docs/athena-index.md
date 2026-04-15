# Athena Feature Index

**Purpose**: Lightweight index to reduce token overhead by loading only active features.  
**Last updated**: 2026-04-14

## How to Use This Index

**For Athena agents**: Load this athena-index.md first. Only load specs marked as "Active" below. Skip "Archived" features unless explicitly requested by user.

**For humans**: This index shows all features. Archived features are complete and should not be modified.

---

## Active Features (Load these during sessions)

*No active features currently. All features are archived.*

---

## Archived Features (Skip unless explicitly requested)

### 20260211-athena-walkthrough-example
- **Status**: Done
- **Spec**: docs/specs/20260211-athena-walkthrough-example/spec.md
- **Summary**: Add an onboarding walkthrough under `docs/examples/` showing how one request moves through CR -> Decision -> PRD -> Spec -> Task -> Progress.

### 20260211-public-release-hardening
- **Status**: Done
- **Spec**: docs/specs/20260211-public-release-hardening/spec.md
- **Summary**: Harden this public-share repository for publication by cleaning local strings, adding governance/security artifacts, and rewriting history to a clean baseline.

### 20260211-public-share-cleanup
- **Status**: Done
- **Spec**: docs/specs/20260211-public-share-cleanup/spec.md
- **Summary**: Remove imported artifacts and rebuild a clean, repo-scoped ATHENA documentation trail for public sharing.

### 20260211-remove-daisy-from-athena-share
- **Status**: Done
- **Spec**: docs/specs/20260211-remove-daisy-from-athena-share/spec.md
- **Summary**: Remove Daisy companion-skill references from this public ATHENA share repo so the published version is scoped only to ATHENA.

### 20260211-single-skill-install
- **Status**: Done
- **Spec**: docs/specs/20260211-single-skill-install/spec.md
- **Summary**: Keep public installation deterministic by exposing only one installable skill target (`skills/athena`) and documenting only that path.

### 20260212-athena-rename
- **Status**: Done
- **Spec**: docs/specs/20260212-athena-rename/spec.md
- **Summary**: Migrate this repository's mutable skill/project identity to `athena`, including path names, install metadata, and code/documentation references, while preserving append-only historical request/decisio

### 20260213-checkin-merge-remote
- **Status**: Done
- **Spec**: docs/specs/20260213-checkin-merge-remote/spec.md
- **Summary**: Perform a traceable local check-in and remote merge/push for the README fast-visual update while excluding unrelated local modifications from the commit.

### 20260213-linkedin-personal-style
- **Status**: Done
- **Spec**: docs/specs/20260213-linkedin-personal-style/spec.md
- **Summary**: Add one additional LinkedIn-ready ATHENA post draft that uses the maintainer's personal writing style: direct, structured, grounded, operator-focused, and low-hype, while preserving concrete setup and

### 20260213-linkedin-post-variants
- **Status**: Done
- **Spec**: docs/specs/20260213-linkedin-post-variants/spec.md
- **Summary**: Create two LinkedIn-ready post variants that explain ATHENA end-to-end flow from invocation/request through loop execution to check-in completion, with clear install instructions for both Codex and Cl

### 20260213-readme-fast-visual
- **Status**: Done
- **Spec**: docs/specs/20260213-readme-fast-visual/spec.md
- **Summary**: Add a fast visual at the top of `README.md` using a new tracked diagram asset derived from the customer-provided image, explicitly avoiding the untracked `docs/athena-napkin-loop.svg` file.

### 20260216-review-findings-remediation
- **Status**: Done
- **Spec**: docs/specs/20260216-review-findings-remediation/spec.md
- **Summary**: Remediate findings 1-5 from the project review: traceability state drift, resume prompt placeholder parsing, markdown secret-scan coverage, local path hygiene, and git-audit output path anchoring.

### 20260217-absolute-path-hygiene
- **Status**: Done
- **Spec**: docs/specs/20260217-absolute-path-hygiene/spec.md
- **Summary**: Remove remaining absolute-path residues from tracked ATHENA docs so repository security audit no longer reports `HIGH` path findings.

### 20260217-athena-hardening-plan
- **Status**: Done
- **Spec**: docs/specs/20260217-athena-hardening-plan/spec.md
- **Summary**: Implement all remaining ATHENA hardening workstreams after the planning phase: traceability linting, canonical merge/check-in checklist consolidation, path-scoped staging defaults, and progress-log sc

### 20260217-athena-install-icon-metadata
- **Status**: Done
- **Spec**: docs/specs/20260217-athena-install-icon-metadata/spec.md
- **Summary**: Ensure ATHENA installs expose the warrior icon asset through skill metadata and keep that contract enforced by install-target validation.

### 20260217-athena-warrior-icon
- **Status**: Done
- **Spec**: docs/specs/20260217-athena-warrior-icon/spec.md
- **Summary**: Add a new SVG icon asset for the `athena` skill package that visually invokes a warrior archetype.

### 20260218-staging-precheck-guardrails
- **Status**: Done
- **Spec**: docs/specs/20260218-staging-precheck-guardrails/spec.md
- **Summary**: Restore broad staging workflow in traceable commits while adding pre-stage guardrails for risky files.

### 20260218-version-bump-1-1-0
- **Status**: Done
- **Spec**: docs/specs/20260218-version-bump-1-1-0/spec.md
- **Summary**: Bump ATHENA repository version from `1.0.1` to `1.1.0` in the canonical `VERSION` file with full ATHENA traceability.

### 20260220-docs-readability-format
- **Status**: Done
- **Spec**: docs/specs/20260220-docs-readability-format/spec.md
- **Summary**: Improve scanability of ATHENA markdown documentation by adding clearer heading hierarchy and bold labels in root docs and `docs/specs/*/spec.md` while keeping traceability structure intact.

### 20260221-athena-localized-templates
- **Status**: Done
- **Spec**: docs/specs/20260221-athena-localized-templates/spec.md
- **Summary**: Keep ATHENA reusable templates inside the `skills/athena` package so the installed skill is self-contained and always references local template assets.

### 20260414-athena-index-rename
- **Status**: Done
- **Spec**: docs/specs/20260414-athena-index-rename/spec.md
- **Summary**: 

### 20260414-owl-memory-bridge
- **Status**: Done
- **Spec**: docs/specs/20260414-owl-memory-bridge/spec.md
- **Summary**: 

---

## Token Optimization

**Without athena-index.md**:
- Load all 21 specs = ~10,500 tokens

**With athena-index.md**:
- Load athena-index.md only = ~1100 tokens
- Load 0 active specs = ~0 tokens
- **Total**: ~1100 tokens
- **Savings**: ~89% reduction

**Usage Pattern**:
1. Athena loads athena-index.md first
2. Identifies active features (currently: 0)
3. Skips 21 archived features
4. If user asks about archived feature, load on-demand
