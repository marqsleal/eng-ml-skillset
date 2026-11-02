# DataFrames, SQL and distributed correctness

Adapted from `spark/spark-sql-dataframes.md` and `spark/rdd-operations.md`. Check behavior against the deployed Spark version and platform.

- Define an explicit source schema where appropriate for CSV/JSON; for Parquet or catalog tables inspect the existing schema and evolution policy instead of imposing one blindly. A schema is not a replacement for validation: parsing, nullability and malformed records depend on the source and settings.
- Keep transformations in functions accepting and returning DataFrames. Name intermediate steps, use `functions as F`, parentheses and one logical operation per line. Alias join inputs; select explicit output columns to prevent ambiguous names.
- Use built-in expressions before Python UDFs. A Python UDF has serialization/runtime costs and special null/error behavior; choose it only for logic that cannot reasonably be expressed natively. Verify executor dependencies.
- Define join cardinality and null semantics, including duplicate keys. Use semi/anti joins for existence tests. Deterministic `row_number` requires a total ordering and a tie breaker; `dropDuplicates` does not promise which duplicate survives.
- SQL strings should use readable indentation, one selected expression per line, explicit joins and qualified names. Do not interpolate untrusted values or identifiers; use supported parameter binding or validate identifiers for the deployed version.
- Avoid `collect()`, `toPandas()` and local Python loops for large or unbounded data. `limit(10).collect()` bounds returned rows, not bytes scanned or intermediate shuffles, and rows can still be large. Avoid logging sensitive values.
- Executors can retry tasks: do not assume `foreach` or `foreachPartition` side effects run exactly once; design idempotent writes when explicitly required. Driver-side threading does not replace distributed transforms, although bounded concurrency can be appropriate for unrelated driver I/O.
- RDD conversion loses DataFrame optimization and is not available in all environments (including Spark Connect). For legacy pair RDDs prefer `reduceByKey` to `groupByKey` for associative/commutative aggregation when semantics allow. Avoid materializing entire partitions.

```python
from pyspark.sql import DataFrame, functions as F


def active_order_totals(orders: DataFrame, customers: DataFrame) -> DataFrame:
    active = customers.filter(F.col("active") == F.lit(True)).select("customer_id")
    return (
        orders.join(active, on="customer_id", how="left_semi")
        .groupBy("customer_id")
        .agg(F.sum("amount").alias("total_amount"))
    )
```

The semi join avoids multiplying orders if the customer input has duplicate IDs. Specify decimal type, overflow and null handling according to the data contract.
