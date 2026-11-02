---
name: pyspark-tooling
description: Configure PySpark development and validation using Python environment dependencies and tools already adopted by the skillset.
---

# PySpark tooling

Prefer the project's existing Python environment and the skillset's Python tooling: Ruff, pytest, mypy, pyscn and uv when already used or appropriate. Add dependencies only when necessary; do not introduce a separate external tool or require a global installation. PySpark and its built-in testing utilities are available from the Python package; check version compatibility and reuse any runtime already supplied by the project.

Read [tooling](rules/tooling.md) for practical checks, validation and runtime limitations. Do not recommend or start local Spark execution or assume that an external Spark service is available. Use an existing authorized test environment only when execution is requested. If execution is unavailable, perform the applicable static checks and report the limitation.

Inspect code and configuration before execution. Never submit remote jobs or change production data or configuration merely to validate code. Do not require `jq`, AWS CLI or additional monitoring services.
