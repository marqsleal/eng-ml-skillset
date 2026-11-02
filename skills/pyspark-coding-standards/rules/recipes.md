# Transformation recipes

Examples are templates: adapt column types, formats, session timezone and business semantics. Java regular-expression and Spark datetime patterns are not Python `re`/`strptime` syntax. ANSI mode and invalid casts vary by configuration and version; validate dirty input explicitly.

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

clean = (
    source
    .select("event_id", "user_id", "event_date", "event_time", "email")
    .withColumn("event_date", F.to_date("event_date", "yyyy-MM-dd"))
    .withColumn("email_domain", F.regexp_extract("email", r"@([^@]+)$", 1))
    .withColumn("email_normalized", F.lower(F.trim("email")))
)

# regexp_extract returns an empty string when there is no match, not null.
window = Window.partitionBy("user_id").orderBy(
    F.col("event_time").desc(), F.col("event_id").desc()
)
latest = (
    clean.withColumn("row_num", F.row_number().over(window))
    .filter(F.col("row_num") == 1)
    .drop("row_num")
)
```

The ordering is deterministic only if `(event_time, event_id)` uniquely breaks ties within each user; decide how nulls sort and handle missing/invalid timestamps. Use `rlike` for regex predicates and `regexp_replace` for replacement; test anchors, escaping, Unicode and no-match/null cases. Set or verify `spark.sql.session.timeZone`; timestamp instants, local timestamps and date boundaries differ, especially around daylight saving.

For Hive-style partition columns, filter on actual column names and types before expensive transformations. Confirm pruning in `explain` and scan metrics. Examples below assume zero-padded string columns; use native integer literals for integer columns.

```python
from pyspark.sql import functions as F

# A single month; combine predicates carefully for intervals across months.
january = source.filter(
    (F.col("year") == "2024")
    & (F.col("month") == "01")
    & F.col("day").between("01", "31")
)
# Lexicographical ordering works for fixed-width YYYYMMDD strings only.
period = source.filter(F.col("yearmonthday").between("20240101", "20240131"))
```

Avoid casting or wrapping partition columns in functions without checking whether the source can still prune. A combined date column, a directory partition column and an Iceberg partition transform are different contracts. Inspect actual schema and table format first.
