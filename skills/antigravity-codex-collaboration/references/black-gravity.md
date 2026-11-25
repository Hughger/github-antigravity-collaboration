# Optional Black Gravity integration

[Black Gravity](https://github.com/Zythenth/black-gravity) inspired this project. This repository does not ship its server or replace its policy checks. Use an existing authorized connection when it fits the user's chosen reading mode.

Inspect the tools and schemas actually exposed by the connected version. Do not assume a fixed tool catalog, modify global models, or create a second server merely because a connection is missing.

## Original workspace versus isolated copy

Keep these modes explicit:

- **Original workspace:** the authorized direct CLI reads current files in place. Paths in a prompt are entry points, not a restricted file bundle. Use a new independent session for the post-execution review.
- **Bridge copy:** confirm which files were copied and which version the reviewer can see. In bridge versions where resuming or handing off preserves the old isolated copy, create a fresh reviewer task from the updated workspace after Codex executes.

Black Gravity 0.9.0 rejected direct source execution with `ISOLATION_REQUIRED` in the observed setup. That observation does not establish what future versions support. If a user requires original-workspace reading and the current bridge cannot provide it, use a separately authorized direct CLI path when available. Authentication or permission failures are not permission to switch transports to evade a denial.

## Preserve real reports

Use planning and review roles for Antigravity; Codex remains the implementer. Do not automatically integrate Antigravity patches under this workflow.

Record actual task IDs, conversation IDs, cursors, full result references, and usage. A completed task or queued message does not prove agreement. Read the complete final report before advancing.

Where the bridge enforces a report schema, place AGREE or review decisions in its supported fields rather than inventing new top-level fields. A blank findings array does not establish PASS.

Consult the [upstream repository](https://github.com/Zythenth/black-gravity) for the current installation and tool documentation. The bilateral responsibilities and closure rules in this repository are an independent collaboration protocol.
