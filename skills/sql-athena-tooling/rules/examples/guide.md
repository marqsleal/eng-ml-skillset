# Result contract and CLI examples

Use these templates only after verifying target account, region, permissions, workgroup, schema and cost. SQL here is read-only; before submitting any other file inspect its entire contents and execution path. No example authorizes table/data mutations during testing or exploration. Make `.aws-athena/` under the agent's working directory, choose a fresh sequential stem, and persist the exact request before running it. Never put secrets in artifacts, arguments or error messages. Do not overwrite an existing pair.

## Common JSON envelope

Every `.result.json` is a JSON object with these keys; use JSON `null` when unavailable, not invented values:

```json
{
  "schema_version": 1,
  "status": "SUCCEEDED",
  "artifact": "002__sales__orders__sample.sql",
  "context": {"account_id": null, "region": "us-east-1", "catalog": "AwsDataCatalog", "database": "sales", "workgroup": "analytics"},
  "query_execution_id": null,
  "execution": null,
  "data": null,
  "pagination": {"complete": true, "next_token": null},
  "error": null
}
```

`status` is `SUCCEEDED`, `FAILED`, `CANCELLED`, `RUNNING`, `QUEUED`, or `UNKNOWN`. For Glue success, `data` contains the complete CLI JSON response; `query_execution_id` and `execution` are null. For Athena, `query_execution_id` is the ID if received, `execution` contains the `QueryExecution` object returned by `get-query-execution`, and `data` contains the complete `get-query-results` JSON including metadata and rows. A failed API call uses `error` as an object with `stage`, numeric `exit_code` when available, and sanitized `message`; an Athena failure also retains its status reason and statistics in `execution`. A successful query with failed result retrieval must have `status: FAILED` and `error.stage: "get-query-results"`, while `execution.Status.State` remains `SUCCEEDED`.

On polling timeout, retain the ID and latest execution, record the last known `RUNNING` or `QUEUED` state (or `UNKNOWN` if unknown), `data: null`, `pagination.complete: false`, and an error with `stage: "poll_timeout"`. It is not a success or a cancellation. Preserve an interrupted attempt and update its own result when resuming the same execution ID; do not submit a new query merely because polling timed out. For a truncated page set `pagination.complete: false` and `next_token` to the applicable CLI continuation token. A failed request has incomplete pagination, not an empty successful dataset. Write valid JSON atomically and retain a valid failure envelope even if submission or retrieval fails. Redact secrets from error text.

## Glue command artifacts

Each file below represents a **separate** request, with its own unused sequence and result. Replace names and region after discovery; `--catalog-id` may be needed for a different Glue catalog. AWS CLI JSON output normally auto-paginates unless disabled or capped. Verify whether results are complete and capture a continuation token when intentionally limited. Quote arguments and avoid `--output text` pagination surprises.

```sh
#!/bin/sh
aws glue get-tables --database-name sales --region us-east-1 --output json --no-cli-pager
```

```sh
#!/bin/sh
aws glue get-table --database-name sales --name orders --region us-east-1 --output json --no-cli-pager
```

```sh
#!/bin/sh
aws glue get-partitions --database-name sales --table-name orders \
    --expression "year='2025' and month='03'" --region us-east-1 \
    --output json --no-cli-pager
```

Save each complete snippet as its own `.sh` artifact, run that file, and capture stdout, exit status and sanitized stderr separately. Wrap parsed JSON stdout in the common envelope only on success; on failure set `data` to null and record the error. Do not pipe directly to the `.result.json`: the raw CLI output is not the envelope and an error could leave invalid or empty JSON. A filter must use verified partition keys and Glue expression syntax. An empty registered-partition result does not establish absence of projected partitions or objects.

## Athena request lifecycle

For example, persist this as `002__sales__orders__sample.sql` before submission, replacing the identifiers and partition filter with verified values:

```sql
SELECT order_id, customer_id
FROM "sales"."orders"
WHERE order_date = '2025-03-01'
LIMIT 10;
```

Then use the **same exact file** in the CLI after read-only and cost review. `file://` is AWS CLI's file-parameter syntax, not a shell substitution; use Python 3 standard-library JSON handling if structured processing is needed. Explicitly set `AWS_PROFILE` if a non-default profile is required, after verifying identity.

```sh
aws athena start-query-execution \
    --query-string file://.aws-athena/002__sales__orders__sample.sql \
    --query-execution-context 'Database=sales,Catalog=AwsDataCatalog' \
    --work-group analytics --region us-east-1 --output json --no-cli-pager
```

Save the successful response and obtain the ID from `.QueryExecutionId`; handle submission errors before trying to parse an ID. With that ID, call `aws athena get-query-execution --query-execution-id "$query_id" --region us-east-1 --output json --no-cli-pager`. Poll at bounded intervals/backoff until a terminal state or a finite deadline. For `SUCCEEDED`, call `aws athena get-query-results --query-execution-id "$query_id" --region us-east-1 --output json --no-cli-pager`. For `FAILED` or `CANCELLED`, retain `Status.StateChangeReason` and do not retrieve results as success. Record the response, statistics and result or error in the common envelope. On CLI errors during polling retain the last known ID and state, record the error, and do not resubmit blindly.

