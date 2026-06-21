# Research and Best-Practice Resolution

Use this reference before planning tests for an unfamiliar or high-risk surface.

## Resolution Order

1. Read project contracts and existing testing rules.
2. Inspect `best-practice-registry.md` for an applicable Active pack.
3. Check the pack's scope, exclusions, sources, `Last Reviewed`, and `Review By`.
4. If no current pack applies, research current primary material online.
5. Use stable general testing knowledge only after current sources, and label assumptions.

## Research Triggers

Research rather than guess when any of these apply:

- The framework or test tool is unfamiliar or recently changed.
- Authentication, authorization, payments, money, privacy, destructive actions, or regulated data are involved.
- Behavior depends on time, concurrency, retries, idempotency, ordering, recovery, or distributed systems.
- A third-party API, protocol, file format, browser behavior, or platform rule is central to the test.
- A test technique or oracle is not routine and simple.
- There is a meaningful chance that remembered advice is stale.

## Source Quality

Prefer:

1. Formal standards and specifications.
2. Official framework, browser, platform, or provider documentation.
3. Primary research or maintainers' engineering guidance.
4. Reputable secondary engineering references when primary material is insufficient.

For technical claims, do not rely on search snippets, content farms, or unattributed examples. Record the URL, date reviewed, applicability, and decision in `QA-PLAN.md` and `qa-manifest.json`.

## Promotion Lifecycle

- `Candidate`: promising guidance with primary sources, not yet shipped as a default.
- `Active`: current, scoped guidance validated on a representative fixture or real case.
- `Superseded`: retained for history and linked to its replacement.

Promote a practice into the universal core only after it succeeds across independent products or stacks and remains valid without a vendor-specific assumption. Promote a mechanically checkable stable rule into `check_qa.py` only when false positives are understood.

Do not label a domain pack an industry best practice without qualified review, explicit jurisdiction where relevant, primary sources, and a review date.

