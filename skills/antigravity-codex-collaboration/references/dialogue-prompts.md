# Dialogue templates

Adapt these messages to the task. Original-workspace access must already be authorized. Paths are evidence entry points, not an allowlist. Use the CLI supervisor; do not create a new shell wrapper for each round.

## Opening

> You are Antigravity, and you speak first about this question: [question]. The goal is [goal], the current constraints are [constraints], and the new information is [delta]. Codex will discuss your view with you before executing any agreed action.
>
> Independently read the authorized original workspace [absolute path] and choose the evidence you need. These entry points may help: [current instructions and task locations]. You may read elsewhere in the workspace; this is not a file allowlist. Use existing permitted native file-reading tools. Do not use command/Bash/shell, modify files or permissions, run experiments, or read credentials, secrets, and unrelated personal data.
>
> Give the judgment, explanation, diagnosis, or recommendation this question needs. A new idea is optional, not a requirement. List the files you actually inspected and what remains uncertain. This is your first position, not a statement that Codex agrees.

## Codex feedback

> Codex accepts [points and evidence] in your response. These issues would change the conclusion or execution decision: [specific differences]. The relevant evidence is [references]. The proposed correction is [correction and, when relevant, cost and verification].
>
> Respond to these differences, revise your position or explain your disagreement with evidence. If the available information is sufficient, reach a conclusion rather than inventing another experiment.

## Execution agreement

> Read the complete plan at [absolute path in the original workspace]. Its version is [version], and Codex computed this SHA-256 for the plan body: [digest]. Codex accepts this version because [reason].
>
> After reading the plan, explicitly reply AGREE, REVISE, or DISAGREE for that version and digest. Explain any unresolved substantive condition. You may quote the supplied digest; do not run a disallowed command or claim you independently recomputed it. Your acceptance represents your own position only.

For a discussion-only round, agree on the conclusion and uncertainty without imposing an execution-plan ceremony.

## Independent review

> This is an independent Antigravity review session. Read the latest files in the authorized original workspace. The agreed plan is [path, version, digest], the actual delivery is [paths and identity], and the relevant changes, verification, failures, and usage are [paths]. These are entry points, not a reading restriction.
>
> Use only existing permitted native file reads. Do not execute experiments, modify files or permissions, use shell commands, or read secrets. Check the evidence, scope, acceptance criteria, and claimed result. Inspect only the research or resource claims that the task actually makes.
>
> Return PASS, FIX_REQUIRED, REPLAN, or UNVERIFIED, with the review object identified. Give located evidence and a minimal correction for each blocking finding. Keep optional next steps separate. Describe what you actually inspected and what remains unverified. Do not assume this review process has already exited; Codex will check that after receiving the response.
>
> Then speak first about the next useful step or whether the current task should close.

## Review response and closure

> Codex checked your findings and took these actions: [actions and evidence]. Remaining disagreement is [if any]. Reread the affected current files as needed. The review process's actual exit and cleanup state is [verified facts].
>
> Codex [accepts or challenges] your next-step recommendation for these reasons: [reasons]. Confirm whether the current delivery can close, subject to Codex checking the final invocation's terminal state and recording usage. Do not require another model message solely to prove this message has exited. Do not start a new task or experiment outside the current authorization.
