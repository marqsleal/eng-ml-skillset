# Logging guidance and examples

These examples describe event intent and JSON records, not a required library, field naming standard, or format for every environment. Match existing project and collector conventions.

## Event design

Give an event a stable name and describe what happened in plain language. Capture enough context to distinguish the operation and outcome, and add a duration when it helps diagnose latency. Prefer timestamps in UTC or with an explicit offset; use a monotonic clock for measuring elapsed time. Trace and span identifiers are optional and should come from the active tracing context.

Good: a single structured event for a failed operation, with safe identifiers and a bounded error classification:

```json
{"timestamp":"2026-01-15T12:34:56Z","severity":"ERROR","event":"payment.authorization.failed","message":"Payment authorization failed","service":"checkout","request_id":"req-42","error_type":"provider_timeout","duration_ms":1200}
```

Bad: `ERROR Something went wrong token=secret` — no useful operation or cause, and a credential is exposed. Avoid building a message from arbitrary input or dumping entire objects, requests, responses, rows, or configuration. Fields such as user IDs and IP addresses can be personal data; include them only when justified and authorized.

Keep types stable across events (`duration_ms` is numeric, for example), document units, and avoid changing established event names or fields without considering dashboards and consumers. High-cardinality identifiers can be valuable in logs but costly for indexes; do not automatically use them as metric labels.

Choose event fields by asking what happened, when and where it happened, and which operation or actor was involved, subject to data minimization. For important operations, include an outcome and a safe reason or error classification. Record the event time, not merely the time at which a collector received it; these can differ.

## Severity and exceptions

| Situation | Typical level | Notes |
| --- | --- | --- |
| Startup complete or a meaningful batch completed | INFO | Include outcome and counts where useful. |
| A transient retry that succeeds or an optional fallback | DEBUG or WARN | Choose according to impact and frequency. |
| An operation ultimately fails | ERROR | Record actionable context at the handling boundary. |
| A process cannot continue | FATAL / CRITICAL | Only if the framework and process semantics support it. |

Include a stack trace when it helps investigate an unexpected failure and its contents are safe. Preserve the original exception when propagating it; log once at a boundary that has enough context unless a separate event is operationally justified. Do not catch an exception merely to log it and silently continue, or include exception text blindly: it can contain SQL, payloads, credentials, and paths.

## Security and lifecycle

- Select fields by allowlist when practical. Redaction is defense in depth, not permission to capture all data. Consider privacy requirements even for debugging and test output.
- A JSON encoder must escape embedded newlines and other control characters; validate size limits and downstream rendering too. Structured output does not automatically protect an unsafe sink or viewer.
- Protect logs in transit and at rest, restrict and monitor access, and define retention and deletion according to applicable requirements. Rotate files only where the application owns files; managed collectors may own rotation and retention.
- Separate diagnostic and security/audit needs where required. Audit events may need integrity, completeness, access controls, and retention beyond ordinary logging. Define explicit behavior for sink outages based on the service's availability and audit obligations; do not universally fail open or fail closed.
- Where appropriate, capture security-relevant outcomes such as authentication and authorization failures, configuration changes, and access to sensitive operations. Record enough context to investigate without recording credentials or unnecessary personal data. Ensure the chosen filtering and delivery policies preserve required events.

## Volume, correlation and tests

In high-throughput or distributed processing, prefer one summary per logical job or batch over logging every row or worker action. Avoid collecting data or triggering an expensive action solely for logging. Define what happens to buffered asynchronous logs on crash, overload, and shutdown; lossless delivery requires an explicitly designed mechanism. Sample repetitive diagnostics only after accounting for detection and audit needs.

For a traced request or job, propagate context using the existing framework and attach valid trace/span IDs when available. A request ID is useful correlation context but is not automatically a trace ID. Logs complement metrics and traces; choose signals and alerts based on what the team needs to observe.

Test with synthetic inputs: verify an important failure emits the expected event and level, that sensitive values do not occur in the emitted record, and that newline-containing untrusted input cannot forge another record. Test retries and failure paths if they affect audit completeness or error duplication. Avoid brittle assertions on incidental wording, timestamps, or complete formatted stack traces. Automated test artifacts and CI logs need the same data minimization as production logs.

