"""Prepare a native Langflow Agent with three existing tools, without secrets.

The flow stays MCP-disabled until a model provider is configured and tested.
It does not create or modify credential variables.
"""

import json

from build_export import ROOT, TOKEN, edge, node, request


NAME = "agent_orchestration_requires_model"
DESCRIPTION = "Native Agent connected to Proof2Pay tools. Model credential is intentionally unset; use review_job_readiness for a runnable offline flow."
def main():
    if not TOKEN:
        request("/api/v1/auto_login")
    project_id = (ROOT / "exports/local-project-id.txt").read_text().strip()
    examples = request("/api/v1/flows/basic_examples/")
    basic = next(x for x in examples if x["name"] == "Basic Prompting")
    simple = next(x for x in examples if x["name"] == "Simple Agent")
    inp = node(next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatInput"), "ChatInput", "agent", 80, 120)
    inp["data"]["node"]["template"]["input_value"]["value"] = '{"job_id":"WO-1028"}'
    prompt = node(next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "Prompt"), "Prompt", "agent", 370, 120)
    prompt["data"]["node"]["template"]["template"]["value"] = (ROOT.parent / "prompts/agent-orchestration.md").read_text()
    agent = node(next(n for n in simple["data"]["nodes"] if n["data"].get("type") == "Agent"), "Agent", "proof2pay", 720, 120)
    agent["data"]["node"]["template"]["add_calculator_tool"]["value"] = False
    agent["data"]["node"]["template"]["add_current_date_tool"]["value"] = False
    agent["data"]["node"]["template"]["model"]["value"] = ""
    out = node(next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatOutput"), "ChatOutput", "agent", 1110, 120)

    core = (ROOT / "components/proof2pay_component.py").read_text().split("class Proof2PayComponent(Component):")[0]
    toolset_source = core + "\n" + (ROOT / "components/proof2pay_toolset_component.py").read_text()
    toolset_meta = request("/api/v1/custom_component", "POST", {"code": toolset_source})["data"]
    toolset = {"id": "CustomComponent-toolset", "type": "genericNode", "position": {"x": 370, "y": 440}, "positionAbsolute": {"x": 370, "y": 440}, "selected": False, "dragging": False, "data": {"id": "CustomComponent-toolset", "type": "CustomComponent", "node": toolset_meta}}
    graph = {
        "nodes": [inp, prompt, agent, out, toolset],
        "edges": [
            edge(inp, agent, "message", "input_value", ["Message"], ["Message"]),
            edge(prompt, agent, "prompt", "system_prompt", ["Message"], ["Message"]),
            edge(toolset, agent, "tools", "tools", ["Tool", "StructuredTool"], ["Tool"], field_type="other"),
            edge(agent, out, "response", "input_value", ["Message"], ["Data", "JSON", "DataFrame", "Table", "Message"]),
        ],
        "viewport": {"x": 0, "y": 0, "zoom": 0.55},
    }
    existing = next((flow for flow in request("/api/v1/flows/") if flow.get("folder_id") == project_id and flow.get("name") == NAME), None)
    if existing:
        flow = request("/api/v1/flows/" + existing["id"], "PATCH", {"data": graph, "description": DESCRIPTION, "mcp_enabled": False})
    else:
        flow = request("/api/v1/flows/", "POST", {"name": NAME, "description": DESCRIPTION, "folder_id": project_id, "data": graph, "mcp_enabled": False})
    target = ROOT / "exports" / (NAME + ".json")
    target.write_text(json.dumps(request("/api/v1/flows/" + flow["id"]), ensure_ascii=False, indent=2) + "\n")
    print("Prepared", NAME, flow["id"], "without a model credential")


if __name__ == "__main__":
    main()
