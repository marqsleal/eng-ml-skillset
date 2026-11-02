# Athena operations and diagnosis

Use the confirmed workgroup and region. These are read-only operational APIs; constrain inventories to the user's task and avoid exposing query texts containing sensitive data. Save any agent-issued SQL or catalog query and result using the artifact contract; operational status/history API calls follow the user's data-handling conventions.

```sh
aws athena get-work-group --work-group analytics --region us-east-1 --output json
aws athena list-query-executions --work-group analytics --region us-east-1 --output json
aws athena batch-get-query-execution --query-execution-ids id1 id2 --region us-east-1 --output json
aws athena get-query-runtime-statistics --query-execution-id id1 --region us-east-1 --output json
aws athena list-named-queries --work-group analytics --region us-east-1 --output json
aws athena batch-get-named-query --named-query-ids id1 id2 --region us-east-1 --output json
```

Use actual IDs, not these placeholders. AWS CLI pagination can fetch many pages: restrict the scope deliberately, handle continuation and disclose incomplete inventories. Batch execution details accept at most 50 IDs; inspect `UnprocessedQueryExecutionIds`, report failures and retry only transient cases with bounded backoff. Check the API's actual batch limits and unprocessed entries for named queries as well. Never treat missing IDs as successful. Named queries are saved SQL, not query results; inspect contents before any attempted execution and apply read-only guardrails.

For failed queries inspect `Status.State`, `StateChangeReason`, structured Athena error when present, and available statistics. Queue time, planning time, engine time and bytes scanned answer different questions. Runtime statistics may be unavailable or incomplete, including due to permissions or execution state; report that rather than inventing values. When comparing runs check effective engine, scope, workgroup, result reuse and equivalent output. Do not hard-code a price or interpret scan bytes as a universal cost.
