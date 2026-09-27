"""Create and export three real Langflow 1.12 flows in an isolated local instance.

Run only against a Langflow instance you control. The script creates a new project,
then exports it to langflow/exports/. It never stores authentication tokens.
"""

import copy
import gzip
import http.cookiejar
import io
import json
import os
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASE = os.environ.get("LANGFLOW_URL", "http://127.0.0.1:7862").rstrip("/")
TOKEN = os.environ.get("LANGFLOW_TOKEN")
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def request(path, method="GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with opener.open(req, timeout=120) as response:
            content = response.read()
            if content[:2] == b"\x1f\x8b":
                content = gzip.decompress(content)
            return json.loads(content) if response.headers.get_content_type() == "application/json" else content
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Langflow {method} {path} returned HTTP {exc.code}: {exc.read()[:400]!r}") from exc


def node(template, kind, suffix, x, y):
    out = copy.deepcopy(template)
    ident = f"{kind}-{suffix}"
    out["id"] = ident
    out["data"]["id"] = ident
    out["position"] = {"x": x, "y": y}
    out["positionAbsolute"] = {"x": x, "y": y}
    code = out["data"]["node"]["template"].get("code", {}).get("value")
    if isinstance(code, list):
        out["data"]["node"]["template"]["code"]["value"] = "\n".join(code)
    return out


def edge(source, target, output_name, input_name, output_types, input_types):
    source_info = {"dataType": source["data"]["type"], "id": source["id"], "name": output_name, "output_types": output_types}
    target_info = {"fieldName": input_name, "id": target["id"], "inputTypes": input_types, "type": "str"}
    compact = lambda value: json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace('"', "œ")
    readable = lambda value: json.dumps(value, ensure_ascii=False).replace('"', "œ")
    return {
        "animated": False,
        "className": "",
        "data": {"sourceHandle": source_info, "targetHandle": target_info},
        "id": f"reactflow__edge-{source['id']}{compact(source_info)}-{target['id']}{compact(target_info)}",
        "selected": False,
        "source": source["id"],
        "sourceHandle": readable(source_info),
        "target": target["id"],
        "targetHandle": readable(target_info),
    }


def main():
    if not TOKEN:
        request("/api/v1/auto_login")
    examples = request("/api/v1/flows/basic_examples/")
    basic = next(item for item in examples if item["name"] == "Basic Prompting")
    input_node = next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatInput")
    output_node = next(n for n in basic["data"]["nodes"] if n["data"].get("type") == "ChatOutput")
    component = request("/api/v1/all")["custom_component"]["CustomComponent"]
    source_code = (ROOT / "components/proof2pay_component.py").read_text()
    project = request("/api/v1/projects/", "POST", {"name": "PROOF2PAY AI - verified local demo", "description": "Synthetic evidence assessment and approval tools"})
    project_id = project["id"]
    flow_ids = []
    for action, name, description in [
        ("analyze", "analyze_job_completion", "Extract labelled claims from the synthetic WO-1028 technician note; claims are not proof."),
        ("validate", "validate_completion_evidence", "Assess synthetic WO-1028 against source-linked requirements and return blockers; never invoice."),
        ("generate", "generate_completion_pack", "Generate a synthetic completion pack only with complete critical evidence and explicit approval; no external action."),
    ]:
        inp = node(input_node, "ChatInput", action, 100, 100)
        inp["data"]["node"]["template"]["input_value"]["value"] = '{"job_id":"WO-1028"}'
        out = node(output_node, "ChatOutput", action, 850, 100)
        mid_id = f"CustomComponent-{action}"
        meta = copy.deepcopy(component)
        meta["display_name"] = name
        meta["description"] = description
        meta["template"]["code"]["value"] = source_code.replace('ACTION = "__ACTION__"', f'ACTION = "{action}"')
        meta["template"]["input_value"]["value"] = "{\"job_id\":\"WO-1028\"}"
        meta["base_classes"] = ["Message"]
        meta["outputs"][0]["name"] = "result"
        meta["outputs"][0]["display_name"] = "Structured result"
        meta["outputs"][0]["types"] = ["Message"]
        meta["outputs"][0]["selected"] = "Message"
        mid = {"id": mid_id, "type": "genericNode", "position": {"x": 475, "y": 100}, "positionAbsolute": {"x": 475, "y": 100}, "selected": False, "dragging": False, "data": {"id": mid_id, "type": "CustomComponent", "node": meta}}
        graph = {"nodes": [inp, mid, out], "edges": [edge(inp, mid, "message", "input_value", ["Message"], ["Message"]), edge(mid, out, "result", "input_value", ["Message"], ["Data", "JSON", "DataFrame", "Table", "Message"])], "viewport": {"x": 0, "y": 0, "zoom": 0.8}}
        created = request("/api/v1/flows/", "POST", {"name": name, "description": description, "folder_id": project_id, "data": graph, "mcp_enabled": True, "action_name": name, "action_description": description})
        flow_ids.append(created["id"])
        print(name, created["id"])
    archive = request(f"/api/v1/projects/download/{project_id}")
    export_dir = ROOT / "exports"
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        names = [name for name in zipped.namelist() if name.endswith(".json")]
        if len(names) != 3:
            raise RuntimeError(f"Expected three exported JSON flows, got {names}")
        for name in names:
            data = json.loads(zipped.read(name))
            target = export_dir / Path(name).name
            target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
            print("exported", target.relative_to(ROOT))
    (export_dir / "local-project-id.txt").write_text(project_id + "\n")
    print("project", project_id)


if __name__ == "__main__":
    main()
