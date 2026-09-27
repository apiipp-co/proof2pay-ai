# Langflow implementation

Three actual Langflow 1.12 exports are in [`exports/`](exports/): `analyze_job_completion`, `validate_completion_evidence`, and `generate_completion_pack`. Each uses a `Chat Input -> Proof2Pay custom component -> Chat Output` graph. The component applies transparent rules to fictional `WO-1028` data and to [three genuine public NYC Parks work-order records](../data/README.md). It does **not** call a language model or use private customer data.

Use `{"job_id":"WO-1028"}` for the synthetic walkthrough. Use `{"job_id":"2792861"}`, `{"job_id":"2791739"}`, or `{"job_id":"2792582"}` for a public record. In public mode, the tools expose published source fields and return `INSUFFICIENT_EVIDENCE`; `generate_completion_pack` refuses to create a billing pack. These records lack the contract, customer acceptance, and completion artifacts needed for a genuine billing decision. Client-supplied extra evidence is rejected in public mode because this prototype cannot authenticate it.

## Run on the prepared Mac

The local Langflow database is stored outside this public repository at `~/Library/Application Support/Proof2Pay Langflow/database.db`. The project ID in [`../.bob/mcp.json`](../.bob/mcp.json) matches that local database. The launcher binds auto-login to `127.0.0.1` only; never expose it on a network.

```bash
scripts/start-langflow-local.sh
```

Open <http://127.0.0.1:7862> to inspect the three flows. From another terminal:

```bash
python3 langflow/verify_live.py  # 11 API scenarios
python3 langflow/verify_mcp.py   # four direct MCP checks
```

To use another Langflow executable, set `LANGFLOW_BIN=/absolute/path/to/langflow`. The script intentionally refuses to start without its local database; it will not silently create an empty instance.

## Recreate elsewhere

Install [Langflow](https://docs.langflow.org/get-started-installation) and import the three JSON files under `exports/` into a project, or run `python3 langflow/build_export.py` against a local Langflow 1.12 instance you control. The builder creates a **new** project and rewrites export files; do not run it casually against an existing shared instance. Update `.bob/mcp.json` with the newly created project ID and endpoint. Re-run both verification scripts with `LANGFLOW_URL` and, if auth is enabled, `LANGFLOW_TOKEN`. Import can assign different flow IDs; update the exported flow references before using `verify_live.py`.

## Evidence and limits

- [`runs/verification-2026-09-28.json`](runs/verification-2026-09-28.json): 11/11 Langflow API scenarios passed on the prepared local instance.
- [`runs/mcp-verification-2026-09-28.json`](runs/mcp-verification-2026-09-28.json): 4/4 direct MCP checks passed.
- [`screenshots/`](screenshots/): genuine local project, graph, and MCP tool list captures.
- The golden case and its `BILLING_READY_DEMO` output are synthetic. Public records are real source metadata; their billing state remains `INSUFFICIENT_EVIDENCE`.
- `proof2pay-main-flow.blueprint.json` is an older architecture sketch. The files in `exports/` are the executable artifacts.

MCP endpoint details follow [Langflow's project MCP documentation](https://docs.langflow.org/mcp-server).
