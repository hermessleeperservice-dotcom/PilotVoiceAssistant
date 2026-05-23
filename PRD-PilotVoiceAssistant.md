# **Pilot — Project Foundation Document**

## **Working Codename**

Pilot

Potential future names:

- Recall
- Continuum
- Thread
- Echo
- Mnemo

Pilot is preferred currently because it feels:

- directional
- assistive without sounding subordinate
- calm and lightweight
- compatible with navigation and guidance metaphors
- broad enough to evolve beyond note-taking

---

# **1. Executive Summary**

Pilot is an AI-assisted reflective memory system designed for strategic knowledge workers.

The system aims to reduce the cognitive fragmentation caused by:

- excessive meetings
- context switching
- information overload
- fragmented tools
- loss of continuity across weeks and months

The core thesis:

Modern knowledge workers increasingly lose continuity of thought.

AI-assisted reflective memory systems can help preserve, synthesise, and retrieve high-value cognition over time.

Pilot is NOT intended to become:

- a generic note-taking app
- another task manager
- a meeting transcription platform
- a chatbot companion
- a productivity dashboard

The product direction is:

Cognitive continuity infrastructure.

The initial wedge:

Voice reflections transformed into retrievable strategic memory.

---

# **2. Naming Clarification**

Meridian is the existing name used internally for the Hermes Agent environment and supporting agent infrastructure.

Pilot is the product/application being created.

Recommended terminology:

| **Name** | **Purpose**                                  |
| -------- | -------------------------------------------- |
| Pilot    | User-facing application/product              |
| Meridian | Internal agent/workspace/runtime environment |
| Hermes   | Agent framework/automation layer             |

This distinction should remain clear in:

- repositories
- documentation
- prompts
- architecture discussions
- branding decisions
- internal tooling

---

# **3. Core Product Thesis**

## **Primary Thesis**

Strategic knowledge workers generate valuable cognition verbally:

- after meetings
- during walks
- during planning
- during reflections
- while processing ambiguity

Much of this cognition is:

- never captured
- poorly organised
- difficult to retrieve
- disconnected over time

Existing tools optimise for:

- storage
- documents
- tasks
- collaboration

Very few optimise for:

- longitudinal cognition
- continuity of thought
- contextual resurfacing
- reflective synthesis

Pilot aims to solve:

effortless cognitive capture + meaningful retrieval.

---

# **4. Product Philosophy**

## **Core Principle**

Pilot should feel like:

- calm memory infrastructure

    not

- productivity software.

---

## **Product Should Optimise For**

- continuity of thought
- retrieval relevance
- reduced cognitive load
- strategic synthesis
- longitudinal understanding
- reflection support

---

## **Product Should NOT Optimise For**

- engagement addiction
- note quantity
- dashboard complexity
- gamification
- task overload
- social mechanics

---

## **Most Important Design Principle**

Retrieval matters more than storage.

The failure mode of most knowledge systems:

becoming a graveyard of information.

Pilot succeeds only if:

- users repeatedly retrieve value
- previous thoughts become reusable
- the system creates continuity across time

---

# **5. Initial Target Users**

## **Primary ICP**

Strategic knowledge workers who:

- think verbally
- operate across many contexts
- attend many meetings
- synthesise ambiguity
- manage long-term initiatives
- value reflection
- experience cognitive fragmentation

Examples:

- product leaders
- UX leaders
- researchers
- founders
- consultants
- strategists
- ADHD/neurodivergent thinkers

---

# **6. Problem Definition**

## **Current Problems**

Users currently:

- lose valuable thoughts
- repeat the same thinking
- forget strategic insights
- struggle to connect past ideas
- store information without resurfacing it

Current tools create:

- archives

    not

- active memory.

---

# **7. MVP Definition**

## **MVP Goal**

Validate whether AI-assisted voice reflections can become genuinely useful reflective memory infrastructure.

The MVP is NOT intended to:

- replace Notion
- replace Obsidian
- replace meeting software
- automate work
- create autonomous agents
- become a full second brain

The MVP only needs to prove:

1. Users capture regularly
2. Summaries are useful
3. Retrieval is valuable
4. Users return repeatedly
5. The system creates continuity of thought

---

# **8. MVP Scope**

## **Core Workflow**

Capture → Transcribe → Summarise → Retrieve

Everything outside this loop is secondary.

---

# **9. MVP Functional Requirements**

## **Feature 1 — Voice Capture**

### **Requirements**

- One-tap recording
- Fast startup
- Background recording support
- Minimal friction
- Mobile-first

