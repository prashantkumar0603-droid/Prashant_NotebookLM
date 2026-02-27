# User Guide — Enterprise NotebookLM

This guide is intended for end users who want to interact with the application through the web interface or APIs.

## Accessing the Application

1. Make sure the backend server is running on `http://localhost:8000` and the frontend is served on `http://localhost:3000`.
2. Open a browser and navigate to the frontend URL; login or authenticate if implemented.

## Features

- **Upload Documents:** Drag and drop or select PDF/DOCX files to ingest them into the vector store.
- **Chat Interface:** Enter natural language questions in the chat box; the system uses LLM and retrieval to answer based on ingested documents.
- **Research Endpoint:** Use `/api/research` to run agent-based research tasks programmatically.
- **Notes:** Save and retrieve notes via `/api/notes`.

## API Usage

The backend exposes several REST endpoints under `/api`:

| Endpoint        | Method | Description |
|-----------------|--------|-------------|
| `/documents`    | POST   | Upload or index a document |
| `/chat`         | POST   | Send a chat query |
| `/research`     | POST   | Execute a research agent task |
| `/notes`        | GET/POST | Retrieve or save notes |
| `/health`       | GET    | Check service health |

Example curl request:

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarize the document."}'
```

## Troubleshooting

- If the frontend cannot reach the backend, verify CORS settings in `backend/app/main.py`.
- Errors from the vector store may mean the FAISS index is corrupted; rebuild it by re-ingesting documents.

