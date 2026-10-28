# Optional GitNexus integration

Use GitNexus for cross-layer navigation when it is available and relevant. It accelerates investigation; its graph is not the verdict. Tool names and parameters vary by version: inspect exposed schemas or installed `--help`, rather than inventing calls.

## Detect and qualify

1. Look for exposed GitNexus MCP tools. If available, use `list_repos`, including pagination only as needed to locate the target. Pin the matching repository/path; never silently use another project's index.
2. Read the target's `gitnexus://repo/{name}/context` resource when exposed. Check revision/path, freshness, and index coverage against the current workspace, including uncommitted changes. If resources are not exposed, use the installed CLI's documented status command or available tool metadata.
3. Without MCP, check an already installed `gitnexus` executable or an existing project-local runner. Inspect documented status/help commands before selecting query or refresh commands. A local runner that downloads a package is not evidence of a preinstalled tool: do not execute an auto-downloading runner merely to detect availability.
4. If the target index is stale, **refresh it automatically**, then verify it matches the current workspace before querying. A lag of one commit or thousands of commits is a refresh trigger, not a reason to decline GitNexus. Follow the refresh procedure below. If the index is for another repository, resolve the correct target rather than refreshing the unrelated index.
5. If GitNexus is unavailable, the target has no usable index, a needed layer remains unsupported, or an attempted refresh fails/is blocked, record the concrete limitation and use ordinary source search. Do not install GitNexus just to satisfy this integration.

## Refresh a stale index

Treat refreshing an existing target index as routine audit preparation, even when application fixes are not authorized. No separate confirmation is needed unless the user explicitly forbids index changes or an actual execution boundary requires it. A general audit-only or source-only request does not by itself prohibit rebuilding derived index data.

1. Announce the stale state, add a refresh task to the report, and record the target path, current revision/dirty state, and available index revision or reported lag.
2. Inspect the installed analyzer's help. From the target repository root, run the installed analyzer in index-only mode when supported:

   ```sh
   gitnexus analyze --index-only
   ```

   An existing project runner may be used with the same supported option only if it resolves to an already installed analyzer. Prefer normal incremental analysis; use a documented force option only when needed to rebuild an index that remains stale/corrupt. Preserve existing index configuration and feature coverage. Use the configured index host/path for remote MCP indexes; rebuilding an unrelated local copy does not refresh the graph being queried.
3. Keep application source, `AGENTS.md`, `CLAUDE.md`, installed skills, and agent configuration unchanged. Use documented equivalent suppression flags if the installed version lacks `--index-only`. Updating the index does not mean pulling or changing the application's Git checkout. Do not reset/stash user work or delete the index as a first attempt.
4. Wait for completion, then re-read status/context through the tool or index actually used for queries. Verify the target revision and relevant working-tree changes are covered; a zero exit code alone is insufficient. Reconnect/reload the MCP context if required by the installed version. Record completion, freshness, and any remaining coverage gaps in the report.
5. If refresh fails, diagnose the concrete error and retry only when there is a specific remedy. Avoid repeating an unchanged failing command. If permissions, inaccessible index host, incompatible tooling, explicit user limits, or another actual blocker prevents completion, record it and continue with current source. Never claim a refresh succeeded or use stale graph output as current evidence.

**Expected:** “Index is 2733 commits behind; refreshing the target index, then checking freshness before tracing.” **Not sufficient:** “Index is stale, so I will not refresh it and will only read source.”

## Choose the smallest useful graph query

| Investigation | Tools, if exposed |
| --- | --- |
| Find the process behind an action | `query`, then `context` on relevant symbols |
| Trace caller → handler → storage | `context`; `trace` for a known start/end |
| Find API consumers and handlers | `route_map` |
| Check API response vs consumer fields | `shape_check` |
| Prioritize an already understood repair | Read-only `impact` or `api_impact` |
| Understand the scope of existing changes | `detect_changes` |

Start with the scenario's action, contract, or symptom, not a repository-wide graph dump. Source inspection is still required before a `CONFIRMED-CODE` finding.

`route_map`, `shape_check`, `trace`, and other advanced tools are version-dependent. Do not require them. Response-shape extraction can miss dynamic serializers, adapters, unions, and language features. A missing edge/path/consumer is not proof that none exists. A reported shape mismatch is a lead until the active handler and consumer are inspected; runtime evidence is only runtime evidence when an actual execution was observed and its provenance is clear.

In a finding, record repository/index revision, tool, relevant symbols/paths, and graph limitations. Link actual inspected `file:line` locations separately. If findings rely on changed files absent from the index, navigate those files directly and explicitly limit graph claims.

Apart from the index refresh described above, do not invoke `rename`, `clean`, reconfiguration, or other mutations during an audit-only run. Do not use graph metrics such as fan-out or dependency count as standalone proof of a product defect.

Upstream documentation: [GitNexus](https://github.com/abhigyanpatwari/GitNexus). Use the installed version's tool schemas as the execution authority.