### **Non-Goals**

- Wearables
- Desktop app
- Meeting bots
- Real-time streaming

---

## **Feature 2 — AI Transcription**

### **Requirements**

- Whisper transcription
- High accuracy
- Timestamp support
- Transcript persistence

### **Success Metric**

90%+ usable transcription quality

---

## **Feature 3 — AI Synthesis**

### **Outputs**

Each reflection should generate:

- summary
- key ideas
- action items
- themes/topics
- unresolved tensions
- strategic observations

### **Important Principle**

Summaries should help users think.

Avoid:

- generic summaries
- shallow extraction
- meeting minutes style outputs

### **Success Metric**

70%+ summaries rated useful

---

## **Feature 4 — Retrieval**

### **Requirements**

Natural language retrieval.

Examples:

- “What did I say about omnichannel strategy?”
- “Show reflections related to stakeholder alignment.”
- “What concerns have I repeated recently?”

### **Technical Direction**

- embeddings
- vector search
- metadata enrichment

### **Success Metric**

80%+ retrieval relevance satisfaction

---

## **Feature 5 — Reflective Timeline**

### **Requirements**

Chronological memory feed including:

- recordings
- summaries
- themes
- actions
- related concepts

### **Goal**

Support longitudinal thinking.

---

# **10. Explicit Non-Goals**

The MVP must NOT include:

- team collaboration
- enterprise admin
- email integration
- calendar integration
- autonomous agents
- proactive AI assistant
- multimodal capture
- advanced knowledge graphs
- wearable hardware
- productivity dashboards
- social features
- advanced workflows

Avoid scope explosion aggressively.

---

# **11. Most Important Product Insight**

The core challenge is NOT:

- storing information

The core challenge IS:

- resurfacing the right cognition at the right time.

The real product question:

When should memories return?

Examples:

- before a stakeholder meeting
- during roadmap planning
- while revisiting strategy
- during recurring organisational tensions
- while making decisions

This becomes a future differentiator.

---

# **12. Recommended Initial Technical Architecture**

## **Recommended Stack**

| **Layer**      | **Recommendation**            |
| -------------- | ----------------------------- |
| Mobile App     | SwiftUI                       |
| Backend        | Supabase                      |
| Authentication | Supabase Auth                 |
| Transcription  | Whisper                       |
| AI Processing  | OpenAI API                    |
| Embeddings     | pgvector                      |
| Storage        | PostgreSQL                    |
| File Storage   | Supabase Storage              |
| Orchestration  | Lightweight workers initially |

---

# **13. Important Architectural Philosophy**

## **Keep Architecture Boring Initially**

Do NOT prematurely build:

- complex agents
- LangGraph orchestration
- heavy memory systems
- autonomous workflows
- advanced RAG pipelines

The MVP should prioritise:

- speed
- iteration
- behavioural learning
- retrieval validation

Technical sophistication is secondary to product truth.

---

# **14. Recommended Product Development Phases**

# **Phase 0 — Foundation**

## **Goal**

Establish:

- product thesis
- scope
- architecture
- evaluation criteria

## **Deliverables**

- PRD
- architecture notes
- UX principles
- success metrics
- repo structure
- event tracking strategy

## **Exit Criteria**

Ability to explain:

- target user
- problem
- workflow
- differentiation

in under 2 minutes.

---

# **Phase 1 — Functional Prototype**

## **Goal**

Validate core memory loop.

## **Scope**

Capture → Transcribe → Summarise → Retrieve

## **Critical Question**

Does captured cognition become meaningfully reusable?

## **Success Signals**

- daily captures occur naturally
- summaries reduce replay need
- retrieval produces useful resurfacing

## **Failure Signals**

Users treat it as:

- simple recorder
- transcript archive
- novelty tool

---

# **Phase 2 — Founder Immersion**

## **Goal**

Deep personal usage.

## **Required Usage**

Use during:

- walks
- post-meeting reflections
- strategy thinking
- organisational processing
- planning sessions

## **Critical Observations**

Track:

- capture friction
- retrieval failures
- shallow summaries
- trust issues
- emotional response

## **Most Important Question**

Does Pilot create continuity of thought across weeks?

---

# **Phase 3 — Closed Beta**

## **Goal**

Validate repeatability.

## **User Type**

5–20 users maximum.

Target:

- product leaders
- researchers
- strategists
- founders
- reflective thinkers

## **Key Metrics**

