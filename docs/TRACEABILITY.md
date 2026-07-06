# Traceability (How to follow the audit trail)

Prefer the scripts: `./scripts/owl show <CR-...|D-...|FR-...>` prints one entry; `./scripts/owl why <FR-...>` walks the whole chain. To follow it by hand:

## Start Here
### 1) Raw Requests
- Locate customer requests in `docs/requests.md` (`CR-...`).

### 2) Decisions
- Locate interpretations and scope tradeoffs in `docs/decisions.md` (`D-...`).

### 3) PRD Source of Truth
- Read source requirements in `docs/PRD.md`.

### 4) Feature Spec
- Read spec files in `docs/specs/<FEATURE_ID>/spec.md` (`FR-...`, `Verifies: FR-...`).

### 5) Tasks
- Read execution mapping in `docs/specs/<FEATURE_ID>/tasks.md` (`T-...`, `Implements: FR-...`).

### 6) Session Notes
- Review execution evidence in `docs/specs/<FEATURE_ID>/notes.md` (commands, outcomes, commit hashes).
- Pre-migration session history not attributable to a feature lives in `docs/audit/progress-legacy.txt`.
