# System Architecture

## Architecture goals

1. Keep IBM Bob as the user-facing orchestration layer.
2. Expose Langflow flows as narrow, well-described tools through MCP.
3. Separate generative reasoning from deterministic readiness rules.
4. Preserve traceability from requirement to evidence to decision.
5. Require human approval for consequential actions.

## Logical architecture

```text
User / Ops / Finance
        |
        v
+-----------------------+
| IBM Bob               |
| Intent + Conversation |
| Tool Discovery/Call   |
+-----------+-----------+
            |
            | MCP
            v
+-----------------------------+
| Langflow Tool Layer         |
|-----------------------------|
| analyze_completion          |
| retrieve_requirements       |
| validate_evidence           |
| assess_billing_readiness    |
| propose_gap_actions         |
| build_completion_pack       |
+---+---------------+---------+
    |               |
    v               v
AI/RAG Layer       Rule Engine
    |               |
    +-------+-------+
            |
            v
     Structured State
      /     |      \\
     v      v       v
Evidence  Knowledge  Audit
Store     Store      Log
            |
            v
       Human Approval
            |
            v
     Completion Package
```

## Recommended flow boundaries

### `analyze_completion`
Purpose: normalize unstructured completion input.  
Returns: extracted job facts, claims, evidence metadata, missing required inputs.

### `retrieve_requirements`
Purpose: return applicable requirements with source references.  
Returns: controlled structured requirement list.

### `validate_evidence`
Purpose: map evidence to requirements and identify uncertainty.  
Returns: evidence matches with reasons, not final financial authorization.

### `assess_billing_readiness`
Purpose: deterministic aggregation of requirement states.  
Returns: final state + blockers + progress indicator.

### `propose_gap_actions`
Purpose: choose the smallest next action for each blocker.  
Returns: action drafts and approval requirements.

### `build_completion_pack`
Purpose: generate a draft evidence summary/service report after approval gates.  
Returns: artifact metadata and links.

## Storage recommendation

For hackathon:
- structured state: lightweight Postgres/Supabase or JSON fixture;
- document/evidence files: object storage/local fixture;
- retrieval knowledge: vector store or retriever supported by the hackathon environment;
- audit: append-only table/log.

## Security boundaries

- No service role secrets in frontend code.
- Secrets only from environment variables.
- Evidence access should be scoped by job/role.
- Do not send sensitive/raw customer identifiers to models when unnecessary.
- Log tool invocation metadata, not raw secrets.

## Failure modes

| Failure | Expected behavior |
|---|---|
| Requirement source unavailable | Return `HUMAN_REVIEW`, do not infer policy. |
| Image/document unreadable | Mark evidence unreadable and request replacement. |
| Conflicting evidence | Return `AMBIGUOUS`, show both sources. |
| LLM timeout | Preserve current state; no destructive transition. |
| External tool unavailable | Prepare action draft and allow manual fallback. |
| User asks to invoice automatically | Explain MVP boundary and require human/downstream system. |
