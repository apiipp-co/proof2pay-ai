# Demo · synthetic WO-1028

[Watch the 104-second screen recording](proof2pay-demo.mp4). It shows the browser prototype moving from missing evidence to an approved synthetic completion pack, then the local Langflow validation graph and MCP tool list. The recording is silent and does not show a Bob call.

## Reproduce

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/app/>. The case begins with a technician completion claim, two photos, and three unresolved requirements: a measured cooling reading, customer acknowledgement, and final report. Add the first two pieces of synthetic evidence in the interface. The report is generated only after a named human approves. The UI marks the output as a demo billing-readiness state.

For the separate Langflow runtime, follow [`../langflow/README.md`](../langflow/README.md). The browser UI and Langflow are separate demo surfaces; the browser does not send calls to Langflow.

For a **genuine published work order**, see the [live Langflow validation result for NYC Parks ID 2792861](public-work-order-2792861-result.json) and its [source snapshot](../data/README.md). The official record says `Completed`, while Proof2Pay returns `INSUFFICIENT_EVIDENCE` for billing. The source is public New York City metadata, not an Indonesian customer case.

[`demo-script.md`](demo-script.md) contains a concise presenter narrative and an optional Bob integration scene once genuinely verified.
