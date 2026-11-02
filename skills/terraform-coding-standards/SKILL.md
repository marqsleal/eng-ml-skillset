---
name: terraform-coding-standards
description: Apply Terraform best practices when writing, reviewing, or refactoring infrastructure configuration and modules.
---

# Terraform coding standards

Respect the existing Terraform version, providers, module boundaries, state backend, and naming conventions. Keep infrastructure changes scoped to the request.

- Format changed configuration with `terraform fmt`; validate with `terraform validate` when initialization and dependencies are available. Avoid changing backend configuration merely to run checks.
- Declare compatible Terraform and provider version constraints. Preserve the dependency lock file and review provider changes rather than upgrading implicitly.
- Make inputs explicit with types, useful descriptions, and validation where it prevents invalid configurations. Mark sensitive inputs and outputs as sensitive; this does not remove values from state.
- Keep secrets out of configuration and version control. Assume state and plan files may contain sensitive values, and use the project's approved storage and access controls.
- Use modules for cohesive, reusable infrastructure, not for every resource. Expose inputs and outputs that callers actually need and avoid hard-coded environment-specific values.
- Prefer stable keys for `for_each`; changing keys or resource addresses can replace infrastructure. When refactoring addresses, use appropriate `moved` blocks or a deliberate state migration.
- Review dependencies and lifecycle changes carefully. Avoid broad `depends_on`, `ignore_changes`, or destructive replacement unless justified by the desired behavior.
- When a plan is available, inspect creates, updates, replacements, and deletes against the request. A plan can refresh remote state and contact providers; do not apply changes or perform state migrations without authorization.
