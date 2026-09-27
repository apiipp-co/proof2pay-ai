"""Update the three prepared local Langflow flows and re-export their JSON.

This preserves flow IDs used by the Bob MCP configuration. It never creates a
new project. Run only against the prepared local instance you control.
"""

import hashlib
import io
import json
import zipfile

from build_export import ROOT, TOKEN, request


def main():
    public = json.loads((ROOT.parent / "data/public/nyc-parks-work-orders.json").read_text())
    records = public["records"]
    canonical = json.dumps(records, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    if digest != public["selected_rows_sha256"]:
        raise RuntimeError("Public snapshot checksum mismatch")
    source = (ROOT / "components/proof2pay_component.py").read_text()
    if digest not in source:
        raise RuntimeError("Embedded snapshot checksum differs from public data")
    # Extract embedded constant without importing Langflow on the host Python.
    import ast
    tree = ast.parse(source)
    record_node = next(node.value for node in tree.body if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "PUBLIC_RECORDS" for target in node.targets))
    embedded = ast.literal_eval(record_node)
    if embedded != {row["evt_code"]: row for row in records}:
        raise RuntimeError("Embedded public records differ from source snapshot")

    if not TOKEN:
        request("/api/v1/auto_login")
    export_dir = ROOT / "exports"
    actions = {"analyze_job_completion": "analyze", "validate_completion_evidence": "validate", "generate_completion_pack": "generate"}
    for name, action in actions.items():
        path = export_dir / (name + ".json")
        flow_id = json.loads(path.read_text())["id"]
        flow = request("/api/v1/flows/" + flow_id)
        graph = flow["data"]
        for node in graph["nodes"]:
            code = node["data"]["node"]["template"].get("code")
            if code and isinstance(code.get("value"), list):
                code["value"] = "\n".join(code["value"])
            if node["data"]["type"] == "CustomComponent":
                code["value"] = source.replace('ACTION = "__ACTION__"', f'ACTION = "{action}"')
        request("/api/v1/flows/" + flow_id, "PATCH", {"data": graph})
        print("Updated", name, flow_id)

    project_id = (export_dir / "local-project-id.txt").read_text().strip()
    archive = request("/api/v1/projects/download/" + project_id)
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        names = [name for name in zipped.namelist() if name.endswith(".json")]
        if len(names) != 3:
            raise RuntimeError("Expected three flow exports")
        for name in names:
            flow = json.loads(zipped.read(name))
            target = export_dir / (flow["name"] + ".json")
            target.write_text(json.dumps(flow, ensure_ascii=False, indent=2) + "\n")
            print("Exported", target)


if __name__ == "__main__":
    main()
