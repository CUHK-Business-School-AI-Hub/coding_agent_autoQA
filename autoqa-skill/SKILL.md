---
name: autoqa-skill
description: Plan, implement, execute, and hand off evidence-driven software QA for projects governed by constitution-skill or equivalent repo-native specifications. Use when creating features or fixing bugs file by file, designing business-facing black-box module tests, proving contract boundaries, running integration flows without relying on GUI judgment, preparing non-technical human E2E checklists, triaging QA failures, auditing test adequacy, or deciding whether software is ready to release. Also use when asked for smoke tests, unit or module tests, integration tests, regression tests, QA plans, test matrices, test evidence, or human acceptance testing. Pair with SPEC.md, ARCH.md, RULES.md, CONTRACTS/, and TASKS/ when present; work in standalone discovery mode when they are absent.
---

# AutoQA

## Purpose

Turn product intent and software contracts into reproducible evidence. Treat quality as a proof obligation, not a confidence statement or a code-coverage percentage.

Use this role split:

- Let the agent own text-readable contracts, test design, test code, commands, fixtures, result interpretation, and defect reproduction.
- Let the human own visual correctness, usability, comprehensibility, device feel, and final risk acceptance.
- Automate semantic GUI checks only when useful; never claim that DOM assertions or screenshots replace human visual judgment.

Keep these obligations fixed while adapting frameworks and tools to the repository:

1. Trace every test to a business rule, contract, risk, or regression.
2. Inventory every exposed module entry and exit before claiming module coverage.
3. Prove new tests can fail for the intended reason.
4. Execute every named business-flow variant at least once.
5. Require fresh command evidence before automated completion claims.
6. Require human completion of the E2E checklist before release claims.
7. Stop for open P0 or P1 defects; report P2 and P3 defects explicitly.

## Workflow

### 1. Discover the project truth

Read existing project instructions and testing conventions first. Then locate, in this order:

- `docs/SPEC.md` or `SPEC.md`
- `docs/ARCH.md` or `ARCH.md`
- `docs/RULES.md` or `RULES.md`
- `docs/CONTRACTS/` or `CONTRACTS/`
- the active file under `docs/TASKS/` or `TASKS/`
- `AGENTS.md`, `CLAUDE.md`, and scoped agent rules
- existing tests, test configuration, CI commands, schemas, and public interfaces

Read `references/constitution-integration.md` when constitution assets exist. In standalone mode, label inferred modules, contracts, and workflows as assumptions and ask the human only about ambiguity that changes risk or expected behavior.

### 2. Resolve test-design knowledge

Before designing tests, read `references/best-practice-registry.md` and follow `references/research-and-best-practice.md`.

Use this precedence:

1. Project contracts and acceptance criteria.
2. Applicable, Active, and current bundled best-practice packs.
3. Current official documentation, formal standards, and primary sources found online.
4. Stable general testing knowledge, with assumptions made explicit.

Do not silently use a stale practice pack. Do not search merely to decorate a routine test plan. Research unfamiliar frameworks, uncommon risks, regulated behavior, concurrency, time, retries, security, money, destructive actions, third-party protocols, or any test design whose correctness is uncertain.

### 3. Create the QA control plane

Create these project artifacts from the templates under `assets/templates/`:

- `docs/QA/QA-PLAN.md`: scope, risks, selected practices, environments, and responsibilities.
- `docs/QA/QA-MATRIX.md`: human-readable traceability across requirements, modules, flows, and tests.
- `docs/QA/qa-manifest.json`: machine-checkable entries, exits, cases, flows, commands, human checks, and defects.
- `docs/QA/HUMAN-E2E.md`: localized checklist for the human.

Use the user's preferred language for human-facing project documents. Keep IDs, commands, schema keys, and file paths in English so evidence remains portable.

Run the planning gate before implementation:

```bash
python3 <autoqa-skill>/scripts/check_qa.py --root <project-root> --phase plan
```

### 4. Pass the file smoke gate

After creating or materially changing each executable source file:

1. Run the narrowest syntax, type, import, compile, or startup check that can detect a broken file.
2. Add a small business-observable smoke test when the file has behavior of its own.
3. Record declarative-only files as `declarative` and state the compiler, schema validator, or consuming test that covers them.
4. Stop and repair a failing file gate before stacking more production changes on top.

Do not create meaningless one-assertion tests for type declarations, constants, generated files, or passive schemas. Record a justified coverage mechanism instead.

### 5. Pass the module black-box gate

Treat each architecture module as a black box. Read `references/business-boundary-testing.md` before planning or auditing module cases.

For every exposed module:

