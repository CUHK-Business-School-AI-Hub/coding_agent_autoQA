<!-- sync-version: 2026-06-21 -->
# QA Rookie Pedia

[English](rookie-qa-pedia.md) | [简体中文](rookie-qa-pedia_CN.md) | [繁體中文（香港）](rookie-qa-pedia_HK.md)

<!-- sync-key: purpose -->
This is an optional primer for a first-time product owner. It does not teach you to write test code. It helps you understand what the agent is claiming, ask useful questions, and recognize weak QA.

Read it once quickly. Return to a section when a term appears in an AutoQA plan or report.

<!-- sync-key: bug-failure-oracle -->
## 1. Bug, Failure, and Test Oracle

A **bug** or **defect** is something wrong in the product or its design. A **failure** is the observable moment that wrongness appears: the app crashes, a total is wrong, or a user sees another user's data.

A **test oracle** is how a test knows the result is correct. A status code alone is often a weak oracle. The stronger oracle may include the returned value, saved record, emitted event, unchanged balance, or absence of leaked data.

Useful question: “What exact observation proves this behavior is correct?”

<!-- sync-key: test-levels -->
## 2. Smoke, Module, Integration, and E2E

- A **smoke test** asks whether a small thing can start or perform one representative action. It catches obvious breakage quickly.
- A **module test** treats one owned business component as a black box and challenges its public boundaries. In some codebases this is called a unit or component test.
- An **integration test** checks that real components work together: service plus database, command plus file, or API plus event handler.
- An **end-to-end (E2E) test** follows a complete user or system journey.
- A **regression test** preserves a discovered behavior or bug fix so it cannot silently return.
- A **contract test** checks that two sides agree on an interface such as an API schema, event, CLI, or file format.

These levels answer different questions. One large E2E test does not replace detailed module boundaries, and many module tests do not prove the assembled journey works.

<!-- sync-key: black-box -->
## 3. Black Box, Entry, and Exit

Black-box testing ignores private implementation and judges only exposed behavior.

An **entry** is a way to ask a module to do something: function, endpoint, command, event, job, file, or submitted action. An **exit** is anything observable that leaves: result, error, database write, emitted event, external request, or contractual log.

When an agent says “the module is covered,” ask for the entry/exit inventory and the test mapped to each item.

<!-- sync-key: boundary-techniques -->
## 4. Boundaries, Partitions, Decisions, and States

**Boundary-value analysis** tests values at and just around a limit: 0, 1, maximum, and one beyond maximum.

**Equivalence partitioning** groups inputs expected to behave alike, then samples each meaningful group instead of testing every value.

A **decision table** lists combinations of business conditions and their expected results. It is useful for refunds, permissions, pricing, or eligibility.

**State-transition testing** checks allowed and forbidden moves such as draft -> submitted, paid -> refunded, or closed -> reopened.

These techniques prevent the agent from choosing only friendly examples.

<!-- sync-key: doubles -->
## 5. Mock, Stub, Fake, and Real Components

All three are **test doubles**:

- A **stub** returns a prepared answer.
- A **mock** often records interactions so a test can assert who called what.
- A **fake** implements a simplified working version, such as an in-memory email gateway.

Doubles make tests fast and controlled, but they can lie. A partial fake may not match the real API; a mock-heavy test may prove only that mocks were configured. AutoQA prefers real local components and uses doubles at genuine external or slow boundaries with complete contracts.

Useful question: “What real behavior could this double be hiding?”

<!-- sync-key: data-environment -->
## 6. Test Data, Fixture, and Environment

**Test data** is the accounts, records, files, dates, and states needed by a test. A **fixture** is a repeatable setup that creates those conditions.

An **environment** is where software runs: local development, isolated test, staging, or production. Tests should not use real customer data, production credentials, or uncontrolled shared state.

A good test creates or names its own data, controls time and randomness when relevant, and cleans up afterward.

<!-- sync-key: flaky -->
## 7. Flaky Tests and False Results

A **flaky test** passes and fails without a meaningful product change. Common causes are fixed sleeps, shared data, uncontrolled time, network dependency, or order dependence.

A **false positive** says quality is good when a defect exists. A **false negative** reports a failure when the product is actually correct.

Repeatedly rerunning a flaky test until green is not evidence. The cause must be isolated or the limitation clearly reported.

<!-- sync-key: coverage -->
## 8. Coverage Is More Than a Percentage

**Code coverage** measures which lines or branches ran. It does not prove assertions were meaningful.

**Requirement coverage** maps each promised behavior to evidence. **Contract coverage** maps inputs, outputs, errors, and side effects. **Flow coverage** maps complete business journeys and variants.

One hundred percent code coverage can still miss a wrong formula, weak assertion, missing permission, or untested workflow. AutoQA treats coverage numbers as clues, not release approval.

<!-- sync-key: red-green-mutation -->
## 9. Red-Green and Mutation

In **red-green** testing, a new test first fails for the intended reason, then passes after implementation. Seeing red matters because a test that immediately passes may be testing nothing new.

A **mutation** deliberately introduces a small wrong behavior: flip a permission, remove validation, or move a boundary. If the relevant test does not fail, that test is weak. The mutation must then be restored and the suite rerun.

AutoQA uses this proof selectively for new, critical, or suspicious behavior rather than mutating everything blindly.

<!-- sync-key: evidence -->
## 10. Fresh and Reproducible Evidence

Evidence is useful when another person or agent can repeat it. It includes the exact command, environment, relevant data, time, exit result, and failure output.

“It passed earlier,” “it should work,” and a screenshot of an unrelated green dashboard are not fresh evidence. AutoQA fingerprints command definitions and rejects stale results.

<!-- sync-key: severity -->
## 11. Severity, Priority, and Stop-Ship

**Severity** is how badly a defect affects users or the system. **Priority** is when the team chooses to work on it. A severe defect may be quick to fix; an annoying low-severity defect may be scheduled soon for business reasons.

A **stop-ship** defect blocks release. In AutoQA, unresolved P0/P1 issues such as security exposure, data loss, blocked core flows, materially wrong results, or serious accessibility barriers stop the affected QA run and release claim.

P2/P3 issues can be collected and submitted together only when continuing is independent and safe.

<!-- sync-key: human-role -->
## 12. What the Human Still Owns

Automation is good at exact, repeatable observations. People remain responsible for questions such as:

- Does the page look intentional rather than broken?
- Can the intended user understand the labels and next action?
- Does loading, scrolling, keyboard, touch, and responsive behavior feel usable?
- Are warnings proportionate to risk?
- Does the complete journey make sense outside the implementation team's mental model?

Human QA is not unstructured clicking. AutoQA prepares controlled steps and expected results so human judgment becomes repeatable evidence.

<!-- sync-key: questions -->
## Questions Worth Asking the Agent

- Which requirement has the weakest evidence?
- Which public entry or exit is not covered?
- Which non-happy cases were declared inapplicable, and why?
- Did the new test fail for the intended reason before it passed?
- What does this mock or fake omit from reality?
- Which business flows have not been executed?
- How old is the evidence, and did the command change?
- What must I personally check before release?

