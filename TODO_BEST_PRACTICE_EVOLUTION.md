# Best-Practice Evolution Backlog

This file holds ideas that are not settled AutoQA guidance. Do not present them as defaults until the promotion rule is satisfied.

## Promotion Rule

- Capture a new official or standards-based technique as a Candidate.
- Validate a Candidate on at least one representative fixture or real project before considering it Active.
- Require an explicit scope, exclusions, primary sources, review date, and known limitations.
- Require repeated cross-project evidence before promoting anything into the universal workflow.
- Add a mechanical check only after reviewing realistic false positives and escape cases.
- Supersede stale guidance; do not silently rewrite its history.

## Candidate Packs

- [ ] Web application accessibility and semantic-browser testing.
- [ ] Authentication and authorization boundary matrices.
- [ ] Payment, refund, and idempotency testing with qualified domain review.
- [ ] LLM evaluation, nondeterminism, tool-use, and safety boundaries.
- [ ] Local-first synchronization, interruption, migration, and recovery.
- [ ] Background jobs and durable workflow replay/recovery testing.
- [ ] Mobile device, offline, permission, and lifecycle testing.

## Evaluation Work

- [ ] Apply AutoQA to at least three constitution-governed products with different stacks.
- [ ] Record tests the agent initially omitted, trivial tests rejected, false-positive gates, and human checklist confusion.
- [ ] Measure whether a fresh agent can reconstruct the QA state without chat history.
- [ ] Forward-test skill triggering, plan quality, anti-shortcut behavior, and human handoff.
- [ ] Review best-practice pack staleness at least twice a year.

## Keep Outside the Core

- Exact framework or dependency versions.
- Universal vendor recommendations.
- Claims of regulatory or legal compliance.
- Product-specific business rules.
- Visual approval delegated to an automated agent.
- Arbitrary minimum test counts or universal code-coverage thresholds.
