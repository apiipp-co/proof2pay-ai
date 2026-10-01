# Executive Proposal - PROOF2PAY AI

## Executive summary

PROOF2PAY AI addresses a narrow but commercially meaningful handoff in field-service operations: **work can be operationally complete before it is financially ready to bill**. Field evidence may arrive as technician notes, photos, checklists, PDFs, customer signatures, and job records. Operations and finance must determine whether the evidence actually satisfies the job's completion requirements before billing can proceed.

PROOF2PAY is designed as an **Evidence-to-Billing Intelligence Layer** that maps requirements to field evidence, identifies unsupported or ambiguous completion claims, proposes follow-up actions, and produces a human-approved completion package. The current MVP demonstrates this with structured synthetic evidence and selected public work-order metadata. Automated interpretation of real photos and documents remains planned work.

## Why now

Existing FSM products demonstrate demand for job forms, photos, signatures, approval, and invoicing workflows. The opportunity for PROOF2PAY is not to duplicate those systems, but to create a focused intelligence layer for teams whose completion evidence is fragmented across tools or whose current system captures data without reasoning about whether the evidence actually supports the billing handoff.

## Initial customer

**Primary persona:** Operations/admin coordinator at a B2B HVAC maintenance SME.  
**Secondary personas:** Field technician, finance/admin billing staff, operations manager, customer approver.

## Job to be done

> When a field job is reported complete, help me prove that every contractual/operational completion requirement has sufficient evidence so I can resolve gaps and hand a verified package to billing without repeatedly chasing technicians and customers.

## Product promise

**Finished -> Proven -> Billing Ready**

PROOF2PAY should answer three questions:

1. **What was required?**
2. **What evidence actually exists?**
3. **What must happen next before this job can be treated as billing-ready?**

## Product wedge

Start with one high-frequency workflow: **preventive HVAC maintenance**. A typical synthetic completion package can include the work order, scope/checklist, before/after photos, readings/tests, material usage, technician notes, customer acknowledgement, and service report.

The MVP does not attempt scheduling, dispatching, payroll, inventory planning, accounting ledgers, or payment processing.

## Differentiation

### 1. Requirement-to-Evidence Graph
Instead of simply checking whether a file exists, PROOF2PAY maintains traceability from each requirement to the evidence that supports it.

### 2. Explainable Billing Readiness
Every blocker has a reason, source, expected evidence type, status, and owner. The system never treats a percentage score as sufficient if a critical blocker remains.

### 3. Gap-to-Action Agent
The current demo proposes a specific next action and re-validates after synthetic evidence is added. Preparing a real request or task and following up through external systems are future steps that would require user approval.

### 4. Integration-first positioning
PROOF2PAY is designed to sit between existing channels/storage/FSM and downstream billing rather than force an SME to replace its entire operational stack.

## Business model hypothesis

B2B SaaS priced by active field team / monthly completed jobs, with potential tiers:

- **Starter** - completion intake, readiness, evidence pack.
- **Pro** - integrations, custom requirement templates, analytics, agentic follow-ups.
- **Multi-branch** - policy governance, role controls, audit exports.
- **Enterprise/API** - private deployment/integration, advanced compliance, SLAs.

Pricing and willingness-to-pay are **not yet validated**.

## Success metrics for the hackathon

Use prototype measurements, not invented market claims:

- time to identify missing evidence;
- number of critical gaps detected before billing;
- completion-pack preparation time;
- number of manual handoff steps in the golden demo;
- groundedness: percentage of readiness conclusions linked to a requirement/evidence source;
- task success rate for the demo scenario.

## Risks

- Evidence can be ambiguous or manipulated.
- Contract/SOW interpretation can be wrong.
- Different customers have different acceptance requirements.
- "Ready" must not become a legally binding or accounting authorization.
- Integrations may be unavailable during the hackathon.

## Mitigation

- deterministic rule gates for critical requirements;
- explicit `AMBIGUOUS` / `HUMAN_REVIEW` states;
- source links and confidence/limitations;
- synthetic demo data;
- human approval before external actions and final readiness confirmation;
- clear out-of-scope boundaries.
