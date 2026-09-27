"""Create or update the runnable four-node Proof2Pay review flow.

Uses the prepared local project. It does not touch credentials or delete flows.
"""

import copy
import json
from pathlib import Path

from build_export import ROOT, TOKEN, edge, node, request


NAME = "review_job_readiness"
DESCRIPTION = "Deterministic review agent: prompt policy, source-linked analysis, evidence validation, next actions, and human gate. No model or invoice."


def main():
    if not TOKEN:
        request("/api/v1/auto_login")
    project_id = (ROOT / "exports/local-project-id.txt").read_text().strip()
    examples = request("/api/v1/flows/basic_examples/")
    basic = next(item for item in examples if item["name"] == "Basic Prompting")
    rag = next(item for item in examples if item["name"] == "Vector Store RAG")
    input_template = next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatInput")
    output_template = next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatOutput")
    prompt_template = next(n for n in rag["data"]["nodes"] if n["data"].get("type") == "Prompt")
    inp = node(input_template, "ChatInput", "main", 100, 120)
    inp["data"]["node"]["template"]["input_value"]["value"] = '{"job_id":"2792861"}'
    prompt = node(prompt_template, "Prompt", "main", 420, 120)
    fields = prompt["data"]["node"]["template"]
    fields["template"]["value"] = (ROOT.parent / "prompts/main-review-policy.md").read_text()
    dynamic = copy.deepcopy(fields["question"])
    dynamic["name"] = "job_request"
    dynamic["display_name"] = "Job request JSON"
    fields.pop("context", None)
    fields.pop("question", None)
    fields["job_request"] = dynamic
    fields["job_request"]["value"] = '{"job_id":"2792861"}'

    component = request("/api/v1/all")["custom_component"]["CustomComponent"]
    meta = copy.deepcopy(component)
    meta["display_name"] = "Proof2Pay Review Agent (rules)"
    meta["description"] = "Analyze source claims, validate evidence, recommend next actions, and retain a human approval gate. Deterministic, no model."
    source = (ROOT / "components/proof2pay_component.py").read_text()
    meta["template"]["code"]["value"] = source.replace('ACTION = "__ACTION__"', 'ACTION = "orchestrate"')
    meta["template"]["input_value"]["value"] = ""
    meta["base_classes"] = ["Message"]
    meta["outputs"][0]["name"] = "result"
    meta["outputs"][0]["display_name"] = "Structured review"
    meta["outputs"][0]["types"] = ["Message"]
    meta["outputs"][0]["selected"] = "Message"
    mid_id = "CustomComponent-main"
    mid = {"id": mid_id, "type": "genericNode", "position": {"x": 755, "y": 120}, "positionAbsolute": {"x": 755, "y": 120}, "selected": False, "dragging": False, "data": {"id": mid_id, "type": "CustomComponent", "node": meta}}
    out = node(output_template, "ChatOutput", "main", 1100, 120)
    graph = {
        "nodes": [inp, prompt, mid, out],
        "edges": [
            edge(inp, prompt, "message", "job_request", ["Message"], ["Message", "Text"]),
            edge(prompt, mid, "prompt", "input_value", ["Message"], ["Message"]),
            edge(mid, out, "result", "input_value", ["Message"], ["Data", "JSON", "DataFrame", "Table", "Message"]),
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 0.75},
    }
    existing = next((flow for flow in request("/api/v1/flows/") if flow.get("folder_id") == project_id and flow.get("name") == NAME), None)
    if existing:
        flow = request("/api/v1/flows/" + existing["id"], "PATCH", {"data": graph, "description": DESCRIPTION, "mcp_enabled": True, "action_name": NAME, "action_description": DESCRIPTION})
    else:
        flow = request("/api/v1/flows/", "POST", {"name": NAME, "description": DESCRIPTION, "folder_id": project_id, "data": graph, "mcp_enabled": True, "action_name": NAME, "action_description": DESCRIPTION})
    target = ROOT / "exports" / (NAME + ".json")
    target.write_text(json.dumps(request("/api/v1/flows/" + flow["id"]), ensure_ascii=False, indent=2) + "\n")
    print("Saved", NAME, flow["id"], "to", target)


if __name__ == "__main__":
    main()
