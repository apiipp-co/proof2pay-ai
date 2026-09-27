# GitHub upload

The project is already unzipped. Upload the **contents of this `proof2pay-ai` directory** as the repository root so GitHub displays `README.md`. Keep `.bob/`, `.github/`, `app/`, `langflow/exports/`, `langflow/runs/`, `docs/`, and `demo/proof2pay-demo.mp4`.

## Before publishing

1. Add your real participant name and final repository URL to `SUBMISSION.md`. You confirmed this is a solo entry; there is no team roster to invent.
2. Run `node --test app/core.test.mjs`. On the prepared Mac, run `scripts/start-langflow-local.sh` and both `python3 langflow/verify_live.py` and `python3 langflow/verify_mcp.py`.
3. Confirm `.bob/mcp.json` contains only the local endpoint and no secret. The private Langflow database and key live outside this repository.
4. Create an empty GitHub repository and upload this folder's contents, including hidden folders. Add its URL to the official submission form.

GitHub Pages can host the static browser demo at `/app/`, but it cannot run the local Langflow server. A published repository or Pages URL is not proof that Bob executed a tool. The silent video is available locally; upload it or link a hosted copy if the organizer requires a video URL.

Check the [official program page](https://hacktiv8.com/projects/ibm/hackathon) and the actual organizer form for current deadlines, certificate requirements, and allowed file/link formats before submitting.
