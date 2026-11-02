# Designing readable, correct Spark SQL

Adapted from `spark/spark-sql-dataframes.md` and `spark/performance-tuning.md`. Establish the source and target grain, key uniqueness, filters, null rules, types, timezone and expected result before building a query. Check schema and view scope in the permitted catalog; ask for missing business semantics rather than inventing them.

1. Express each meaningful step with a clearly named CTE when that makes the logic easier to follow. A CTE improves readability but does not guarantee caching or materialization.
2. Use uppercase SQL keywords, four-space indentation, one selected expression per line, descriptive aliases and explicit `JOIN ... ON`; qualify ambiguous columns. Follow existing project formatting if it differs.
3. Select only needed columns in the result. Define cardinality and match semantics; duplicates in either side can multiply rows. Use `LEFT SEMI JOIN` / `LEFT ANTI JOIN` for existence or absence when appropriate.
4. Choose grouping grain deliberately. In outer joins, moving a right-side predicate from `ON` to `WHERE` can remove unmatched rows. `COUNT(*)` counts rows and `COUNT(column)` counts non-null values. `NULL` comparisons use three-valued logic; use `IS NULL` or Spark's null-safe equality `<=>` when the business contract calls for it.
5. For window functions define partitions, ordering, tie-breakers, null ordering and frame. An `ORDER BY` without a unique tie-breaker is not deterministic. Use explicit `ROWS` when row-based cumulative semantics are intended.
6. `ORDER BY` establishes a global order and can be expensive; `SORT BY` only sorts within partitions. Without ordering, a result or `LIMIT` sample has no stable order. Do not assume output file ordering.
7. Spark uses backticks for delimited identifiers. Confirm catalog and case-sensitivity configuration; use fully qualified names where supported. Use safe parameter binding where the interface and version support it; do not interpolate untrusted input or treat value parameters as identifiers. Validate dynamic identifiers against an allowlist.

Review examples against the deployed dialect and ANSI settings: `spark.sql.ansi.enabled`, timezone and case sensitivity can change interpretation or errors. Reserved keywords and platform extensions are version-dependent.

References: [Spark SQL SELECT](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select.html), [identifiers](https://spark.apache.org/docs/latest/sql-ref-identifier.html).
