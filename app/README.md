# MVP Application

This folder contains a runnable, dependency-free browser prototype for the synthetic `WO-1028` case.

## Run

From the repository root:

```bash
python3 -m http.server 8000
```

Visit `http://localhost:8000/app/`. The app also works from GitHub Pages when Pages publishes the repository root. Do not open `index.html` as a `file://` URL: the browser must fetch the case JSON.

To verify the deterministic rules (Node 18+):

```bash
node --test app/core.test.mjs
```

## Demo sequence

1. Open `WO-1028`: cooling evidence is ambiguous; acknowledgement and final report are missing.
2. Add the synthetic cooling reading and customer acknowledgement.
3. Enter a reviewer name and explicitly confirm review.
4. Generate the final demo report and download the JSON completion pack.

The state and evidence live in browser memory; reload to reset. No files are uploaded and no external action occurs. This prototype uses hard-coded demo actions and deterministic rules. It does not run AI, IBM Bob, MCP, or Langflow.

## Minimum screens

1. Dashboard / job queue
2. Job detail + readiness state
3. Requirement-to-evidence matrix
4. Blocker detail / source explanation
5. Human approval modal
6. Completion-pack result

## UX principle

The interface should answer four questions quickly:

1. What was required?
2. What proof exists?
3. What blocks billing readiness?
4. What should happen next?

## Files

- `index.html` / `style.css` / `main.mjs`: accessible interface and local interaction.
- `core.mjs`: pure assessment and approval rules.
- `core.test.mjs`: runnable safety and golden-case checks.
- `../demo/golden-case-WO-1028.json`: source fixture.
