# Evaluation evidence · 28 September 2026

| Surface | Command | Result | Scope |
|---|---|---|---|
| Browser rules | `node --test app/core.test.mjs` | 4/4 passed | Golden case, gate, conflict, traceability |
| Langflow API | `python3 langflow/verify_live.py` | 7/7 passed | Claim versus proof, blockers, revalidation, approval, conflict, pack |
| Direct MCP | `python3 langflow/verify_mcp.py` | 3/3 passed | Named tool discovery, validator call, approval gate |

Machine-readable run reports are in [`../langflow/runs/`](../langflow/runs/). These are synthetic rule checks on one work order. They do not measure AI model accuracy, Bob orchestration, customer usefulness, production reliability, or commercial impact. The case set in [`golden-cases.json`](golden-cases.json) remains a design reference for a larger future evaluation.

The strongest observed safety behaviors are: a technician claim cannot substitute for a measured result; missing critical evidence blocks readiness; a conflict requests human review; and pack generation requires explicit approval and an approver name.
