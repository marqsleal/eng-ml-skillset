# Athena query patterns

These are illustrative SELECT templates, not instructions to execute. Replace example names, values and types only after checking the real schema and scope. Persist each executed query and JSON result as specified in [artifact rules](../../../sql-athena-tooling/rules/cli/guide.md). Apply the exploration read-only and cost guardrails; `LIMIT` does not guarantee a cheap scan. A sample without `ORDER BY` is not deterministic or representative.

## Narrow sample

```sql
-- Hive table: event_date is a string partition key YYYY-MM-DD.
SELECT event_id, event_time, event_type
FROM analytics.events
WHERE event_date = '2025-03-01'
LIMIT 10;
```

Avoid `SELECT * FROM analytics.events LIMIT 10` as a discovery default: it exposes unnecessary columns and can still scan significant data. A broad scan is not made safe merely by the limit.

## Aggregation at the intended grain

```sql
SELECT event_type, count(*) AS event_count,
       count(DISTINCT user_id) AS unique_users
FROM analytics.events
WHERE event_date >= '2025-03-01' AND event_date < '2025-03-04'
GROUP BY event_type
ORDER BY event_count DESC;
```

Define what constitutes a user or event and how NULL is treated: `count(*)` counts rows and `count(user_id)` ignores NULL. Never infer data completeness from a sample. An aggregate can scan all qualifying data even if a limit is appended.

## Join without accidental multiplication

```sql
-- Assumes customers has at most one row per customer_id; verify this first.
SELECT o.order_id, o.customer_id, c.customer_name
FROM analytics.orders AS o
LEFT JOIN analytics.customers AS c ON o.customer_id = c.customer_id
WHERE o.order_date = '2025-03-01'
LIMIT 10;
```

Bad practice: add `DISTINCT` after a many-to-many join to hide duplicate rows. First establish key uniqueness and the target grain; if a dimension has history, define a deterministic rule to select its relevant row.

## Deterministic latest record per key

```sql
WITH ranked AS (
    SELECT user_id, status, updated_at, event_id,
           row_number() OVER (
               PARTITION BY user_id ORDER BY updated_at DESC, event_id DESC
           ) AS rn
    FROM analytics.user_events
    WHERE event_date = '2025-03-01'
)
SELECT user_id, status, updated_at
FROM ranked
WHERE rn = 1;
```

This returns the latest record **within the selected partition**, not necessarily the latest ever. The tie-breaker must actually be unique; a wider history may be expensive. A CTE improves clarity but is not a materialization guarantee.

## Missing related rows and NULL

Prefer `NOT EXISTS` to `NOT IN` when the subquery may contain NULL:

```sql
SELECT o.order_id
FROM analytics.orders AS o
WHERE o.order_date = '2025-03-01'
  AND NOT EXISTS (
      SELECT 1 FROM analytics.refunds AS r WHERE r.order_id = o.order_id
  )
LIMIT 10;
```

The unpartitioned side can still be costly; inspect its schema and include an appropriate partition predicate when it preserves the intended semantics. NULL order IDs require an explicit business decision.
