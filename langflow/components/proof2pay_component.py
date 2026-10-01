"""Self-contained Langflow component source embedded into three exported flows.

The export builder replaces ACTION with analyze, validate, or generate.
The AC walkthrough is synthetic. Three separate public work orders are real
source records; their missing billing evidence is never fabricated.
"""

import json

from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output
from lfx.schema.message import Message


ACTION = "__ACTION__"

# Verbatim selected fields from data/public/nyc-parks-work-orders.json.
# Kept inside the component so each exported Langflow flow works offline.
PUBLIC_RECORDS = {
    "2791739": {"evt_code": "2791739", "evt_desc": "install air conditioners", "evt_type": "JOB", "evt_date": "2026-09-17T00:00:00.000", "evt_completed": "2026-09-21T07:01:00.000", "evt_udfchar13": "Completed", "evt_udfchar06": "CARPENTER"},
    "2792582": {"evt_code": "2792582", "evt_desc": "Inspect in/outdoor fridge  walk-in-boxes,heating,cooling and  complete logs", "evt_type": "JOB", "evt_date": "2026-09-21T00:00:00.000", "evt_completed": "2026-09-21T11:38:00.000", "evt_udfchar13": "Completed", "evt_udfchar06": "STAENG"},
    "2792861": {"evt_code": "2792861", "evt_desc": "work on plant repairs with oiler HVAC units belts and filters", "evt_type": "JOB", "evt_date": "2026-09-22T00:00:00.000", "evt_completed": "2026-09-22T11:18:00.000", "evt_udfchar13": "Completed", "evt_udfchar06": "STAENG"},
}
PUBLIC_DATASET_URL = "https://data.cityofnewyork.us/d/8sdw-8vja"
PUBLIC_SNAPSHOT_SHA256 = "87fb2031a46adaf41ca455e9928d27ccf6826705e7bead5f8c46d061ef685633"

REQUIREMENTS = [
    {"id": "REQ-BEFORE-AFTER", "description": "Before and after service photos", "source_ref": "SOW-1028#evidence", "critical": True},
    {"id": "REQ-COOLING-TEST", "description": "Post-service cooling performance evidence", "source_ref": "SOW-1028#acceptance-test", "critical": True},
    {"id": "REQ-CUSTOMER-ACK", "description": "Customer completion acknowledgement", "source_ref": "SOW-1028#acceptance", "critical": True},
    {"id": "REQ-SERVICE-REPORT", "description": "Final service report", "source_ref": "WO-1028#closeout", "critical": True},
]
BASE_EVIDENCE = [
    {"id": "EV-001", "type": "photo", "label": "before_photo", "synthetic": True},
    {"id": "EV-002", "type": "photo", "label": "after_photo", "synthetic": True},
    {"id": "EV-003", "type": "technician_note", "label": "completion_note", "synthetic": True},
]
DEFAULT_NOTE = "Preventive maintenance completed for AC Unit L2-07. Drain cleaned and filter cleaned. Cooling test performed after service."


def parse_request(raw):
    text = getattr(raw, "text", raw)
    text = str(text or "").strip()
    if "<job_request_json>" in text:
        if "</job_request_json>" not in text:
            raise ValueError("Main flow request marker is incomplete")
        text = text.split("<job_request_json>", 1)[1].split("</job_request_json>", 1)[0].strip()
    if text.startswith("{"):
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("Input must be a JSON object")
    elif "WO-1028" in text.upper():
        payload = {"job_id": "WO-1028"}
    elif text in PUBLIC_RECORDS:
        payload = {"job_id": text}
    else:
        raise ValueError("Provide job_id=WO-1028 or a published NYC Parks ID: " + ", ".join(PUBLIC_RECORDS))
    if str(payload.get("job_id")) not in ("WO-1028", *PUBLIC_RECORDS):
        raise ValueError("Unknown job ID; choose WO-1028 or a published NYC Parks ID")
    payload["job_id"] = str(payload["job_id"])
    return payload


def public_validation(record, common):
    checks = [
        {"id": "PUBLIC-WORK-ORDER", "status": "OBSERVED", "source_field": "evt_code", "detail": "Official record ID is present"},
        {"id": "PUBLIC-DESCRIPTION", "status": "OBSERVED", "source_field": "evt_desc", "detail": "Work order description is present; it is not a completion report"},
        {"id": "PUBLIC-COMPLETION-STATUS", "status": "OBSERVED", "source_field": "evt_udfchar13,evt_completed", "detail": "Published record says Completed and contains a completion timestamp"},
        {"id": "BILLING-TERMS", "status": "NOT_AVAILABLE", "source_field": None, "detail": "No contract or billing terms in this selected public record"},
        {"id": "CUSTOMER-ACCEPTANCE", "status": "NOT_AVAILABLE", "source_field": None, "detail": "No customer acknowledgement in this selected public record"},
        {"id": "COMPLETION-ARTIFACTS", "status": "NOT_AVAILABLE", "source_field": None, "detail": "No inspection log, photos, or signed service report in this selected public record"},
    ]
    return {
        **common,
        "record": record,
        "billing_state": "INSUFFICIENT_EVIDENCE",
        "checks": checks,
        "blockers": [item["id"] for item in checks if item["status"] == "NOT_AVAILABLE"],
        "next_action": "Obtain the actual contract, completion artifacts, and customer acceptance from an authorized owner before making a billing decision.",
        "caution": "These are prototype evidence gaps, not verified contractual requirements for this NYC Parks job.",
    }


