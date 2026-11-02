# Human-readable Athena SQL formatting

Optimize SQL for people who will read, review, and maintain it. Follow the repository's established formatter and conventions when present; otherwise use the following defaults consistently. Formatting does not fix a query's logic, type compatibility, partition pruning, or cost.

## Layout and spacing

- Use uppercase for SQL keywords and functions consistently with project style; the examples below use uppercase keywords and lowercase function names. Preserve identifier spelling and quote identifiers only when required or when the project consistently quotes them. Athena uses double quotes for quoted identifiers in `SELECT`; do not mistake single-quoted string literals for identifiers.
- Place major clauses (`SELECT`, `FROM`, `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`) on separate lines. For nontrivial queries put each selected expression on its own line, using trailing commas. Keep a simple single-expression query compact if it remains clear.
- Indent nested queries, CTE bodies and multiline expressions by four spaces. Align related conditions at the same indentation level; avoid tabs and alignment that creates large runs of spaces or noisy changes when names grow.
- Put spaces around comparison and arithmetic operators, and after commas; omit spaces immediately inside parentheses. Use blank lines sparingly to separate meaningful stages, such as CTEs or logical blocks.
- Use explicit, descriptive aliases and `AS` for column aliases; qualify columns where more than one source could make them ambiguous. Avoid cryptic aliases, positional `GROUP BY` and `ORDER BY` when names make intent clearer.
- Keep lines reasonably short according to the project convention; wrap by logical expression rather than splitting identifiers or literals. Use comments to explain business intent, assumptions, time zones or surprising decisions, not to restate obvious SQL. Keep comments accurate when changing the query.

## Example: filters and joins

Hard to review:

```sql
select o.order_id,o.customer_id,c.name customer_name,sum(o.amount) total_amount from analytics.orders o left join analytics.customers c on o.customer_id=c.customer_id where o.order_date>='2025-03-01' and o.order_date<'2025-03-04' and o.status='paid' group by 1,2,3 order by 4 desc;
```

More readable, with the same logic:

```sql
SELECT
    o.order_id,
    o.customer_id,
    c.name AS customer_name,
    sum(o.amount) AS total_amount
FROM analytics.orders AS o
LEFT JOIN analytics.customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_date >= '2025-03-01'
    AND o.order_date < '2025-03-04'
    AND o.status = 'paid'
GROUP BY
    o.order_id,
    o.customer_id,
    c.name
ORDER BY total_amount DESC;
```

This is a formatting example, not an assertion that the join is unique or cheap. Check the actual schema, cardinality and partition keys. Add a filter on the joined side only if it preserves the intended `LEFT JOIN` semantics; a `WHERE` predicate on the right side can exclude unmatched rows.

## Example: CTE, CASE and window function

```sql
WITH ranked_events AS (
    SELECT
        user_id,
        event_id,
        event_time,
        CASE
            WHEN event_type = 'purchase' THEN 'conversion'
            WHEN event_type = 'view' THEN 'engagement'
            ELSE 'other'
        END AS event_group,
        row_number() OVER (
            PARTITION BY user_id
            ORDER BY event_time DESC, event_id DESC
        ) AS row_number
    FROM analytics.events
    WHERE event_date = '2025-03-01'
)
SELECT
    user_id,
    event_id,
    event_time,
    event_group
FROM ranked_events
WHERE row_number = 1;
```

The example finds the latest row **within the selected date**, assuming `event_id` breaks ties. Use parentheses to make mixed `AND`/`OR` conditions explicit and align each branch; do not change logical grouping while reformatting. Lay out long `IN` lists across lines when that improves review, but avoid expanding short, clear lists unnecessarily.

Formatting existing SQL should preserve behavior: check string and regex literals, quoted names, comments, operator precedence, window frames, ordering, and semicolons. Do not execute write statements via AWS CLI during tests or exploration; persist any executed query and its result according to [artifact rules](../../../sql-athena-tooling/rules/cli/guide.md).
