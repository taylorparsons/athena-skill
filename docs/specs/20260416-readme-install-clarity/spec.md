# README Install Clarity

## Metadata
- **Status:** Done
- **Sources:** CR-20260416-1446; D-20260416-1447

## User Story
As a new ATHENA user, I want the README install section to show the right path for Codex and the right path for Claude Code at a glance, so I can install the framework without scanning through irrelevant steps.

## Functional Requirements
- FR-001: `README.md` must present a distinct Codex quick-start install path for the packaged ATHENA skill. (Sources: CR-20260416-1446; D-20260416-1447)
- FR-002: `README.md` must present a distinct Claude Code quick-start install path for the ATHENA skill. (Sources: CR-20260416-1446; D-20260416-1447)
- FR-003: `README.md` must explicitly identify Owl setup as Claude Code only and tell Codex users they can stop after the ATHENA skill install. (Sources: CR-20260416-1446; D-20260416-1447)
- FR-004: This feature must not change install scripts or Claude configuration files. (Sources: CR-20260416-1446; D-20260416-1447)

## Acceptance Scenarios
- Given a user opens the README Installation section, when they use Codex, then they can follow a dedicated Codex quick-start path without reading Claude-only Owl setup. (Verifies: FR-001, FR-003)
- Given a user opens the README Installation section, when they use Claude Code, then they can follow a dedicated Claude Code quick-start path and see Owl setup called out as an additional Claude-only step. (Verifies: FR-002, FR-003)
- Given the tracked diff for this feature, when changed files are reviewed, then only `README.md` and the required ATHENA audit docs/spec files are changed. (Verifies: FR-004)

## Safety Constraints
- Do not change install commands or runtime behavior.
- Do not modify `.claude/*`, `scripts/install-owl.sh`, `skills/athena/scripts/install-owl.sh`, or migration scripts.
