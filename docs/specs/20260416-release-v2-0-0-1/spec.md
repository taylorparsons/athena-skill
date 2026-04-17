# Release v2.0.0.1

## Metadata
- **Status:** Done
- **Sources:** CR-20260416-1656; D-20260416-1657

## User Story
As the ATHENA maintainer, I want a `v2.0.0.1` version bump, a local tag, and GitHub-release-ready notes based on the already-published `v2.0.0` release, so I can publish the next patch release without ambiguity.

## Functional Requirements
- FR-001: `VERSION` must be updated to `2.0.0.1`. (Sources: CR-20260416-1656; D-20260416-1657)
- FR-002: `CHANGELOG.md` must contain a `v2.0.0.1` entry with `Summary` and `What's Changed` sections suitable for a GitHub release draft. (Sources: CR-20260416-1656; D-20260416-1657)
- FR-003: The `v2.0.0.1` notes must be written as a patch release on top of the already-published GitHub release `v2.0.0`. (Sources: CR-20260416-1656; D-20260416-1657; D-20260416-1659)
- FR-004: A local git tag `v2.0.0.1` must exist after the release commit. (Sources: CR-20260416-1656; D-20260416-1657)

## Acceptance Scenarios
- Given the repository root, when `VERSION` is read, then the file contains `2.0.0.1`. (Verifies: FR-001)
- Given `CHANGELOG.md`, when the top release entry is reviewed, then it includes `Summary` and `What's Changed` for `v2.0.0.1` and only covers the post-`v2.0.0` patch delta. (Verifies: FR-002, FR-003)
- Given the local repository tags, when tags are listed, then `v2.0.0.1` appears. (Verifies: FR-004)

## Safety Constraints
- Do not rewrite or delete the existing `v2.0.0` tag.
- Use the already-published `v2.0.0` release as the baseline and keep that distinction explicit in the release notes.
