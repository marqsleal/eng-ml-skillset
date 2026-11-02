# Architecture decision records

An ADR captures one consequential decision, the context that made it necessary and its trade-offs. Record the reasoning a future maintainer cannot infer from code. Use the project's language, location, template, naming, review and status conventions; inspect the existing decision log before choosing a number or creating a new directory.

## Prepare and draft

1. Identify the decision and affected scope. Consult existing ADRs, specifications, code and user-provided context; link relevant evidence. Ask only for information that materially changes the decision and cannot be inferred. If the decision has not been made, present the options as a proposal rather than selecting one on the team's behalf.
2. Capture the problem, decision drivers and constraints, including relevant technical, business and organizational forces. Separate established facts, assumptions and unresolved questions.
3. State the chosen or proposed direction clearly and explain why it fits the drivers. Record alternatives actually considered, including doing nothing only if it was a real option, and the reasons they were not chosen. If the history is unknown, say so instead of inventing options or rationale.
4. Document positive and negative consequences, risks, affected interfaces or systems, and relevant implementation, migration or operational implications. Include verification measures or signals to revisit the decision where useful; do not invent metrics or force a fixed number of items.
5. Reference related decisions, specs and supporting sources. Identify owner, reviewers or stakeholders where known, without attributing approval to someone who has not provided it.

## Review and lifecycle

Use the project's statuses and review process. In the absence of a convention, a new decision that has not been approved can be marked **Proposed**; **Accepted**, **Rejected**, **Deprecated** and **Superseded** are common later states. Describe a rejection's reason when known. Do not change a status to accepted, imply consensus or invent the date of a past decision without evidence.

An owner can coordinate feedback, track open actions and communicate the outcome. Match the review to the significance of the choice and the project's process; a request to draft an ADR does not authorize soliciting external approvals or publishing it.

Treat accepted or rejected decisions as historical records. For a substantive change, normally propose a new ADR and cross-link the replacement and previous record, updating status when the project's process and actual decision warrant it. Follow local policy for corrections and metadata changes; never erase the prior rationale. During code or design review, identify conflicts with accepted decisions and distinguish a possible exception, remediation or proposed replacement from an already approved change. Existing noncompliant code may need a separately scoped follow-up rather than an unsolicited refactor.

## Adaptable template

When the project has no established template, adapt the [short template](../assets/templates/adr-short.md) for a focused decision or the [detailed template](../assets/templates/adr-detailed.md) when migration, risks or verification need more space. Omit inapplicable fields rather than filling placeholders with guesses; copy the chosen template to the project's decision log and follow its naming conventions.

## Review checklist

Confirm the status matches evidence, the rationale and consequences are concrete, the alternatives are genuine, the affected scope and outstanding questions are clear, and links resolve. Check that any numbering or metadata follows local conventions and that sensitive information is excluded. Report unknowns and validation limitations honestly.
