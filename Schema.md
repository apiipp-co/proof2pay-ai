# Data Schema

## Entity overview

```text
Job 1---* Requirement
Job 1---* Evidence
Job 1---* Claim
Requirement 1---* EvidenceMatch *---1 Evidence
Job 1---* ReadinessAssessment
Job 1---* GapAction
Job 1---* Approval
Job 1---0..1 CompletionPack
Job 1---* AuditEvent
```

## Job

| Field | Type | Notes |
|---|---|---|
| `job_id` | string | Immutable business key, e.g. `WO-1028` |
| `customer_ref` | string | Demo-safe reference, not raw PII |
| `service_type` | enum/string | e.g. HVAC preventive maintenance |
| `reported_complete_at` | datetime/null | Field report timestamp |
| `state` | enum | `OPEN`, `REPORTED_COMPLETE`, `BLOCKED`, `REVIEW`, `BILLING_READY` |
| `source_system` | string | manual/demo/FSM connector |

## Requirement

| Field | Type | Notes |
|---|---|---|
| `requirement_id` | string | e.g. `REQ-CUST-SIGNOFF` |
| `job_id` | string | FK |
| `title` | string | Human-readable requirement |
| `critical` | boolean | Blocks final readiness when unresolved |
| `expected_evidence_types` | array | signature/photo/checklist/report/etc. |
| `source_ref` | string | Work order/SOW/policy reference |
| `source_excerpt` | string | Short excerpt/normalized rule |

## Evidence

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | string | Immutable ID |
| `job_id` | string | FK |
| `type` | enum | photo, signature, note, checklist, report, reading, file |
| `uri` | string | Storage reference, not necessarily public URL |
| `captured_at` | datetime/null | Can be unknown |
| `submitted_by_role` | string | technician/customer/admin/system |
| `metadata` | object | filename, mimetype, hash, etc. |

## Claim

Represents a statement extracted from notes/documents, e.g. "cooling test completed". Claims are not automatically facts.

| Field | Type |
|---|---|
| `claim_id` | string |
| `job_id` | string |
| `text` | string |
| `source_evidence_id` | string/null |
| `confidence` | number/null |

## EvidenceMatch

| Field | Type |
|---|---|
| `match_id` | string |
| `requirement_id` | string |
| `evidence_id` | string |
| `status` | enum |
| `reason` | string |
| `confidence` | number/null |
| `review_required` | boolean |

## ReadinessAssessment

Stores a snapshot, not an immutable truth.

| Field | Type |
|---|---|
| `assessment_id` | string |
| `job_id` | string |
| `created_at` | datetime |
| `blocking_requirement_ids` | array |
| `progress_percent` | number/null |
| `final_state` | enum |
| `explanation` | string |
| `human_confirmed` | boolean |

## GapAction

| Field | Type |
|---|---|
| `action_id` | string |
| `job_id` | string |
| `requirement_id` | string |
| `action_type` | enum |
| `owner_role` | enum |
| `draft_payload` | object |
| `requires_approval` | boolean |
| `status` | enum |

## AuditEvent

Every tool call, assessment transition, approval, and generated artifact should produce an audit event with actor, timestamp, input references, output references, and status.
