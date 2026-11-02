# Partitions, files and Python

Adapted from `spark/partitioning-caching.md` and `spark/rdd-operations.md`.

- Distinguish physical input files, storage partition columns and in-memory/shuffle partitions; tuning one does not automatically set the others. Measure task sizes and parallelism against executor capacity.
- `repartition` redistributes with shuffle; `coalesce` generally reduces partitions without a full shuffle, but can leave skew and limit parallelism. Neither guarantees a particular number of output files, especially with partitioned writes, retries or writer settings. Never force one partition merely to obtain one file at scale.
- Choose storage partition keys from real predicates, cardinality and file sizes. Over-partitioning produces small files; compaction writes data and must only run on an authorized target. Filtering partition columns may enable pruning; verify source support and actual plan.
- Prefer native Spark functions, then evaluate a Python UDF only when needed. `pandas_udf` processes vectorized batches, `mapInPandas` processes iterators of pandas batches, and `applyInPandas` groups and shuffles data; a large skewed group can exhaust worker memory. Check available APIs and dependencies. Arrow batch-size settings may help for `mapInPandas`, but do not guarantee a bound for grouped operations.
- Do not blindly convert to RDDs or move datasets to the driver; use distributed operations. Built-in functions, Arrow and caches have workload-dependent costs: benchmark with representative inputs.
