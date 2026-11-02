# Dates, timestamps and regular expressions

Examples assume compatible Athena engine functions and illustrative column types; inspect the effective engine and actual schema. SQL examples are templates, not permission to execute; use the exploration guardrails and persist executed queries/results.

## Date and timestamp ranges

Prefer half-open ranges: they avoid missing fractional seconds and make adjacent windows non-overlapping. The example assumes `event_time` is a timestamp without time zone and the business window uses the same interpretation.

```sql
SELECT event_id, event_time
FROM analytics.events
WHERE event_date = '2025-03-01' -- Hive string partition, when applicable
  AND event_time >= TIMESTAMP '2025-03-01 00:00:00'
  AND event_time <  TIMESTAMP '2025-03-02 00:00:00'
LIMIT 10;
```

Bad: `event_time BETWEEN TIMESTAMP '2025-03-01 00:00:00' AND TIMESTAMP '2025-03-01 23:59:59'` misses later fractional seconds. Bad for Hive partition pruning: filtering only `date(event_time)` while omitting the separate partition key. Partition and event time must align; late-arriving data or ingestion-time partitions require a deliberately wider partition window.

For strings, parse explicitly and handle malformed input rather than guessing its format:

```sql
SELECT raw_date,
       try_cast(raw_date AS date) AS iso_date,
       try(date_parse(raw_date, '%d/%m/%Y')) AS parsed_date
FROM analytics.events
WHERE event_date = '2025-03-01'
LIMIT 10;
```

`try`/`try_cast` can turn invalid values into NULL: report or count invalid inputs when quality matters; do not silently treat them as valid dates. `date_parse` returns a timestamp. Use `date_add('day', 1, ...)` and `date_trunc('month', ...)` only with understood types and boundary semantics. Avoid applying casts/functions to a partition key in a predicate if a direct typed/string comparison can be used; verify pruning in the plan.

For time zones, distinguish a wall-clock timestamp from an instant: `with_timezone` attaches a zone to a zone-less timestamp, while `at_timezone` converts an instant with time zone. Define the business zone, DST behavior and UTC partition boundary before constructing predicates. ISO 8601 strings with offsets can be parsed with `from_iso8601_timestamp`; validate behavior for missing offsets and the actual engine version.

## Regular expressions

Athena's regex functions follow engine-specific semantics; verify patterns and engine version. `regexp_like` searches for a match anywhere unless anchored. SQL string escaping is not shell escaping; save the exact SQL in its artifact.

```sql
SELECT event_id,
       regexp_extract(message, 'order_id=([0-9]+)', 1) AS order_id,
       regexp_replace(message, '[0-9]+', '<number>') AS masked_message
FROM analytics.events
WHERE event_date = '2025-03-01'
  AND regexp_like(message, '^ERROR:')
LIMIT 10;
```

Bad: `regexp_like(code, '[0-9]+')` when the requirement is a whole string of digits; use `regexp_like(code, '^[0-9]+$')` instead. Test NULL, empty strings, Unicode and malformed cases; extraction without a match returns NULL. Regex validation is not proof that a date or identifier is semantically valid. Prefer equality, `IN`, `LIKE` or string functions where they express the actual requirement; avoid costly regex on an unrestricted scan. Do not interpolate untrusted text as SQL or a regex without validation and appropriate parameterization/escaping.

References: [Athena timestamps](https://docs.aws.amazon.com/athena/latest/ug/data-types-timestamps.html), [Athena engine v3](https://docs.aws.amazon.com/athena/latest/ug/engine-versions-reference-0003.html), [Trino date functions](https://trino.io/docs/current/functions/datetime.html), [Trino regex functions](https://trino.io/docs/current/functions/regexp.html). Athena is not identical to current Trino; confirm support in the actual engine.
