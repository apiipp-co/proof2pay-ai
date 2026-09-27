# IBM Bob Tool Catalog

| Tool | Description for discovery | Approval |
|---|---|---|
| `analyze_job_completion` | Label note claims for synthetic WO-1028; do not treat claims as proof. | Exposed; no external action |
| `validate_completion_evidence` | Compare four synthetic requirements with evidence, source refs, and blockers. | Exposed; no external action |
| `generate_completion_pack` | Build a synthetic pack only when critical evidence is complete and `approved=true` plus `approved_by` are supplied. | Exposed; approval required |
| `review_job_readiness` | Return a combined analysis, validation, blockers, and next actions for a synthetic or public work order. | Exposed; human approval remains required for any demo pack |

`resolve_missing_evidence`, retrieval, and billing calculations remain design concepts in this version. Direct MCP calls to the four exposed tools are verified; IBM Bob calls are not yet verified. The separate native Agent flow is not exposed as an MCP tool while its model remains unconfigured.
