# Direct CLI reference

Use the user's installed and authenticated `agy` executable. Check its local help when the CLI version changes. The integration has been exercised with Antigravity CLI 1.5.16; other versions may change flags or response shape.

The supervisor always invokes the CLI with `--mode plan --sandbox --output-format json --print-timeout <deadline>` and the prompt supplied through UTF-8 standard input to the supervisor. It passes arguments directly, without a shell, and does not change the user's model selection.

## Arguments

| Argument | Meaning |
|---|---|
| `--agy` | Path to the installed executable. |
| `--workspace` | Existing original workspace directory. |
| `--output-dir` | A new directory inside the workspace; existing directories are rejected to protect evidence. |
| `--conversation` | Exact conversation ID for a resumed discussion. Omit for a new or independent review session. |
| `--timeout-seconds` | Overall process deadline, default 600. |
| `--exit-grace-seconds` | Time allowed for exit after a complete, identity-matched JSON envelope, default 5. |

Use a fresh output directory for every invocation. Keep the same host session handle while a call is running. Waiting does not authorize a duplicate model call. In a PowerShell script used as a host command, end with `exit $LASTEXITCODE` when the host must preserve the supervisor's exact exit code; otherwise PowerShell may report a generic nonzero status.

## Output and identity

- `stdout.json` preserves raw CLI output, including partial or failed output.
- `stderr.log` preserves diagnostics.
- `process.json` records the PID, conversation identity, output digest, child exit code, supervisor exit code, validity, and cleanup reason. A RUNNING snapshot is replaced with the terminal record.

A usable response must contain a conversation UUID and a nonempty string response, and must not report denied actions. On resume, the conversation must match the requested ID. Complete terminal JSON can still be an empty or denied response; it triggers bounded process cleanup but is not accepted as useful content.

Only the actual model response can establish plan agreement or review acceptance. The supervisor does not interpret AGREE or PASS and is not an autonomous workflow engine.

## Known lifecycle behavior

The CLI may return final JSON without exiting. After the exit grace, the supervisor terminates only its owned child process and waits for it. The raw response is retained, while `RESULT_RECEIVED_PROCESS_TERMINATED` and exit code 2 disclose that cleanup was required. Never relabel this as a natural exit.

An overall timeout terminates the owned child and preserves available output without automatically retrying. If cleanup fails, the record explicitly marks the process as still active. Investigate that exact process identity; do not kill all processes with the same executable name.

This ownership protection does not cover arbitrary descendant trees or a supervisor that is forcibly killed before its cleanup handler runs. The helper does not patch the provider CLI's internal lifecycle.

## Headless permission denials

A command tool may require approval that headless mode cannot request. In one observed failure shape, the CLI returned SUCCESS with an empty response and a nonempty `denied_actions` array. The supervisor reports PERMISSION_DENIED instead of treating this as a completed discussion.

Do not add permission allow-rules, enable a skip-permissions flag, or use another execution route to bypass a denial. When the authorized task can be completed with already permitted native file-reading tools, use those tools for the subsequent turn instead of retrying the denied command. Ask for the specific missing authorization only if the task actually requires it.

The supervisor requests plan mode and the CLI sandbox, but it does not create an independent filesystem sandbox or enforce a secret-exclusion policy. The host and CLI enforce their actual controls; prompts and project instructions state the authorized reading and writing boundaries.

## Retention and usage

Raw responses may contain project content, local paths, or sensitive context. Keep the output directory private and ignored by version control. No raw provider logs or credentials are distributed with this project.

For resumed conversations, usage may be cumulative. Keep the latest reported total per conversation once, distinguish separate sessions, and leave unknown billing amounts or model IDs unknown.
