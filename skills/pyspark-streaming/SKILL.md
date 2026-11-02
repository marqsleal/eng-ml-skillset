---
name: pyspark-streaming
description: Design, implement, test or troubleshoot PySpark Structured Streaming pipelines, event time, watermarks, state, sinks and recovery.
---

# PySpark Structured Streaming

Establish source/sink, Spark and connector versions, event-time semantics, lateness, delivery guarantees, checkpoint ownership and operational latency before choosing a pattern. Read [streaming patterns](rules/streaming.md). Use `pyspark-performance` for measured batch/cluster bottlenecks and `pyspark-testing` for test design.

Never start a real stream, create or delete checkpoints, or write to a live sink just to validate a change. Do not recommend local Spark execution. Use an isolated, specifically authorized test environment only when execution is requested.
