# Python-first tooling and execution

Reuse the project's Python environment, dependency declarations and existing `python-tooling` skill. Keep the dependency set small: do not add a tool just because it is listed here. Do not install packages implicitly or change runtime versions without understanding compatibility.

| Need | Preferred tool | Boundary |
| --- | --- | --- |
| Python lint and formatting | Ruff | Static analysis only; no Spark execution |
| Tests | pytest and Python standard library | pytest runs tests; real Spark tests also need a compatible runtime |
| DataFrame and schema assertions | `pyspark.testing`, when available in the project's PySpark version | Check assertion defaults and version-specific options |
| Types and project analysis | mypy or pyscn if already adopted and useful | Do not require them for every task |
| Python packages | Existing project manager; uv when already adopted | Pin compatible versions using the project's conventions |
| Spark SQL and DataFrame plans | Installed PySpark APIs, including `spark.sql(...)` and `DataFrame.explain()` | Requires a usable Spark session; does not establish result correctness |

For SQL-only workflows, keep SQL independent of Python. Reviewed Spark SQL can be tested with synthetic fixtures in an existing authorized test environment when execution is requested; do not add an SQL linter or another external service by default. The SQL skill can still review SQL statically when no Spark runtime is available.

Do not recommend or start local Spark execution. An installed Python package does not guarantee a usable Spark runtime. Check compatibility with the existing authorized execution environment; do not install system packages, start services or replace a managed runtime. Report unavailable prerequisites and which checks remain unexecuted.

Examples of checks when the tools are already present and the project uses them:

```bash
ruff check .
ruff format --check .
```

Before running tests, inspect fixtures and configuration: tests and Spark sessions may access networks, read live data or write files. Use isolated synthetic fixtures and dedicated test paths in the authorized environment. Select commands appropriate to the project rather than treating every check as mandatory. Do not submit remote jobs merely to validate a change; execute tests only when requested in an existing authorized test environment, without mutating production resources.

Use `df.explain("formatted")` on a reviewed DataFrame in an authorized, compatible session. Plans can access catalog metadata and do not prove actual cost or output. If runtime metrics or existing logs are already accessible, use them as evidence without requiring the installation of monitoring infrastructure. Record version, relevant nonsecret configuration, input scale and observed metrics; never invent measurements. Do not require `jq`.
