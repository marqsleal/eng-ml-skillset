---
name: pyspark-testing
description: Test PySpark DataFrame transformations, batch jobs and integration boundaries using synthetic fixtures and deterministic assertions in an existing authorized test environment.
---

# PySpark testing

Design tests around small synthetic datasets and mock external services at boundaries, not DataFrame operations. Do not recommend or start local Spark execution. Run Spark tests only in an existing authorized test environment when execution is requested; otherwise review and prepare tests without claiming execution. Read [testing patterns](rules/testing.md) for fixtures, assertions and edge cases. For streaming-specific recovery and event-time tests also use `pyspark-streaming`.
