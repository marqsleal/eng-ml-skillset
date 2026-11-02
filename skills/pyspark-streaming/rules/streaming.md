# Structured Streaming patterns

Adapted from `spark/streaming-patterns.md`. Validate operations, output modes, sink and trigger compatibility for the installed version; support differs between micro-batch and continuous modes.

```python
from pyspark.sql import functions as F

# events is an existing streaming DataFrame with event_time and event_id.
window_counts = (
    events.withWatermark("event_time", "10 minutes")
    .groupBy(F.window("event_time", "5 minutes"))
    .count()
)
```

A watermark is based on observed event time and is not a wall-clock timer or a promise that every later record is dropped. Choose lateness from the business contract. State cleanup depends on the operator, watermark placement and output mode; some stateful operations can grow indefinitely even with a watermark. Append window results may be delayed until watermark progress. For deduplication understand the key and watermark semantics; `dropDuplicatesWithinWatermark` requires a watermark and is available in Spark 3.5+, subject to runtime support.

Stream-stream joins require appropriate event-time constraints and watermark configuration for bounded state and outer-join output; validate supported join types and modes. Stream-static lookup freshness depends on source and execution environment, not an automatic refresh guarantee.

Use a stable, unique checkpoint per query at a durable location, compatible with its source and sink. Checkpoint encodes offsets, progress and possibly state; never share or delete it as a casual recovery step. Some query changes are incompatible with checkpoint reuse; plan migration and replay with the operator. Protect checkpoint contents.

`foreachBatch` is micro-batch only and may run again for a batch after failure: implement idempotent/transactional writes keyed by batch ID or source offsets and sink semantics. A checkpoint alone does not make an arbitrary sink exactly-once. Ensure batch code handles empty batches and completely consumes stateful batch output where required. Avoid unsafe external side effects in executor callbacks.

When execution is requested in an existing authorized test environment, test using bounded synthetic events and isolated checkpoint/output directories: in-order and late arrivals, duplicates, state and watermark progress, failure/restart and sink idempotency. Assert only guarantees of the actual source/sink; avoid sleeps as the sole synchronization mechanism. Monitor input and processing rates, batch duration, state size, watermark progress and failures.

Reference: [Spark 3.5 Structured Streaming](https://spark.apache.org/docs/3.5.6/structured-streaming-programming-guide.html); consult the documentation matching your deployed Spark version.
