"""Check the local Granite Agent graph's guarded final result.

Requires the prepared Langflow project and Ollama's granite3.3:2b model.
This checks the graph output, not model accuracy or IBM Bob execution.
"""

import json
from datetime import datetime, timezone

from verify_live import ROOT, TOKEN, api, flow


def main():
    if not TOKEN:
        api("/api/v1/auto_login")
    result = flow("agent_orchestration_local_granite", {"job_id": "WO-1028"})
    requirements = {
        row["id"]: row["status"]
        for row in result.get("validation", {}).get("requirements", [])
    }
    checks = {
        "graph_returns_synthetic_case": result.get("job_id") == "WO-1028" and result.get("synthetic") is True,
        "guard_is_authoritative": result.get("output_policy") == "SOURCE_LINKED_RULES_AUTHORITATIVE" and result.get("model_draft_used") is False,
        "existing_photos_remain_ready": requirements.get("REQ-BEFORE-AFTER") == "READY",
        "critical_blockers_remain": set(result.get("validation", {}).get("blockers", [])) == {
            "REQ-COOLING-TEST", "REQ-CUSTOMER-ACK", "REQ-SERVICE-REPORT"
        },
        "approval_remains_required": result.get("billing_state") == "BLOCKED" and result.get("human_approval_required") is True,
    }
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "flow": "agent_orchestration_local_granite",
        "model": "granite3.3:2b via local Ollama",
        "input": {"job_id": "WO-1028"},
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "limit": "Guarded final-output check only; does not score model interpretation or prove an IBM Bob tool call.",
    }
    target = ROOT / "runs" / f"agent-verification-{datetime.now().astimezone().date().isoformat()}.json"
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
