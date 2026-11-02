---
name: sql-athena-tooling
description: Use AWS CLI to inspect Glue catalog metadata and run or diagnose Amazon Athena queries with persisted artifacts.
---

# Athena and Glue tooling

Prefer AWS CLI and existing account configuration. Read [CLI workflow and artifacts](rules/cli/guide.md) for discovery, query execution, failure handling and persistence. During tests and explorations, follow [exploration guardrails](../sql-athena-exploration/SKILL.md): never execute any table or data mutation through AWS CLI, including SQL passed indirectly from a file or script. Drafting such SQL for review is allowed.

Do not depend on `jq`: it is unavailable in the target environment. For JSON processing use Python 3's standard library when present; if no suitable JSON processor is available, report the limitation rather than producing invalid result files.

- For the result JSON contract and worked CLI workflows, read [examples](rules/examples/guide.md).
- For query history, runtime statistics and failed executions, read [operations and diagnosis](rules/operations/guide.md).
- For offline behavior checks, use [validation scenarios](rules/examples/validation.md).