## Complete bounded example

This standalone example uses AWS CLI and Python 3 standard library, without `jq`. It submits only the fixed SELECT shown below. Adapt the verified context and SQL together, then review the entire SQL for read-only behavior and cost; this is not a SQL validator. The sample refuses existing artifacts, captures ordinary CLI errors and timeouts, and does not persist raw stderr. It requires Python 3 and AWS CLI; if Python 3 is unavailable, do not assume an alternative exists: use another available JSON-capable tool or report the limitation. Process termination and disk failures can leave incomplete artifacts and must be reported.

```python
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

os.umask(0o077)
root = Path.cwd() / ".aws-athena"
root.mkdir(exist_ok=True)
stem = "002__sales__orders__sample"
sql_path = root / f"{stem}.sql"
result_path = root / f"{stem}.result.json"
region, database, catalog, workgroup = "us-east-1", "sales", "AwsDataCatalog", "analytics"
sql = """SELECT order_id, customer_id
FROM "sales"."orders"
WHERE order_date = '2025-03-01'
LIMIT 10;
"""

if result_path.exists():
    raise SystemExit("Result already exists; choose a fresh sequence")
try:
    with sql_path.open("x", encoding="utf-8") as output:
        output.write(sql)
except FileExistsError:
    raise SystemExit("SQL artifact already exists; choose a fresh sequence")

envelope = {
    "schema_version": 1, "status": "UNKNOWN", "artifact": sql_path.name,
    "context": {"account_id": None, "region": region, "catalog": catalog,
                "database": database, "workgroup": workgroup},
    "query_execution_id": None, "execution": None, "data": None,
    "pagination": {"complete": False, "next_token": None}, "error": None,
}

class RequestError(Exception):
    def __init__(self, stage, code):
        self.stage, self.code = stage, code


def aws(stage, *args):
    try:
        result = subprocess.run(
            ["aws", *args, "--region", region, "--output", "json", "--no-cli-pager"],
            capture_output=True, text=True, timeout=30, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RequestError(stage, None) from exc
    if result.returncode != 0:
        raise RequestError(stage, result.returncode)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RequestError(stage + "_response", None) from exc


try:
    start = aws("start_query_execution", "athena", "start-query-execution",
                "--query-string", "file://" + str(sql_path),
                "--query-execution-context", f"Database={database},Catalog={catalog}",
                "--work-group", workgroup)
    query_id = start.get("QueryExecutionId")
    if not query_id:
        raise RequestError("start_response", None)
    envelope["query_execution_id"] = query_id
    for attempt in range(12):
        response = aws("get_query_execution", "athena", "get-query-execution",
                       "--query-execution-id", query_id)
        execution = response.get("QueryExecution")
        if not isinstance(execution, dict):
            raise RequestError("poll_response", None)
        envelope["execution"] = execution
        envelope["status"] = execution.get("Status", {}).get("State", "UNKNOWN")
        if envelope["status"] in ("SUCCEEDED", "FAILED", "CANCELLED"):
            break
        if attempt < 11:
            time.sleep(2)
    status = envelope["status"]
    if status == "SUCCEEDED":
        data = aws("get_query_results", "athena", "get-query-results",
                   "--query-execution-id", query_id)
        envelope["data"] = data
        token = data.get("NextToken")
        envelope["pagination"] = {"complete": token is None, "next_token": token}
    elif status in ("FAILED", "CANCELLED"):
        envelope["error"] = {"stage": "athena_execution", "exit_code": None,
                             "message": "See execution status for the reason."}
    else:
        envelope["error"] = {"stage": "poll_timeout", "exit_code": None,
                             "message": "Execution has not reached a terminal state."}
except RequestError as exc:
    if exc.stage == "get_query_results":
        envelope["status"] = "FAILED"  # execution.Status retains Athena's SUCCEEDED
    elif envelope["query_execution_id"] is None:
        envelope["status"] = "UNKNOWN"  # submission may have reached Athena
    envelope["error"] = {"stage": exc.stage, "exit_code": exc.code,
                         "message": "Inspect the CLI error securely."}

# Create a valid result atomically, without overwriting another attempt.
fd, temp_name = tempfile.mkstemp(prefix=".result-", dir=root)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as output:
        json.dump(envelope, output, ensure_ascii=False, indent=2)
        output.write("\n")
    os.link(temp_name, result_path)
finally:
    os.unlink(temp_name)

if envelope["status"] != "SUCCEEDED" or not envelope["pagination"]["complete"]:
    sys.exit(1)
```

AWS CLI auto-paginates in this example: do not add `--no-paginate` or `--max-items` without handling continuation and marking incomplete results. Retain AWS column metadata and header rows as returned. If submission times out or the response is lost, Athena might have accepted it; reconcile using an idempotency token or query history instead of immediately resubmitting. If polling fails or times out, resume with the same ID. Treat a result-retrieval failure separately from query execution failure. A polling timeout is not cancellation or success. For Glue requests, run each saved `.sh` and wrap its parsed JSON or sanitized failure using the same envelope.
