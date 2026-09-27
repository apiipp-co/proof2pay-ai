# Langflow implementation

Five actual Langflow 1.12 exports are in [`exports/`](exports/). Four run locally: `analyze_job_completion`, `validate_completion_evidence`, `generate_completion_pack`, and `review_job_readiness`. The first three use `Chat Input -> Proof2Pay custom component -> Chat Output`. The main review flow uses `Chat Input -> Prompt Template -> Proof2Pay Review Agent (rules) -> Chat Output`. These components apply transparent rules to fictional `WO-1028` data and [three genuine public NYC Parks work-order records](../data/README.md). The fifth flow, `agent_orchestration_requires_model`, connects a native Langflow Agent to the three Proof2Pay tools and a policy prompt; it needs a model provider before it can run. No configured flow uses private customer data.

Use `{"job_id":"WO-1028"}` for the synthetic walkthrough. Use `{"job_id":"2792861"}`, `{"job_id":"2791739"}`, or `{"job_id":"2792582"}` for a public record. In public mode, the tools expose published source fields and return `INSUFFICIENT_EVIDENCE`; `generate_completion_pack` refuses to create a billing pack. These records lack the contract, customer acceptance, and completion artifacts needed for a genuine billing decision. Client-supplied extra evidence is rejected in public mode because this prototype cannot authenticate it.

## Run on the prepared Mac

The local Langflow database is stored outside this public repository at `~/Library/Application Support/Proof2Pay Langflow/database.db`. The project ID in [`../.bob/mcp.json`](../.bob/mcp.json) matches that local database. The launcher binds auto-login to `127.0.0.1` only; never expose it on a network.

```bash
scripts/start-langflow-local.sh
```

Open <http://127.0.0.1:7862> and enter the `PROOF2PAY AI - verified local demo` project to inspect the flows. Run `review_job_readiness` with `{"job_id":"WO-1028"}` or `{"job_id":"2792861"}`. From another terminal:

```bash
python3 langflow/verify_live.py  # 13 API scenarios
python3 langflow/verify_mcp.py   # five direct MCP checks
```

To use another Langflow executable, set `LANGFLOW_BIN=/absolute/path/to/langflow`. The script intentionally refuses to start without its local database; it will not silently create an empty instance.

## Recreate elsewhere

Install [Langflow](https://docs.langflow.org/get-started-installation) and import the four runnable JSON files under `exports/` into a project. The native Agent export is optional until you have a supported model provider. Alternatively, `python3 langflow/build_export.py` creates a **new** project and writes the original three flows; then run `python3 langflow/build_main_flow.py` and `python3 langflow/build_agent_flow.py` to add the newer graphs to that project. The builder creates a new project and rewrites export files; do not run it casually against an existing shared instance. Update `.bob/mcp.json` with the newly created project ID and endpoint. Re-run both verification scripts with `LANGFLOW_URL` and, if auth is enabled, `LANGFLOW_TOKEN`. Import can assign different flow IDs; update the exported flow references before using `verify_live.py`.

## Native Agent setup

The Agent graph and its three tool connections are prepared. To activate it, open `agent_orchestration_requires_model` in Langflow, select **Setup Provider** on the Agent node, choose a supported model, and enter any required credential in Langflow's own UI. Do not put secrets into the repository or chat. Then run the flow in Playground with `{"job_id":"WO-1028"}` and inspect whether it called the expected tool and preserved the approval boundary. Until that test succeeds, use the deterministic `review_job_readiness` flow for the working demonstration. The native Agent flow is deliberately not MCP exposed while unconfigured.

## Evidence and limits

- [`runs/verification-2026-09-28.json`](runs/verification-2026-09-28.json): 13/13 Langflow API scenarios passed on the prepared local instance.
- [`runs/mcp-verification-2026-09-28.json`](runs/mcp-verification-2026-09-28.json): 5/5 direct MCP checks passed.
- [`screenshots/`](screenshots/): genuine local project, graph, and MCP tool list captures.
- The golden case and its `BILLING_READY_DEMO` output are synthetic. Public records are real source metadata; their billing state remains `INSUFFICIENT_EVIDENCE`.
- `proof2pay-main-flow.blueprint.json` is an older architecture sketch. Four files in `exports/` are executable now; `agent_orchestration_requires_model.json` requires a model.

MCP endpoint details follow [Langflow's project MCP documentation](https://docs.langflow.org/mcp-server).
