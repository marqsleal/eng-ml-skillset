# Specification and traceability

Use the existing project format. For a substantial change, a spec bundle can separate four concerns without requiring four files:

- **Specification:** user and problem, scope and non-goals, scenarios, requirements, acceptance criteria, constraints and open questions.
- **Plan:** technical approach, affected boundaries, dependencies, rollout and compatibility risks. Trace the approach to the requirements and identify decisions needing resolution.
- **Tasks:** independently verifiable work, dependencies and the checks that demonstrate acceptance. Place regression tests before implementation when test-first work is useful and feasible.
- **History:** meaningful changes in scope, rationale and links to decisions; distinguish confirmed decisions from proposals.

When no project templates exist, adapt the bundled [specification](../assets/templates/spec.md), [plan](../assets/templates/plan.md), [tasks](../assets/templates/tasks.md), and [history](../assets/templates/history.md) templates to the scope and project conventions.

Use Given/When/Then to describe relevant scenarios. EARS-style criteria can make conditions explicit: “WHEN [trigger], THE SYSTEM SHALL [observable behavior].” Include measurable limits where they matter; avoid invented targets. Map each consequential criterion to a test, inspection or other evidence, and record why a criterion cannot be verified if necessary.

When reviewing, identify the affected section, severity, problem and practical consequence. Look for ambiguous terms, missing failure cases, contradictions, criteria without evidence, plans outside scope, and tasks that cannot establish the intended behavior. Clearly distinguish blockers from suggestions. Do not mark a specification approved or a task complete without evidence.

For significant architecture choices, link an existing decision record or use the project's ADR convention. Record alternatives actually considered, trade-offs and any signal that would warrant revisiting the choice; never invent an alternative or rationale.
