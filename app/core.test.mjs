import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { assess, finalize } from "./core.mjs";

const fixture = JSON.parse(readFileSync(new URL("../demo/golden-case-WO-1028.json", import.meta.url)));
const base = fixture.evidence;
const reading = { id: "EV-004", label: "cooling_reading", type: "reading", value: 22, unit: "°C", synthetic: true };
const ack = { id: "EV-005", label: "customer_ack", type: "acknowledgement", confirmed: true, synthetic: true };

test("golden case remains blocked with traceable gaps", () => {
  const result = assess(fixture, base);
  assert.equal(result.state, "BLOCKED");
  assert.deepEqual(result.blockers, fixture.expected_initial_state.expected_blockers);
  assert.equal(result.rows.find((row) => row.id === "REQ-COOLING-TEST").status, "AMBIGUOUS");
});

test("critical evidence cannot be bypassed by approval", () => {
  assert.equal(assess(fixture, base, true).state, "BLOCKED");
  assert.throws(() => finalize(fixture, base, "Koordinator"), /belum lengkap/);
});

test("conflicting reading requires review", () => {
  assert.equal(assess(fixture, [...base, { ...reading, conflict: true }, ack]).state, "HUMAN_REVIEW");
});

test("complete evidence plus explicit approval produces a sourced pack", () => {
  const evidence = [...base, reading, ack];
  assert.equal(assess(fixture, evidence).state, "BLOCKED"); // final report still missing
  const { result, pack } = finalize(fixture, evidence, "Koordinator Demo");
  assert.equal(result.state, "BILLING_READY");
  assert.equal(pack.requirement_results.length, fixture.requirements.length);
  assert.equal(pack.approved_by, "Koordinator Demo");
  assert.ok(pack.requirement_results.every((row) => row.source_ref && row.evidence_ids.length));
  assert.deepEqual(pack.service_report.content.photo_evidence_ids, ["EV-001", "EV-002"]);
  assert.deepEqual(pack.service_report.content.cooling_reading, { value: 22, unit: "°C", source_evidence_id: "EV-004" });
  assert.equal(pack.service_report.content.customer_acknowledgement_evidence_id, "EV-005");
  assert.equal(pack.service_report.content.technician_note_status, "CLAIM_ONLY");
});