- List all entries: functions, endpoints, commands, events, jobs, files, or UI-submitted actions.
- List all exits: return values, errors, writes, emitted events, logs with contractual meaning, and external calls.
- Select applicable case classes from happy, negative, boundary, state, permission, dependency, idempotency, concurrency, and recovery.
- Cover every listed entry and exit with at least one business-named case.
- Assert observable results and side effects, not private call structure.
- Record why any normally expected class is not applicable.

Reject a minimal penetration test that only proves one request reaches one response. For new behavior, observe the test fail correctly before implementation. For pre-existing behavior, use a controlled mutation, fault injection, or remove-and-restore challenge on critical cases to prove the suite can detect a wrong implementation.

### 6. Pass the feature integration gate

Read `references/integration-flow-testing.md`. Derive named happy, alternate, and failure flows from SPEC workflows, acceptance criteria, state transitions, and task requirements.

- Execute every named flow variant at least once through scriptable interfaces such as HTTP, CLI, events, database fixtures, or domain adapters.
- Prefer real internal components and realistic persistence.
- Replace external systems only at their contract boundary with complete, contract-valid fakes.
- Control time, randomness, and external instability explicitly.
- Keep flows independent and clean up their data.
- Record exact commands and fresh evidence.

Do not use integration tests to exhaustively repeat module edge cases. Do not omit alternate and failure flows merely because the happy path passes.

### 7. Run the automated completion gate

Define commands as argument arrays in `qa-manifest.json`; never hide required checks in prose. Execute and validate them with:

```bash
python3 <autoqa-skill>/scripts/check_qa.py --root <project-root> --phase automated --run
```

The script writes local evidence under `.autoqa/evidence/`. Do not claim automated QA is complete when evidence is missing, stale, mismatched to the current command, or nonzero.

Test counts and code coverage are diagnostic signals. They do not replace entry/exit coverage, flow coverage, or proof that tests catch faults.

### 8. Hand off human E2E

Read `references/human-e2e-and-triage.md`. Prepare the environment and test data before asking the human to start. Give numbered steps, plain-language expected results, evidence requests, and a failure severity for every check.

When the human reports a failure:

- Stop immediately for P0 or P1. Reproduce, add an automated regression test when possible, fix, rerun impacted automated gates, and tell the human which earlier checks must be repeated.
- Record P2 or P3, continue the checklist when safe, then submit those defects together after the run.
- Escalate uncertain severity conservatively. Never downgrade a defect to keep the checklist moving.

### 9. Run the release gate

After the human finishes, update human check statuses and defects in `qa-manifest.json`, then run:

```bash
python3 <autoqa-skill>/scripts/check_qa.py --root <project-root> --phase release
```

Release requires current automated evidence, all human checks passed, and no open P0 or P1 defects. Report open P2/P3 defects as residual risk even when the gate exits successfully.

## Defect-Fix Loop

For every defect:

1. Reproduce it with the smallest reliable automated or human procedure.
2. Map it to the violated requirement, contract, boundary, or flow.
3. Add a failing regression test when the behavior is machine-observable.
4. Fix the root cause, not the symptom or the test.
5. Rerun the narrow test, affected module tests, affected flows, and required project checks.
6. Update the matrix, evidence, defect status, and human retest instructions.

## Completion Contract

Before saying QA is complete, verify all of the following:

- The QA plan cites its governance sources and selected current practices.
- Every changed executable file has a file-gate record.
- Every module entry and exit is covered or explicitly out of scope.
- Every applicable case class is represented.
- Every named business-flow variant passed with current evidence.
- Tests demonstrate fault sensitivity for new or critical behavior.
- Human E2E is complete for release claims.
- No P0 or P1 defect remains open.
- P2/P3 residual defects and untested risks are visible to the human.

If any item is false, state the actual status and the missing proof. Never replace evidence with `should`, `probably`, or agent confidence.

## Reference Map

- `references/constitution-integration.md`: translate constitution assets into QA inputs and outputs.
- `references/qa-gates.md`: detailed gate criteria, evidence rules, and anti-shortcut checks.
- `references/business-boundary-testing.md`: design business-facing black-box module cases.
- `references/integration-flow-testing.md`: build script-driven feature-flow tests.
- `references/human-e2e-and-triage.md`: prepare human QA and classify failures.
- `references/research-and-best-practice.md`: decide when and how to research current practice.
- `references/best-practice-registry.md`: discover bundled practice packs and staleness.
- `references/rookie-qa-pedia.md`: optional English primer for first-time product builders; Chinese variants sit beside it.

## Skill Maintenance

Keep universal obligations in this file. Add technology or domain advice as a versioned reference pack, not as a new universal rule. Promote a lesson into the core only after cross-project evidence shows that it is stable and mechanically useful. Use `assets/templates/BEST-PRACTICE-PACK.md` for candidates and the repository-level `TODO_BEST_PRACTICE_EVOLUTION.md` for unproven ideas.

