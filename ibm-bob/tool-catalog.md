# IBM Bob Tool Catalog

| Tool | Description for discovery | Approval |
|---|---|---|
| `analyze_job_completion` | Label note claims for synthetic WO-1028; do not treat claims as proof. | Exposed; no external action |
| `validate_completion_evidence` | Compare four synthetic requirements with evidence, source refs, and blockers. | Exposed; no external action |
| `generate_completion_pack` | Build a synthetic pack only when critical evidence is complete and `approved=true` plus `approved_by` are supplied. | Exposed; approval required |

`resolve_missing_evidence`, retrieval, and billing calculations remain design concepts in this version. Direct MCP calls to the three exposed tools are verified; IBM Bob calls are not yet verified.
