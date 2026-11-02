---
name: sql-spark-coding-standards
description: Write, review and validate Spark SQL queries for Spark SQL interfaces, notebooks, applications or SQL files, independently of the host language.
---

# Spark SQL: construction and validation

Use this skill for Spark SQL in SQL files, SQL CLI, notebooks or any Spark application, including `spark.sql`. Determine the actual Spark and distribution version, SQL configuration, catalog, table schemas, business grain and permitted execution environment. Do not invent columns or assume Athena/Trino syntax applies to Spark SQL.

- Read [query design and formatting](rules/design.md) for semantics, structure, readability and query review.
- Read [SQL recipes](rules/recipes.md) for joins, windows, dates, regex and partition predicates.
- Read [validation](rules/validation.md) to validate semantics, SQL compatibility and plans with bounded synthetic data before considering actual data.
- For runtime bottlenecks and execution metrics, also use `pyspark-performance`; its plan principles apply to Spark SQL regardless of host language. For embedding in Python and application testing, use `pyspark-coding-standards` and `pyspark-testing` when relevant.

SQL files can contain commands that change state. Inspect the entire statement and execution method before running it. Do not recommend or start local Spark execution. Prepare isolated, read-only synthetic fixtures; use an existing authorized test environment only when execution is requested. Do not execute writes, submit remote jobs or access live data merely to validate a query. Follow existing project authorization and environment boundaries; planning and `EXPLAIN` can still access catalogs or external metadata. Never execute Athena table/data mutations through AWS CLI during exploration or tests.
