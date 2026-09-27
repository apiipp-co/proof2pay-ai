# IBM Bob local MCP setup

The repository includes a real [Bob project MCP configuration](../.bob/mcp.json) pointing to the prepared local Langflow project. The endpoint was tested with a direct MCP client, and Bob Settings displayed the workspace server as **Connected** in [this screenshot](screenshots/01-mcp-connected.jpeg). A Bob tool call has **not** been captured, so Bob orchestration remains unverified.

1. Open this entire `proof2pay-ai` folder as the project in IBM Bob.
2. Start Langflow in a separate terminal with `scripts/start-langflow-local.sh` and leave it running.
3. Run `python3 langflow/verify_mcp.py`; it should print three `PASS` lines.
4. In Bob, inspect the workspace MCP server and confirm `proof2pay-langflow-local` is `Connected`. Langflow directly exposes `analyze_job_completion`, `validate_completion_evidence`, and `generate_completion_pack`. Keep tool approval prompts enabled.
5. Ask: “Use `validate_completion_evidence` for synthetic job WO-1028. Explain each blocker with its requirement source. Do not issue an invoice.”
6. Capture a genuine Bob tool call and resulting explanation before describing the Bob integration as working in a submission.

If Bob cannot connect, verify that port 7862 is running, the project ID in `.bob/mcp.json` matches `langflow/exports/local-project-id.txt`, and no other Langflow instance owns the port. Bob's project MCP format is documented in [IBM Bob MCP documentation](https://bob.ibm.com/docs/ide/configuration/mcp/mcp-in-bob).

The local server uses auto-login bound to `127.0.0.1`. Do not expose this configuration outside the laptop or reuse it for production. The repo contains no API key.