def public_result(payload, action):
    """Only report fields actually published; never accept supplied mock artifacts."""
    if any(key in payload for key in ("evidence", "additional_evidence", "technician_note")):
        raise ValueError("Public record mode accepts only the official snapshot; external evidence is not verified in this prototype")
    record = PUBLIC_RECORDS[payload["job_id"]]
    source = "https://data.cityofnewyork.us/resource/8sdw-8vja.json?%24where=evt_code%3D" + record["evt_code"]
    common = {
        "job_id": record["evt_code"],
        "synthetic": False,
        "data_origin": "NYC_PARKS_PUBLIC_WORK_ORDER",
        "source_url": source,
        "source_dataset_url": PUBLIC_DATASET_URL,
        "snapshot_sha256": PUBLIC_SNAPSHOT_SHA256,
    }
    if action == "analyze":
        return {
            **common,
            "record": record,
            "claims": [{"text": record["evt_desc"], "source_field": "evt_desc", "status": "WORK_ORDER_DESCRIPTION_ONLY"}],
            "method": "source_field_extraction",
            "caution": "The published description and Completed status do not prove each task was performed or accepted by a customer.",
        }
    if action == "validate":
        return public_validation(record, common)
    if action == "orchestrate":
        validation = public_validation(record, common)
        return {
            **common,
            "role": "deterministic_review_agent",
            "policy_version": "P2P-MAIN-1",
            "analysis": {"work_order_description": record["evt_desc"], "source_field": "evt_desc", "status": "WORK_ORDER_DESCRIPTION_ONLY"},
            "validation": validation,
            "billing_state": validation["billing_state"],
            "next_action": validation["next_action"],
            "human_approval_required": True,
        }
    if action == "generate":
        return {**common, "billing_state": "INSUFFICIENT_EVIDENCE", "error": "Completion pack refused: public work-order metadata alone cannot verify billing terms or customer acceptance"}
    raise ValueError("Unknown flow action")


def get_evidence(payload):
    evidence = payload.get("evidence", BASE_EVIDENCE)
    extra = payload.get("additional_evidence", [])
    if not isinstance(evidence, list) or not isinstance(extra, list):
        raise ValueError("evidence and additional_evidence must be arrays")
    evidence = evidence + extra
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) or not isinstance(item.get("label"), str) for item in evidence):
        raise ValueError("Each evidence item needs string id and label")
    ids = [item["id"] for item in evidence]
    if len(ids) != len(set(ids)):
        raise ValueError("Evidence IDs must be unique")
    return evidence


def assess(evidence):
    def items(label):
        return [item for item in evidence if item["label"] == label]

    rows = []
    for req in REQUIREMENTS:
        rid = req["id"]
        if rid == "REQ-BEFORE-AFTER":
            matched = items("before_photo") + items("after_photo")
            status = "READY" if items("before_photo") and items("after_photo") else "INCOMPLETE" if matched else "MISSING"
            next_action = "Add before and after photos"
        elif rid == "REQ-COOLING-TEST":
            matched = items("completion_note") + items("cooling_reading")
            readings = items("cooling_reading")
            if any(item.get("conflict") is True for item in readings):
                status = "HUMAN_REVIEW"
            elif any(isinstance(item.get("value"), (int, float)) and not isinstance(item.get("value"), bool) and item.get("unit") for item in readings):
                status = "READY"
            else:
                status = "AMBIGUOUS" if items("completion_note") else "MISSING"
            next_action = "Request a measured post-service reading with unit"
        elif rid == "REQ-CUSTOMER-ACK":
            matched = items("customer_ack")
            status = "READY" if any(item.get("confirmed") is True for item in matched) else "HUMAN_REVIEW" if matched else "MISSING"
            next_action = "Record customer acknowledgement and its source"
        else:
            matched = items("service_report")
            status = "READY" if matched else "MISSING"
            next_action = "Create a final demo report after human approval"
        rows.append({**req, "status": status, "evidence_ids": [item["id"] for item in matched], "next_action": None if status == "READY" else next_action})
    blockers = [row for row in rows if row["critical"] and row["status"] != "READY"]
    state = "HUMAN_REVIEW" if any(row["status"] == "HUMAN_REVIEW" for row in blockers) else "BLOCKED" if blockers else "AWAITING_APPROVAL"
    return {"job_id": "WO-1028", "billing_state": state, "requirements": rows, "blockers": [row["id"] for row in blockers], "synthetic": True}


