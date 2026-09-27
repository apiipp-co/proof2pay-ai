# Product & Decision Rules

## Core principle

**No proof -> no final billing-ready status for critical requirements.**

## Readiness states

| State | Meaning |
|---|---|
| `READY` | Required evidence exists and passes configured checks. |
| `MISSING` | Expected evidence is absent. |
| `INCOMPLETE` | Evidence exists but required fields/details are missing. |
| `AMBIGUOUS` | Evidence can support multiple interpretations or is insufficiently clear. |
| `HUMAN_REVIEW` | Automated assessment must not decide this requirement. |

## Critical blocker rule

`BILLING_READY = true` only when:

1. all critical requirements are `READY`, **and**
2. required human approvals are recorded, **and**
3. no unresolved safety/compliance flag exists.

A numeric readiness percentage is visual progress only and **cannot override blockers**.

## AI rules

- Never invent evidence, timestamps, measurements, signatures, or job events.
- Never treat absence of evidence as evidence of completion.
- Cite/source the requirement used for each conclusion.
- Distinguish facts, inference, and recommendation.
- Use `AMBIGUOUS` when a source cannot support a confident match.
- Ask for clarification rather than hallucinate missing fields.

## Human approval rules

Human approval is mandatory before:

- sending a customer-facing request;
- asserting final billing-ready status in the MVP;
- generating/signing a formal handover document intended for external use;
- sending anything to accounting/billing;
- any action that could trigger an invoice, payment, legal acceptance, or irreversible downstream workflow.

## Demo integrity rules

- Demo data is synthetic and labeled as such.
- Concept mockups are not submitted as implementation screenshots.
- Readiness percentages used in the demo are illustrative outputs of the synthetic ruleset, not empirical market metrics.
- Secondary research is never described as a user interview.
