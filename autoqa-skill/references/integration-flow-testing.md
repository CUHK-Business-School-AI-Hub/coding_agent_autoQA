# Integration Flow Testing

Use this reference after module cases are designed and a vertical feature slice exists.

## Build the Flow Catalog

Derive flows from product language, not routes or screens alone:

- Main success journey.
- Alternate valid journeys.
- Business rejection journeys.
- Dependency or recovery journeys.
- Approval, retry, cancellation, expiration, or compensation paths.

Define `every possible flow` as every named variant in the approved catalog. Keep the catalog finite by modeling meaningful business decisions and state transitions, not every permutation of harmless data.

## Choose Scriptable Interfaces

Prefer the interface closest to the real system boundary that avoids human visual judgment:

- HTTP request sequences.
- CLI commands.
- Event publish/consume scripts.
- File import/export.
- Background-job triggers.
- Domain adapters with a real database.

For a GUI-only product, add a test adapter or semantic browser automation when necessary, but keep visual and usability judgment in the human checklist.

## Environment Rules

- Use an isolated database or namespace.
- Create deterministic data per flow.
- Freeze time or random seeds when relevant.
- Never use production data or credentials.
- Clean up after each flow or recreate the environment.
- Use real internal modules and persistence unless the test goal explicitly isolates one integration.
- Fake external systems only at documented contracts and include failure behavior.

## Assertions

Assert the outcome a business stakeholder cares about:

- Final state and ownership.
- Durable records and totals.
- Events or notifications promised by the contract.
- Absence of forbidden side effects.
- Retry, idempotency, compensation, or recovery results.
- Security and privacy boundaries.

Avoid treating `200 OK`, page navigation, or process exit zero as sufficient when the business result can still be wrong.

## Avoid Duplication

Keep exhaustive boundary combinations in module tests. Integration flows should prove that real components honor representative business journeys and key failures. When a flow failure reveals a module edge case, add the narrow regression test first, then retain a focused flow assertion if the cross-module behavior matters.

