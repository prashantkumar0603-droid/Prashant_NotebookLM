# Developer Guide — Enterprise NotebookLM

This document helps contributors and maintainers get the project running locally and explains the repository structure and development workflow.

## Project overview

- Backend: FastAPI app in `backend/app`
- Frontend: React app in `frontend`
- Data: vector store index at `data/vectorstore/index.faiss` (may be large)

## Prerequisites

- Python 3.10+ (recommended)
- Node.js 18+ and npm
- Git
- (Optional) `gh` CLI for repository management

## Local setup — backend

1. Create and activate a virtual environment:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

3. Run the backend locally:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API servers run on `http://localhost:8000` with endpoints under `/api`.

## Local setup — frontend

1. Install dependencies and start dev server:

```bash
cd frontend
npm install
npm start
```

2. Open `http://localhost:3000` to view the UI. The frontend expects the backend to be available; update API base URLs in `frontend/src` if needed.

## Env vars and configuration

- `backend/app/config.py` contains central configuration. Add secrets and API keys via a `.env` file and load them in a secure way.
- Do NOT commit secrets or large binary files (consider Git LFS for large artifacts).

## Working with the vectorstore

- A FAISS index is stored at `data/vectorstore/index.faiss`. If it is large, remove it from git and add it to `.gitignore`.
- To rebuild the index, run the ingestion/parsing routines in `backend/app/parsers` and `backend/app/rag/retriever.py` as implemented.

## Tests and CI

- The repository includes a GitHub Actions workflow: `.github/workflows/ci.yml` which installs Python and Node and attempts a frontend build on push / pull_request.
- Add unit tests under `backend/tests` and `frontend/src/__tests__` and update the workflow to run those tests.

## Contributing

- Create feature branches from `main`: `feature/<short-descriptor>`.
- Open pull requests targeting `main`. Keep PRs focused and include a short description and testing notes.

## Debugging tips

- Backend logs: the app uses Python logging — check console output where `uvicorn` runs.
- Frontend devtools: use browser devtools for network/API issues.
- If a dependency mismatch occurs, remove `node_modules` and run `npm ci`.

## Formatting and linters

- Consider adding `prettier`, `eslint` for frontend and `ruff` / `black` / `mypy` for Python to keep code consistent.

## Deployment notes

- For production, run the backend under a production ASGI server (e.g., `gunicorn` + `uvicorn.workers.UvicornWorker`) behind a reverse proxy.
- Serve the frontend as static files from a web host / CDN or via a container.

## Repository maintenance

- Regularly audit `data/` for large files and move non-source artifacts out of git.
- Keep `requirements.txt` pinned for reproducible installs.

## Contact / ownership

- Repo: https://github.com/prashantkumar0603-droid/Prashant_NotebookLM
- Open issues for questions or to request access.
