# SDD Builder request queue

Use only when explicitly asked to serve or listen to the SDD Builder queue and the queue tools are available. The builder's acceptance action applies a proposal; serving is proposal-only and does not authorize writing spec files.

1. Call `sdd_next_request` with the current project root and an appropriate agent identifier. Read the entire request, including target, current text, instruction and any read-only context. Read relevant workspace material if needed to avoid contradicting the existing spec.
2. For a drafting request, return only the proposed text for the target field, matching its language and format. Preserve EARS criteria where used. For `structure-idea`, return the exact JSON required by the request, without Markdown fences.
3. For `review-spec`, return findings rather than a rewritten spec. Use the requested JSON shape: `summary` and `findings`, each finding containing `section`, `severity` and `finding` plus `why`. Use the section and severity values required by the request.
4. Submit using `sdd_respond_request` with the request ID and proposal, then process the next request. Never edit spec files or call spec-writing tools while serving; the user applies proposals in the builder.
5. If the queue is empty, report it and stop unless continuous listening was explicitly requested and supported. If the tools are missing, explain the integration is unavailable; do not invent results or install software automatically.

Do not invent missing context. If uncertainty prevents a reliable proposal, follow the request's output contract and communicate the uncertainty without corrupting required JSON.
