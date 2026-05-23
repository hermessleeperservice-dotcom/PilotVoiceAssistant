# Pilot API

<!-- Written autonomously by Hermes agent to build Pilot MVP -->
<!-- Date: 2026-05-23 -->

## MVP Core Loop

```
Capture → Transcribe → Summarize → Retrieve
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/v1/capture` | Save uploaded audio file |
| `POST` | `/api/v1/transcribe/{reflection_id}` | Transcribe audio via Whisper |
| `POST` | `/api/v1/retrieve` | Semantic search reflections |
| `GET` | `/api/v1/timeline` | Chronological reflection feed |
| `GET` | `/api/v1/reflections/{id}` | Get single reflection |
| `GET` | `/api/v1/recommendations` | Suggested related reflections |
| `GET` | `/api/v1/health` | Health check |
