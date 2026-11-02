# Discovery and exploratory guardrails

## Scope and safety

- Establish the intended account, region, catalog, database, workgroup and scope from the request or configuration; verify before querying. Do not disclose credentials. If the target is ambiguous or access is denied, report it rather than guessing or expanding permissions.
- During testing or exploration, never execute table or data changes through AWS CLI, even if explicitly embedded in a SQL file, shell script, multi-statement string, prepared statement, or `EXPLAIN ANALYZE`. Prohibited examples include `CREATE` (including CTAS), `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `ALTER`, `DROP`, `TRUNCATE`, `MSCK REPAIR`, `UNLOAD`, and equivalent operations or Glue mutation APIs. Do not bypass the restriction through another CLI command or indirect invocation. Only execute statements whose read-only behavior is established; if uncertain, do not execute. Creating a proposed SQL file for a human to review is allowed.
- Read-only Athena queries can still incur charges and write query results to configured result storage. Avoid displaying or persisting credentials; treat schema, query text and returned data as potentially sensitive and respect local access and versioning conventions.

## Discovery then sampling

1. Prefer Glue `get-tables` and `get-table` for a Glue-backed catalog; inspect columns, partition keys, table type, format and location. Use pagination appropriately. For non-Glue or federated catalogs, use the appropriate Athena catalog metadata APIs; don't assume Glue describes them. An inaccessible field is unknown, not empty.
2. Use the relevant table's partition keys and format to choose a narrow, meaningful slice. In Hive, filtering a timestamp alone may not filter its separate partition key; Iceberg partition transforms differ. Do not invent partition values. Discover them where appropriate or use task-provided values.
3. For an initial row sample select only needed columns, restrict relevant partitions, and default to `LIMIT 10`. A limit bounds rows returned, not bytes scanned or cost; sorting, joins and aggregation can require extensive reads. A sample is not necessarily representative.
4. Inspect the existing workgroup and its per-query scan cutoff if accessible. Do not change the workgroup. If scope, expected scan or budget remains uncertain, narrow the query or stop and explain the uncertainty before a potentially expensive scan. A cutoff is a safeguard, not a cost guarantee.
5. Use `EXPLAIN` to inspect applicable plans and partition selection. `EXPLAIN ANALYZE` executes the underlying statement and incurs scan charges; apply all read-only and cost guardrails. Do not repeat expensive queries without a reason. Measure actual bytes scanned and report limitations.

Persist every agent-issued catalog query and Athena SQL with its JSON result according to [artifact rules](../../../sql-athena-tooling/rules/cli/guide.md), including failures. Handle pagination, access errors and throttling explicitly; never silently turn an error into an empty result.

For examples to adapt after inspecting the real schema, see [query patterns](../../../sql-athena-coding-standards/rules/query-patterns/guide.md) and [partition patterns](../../../sql-athena-performance/rules/partition-patterns/guide.md).

When actual partition values are needed, the partition patterns include the read-only `"database"."table$partitions"` metadata query, plus its Hive, projection and Iceberg limitations. Prefer Glue table discovery first; persist the Athena metadata query and result like any other SQL query.
