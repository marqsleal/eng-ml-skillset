# Athena SQL design and review

- Confirm table grain, keys, data types, nullability assumptions, time zone and desired result grain before choosing joins and aggregates. Highlight uncertainty rather than inventing a schema.
- Use explicit columns and clear aliases. Qualify ambiguous columns; format joins, filters, and expressions so the data flow is readable. Use CTEs where they clarify logic, without assuming they materialize.
- Select join types deliberately; check key cardinality and fan-out before aggregation. Handle NULL explicitly, including `NOT IN` and comparisons. Avoid using `DISTINCT` to conceal an incorrect join.
- Define time boundaries and time zones; use appropriate casts and typed literals. Preserve filters on partition keys where needed. Validate syntax and function support against the effective Athena engine and table format.
- For window functions specify partitioning, ordering, tie-breakers and frame where behavior requires them. Explain non-deterministic sampling or ordering. Guard division by zero and test edge cases with representative inputs.
- When reviewing, report concrete correctness, security, and performance findings with evidence, impact, and a proposed fix. Treat SQL injection and sensitive results according to the actual input and access boundaries. Do not prescribe relational indexes or dialect-specific syntax without evidence Athena supports them.
- For generated DDL/DML, distinguish a proposed file from an executed operation. During testing and exploration never execute such statements through AWS CLI. See [exploration](../../../sql-athena-exploration/SKILL.md).
