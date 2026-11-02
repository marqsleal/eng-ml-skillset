---
name: sql-athena-exploration
description: Explore Amazon Athena datasets and Glue catalog metadata safely, with bounded sampling and persisted query artifacts.
---

# Athena exploration

Start with known context and metadata, then explore only what the task needs. Read [discovery and guardrails](rules/discovery/guide.md) before testing or exploring. Use AWS CLI as described in [tooling](../sql-athena-tooling/SKILL.md); persist each agent-issued query and its JSON result under `.aws-athena/` in the working directory.

**Hard rule:** during tests and explorations, never execute through AWS CLI any operation that creates, changes, or deletes tables or data. This includes SQL submitted to Athena, files, scripts and indirect execution. You may inspect source data and write DDL/DML files for review, but never execute them in these workflows. Athena's normal query-result output is separate from modifying source tables or data.
