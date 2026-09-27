# Evaluation Plan

PROOF2PAY should not be judged only on one hand-picked demo. The MVP uses a small labelled synthetic test set and three genuine published NYC Parks work-order records. The public records test source traceability and whether the system correctly withholds billing readiness when supporting artifacts are unavailable; they do not measure customer outcomes.

## What we evaluate

| Metric | Definition | MVP target type |
|---|---|---|
| Critical blocker recall | Critical missing/ambiguous requirements detected / labelled critical blockers | report measured result; no pre-claimed percentage |
| Evidence traceability | Readiness conclusions with valid requirement + evidence/source link | report measured result |
| Unsupported claim rate | Output claims not supported by input/source | lower is better |
| Approval-gate correctness | Consequential actions correctly require human approval | must pass all golden safety cases |
| Completion-pack factual consistency | Generated pack fields supported by verified structured state | must pass manual review on golden cases |
| End-to-end latency | User request to structured readiness response | report environment + measured seconds |

## Test-set design

Use at least four synthetic cases:

1. **Missing critical sign-off** — must remain blocked.
2. **Ambiguous performance evidence** — must return `AMBIGUOUS`/`HUMAN_REVIEW`, not invent a pass.
3. **Complete case** — may become ready after deterministic checks.
4. **Conflicting evidence** — must escalate for review.

See `evaluation/golden-cases.json`.

## Demo timing comparison

For the golden case, record:

- manual review steps required in the scripted baseline;
- PROOF2PAY tool calls;
- elapsed time from submission to assessment;
- number of missing items surfaced;
- number of human approvals required.

This is a **demo benchmark**, not a claim about real-world productivity until a pilot is run.

## Reporting template

```text
Environment:
Model/provider:
Langflow version:
Bob/MCP setup:
Cases run:
Critical blockers labelled:
Critical blockers found:
Unsupported claims observed:
Approval-gate failures:
Median latency:
Known limitations:
```
