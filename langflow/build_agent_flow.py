"""Prepare native Langflow Agents with three existing tools, without secrets.

Run with --local-granite to add an Ollama model node to a separate flow.
Both flows stay MCP-disabled until independently verified. No credential is changed.
"""

import json
import sys

from build_export import ROOT, TOKEN, edge, node, request


LOCAL_GRANITE = "--local-granite" in sys.argv
NAME = "agent_orchestration_local_granite" if LOCAL_GRANITE else "agent_orchestration_requires_model"
DESCRIPTION = (
    "Native Agent using local IBM Granite 3.3 2B and four tools; a deterministic output guard blocks unsupported model summaries."
    if LOCAL_GRANITE else
    "Native Agent connected to Proof2Pay tools. Model credential is intentionally unset; use review_job_readiness for a runnable offline flow."
)
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
    if LOCAL_GRANITE:
        agent["data"]["node"]["template"]["max_iterations"]["value"] = 5
        agent["data"]["node"]["template"]["max_tokens"]["value"] = 512
        agent["data"]["node"]["template"]["n_messages"]["value"] = 0
    out = node(next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatOutput"), "ChatOutput", "agent", 1410 if LOCAL_GRANITE else 1110, 120)

    core = (ROOT / "components/proof2pay_component.py").read_text().split("class Proof2PayComponent(Component):")[0]
    toolset_source = core + "\n" + (ROOT / "components/proof2pay_toolset_component.py").read_text()
    toolset_meta = request("/api/v1/custom_component", "POST", {"code": toolset_source})["data"]
    toolset = {"id": "CustomComponent-toolset", "type": "genericNode", "position": {"x": 370, "y": 440}, "positionAbsolute": {"x": 370, "y": 440}, "selected": False, "dragging": False, "data": {"id": "CustomComponent-toolset", "type": "CustomComponent", "node": toolset_meta}}
    nodes = [inp, prompt, agent, out, toolset]
    edges = [
            edge(inp, agent, "message", "input_value", ["Message"], ["Message"]),
            edge(inp, toolset, "message", "job_request", ["Message"], ["Message"], field_type="str"),
            edge(prompt, agent, "prompt", "system_prompt", ["Message"], ["Message"]),
            edge(toolset, agent, "tools", "tools", ["Tool", "StructuredTool"], ["Tool"], field_type="other"),
    ]
    if LOCAL_GRANITE:
        guard_source = core + "\n" + (ROOT / "components/proof2pay_guard_component.py").read_text()
        guard_meta = request("/api/v1/custom_component", "POST", {"code": guard_source})["data"]
        guard = {"id": "CustomComponent-guard", "type": "genericNode", "position": {"x": 1070, "y": 120}, "positionAbsolute": {"x": 1070, "y": 120}, "selected": False, "dragging": False, "data": {"id": "CustomComponent-guard", "type": "CustomComponent", "node": guard_meta}}
        nodes.append(guard)
        edges.extend([
            edge(inp, guard, "message", "job_request", ["Message"], ["Message"], field_type="str"),
            edge(agent, guard, "response", "agent_response", ["Message"], ["Message"], field_type="str"),
            edge(guard, out, "result", "input_value", ["Message"], ["Data", "JSON", "DataFrame", "Table", "Message"]),
        ])
        structured_example = next(x for x in examples if x["name"] == "Structured Data Analysis Agent")
        ollama_template = next(n for n in structured_example["data"]["nodes"] if n["data"].get("type") == "OllamaModel")
        ollama = node(ollama_template, "OllamaModel", "proof2pay", 370, -200)
        ollama["data"]["node"]["template"]["model_name"]["value"] = "granite3.3:2b"
        ollama["data"]["node"]["template"]["base_url"]["value"] = "http://127.0.0.1:11434"
        ollama["data"]["node"]["template"]["temperature"]["value"] = 0.1
        ollama["data"]["node"]["template"]["num_ctx"]["value"] = 8192
        nodes.append(ollama)
        edges.append(edge(ollama, agent, "model_output", "model", ["LanguageModel"], ["LanguageModel"], field_type="model"))
    else:
        edges.append(edge(agent, out, "response", "input_value", ["Message"], ["Data", "JSON", "DataFrame", "Table", "Message"]))
    graph = {
        "nodes": nodes,
        "edges": edges,
        "viewport": {"x": 0, "y": 0, "zoom": 0.55},
    }
    existing = next((flow for flow in request("/api/v1/flows/") if flow.get("folder_id") == project_id and flow.get("name") == NAME), None)
    if existing:
        flow = request("/api/v1/flows/" + existing["id"], "PATCH", {"data": graph, "description": DESCRIPTION, "mcp_enabled": False})
    else:
        flow = request("/api/v1/flows/", "POST", {"name": NAME, "description": DESCRIPTION, "folder_id": project_id, "data": graph, "mcp_enabled": False})
    target = ROOT / "exports" / (NAME + ".json")
    target.write_text(json.dumps(request("/api/v1/flows/" + flow["id"]), ensure_ascii=False, indent=2) + "\n")
    print("Prepared", NAME, flow["id"], "with local Granite" if LOCAL_GRANITE else "without a model credential")


if __name__ == "__main__":
    main()
