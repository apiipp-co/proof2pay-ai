# Implementation status · 2 October 2026

This is the source of truth for what has actually run. `DONE` means a local artifact and a reproducible check exist; it does not mean production or organizer acceptance.

| Capability | Status | Evidence / limit |
|---|---|---|
| Product, architecture, business, safety, and pitch documentation | DONE | Root Markdown files and `docs/` PDFs/PPTX |
| Synthetic `WO-1028` case | DONE | `demo/golden-case-WO-1028.json`; all case entities are fictional |
| Genuine public work-order snapshot | DONE | Three selected NYC Parks AMPS records with IDs, verbatim selected fields, exact query, and checksum in `data/public/nyc-parks-work-orders.json` |
| Published Indonesian service-business evidence | DONE | Three source-linked AC-service case studies in `research/indonesia-field-studies.md`; secondary research by others, not our own interviews |
| Browser prototype | DONE | `app/`, screenshot, and four Node tests passed on 2 October; in-memory rules only |
| Langflow `analyze_job_completion` | DONE | Real export and live test; labels synthetic note claims as `CLAIM_ONLY` and public descriptions as `WORK_ORDER_DESCRIPTION_ONLY` |
| Langflow `validate_completion_evidence` | DONE | Real export and live tests for synthetic blockers and public-record evidence gaps |
| Langflow `generate_completion_pack` | DONE | Real export and live tests; source-linked synthetic pack requires approval, and public-record generation is refused |
| Langflow `review_job_readiness` | DONE | Runnable Prompt Template and deterministic review component; synthetic and public-record outputs passed API and MCP checks |
| Native Langflow Agent graph | DONE LOCALLY | `agent_orchestration_local_granite` runs IBM Granite 3.3 2B via Ollama; five guarded final-output checks passed on 2 October in `langflow/runs/agent-verification-2026-10-02.json`. The output guard discards unsupported model prose and publishes a deterministic source-linked review. The separate `agent_orchestration_requires_model` remains unconfigured. |
| Direct Langflow MCP endpoint | DONE | Four tools discovered, validation called, approval gate and main review checked in `langflow/runs/mcp-verification-2026-10-02.json` |
| Bob MCP connection | DONE | `.bob/mcp.json` points to `127.0.0.1:7862`; Bob Settings showed `proof2pay-langflow-local` as `Connected` in the workspace; see `ibm-bob/screenshots/01-mcp-connected.jpeg` |
| Bob tool call and explanation | UNVERIFIED | Need genuine Bob call/result screenshot or log |
| AI model inference | VERIFIED WITH LIMITS | Local Granite made a genuine Langflow tool call. Its free-form summary misstated photo status, so the final output is guarded by deterministic validation. This does not establish reliable model interpretation of unstructured evidence. |
| Actual customer service evidence or commercial outcome | NOT DONE | No private customer work order, signed acceptance, photos, contract, paid invoice, or pilot outcome was provided |
| Public static browser demo | DONE | GitHub Pages serves `app/` at `https://apiipp-co.github.io/proof2pay-ai/app/`; it uses in-browser state and synthetic data |
| Hosted Langflow backend | NOT DEPLOYED | Langflow and Ollama run only on the prepared local Mac |
| Demo video | DONE | `demo/proof2pay-demo.mp4`; silent screen recording of browser demo and Langflow UI |
| Primary user interviews or measured commercial impact | NOT DONE | Published local cases strengthen secondary evidence, but PROOF2PAY has no consented interviews, pilot, or measured business result |
| Organizer form submission | NOT DONE | Final links and field-by-field answers are prepared in `FORM_JAWABAN.md`; participant must enter correct identity, upload their authentic IBM SkillsBuild University Education course certificate, deck and screenshots, then submit personally. Hackathon Certificate of Participation follows submission per organizer message. |

## Reproduce the checks

```bash
node --test app/core.test.mjs
scripts/start-langflow-local.sh  # second terminal; local Mac setup only
python3 langflow/verify_live.py
python3 langflow/verify_mcp.py
python3 langflow/verify_agent.py  # needs Ollama granite3.3:2b
```

On 2 October 2026, the Langflow API check passed 13/13 scenarios (eight synthetic, five public-record safety checks), direct MCP passed 5/5, and the guarded Agent-output check passed 5/5. See `evaluation/README.md` for what those tests do and do not establish. Do not state that Bob executed a tool, that a model reliably interpreted field evidence, or that billing was authorized until independently demonstrated.
