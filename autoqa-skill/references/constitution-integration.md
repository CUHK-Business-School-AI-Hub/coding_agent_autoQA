# Constitution Integration

Use this reference when `constitution-skill` governance assets are present.

## Input Mapping

| Constitution asset | Extract for QA | AutoQA output |
| --- | --- | --- |
| `SPEC.md` | Users, workflows, non-goals, acceptance criteria, risks | Flow catalog and requirement rows |
| `ARCH.md` | Module responsibilities, ownership, forbidden ownership, dependencies | Module black-box inventory |
| `RULES.md` | Required checks, data rules, security rails, approval requirements | Gate commands and risk constraints |
| `CONTRACTS/` | Inputs, outputs, errors, schemas, events, CLI/file formats | Entry/exit and boundary cases |
| `TASKS/*.md` | Current scope, touched files, acceptance criteria, verification | Incremental file gates and task-specific suite |
| `AGENTS.md` | Repository workflow and handoff rules | Agent operating constraints |

## Operating Sequence

1. Read the active task and every durable source it cites.
2. Add missing QA rows before writing production code.
3. Run a file gate after each changed executable file.
4. Complete module cases before declaring the bounded task implemented.
5. Complete feature flows when the task closes a vertical slice.
6. Feed durable discoveries back into governance in the same change:
   - Changed product behavior -> `SPEC.md`.
   - Changed module boundary -> `ARCH.md`.
   - Changed interface -> `CONTRACTS/`.
   - Repeated QA rule -> `RULES.md` or `AGENTS.md`.

Do not edit governance merely to make a test pass. Reconcile the disagreement with product intent.

## Modes

### Standard

Build the full QA control plane under `docs/QA/`. Cover all modules and business flows in the active release scope.

### Retrofit

Start at the next seam being changed. Characterize current behavior, identify contract drift, and cover only that module plus directly affected flows. Mark the rest of the system `out_of_scope` with a reason; do not imply repo-wide coverage.

### Minimal

Keep one compact plan and manifest, but do not relax evidence. A small project may have fewer modules and commands; it still needs file checks, business cases, fresh execution evidence, and human visual review when it has a GUI.

## Conflict Rules

- Project contracts outrank generic best practices.
- Explicit human product decisions outrank inferred acceptance criteria.
- Security, privacy, data-loss, and irreversible-operation risks require human confirmation.
- If code and contract disagree, report contract drift; do not silently choose code as truth.

