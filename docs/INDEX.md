# Athena Feature Index

**Purpose**: Lightweight index to reduce token overhead by loading only active features.  
**Last updated**: 2026-04-13

## How to Use This Index

**For Athena agents**: Load this INDEX.md first. Only load specs marked as "Active" below. Skip "Archived" features unless explicitly requested by user.

**For humans**: This index shows all features. Archived features are complete and should not be modified.

---

## Active Features (Load these during sessions)

*No active features currently. All features are archived.*

---

## Archived Features (Skip unless explicitly requested)

### 20260221-athena-localized-templates
- **Status**: Done (2026-02-21)
- **Spec**: docs/specs/20260221-athena-localized-templates/spec.md
- **Summary**: Add localized skill templates and traceability

### 20260220-docs-readability-format
- **Status**: Done (2026-02-20)
- **Spec**: docs/specs/20260220-docs-readability-format/spec.md
- **Summary**: Improve docs readability and formatting

### 20260218-version-bump-1-1-0
- **Status**: Done (2026-02-18)
- **Spec**: docs/specs/20260218-version-bump-1-1-0/spec.md
- **Summary**: Version bump to 1.1.0

### 20260218-staging-precheck-guardrails
- **Status**: Done (2026-02-18)
- **Spec**: docs/specs/20260218-staging-precheck-guardrails/spec.md
- **Summary**: Add staging precheck guardrails

### 20260217-athena-warrior-icon
- **Status**: Done (2026-02-17)
- **Spec**: docs/specs/20260217-athena-warrior-icon/spec.md
- **Summary**: Add Athena warrior icon

### 20260217-athena-install-icon-metadata
- **Status**: Done (2026-02-17)
- **Spec**: docs/specs/20260217-athena-install-icon-metadata/spec.md
- **Summary**: Add install icon metadata

### 20260217-athena-hardening-plan
- **Status**: Done (2026-02-17)
- **Spec**: docs/specs/20260217-athena-hardening-plan/spec.md
- **Summary**: ATHENA hardening planning docs

### 20260217-absolute-path-hygiene
- **Status**: Done (2026-02-17)
- **Spec**: docs/specs/20260217-absolute-path-hygiene/spec.md
- **Summary**: Absolute path hygiene improvements

### 20260216-review-findings-remediation
- **Status**: Done (2026-02-16)
- **Spec**: docs/specs/20260216-review-findings-remediation/spec.md
- **Summary**: Remediate review findings

### 20260213-readme-fast-visual
- **Status**: Done (2026-02-13)
- **Spec**: docs/specs/20260213-readme-fast-visual/spec.md
- **Summary**: README fast visual improvements

### 20260213-linkedin-post-variants
- **Status**: Done (2026-02-13)
- **Spec**: docs/specs/20260213-linkedin-post-variants/spec.md
- **Summary**: LinkedIn post variants

### 20260213-linkedin-personal-style
- **Status**: Done (2026-02-13)
- **Spec**: docs/specs/20260213-linkedin-personal-style/spec.md
- **Summary**: LinkedIn personal style guide

### 20260213-checkin-merge-remote
- **Status**: Done (2026-02-13)
- **Spec**: docs/specs/20260213-checkin-merge-remote/spec.md
- **Summary**: Check-in merge remote workflow

### 20260212-athena-rename
- **Status**: Done (2026-02-12)
- **Spec**: docs/specs/20260212-athena-rename/spec.md
- **Summary**: Rename skill to Athena

### 20260211-single-skill-install
- **Status**: Done (2026-02-11)
- **Spec**: docs/specs/20260211-single-skill-install/spec.md
- **Summary**: Single skill install support

### 20260211-remove-daisy-from-athena-share
- **Status**: Done (2026-02-11)
- **Spec**: docs/specs/20260211-remove-daisy-from-athena-share/spec.md
- **Summary**: Remove Daisy from Athena share

### 20260211-public-share-cleanup
- **Status**: Done (2026-02-11)
- **Spec**: docs/specs/20260211-public-share-cleanup/spec.md
- **Summary**: Public share cleanup

### 20260211-public-release-hardening
- **Status**: Done (2026-02-11)
- **Spec**: docs/specs/20260211-public-release-hardening/spec.md
- **Summary**: Public release hardening

### 20260211-athena-walkthrough-example
- **Status**: Done (2026-02-11)
- **Spec**: docs/specs/20260211-athena-walkthrough-example/spec.md
- **Summary**: Onboarding walkthrough showing CR→Task chain

---

## Token Optimization

**Without INDEX.md**:
- Load all 19 specs = ~9,500 tokens

**With INDEX.md**:
- Load INDEX.md only = ~500 tokens
- Load 0 active specs = 0 tokens
- **Total**: ~500 tokens
- **Savings**: 95%

**Usage Pattern**:
1. Athena loads INDEX.md first
2. Identifies active features (currently: 0)
3. Skips all 19 archived features
4. If user asks about archived feature, load on-demand
