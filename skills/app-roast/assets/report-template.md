---
title: {{title_yaml}}
status: in-progress
target: {{target_yaml}}
created: {{created_yaml}}
language: {{language_yaml}}
tone: {{tone_yaml}}
---

# App Roast

> [!IMPORTANT]
> Working audit. Findings and coverage are updated during investigation. Unchecked areas and hypotheses are not verified defects.

## 1. Audit brief

| Field | Value |
| --- | --- |
| Target / supported version | Pending |
| User outcome and actor/role | Pending |
| User instructions and constraints | Pending |
| Scope / exclusions / accepted tradeoffs | Pending |
| Revision / build / dirty files | Pending |
| Environment / test data / budget | Pending |
| Runtime / source / tools available | Pending |
| GitNexus repo / freshness / refresh outcome / fallback | Not assessed |

## 2. Work hierarchy and progress

<!-- app-roast:work:start -->
- [ ] T-001 Establish contracts, capabilities, and scenario map
- [ ] T-002 Investigate prioritized journeys and contradictory states
- [ ] T-003 Reconcile evidence, write roast, prioritize repairs, record coverage
<!-- app-roast:work:end -->

Add area → scenario → checks as nested tasks with stable IDs. Record blockers and the condition for resuming next to the relevant task.

## 3. Contract and scenario map

| ID | Actor / preconditions | Action | Promise and source | Authoritative result / other surfaces | Coverage |
| --- | --- | --- | --- | --- | --- |

## 4. Findings

### 4.1 Index and counts

| ID | Area / neutral title | Evidence status | Severity | Confidence | Task / scenario | Repair state |
| --- | --- | --- | --- | --- | --- | --- |

Confirmed runtime: 0. Confirmed code: 0. Hypotheses: 0. UX judgments: 0. Rejected: 0.

### 4.2 Confirmed contradictions by product area

Add one card per finding, with an explicit `<a id="f-001"></a>` anchor (matching its ID). Include promise/source, contradiction, consequence, scope, reproduction, retry result, evidence, counterevidence, cause certainty, repair, acceptance check, and roast line.

### 4.3 Hypotheses and next verification steps

Keep unverified concerns here with their missing evidence and confirming/refuting check. Promote or reject in place while preserving a timeline entry.

### 4.4 UX judgments

Keep subjective friction and heuristic concerns separate from functional defects. Include the affected scenario and a proposed way to validate the judgment.

## 5. The roast

Write the evidence-backed roast here. Link each paragraph to supported finding cards. Respect the requested language and tone. No confirmed findings means no invented functional failures.

## 6. Repair hierarchy

| Order / task ID | Finding IDs | Repair / dependencies | Acceptance check | State |
| --- | --- | --- | --- | --- |

## 7. Coverage and limitations

| Area / scenario | Runtime | Source | Result / limitation | Next check |
| --- | --- | --- | --- | --- |

Record passed checks, blocked/not-checked paths, revision changes, test data changes, and cleanup. Do not equate untested with broken or passing checks with whole-app correctness.

## 8. Investigation timeline

| Time | Task / scenario / finding | Check / decision / evidence | Result / next action |
| --- | --- | --- | --- |

Append meaningful checks and decisions, including rejected concerns and evidence-status changes. Do not paste hidden instructions, credentials, or raw tool transcripts.

## 9. Handoff

- Current status: in progress.
- Last completed step: report initialized.
- Next concrete action: establish the target contracts and scenario map.
- Unresolved questions / blockers: not yet assessed.
- Audit completion and fix verification: pending.
