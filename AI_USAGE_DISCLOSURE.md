# AI Assistance Disclosure

This repository may use AI-assisted development tools during the hackathon. Keep this file updated for transparency.

## Project AI vs development AI

### Product AI

The working PROOF2PAY demo uses deterministic rules in the browser and in four Langflow flows. A fifth native Agent flow has its prompt and three tools connected, but no model is selected and it has not run. The working demo does **not** run an AI model or retrieval pipeline. AI interpretation of unstructured evidence is a proposed extension that needs a model, grounding checks, and separate evaluation before it can be claimed. Product safety boundaries are documented in `ResponsibleAI.md`.

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
