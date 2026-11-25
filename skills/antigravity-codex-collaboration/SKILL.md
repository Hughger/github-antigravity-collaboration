---
name: antigravity-codex-collaboration
description: Coordinate real Antigravity and Codex sessions. Antigravity speaks first, both agree on direction and any execution plan, Codex implements and verifies, and Antigravity reviews before the next round. Supports authorized original-workspace reads and supervised CLI cleanup. Use when the user requests this collaboration, not for every routine edit.
---

# Antigravity-Codex Collaboration

Antigravity makes the first substantive contribution to each new question. Codex responds critically and constructively. Both agree on the direction; when execution is needed, Codex performs and verifies it. Antigravity reviews the latest deliverable, then speaks first about the next step. Either party can disagree.

Speaking first does not require inventing something. A round may involve classification, explanation, diagnosis, a local fix, a plan, interpretation of results, or closure. Do not manufacture experiments or innovation claims to fill the workflow.

## Restore context and authorization

Read the project's current instructions, active task, and directly relevant evidence. Resume the existing phase and conversation when the user says to continue. Do not reopen settled questions without new evidence.

When the user has authorized original-workspace access, let Antigravity independently read the entire workspace and choose its evidence. Supplied paths are starting points, not an allowlist. Exclude credentials, secrets, and unrelated personal data. Record what was actually inspected; broad access is not proof of exhaustive reading.

Use the existing authenticated provider and model selection. Do not install a bridge, change permissions, switch global models, create additional agents, or spend a new experiment budget merely because this skill is active. Existing authorization persists across turns.

For direct CLI use, read the [CLI reference](references/cli.md) and use [run_agy.py](scripts/run_agy.py). A missing MCP connection does not block an already authorized, working direct CLI. For an existing Black Gravity connection, read the [bridge notes](references/black-gravity.md); respect the user's choice of original workspace versus isolated copies.

Never simulate an Antigravity response. If no real authorized connection is available, preserve the prepared context and report the specific blocker.

## 1. Antigravity speaks first

Give Antigravity the question, current constraints, known factual entry points, and new information. Do not preselect a substantive answer and ask for a rubber stamp. Codex may prepare context and operate the connection before the first response.

Ask Antigravity for the judgment, explanation, diagnosis, or recommendation the question needs, along with evidence and uncertainty. In headless original-workspace mode, request existing permitted native file reads such as `read_file` or `view_file`, not command execution or shell-based directory enumeration. If the required reading is not available, report the limitation without changing permissions.

Only when the task actually calls for a new research mechanism should the first response propose a new mechanism and a discriminating validation. For ordinary questions, a reasoned answer is sufficient.

## 2. Discuss and agree

Codex checks the actual response, tests its reasoning against evidence, and offers specific corrections. Send those differences back and read Antigravity's real reply. Prefer a bounded repair for a local problem; do not turn every imperfection into a direction reset.

A discussion-only round may finish with an agreed conclusion and remaining uncertainty. If a written deliverable is requested, Codex writes it and Antigravity reviews it. Do not add code changes or experiments just to create an execution phase.

For actual execution, record a compact plan in the existing task record:

- Question, evidence, and what has changed.
- Intended decision, implementation scope, and allowed write locations.
- Execution, verification, acceptance, and stopping conditions.
- Required resources and existing authorization.

Assign a version and compute a SHA-256 for the plan body, excluding subsequent approval records. Let Antigravity read the complete plan from the original workspace and identify its agreement by version and digest. It may explicitly quote Codex's digest without claiming to have recomputed it; do not ask it to run an otherwise disallowed hash command.

Proceed only when both parties accept the same plan and substantive blockers are resolved. Antigravity should explicitly return `AGREE`, `REVISE`, or `DISAGREE`. A queued message, task completion flag, empty response, or CLI SUCCESS envelope is not agreement.

Revise the version when scope, mechanism, quality criteria, or budget changes materially. Discuss only the differences. If disagreement cannot be resolved with available evidence, propose a small useful diagnostic within existing authorization, or report the unresolved choice.

## 3. Codex executes and verifies

Codex implements the agreed plan, preserves existing user changes, and performs checks proportional to the change. Keep real commands, exit states, outputs, evidence identities, and deviations in the task record.

Existing authorization covers necessary local repairs within scope. If execution disproves a key premise, pause the affected action and return the new evidence to bilateral discussion. Do not silently keep an old approval while changing the plan.

Prepare the actual change and verification record for review. In a dirty workspace, the entire diff against HEAD is not necessarily the change for this round. Include relevant untracked artifacts and report missing evidence honestly.

## 4. Antigravity reviews current work

Use an independent read-only review session after Codex's execution. In original-workspace mode, request fresh reads of the current files. In an isolated bridge, create a fresh reviewer task from the updated workspace; an old planner copy or handoff may be stale.

Provide the agreed plan identity, actual changes, verification evidence, and deliverable identity. Ask for `PASS`, `FIX_REQUIRED`, `REPLAN`, or `UNVERIFIED`, with the reviewed object stated explicitly. Findings need a location, impact, and practical correction. An empty findings list is not an explicit PASS.

Keep optional future suggestions separate from current blockers. Only review novelty, mechanism claims, or resource benefits when they are relevant to the task. An ordinary explanation or repair can pass without introducing an innovation.

Codex evaluates the feedback instead of applying it mechanically. Fix local issues, verify the affected behavior, and request a focused reread. Return to shared planning only for material changes. A review applies to the version actually read, not later edits.

## 5. Discuss the next step and close

After review, Antigravity first explains the next useful step or why the task can close. Codex discusses its value, cost, and dependencies. The next round may be a repair, explanation, validation, new idea, or closure.

Continue authorized work while the user goal remains unmet. Do not ask for approval at each tool call or create an unbounded series of new experiments. When the goal is met, deliver the result and stop.

Verify content and process closure separately. Retain each full response and reach a terminal host/process state. A useful response followed by automatic cleanup is not a natural exit. An empty SUCCESS with denied actions is a failed turn. Use the supervisor's recorded state and never rerun a completed model turn merely to address a hanging process.

The last message need not trigger an infinite chain of confirmations: both parties may agree to close after Codex verifies that final invocation's terminal state.

## Minimal record

Keep one compact record for the current round: phase, plan version/digest, actual agreement source, conversation or task IDs, delivery and review identities, exit/cleanup state, measured usage, and next dependency. Preserve failures rather than replacing them with a clean narrative.

When the CLI reports cumulative usage for a resumed conversation, use its latest total once; do not sum every cumulative snapshot. Missing usage or model identity remains unknown.

Use the [dialogue templates](references/dialogue-prompts.md) as message content, not a new approval system. Keep raw logs private unless they are deliberately sanitized for publication.
