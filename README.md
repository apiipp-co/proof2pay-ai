# PROOF2PAY AI

**Finish the job. Prove the job. Get paid.**

PROOF2PAY helps B2B field-service teams decide whether a completed job has enough evidence to prepare a billing handoff. The demo starts with synthetic AC maintenance work order `WO-1028`: the technician reports completion, but the cooling reading, customer acknowledgement, and service report still need attention. Each decision points to a requirement and its evidence. A person must approve generation of the completion pack.

> **Implementation snapshot · 28 September 2026.** The browser prototype and four deterministic Langflow 1.12 flows run locally on a synthetic AC case and three genuine NYC Parks work-order records. A fifth, native Agent flow is wired to the project tools but awaits a model provider. Thirteen API scenarios and five direct MCP checks passed. IBM Bob recognized the project MCP server as **Connected**, but tool execution inside Bob has **not yet been verified**. Public records do not include billing proof. See [implementation status](IMPLEMENTATION_STATUS.md) for the precise boundary.

## Watch and try

- [104-second local demo video](demo/proof2pay-demo.mp4) (screen recording, no voiceover).
- [Pitch deck](docs/02-pitch-deck.pdf) · [one-page judge brief](docs/09-judge-one-pager.pdf) · [submission answers](SUBMISSION.md).
- [Genuine public work-order snapshot and provenance](data/README.md): IDs `2791739`, `2792582`, and `2792861`.
- Start the browser demo with `python3 -m http.server 8000` from this folder, then open <http://localhost:8000/app/>.
- Run the browser checks with `node --test app/core.test.mjs` (Node 18+).

The browser demo runs without keys and keeps edits in memory. Add a measured cooling reading and customer acknowledgement, enter an approver name, then generate the synthetic pack. It does not send messages, create an invoice, or access customer records.

## What is implemented

| Layer | Evidence | Limit |
|---|---|---|
| Browser MVP | [Interactive local app](app/) and four Node checks | Deterministic simulation; no backend persistence |
| Langflow | [Five real exports](langflow/exports/), [runnable main flow screenshot](langflow/screenshots/04-main-review-flow.png), [13 API test results](langflow/runs/verification-2026-09-28.json) | Four deterministic flows run; the native Agent flow needs a model provider |
| MCP / Bob | [Five direct MCP checks](langflow/runs/mcp-verification-2026-09-28.json), [Bob connected screenshot](ibm-bob/screenshots/01-mcp-connected.jpeg), and [local configuration](.bob/mcp.json) | Four tools exposed through MCP; Bob invocation still needs verification |
| Research | [Secondary sources and limits](research/validation-results.md) | No primary customer interviews yet |

## How the decision works

```text
Technician completion claim
    -> requirement and evidence assessment
    -> missing / ambiguous / conflicting blocker
    -> exact next action with source reference
    -> human approval
    -> synthetic completion pack
```

For `WO-1028`, a note saying “cooling test performed” is a **claim**, not a measured result. The validator initially returns `BLOCKED`. Adding a reading and an acknowledged handover resolves those two gaps; report generation still requires explicit approval. Conflicting evidence returns `HUMAN_REVIEW`. The generated pack is marked `BILLING_READY_DEMO`, never an actual invoice or authorization to bill.

## Langflow and IBM Bob

The four executable Langflow tools are `analyze_job_completion`, `validate_completion_evidence`, `generate_completion_pack`, and `review_job_readiness`. The first three assess individual steps; the main review flow chains a Prompt Template with a deterministic component that returns analysis, validation, and next actions. Use `{"job_id":"2792861"}` to inspect a genuine public HVAC work order: the validator reports its official `Completed` field but returns `INSUFFICIENT_EVIDENCE` for billing. The same applies to `2791739` and `2792582`. A separate native Agent graph connects the three project tools and instructions but cannot run until a model is selected in Langflow. The four runnable flows are exposed through Langflow's project MCP endpoint. The checked-in [.bob/mcp.json](.bob/mcp.json) points Bob to the local endpoint on this Mac; Bob Settings recognized it as connected. Start and verification instructions are in [langflow/README.md](langflow/README.md) and [ibm-bob/setup-guide.md](ibm-bob/setup-guide.md). A Bob tool-call screenshot or log is still required before claiming Bob orchestration.

The intended architecture is:

```text
Operations user -> IBM Bob -> Langflow MCP tools -> evidence rules
                                      -> structured result -> human decision
```

The runnable flows deliberately use deterministic rules. The broader AI design, including grounded interpretation of unstructured evidence, is documented as a roadmap in [PRD.md](PRD.md) and [Architecture.md](Architecture.md), not as a tested model capability. The [native Agent graph](langflow/screenshots/05-agent-toolset-awaiting-model.png) is prepared for that next step; no model credentials were changed.

## Judge navigation

| Question | File |
|---|---|
| Why this problem and who pays? | [Proposal](Proposal.md), [business canvas](docs/01-idea-business-canvas.pdf) |
| How does the MVP behave? | [Demo script](demo/demo-script.md), [rules](Rules.md), [app](app/) |
| What is real today? | [Implementation status](IMPLEMENTATION_STATUS.md), [evaluation](evaluation/README.md) |
| How is it built? | [Architecture](Architecture.md), [Langflow guide](langflow/README.md), [MCP integration](ibm-bob/mcp-integration.md) |
| What are the safety limits? | [Responsible AI](ResponsibleAI.md), [AI usage disclosure](AI_USAGE_DISCLOSURE.md) |
| How do I submit it? | [Submission pack](SUBMISSION.md), [GitHub upload](GITHUB_UPLOAD.md) |

## Responsible claims

No customer results, percentage improvements, primary interviews, Bob calls, live deployment, or model accuracy are claimed without direct evidence. The browser walkthrough is synthetic; the separate NYC Parks records are genuine public data, not a customer pilot. The project does not authenticate signatures, send customer messages, issue invoices, or move money.

License: [MIT](LICENSE).
