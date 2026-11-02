# SDD template workflow

Use this reference only when the project actually uses the SDD template or its sidecar. First inspect the repository instructions, policy, scripts and active spec; determine whether artifacts are in the root or under `spec/`. Do not assume scripts or the template are installed, and do not run setup commands automatically.

- **Orient:** inspect existing `idea/IDEA_GENERAL.md`, `specs/INDEX.md`, `STATUS.md` and relevant handoffs where present. Identify the active specification and any inconsistency between its spec, plan and tasks.
- **Develop the bundle:** follow the project's existing `spec.md`, `plan.md`, `tasks.md` and `history.md` conventions. Keep criteria testable and maintain traceability between requirements, work and evidence.
- **Check readiness:** when applicable run the project's `check-sdd-policy.sh` and `check-sdd-gate.sh` with the correct root and documented arguments. Report the actual verdict, warnings, errors and stated limitations. In this template a closed gate can be a normal state and a successful process exit does not necessarily mean implementation is authorized. Do not claim the gate checked code if it did not.
- **Consent:** obey a project rule requiring a specific approval or recorded consent; never infer or fabricate it. Check existing approval evidence and prior user authorization before asking again. Record consent only when supported by actual authorization and the project's method; do not use consent to conceal other validation failures.
- **Close:** when requested or appropriate, run available applicable validation scripts, report their actual results, and update relevant history, index or handoff artifacts according to the project's conventions and authorized scope. Summarize objective, active spec, changes, validation, risks, decisions and next step. Do not report a clean result after a failed or unavailable check.

Template commands may prescribe a narrower scope, such as drafting without implementation. Follow that scope when the user invokes that command; do not transfer its restrictions to unrelated projects.
