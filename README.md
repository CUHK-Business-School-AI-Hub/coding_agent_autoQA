<!-- sync-version: 2026-06-21 -->
# Coding Agent AutoQA

[English](README.md) | [简体中文](README_CN.md) | [繁體中文（香港）](README_HK.md)

<!-- sync-key: promise -->
AutoQA is an evidence-driven quality-assurance skill for people building software with coding agents, especially people without a technical background. It pairs with [coding_agent_constitution](https://github.com/CUHK-Business-School-AI-Hub/coding_agent_constitution): constitution makes product intent, architecture, and contracts durable; AutoQA turns those assets into tests, executable business flows, fresh evidence, and a human-friendly release checklist.

AutoQA does not replace a test framework, a reviewer, or human judgment. It prevents a coding agent from treating its default test harness, one happy-path test, or a green coverage number as sufficient proof.

<!-- sync-key: mindset -->
## The QA Mindset

Feature development can explore many valid implementations. QA has less freedom because its job is to challenge the implementation, not admire it.

The tools may change, but the proof obligations do not:

- Start from business behavior and contracts, not from the code the agent happened to write.
- Name every exposed module entry and exit before claiming module coverage.
- Test rejection, boundary, state, permission, and dependency behavior when applicable.
- Prove important tests can detect a deliberately wrong implementation.
- Run every named business-flow variant and preserve fresh command evidence.
- Let a human judge visual quality, usability, clarity, and the complete real-world journey.
- Stop for security, privacy, data-loss, core-flow, or materially wrong-result failures.

QA is not pessimism. It is a disciplined way to replace “the agent seems confident” with “here is the evidence, here are the gaps, and here is the human decision.”

| Non-negotiable | Adaptable to the project |
| --- | --- |
| Requirement-to-test traceability | pytest, Vitest, JUnit, or another framework |
| Entry/exit and business-boundary coverage | Test-file layout and naming convention |
| Fresh executable evidence | Exact command organization |
| Human ownership of visual and usability judgment | Browser, device, and checklist format |
| No unresolved P0/P1 at release | How P2/P3 work is scheduled |

<!-- sync-key: partnership -->
## How It Works With Constitution

```text
Product idea
   |
   v
constitution-skill
   SPEC -> user goals, workflows, acceptance criteria
   ARCH -> modules and ownership boundaries
   CONTRACTS -> inputs, outputs, errors, schemas, events
   RULES -> repository-specific safety and test rules
   TASKS -> small implementation slices
   |
   v
autoqa-skill
   QA plan -> what must be proven and why
   file gates -> fast feedback after each changed source file
   module cases -> black-box business boundaries
   integration flows -> complete script-driven journeys
   human E2E -> visual, usability, and release judgment
   |
   v
Evidence-backed release decision
```

AutoQA can work without constitution assets, but it must then infer requirements and label them as assumptions. The combination is stronger because the QA agent can design tests independently from durable product truth rather than reverse-engineering intent from implementation code.

<!-- sync-key: gates -->
## Why There Are Gates

A gate is a stopping condition, not a ceremony. Each gate catches a different class of mistake at the cheapest useful moment.

### Gate 0: QA planning

Before implementation, the agent maps requirements, risks, modules, entries, exits, flow variants, environments, commands, and human checks. This prevents tests from being biased toward the implementation that already exists.

### Gate 1: file smoke

After each changed executable file, the agent runs the narrowest useful parse, type, import, compile, startup, or business-smoke check. A passive schema or type file is covered by its validator or consumer instead of receiving a meaningless test.

Why: a broken file is easier to diagnose immediately than after five more files depend on it.

### Gate 2: module black box

Each architecture module is treated as a black box. Tests cover all exposed entries and exits plus applicable happy, rejection, boundary, state, permission, dependency, idempotency, concurrency, and recovery behavior.

Why: one request reaching one response proves connectivity, not business correctness.

### Gate 3: feature integration

Every named happy, alternate, and failure journey is executed through HTTP, CLI, events, files, jobs, or another scriptable interface. Internal components remain real where practical; external systems are replaced only at documented contracts.

Why: correct modules can still be connected incorrectly.

### Gate 4: human E2E

The agent prepares a plain-language checklist and test environment. A person follows the real journey and judges layout, copy, feedback, keyboard/touch behavior, responsiveness, clarity, and overall sense-making.

Why: an agent can read pixels and DOM state, but it cannot own the intended user's visual and experiential approval.

### Release gate

AutoQA accepts a release claim only when automated evidence is current, human checks are complete, and no P0/P1 defect remains unresolved. Open P2/P3 issues remain visible as residual risk.

<!-- sync-key: quick-start -->
## Quick Start for a Non-Technical Owner

### 1. Install or expose the skill

Place the `autoqa-skill/` folder in the skill directory supported by your coding harness, or give the agent the folder path directly. Typical installations are:

```bash
# Codex personal skill
mkdir -p ~/.codex/skills
cp -R autoqa-skill ~/.codex/skills/autoqa-skill

# Cursor project skill
mkdir -p .cursor/skills
cp -R autoqa-skill .cursor/skills/autoqa-skill

# Claude Code project skill
mkdir -p .claude/skills
cp -R autoqa-skill .claude/skills/autoqa-skill
```

Restart or open a fresh agent session after installation. Harness conventions can evolve, so use its current documentation if it does not discover the skill.

### 2. Build with constitution and AutoQA together

Start with a prompt like:

```text
Use constitution-skill to define this product and split the next feature into a bounded task.
Then use autoqa-skill to create the QA plan before implementation, run the file and
module gates while coding, and prepare the human E2E checklist when the feature is ready.
Explain any decision I need to make in non-technical language.
```

### 3. Ask for the actual evidence

Useful prompts include:

```text
Show me which business requirements still have no test.
```

```text
Audit this module as a black box. List every entry, exit, applicable boundary,
and the test that proves it.
```

```text
Run the automated AutoQA gate and tell me what passed, what failed, and what remains untested.
```

```text
Prepare the human E2E guide in Simplified Chinese. Stop me immediately if I find a P0 or P1 issue.
```

### 4. Do the human part

Open `docs/QA/HUMAN-E2E.md` and follow it step by step. You do not need to inspect code or logs. Record what happened, attach the requested evidence, and give the check ID back to the agent when something fails.

For unfamiliar words, use the optional [QA Rookie Pedia](autoqa-skill/references/rookie-qa-pedia.md).

<!-- sync-key: artifacts -->
## What AutoQA Adds to a Project

| Artifact | Audience | Purpose |
| --- | --- | --- |
| `docs/QA/QA-PLAN.md` | Human and agent | Scope, risks, sources, environments, and exit rules |
| `docs/QA/QA-MATRIX.md` | Human and reviewer | Readable trace from requirements to tests and evidence |
| `docs/QA/qa-manifest.json` | Agent and validator | Machine-checkable boundaries, cases, flows, commands, checks, and defects |
| `docs/QA/HUMAN-E2E.md` | Non-technical human | Numbered visual and usability checklist |
| `.autoqa/evidence/latest.json` | Local validator | Fresh command results and command fingerprints; normally not committed |

Run the deterministic gates with:

```bash
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase plan
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase automated --run
python3 autoqa-skill/scripts/check_qa.py --root /path/to/project --phase release
```

The command runner uses argument arrays rather than shell strings. Evidence becomes invalid when a command changes or grows older than the configured limit.

<!-- sync-key: defects -->
## What To Do When QA Fails

| Severity | Typical examples | What happens next |
| --- | --- | --- |
| P0 | Data loss, privacy/security breach, unsafe irreversible action | Stop immediately; do not continue in that environment |
| P1 | App cannot start, core journey blocked, materially wrong result, serious accessibility barrier | Stop the affected run; fix and retest before continuing |
| P2 | Non-core behavior is wrong or confusing but has a safe workaround | Record evidence; continue independent safe checks; submit together later |
| P3 | Cosmetic, copy, spacing, or low-impact polish problem | Record and finish the checklist |

Severity is about impact, not how easy the fix looks. After a blocking fix, the agent must say which automated tests and earlier human checks need to be repeated.

<!-- sync-key: best-practices -->
## Evolving Best Practices

AutoQA intentionally ships with an empty best-practice pack registry at first. Before planning tests, the agent checks that registry. If no current pack applies, it researches current official documentation, standards, and primary sources instead of relying only on remembered advice.

New practice packs move through `Candidate`, `Active`, and `Superseded` states. Each pack records scope, exclusions, sources, review dates, validation cases, and limitations. Unproven ideas live in `TODO_BEST_PRACTICE_EVOLUTION.md`; they are not silently treated as industry truth.

<!-- sync-key: languages -->
## Languages

English is canonical for `SKILL.md`, scripts, schema fields, IDs, and agent-facing technical references. README, the QA Rookie Pedia, and the human E2E template are maintained in English, Simplified Chinese, and Traditional Chinese for Hong Kong. `check_translations.py` checks version and section parity across these critical documents.

<!-- sync-key: influences -->
## Influences and License

AutoQA's evidence-before-claims, red-green testing, and anti-mock shortcuts are inspired by the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers). Its broader testing vocabulary also benefited from reviewing the MIT-licensed [wshobson/agents](https://github.com/wshobson/agents) and [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills).

This repository is licensed under the [MIT License](LICENSE).
