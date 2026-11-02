---
name: workflow-documentation-and-adrs
description: Write or update technical documentation and architecture decision records when recording usage, a consequential decision, or its trade-offs is useful.
---

# Documentation and architecture decisions

Document the information a reader needs to use, operate or change the system. Follow the repository's existing locations, templates, language and review conventions; avoid creating documents for decisions that do not need a lasting record.

## Choose the artifact

- Update a README or user guide for setup, commands, configuration and observable behavior. Verify commands against the repository and label environment-specific prerequisites.
- Update API documentation for changed inputs, outputs, authentication, errors and compatibility guarantees. Keep examples and generated specifications consistent with the implementation.
- Use comments for non-obvious constraints or intent that the code alone cannot explain; remove stale comments when behavior changes.
- Write an ADR for a consequential architectural decision with meaningful alternatives or long-lived trade-offs. This can include structure, quality attributes, interfaces, dependencies or development processes. Prefer an existing ADR convention and numbering scheme.

## ADR contents

Record the title, date and status; context and constraints; the decision and its rationale; alternatives actually considered and why they were rejected; and consequences, including benefits, risks and follow-up. Identify the owner and affected stakeholders when known. Distinguish a proposed decision from an accepted one; never invent approval, rationale, dates or alternatives.

For example, a choice of database should state workload and operational constraints, the selection criteria and costs, not merely assert that one database is best.

For the decision workflow, lifecycle and review, read [ADR guidance](references/adr-guidance.md). When the project has no existing template, adapt the [short ADR template](assets/templates/adr-short.md) or the [detailed ADR template](assets/templates/adr-detailed.md). Preserve accepted decisions and link replacements according to project conventions. Use an accepted ADR during relevant design or code review; if a change conflicts with it, report the conflict and possible next steps rather than silently changing the decision.

## Verify

Check links, paths, commands and examples that can be checked locally. Do not present untested examples or proposed behavior as verified facts. Avoid secrets, private data and unnecessary implementation history. Report any important parts that could not be verified.
