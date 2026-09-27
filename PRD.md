# Product Requirements Document (PRD)

**Product:** PROOF2PAY AI  
**Version:** Hackathon MVP v0.1  
**Theme:** Productivity & Smart Business  
**Tagline:** Finish the job. Prove the job. Get paid.

## 1. Product objective

Enable a B2B field-service team to transform a reported-complete job into an **explainable, evidence-backed, human-approved billing-ready package**.

## 2. Problem statement

Field jobs can be completed on-site while supporting proof remains incomplete or fragmented. Operations/finance may need to reconcile requirements against technician notes, photos, checklists, readings, materials, customer acknowledgement, and reports before billing. Manual reconciliation creates rework and makes it difficult to know what is truly blocking the handoff.

## 3. Personas

### Field technician
- Wants to finish documentation quickly.
- Usually communicates in short, unstructured notes.
- Needs precise requests when something is missing.

### Operations/admin coordinator - primary MVP user
- Needs one view of requirement, evidence, blocker, owner, and next action.
- Wants to avoid repeated manual chasing.

### Finance/admin billing
- Needs a trusted, reviewable completion packet before invoicing.
- Does not want an AI to authorize financial action autonomously.

### Customer approver
- May need to confirm work completion or provide sign-off.

## 4. MVP user stories

1. As an operations coordinator, I can submit a work order, notes, and evidence so the system can build a structured completion case.
2. I can see each requirement and the evidence mapped to it.
3. I can see blockers explained with source, expected proof, status, and next action.
4. I can ask Bob "Why is this not billing-ready?" and receive a grounded answer.
5. I can approve a prepared follow-up action for a missing item.
6. When new evidence arrives, I can re-run validation.
7. I can approve generation of a completion package after critical blockers are resolved.

## 5. Functional requirements

### FR-01 Completion intake
Input: job metadata, free-text technician note, work order/SOW, checklist, photos/document metadata.  
Output: normalized job + extracted completion claims + linked evidence candidates.

### FR-02 Requirement retrieval
The system retrieves applicable completion requirements from a controlled knowledge source and records the source reference.

### FR-03 Evidence matching
For each requirement, the system proposes evidence matches and classifies status as:

- `READY`
- `MISSING`
- `INCOMPLETE`
- `AMBIGUOUS`
- `HUMAN_REVIEW`

### FR-04 Critical blocker policy
A job cannot reach final `BILLING_READY` while any `critical=true` requirement has unresolved status.

### FR-05 Readiness explanation
The system explains why the job is blocked without claiming certainty that is not supported by evidence.

### FR-06 Gap resolution
For each blocker, the system creates a recommended next action with owner and rationale. External communication requires approval.

### FR-07 Re-validation
New evidence triggers re-evaluation of affected requirements.

### FR-08 Completion pack
After human confirmation, the system can generate a draft service report/evidence summary/handover pack. It does not issue an invoice or move money.

## 6. Non-functional requirements

- Traceability: every readiness conclusion links to requirement and evidence IDs.
- Explainability: no opaque "AI says ready" result.
- Safety: consequential actions require human approval.
- Privacy: minimize PII and redact/mask in demo data.
- Reliability: invalid/missing input produces an actionable error, not a hallucinated value.
- Auditability: tool calls and state changes are logged.
- Performance target for demo: typical validation response under 10 seconds on the hackathon environment, subject to model/API latency.

## 7. AI responsibilities

AI is appropriate for:
- interpreting unstructured technician notes;
- extracting completion claims;
- retrieving relevant requirement text;
- proposing evidence matches;
- explaining ambiguity;
- planning a next action;
- drafting a completion report.

AI is **not** the sole authority for:
- legal acceptance;
- customer signature authenticity;
- invoice authorization;
- payment;
- final financial/accounting posting;
- irreversible external actions.

## 8. Business-rule responsibilities

Deterministic logic handles:
- required/optional flags;
- critical blockers;
- valid state transitions;
- required approval gates;
- document presence;
- rule-based date/amount checks when enabled.

## 9. MVP data model

Core entities: `Job`, `Requirement`, `Evidence`, `Claim`, `EvidenceMatch`, `ReadinessAssessment`, `GapAction`, `Approval`, `CompletionPack`, `AuditEvent`.

See [`Schema.md`](Schema.md).

## 10. Golden acceptance test

Given synthetic job `WO-1028` where:
- work is reported complete;
- before/after photos exist;
- customer sign-off is missing;
- cooling-performance proof is ambiguous;
- final report is missing;

Then PROOF2PAY must:
1. mark the job `BLOCKED` / not billing-ready;
2. identify the three gaps;
3. explain each gap with requirement/evidence linkage;
4. prepare follow-up actions;
5. require approval for external action;
6. re-check after evidence update;
7. generate a draft completion pack only after critical blockers are resolved and a human confirms.

## 11. Out of scope

- technician dispatch optimization;
- inventory procurement;
- full CRM/FSM replacement;
- accounting ledger;
- autonomous invoicing/payment;
- legal advice or definitive contract interpretation;
- biometric/signature authentication;
- production-grade computer vision fraud detection.
