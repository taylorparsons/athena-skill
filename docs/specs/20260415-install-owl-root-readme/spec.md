# Install Owl Root README Guidance

## Metadata
- **Status:** Done
- **Sources:** CR-20260415-1221; D-20260415-1221

## User Story
As an ATHENA user setting up Owl, I want README commands to distinguish root repository setup tooling from packaged skill runtime files so I run the installer from the correct location.

## Functional Requirements
- FR-001: README must not instruct users to run `install-owl.sh` from `~/.claude/skills/athena/scripts/`. (Sources: CR-20260415-1221; D-20260415-1221)
- FR-002: README must document `install-owl.sh` as requiring access to a full `athena-skill` checkout. (Sources: CR-20260415-1221; D-20260415-1221)
- FR-003: README must instruct users to run the full-checkout script from the target ATHENA project root. (Sources: CR-20260415-1221; D-20260415-1221)
- FR-004: Phase 1 must not change `CHANGELOG.md`, migration scripts, sweeper scripts, packaged skill scripts, hook installers, or validation rules. (Sources: CR-20260415-1221; D-20260415-1221)

## Acceptance Scenarios
- Given a user reads README Owl setup guidance, when they see the installer command, then it uses `/path/to/athena-skill/scripts/install-owl.sh` instead of the packaged skill path. (Verifies: FR-001, FR-002)
- Given a user is setting up a separate ATHENA project, when they follow README guidance, then they run the full-checkout script from that target project root. (Verifies: FR-003)
- Given the Phase 1 diff is reviewed, when changed tracked files are listed, then no prohibited files are included. (Verifies: FR-004)

## Safety Constraints
- Do not run `scripts/install-owl.sh`, `skills/athena/scripts/install-owl.sh`, migration scripts, sweeper scripts, or hook installers.
- Do not change `CHANGELOG.md`, migration scripts, sweeper scripts, packaged skill scripts, hook installers, or validation rules.
- Do not delete the untracked rejected Option A spec directory in this phase.
