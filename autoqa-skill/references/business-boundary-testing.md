# Business Boundary Testing

Use this reference to design black-box tests for an architecture module.

## Start With the Contract

Describe the module without reading private implementation details:

1. Who or what can enter it?
2. What data or state may enter?
3. What can leave: values, errors, writes, events, calls, or visible state?
4. What business invariants must always hold?
5. Which transitions are allowed or forbidden?
6. Which failures must be contained, retried, exposed, or compensated?

Add every entry and exit to `qa-manifest.json` before writing cases.

## Select Applicable Techniques

| Situation | Technique | Example |
| --- | --- | --- |
| Ranged or sized input | Boundary-value analysis | Minimum quantity, maximum quantity, just outside each |
| Many similar inputs | Equivalence partitioning | Valid email, malformed email, unsupported domain |
| Rules combine conditions | Decision table | Refund eligibility by payment state, age, and role |
| Behavior depends on lifecycle | State transition | Draft -> submitted allowed; paid -> draft forbidden |
| Large structured input space | Property-based testing | Serialization round-trip preserves valid records |
| Permissions or ownership | Actor-resource matrix | Owner, member, outsider, missing identity |
| Repeated commands | Idempotency testing | Same request key does not create a second charge |
| External dependency | Failure matrix | Timeout, unavailable, malformed response, duplicate callback |
| Time-sensitive behavior | Controlled-clock cases | Before, at, and after expiry |
| Concurrent behavior | Interleaving/invariant cases | Two reservations cannot consume one final unit |

Choose techniques because the contract needs them, not to fill a quota. Record a reason when a common class is inapplicable.

## Write Business Cases

Use names that remain meaningful after refactoring:

- Good: `closed invoice cannot accept another payment`.
- Bad: `paymentService throws`.
- Good: `guest cannot read another customer's address`.
- Bad: `controller returns 403`.

Each case must state:

- Given: relevant business state and actor.
- When: one entry is exercised.
- Then: observable exits and invariants.
- Because: requirement, contract clause, risk, or regression ID.

Assert both the visible response and important durable side effects. For a rejected payment, for example, assert the error, unchanged balance, no success event, and safe audit record when those are contractual.

## Use Doubles Carefully

- Prefer real pure collaborators and local persistence when fast and deterministic.
- Fake external systems at the narrowest owned boundary.
- Mirror complete request and response schemas.
- Do not assert on fake internals unless the outbound interaction is itself a contract.
- Run at least one integration or contract test against a realistic boundary when a fake could drift.

## Prove Test Quality

For critical rules, deliberately challenge the suite:

- Remove a validation branch.
- Flip an authorization decision.
- Change an inclusive boundary to exclusive.
- Skip a write or event.
- Return a malformed external payload.

The relevant test must fail for the intended reason. Restore the implementation immediately and rerun. Use a mutation tool when the repository already supports one; otherwise perform a narrowly controlled manual challenge and record it.

