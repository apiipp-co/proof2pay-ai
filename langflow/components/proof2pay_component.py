"""Self-contained Langflow component source embedded into three exported flows.

The export builder replaces ACTION with analyze, validate, or generate.
Data and rules are deliberately synthetic and local; no invoice is issued.
"""

import json

from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output
from lfx.schema.message import Message


ACTION = "__ACTION__"

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
    if text.startswith("{"):
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise ValueError("Input must be a JSON object")
    elif "WO-1028" in text.upper():
        payload = {"job_id": "WO-1028"}
    else:
        raise ValueError("Provide a JSON object with job_id=WO-1028 or mention WO-1028")
    if payload.get("job_id") != "WO-1028":
        raise ValueError("This demo supports only synthetic job WO-1028")
    return payload


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


class Proof2PayComponent(Component):
    display_name = "Proof2Pay Evidence Tool"
    description = "Assess synthetic WO-1028 evidence with source-linked, deterministic rules."
    icon = "ShieldCheck"
    name = "Proof2PayComponent"

    inputs = [MessageTextInput(name="input_value", display_name="Job request JSON", info="JSON with job_id, optional evidence, approval; no live customer data", tool_mode=True)]
    outputs = [Output(display_name="Structured result", name="result", method="build_output")]

    def build_output(self) -> Message:
        try:
            payload = parse_request(self.input_value)
            evidence = get_evidence(payload)
            if ACTION == "analyze":
                note = str(payload.get("technician_note", DEFAULT_NOTE))
                claims = []
                if "cooling test" in note.lower():
                    claims.append({"text": "Cooling test performed", "source_evidence_id": "EV-003", "status": "CLAIM_ONLY"})
                if "filter cleaned" in note.lower():
                    claims.append({"text": "Filter cleaned", "source_evidence_id": "EV-003", "status": "CLAIM_ONLY"})
                result = {"job_id": "WO-1028", "claims": claims, "evidence_ids": [item["id"] for item in evidence], "synthetic": True, "method": "rule_based_demo"}
            elif ACTION == "validate":
                result = assess(evidence)
            elif ACTION == "generate":
                approver = payload.get("approved_by")
                if payload.get("approved") is not True or not isinstance(approver, str) or not approver.strip():
                    raise ValueError("Explicit approved=true and approved_by are required")
                before = assess(evidence)
                unresolved = [rid for rid in before["blockers"] if rid != "REQ-SERVICE-REPORT"]
                if unresolved:
                    raise ValueError("Critical evidence unresolved: " + ", ".join(unresolved))
                if not any(item["label"] == "service_report" for item in evidence):
                    evidence.append({"id": "EV-REPORT-DEMO", "type": "report", "label": "service_report", "synthetic": True})
                after = assess(evidence)
                result = {"job_id": "WO-1028", "billing_state": "BILLING_READY_DEMO", "approved_by": approver.strip(), "evidence_ids": [item["id"] for item in evidence], "requirements": after["requirements"], "synthetic": True, "disclaimer": "Demo only; no invoice or external communication"}
            else:
                raise ValueError("Unknown flow action")
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            result = {"error": str(exc), "synthetic": True, "action": ACTION}
        return Message(text=json.dumps(result, ensure_ascii=False, separators=(",", ":")))
