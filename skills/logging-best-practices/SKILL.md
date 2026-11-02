---
name: logging-best-practices
description: Design, implement, review, or test application logging across languages, including structured events, severity, security, correlation, and operational cost.
---

# Logging best practices

Apply this guidance alongside the relevant language, framework, and testing skills. Inspect existing logging conventions, sinks, and operational requirements first; reuse the project's logger and configuration. Do not introduce a dependency, logging platform, or infrastructure change unless justified by the task.

## Design and implementation

- Decide which operational, business, and security events are useful to diagnose a problem or meet an explicit audit requirement. Log meaningful state transitions and failures, not every function call or record.
- Prefer structured events when supported by the existing environment. Use stable event names, a concise human-readable message, appropriate severity, event time with timezone, and minimal context such as service, operation, outcome, and safe correlation identifiers. Match the existing schema and collector; do not claim illustrative field names are a standard.
- Select severity by impact and recovery: DEBUG/TRACE for diagnostic detail, INFO for meaningful expected events, WARN for an unexpected but handled condition, ERROR for a failed operation, and FATAL/CRITICAL for unrecoverable process failure where supported. Expected business outcomes need not be errors. Avoid logging and rethrowing the same failure at every layer.
- Treat all external input as untrusted. Never log secrets, passwords, access tokens, session credentials, or raw authorization headers. Exclude sensitive or personal data unless explicitly necessary and permitted; minimize and protect any approved fields. Do not assume hashing or masking automatically makes data anonymous or safe.
- Use a proper structured encoder to escape control characters and delimiters, bound untrusted values, and prevent forged records. Parameterization alone is not a log-injection defense. Scrutinize exception messages, stack traces, URLs, query parameters, headers and payloads for sensitive data.
- Correlate with existing request/job identifiers and, when available, trace and span context. Do not invent trace identifiers or use personal data as correlation keys. Include relevant context without duplicating it throughout every message.
- Control cost and latency: use level checks or lazy parameter evaluation for expensive values, aggregate repetitive events and consider bounded sampling or rate limiting for high-volume diagnostics. Do not sample away required audit or security events. Define backpressure, loss and shutdown behavior if asynchronous logging is used.
- Configure levels at the application boundary and keep libraries from unexpectedly configuring global sinks. Follow the environment's collection, access, transmission, retention and rotation policies; recommend changes only when in scope. Do not equate ordinary diagnostic logs with a compliant audit trail.
- Test behavior when it matters: meaningful event and severity, safe context, redaction and encoding of hostile input, and no duplicate error records. In automated tests avoid secrets and real customer data, keep output bounded, and preserve failure diagnostics without exposing fixtures or credentials. Validate logging failures and audit guarantees when these are requirements.

For concrete examples, edge cases, and operational tradeoffs, read [logging examples and guidance](references/logging-guidance.md).

For investigating existing application or service logs on AWS, use `aws-logging-exploration`.
