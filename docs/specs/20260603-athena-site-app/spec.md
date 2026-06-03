# ATHENA Site App Redesign

## Metadata
- **Status:** In Progress
- **Sources:** CR-20260603-1258; D-20260603-1300

## User Story
As a prospective ATHENA adopter, I want a richer site experience than the current static prototype, so I can understand the framework, evaluate why it matters, and navigate deeper material about install, architecture, examples, and Owl from one coherent frontend app.

## Functional Requirements
- FR-001: The repository must define a follow-on site redesign that supersedes the simple static prototype as the target experience. (Sources: CR-20260603-1258; D-20260603-1300)
- FR-002: The site must open with a hybrid hero that explains why ATHENA matters and immediately exposes the core loop. (Sources: CR-20260603-1258; D-20260603-1300)
- FR-003: The site must include deeper sections for install, core loop, architecture, examples, and Owl. (Sources: CR-20260603-1258; D-20260603-1300)
- FR-004: The design must assume a real frontend app structure with navigation and richer interactions than the current static prototype. (Sources: CR-20260603-1258; D-20260603-1300)
- FR-005: The tone and visual system must feel assertive and visionary, like a framework launch page, while staying concrete and technically legible. (Sources: CR-20260603-1258; D-20260603-1300)

## Acceptance Scenarios
- Given the design doc, when the user reviews the first-screen description, then the hybrid hero and immediate loop placement are explicit. (Verifies: FR-002)
- Given the design doc, when the information architecture is reviewed, then install, loop, architecture, examples, and Owl are all included. (Verifies: FR-003)
- Given the design doc, when the implementation direction is reviewed, then the site is framed as a real frontend app rather than the current static prototype. (Verifies: FR-001, FR-004)
- Given the design doc, when the visual direction is reviewed, then the launch-page tone and technical readability goals are explicit. (Verifies: FR-005)

## Safety Constraints
- Do not implement the redesign before the user reviews the written design.
- Preserve the existing static `site/` prototype as baseline context until the redesign is approved.
