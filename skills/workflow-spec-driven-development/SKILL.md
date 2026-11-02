---
name: workflow-spec-driven-development
description: Create, refine, review, or track a specification and its implementation when requirements, acceptance criteria, and traceability need to be explicit; also serve an SDD Builder request queue when explicitly requested.
---

# Specification-driven development

Use a specification to align implementation with observable outcomes. Scale its detail to the task: a short acceptance checklist may suffice for a small change. An explicit request for a spec does not itself authorize implementation.

1. Inspect existing documentation, code and project conventions. Record the objective, intended users, scope and constraints; distinguish confirmed requirements from assumptions and unresolved decisions.
2. Describe behavior at system boundaries: inputs, outputs, failure cases, permissions, compatibility and operational requirements where applicable. Define testable acceptance criteria and relevant non-goals.
3. For broad work, split the specification into independently verifiable capabilities with their dependencies and migration or rollout needs. Avoid inventing technology choices or specifying irrelevant implementation details.
4. Resolve questions that materially affect the solution. When a decision is not blocking, state the assumption and continue the work already authorized. Do not require approval at every phase unless requested or necessary for an external action.
5. Choose the project's existing location and format for a durable spec when one is needed; otherwise present a concise spec in the response. Keep it current when decisions or scope change.

## Working modes

- **Create or refine:** connect the problem and scope to scenarios, observable criteria, a feasible plan and verifiable tasks. Read [specification and traceability](references/specification-and-traceability.md) for a suggested bundle and review checks.
- **Assess readiness or close:** inspect the existing project's policy and validation tools, report their actual results and limitations, and record progress in existing project artifacts when appropriate. For SDD template projects, use [SDD template workflow](references/sdd-template-workflow.md).
- **Serve the SDD Builder queue:** only when asked to serve or listen to that queue, use [SDD Builder queue](references/sdd-builder-queue.md). It has a distinct proposal-only contract.

When a reusable bundle is helpful and the project has no established templates, adapt the [specification](assets/templates/spec.md), [plan](assets/templates/plan.md), [tasks](assets/templates/tasks.md), and [history](assets/templates/history.md) templates. Use only the artifacts appropriate to the work; omit inapplicable fields and never invent approvals, decisions or requirements.

Do not install tooling, create a particular directory structure, impose a formal approval gate, or write project code merely because this skill is active. Respect applicable project gates and the user's scope. An already authorized implementation does not require another approval unless the applicable project workflow or action requires it.

## Acceptance example

Instead of “pagination works”, specify: “Given 55 records and a page size of 20, the first two pages contain 20 records each, the third contains 15, and an invalid cursor returns a documented client error.” Adapt this to the actual API contract.

Before finishing, check that each criterion is observable, edge cases are proportional to risk, open questions are visible and the spec does not imply authorization for deployment, migration or other external changes.
