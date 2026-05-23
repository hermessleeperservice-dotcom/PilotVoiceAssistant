# Pilot Voice Assistant Tests

Unit tests for backend API.

```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/ -v
```

## Writing Tests

Follow the pattern:
1. Setup test client with FastAPI's TestClient
2. Mock OpenAI/Whisper calls
3. Assert response structure and status codes
4. Validate event logging occurs

## Test Categories

- `test_capture_endpoint` — file upload, validation
- `test_transcribe_endpoint` — Whisper integration
- `test_summarize_endpoint` — OpenAI summarization
- `test_search_endpoint` — retrieval accuracy
- `test_timeline_endpoint` — pagination, ordering
- `test_event_logging` — behavioral tracking
