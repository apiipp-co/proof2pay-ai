# Langflow / MCP Tool Contracts

Tool names should describe one business action clearly. Bob should not have to guess among vague tools such as `process_data` or `agent_tool`.

| Tool | When Bob should call it | Must not do |
|---|---|---|
| `analyze_job_completion` | user submits a completed-job note/evidence | decide final billing readiness |
| `retrieve_job_requirements` | applicable requirements are needed | invent missing contract terms |
| `validate_completion_evidence` | user asks what is complete/missing/ambiguous | authorize invoice/payment |
| `calculate_billing_readiness` | structured requirement states exist | override unresolved critical blockers |
| `resolve_missing_evidence` | blockers need next steps | send externally without approval |
| `generate_completion_pack` | critical blockers resolved + approval present | fabricate evidence or legal acceptance |

Stable JSON schemas live under `/contracts`.
