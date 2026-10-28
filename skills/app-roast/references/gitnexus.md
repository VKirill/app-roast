# Optional GitNexus integration

Use GitNexus for cross-layer navigation when it is available and relevant. It accelerates investigation; its graph is not the verdict. Tool names and parameters vary by version: inspect exposed schemas or installed `--help`, rather than inventing calls.

## Detect and qualify

1. Look for exposed GitNexus MCP tools. If available, use `list_repos`, including pagination only as needed to locate the target. Pin the matching repository/path; never silently use another project's index.
2. Read the target's `gitnexus://repo/{name}/context` resource when exposed. Check revision/path, freshness, and index coverage against the current workspace, including uncommitted changes. If resources are not exposed, use the installed CLI's documented status command or available tool metadata.
3. Without MCP, check an already installed `gitnexus` executable or an existing project-local runner. Run only documented status/help/query commands. A local runner that downloads a package is not evidence of a preinstalled tool: do not execute an auto-downloading runner merely to detect availability.
4. If unavailable, stale, wrong-repository, or missing the needed layer, record the limitation and use ordinary source search. If refreshing an index is already authorized, inspect the installed version's flags and prefer index-only behavior to avoid rewriting repository instruction files. Otherwise skip refresh; do not make installation or indexing a prerequisite.

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

Do not invoke `rename`, `clean`, reconfiguration, or other mutations during an audit-only run. Do not use graph metrics such as fan-out or dependency count as standalone proof of a product defect.

Upstream documentation: [GitNexus](https://github.com/abhigyanpatwari/GitNexus). Use the installed version's tool schemas as the execution authority.
