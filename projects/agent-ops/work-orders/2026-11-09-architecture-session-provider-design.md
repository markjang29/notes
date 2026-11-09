# Architecture visibility and execution-provider design

Work order: ARCH-OBS-20261109-01
Requested scheduling policy: after_current_work
Publication status: issued; manager acknowledgment and queue registration must be reported separately.

## Scheduling

Record this as the next work item. Identify currently active development/review work and its existing completion criteria, finish that work, then begin. Do not interrupt active sessions or start a duplicate implementation. Distinguish blocked work from completed work; ongoing background services are not predecessor development tasks. If no work is active, record that fact and begin within the existing delegated scope.

Extend the already received reporting/acceptance guidance. Reuse overlapping inventory, collection, reporting and verification work. Preserve prior approvals and acceptance criteria.

## Requested outcome

Provide a read-only overview that connects objectives, architecture components, changes, tasks, execution sessions, source changes, review and deployment evidence. The user must be able to identify why a change exists, where it acts, what depends on it and which decision is needed, without reading code or reconstructing many chat threads.

Make original directives and existing conversation/session history available as drill-down evidence. Distinguish observed facts, declared design, proposed changes, AI-inferred associations and missing observations. Show freshness and unmapped items. Keep the expected actor denominator independent of responders.

## Provider-management design option

Evaluate a unified catalog for providers, connections, models, agent harnesses and versioned execution profiles. Preserve separate contracts for API requests and harness session lifecycle operations. Record capabilities, identity references, run lineage, evidence and measured/estimated/unknown usage distinctly. Do not double-count direct requests and harness aggregates. Unsupported resume/cancel capabilities must remain explicit.

This requests a catalog and adapter design, plus a small isolated proof of the contracts. Live provider migration and takeover of existing sessions are subsequent work. Compare reuse of the existing components before adding another management product.

## Acceptance and report

First deliver a read-only pilot with one real task traceable from objective to original instruction, session and code/review evidence. Demonstrate missing-actor visibility, orphan-task/session discovery, stale collection, duplicate events and restart recovery. Keep implementation, submission and independent review separate.

For a later control pilot, design one owner per execution, explicit handoff and command idempotency so two interfaces cannot execute the same command twice.

Submit one integrated report with the predecessor work, acknowledgment of this work order, implementation/evidence links, passed/failed/not-run checks, and at most three decisions with recommendations. Existing authority governs operational changes; this work order does not grant unrelated approvals.
