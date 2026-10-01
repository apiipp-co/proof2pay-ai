"""Run synthetic and public-record checks against the exported Langflow flows.

Requires a local Langflow instance with these flow IDs imported. Saves only
sanitized results; no session cookies, tokens, or personal data are written.
"""

import gzip
import http.cookiejar
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = os.environ.get("LANGFLOW_URL", "http://127.0.0.1:7862").rstrip("/")
TOKEN = os.environ.get("LANGFLOW_TOKEN")
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def api(path, payload=None):
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    request = urllib.request.Request(BASE + path, data=json.dumps(payload).encode() if payload is not None else None, headers=headers)
    try:
        with opener.open(request, timeout=120) as response:
            content = response.read()
            return json.loads(gzip.decompress(content) if content[:2] == b"\x1f\x8b" else content)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Langflow {path} returned HTTP {exc.code}: {exc.read()[:300]!r}") from exc


def flow(name, payload):
    identifier = json.loads((ROOT / "exports" / f"{name}.json").read_text())["id"]
    raw = api(f"/api/v1/run/{identifier}", {"input_request": {"input_value": json.dumps(payload), "input_type": "chat", "output_type": "chat"}})
    text = raw["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    return json.loads(text)


def main():
    if not TOKEN:
        api("/api/v1/auto_login")
    reading = {"id": "EV-004", "type": "reading", "label": "cooling_reading", "value": 22, "unit": "°C", "synthetic": True}
    ack = {"id": "EV-005", "type": "acknowledgement", "label": "customer_ack", "confirmed": True, "synthetic": True}
    complete = {"job_id": "WO-1028", "additional_evidence": [reading, ack]}
    cases = [
        ("claim_is_not_proof", "analyze_job_completion", {"job_id": "WO-1028"}, lambda r: any(x["status"] == "CLAIM_ONLY" for x in r["claims"])),
        ("initial_blockers", "validate_completion_evidence", {"job_id": "WO-1028"}, lambda r: r["billing_state"] == "BLOCKED" and set(r["blockers"]) == {"REQ-COOLING-TEST", "REQ-CUSTOMER-ACK", "REQ-SERVICE-REPORT"}),
        ("reading_and_ack_still_need_report", "validate_completion_evidence", complete, lambda r: r["billing_state"] == "BLOCKED" and r["blockers"] == ["REQ-SERVICE-REPORT"]),
        ("explicit_approval_required", "generate_completion_pack", complete, lambda r: "approved=true" in r.get("error", "")),
        ("missing_evidence_cannot_be_approved", "generate_completion_pack", {"job_id": "WO-1028", "approved": True, "approved_by": "Koordinator Demo"}, lambda r: "Critical evidence unresolved" in r.get("error", "")),
        ("conflict_requires_review", "validate_completion_evidence", {"job_id": "WO-1028", "additional_evidence": [{**reading, "conflict": True}, ack]}, lambda r: r["billing_state"] == "HUMAN_REVIEW"),
        ("approved_pack_is_traceable", "generate_completion_pack", {**complete, "approved": True, "approved_by": "Koordinator Demo"}, lambda r: r["billing_state"] == "BILLING_READY_DEMO" and len(r["requirements"]) == 4 and all(x["source_ref"] and x["evidence_ids"] for x in r["requirements"]) and r["service_report"]["content"]["cooling_reading"]["source_evidence_id"] == "EV-004" and r["service_report"]["content"]["customer_acknowledgement_evidence_id"] == "EV-005"),
        ("public_record_is_source_linked", "analyze_job_completion", {"job_id": "2792861"}, lambda r: r["synthetic"] is False and r["record"]["evt_code"] == "2792861" and r["record"]["evt_desc"] == "work on plant repairs with oiler HVAC units belts and filters" and r["claims"][0]["status"] == "WORK_ORDER_DESCRIPTION_ONLY"),
        ("public_completed_not_billing_ready", "validate_completion_evidence", {"job_id": "2791739"}, lambda r: r["billing_state"] == "INSUFFICIENT_EVIDENCE" and r["record"]["evt_udfchar13"] == "Completed" and set(r["blockers"]) == {"BILLING-TERMS", "CUSTOMER-ACCEPTANCE", "COMPLETION-ARTIFACTS"}),
        ("public_pack_refused_even_with_approval", "generate_completion_pack", {"job_id": "2792582", "approved": True, "approved_by": "Demo"}, lambda r: r["synthetic"] is False and r["billing_state"] == "INSUFFICIENT_EVIDENCE" and "refused" in r.get("error", "")),
        ("public_injected_evidence_refused", "validate_completion_evidence", {"job_id": "2792861", "additional_evidence": [{"id": "EV-FAKE", "label": "customer_ack"}]}, lambda r: r["synthetic"] is False and "not verified" in r.get("error", "")),
        ("main_synthetic_review", "review_job_readiness", {"job_id": "WO-1028"}, lambda r: r["billing_state"] == "BLOCKED" and r["role"] == "deterministic_review_agent" and r["human_approval_required"] is True and len(r["validation"]["blockers"]) == 3),
        ("main_public_review", "review_job_readiness", {"job_id": "2792861"}, lambda r: r["billing_state"] == "INSUFFICIENT_EVIDENCE" and r["synthetic"] is False and r["analysis"]["source_field"] == "evt_desc" and r["human_approval_required"] is True),
    ]
    results = []
    for label, name, payload, check in cases:
        output = flow(name, payload)
        passed = bool(check(output))
        results.append({"case": label, "flow": name, "pass": passed, "billing_state": output.get("billing_state"), "error": output.get("error")})
        print(f"{'PASS' if passed else 'FAIL'} {label}")
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "langflow_version": "1.12.0", "server": "isolated local instance", "datasets": ["synthetic WO-1028", "three selected NYC Parks public records"], "passed": sum(row["pass"] for row in results), "total": len(results), "cases": results}
    target = ROOT / "runs" / f"verification-{datetime.now().astimezone().date().isoformat()}.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
