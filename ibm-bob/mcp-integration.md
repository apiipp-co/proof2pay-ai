# IBM Bob <-> MCP <-> Langflow Integration

## Contract

```text
User intent
  -> IBM Bob
  -> MCP tool discovery
  -> selected PROOF2PAY tool + JSON args
  -> Langflow flow
  -> deterministic rule checks for synthetic WO-1028
  -> structured result
  -> MCP
  -> Bob explanation / approval request
```

## Example

User:

> Check whether WO-1028 is ready for billing and explain any blocker.

If connected, Bob should select `validate_completion_evidence`. The flow and direct MCP endpoint have been tested; Bob selection itself has not.

Example result shape:

```json
{
  "job_id": "WO-1028",
  "billing_state": "BLOCKED",
  "blockers": ["REQ-COOLING-TEST", "REQ-CUSTOMER-ACK", "REQ-SERVICE-REPORT"],
  "requirements": [
    {
      "id": "REQ-CUSTOMER-ACK",
      "status": "MISSING",
      "evidence_ids": [],
      "source_ref": "SOW-1028#acceptance",
      "next_action": "Record customer acknowledgement and its source"
    }
  ],
  "synthetic": true
}
```

Bob explanation:

> WO-1028 is blocked. Customer acknowledgement required by SOW-1028#acceptance has no linked evidence. A measured cooling result and final service report are also unresolved. I can outline the needed evidence; this demo does not send a sign-off request.

## Tool-description rule

Tool descriptions should state:
- trigger/when to call;
- required inputs;
- output intent;
- explicit non-goals;
- whether external action is possible and gated.

## Debug checklist

If Langflow works but Bob does not call it:
- verify MCP endpoint reachable;
- verify tool is exposed;
- simplify tool name/description;
- validate JSON schema required fields;
- test with an explicit user request matching the description;
- inspect Bob/MCP logs for discovery/call errors.
