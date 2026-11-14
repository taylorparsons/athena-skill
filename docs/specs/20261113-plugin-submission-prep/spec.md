# Feature Spec: 20261113-plugin-submission-prep

Status: Active
Created: 2026-11-13 10:34
Inputs: CR-20261113-1034
Decisions: D-20261113-1035 (plugin folder), D-20261113-1036 (name), D-20261113-1037 (version), D-20261113-1038 (license/author), D-20261113-1039 (OWL doc move), D-20261113-1040 (icon), D-20261113-1041 (marketplace.json), D-20261113-1042 (local branch only)

## Summary
- Prepare taylorparsons/athena-skill to be submitted as a Claude plugin to the Claude plugin directory. Add the plugin manifest, a README install section, draft privacy notes, and a passing `claude plugin validate`. Owner-only facts are TODO, not guessed.

## Requirements

Functional requirements:
- FR-001: The repo root contains .claude-plugin/plugin.json with name, description, version, author, license, and repository. Contact email and any unknown fact are TODO. (Sources: CR-20261113-1034; D-20261113-1035; D-20261113-1037; D-20261113-1038)
- FR-002: The skill (skills/athena/SKILL.md) sits in the plugin's skills tree and its frontmatter has name and description. No changes to SKILL.md content. (Sources: CR-20261113-1034)
- FR-003: The README gets an added plugin-install section that states only behavior the code shows, including the per-project scripts/owl requirement. Rest of README unchanged. (Sources: CR-20261113-1034; D-20261113-1041)
- FR-004: SUBMISSION_NOTES.md at the repo root holds draft privacy and data-handling answers, labeled as drafts for the owner to confirm. (Sources: CR-20261113-1034)
- FR-005: `claude plugin validate` passes with no warnings for the plugin, including the --profile directory check. (Sources: CR-20261113-1034; D-20261113-1040)
- FR-006: No push, merge, visibility change, or directory submission. (Sources: CR-20261113-1034; D-20261113-1042)

## Edge cases
- agents/OWL-IMPLEMENTATION.md lacks frontmatter and would load as an agent (Verifies: FR-005; D-20261113-1039)
- docs/athena-index.md is modified by the SessionStart hook and must stay out of commits (Verifies: FR-006; D-20261113-1042)
