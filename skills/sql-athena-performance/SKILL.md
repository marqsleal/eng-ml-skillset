---
name: sql-athena-performance
description: Analyze or improve Amazon Athena query performance, scanned data, execution plans, and cost drivers.
---

# Athena performance

Base recommendations on actual table metadata, query plans and execution statistics; state assumptions and avoid claiming a cost reduction without evidence. Read [optimization](rules/optimization/guide.md). For live tests or exploration also follow [exploration guardrails](../sql-athena-exploration/SKILL.md): never execute table or data mutations via AWS CLI in those workflows, even to benchmark an optimization.

For concrete date-partition filters, including separate year/month/day keys and a single date key, read [partition patterns](rules/partition-patterns/guide.md).
