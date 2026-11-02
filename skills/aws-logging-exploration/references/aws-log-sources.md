# AWS log sources and investigation practices

## CloudTrail: AWS activity

CloudTrail records supported AWS API and account activity initiated by users, assumed roles and AWS services. Choose it to investigate who called an API, what operation and resource were involved, where, when, and whether the call reported an error. Relevant event fields include `eventTime`, `eventSource`, `eventName`, `awsRegion`, `userIdentity`, `sourceIPAddress`, `requestID`, `requestParameters`, `responseElements`, `errorCode`, and `errorMessage`; availability varies by event and service. Event identity may represent an assumed role or an AWS service rather than the original human. Inspect session context and related events before attributing an action. `lookup-events` returns the detailed `CloudTrailEvent` as a JSON-encoded string: parse it with a JSON parser rather than assuming it is already an object.

Event history is regional and account-specific, covers the last 90 days of management events, and is independent of configured trails. A lookup can filter by a single supported attribute plus time. Recent Insights events are separately queried when configured. Event history does not cover data events; management event coverage alone cannot establish S3 object access, Lambda invocations, or all network activity. Data events, network activity events and Insights depend on configuration, service support and the selected source. Log files can arrive with delay and are not guaranteed to be ordered. For older or other event types inspect existing trail delivery, S3 locations, CloudWatch integration, or an existing event data store when authorized; absence in one source is not proof no action occurred.

Check relevant trail configuration, status and event selectors using read-only APIs when needed: account and region coverage, organization or multi-region settings, enabled event types and delivery status. A trail may deliver to S3 and optionally to CloudWatch Logs; neither implies all event types were enabled. Avoid broad S3 scans or costly Lake/Athena queries merely to establish coverage. An existing CloudTrail Lake store may offer broader queries if available, but treat its queries as potentially billable and verify its actual configuration.

## Applications and AWS services

CloudWatch Logs is a collection and analysis destination, not a guarantee that a service publishes its logs there. Discover existing log groups using a narrow prefix and verify the group belongs to the intended account, region, service and environment. Inspect the configured destination and retention before drawing conclusions. A CloudTrail event describes a supported API action; it is not automatically the workload execution log or network traffic log.

Select the source for the question:

| Question | Candidate evidence | Limitation |
| --- | --- | --- |
| Who changed a resource or invoked a supported API? | CloudTrail management or configured data events | Account, region, event type, delivery and selectors determine coverage. |
| Why did a Lambda invocation, container or application fail? | Existing application/runtime logs in CloudWatch Logs or the configured destination | Logs exist only if emitted and delivered; execution role and tracing context may differ from the caller. |
| Was network traffic accepted or rejected? | Existing VPC Flow Logs in their configured destination | Records describe observed flow metadata, not full packet contents or every possible traffic path. |
| What happened to a database or load balancer request? | Existing engine/service or access logs in CloudWatch Logs or S3 | Availability, content, configuration and delivery delay vary by service. |

Correlate by event and ingestion times, account, region, resource, request ID and trace context where available. These IDs have different scopes and may be absent; do not assume they are interchangeable. Record timezone and possible delivery delay. Logs may be filtered, incomplete, sampled or retained for less time than the investigation requires.

## Security and operational recommendations

When asked to assess logging configuration, consider multi-region and organization coverage, a separate restricted log archive account or bucket, encryption in transit and at rest, least-privilege access, retention, delivery monitoring and alerting, and CloudTrail log file integrity validation. Verify whether these are already configured and suited to the requirements; recommend changes instead of applying them as part of exploration. Integrity validation depends on existing digest files and the covered interval; an unvalidated or incomplete interval is not proof of tampering or completeness. Enable relevant data events selectively because event volume and cost can be substantial. Never enable logging or change permissions merely to complete an investigation without explicit authorization.
