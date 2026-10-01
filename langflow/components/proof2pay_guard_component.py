"""Append to the core helper source for a guarded native-Agent output."""


class Proof2PayAgentGuard(Component):
    display_name = "Proof2Pay output guard"
    description = "Publish a source-linked deterministic review after the Agent runs; discard unverified model prose."
    icon = "ShieldCheck"
    name = "Proof2PayAgentGuard"

    inputs = [
        MessageTextInput(name="job_request", display_name="Original job request", required=True),
        MessageTextInput(name="agent_response", display_name="Agent draft", required=True),
    ]
    outputs = [Output(display_name="Guarded review", name="result", method="build_output")]

    def build_output(self) -> Message:
        try:
            draft = getattr(self.agent_response, "text", self.agent_response)
            if not str(draft or "").strip():
                raise ValueError("Agent did not return a draft; review was not published")
            payload = parse_request(self.job_request)
            result = run_action(payload, "orchestrate")
            result["output_policy"] = "SOURCE_LINKED_RULES_AUTHORITATIVE"
            result["model_draft_used"] = False
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            result = {"error": str(exc), "output_policy": "BLOCKED"}
        return Message(text=json.dumps(result, ensure_ascii=False, separators=(",", ":")))
