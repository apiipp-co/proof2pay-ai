# AI Assistance Disclosure

This repository may use AI-assisted development tools during the hackathon. Keep this file updated for transparency.

## Project AI vs development AI

### Product AI

The browser demo and four MCP-exposed Langflow flows use deterministic rules. A separate native Agent flow runs local IBM Granite 3.3 2B through Ollama and calls the source-linked review tool. The model's free-form summary once misstated photo status, so the flow discards that draft and publishes a deterministic guarded result. This demonstrates model orchestration and a tool call, **not** reliable interpretation of unstructured field evidence. No retrieval pipeline or model accuracy result is claimed. Product safety boundaries are documented in `ResponsibleAI.md`.

### Development assistance

Record any AI coding/writing/design tools used to assist implementation.

| Tool | Assisted areas | Human verification |
|---|---|---|
| OpenAI Codex | repository audit, research synthesis, browser prototype, Langflow export builder and rules, documentation, tests, screen recording | solo participant should review code and final claims before submission |

## Human direction retained

The solo participant remains responsible for:

- choosing the problem and scope;
- validating claims and references;
- architecture and integration decisions;
- reviewing generated code/prompts;
- running tests;
- verifying the live demo;
- approving final submission claims.
