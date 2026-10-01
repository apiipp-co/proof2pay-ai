# Langflow implementation

Six actual Langflow 1.12 exports are in [`exports/`](exports/). Four deterministic flows run locally: `analyze_job_completion`, `validate_completion_evidence`, `generate_completion_pack`, and `review_job_readiness`. The first three use `Chat Input -> Proof2Pay custom component -> Chat Output`. The main review flow uses `Chat Input -> Prompt Template -> Proof2Pay Review Agent (rules) -> Chat Output`. These components apply transparent rules to fictional `WO-1028` data and [three genuine public NYC Parks work-order records](../data/README.md). `agent_orchestration_local_granite` adds a native Agent backed by local IBM Granite 3.3 2B, four project tools, and an output guard. `agent_orchestration_requires_model` remains an unconfigured provider template. No configured flow uses private customer data.

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
python3 langflow/verify_agent.py # five guarded Agent-output checks; needs Ollama
```

To use another Langflow executable, set `LANGFLOW_BIN=/absolute/path/to/langflow`. The script intentionally refuses to start without its local database; it will not silently create an empty instance.

## Recreate elsewhere

Install [Langflow](https://docs.langflow.org/get-started-installation) and import the four deterministic JSON files under `exports/` into a project. To run the local Agent export, install [Ollama](https://ollama.com/download), pull `granite3.3:2b`, start Ollama on `127.0.0.1:11434`, and import `agent_orchestration_local_granite.json`. The Ollama model is stored on the local machine, not in GitHub. Alternatively, `python3 langflow/build_export.py` creates a **new** project and writes the original three flows; then run `python3 langflow/build_main_flow.py` and `python3 langflow/build_agent_flow.py --local-granite` to add newer graphs to that project. The initial builder creates a new project and rewrites export files; do not run it casually against an existing shared instance. Update `.bob/mcp.json` with the newly created project ID and endpoint. Re-run verification scripts with `LANGFLOW_URL` and, if auth is enabled, `LANGFLOW_TOKEN`. Import can assign different flow IDs; update exported flow references before using `verify_live.py`.

## Native Agent setup

On the prepared Mac, open `agent_orchestration_local_granite` and run `{"job_id":"WO-1028"}`. The Agent calls the source-linked `review_job_readiness` tool. A test of the model's free-form summary incorrectly called the existing before/after photos missing; the output guard therefore discards that draft and returns the deterministic review from the original Chat Input. The final result preserves `REQ-BEFORE-AFTER: READY` and the three actual blockers. This is a working Agent tool-call demonstration with an explicit safety boundary, not validated AI evidence interpretation. The Agent flow is kept off the project MCP endpoint while its behavior is evaluated.

The separate `agent_orchestration_requires_model` graph can be used with another provider: select **Setup Provider** on its Agent node and enter any required credential in Langflow's own UI. Do not put secrets into the repository or chat. Its model remains unset.

## Evidence and limits

- [`runs/verification-2026-09-28.json`](runs/verification-2026-09-28.json): 13/13 Langflow API scenarios passed on the prepared local instance.
- [`runs/mcp-verification-2026-09-28.json`](runs/mcp-verification-2026-09-28.json): 5/5 direct MCP checks passed.
- [`runs/verification-2026-10-02.json`](runs/verification-2026-10-02.json): 13/13 API scenarios passed again on 2 October.
- [`runs/mcp-verification-2026-10-02.json`](runs/mcp-verification-2026-10-02.json): 5/5 direct MCP checks passed again on 2 October.
- [`runs/agent-verification-2026-10-02.json`](runs/agent-verification-2026-10-02.json): 5/5 guarded Agent-output checks passed on 2 October.
- [`screenshots/`](screenshots/): genuine local project, graph, and MCP tool list captures.
- The golden case and its `BILLING_READY_DEMO` output are synthetic. Public records are real source metadata; their billing state remains `INSUFFICIENT_EVIDENCE`.
- `proof2pay-main-flow.blueprint.json` is an older architecture sketch. Five files in `exports/` are executable on the prepared Mac; `agent_orchestration_requires_model.json` requires a provider.

MCP endpoint details follow [Langflow's project MCP documentation](https://docs.langflow.org/mcp-server).
