"""Append this class to the core component helpers before embedding in Langflow."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class JobRequestSchema(BaseModel):
    input_value: str = Field(description="JSON string with job_id and optional demo evidence or approval fields")


class Proof2PayToolset(Component):
    display_name = "Proof2Pay toolset"
    description = "Three source-linked review tools for a native Agent. No external action or credential."
    icon = "Wrench"
    name = "Proof2PayToolset"
    inputs = []
    outputs = [Output(display_name="Toolset", name="tools", method="build_tools", types=["Tool"])]

    def build_tools(self) -> list[StructuredTool]:
        descriptions = {
            "analyze": "Label work-order descriptions and technician claims with exact source references. Input is JSON text.",
            "validate": "Return requirement status and blockers. A Completed database status alone is not billing proof. Input is JSON text.",
            "generate": "Create only a synthetic demo completion pack after complete evidence and named human approval. Input is JSON text.",
        }
        names = {"analyze": "analyze_job_completion", "validate": "validate_completion_evidence", "generate": "generate_completion_pack"}
        tools = []
        for action, description in descriptions.items():
            def invoke(input_value: str, selected_action=action) -> str:
                try:
                    payload = parse_request(input_value)
                    result = run_action(payload, selected_action)
                except (ValueError, TypeError, json.JSONDecodeError) as exc:
                    result = {"error": str(exc), "action": selected_action}
                return json.dumps(result, ensure_ascii=False)

            tools.append(StructuredTool.from_function(
                name=names[action],
                description=description,
                func=invoke,
                args_schema=JobRequestSchema,
            ))
        return tools
