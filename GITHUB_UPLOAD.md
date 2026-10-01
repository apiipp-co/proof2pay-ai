# GitHub repository and submission links

The public repository is [apiipp-co/proof2pay-ai](https://github.com/apiipp-co/proof2pay-ai). The contents of this directory are the repository root, so `README.md` opens first. Hidden `.bob/` and `.github/` folders, the Langflow JSON exports, evaluation reports, presentation files, and demo video are tracked.

The public [browser MVP](https://apiipp-co.github.io/proof2pay-ai/app/) is hosted as a static GitHub Pages site. It uses synthetic data in browser memory; the Langflow backend is not publicly hosted.

## Before submitting to the organizer

1. Check the participant name in [`SUBMISSION.md`](SUBMISSION.md) against the original registration, then use that exact name in the organizer's form. This is a solo entry.
2. Open the repository in a signed-out browser window and check that `README.md`, [`docs/02-pitch-deck.pptx`](docs/02-pitch-deck.pptx), [`langflow/exports/`](langflow/exports/), and [`demo/proof2pay-demo.mp4`](demo/proof2pay-demo.mp4) are accessible.
3. Submit the GitHub URL, authentic IBM SkillsBuild University Education course certificate, pitching deck PDF, and 3–5 project screenshots required by the official form. Use [`FORM_JAWABAN.md`](FORM_JAWABAN.md) for field-by-field answers.
4. Keep claims aligned with [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md). The browser demo, four deterministic Langflow flows, and guarded local Granite Agent work on the prepared Mac; an IBM Bob tool call has not been verified.

The public repository does not host the local Langflow server. `.bob/mcp.json` contains a loopback endpoint for the prepared Mac, not a public service or a credential. Never commit a private Langflow database, `.env` secret, or API key.

Check the [official program page](https://hacktiv8.com/projects/ibm/hackathon) and the actual organizer form for the current deadline and file formats. The course certificate required in the form is distinct from the Hackathon Certificate of Participation awarded after submission according to the organizer's message to the participant.
