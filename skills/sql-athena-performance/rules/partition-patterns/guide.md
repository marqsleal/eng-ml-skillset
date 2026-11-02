# Time partition patterns for Athena

All examples assume Hive tables and string keys unless stated otherwise. Replace identifiers and values with verified metadata. The partition filter must include every partition that can contain the requested events; these examples assume partitions track event time, not ingestion time. Consider late arrivals and time zones. Use `EXPLAIN` to inspect pruning, and measure actual scan bytes; `LIMIT 10` only limits returned rows. Persist executed SQL and results under `.aws-athena/`; never run table/data mutations via AWS CLI during exploration or tests.

## Discover partitions with `$partitions`

After inspecting the table and partition keys via Glue, consider the Athena metadata table when actual registered partition values are needed. Quote the **entire** table name plus `$partitions` as one identifier; this example assumes Hive string keys named `year`, `month`, and `day`:

```sql
SELECT year, month, day
FROM "analytics"."events$partitions"
WHERE year = '2025' AND month = '03'
LIMIT 10;
```

For a single key, select and filter the actual key, for example `SELECT dt FROM "analytics"."events_compact$partitions" WHERE dt >= '20250301' AND dt < '20250304' LIMIT 10`. Use `ORDER BY` only if ordering is required: it can require processing more metadata, and without it the sample is not the latest or a complete inventory. `LIMIT` does not guarantee bounded metadata work or cost. Athena queries and Glue metadata operations can incur charges; check workgroup and scope first. Save this as a `.sql` query and persist its `.result.json`, just like any other agent-issued Athena query.

For a Glue-backed Hive table, `aws glue get-partitions` is another metadata option; apply an appropriate expression and pagination, and persist the command and JSON result. Both registered metadata and a successful listing do not prove files exist or that every requested partition contains records. If pagination or a sample truncates results, do not describe it as a complete inventory.

Partition projection calculates locations from table properties, and projected values need not be registered in Glue; a registered-partition listing cannot establish all projected values or physical data. Inspect projection properties and ranges, and do not assume `$partitions` lists all projected values. Iceberg also exposes `$partitions`, but its metadata schema and semantics differ from Hive; inspect its actual fields instead of assuming `year`, `month`, and `day` columns. `SHOW PARTITIONS` is unsupported for Iceberg and does not list unregistered projected partitions. Lake Formation restrictions can deny access to Iceberg metadata tables; treat denial as unknown, not as absence of partitions. See [AWS partition listing](https://docs.aws.amazon.com/athena/latest/ug/querying-glue-catalog-listing-partitions.html), [Iceberg metadata](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg-table-data.html), and [projection](https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html).

## Separate year, month, day

For a single day, use all keys and their real encoding (here zero-padded strings):

```sql
SELECT event_id, event_time
FROM analytics.events
WHERE year = '2025' AND month = '03' AND day = '01'
  AND event_time >= TIMESTAMP '2025-03-01 00:00:00'
  AND event_time <  TIMESTAMP '2025-03-02 00:00:00'
LIMIT 10;
```

For a range crossing a month or year, enumerate relevant partition combinations without losing boundary days. For the interval February 28 through March 2 inclusive:

```sql
SELECT event_id, event_time
FROM analytics.events
WHERE ((year = '2025' AND month = '02' AND day = '28')
    OR (year = '2025' AND month = '03' AND day IN ('01', '02')))
  AND event_time >= TIMESTAMP '2025-02-28 00:00:00'
  AND event_time <  TIMESTAMP '2025-03-03 00:00:00'
LIMIT 10;
```

Bad: `month IN ('02','03') AND day BETWEEN '28' AND '02'` misses dates. An `OR` plan may behave differently across engines or catalogs; inspect `EXPLAIN`. For long intervals build correct bounded predicates from the calendar instead of enumerating an unbounded history.

## One partition column: YYYY-MM-DD or YYYYMMDD

Lexicographic range comparisons work for consistently zero-padded strings in these exact formats. Use the actual format and column type; do not assume equivalent behavior for unpadded or differently ordered dates.

```sql
-- event_date is STRING 'YYYY-MM-DD'.
SELECT event_id, event_time
FROM analytics.events
WHERE event_date >= '2025-02-28' AND event_date < '2025-03-03'
  AND event_time >= TIMESTAMP '2025-02-28 00:00:00'
  AND event_time <  TIMESTAMP '2025-03-03 00:00:00'
LIMIT 10;
```

```sql
-- dt is STRING 'YYYYMMDD'; same three-day interval.
SELECT event_id, event_time
FROM analytics.events_compact
WHERE dt >= '20250228' AND dt < '20250303'
  AND event_time >= TIMESTAMP '2025-02-28 00:00:00'
  AND event_time <  TIMESTAMP '2025-03-03 00:00:00'
LIMIT 10;
```

Bad: `WHERE date_parse(dt, '%Y%m%d') >= ...` as the sole partition predicate; applying a function to the key can interfere with pruning. Compare the original key directly in its declared type and representation, then separately filter the timestamp if needed. For integer or date keys use correctly typed literals. Projection configuration may require a specific format.

## Iceberg and validation

Iceberg may use hidden partition transforms derived from `event_time`; a direct timestamp range can enable pruning without exposing a separate partition column. Do not mechanically apply Hive key predicates. Full-day ranges can enable more effective pushdown for a day transform; inspect the actual plan, transform and engine behavior.

Prefix the intended read-only query with `EXPLAIN` and inspect partition selection; `EXPLAIN ANALYZE` runs it and incurs scan charges. A scan cutoff can cancel a query but doesn't guarantee zero cost. AWS references: [timestamp and partition behavior](https://docs.aws.amazon.com/athena/latest/ug/data-types-timestamps.html), [partition optimization](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning-data-optimization-techniques.html).
