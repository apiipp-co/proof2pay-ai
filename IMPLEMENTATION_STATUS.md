# Implementation status · 28 September 2026

This is the source of truth for what has actually run. `DONE` means a local artifact and a reproducible check exist; it does not mean production or organizer acceptance.

| Capability | Status | Evidence / limit |
|---|---|---|
| Product, architecture, business, safety, and pitch documentation | DONE | Root Markdown files and `docs/` PDFs/PPTX |
| Synthetic `WO-1028` case | DONE | `demo/golden-case-WO-1028.json`; all case entities are fictional |
| Genuine public work-order snapshot | DONE | Three selected NYC Parks AMPS records with IDs, verbatim selected fields, exact query, and checksum in `data/public/nyc-parks-work-orders.json` |
| Browser prototype | DONE | `app/`, screenshot, and four passing Node tests; in-memory rules only |
| Langflow `analyze_job_completion` | DONE | Real export and live test; labels synthetic note claims as `CLAIM_ONLY` and public descriptions as `WORK_ORDER_DESCRIPTION_ONLY` |
| Langflow `validate_completion_evidence` | DONE | Real export and live tests for synthetic blockers and public-record evidence gaps |
| Langflow `generate_completion_pack` | DONE | Real export and live tests; source-linked synthetic pack requires approval, and public-record generation is refused |
| Direct Langflow MCP endpoint | DONE | Three tools discovered, validation called, approval gate checked in `langflow/runs/mcp-verification-2026-09-28.json` |
| Bob MCP connection | DONE | `.bob/mcp.json` points to `127.0.0.1:7862`; Bob Settings showed `proof2pay-langflow-local` as `Connected` in the workspace; see `ibm-bob/screenshots/01-mcp-connected.jpeg` |
| Bob tool call and explanation | UNVERIFIED | Need genuine Bob call/result screenshot or log |
| AI model inference | NOT IMPLEMENTED | The current Langflow component is deterministic and covers one synthetic job plus three public records |
| Actual customer service evidence or commercial outcome | NOT DONE | No private customer work order, signed acceptance, photos, contract, paid invoice, or pilot outcome was provided |
| Live website / hosted backend | NOT DEPLOYED | Browser app and Langflow run locally only |
| Demo video | DONE | `demo/proof2pay-demo.mp4`; silent screen recording of browser demo and Langflow UI |
| Primary user interviews or measured commercial impact | NOT DONE | Only secondary research; no fabricated users or outcomes |
| Organizer form submission | NOT DONE | Needs participant name, final links, required certificate/eligibility evidence, and human submission |

## Reproduce the checks

```bash
node --test app/core.test.mjs
scripts/start-langflow-local.sh  # second terminal; local Mac setup only
python3 langflow/verify_live.py
python3 langflow/verify_mcp.py
```

The Langflow API check passed 11/11 scenarios (seven synthetic, four public-record safety checks) and the direct MCP check passed 4/4 on 28 September 2026. See `evaluation/README.md` for what those tests do and do not establish. Do not state that Bob executed a tool, that a model interpreted field evidence, or that billing was authorized until independently demonstrated.
