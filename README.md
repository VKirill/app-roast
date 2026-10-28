---
title: App Roast
tags: [agent-skill, product-audit, qa]
---

# App Roast

**Your app says “Saved.” Did it actually save?**

An agent skill that hunts contradictions between product promises, interface copy, runtime behavior, API contracts, and implementation. Every finding gets evidence, a consequence, a repair, and an acceptance check. Then the app gets roasted.

[Русский](README.ru.md) · [Skill instructions](skills/app-roast/SKILL.md) · [Example report](examples/report.ru.md) · [Evaluation](evals/README.md)

> [!IMPORTANT]
> The audit document is the primary output. The agent creates it before investigating and updates it as it works, so an interrupted session still leaves findings, evidence, coverage, and next actions.

## Install

With the [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add VKirill/app-roast --skill app-roast
```

Or copy `skills/app-roast/` into the skill directory supported by your agent, such as `.agents/skills/` or `.claude/skills/` inside your project. For a managed skill hub, publish the folder through that hub instead of creating duplicate machine copies.

The instructions are agent-independent Markdown. Your agent needs filesystem access to keep the report and suitable tools to inspect the target. Python 3 is optional for the bundled report initializer. No API key, browser package, or GitNexus installation is required by the skill itself. Invocation syntax and automatic discovery depend on your host.

## Use

Ask your agent to load `app-roast` and give it the target:

```text
Use app-roast on this repository and http://localhost:3000.
Focus on saving, filters, export, cancellation, and recovery after errors.
Maintain the audit document while working. Report only; do not fix yet.
```

For the original Russian experience:

```text
Используй app-roast. Прожарь работоспособность этого приложения.
Язык: русский. Тон: brutal, с матом.
Ищи противоречия между обещаниями интерфейса, поведением, API и кодом.
Веди документ по ходу проверки. Если GitNexus доступен — используй его.
```

To continue an interrupted run:

```text
Resume app-roast from app-roast/<run>/report.md.
Preserve finding IDs and earlier evidence. Continue the next unfinished task.
```

Set `tone: professional` for a neutral engineering report, `roast` for sharp sarcasm, or `brutal` for strong profanity. The report follows the user's language. Technical finding cards stay precise in every mode. Fixes happen only when the user's request also authorizes them.

## What it checks

| Contradiction | Example investigation |
| --- | --- |
| Promise vs behavior | Does Cancel stop the operation, or just close the dialog? |
| Success vs persistence | Does Saved survive a reload or restart? |
| Screen vs screen | Do list, detail, count, search, and export agree? |
| UI vs API | Do request/response shapes, units, defaults, and validation match? |
| Permission vs enforcement | Is the stated role restriction enforced on the active server path? |
| Error vs recovery | Can retry create duplicates or silently discard input? |
| Configuration vs execution | Is the setting read by the implementation actually used? |

Applicable to web, desktop, mobile, CLI, and API products. Runtime-only and source-only audits work too, with explicit coverage limits. Source-only proof is never presented as runtime reproduction.

## The live document

```tree
app-roast/<run>/
├── report.md              # Brief, work hierarchy, findings, roast, repair backlog
└── evidence/              # Sanitized logs, responses, screenshots, recordings
```

The report contains:

1. Audit brief: target, instructions, scope, version, environment, tools.
2. Work hierarchy: area → scenario → check, with progress and blockers.
3. Contract map: actor → action → promise → authoritative result.
4. Findings: stable IDs, proof, counterevidence, consequences, repair checks.
5. The roast: each punchline links to a supported finding.
6. Repair hierarchy: priorities, dependencies, and acceptance checks.
7. Coverage: passed, partial, blocked, and untested paths.
8. Timeline: discoveries, rejected concerns, and status changes.
9. Handoff: current state and the next concrete action.

`CONFIRMED-RUNTIME`, `CONFIRMED-CODE`, `HYPOTHESIS`, `UX-JUDGMENT`, and `REJECTED` are separate statuses. There is no bug quota, invented quality score, or requirement to produce insults when the evidence says the journey works.

## Optional GitNexus

When available, the agent checks the target index and uses exposed tools such as `query`, `context`, `trace`, `route_map`, and `shape_check` where relevant. Advanced tools vary by version. A graph mismatch is a lead; the agent must inspect the active implementation before treating it as a code-confirmed defect. A missing/stale index falls back to ordinary source search without blocking the audit. [Integration details](skills/app-roast/references/gitnexus.md).

## Development and limits

```sh
python3 -m unittest discover -s tests -v
```

The included synthetic fixture and behavioral evaluation rubric test contradiction discovery, evidence labels, incremental reporting, and false positives. See [evaluation notes](evals/README.md) for what has actually been exercised. This skill guides an agent; it is not a deterministic scanner and cannot establish complete application correctness.

MIT licensed. Original instructions; inspired by the general practices of exploratory testing, contract checking, and adversarial product review.
