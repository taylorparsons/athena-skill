# Feature Spec: 20260706-readme-release-push

Status: Active
Created: 2026-07-06 06:52
Inputs: CR-20260706-0651
Decisions: D-20260706-0652

## Summary
- Bring README.md up to v2.2.0 reality (script-gated KB, tasks.md/notes.md instead of progress.txt, owl context/migrate, current package contents, retired scripts removed), publish GitHub releases v2.1.0 and v2.2.0 with measured per-harness value (Claude and Codex), and push main + tags to origin.

## Requirements

Functional requirements:
- FR-001: README.md contains no stale progress.txt-era workflow guidance: artifacts list, Owl section, token table, mermaid flows, upgrade path, fleet section, key-files table, and quick start reflect v2.2.0 (script-gated owl commands, per-feature notes.md, owl migrate, measured A/B numbers for both harnesses). (Sources: CR-20260706-0651; D-20260706-0652)
- FR-002: Install/setup steps verified against the shipped package: package contents (SKILL.md, references/, templates/, scripts/, agents/, assets/), Codex AGENTS.md minimal block, hooks unchanged and conditional, retired scripts (migrate-all-projects.py) removed from docs. (Sources: CR-20260706-0651; D-20260706-0652)
- FR-003: GitHub releases v2.1.0 and v2.2.0 exist with tags, bodies stating measured value for both Claude (−63% end-to-end, −94% fixed overhead) and Codex (−13.5% end-to-end ≈ the removed doc-stack overhead), and the v2.1.0 release-note doc gains the same A/B table. (Sources: CR-20260706-0651; D-20260706-0652)
- FR-004: main and the new tags pushed to origin; working tree clean afterward. (Sources: CR-20260706-0651)

## Edge cases
- site/ remains untracked (belongs to 20260603-athena-site-app) and must not be swept into the push. (Verifies: FR-004)
