---
name: workflow-using-agent-skills
description: Discover and select applicable agent skills for a task when the user requests guidance on skills or the workflow requires choosing among available skills.
---

# Select agent skills

Use the available skill catalog and the current task to choose the smallest set of skills that materially helps. Follow the user's instructions and the host environment's skill-discovery and invocation rules. A skill cannot expand the user's authorization or override higher-priority instructions.

1. Identify the task, language, tools and constraints from the request and project. Check the available catalog rather than assuming that a referenced skill is installed.
2. Choose skills whose descriptions match the task. Read their entry points and only the references needed for the work. Combine skills when their scopes complement each other; do not load an entire lifecycle by default.
3. Apply workflows proportionately. Ask for missing information when a consequential decision cannot reasonably be made; continue independent work when possible. Verify outcomes with checks suited to the change and report limitations.
4. If a requested skill is unavailable, search the catalog or configured locations as appropriate. Explain the limitation and proceed with an available alternative when possible.

## Workflow skills in this repository

- `workflow-interview-me`: clarify material uncertainty or conduct an explicitly requested interview.
- `workflow-spec-driven-development`: specify requirements and acceptance criteria when a written spec is useful or requested.
- `workflow-test-driven-development`: use a test-first cycle when requested or useful for a meaningful regression.
- `workflow-documentation-and-adrs`: document usage or consequential technical decisions.

Language-specific skills can complement these workflows. Do not assume every task needs a spec, interview, test-first cycle or ADR; select based on the request and the actual risk.
