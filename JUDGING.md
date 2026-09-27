# Judging Evidence Map

This document maps a **working judging hypothesis** to concrete evidence. The weight percentages below came from team planning materials and were not verified against an official published 2026 rubric. The [official program page](https://hacktiv8.com/projects/ibm/hackathon) confirms the broad deliverables but does not publish these weights. Replace them if organizers provide an official rubric. Every scoring claim should point to a file, screenshot, demo step, test, or cited source.

## Rubric map

| Criterion | Weight | What PROOF2PAY must prove | Evidence before final submission |
|---|---:|---|---|
| Problem Clarity | 20% | A narrow, observable handoff problem with target user and consequence | `Proposal.md`, `research/validation-results.md`, pitch slides 2-4 |
| Innovation, Creativity, Feasibility & Monetization | 30% | Differentiated evidence intelligence, feasible MVP, credible SaaS path | `CompetitiveAnalysis.md`, `PRD.md`, working golden demo, `Roadmap.md` |
| User Impact & Benefits | 20% | Clear operational outcome and measurable pilot metrics | `EVALUATION.md`, demo before/after workflow, impact slide |
| Technical Execution | 10% | Real Bob -> MCP -> Langflow path with structured outputs | four runnable Langflow flows and direct MCP tests exist; native Agent awaits model setup and Bob call screenshot/log is still needed |
| Responsible AI | 15% | Grounding, uncertainty, deterministic blocker rules, approval gates | `ResponsibleAI.md`, demo of `HUMAN_REVIEW`, action gate test |
| Participation | 5% | Meet event/session requirements | event attendance/submission evidence outside repository as required |

## Judge questions we should be ready for

### “Why does this need AI?”

Field evidence can be unstructured and heterogeneous, so a future AI layer could help extract claims and propose evidence matches. **The current demo does not perform model inference.** It tests the traceability and approval workflow with deterministic rules; any AI extension must be evaluated separately.

### “Why not just use a checklist?”

A checklist works when inputs are known and structured. PROOF2PAY's value hypothesis is the layer that reconciles mixed notes/documents/evidence against requirements, preserves traceability, and resolves gaps across an existing stack.

### “Why not ServiceTitan/ServiceM8?”

They validate that job documentation, signatures, closeout, approval, and billing are real workflow categories. PROOF2PAY does not claim they lack those capabilities; it deliberately focuses on a narrower intelligence layer that can complement existing systems and fragmented SME workflows.

### “What is actually working?”

Answer only from [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md). Never turn a concept diagram into an implementation claim.

### “What is your measurable result?”

For the hackathon: report test-set results from [`evaluation/`](evaluation/) and golden-demo timings. Do not fabricate business uplift before a pilot exists.

## Final evidence gate

A claim may enter the final pitch only if it has one of these:

- real implementation artifact;
- reproducible test result;
- clearly identified synthetic-demo outcome;
- cited secondary research;
- real primary research collected with consent.

Otherwise label it as a hypothesis or roadmap item.
