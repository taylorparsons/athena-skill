# ATHENA Site App Design

## Intent

Replace the current single-page static prototype with a richer frontend app that feels like a framework launch and a technical product surface at the same time. The site should persuade new users that ATHENA is a serious operating model for agent-driven delivery, then let them move directly into install, loop mechanics, architecture, examples, and Owl without context loss.

## Audience

- Primary: new users deciding whether to adopt ATHENA.
- Secondary: technically capable evaluators who want to inspect how ATHENA works before installing it.

## Product Goal

The site should answer three questions in one pass:

1. What is ATHENA?
2. Why is it better than ad hoc agent work?
3. How do I start using it?

## Recommended Shape

Build the redesign as a real frontend app rather than another static document page. In practice, that means route-aware navigation, richer section transitions, interactive loop and architecture views, and content modules that can grow without collapsing back into a long linear page.

For the first version, the app can still ship as a mostly single-flow experience, but the architecture should assume multiple screens or routes so deeper technical sections do not compete with the launch narrative in the first viewport.

## Information Architecture

### 1. Landing / Hero

The first screen should be a hybrid hero:

- Top half: why ATHENA matters.
- Immediately below: the ATHENA loop visible without requiring a second navigation step.

The hero should establish ATHENA as a framework for turning ambiguous requests into inspectable delivery. The loop should be visible fast enough that a user can understand the system model in seconds, not after reading paragraphs.

### 2. Install

The install surface should remain practical and split by environment:

- Codex
- Claude Code

This section should feel like a product setup surface, not a README dump. Commands and next steps should be directly scannable.

### 3. Core Loop

This section should explain the request-to-shipped-code chain:

- Customer Request
- Decision
- PRD
- Feature Spec
- Task
- Validation
- Commit / traceability

Each stage should answer both what it is and why it exists.

### 4. Architecture

This section should explain how ATHENA is structured in the repo:

- Core framework
- Adapters
- Docs artifacts
- Scripts
- Owl

The goal is not exhaustive file inventory. The goal is to make the system legible enough that a new adopter understands where logic, process, and automation live.

### 5. Examples

Show one concrete traceability path from a request to shipped work. This should visually connect the abstract loop to the real artifact chain already present in the repo.

### 6. Owl

Owl should be framed as the archive and memory-management companion, not as the main framework itself. This section should explain what Owl does, when it matters, and why it helps long-running ATHENA repos stay usable.

## Visual Direction

The site should feel assertive and deliberate, like a framework launch page rather than a documentation theme. It should not look like a generic gradient landing page or a corporate SaaS shell.

Recommended visual characteristics:

- Strong typography with large, compressed headlines for the hero.
- Structured diagram language drawn from traceability artifacts, IDs, ledgers, commit markers, and audit surfaces.
- A palette that feels editorial and operational at once: ink, paper, signal colors, and one or two forceful accent hues.
- Motion that supports comprehension: staged reveals, line draws, and section transitions tied to the loop and architecture diagrams.

Avoid:

- Soft card farms
- Generic startup gradient heroes
- Decorative blobs or abstract mood visuals
- Hiding the loop below the fold

## Interaction Model

The redesign should introduce richer interactions than the current prototype, but those interactions must increase comprehension rather than novelty.

Recommended interactions:

- A loop module where hovering or tapping a stage expands its role and artifact mapping.
- A route or tab switch between “Adopt”, “How It Works”, and “Inside the Repo”.
- Install panels that can switch between Codex and Claude Code cleanly.
- An architecture section with highlighted subsystem relationships.

Do not make the core explanation depend on a complex animation sequence. The page should remain understandable even if a user only scrolls and scans.

## Content Strategy

The writing should stay concrete. The voice can be assertive, but the claims need to be grounded in what the repo actually does.

Content priorities:

1. Explain the framework in plain language.
2. Show the loop early.
3. Connect abstract claims to real repo artifacts.
4. Give install paths before the user loses patience.
5. Reserve longer explanation for architecture, examples, and Owl.

## Technical Direction

The implementation should move from the current static prototype toward an app structure with reusable content modules and navigable sections. The exact framework can be chosen during implementation planning, but the resulting shape should support:

- navigation state
- interactive loop views
- reusable documentation sections
- responsive behavior across desktop and mobile

The redesign should treat the current `site/` directory as baseline content and interaction research, not as the final structure that must be preserved verbatim.

## Testing and Verification

Implementation planning should cover:

- content-level smoke tests for required sections and copy anchors
- responsive verification across desktop and mobile
- local server verification
- browser-level rendering checks once a real app runtime exists

## Scope Boundary

In scope:

- design for the richer app experience
- information architecture
- visual direction
- interaction model
- implementation guidance

Out of scope for this design pass:

- final framework selection
- production deployment
- full docs content authoring beyond the structure and representative examples

## Self-Review

- Placeholder scan: no placeholders remain.
- Internal consistency: the app direction, hybrid hero, and deeper docs structure all align.
- Scope check: focused on one redesign initiative and ready for implementation planning.
- Ambiguity check: the site is explicitly framed as a real frontend app rather than another static single-page artifact.
