# Athena and Glue tooling

Use AWS CLI to inspect Glue catalog metadata and run or diagnose Amazon Athena queries with persisted artifacts.

## Usage

Read [SKILL.md](SKILL.md) for the workflow and its constraints.

Use AWS CLI and persisted artifacts without depending on `jq`; never execute table or data mutations through AWS CLI during tests or exploration.

## Supporting guidance

- [CLI workflow and artifacts](rules/cli/guide.md)
- [examples](rules/examples/guide.md)
- [operations and diagnosis](rules/operations/guide.md)
- [validation scenarios](rules/examples/validation.md)
