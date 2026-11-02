# AWS CLI workflow and artifacts

## Persist every agent-issued query

In the directory where the agent is working, create `.aws-athena/` before running a catalog or Athena query. Save the exact executable Glue catalog request as a `.sh` file, or the exact Athena SQL as a `.sql` file, **before** execution. Store its result as valid JSON with the same stem and `.result.json` suffix, including failed requests. This applies to metadata discovery, exploratory queries, `EXPLAIN`, and retries; preserve prior artifacts. Ancillary account/workgroup/status API calls are operational checks, not catalog or SQL queries.

Use `NNN__database__table__context` as the stem: a sequential number zero-padded to at least three digits, database, primary table, and the reason in up to three short words joined by `_`. Determine the next unused number from existing files; never overwrite an existing pair. For a database-wide catalog query use `all` as the table; if the database is not yet known use `unknown`. For multiple tables, use the principal table and identify the others in the query. Normalize unsafe filename characters to `_`; use actual identifiers in the SQL or CLI arguments. Keep each query in its own file and assign a new number to each new attempt.

```text
.aws-athena/001__sales__orders__schema.sh
.aws-athena/001__sales__orders__schema.result.json
.aws-athena/002__sales__orders__recent_sample.sql
.aws-athena/002__sales__orders__recent_sample.result.json
```

Use the common envelope defined in [result contract and CLI examples](../examples/guide.md), for success, failure and timeout. Capture pagination completely unless a deliberately bounded result is appropriate; record truncation and continuation token when incomplete. For Athena, retain returned column metadata, rows, status and execution statistics. On CLI failure serialize the exit code and sanitized stderr into valid JSON, not an empty result or raw text masquerading as JSON. Avoid persisting secrets and respect local data-handling and version-control conventions. Do not silently remove existing artifacts.

## CLI procedure

1. Confirm effective account (`aws sts get-caller-identity`), region, catalog, database and workgroup; specify profile/region consistently when needed. Inspect `aws athena get-work-group` for engine, result configuration, enforcement and scan cutoff. Do not change settings. Query results require a configured result location or managed results; report missing access or configuration.
2. For Glue-backed catalogs, persist and execute read-only `aws glue get-tables --database-name ... --output json` or `aws glue get-table --database-name ... --name ... --output json` in `.sh` artifacts. Set `--catalog-id` when needed for the intended Glue catalog. Use AWS CLI pagination or explicitly capture continuation; distinguish access denial from an empty catalog. For other catalog types use Athena catalog metadata APIs as appropriate, persist the request as a `.sh` artifact and its JSON result, and do not presume Glue is authoritative.
3. In testing and exploration inspect the whole statement and execution path before submission. Only established read-only SQL is eligible; never execute `CREATE`, CTAS, `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `ALTER`, `DROP`, `TRUNCATE`, `MSCK REPAIR`, `UNLOAD`, equivalent statements, Glue mutation APIs, or an indirect invocation of them through AWS CLI. This also applies to files, prepared statements and `EXPLAIN ANALYZE`. Writing a proposed SQL file is allowed; do not execute it. If read-only behavior is unclear, stop.
4. Submit persisted SQL with `aws athena start-query-execution`, the intended workgroup and query execution context. Record its execution ID. Poll `get-query-execution` with bounded backoff until `SUCCEEDED`, `FAILED`, or `CANCELLED`; treat timeout as unknown/running, not success. Do not repeatedly submit a running query. If cancellation is necessary, use the known execution ID and report the outcome.
5. On success retrieve `get-query-results` as JSON with pagination as required, retaining metadata, and record scan bytes, times and reuse from `get-query-execution`. On failure record the reason and available statistics. Report incomplete results and errors. Control concurrency and back off on throttling; don't mandate parallel calls.

`LIMIT 10` bounds returned rows, not the scan; validate partition filters and use the existing workgroup cutoff and cost guardrails. `EXPLAIN` does not scan data but can incur Glue charges; `EXPLAIN ANALYZE` executes its statement. See [exploration](../../../sql-athena-exploration/rules/discovery/guide.md) and [performance](../../../sql-athena-performance/rules/optimization/guide.md).
