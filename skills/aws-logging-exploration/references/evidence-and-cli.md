# Evidence and AWS CLI workflows

## Evidence contract

Create `.aws-logs/` under the agent's working directory before the first AWS call. Store a numbered command script and valid JSON result for each agent-issued AWS command, including identity and discovery calls. Use:

```text
00X__service__resource__context.sh
00X__service__resource__context.result.json
```

Use a zero-padded increasing sequence (`001`, `002`, ...), short lowercase filesystem-safe components, and at most three short words for context, separated by underscores. Use `account` or `general` when no individual resource applies. Never overwrite existing evidence; continue from the next available sequence. A script contains the actual reproducible command and safe, explicit parameters, not credentials or secret-bearing values. Keep each command independently attributable; do not hide additional AWS calls in command substitutions or unrecorded scripts. For Insights also persist the exact query text beside the script as `00X__service__resource__context.query` and refer to it from the script.

Write one valid JSON document per result file. Preserve the response or an explicitly described safe redacted form together with status, account/profile/region and UTC interval when known, command exit status, retrieval time, pagination or truncation state, and the reason for any incompleteness. An envelope with `status`, `context`, `response`, and `error` is acceptable. A successful empty response differs from an error, a partial response, or a timeout. Never put error text or AWS CLI output directly into a `.result.json` unless properly JSON-encoded. Do not invent missing events. When an API returns a continuation token or a CLI `--max-items` cap is reached, record the available token and mark the result incomplete unless completion is established. Continue with explicitly recorded bounded pages only as needed; CLI pagination tokens must be resumed using the appropriate CLI options and the same original filters.

Use restrictive file and directory permissions where supported (for example, `umask 077`). Apply existing data handling policy before persisting; CloudTrail event parameters, log messages, identity information and even pagination tokens can be sensitive. Exclude credentials and secrets from scripts, filenames, terminal output and persisted results. If the response includes secrets, use an approved local redaction process before persisting and label the artifact redacted; do not falsely present it as an unmodified forensic original. If safe handling or required preservation cannot be reconciled, stop and report the limitation. Do not commit artifacts automatically. Record access restrictions and material transformations when evidence integrity matters; these files alone do not establish chain of custody.

## Discovery and CloudTrail

The following command bodies are examples to save in distinct numbered `.sh` artifacts and execute with the evidence contract above. Replace placeholders with verified, non-secret values and capture each command's exit status and JSON output separately. `AWS_PAGER` prevents an interactive pager. Do not embed credentials. Use profile only if the environment uses named profiles.

```sh
AWS_PAGER='' aws sts get-caller-identity --profile example --region us-east-1 --output json
```

```sh
AWS_PAGER='' aws cloudtrail lookup-events \
  --profile example --region us-east-1 \
  --start-time 2026-01-15T12:00:00Z --end-time 2026-01-15T13:00:00Z \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=iam.amazonaws.com \
  --max-items 10 --output json
```

CloudTrail lookup returns at most 50 records per service page, and requests are throttled per account and region. `--max-items` bounds CLI output but may yield a continuation token; it does not prove the interval was fully examined. One lookup supports one attribute filter. An empty page is only evidence about that account, region, time and filter, subject to coverage and delivery delays. To inspect escaped `CloudTrailEvent` JSON, use `json.loads` from Python's standard library after safely loading the outer JSON.

```sh
AWS_PAGER='' aws logs describe-log-groups \
  --profile example --region us-east-1 \
  --log-group-name-prefix /aws/lambda/example --max-items 10 --output json
```

For direct event retrieval, `filter-log-events` can use a specific log group, start and end time in Unix milliseconds, a filter pattern and bounded pagination. Verify the service's filtering semantics and preserve pagination state; a partially full or empty page is not necessarily the final page. `--limit` controls returned events, not a guarantee of full coverage.

## CloudWatch Logs Insights

Choose known existing log groups and a tight UTC time window. Querying scans data and may incur charges; a result `limit` bounds returned rows, not necessarily bytes scanned. Avoid broad groups, long windows, repeated polling and expensive queries. Group class, query language, region, permissions, concurrency and retention affect availability and behavior. Prepare a query file with minimal fields, for example:

```text
fields @timestamp, @message, @logStream
| filter @message like /ERROR/
| sort @timestamp desc
| limit 10
```

`ERROR` is an illustrative text filter, not a guarantee that every error is captured. A request may be sensitive even after selecting fields; restrict output accordingly. Save the query file and a separate script per AWS CLI operation. For `start-query`, use explicit Unix **seconds** for start and end and the exact persisted query content, then persist its JSON response and query ID. A shell script can load the query file without making an extra AWS call:

```sh
AWS_PAGER='' aws logs start-query \
  --profile example --region us-east-1 \
  --log-group-name /aws/lambda/example \
  --start-time 1768478400 --end-time 1768482000 \
  --query-string "$(cat .aws-logs/003__cloudwatch__example__recent_errors.query)" \
  --output json
```

Use the returned query ID in separately persisted `aws logs get-query-results` commands. Poll at a bounded, reasonable interval and stop after a finite deadline; preserve each response and its status. `Scheduled` and `Running` results are partial, not final. Treat `Complete` as successful execution, while noting result limits and any returned statistics; `Failed`, `Cancelled`, `Timeout`, `Unknown`, API errors and a local polling deadline are not complete results. Report query ID, exact time window, log groups, status, relevant scan statistics and limits. A local timeout does not imply the remote query stopped; stopping it is a separate state-changing action and requires appropriate authorization. Do not automatically issue a cancellation.
