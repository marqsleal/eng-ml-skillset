---
name: workflow-test-driven-development
description: Apply test-driven development when requested or when adding a meaningful regression test before changing behavior would reduce risk.
---

# Test-driven development

Use a short red–green–refactor cycle for behavior that benefits from automated verification. Respect the project's test tools, conventions and supported environments. Do not invent tests for trivial reversible changes or simply mirror implementation details.

1. Identify a behavior and its observable contract. Inspect existing tests and select the smallest useful test level: unit for isolated logic, integration for real component boundaries, end-to-end for a critical user flow.
2. Add a focused test and run it before changing behavior. Confirm that it fails for the expected reason; a compilation error, missing dependency or broken fixture is not evidence of the intended regression.
3. Make the smallest coherent change that satisfies the test. Run it again, then refactor while preserving behavior. Repeat for other meaningful cases, including errors and boundary conditions when relevant.
4. Run the affected suite and project-required checks. Add broader coverage when the change or a failure warrants it. Report commands, results and any checks that could not run.

For a bug, first reproduce the reported failure at a realistic boundary if feasible. When reproduction requires unavailable infrastructure or a risky external action, document the limitation, use the best safe substitute and avoid claiming the bug was reproduced.

Prefer real deterministic collaborators and small fakes; mock external boundaries when necessary. Avoid tests coupled to private calls, timing assumptions or incidental formatting. Use isolation and cleanup for shared state and resources. For concurrency changes, test cancellation and lifecycle behavior and use race detection where available.

If the test cannot be run, explain the limitation rather than claiming a red or green result. Do not introduce a new test framework or require network services solely to follow the cycle.
