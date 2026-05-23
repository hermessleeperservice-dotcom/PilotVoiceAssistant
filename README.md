# Pilot Voice Assistant

**AI-assisted reflective memory system for strategic knowledge workers.**

> Cognitive continuity infrastructure — not another note-taking app.

## Working Codename

Pilot is a calm, calm and cognitive memory system.
Potential future names: Recall, Continuum, Thread, Echo, Mnemo

## Executive Summary

Pilot is an AI-assisted reflective memory system designed for strategic knowledge workers.

The core thesis: modern knowledge workers increasingly lose continuity of thought.

**What Pilot is NOT:**
- NOT a generic note-taking app
- NOT another task manager
- NOT a meeting transcription platform
- NOT a chatbot companion
- NOT a productivity dashboard

**What Pilot IS:** Cognitive continuity infrastructure
Initial wedge: **Voice reflections transformed into retrievable strategic memory.**

## Product Philosophy

**Pilot should feel like:** calm memory infrastructure, not productivity software.

### What Pilot optimizes for:
- continuity of thought
- retrieval relevance
- reduced cognitive load
- strategic synthesis
- longitudinal understanding
- reflection support

### What Pilot does NOT optimize for:
- engagement addiction
- note quantity
- dashboard complexity
- gamification
- task overload
- social mechanics

**Most important principle:** Retention matters more than storage.
The failure mode of most knowledge systems: becoming a graveyard of information.

## Initial Build Priorities

### Highest priority:
1. Fast capture
2. Strong summaries
3. High-quality retrieval
4. Reflection continuity

### Lowest priority:
- polish
- scale
- integrations
- collaboration
- automation complexity

## MVP Core Workflow

```mermaid
Capture → Transcribe → Summarize → Retrieve
```

## Recommended Stack

| Layer | Recommendation |
|-- ---|-- ----|-- ---|
| Mobile | SwiftUI |
| Backend | FastAPI + PostgreSQL |
| Storage | Supabase |
| Transcription | Whisper |
| AI Processing | OpenAI API |
| Embeddings | pgvector |
| File Storage | Supabase Storage |

## MVP Functional Requirements

### Feature 1 — Voice Capture
- One-tap recording
- Fast startup (<1 second)
- Background recording support
- Minimal friction
- Mobile-first

### Feature 2 — AI Transcription (Whisper)
- High accuracy
- Timestamp support
- transcript persistence
- **Success Metric:** 90%+ usable transcription quality

### Feature 3 — AI Synthesis
Each reflection should generate:
- summary
- key ideas
- action items
- themes/topics
- unresolved tensions
- strategic observations

**Important Principle:** Summaries should help users think.
Avoid: generic summaries, shallow extraction, meeting minutes style outputs.
- **Success Metric:** 70%+ summaries rated useful

### Feature 4 — Retrieval
Natural language retrieval.

Examples:
> "What did I say about omnichannel strategy?"
> "Show reflections related to stakeholder alignment."
> "What concerns have I repeated recently?"

**Technical Direction:** embeddings, vector search, metadata enrichment
- **Success Metric:** 80%+ retrieval relevance satisfaction

### Feature 5 — Reflective Timeline
Chronological memory feed including:
- recordings
- summaries
- themes
- actions
- related concepts

## Key Product Metrics

| **Metric**             | **Target** |
| ------ ----------      | ---------- |
| Weekly retrieval usage | 50%+       |
| Week 4 retention       | 40%+       |
| Daily captures         | 1+         |
| Summary usefulness     | 70%+       |
| Retrieval relevance    | 80%+       |
| Transcription quality  | 90%+       |

## Development Phases

### Phase 0 — Foundation
- [x] PRD
- [x] Architecture notes
- [x] Event tracking strategy
- [ ] Mobile app
- [ ] Backend API
- [ ] AI prompts

### Phase 1 — Functional Prototype
- [ ] Mobile capture MVP
- [ ] Backend API (capture → transcribe → summarize → retrieve)
- [ ] Whisper integration
- [ ] AI summarization
- [ ] Vector retrieval
- [ ] Reflective timeline
- [ ] Basic UI/UX

### Phase 2 — Founder Immersion
TBD

### Phase 3 — Closed Beta
TBD

### Phase 4 — Retrieval Intelligence
TBD

## Operating Principle

Every phase must answer a specific uncertainty.
Progression should happen only when:
- evidence supports the next step
- behavioral signals are positive
- retrieval demonstrates value

Avoid roadmap theatre.
The goal is: rapid learning, behavioral validation, product truth discovery.

## Suggested Repository Structure

```
/PilotVoiceAssistant
├── /mobile-app         # SwiftUI iOS app
├── /backend            # FastAPI backend
│   ├── /app            # API routes / services
│   ├── /db             # Database migrations
│   └── /tests          # Test suite
├── /docs               # Architecture, UX, strategy docs
├── /prompts            # AI prompt templates
├── /architecture       # Architecture notes
├── /experiments        # Experiment results
├── /weekly-learnings   # Phase 2 field notes
└── PRD-PilotVoiceAssistant.md  # Product Requirements Document
```
