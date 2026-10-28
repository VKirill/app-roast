# Contradiction-driven investigation

Use these lenses to choose consequential checks, not as a mandatory list for every product. Prefer one fully traced broken journey to a catalog of untested opinions.

## Contradiction lenses

| Boundary | Probe | Verify against |
| --- | --- | --- |
| Promise → action | Does a label such as Save, Cancel, Delete, Retry, Private, or Export describe what actually happens? | Published contract and authoritative result |
| UI → API | Do methods, fields, status codes, pagination, units, nullability, and error formats agree? | Active consumer, adapter, actual handler/response |
| Optimistic UI → persistence | Does success survive reload, restart, reconnect, or another client? | Storage/read endpoint after the write completes |
| Screen → screen | Do details, list, search, totals, badges, and exports agree under the same filters and snapshot? | Same entity IDs, role, timezone, time, filters |
| Actor → authorization | Does the server enforce what the UI promises for this role/tenant? | Authorized test accounts, service checks, ownership predicates |
| Start → completion | Is queued/running distinguished from succeeded/failed? What happens after disconnect? | Job state machine and eventual authoritative result |
| Error → recovery | Can the user retry without duplicates, stale state, or losing input? | Error branches, retry semantics, idempotency |
| Cancel/undo → effects | Does cancellation stop effects, or merely hide the spinner? What is reversible? | Request lifecycle and committed effects |
| Defaults → validation | Can a valid-looking default be rejected? Do frontend/backend boundaries differ? | Parsing, units, limits, schemas, encoding |
| Configuration → active path | Does changing a setting affect the implementation actually used? | Configuration read sites, flags, environment, invocation |
| Docs/tests → implementation | Do promised guarantees exist on the supported path? Can tests pass while skipping the guarantee? | Actual assertions, wiring, current revision |
| Device/lifecycle → continuity | Does back navigation, rotation, offline mode, expiry, or app resume corrupt state? | Applicable platform behavior and state restoration |

## Small adversarial moves

Choose realistic boundaries: zero/one/many items, empty/invalid/long input, duplicate action, slow/failing request, role change, pagination boundary, date/time boundary, refresh after success, interruption before completion. Build a minimal state and vary one factor at a time.

For filtered results, compare lists and counters under the same contract: a documented global count beside a filtered list is not automatically a bug. For eventual consistency, test the documented completion/consistency boundary rather than declaring an immediate stale read a permanent loss. For role checks, a hidden control does not prove the server lacks authorization; inspect or exercise the server path within authorized scope.

## Source tracing and disconfirmation

Start with the visible action or external entry point. Search symbols and call sites with `rg` or equivalent. Follow the active route/command through adapters and shared wrappers before claiming a mismatch. Verify the concrete serializer, validator, query, and persistence call. Check whether generated code, a feature flag, a different build, or an outer middleware changes the apparent result.

Before filing a code finding, ask: What would make this conclusion false? Inspect that plausible counterexample. A missing direct call may be an indirect/queued call; a missing local auth check may be enforced by middleware; a response mismatch may be normalized by a shared client. If the chain is incomplete, use `HYPOTHESIS`.

Do not run a huge test suite just because it exists. Choose checks that discriminate between the suspected defect and the strongest alternative explanation. If a new regression test is justified, it must assert the user-visible contract, not mirror the implementation.

## Evidence hygiene

- Keep evidence in the report's `evidence/` folder; use relative links. Prefer small, reproducible logs/commands and screenshots to enormous dumps.
- Record timestamps for timing-sensitive findings and revision/build for source findings. If a log is synthesized from code rather than execution, call it an explanation, not runtime evidence.
- Do not put credentials, auth cookies, raw session files, personal data, or unrelated app content into evidence. Redact values before saving excerpts. Refer to a test identity by role or a non-sensitive alias.
- An unavailable browser, login, server, or graph is a coverage limitation, not an application bug.
- Capture relevant findings, checks, decisions, and blockers. The report does not need every shell command, internal reasoning, or tool payload.
- Never upload the audit, publish issues, send messages, or change application code just because this skill is loaded. Follow the user's actual authorized task.
