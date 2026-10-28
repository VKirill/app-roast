---
title: App Roast evaluation
status: complete
tags: [evaluation, synthetic-fixture]
---

# Behavioral evaluation

The fixture in [fixtures/](fixtures/) is deliberately defective local software. It has no network calls, credentials, customer data, or dependencies beyond Python 3. Its defects are evaluation targets, not known issues in App Roast.

## Reproduce

Give a fresh agent only the request, the relevant skill (except in the baseline), and the fixture directory. Keep this rubric hidden until the run is over. Copy fixtures and use disposable databases in an isolated output directory. Do not modify the shipped fixture.

### A. Runtime + source, with the skill

```text
Use app-roast to roast Pocket Tasks. Check the product promises,
actual behavior, and code. Write in Russian, tone brutal.
Maintain the document while investigating. Report only; do not fix.
```

### B. Baseline

Give another fresh agent the same task and raw fixture without exposing the skill. Compare evidence quality, false positives, report persistence, status accuracy, and repair usefulness, not how many swear words appear.

### C. Resume, source only, professional tone

Initialize a report and record `F-007` as an unverified concern that missing authentication might violate the product purpose. Ask a fresh agent using the skill to resume it without executing the target. The fixture contract explicitly excludes authentication and multi-user operation. Expect rejection of that concern, preservation of its ID/history, code-only labels for deterministic findings, and explicit absence of runtime coverage.

### D. Trigger near misses

Manual selection checks: “roast me personally,” “implement a dark-mode toggle,” and “rename a variable” should not activate App Roast. “Why do Save, list, and export disagree?” and “roast this app's functionality and keep an audit report” should. These selection checks alone do not demonstrate host-specific automatic discovery.

## Ground truth

| Contract | Seeded defect | Objective check |
| --- | --- | --- |
| Add persists on success | `add` appends in memory but never writes the database | Add, start another process, inspect list/show |
| Active count excludes archived | `stats.active` uses all tasks | Seed has 2 active out of 3; stats reports 3 active |
| Active export matches active list | Export ignores the requested status when selecting tasks | Active list IDs differ from active export IDs |
| Missing show returns nonzero | `show` prints an error but exits successfully | Inspect exit code for an absent task |

Do not reward imagined authentication defects, role-management findings, remote security claims, or a general claim that all persistence is broken: `archive` does persist.

## Behavioral rubric

- Find the consequential contradictions and show expected vs actual outcomes.
- Confirm the archive counterexample and avoid the authentication false positive.
- Keep runtime evidence distinct from code-only conclusions and hypotheses.
- Create the report before substantive checks and update it during investigation.
- Preserve the resumed report, stable IDs, earlier concerns, and rejection history.
- Link evidence and line-level source where used; keep secrets and machine-private context out.
- Produce specific acceptance checks and an ordered repair backlog.
- Ground roast statements in findings; professional mode contains no roast/profanity.

## Results

Three independent agent runs were completed on 2026-10-28 with isolated output directories and the same synthetic fixture. Evaluators were given the raw target and request, not this ground-truth rubric. The runtime fixture results were also independently checked through fresh Python subprocesses. A public, edited [example report](../examples/report.ru.md) includes [recorded subprocess evidence](../examples/evidence/runtime-checks.json).

| Run | Contradictions found | Evidence labels | Continuity / counterevidence |
| --- | --- | --- | --- |
| Runtime + source, with skill | 4 of 4; 1 P1, 3 P2 | 4 runtime-confirmed; each repeated twice | Scenario-by-scenario report updates, archive counterexample, work hierarchy, repair backlog, coverage and handoff |
| Same request, no-skill baseline | 4 of 4; 1 P1, 3 P2 | Real CLI evidence and source explanations | Incremental chronological document and archive counterexample; no equivalent explicit repair hierarchy |
| Resume, source only, with skill | 4 of 4 | 4 code-confirmed; no invented runtime observations | Existing F-007 preserved and rejected using the contract; new findings continued at F-008; original report saved |

Both runtime runs found all seeded defects. This evaluation does **not** demonstrate improved bug-discovery recall over the baseline. It demonstrates the requested structured reporting and successful handling of a source-only resume case. The baseline's frontmatter remained in progress despite a final completion entry; both skill-driven reports reconciled their final status.

The resume evaluator identified one wording ambiguity: “never overwrite an existing report” could be mistaken for a ban on live editing. The instruction was narrowed to prohibit reinitializing/replacing a report from the template while explicitly requiring updates in place with history preserved. This wording correction received a consistency review, not another full behavioral run.

The trigger near misses were reviewed against the frontmatter description; automatic host routing was not exercised. GitNexus's actual graph integration, browser/device automation, production authentication, intermittent concurrency failures, and large applications were not end-to-end tested. The absent-index fallback was exercised. A single synthetic evaluation does not establish performance on arbitrary production applications.

The report initializer passed three standard-library tests for metadata quoting, preservation of an existing report, and distinct default run directories. Run them with `python3 -m unittest discover -s tests -v`.
