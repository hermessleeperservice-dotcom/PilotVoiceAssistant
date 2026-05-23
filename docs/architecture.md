# Architecture Notes

> Per PRD §12, §13: **Keep architecture boring initially.**

## System Overview

```
┌─────────────┐     HTTPS/JSON     ┌──────────────────┐     PostgreSQL     ┌──────────────┐
│   Mobile App │ ◄────────────────► │    FastAPI Backend│ ◄────────────────► │   Supabase    │
│   (SwiftUI)  │  REST APIs         │     (Python)      │   pgvector search │   (Storage +  │
│              │ ↑                  │                   │                   │   Database)   │
│  ┌────────┐  │ │                  │  ┌─────────────┐  │                   └──────────────┘
│  │ Capture │  │ │                  │  │ Whisper     │  │
│  │ Service │  │ │                  │  │ Engine      │  │
│  └────────┘  │ │                  │  └─────────────┘  │
│  ┌────────┐  │ │                  │  ┌─────────────┐  │
│  │Timeline│  │ │                  │  │ OpenAI API  │  │
│  │  Feed  │  │ │                  │  │ (Summaries) │  │
│  └────────┘  │ │                  │  └─────────────┘  │
└─────────────┘  │                  └──────────────────┘
                 │
                 │
            ┌─────────────┐
            │  pgvector   │
            │  Embeddings │
            └─────────────┘
```

## Core Components

### 1. Mobile App (SwiftUI)
- Primary interface for voice capture
- Minimal UI: one-record button, timeline feed, search
- Background recording capability
- Local caching for offline support

### 2. Backend API (FastAPI)
- RESTful endpoints for:
  - `POST /api/v1/capture` - Upload audio
  - `POST /api/v1/transcribe` - Transcribe audio (async)
  - `POST /api/v1/summarize` - AI synthesis (async)
  - `GET /api/v1/reflections` - Retrieval feed
  - `GET /api/v1/search` - Vector-based retrieval
  - `GET /api/v1/reflections/{id}` - Individual reflection
  - `GET /api/v1/timeline` - Chronological feed
- Lightweight workers for async processing

### 3. Database (PostgreSQL + pgvector)
- Core tables: `reflections`, `user`, `embeddings`, `events`
- pgvector for semantic search
- GIN indexes for metadata filtering

### 4. Transcription (Whisper)
- openai-whisper Python library
- `base` model for MVP (scalable to `medium`/`large`)
- Output: full transcript with timestamps

### 5. AI Processing (OpenAI API)
- `gpt-4o-mini` for MVP (cost-effective)
- Tasks:
  - Summarization
  - Key idea extraction
  - Action item detection
  - Theme/topic labeling
  - Unresolved tension identification
  - Embedding generation (text-embedding-ada-002)

## Data Flow

```
Capture → Audio File → Backend → Whisper → Transcript → OpenAI → Summary
                                                                ↓
                                                          Embedding
                                                                ↓
                                                          pgvector Store
                                                                ↓
                                                      User searches →
                                                    Vector similarity →
                                                        Reflections
```

## MVP Constraints

Per PRD §13, the architecture MUST NOT include:
- ❌ Complex agents
- ❌ LangGraph orchestration
- ❌ Heavy memory systems
- ❌ Autonomous workflows
- ❌ Advanced RAG pipelines
- ❌ Enterprise abstractions

Per PRD §13, MVP MUST prioritize:
- ✅ Speed
- ✅ Iteration
- ✅ Behavioral learning
- ✅ Retrieval validation

## Cost Considerations

### OpenAI API (MVP estimates for 10 reflections/day):
- Whisper transcription: ~$0.006/min (base model)
- GPT-4o-mini summarization: ~$0.00015/1K tokens
- text-embedding-ada-002: ~$0.0001/1K tokens
- **Estimated daily cost**: ~$0.50-1.00 (at 3 min/reflection × 10/day)
- **Estimated monthly cost**: ~$15-30

### Supabase (Free Tier):
- 500MB database
- 1GB storage
- 50GB bandwidth
- **More than sufficient for MVP**

## Deployment Strategy

### Phase 1 (MVP):
- Backend: Local development → Supabase Edge Functions or Railway
- Database: Supabase PostgreSQL
- Storage: Supabase Storage
- Mobile: App Store submission (Phase 3)

### Phase 3+ (Beta):
- Backend: Supabase Edge Functions or Fly.io
- Database: Supabase PostgreSQL (scaled if needed)
- Mobile: App Store + TestFlight beta

## Tech Decisions Rationale

### Why FastAPI over other frameworks?
- Async support for concurrent Whisper/OpenAI calls
- Automatic OpenAPI docs
- Pydantic models for validation
- Fast startup, low overhead

### Why pgvector?
- Native PostgreSQL integration (no separate vector DB)
- HNSW index for fast similarity search
- Mature, well-documented
- Avoids additional infrastructure

### Why OpenAI for MVP?
- Proven quality (Whisper + GPT-4o-mini + ada-002)
- Simple API, fast iteration
- Cost-effective at small scale
- Can swap to alternatives later (Azure, local models)

### Why Supabase?
- PostgreSQL + Auth + Storage in one package
- Reduces infrastructure complexity
- Free tier covers MVP scale
- Follows "boring architecture" principle

## Future Considerations (NOT for MVP)

- [ ] Local Whisper model (privacy, cost savings)
- [ ] Custom embedding model (domain-specific)
- [ ] Advanced RAG for retrieval
- [ ] Knowledge graph for cross-reflection linking
- [ ] Proactive resurfacing engine
- [ ] Desktop app (macOS/Windows)
- [ ] Web interface