def run_action(payload, action):
    if payload["job_id"] in PUBLIC_RECORDS:
        return public_result(payload, action)
    evidence = get_evidence(payload)
    if action == "analyze":
        note = str(payload.get("technician_note", DEFAULT_NOTE))
        claims = []
        if "cooling test" in note.lower():
            claims.append({"text": "Cooling test performed", "source_evidence_id": "EV-003", "status": "CLAIM_ONLY"})
        if "filter cleaned" in note.lower():
            claims.append({"text": "Filter cleaned", "source_evidence_id": "EV-003", "status": "CLAIM_ONLY"})
        return {"job_id": "WO-1028", "claims": claims, "evidence_ids": [item["id"] for item in evidence], "synthetic": True, "method": "rule_based_demo"}
    if action == "validate":
        return assess(evidence)
    if action == "orchestrate":
        validation = assess(evidence)
        note = str(payload.get("technician_note", DEFAULT_NOTE))
        claims = []
        for phrase in ("cooling test", "filter cleaned"):
            if phrase in note.lower():
                claims.append({"text": phrase, "source_evidence_id": "EV-003", "status": "CLAIM_ONLY"})
        return {
            "job_id": "WO-1028",
            "synthetic": True,
            "role": "deterministic_review_agent",
            "policy_version": "P2P-MAIN-1",
            "analysis": {"claims": claims, "note_is_proof": False},
            "validation": validation,
            "billing_state": validation["billing_state"],
            "recommended_actions": [row["next_action"] for row in validation["requirements"] if row["next_action"]],
            "human_approval_required": True,
            "next_tool": "generate_completion_pack only after critical evidence is complete and a named person approves",
        }
    if action == "generate":
        approver = payload.get("approved_by")
        if payload.get("approved") is not True or not isinstance(approver, str) or not approver.strip():
            raise ValueError("Explicit approved=true and approved_by are required")
        before = assess(evidence)
        unresolved = [rid for rid in before["blockers"] if rid != "REQ-SERVICE-REPORT"]
        if unresolved:
            raise ValueError("Critical evidence unresolved: " + ", ".join(unresolved))
        if not any(item["label"] == "service_report" for item in evidence):
            reading = next(item for item in evidence if item["label"] == "cooling_reading" and isinstance(item.get("value"), (int, float)) and not isinstance(item.get("value"), bool) and item.get("unit"))
            acknowledgement = next(item for item in evidence if item["label"] == "customer_ack" and item.get("confirmed") is True)
            evidence.append({
                "id": "EV-REPORT-DEMO", "type": "report", "label": "service_report", "synthetic": True,
                "approved_by": approver.strip(),
                "content": {
                    "job_id": "WO-1028", "service_type": "Preventive AC Maintenance",
                    "photo_evidence_ids": [item["id"] for item in evidence if item["label"] in ("before_photo", "after_photo")],
                    "cooling_reading": {"value": reading["value"], "unit": reading["unit"], "source_evidence_id": reading["id"]},
                    "customer_acknowledgement_evidence_id": acknowledgement["id"],
                    "technician_note_status": "CLAIM_ONLY",
                    "source_evidence_ids": [item["id"] for item in evidence],
                },
            })
        after = assess(evidence)
        return {"job_id": "WO-1028", "billing_state": "BILLING_READY_DEMO", "approved_by": approver.strip(), "evidence_ids": [item["id"] for item in evidence], "service_report": next(item for item in evidence if item["label"] == "service_report"), "requirements": after["requirements"], "synthetic": True, "disclaimer": "Demo only; no invoice or external communication"}
    raise ValueError("Unknown flow action")


class Proof2PayComponent(Component):
    display_name = "Proof2Pay Evidence Tool"
    description = "Assess synthetic WO-1028 or source-linked public NYC Parks records without inventing evidence."
    icon = "ShieldCheck"
    name = "Proof2PayComponent"

    inputs = [MessageTextInput(name="input_value", display_name="Job request JSON", info="JSON with job_id. WO-1028 is synthetic; 2791739, 2792582, and 2792861 are public records.", tool_mode=True)]
    outputs = [Output(display_name="Structured result", name="result", method="build_output")]

    def build_output(self) -> Message:
        try:
            payload = parse_request(self.input_value)
            result = run_action(payload, ACTION)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            result = {"error": str(exc), "synthetic": False if "payload" in locals() and payload.get("job_id") in PUBLIC_RECORDS else True, "action": ACTION}
        return Message(text=json.dumps(result, ensure_ascii=False, separators=(",", ":")))
