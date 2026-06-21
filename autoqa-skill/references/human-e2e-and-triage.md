# Human E2E and Triage

Use this reference to prepare a non-technical person for release QA.

## Prepare the Human

Before handoff:

- Start the correct environment and verify its version.
- Seed named test accounts and data without real personal information.
- State the browser, device, role, and starting page.
- Explain how to reset or recover the test state.
- Separate one check per numbered item.
- Give a plain-language expected result and evidence request.
- Predetermine severity if that result fails.

Do not ask the human to inspect logs, run developer tools, infer API behavior, or decide whether a technical error is acceptable.

## Human-Owned Questions

- Does the interface look complete and intentional?
- Can the intended user understand what to do next?
- Are copy, labels, errors, and confirmations clear?
- Does keyboard, touch, scrolling, focus, and responsive layout feel usable?
- Are loading and progress states understandable?
- Is sensitive or destructive behavior communicated honestly?
- Does the complete real-world journey make sense?

## Severity and Action

| Severity | Meaning | Action during checklist |
| --- | --- | --- |
| P0 | Security/privacy breach, data loss/corruption, unsafe or uncontrolled irreversible action | Stop immediately; do not continue in that environment |
| P1 | App cannot start, core flow blocked, materially wrong business result, serious accessibility barrier, contract-breaking behavior | Stop the affected run; fix before continuing affected checks |
| P2 | Non-core behavior incorrect or confusing with a safe workaround | Record evidence; continue when independent and safe |
| P3 | Cosmetic, copy, spacing, or low-impact polish issue | Record; finish the checklist |

Severity measures impact, not difficulty to fix. When uncertain between two levels, use the higher level until triage proves otherwise.

## Fix and Retest

For P0/P1:

1. Preserve evidence and exact reproduction steps.
2. Reproduce through an agent-readable interface where possible.
3. Add a regression test.
4. Fix and rerun affected automated gates.
5. Tell the human exactly which failed and previously passed checks must be repeated.

For P2/P3, collect all independent issues, complete the safe remainder, then submit one organized defect batch with IDs, evidence, severity, and expected behavior.

The human may accept residual P2/P3 risk. The agent must never accept P0/P1 risk on the human's behalf.

