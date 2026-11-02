---
name: sql-athena-coding-standards
description: Write or review SQL for Amazon Athena, including query correctness, readability, and engine-specific behavior.
---

# Athena SQL standards

Use the actual catalog schema and effective Athena engine version; do not invent tables, fields, relationships, or dialect features. Follow existing project conventions. For Athena SQL design and review, read [SQL design](rules/sql/guide.md).

- For reusable read-only queries and good/bad examples, read [query patterns](rules/query-patterns/guide.md).
- For human-readable layout, indentation, spacing and formatting examples, read [SQL formatting](rules/formatting/guide.md).
- For parsing, ranges, time zones and regular expressions, read [dates and regex](rules/dates-regex/guide.md).
- For temporal partition layouts and pruning, read [partition patterns](../sql-athena-performance/rules/partition-patterns/guide.md).
- For window functions, retention cohorts and ordered funnels, read [analytics patterns](rules/analytics/guide.md).
- For structured reviews and common failure symptoms, read [review and debugging](rules/review/guide.md).

For exploration and testing, follow [exploration guardrails](../sql-athena-exploration/SKILL.md). Never execute table or data mutations through AWS CLI during those workflows, including SQL in a file or script. Writing SQL for later review is allowed.