| **Metric**             | **Target** |
| ---------------------- | ---------- |
| Week 4 retention       | 40%+       |
| Weekly retrieval usage | 50%+       |
| Daily captures         | Stable     |
| Retrieval satisfaction | High       |

## **Most Important Signal**

Users say:

“It remembered something important I forgot.”

---

# **Phase 4 — Retrieval Intelligence**

## **Goal**

Transition from archive → cognitive augmentation.

## **Potential Capabilities**

- contextual resurfacing
- repeated theme detection
- strategic continuity
- unresolved tension tracking
- related memory suggestions

## **Important Warning**

Avoid becoming:

- AI therapist
- pseudo-human companion
- intrusive assistant

Pilot should remain:

- grounded
- calm
- strategically useful

---

# **15. UX Principles**

## **Principle 1 — Capture Must Feel Instant**

Target:

- recording within 1 second

---

## **Principle 2 — Minimal Cognitive Overhead**

Avoid:

- manual tagging
- folder management
- workflow complexity

---

## **Principle 3 — Retrieval Over Filing**

Users should ask naturally.

Not:

- navigate hierarchies
- manage folders
- maintain systems

---

## **Principle 4 — Calm Interface**

Avoid:

- productivity aesthetics
- noisy dashboards
- over-optimisation
- clutter

The interface should feel:

- trustworthy
- quiet
- reflective
- cognitively lightweight

---

# **16. Data & Metadata Philosophy**

Metadata should initially be AI-generated.

Examples:

- themes
- stakeholders
- strategic topics
- organisational tensions
- initiatives
- unresolved questions

Do NOT require heavy manual organisation.

---

# **17. Suggested Initial Repository Structure**

```other
/Pilot
    /mobile-app
    /backend
    /docs
    /prompts
    /architecture
    /experiments
    /weekly-learnings
```

---

# **18. Suggested Obsidian Vault Structure**

```other
/00 Inbox
/01 Vision
/02 Product
/03 Architecture
/04 Research
/05 Experiments
/06 Learnings
/07 Retrieval Philosophy
/08 Prompts
/09 Meetings
/10 Journal
```

Important:

- keep structure shallow initially
- avoid over-engineering the knowledge system

---

# **19. Key Product Risks**

## **Risk 1 — Novelty Collapse**

Many AI tools feel magical briefly.

Need:

- durable retrieval value
- longitudinal usefulness

---

## **Risk 2 — Shallow Summaries**

If outputs feel generic:

- trust collapses quickly.

---

## **Risk 3 — Information Graveyard**

If retrieval fails:

- capture becomes noise.

This is the most critical risk.

---

## **Risk 4 — Overbuilding**

Premature complexity may kill iteration speed.

Avoid:

- large infra
- agent frameworks
- enterprise abstractions
- unnecessary integrations

---

# **20. Key Product Metrics**

## **Behavioural Metrics**

| **Metric**               | **Target** |
| ------------------------ | ---------- |
| Daily captures           | 1+         |
| Weekly retrieval usage   | 50%+       |
| Week 4 retention         | 40%+       |
| Average recording length | 90s+       |

---

## **Quality Metrics**

| **Metric**            | **Target** |
| --------------------- | ---------- |
| Summary usefulness    | 70%+       |
| Retrieval relevance   | 80%+       |
| Transcription quality | 90%+       |

---

# **21. Most Important Long-Term Strategic Insight**

The deeper opportunity may not be:

“better note-taking.”

The deeper opportunity may be:

AI-readable human context systems.

Pilot may eventually evolve toward:

- strategic memory infrastructure
- reflective cognition systems
- contextual continuity layers
- AI-native knowledge augmentation

This should NOT influence MVP scope yet.

---

# **22. Initial Build Priorities**

## **Highest Priority**

1. Fast capture
2. Strong summaries
3. High-quality retrieval
4. Reflection continuity

---

## **Lowest Priority**

- polish
- scale
- integrations
- collaboration
- automation complexity

---

# **23. Operating Principle For Development**

Every phase must answer a specific uncertainty.

Progression should happen only when:

- evidence supports the next step
- behavioural signals are positive
- retrieval demonstrates value

Avoid roadmap theatre.

The goal is:

- rapid learning
- behavioural validation
- product truth discovery

---

# **24. Final Product Definition**

Pilot is:

an AI-assisted reflective memory system designed to preserve and resurface high-value cognition over time.

It aims to reduce cognitive fragmentation and improve continuity of thought for strategic knowledge workers.

The core differentiator is not capture.

The core differentiator is:

meaningful retrieval and longitudinal reflective continuity.
