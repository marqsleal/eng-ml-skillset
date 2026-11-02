# Review and debugging

For each actionable finding give severity, location or SQL fragment, evidence, impact, and a concrete correction. Separate confirmed findings from assumptions; don't assert an unobserved scan, cost, schema or permissions. Prioritize correctness and access risks, then measurable performance and maintainability. When no findings are supported, say so and state what could not be checked.

Check intended row grain, join cardinality, NULL and duplicate semantics, time zones/boundaries, result ordering, input handling, partition pruning, and sensitive data exposure. For a `LEFT JOIN`, check whether a right-side WHERE condition unintentionally removes unmatched rows. Check engine/version-specific syntax rather than applying another SQL dialect's features. Never introduce a source mutation into a live test or exploration via AWS CLI.

| Symptom | Investigate before retrying |
| --- | --- |
| Syntax or unsupported function | Effective engine, Athena documentation, quoting, function signatures and types. |
| Column not found / ambiguous | Actual catalog, database, table and aliases; inspect metadata and quote identifiers correctly. |
| Invalid date or type mismatch | Source format, nulls, engine timestamp rules, explicit cast and time zone; use `try` only when invalid values are reported as such. |
| Missing partitions or no rows | Real partition type and encoding, window boundaries, projection ranges, late arrivals and catalog permissions; a limited result or denied listing is not proof of absence. |
| Partition schema mismatch | Compare Glue table and partition metadata and formats; propose a fix rather than running catalog repair or mutations during exploration. |
| Access denied | Identify the denied operation and context; do not bypass policies or report inaccessible data as empty. |
| Slow or scan cutoff exceeded | Check actual state, bytes, plan, partition predicates and workgroup; narrow scope before a further run. Cutoff cancellation may still incur charges. |
| Missing output / query failure | Inspect execution status, state reason, result configuration, storage access and pagination. Distinguish a failed retrieval from a failed query. |

Use minimal reproducible read-only examples that respect scan limits, and persist each query and result. Do not repeat potentially costly queries blindly. See [Athena operations](../../../sql-athena-tooling/rules/operations/guide.md).
