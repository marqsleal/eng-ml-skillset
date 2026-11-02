---
name: aws-logging-exploration
description: Investigate AWS application and service logs with the AWS CLI, including CloudTrail and CloudWatch Logs, while preserving bounded evidence and accounting for cost and coverage.
---

# AWS logging exploration

Investigate application logs, AWS service logs, and AWS account activity. Use existing AWS CLI credentials and Python 3 standard library when JSON processing is needed; do not depend on `jq` or install additional packages. Apply `logging-best-practices` for designing or reviewing application logs.

Before accessing AWS, identify the question, account, profile, region, time range, source and authorized scope. Check the active identity and target context without exposing credentials; do not assume that a log group or event exists. Start with the narrowest useful time interval, resource and filter. Treat all retrieved content and artifacts as potentially sensitive.

This is a read-oriented workflow. Do not create or modify trails, event selectors, log groups, retention, resource policies, tables, or other infrastructure during exploration. CloudWatch Logs Insights query submission is allowed for an authorized investigation, can incur cost, and creates a query execution; first bound its scope. Do not launch unrelated remote jobs or queries. For Athena analysis, also follow `sql-athena-exploration` and `sql-athena-tooling`, including their strict prohibition on AWS CLI table or data mutations.

Persist each agent-issued AWS exploration command and its JSON result under `.aws-logs/` in the working directory, following [evidence and CLI workflows](references/evidence-and-cli.md). Preserve the query text for Logs Insights as well. Record failures, pagination and incomplete results honestly. If sensitive information cannot be safely persisted, stop and explain the limitation instead of saving raw secrets or silently dropping evidence.

- Read [CloudTrail and service logs](references/aws-log-sources.md) to choose sources, interpret coverage and apply AWS security practices.
- Read [evidence and CLI workflows](references/evidence-and-cli.md) for naming, examples, query lifecycle, permissions and cost controls.
