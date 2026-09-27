# Langflow Flow Specification

## 1. analyze_job_completion

**Purpose:** transform technician/job inputs into normalized claims and evidence candidates.

Inputs:
- `job_id`
- `technician_note`
- `job_metadata`
- `attachment_metadata[]`

Core steps:
1. validate required identifiers;
2. parse unstructured note;
3. extract completion claims;
4. normalize evidence metadata;
5. return structured JSON only.

Output schema: see `contracts/analyze-job-completion.schema.json`.

## 2. retrieve_job_requirements

**Purpose:** retrieve applicable completion requirements from controlled SOW/work-order/policy sources.

Rules:
- include source document ID and source fragment;
- do not invent a requirement when retrieval fails;
- return `HUMAN_REVIEW` when scope applicability is ambiguous.

## 3. validate_completion_evidence

**Purpose:** compare requirements against available evidence.

Core steps:
1. load structured claims/evidence;
2. retrieve requirement set;
3. semantically propose matches;
4. attach rationale + source IDs;
5. pass proposed result to deterministic policy checks;
6. emit `READY`, `MISSING`, `INCOMPLETE`, `AMBIGUOUS`, or `HUMAN_REVIEW` per requirement.

Never turn model confidence alone into a critical `READY` decision.

## 4. calculate_billing_readiness

**Purpose:** aggregate requirement states deterministically.

Example policy:
- any unresolved critical requirement => `BLOCKED`;
- noncritical unresolved requirement => `REVIEW_REQUIRED` or configured state;
- all critical requirements ready + human confirmation => eligible for `BILLING_READY`.

The percentage shown in UI is presentation metadata, not the legal/financial decision itself.

## 5. resolve_missing_evidence

**Purpose:** propose the smallest next action for each blocker.

Examples:
- missing technician photo -> technician follow-up;
- missing customer acknowledgement -> prepare sign-off request;
- ambiguous reading -> request measurable value/photo;
- missing final report -> draft report from verified structured state.

Any external communication remains `approval_required=true`.

## 6. generate_completion_pack

**Purpose:** draft a factual package from verified state after approval.

Must include:
- job summary;
- requirement/evidence matrix;
- unresolved items if any;
- service report draft;
- evidence index;
- handover/BAST draft only when applicable to configured workflow.

Must not issue an invoice or claim legal acceptance.
