# Presenter script · 60–90 seconds

1. **Problem (0:00–0:10).** “The technician says the AC job is finished. Finance needs evidence before it can prepare billing.”
2. **Blocked case (0:10–0:25).** Open `WO-1028`. Show the cooling claim with no measurement, missing customer acknowledgement, and missing report. Point to the source reference for each requirement.
3. **Resolve evidence (0:25–0:45).** Add a synthetic measured cooling reading and a synthetic acknowledgement. Revalidate: the report remains a blocker.
4. **Human gate (0:45–1:00).** Enter the approver name and explicitly approve. Generate the demo pack. Open the [sample JSON](approved-completion-pack-WO-1028.json) to point out the source photo IDs, 22 °C reading, customer acknowledgement ID, and claim-only technician note. State that no invoice or external message was sent.
5. **Execution proof (1:00–1:20).** Show `review_job_readiness` and the four MCP tools, then the 13/13 API and 5/5 direct MCP verification reports. Enter `{"job_id":"2792861"}` to show a real public HVAC work order remaining `INSUFFICIENT_EVIDENCE`. If showing the native Agent graph, explain that local Granite runs but its final answer comes from a deterministic output guard.

**Optional Bob scene, only after a real call is captured:** Ask Bob to use `validate_completion_evidence` for `WO-1028`. Show the actual tool call and Bob's explanation. Until then, describe Bob as configured but unverified.

The browser case is fictional. The separate NYC Parks work-order metadata is public and genuine. The screen recording in this folder covers the browser and Langflow UI; it does not include voiceover or Bob.
