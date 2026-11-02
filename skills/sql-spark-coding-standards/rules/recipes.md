# Spark SQL recipes

Adapt table and column names to the real schema. Examples are read-only templates, not instructions to query a production catalog. Date literals and formats, key types, session timezone and data quality must match the source.

## Filter, join and aggregate

```sql
WITH active_customers AS (
    SELECT DISTINCT
        customer_id
    FROM customers
    WHERE is_active = true
), filtered_orders AS (
    SELECT
        order_id,
        customer_id,
        amount
    FROM orders
    WHERE order_date >= DATE '2024-01-01'
        AND order_date < DATE '2024-02-01'
)
SELECT
    o.customer_id,
    COUNT(*) AS order_count,
    SUM(o.amount) AS total_amount
FROM filtered_orders AS o
LEFT SEMI JOIN active_customers AS c
    ON o.customer_id = c.customer_id
GROUP BY
    o.customer_id
```

Here `LEFT SEMI JOIN` already prevents customer duplicates from multiplying orders; `DISTINCT` can be removed if the plan or use case does not justify it. Half-open time intervals avoid an inclusive timestamp end boundary. Check actual source types and partition pruning.

Bad: joining the customer dimension without confirming uniqueness and then masking inflated totals with `DISTINCT`. Better: state the grain, validate keys and use a semi join for existence. Bad: `SELECT *` over a wide join and ambiguous duplicate column names; better: explicitly select the required qualified columns.

## Latest event per entity

```sql
WITH ranked_events AS (
    SELECT
        user_id,
        event_id,
        event_time,
        ROW_NUMBER() OVER (
            PARTITION BY user_id
            ORDER BY event_time DESC NULLS LAST, event_id DESC
        ) AS row_num
    FROM events
)
SELECT
    user_id,
    event_id,
    event_time
FROM ranked_events
WHERE row_num = 1
```

This is deterministic only if the ordering uniquely distinguishes ties in each user group. Specify the treatment of missing timestamps and tie breakers.

## Dates, regex and temporal partitions

```sql
SELECT
    TO_DATE(date_text, 'yyyy-MM-dd') AS event_date,
    REGEXP_EXTRACT(email, '@([^@]+)$', 1) AS email_domain
FROM incoming_events
WHERE email RLIKE '^[^@]+@[^@]+$'
```

`REGEXP_EXTRACT` returns an empty string for no match, not null. Spark uses Java regex and Spark datetime patterns; escaping depends on SQL string settings and any host language. Test invalid input under the deployed ANSI and parser settings; configure or verify session timezone and DST behavior.

```sql
-- Example: separate zero-padded STRING partition columns, one month.
SELECT event_id
FROM events
WHERE year = '2024'
    AND month = '01'
    AND day BETWEEN '01' AND '31'

-- Example: one fixed-width STRING partition column YYYYMMDD.
SELECT event_id
FROM events
WHERE yearmonthday BETWEEN '20240101' AND '20240131'
```

For integer columns use integer literals. Fixed-width strings are required for lexical ordering; crossing month or year boundaries requires careful predicates. Avoid wrapping a partition column in a function when it prevents pruning, and inspect `PartitionFilters` and scan metrics. Hive directory columns and Iceberg partition transforms are different; check the table format and provider. Spark SQL is not Athena SQL: do not assume Athena's `$partitions` metadata syntax is available.
