# GitHub repository and submission links

The public repository is [apiipp-co/proof2pay-ai](https://github.com/apiipp-co/proof2pay-ai). The contents of this directory are the repository root, so `README.md` opens first. Hidden `.bob/` and `.github/` folders, the Langflow JSON exports, evaluation reports, presentation files, and demo video are tracked.

The public [browser MVP](https://apiipp-co.github.io/proof2pay-ai/app/) is hosted as a static GitHub Pages site. It uses synthetic data in browser memory; the Langflow backend is not publicly hosted.

## Before submitting to the organizer

1. Fill in your real participant name in [`SUBMISSION.md`](SUBMISSION.md) and the organizer's form. This is a solo entry.
2. Open the repository in a signed-out browser window and check that `README.md`, [`docs/02-pitch-deck.pptx`](docs/02-pitch-deck.pptx), [`langflow/exports/`](langflow/exports/), and [`demo/proof2pay-demo.mp4`](demo/proof2pay-demo.mp4) are accessible.
3. Submit the GitHub URL and any other links or eligibility documents the official form requires. Attach only authentic participation evidence.
4. Keep claims aligned with [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md). The browser demo, four deterministic Langflow flows, and guarded local Granite Agent work on the prepared Mac; an IBM Bob tool call has not been verified.

The public repository does not host the local Langflow server. `.bob/mcp.json` contains a loopback endpoint for the prepared Mac, not a public service or a credential. Never commit a private Langflow database, `.env` secret, or API key.

Check the [official program page](https://hacktiv8.com/projects/ibm/hackathon) and the actual organizer form for current deadlines, certificate requirements, and allowed file/link formats before submitting.
