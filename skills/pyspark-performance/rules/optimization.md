# Measure, then optimize

Adapted from `spark/performance-tuning.md`, `spark/spark-performance.agent.md` and `spark/spark-sql-dataframes.md`.

1. Compare equivalent inputs, output correctness, runtime and resource consumption. Identify version, AQE settings, source statistics and whether the job is batch or streaming.
2. Inspect `df.explain("formatted")`, optimized/physical plans and the executed adaptive plan when available. Look at `PartitionFilters`, `PushedFilters`, `ReadSchema`, `Exchange`, join strategy and Python execution nodes. A pushed filter in a plan alone does not prove effective pruning or low I/O.
3. When runtime metrics are already accessible, check SQL/stage duration, bytes and files read, shuffle read/write, spill, task duration distribution, executor memory and GC; otherwise state that these measurements are unavailable. Compare median and slowest tasks to investigate skew. Report evidence and what would confirm a hypothesis.
4. Project required columns and filter early when semantics permit. Catalyst may push projections even if written later; inspect the plan. Avoid repeated full actions such as `count` unless required. `limit` bounds output, not necessarily input scans, sorts or shuffles.
5. Let the optimizer choose joins with reliable statistics; consider broadcast only when the actual build side fits driver/executor memory and network budget. Confirm the executed strategy. Never assume a fixed size threshold is universally safe.
6. AQE can coalesce shuffle partitions and mitigate some skew joins; availability and effects vary by version and operation. A hot key can still dominate an aggregation. Consider selective salting or splitting hot keys only after measuring and preserving join multiplicity and null semantics.
7. Cache only reused expensive intermediates after considering recomputation, memory, materialization and source changes; inspect Storage and `unpersist()` after use. Caching is not durable checkpointing.

For review, cite relevant lines and rank findings by likely impact, evidence and risk; offer concrete checks and next steps. Do not write a review report file unless requested or established by the project.

References: [Spark SQL performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html), [Spark tuning](https://spark.apache.org/docs/latest/tuning.html).
