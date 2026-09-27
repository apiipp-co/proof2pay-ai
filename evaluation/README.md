# Evaluation evidence · 28 September 2026

| Surface | Command | Result | Scope |
|---|---|---|---|
| Browser rules | `node --test app/core.test.mjs` | 4/4 passed | Golden case, gate, conflict, traceability |
| Langflow API | `python3 langflow/verify_live.py` | 13/13 passed | Eight synthetic scenarios plus five public-record source and safety checks, including the main review flow |
| Direct MCP | `python3 langflow/verify_mcp.py` | 5/5 passed | Four named tools, synthetic gates, genuine public record blocked, main review call |

Machine-readable run reports are in [`../langflow/runs/`](../langflow/runs/). The browser and eight Langflow cases use one synthetic work order. Five Langflow cases and two MCP checks use [genuine public work-order metadata](../data/README.md) to verify provenance and refusal to infer billing readiness. The native Agent flow has not run because no model is selected. These checks do not measure AI model accuracy, Bob orchestration, customer usefulness, production reliability, or commercial impact. The case set in [`golden-cases.json`](golden-cases.json) remains a design reference for a larger future evaluation.

The strongest observed safety behaviors are: a technician claim cannot substitute for a measured result; missing critical evidence blocks readiness; a conflict requests human review; and pack generation requires explicit approval and an approver name.
