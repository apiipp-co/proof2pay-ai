# Judge Q&A Prep

## Why does this problem matter?

Because a completed field job can still require reconciliation of proof before finance can proceed. The product targets the operational handoff, not generic invoicing.

## What makes it innovative?

The innovation is not “AI + invoice”. It is a traceable evidence-intelligence workflow: mixed evidence -> requirement matching -> blocker explanation -> smallest next action -> human-governed completion pack.

## Why AI?

Field evidence can eventually include free-text notes, documents, and photos with inconsistent terminology. In the current MVP, a local IBM Granite Agent calls the structured review tool, but a deterministic output guard supplies the final decision because the model's free-form draft once misstated evidence status. Extraction and semantic matching from real photos/documents are planned capabilities that still require separate testing.

## What if the AI is wrong?

Critical conclusions require source/evidence traceability. Ambiguity becomes `HUMAN_REVIEW`; the model cannot invent evidence or bypass critical blockers.

## Does the IBM Bob integration already work end to end?

Not yet. Bob Settings showed the local Langflow MCP server as `Connected`, and a separate direct MCP client exercised the four tools. A tool call from a Bob chat has not been captured. The organizer permits Stage 1 submission at this maturity level; Bob chat invocation is the next integration check.

## Is the generated report real customer evidence?

No. `WO-1028` and every photo ID, reading, acknowledgement, and approver in the demo are synthetic. The generated JSON report now records the supporting IDs and measured value rather than merely adding a report marker. It cannot be used as a real customer acceptance or invoice authorization.

## Why does the MCP screenshot say `Auth: None (public)`?

The demo server listens only on `127.0.0.1` on the prepared Mac. It is not a hosted public API. Authentication, user roles, and audit retention are required before any real customer deployment.

## Why not replace existing FSM/accounting software?

Replacement creates adoption friction and broadens scope. PROOF2PAY is designed as an intelligence layer that can sit between field evidence and existing operational/billing systems.

## What is still unvalidated?

Frequency, delay magnitude, willingness-to-pay, and best first vertical in Indonesian SMEs. These are explicitly labelled hypotheses.
