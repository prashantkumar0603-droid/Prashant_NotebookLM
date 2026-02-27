# Enterprise NotebookLM

This repository contains a small Enterprise-focused NotebookLM project with a Python FastAPI backend and a React frontend.

## Repository

- GitHub: https://github.com/prashantkumar0603-droid/Prashant_NotebookLM

## Structure

- `backend/` — FastAPI backend and services
- `frontend/` — React frontend
- `data/` — local data (vectorstore index)

## Quickstart

Backend (recommended to use a virtual environment):

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\Activate.ps1 (PowerShell) or .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm start
```

## CI

A basic GitHub Actions workflow is included at `.github/workflows/ci.yml` which installs Python and Node dependencies and attempts a build on `push` and `pull_request`.

## Topics

Suggested repository topics: `notebooklm`, `fastapi`, `react`, `faiss`, `vector-search`, `rAG`.

## License

Unlicensed — add a license of your choice.

## Notes

- The FAISS index `data/vectorstore/index.faiss` is present in the repo; consider removing it from the repository if it's large and should not be tracked.

# Enterprise NotebookLM Local

Local AI research assistant similar to NotebookLM.

## Run

Backend:
uvicorn app.main:app --reload

Frontend:
npm start

Install models:
ollama pull mistral
