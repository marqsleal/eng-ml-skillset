# Athena exploration

Explore Amazon Athena datasets and Glue catalog metadata safely, with bounded sampling and persisted query artifacts.

## Usage

Read [SKILL.md](SKILL.md) for the workflow and its constraints.

Persist exploration artifacts in `.aws-athena/` and never execute table or data mutations through AWS CLI during tests or exploration.

## Supporting guidance

- [discovery and guardrails](rules/discovery/guide.md)
