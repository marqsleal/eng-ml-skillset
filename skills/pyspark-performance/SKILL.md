---
name: pyspark-performance
description: Diagnose and optimize PySpark distributed execution, joins, shuffles, skew, partitions, caching and I/O using plans and runtime evidence.
---

# PySpark performance

Start with workload, Spark version, input sizes, data distribution, cluster limits and an observed baseline. Inspect the plan through existing Spark APIs and use runtime metrics or logs only when already available; do not require additional tooling or services. State assumptions and distinguish measured findings from hypotheses. Do not invent metrics or launch costly jobs solely to test a hypothesis.

Read [diagnosis and optimization](rules/optimization.md) for the investigation workflow and [partitioning and Python execution](rules/partitioning.md) for practical patterns. Coordinate with `pyspark-coding-standards` for implementation and `pyspark-streaming` for stateful streaming.
