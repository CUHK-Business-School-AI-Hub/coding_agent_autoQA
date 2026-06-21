<!-- sync-version: 2026-06-21 -->
<!-- autoqa:document:human-e2e -->
# Human E2E Guide

[English](HUMAN-E2E.md) | [简体中文](HUMAN-E2E_CN.md) | [繁體中文（香港）](HUMAN-E2E_HK.md)

<!-- sync-key: purpose -->
This checklist is for visual correctness, usability, clarity, and complete real-world journeys. The agent prepares the environment and handles command-based checks; the human records what the product actually feels like to use.

<!-- autoqa:section:instructions -->
<!-- sync-key: instructions -->
## Instructions

1. Follow the checks in order unless a check says it is independent.
2. Record `Pass`, `Fail`, or `Blocked`; do not silently skip a check.
3. Attach the requested screenshot or short note.
4. Stop immediately for a P0 or P1 result and send the check ID to the agent.
5. Record P2/P3 issues and continue only when the remaining checks are independent and safe.

<!-- autoqa:section:environment -->
<!-- sync-key: environment -->
## Environment

- Build or version:
- URL or application:
- Browser/device:
- Test account and role:
- Starting data:
- Reset instructions:

<!-- autoqa:section:checks -->
<!-- sync-key: checks -->
## Checks

### HUMAN-001: <plain-language journey or visual question>

- Preconditions:
- Steps:
  1.
- Expected result:
- Pay attention to:
- Evidence to attach:
- Severity if failed: `P0 | P1 | P2 | P3`
- Result: `Pending | Pass | Fail | Blocked`
- Notes:

<!-- autoqa:section:defects -->
<!-- sync-key: defects -->
## Defects Found

| Defect ID | Check ID | What happened | Expected | Severity | Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

<!-- autoqa:section:sign-off -->
<!-- sync-key: sign-off -->
## Human Sign-Off

- All checks completed:
- Open P0/P1 defects:
- Open P2/P3 defects accepted for this release:
- Untested devices, roles, or journeys:
- Decision: `Approve | Do not approve | Approve with recorded residual risk`
- Name/date:
