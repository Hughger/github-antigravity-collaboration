# Contributing

Keep the collaboration protocol independent of any particular research project, machine, or provider account. Use English for documentation, examples, and user-visible messages.

Run the standard-library regression suite before submitting a change:

```sh
python -m unittest discover -s skills/antigravity-codex-collaboration/scripts -p "test_*.py" -v
```

For process handling changes, add a focused test of the affected failure boundary. Preserve raw output, truthful exit states, conversation identity checks, and cleanup limited to the owned child. Never treat a permission denial or an empty response as a successful review.

Do not commit provider credentials, real workspace prompts, conversation logs, personal paths, or private project artifacts. Use synthetic fixtures for tests. A live model test is optional and must be explicitly authorized; CI never runs one.

The skill should guide actual dialogue, not require an innovative idea or a new experiment on every round. Preserve existing project instructions and the user's current authorization.
