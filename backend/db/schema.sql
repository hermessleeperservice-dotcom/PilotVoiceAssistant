-- Pilot Voice Assistant -- PostgreSQL Schema
-- Per PRD: Keep architecture boring initially. Lightweight workers.

-- Enable pgvector extension
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reflections (core of Pilot -- per PRD Section 9)
CREATE TABLE IF NOT EXISTS reflections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    -- Capture
    audio_file_url TEXT,
    duration_ms INTEGER,
    
    -- Transcription
    transcript TEXT,
    transcript_status TEXT DEFAULT 'pending',
    transcription_confidence REAL,
    transcription_error TEXT,
    whisper_model TEXT DEFAULT 'base',
    
    -- AI Synthesis (per PRD Section 9 -- outputs from OpenAI)
    summary TEXT,
    key_ideas TEXT[] DEFAULT '{}',
    action_items TEXT[] DEFAULT '{}',
    themes TEXT[] DEFAULT '{no data}',
    unresolved_tensions TEXT[] DEFAULT '{no data}',
    strategic_observations TEXT[] DEFAULT '{no data}',
    tags TEXT[] DEFAULT ARRAY['no data'],
    
    -- Quality tracking
    summary_quality_score INTEGER,
    
    -- Metadata
    metadata JSONB,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector Embeddings (per PRD Section 9 retrieval)
CREATE TABLE IF NOT EXISTS reflection_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reflection_id UUID REFERENCES reflections(id) ON DELETE CASCADE,
    text_for_embedding TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- HNSW index for fast cosine similarity search
CREATE INDEX IF NOT EXISTS embedding_idx ON reflection_embeddings USING hnsw (embedding vector_cosine_ops);

-- Search History (for behavioral analytics -- per PRD event tracking)
CREATE TABLE IF NOT EXISTS search_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    query_text TEXT NOT NULL,
    results_count INTEGER,
    quality_score INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Events (per event-tracking.md -- behavioral validation)
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id UUID,
    event_type TEXT NOT NULL,
    event_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS reflections_user_id_idx ON reflections(user_id);
CREATE INDEX IF NOT EXISTS reflections_themes_idx ON reflections USING gin(themes);
CREATE INDEX IF NOT EXISTS reflections_key_ideas_idx ON reflections USING gin(key_ideas);
CREATE INDEX IF NOT EXISTS reflections_action_items_idx ON reflections USING gin(action_items);
CREATE INDEX IF NOT EXISTS reflections_created_at_idx ON reflections(created_at DESC);
