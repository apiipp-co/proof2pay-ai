# Evaluation evidence · 2 October 2026

| Surface | Command | Result | Scope |
|---|---|---|---|
| Browser rules | `node --test app/core.test.mjs` | 4/4 passed | Golden case, gate, conflict, traceability |
| Langflow API | `python3 langflow/verify_live.py` | [13/13 passed](../langflow/runs/verification-2026-10-02.json) | Eight synthetic scenarios plus five public-record source and safety checks, including the main review flow |
| Direct MCP | `python3 langflow/verify_mcp.py` | [5/5 passed](../langflow/runs/mcp-verification-2026-10-02.json) | Four named tools, synthetic gates, genuine public record blocked, main review call |
| Local Granite Agent output | `python3 langflow/verify_agent.py` | [5/5 passed](../langflow/runs/agent-verification-2026-10-02.json) | Guarded final answer preserves photo evidence, blockers, and approval requirement |

Machine-readable run reports are in [`../langflow/runs/`](../langflow/runs/). The browser and eight Langflow cases use one synthetic work order. Five Langflow cases and two MCP checks use [genuine public work-order metadata](../data/README.md) to verify provenance and refusal to infer billing readiness. The local Granite Agent ran, but its free-form answer is discarded by an output guard; the Agent check tests the final guarded output only. These checks do not measure AI interpretation accuracy, Bob orchestration, customer usefulness, production reliability, or commercial impact. The case set in [`golden-cases.json`](golden-cases.json) remains a design reference for a larger future evaluation.

The strongest observed safety behaviors are: a technician claim cannot substitute for a measured result; missing critical evidence blocks readiness; a conflict requests human review; and pack generation requires explicit approval and an approver name.
