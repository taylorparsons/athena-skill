# ATHENA Explanatory Site

## Metadata
- **Status:** Done
- **Sources:** CR-20260602-2025; D-20260602-2026

## User Story
As a new potential ATHENA user, I want a bold, concise site that explains what ATHENA is, how its traceability loop works, and how to install it, so I can decide whether to adopt it without reading the full repository README first.

## Functional Requirements
- FR-001: The repository must include a static site under `site/` that can be served without installing a frontend toolchain. (Sources: CR-20260602-2025; D-20260602-2026)
- FR-002: The homepage must explain ATHENA in plain language as a framework for turning requests into traceable shipped work. (Sources: CR-20260602-2025; D-20260602-2026)
- FR-003: The homepage must show the ATHENA loop: customer request, decision, PRD, spec, task, validation, and commit/audit trail. (Sources: CR-20260602-2025; D-20260602-2026)
- FR-004: The homepage must include install paths for Codex and Claude Code. (Sources: CR-20260602-2025; D-20260602-2026)
- FR-005: The homepage must use a bold, distinctive product-launch visual direction while remaining readable on desktop and mobile. (Sources: CR-20260602-2025; D-20260602-2026)
- FR-006: The site must be locally publishable and visible in a browser during the session. (Sources: CR-20260602-2025; D-20260602-2026)

## Acceptance Scenarios
- Given the repository root, when `site/index.html` is opened through a local static server, then the ATHENA homepage renders. (Verifies: FR-001, FR-006)
- Given the homepage content, when a new user scans the first viewport and explanation sections, then they can identify what ATHENA does and how the traceability loop works. (Verifies: FR-002, FR-003)
- Given the install section, when a user chooses Codex or Claude Code, then they see the correct install path for that environment. (Verifies: FR-004)
- Given desktop and mobile viewport widths, when the page is rendered, then key text and layout elements remain readable without overlap. (Verifies: FR-005)

## Safety Constraints
- Do not add a package-manager dependency for this site.
- Do not replace or delete existing README content.
