# Exported Langflow flows

These are genuine JSON exports downloaded from the local Langflow 1.12 project on 28 September 2026. They are not hand-written flow diagrams.

| File | Purpose |
|---|---|
| `analyze_job_completion.json` | Labels technician note statements as claims, never verified proof |
| `validate_completion_evidence.json` | Returns requirement status, source references, blockers, and next actions |
| `generate_completion_pack.json` | Requires complete critical evidence and explicit approver identity |

`local-project-id.txt` identifies the prepared Mac's project. On another Langflow installation, importing may assign a new project ID. Update `.bob/mcp.json` accordingly. Each export embeds the component code and a fixed [three-record public snapshot](../../data/README.md), alongside the separate synthetic `WO-1028` case. The published source fields are genuine; no customer acceptance or billing proof is supplied.
