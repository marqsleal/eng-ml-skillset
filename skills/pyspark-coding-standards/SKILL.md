---
name: pyspark-coding-standards
description: Write, review, or refactor PySpark DataFrame and Spark SQL transformations and batch pipelines with correct distributed semantics.
---

# PySpark coding standards

Establish the Spark, Python, connector and execution environment versions and the input/output contracts. For structured data prefer DataFrames and built-in functions; use RDDs only when they solve a concrete need. Transformations are lazy: actions and writes execute work. Keep transformation functions separate from I/O and orchestration when practical.

- Read [DataFrames and SQL](rules/dataframes.md) for schemas, joins, nulls, windows, SQL, formatting and RDD tradeoffs.
- Read [recipes](rules/recipes.md) for dates, regex, partitions and readable transformation examples.
- For writing and validating Spark SQL independently of the host language, use `sql-spark-coding-standards`.
- For Spark execution plans and tuning use `pyspark-performance`; for automated tests use `pyspark-testing`; for streaming use `pyspark-streaming`.
- Respect existing project conventions. Don't read production datasets, submit remote jobs, write tables or change cloud resources just to validate a code change. Do not recommend or start local Spark execution. Prepare bounded synthetic fixtures for an existing authorized test environment when execution is requested; otherwise perform static review.
