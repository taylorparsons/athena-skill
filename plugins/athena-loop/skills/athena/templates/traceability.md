# Traceability (How to follow the audit trail)

Prefer the scripts: `./scripts/owl show <CR-...|D-...|FR-...>` prints one entry; `./scripts/owl why <FR-...>` walks the whole chain. To follow it by hand:

1) Find the relevant raw request in `docs/requests.md` (CR-...).
2) Read linked interpretations/tradeoffs in `docs/decisions.md` (D-...).
3) Open the feature spec at `docs/specs/<FEATURE_ID>/spec.md`.
   - Requirements use IDs (FR-...) and include `Sources: CR-...; D-...`.
   - Acceptance scenarios include `Verifies: FR-...`.
4) Open the feature task list at `docs/specs/<FEATURE_ID>/tasks.md`.
   - Tasks include `Implements: FR-...`.
5) Review session notes in `docs/specs/<FEATURE_ID>/notes.md` for commands, outcomes, and commit hashes.

If the repo adopted ATHENA after it already had history, review `docs/audit/git-history.md` as part of step 1 (derived from Git; not customer verbatim). Repos migrated from the legacy layout may also have `docs/audit/progress-legacy.txt` (pre-migration session notes not attributable to a feature).
