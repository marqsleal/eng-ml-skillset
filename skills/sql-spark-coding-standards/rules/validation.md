# Validation workflow

Validation covers syntax, semantic results and execution characteristics independently. Do not claim execution when only a static review was performed.

1. Identify the engine, version, catalog, schemas, source types, timezone and ANSI mode. Compare SQL syntax and built-in functions with the documentation for that exact environment. Check output grain, null semantics, joins, grouping, ordering, literals and source partition columns.
2. Prepare small synthetic fixtures using SQL `VALUES` CTEs when possible; they do not require Python or tables. Do not recommend or start local Spark execution. Execute only when requested in an existing authorized test environment. The following complete query should return one row, `(1, 30)`, even with a duplicate customer:

```sql
WITH orders AS (
    SELECT *
    FROM VALUES (1, 10), (1, 20), (2, 7) AS t(customer_id, amount)
), customers AS (
    SELECT *
    FROM VALUES (1, true), (1, true), (2, false) AS t(customer_id, is_active)
)
SELECT
    o.customer_id,
    SUM(o.amount) AS total_amount
FROM orders AS o
LEFT SEMI JOIN customers AS c
    ON o.customer_id = c.customer_id
    AND c.is_active = true
GROUP BY
    o.customer_id
```

A semi join exposes only left-side columns after the join, so the right-side predicate belongs in `ON` or a filtered CTE, not in the outer `WHERE`. Assert rows and schema, not merely successful parsing. Include cases for missing and duplicate keys, nulls, empty data, invalid dates, regex no-match, interval boundaries and window ties when relevant. Compare unordered results as a multiset, preserving duplicate counts. A synthetic fixture is not proof of source schema, permissions, production performance or connector behavior.

3. Run `EXPLAIN FORMATTED` on the reviewed read-only query in an allowed environment. Inspect `ReadSchema`, `PartitionFilters`, `PushedFilters`, `Exchange` and join operators where applicable. `EXPLAIN` does not validate actual outputs or guarantee low cost; it can require catalog access. Adaptive execution may change the final plan, so compare runtime metrics when already available from an authorized execution; do not require additional monitoring tools. See [EXPLAIN](https://spark.apache.org/docs/3.5.6/sql-ref-syntax-qry-explain.html).
4. If querying real data is authorized, restrict scope with actual partition predicates and select minimal columns; `LIMIT 10` limits returned rows, not scan bytes, global sort or shuffle work. Avoid `COUNT(*)` solely as a cheap existence check. Do not expose sensitive data in logs or artifacts.
5. Report the version/environment, what was tested, expected and observed results, plan findings and limitations. If Spark is unavailable, perform static review and explicitly report execution as unverified. Do not install tooling or submit remote queries merely to produce a passing check.
