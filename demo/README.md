# Demo · synthetic WO-1028

[Watch the 76-second Stage 1 video](proof2pay-demo-stage1-final.mp4). It combines a browser interaction recording with current screenshots of the approved synthetic completion pack and the four Langflow MCP tools. The video is silent and does not show a Bob call. The [older raw recording](proof2pay-demo.mp4) is retained for provenance; its ending shows an outdated tool list and should not be submitted. [Inspect the resulting structured demo pack](approved-completion-pack-WO-1028.json): it lists the photo IDs, measured cooling reading, customer acknowledgement, claim-only technician note status, and human approver. The browser and Langflow generators produced matching report content on 2 October 2026.

## Reproduce

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/app/>. The case begins with a technician completion claim, two photos, and three unresolved requirements: a measured cooling reading, customer acknowledgement, and final report. Add the first two pieces of synthetic evidence in the interface. The report is generated only after a named human approves. The UI marks the output as a demo billing-readiness state.

For the separate Langflow runtime, follow [`../langflow/README.md`](../langflow/README.md). The browser UI and Langflow are separate demo surfaces; the browser does not send calls to Langflow.

For a **genuine published work order**, see the [live Langflow validation result for NYC Parks ID 2792861](public-work-order-2792861-result.json) and its [source snapshot](../data/README.md). The official record says `Completed`, while Proof2Pay returns `INSUFFICIENT_EVIDENCE` for billing. The source is public New York City metadata, not an Indonesian customer case.

[`demo-script.md`](demo-script.md) contains a concise presenter narrative and an optional Bob integration scene once genuinely verified.
