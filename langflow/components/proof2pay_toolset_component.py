"""Append this class to the core component helpers before embedding in Langflow."""

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class JobRequestSchema(BaseModel):
    input_value: str | None = Field(default=None, description="JSON string with job_id and optional demo evidence or approval fields")
    type: str | None = Field(default=None, description="Use only when the model wraps a tool call")
    arguments: dict | None = Field(default=None, description="Use only when the model wraps a tool call; include input_value")


class Proof2PayToolset(Component):
    display_name = "Proof2Pay toolset"
    description = "Source-linked review tools for a native Agent. No external action or credential."
    icon = "Wrench"
    name = "Proof2PayToolset"
    inputs = [MessageTextInput(name="job_request", display_name="Original job request", required=True)]
    outputs = [Output(display_name="Toolset", name="tools", method="build_tools", types=["Tool"])]

    def build_tools(self) -> list[StructuredTool]:
        original_request = self.job_request
        descriptions = {
            "orchestrate": "Use this for a new job or billing-readiness question. It performs source-linked analysis and validation together and returns exact blockers. Input comes from the connected Chat Input.",
            "analyze": "Label work-order descriptions and technician claims with exact source references. Input is JSON text.",
            "validate": "Return requirement status and blockers. A Completed database status alone is not billing proof. Input is JSON text.",
            "generate": "Create only a synthetic demo completion pack after complete evidence and named human approval. Input is JSON text.",
        }
        names = {"orchestrate": "review_job_readiness", "analyze": "analyze_job_completion", "validate": "validate_completion_evidence", "generate": "generate_completion_pack"}
        tools = []
        for action, description in descriptions.items():
            def invoke(input_value: str | None = None, type: str | None = None, arguments: dict | None = None, selected_action=action) -> str:
                try:
                    # The connected Chat Input is authoritative. Small models can
                    # omit, wrap, or invent tool arguments; none may alter a job.
                    payload = parse_request(original_request)
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
