# Pilot Project Foundation Document (PRD)

**Working Codename**: Pilot
Potential future names: Recall, Continuum, Thread, Echo, Mnemo

Pilot is a directional, assistive, calm memory system.

## Executive Summary

Pilot is an AI-assisted reflective memory system for strategic knowledge workers. It reduces cognitive fragmentation caused by:
- Excessive meetings
- Context switching
- Information overload
- Fragmented tools
- Lost continuity across weeks/months

Core thesis: Modern knowledge workers increasingly lose continuity of thought. AI-assisted reflective memory systems can preserve, synthesize, and retrieve high-value cognition over time.

**What Pilot is NOT**: A generic note-taking app, task manager, meeting transcription platform, chatbot companion, or productivity dashboard.

Pilot is: **Cognitive continuity infrastructure.**
Wedge: **Voice reflections transformed into retrievable strategic memory.**

## MVP Goal

Validate whether AI-assisted voice reflections can become genuinely useful reflective memory infrastructure.

**MVP Core Workflow**: `Capture → Transcribe → Summarize → Retrieve`

Everything outside this loop is secondary.

## MVP Functional Requirements

### Feature 1 — Voice Capture
- One-tap recording, fast startup, background recording support
- Minimal friction, mobile-first

### Feature 2 — AI Transcription (Whisper)
- High accuracy, timestamp support
- **Success Metric**: 90%+ usable transcription quality

### Feature 3 — AI Synthesis
Each reflection generates:
- Summaries (help users think, not generic meeting minutes)
- Key ideas, action items, themes/topics
- Unresolved tensions, strategic observations
- **Success Metric**: 70%+ summaries rated useful

### Feature 4 — Retrieval
- Natural language retrieval with embeddings/vector search
- **Success Metric**: 80%+ retrieval relevance satisfaction

### Feature 5 — Reflective Timeline
- Chronological memory feed with recordings, summaries, themes, actions

## Recommended Stack
| Layer | Recommendation |
|-------|----------------|
| Mobile | SwiftUI |
| Backend | Supabase + FastAPI |
| Auth | Supabase Auth |
| Transcription | Whisper |
| AI Processing | OpenAI API |
| Embeddings | pgvector |
| Storage | PostgreSQL |
| File Storage | Supabase Storage |

## Architecture Philosophy
**Keep architecture boring initially.** Do NOT build complex agents, LangGraph, heavy memory systems, or autonomous workflows. Prioritize speed, iteration, and retrieval validation.

## Development Phases
1. **Phase 0** — Foundation (PRD, architecture, UX, event tracking)
2. **Phase 1** — Functional prototype (capture → transcribe → summarize → retrieve)
3. **Phase 2** — Founder immersion (deep personal usage, behavioral tracking)
4. **Phase 3** — Closed beta (5-20 users, retention/retrieval metrics)
5. **Phase 4** — Retrieval intelligence (contextual resurfacing, theme detection)

## Operating Principle
Every phase must answer a specific uncertainty. Progress only when evidence supports it. Goal: rapid learning, behavioral validation, discovery.
