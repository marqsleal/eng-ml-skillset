# Analytic SQL patterns

Templates assume verified schema, types and compatible engine. Choose a bounded partition range for every large source, respecting its actual partition scheme and the intended history; a filter in the examples only bounds the specified table. Apply read-only and cost guardrails, persist each executed query/result, and do not assume `LIMIT` bounds scans. See [partition patterns](../../../sql-athena-performance/rules/partition-patterns/guide.md).

## Previous value and running totals

```sql
SELECT
    account_id,
    event_time,
    event_id,
    amount,
    lag(amount) OVER (
        PARTITION BY account_id
        ORDER BY event_time, event_id
    ) AS previous_amount,
    sum(amount) OVER (
        PARTITION BY account_id
        ORDER BY event_time, event_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_amount
FROM analytics.events
WHERE event_date >= '2025-03-01' AND event_date < '2025-04-01';
```

This running total starts at the beginning of the **filtered** interval; `lag` has no previous row outside it. `event_id` must actually break ties. For a seven-**row** moving average use `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`; this does not mean seven calendar days if dates are missing or multiple records exist per day. `lead` follows the same ordering considerations. Choose `rank`, `dense_rank` or `row_number` based on desired tie handling, and explicitly specify window frames where relevant.

## Monthly cohort retention

Assume one verified `users` row per user with `first_activity_date` of type DATE, and an `activity` table with `activity_date` DATE and string `activity_partition` equal to its event date. This computes March cohort membership and its activity in March and April; absence of April data is not evidence of churn if the period is incomplete.

```sql
WITH cohort AS (
    SELECT user_id
    FROM analytics.users
    WHERE first_activity_date >= DATE '2025-03-01'
        AND first_activity_date < DATE '2025-04-01'
),
activity AS (
    SELECT user_id, date_trunc('month', activity_date) AS activity_month
    FROM analytics.user_activity
    WHERE activity_partition >= '2025-03-01'
        AND activity_partition < '2025-05-01'
        AND activity_date >= DATE '2025-03-01'
        AND activity_date < DATE '2025-05-01'
)
SELECT
    count(DISTINCT c.user_id) AS cohort_size,
    count(DISTINCT CASE WHEN a.activity_month = DATE '2025-03-01' THEN c.user_id END) AS month_0,
    count(DISTINCT CASE WHEN a.activity_month = DATE '2025-04-01' THEN c.user_id END) AS month_1
FROM cohort AS c
LEFT JOIN activity AS a ON c.user_id = a.user_id;
```

Confirm `users` is adequately bounded too. Define cohort membership, identity, date zone, data completeness and whether month 0 requires a qualifying event. Duplicate activity must not multiply users; distinct counts handle that in this example. Retention percentage can use `1.0 * month_1 / nullif(cohort_size, 0)` in an outer query.

## Ordered funnel

Assume event timestamps are comparable and the task requires view → signup → purchase in strict time order within a bounded interval. Aggregate the earliest qualifying next step per user; do not count unordered event presence as a sequential funnel.

```sql
WITH scoped AS (
    SELECT user_id, event_time, event_type
    FROM analytics.events
    WHERE event_date >= '2025-03-01' AND event_date < '2025-04-01'
        AND event_type IN ('view', 'signup', 'purchase')
),
views AS (
    SELECT user_id, min(event_time) AS view_time
    FROM scoped WHERE event_type = 'view' GROUP BY user_id
),
signups AS (
    SELECT v.user_id, min(e.event_time) AS signup_time
    FROM views AS v
    JOIN scoped AS e ON e.user_id = v.user_id
        AND e.event_type = 'signup' AND e.event_time > v.view_time
    GROUP BY v.user_id
),
purchases AS (
    SELECT s.user_id, min(e.event_time) AS purchase_time
    FROM signups AS s
    JOIN scoped AS e ON e.user_id = s.user_id
        AND e.event_type = 'purchase' AND e.event_time > s.signup_time
    GROUP BY s.user_id
)
SELECT
    count(*) AS viewed,
    count(s.user_id) AS signed_up,
    count(p.user_id) AS purchased
FROM views AS v
LEFT JOIN signups AS s ON s.user_id = v.user_id
LEFT JOIN purchases AS p ON p.user_id = v.user_id;
```

This definition chooses the first view and first later signup; it excludes tied timestamps and steps outside the interval. A conversion deadline, session boundary, event deduplication, timezone, equal timestamps, multiple attempts or late arrivals require an explicit alternative definition. CTEs are not guaranteed materialized; inspect the plan and scan cost for repeated references to `scoped`.
