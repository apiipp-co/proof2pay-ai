"""Verify Langflow's real project MCP endpoint and save a sanitized report."""

import http.cookiejar
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = os.environ.get("LANGFLOW_URL", "http://127.0.0.1:7862").rstrip("/")
TOKEN = os.environ.get("LANGFLOW_TOKEN")
PROJECT_ID = (ROOT / "exports/local-project-id.txt").read_text().strip()
ENDPOINT = f"{BASE}/api/v1/mcp/project/{PROJECT_ID}/streamable"
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def call(method, params, request_id):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params}
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), headers=headers, method="POST")
    with opener.open(request, timeout=120) as response:
        body = response.read().decode()
    events = [json.loads(line[6:]) for line in body.splitlines() if line.startswith("data: ")]
    if not events:
        raise RuntimeError(f"No MCP response for {method}: {body[:300]}")
    result = events[-1]
    if "error" in result:
        raise RuntimeError(f"MCP {method} error: {result['error']}")
    return result["result"]


def tool_result(name, arguments, request_id):
    result = call("tools/call", {"name": name, "arguments": {"input_value": json.dumps(arguments)}}, request_id)
    if result.get("isError"):
        raise RuntimeError(f"MCP tool error: {name}")
    return json.loads(next(item["text"] for item in result["content"] if item["type"] == "text"))


def main():
    if not TOKEN:
        opener.open(f"{BASE}/api/v1/auto_login", timeout=30).close()
    initialized = call("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "proof2pay-verifier", "version": "1.0"}}, 1)
    names = sorted(item["name"] for item in call("tools/list", {}, 2)["tools"])
    expected = sorted(["analyze_job_completion", "validate_completion_evidence", "generate_completion_pack"])
    blocked = tool_result("validate_completion_evidence", {"job_id": "WO-1028"}, 3)
    no_approval = tool_result("generate_completion_pack", {"job_id": "WO-1028"}, 4)
    checks = {
        "three_named_tools": names == expected,
        "validation_call_blocked": blocked.get("billing_state") == "BLOCKED" and len(blocked.get("blockers", [])) == 3,
        "generation_requires_approval": "approved=true" in no_approval.get("error", ""),
    }
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": "local Langflow project MCP endpoint",
        "protocol_version": initialized.get("protocolVersion"),
        "tool_names": names,
        "synthetic_job": "WO-1028",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "note": "Direct MCP client verification; IBM Bob invocation is not established by this report.",
    }
    target = ROOT / "runs/mcp-verification-2026-09-28.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    if report["passed"] != report["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
