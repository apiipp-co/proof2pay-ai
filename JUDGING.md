# Judging Evidence Map

This document maps likely judge questions to concrete evidence. The [official program page](https://hacktiv8.com/projects/ibm/hackathon) asks for an MVP/prototype, business model, demo video, and documentation/technical diagram; it does not publish criterion weights. Every claim should point to a file, screenshot, demo step, test, or cited source.

## Rubric map

| Area | What PROOF2PAY can show | Evidence / remaining limit |
|---|---|---|
| Problem and user | A specific gap between field completion and evidence for billing handoff | `Proposal.md`, `research/validation-results.md`, pitch slides 2–4; no direct customer interview yet |
| Solution and business model | Traceable evidence review, blockers, next actions, and a SaaS hypothesis | `CompetitiveAnalysis.md`, `PRD.md`, working golden demo, `Roadmap.md`; pricing remains unvalidated |
| MVP and technical execution | Browser prototype, four deterministic Langflow tools, direct MCP endpoint, and guarded local Granite Agent | `app/`, `langflow/exports/`, `langflow/runs/`; a Bob tool call is still unverified |
| Safety | Critical blockers, conflict review, source links, and explicit human approval | `ResponsibleAI.md`, `HUMAN_REVIEW` demo, approval-gate checks |
| Participation | Course completion and Stage 1 submission | Official form asks for an authentic IBM SkillsBuild University Education course certificate and matching registration details; Hackathon Certificate of Participation follows submission per the organizer's message |

## Judge questions we should be ready for

### “Why does this need AI?”

Field evidence can be unstructured and heterogeneous. The local Granite Agent demonstrates model inference and tool selection, but its free-form draft once misstated evidence status. The final result comes from a deterministic output guard. The current demo does not establish reliable model extraction or matching of field photos and documents; that capability needs separate evaluation.

### “Why not just use a checklist?”

A checklist works when inputs are known and structured. PROOF2PAY's value hypothesis is the layer that reconciles mixed notes/documents/evidence against requirements, preserves traceability, and resolves gaps across an existing stack.

### “Why not ServiceTitan/ServiceM8?”

They validate that job documentation, signatures, closeout, approval, and billing are real workflow categories. PROOF2PAY does not claim they lack those capabilities; it deliberately focuses on a narrower intelligence layer that can complement existing systems and fragmented SME workflows.

### “What is actually working?”

Answer only from [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md). Never turn a concept diagram into an implementation claim.

### “What is your measurable result?”

For the hackathon: report test-set results from [`evaluation/`](evaluation/) and the golden demo. No customer productivity or billing-delay outcome has been measured.

## Final evidence gate

A claim may enter the final pitch only if it has one of these:

- real implementation artifact;
- reproducible test result;
- clearly identified synthetic-demo outcome;
- cited secondary research;
- real primary research collected with consent.

Otherwise label it as a hypothesis or roadmap item.
