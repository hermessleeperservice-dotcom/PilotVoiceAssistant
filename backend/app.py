"""
Pilot Voice Assistant — Backend API

MVP Core: Capture → Transcribe → Summarize → Retrieve
Architecture: FastAPI + SQLite (MVP) + Whisper + OpenAI

Per PRD: Keep architecture boring initially.
"""

from __future__ import annotations

import os
import uuid
import json
import sqlite3
import tempfile
from typing import Optional, List
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Depends
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
DB_PATH = os.getenv("DB_PATH", "pilot.db")


# === Pydantic Models ===

class ReflectionCreate(BaseModel):
    user_id: str
    audio_file_url: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    key_ideas: List[str] = []
    action_items: List[str] = []
    themes: List[str] = []
    unresolved_tensions: List[str] = []
    strategic_observations: List[str] = []
    tags: List[str] = []


class SearchRequest(BaseModel):
    query: str


class ReflectionResponse(BaseModel):
    id: str
    user_id: str
    audio_file_url: Optional[str]
    transcript: Optional[str]
    summary: Optional[str]
    key_ideas: List[str]
    action_items: List[str]
    themes: List[str]
    unresolved_tensions: List[str]
    strategic_observations: List[str]
    tags: List[str]
    created_at: str


class SearchResponse(BaseModel):
    query: str
    results: List[ReflectionResponse]
    total: int


class TimelineResponse(BaseModel):
    reflections: List[ReflectionResponse]
    total: int
    date_groups: dict  # {date_str: count}


class EventLog(BaseModel):
    user_id: str
    event_type: str
    event_data: dict = {}


# === Database ===

def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize the database schema (SQLite MVP per PRD §13)."""
    conn = get_db()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            display_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Reflections (core table — per PRD §9)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reflections (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            audio_file_url TEXT,
            duration_ms INTEGER,
            transcript TEXT,
            transcript_status TEXT DEFAULT 'pending',
            transcription_confidence REAL,
            summary TEXT,
            key_ideas TEXT DEFAULT '[]',
            action_items TEXT DEFAULT '[]',
            themes TEXT DEFAULT '[]',
            unresolved_tensions TEXT DEFAULT '[]',
            strategic_observations TEXT DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            metadata TEXT DEFAULT '{}',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Search history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            query TEXT,
            results_count INTEGER,
            quality_score INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            session_id TEXT,
            event_type TEXT,
            event_data TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# === OpenAI Services ===

async def transcribe_audio(audio_path: str) -> dict:
    """Transcribe audio using Whisper (per PRD §9 Feature 2)."""
    try:
        import whisper
        model = whisper.load_model(WHISPER_MODEL)
        result = model.transcribe(audio_path, fp16=False)
        return {
            "text": result.get("text", ""),
            "confidence": result.get("confidence", 0.0),
            "segments": result.get("segments", []),
            "word_count": len(result.get("text", "").split()),
        }
    except ImportError:
        # Fallback if whisper not installed
        return {
            "text": f"[Transcription placeholder — whisper not installed. Model: {WHISPER_MODEL}]",
            "confidence": 0.0,
            "segments": [],
            "word_count": 0,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


async def summarize_transcript(transcript: str) -> dict:
    """Generate AI summary per PRD §9 Feature 3."""
    if not OPENAI_API_KEY:
        return {
            "summary": f"[Summary placeholder — OpenAI API key not configured]",
            "key_ideas": ["no key ideas"],
            "action_items": ["no action items"],
            "themes": ["no themes"],
            "unresolved_tensions": ["no unresolved tensions"],
            "strategic_observations": ["no observations"],
            "error": "OPENAI_API_KEY not set",
        }

    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are Pilot's AI synthesis engine. Analyze the user's voice reflection and return JSON with:
- summary: a concise, meaningful summary (not generic, not meeting-minutes style)
- key_ideas: list of key ideas the speaker expressed
- action_items: any actionable commitments or next steps
- themes: topic labels (e.g., "strategy", "team dynamics", "product vision")
- unresolved_tensions: any uncertainties, tensions, or unresolved questions
- strategic_observations: any strategic insight worth remembering

Return ONLY valid JSON. No markdown. No explanation."""
                },
                {
                    "role": "user",
                    "content": transcript[:4000]  # Limit length
                }
            ],
            max_tokens=1000,
            temperature=0.3,  # Keep it grounded, not creative
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            parsed = {
                "summary": content[:500],
                "key_ideas": [],
                "action_items": [],
                "themes": [],
                "unresolved_tensions": [],
                "strategic_observations": [],
            }

        # Normalize list fields
        for field in ["key_ideas", "action_items", "themes", "unresolved_tensions", "strategic_observations"]:
            if field in parsed and isinstance(parsed[field], list):
                parsed[field] = [x for x in parsed[field] if x]
            elif field not in parsed:
                parsed[field] = []

        return parsed

    except Exception as e:
        return {
            "summary": f"[Error: {str(e)}]",
            "key_ideas": ["error"],
            "action_items": [],
            "themes": [],
            "unresolved_tensions": [],
            "strategic_observations": [],
        }


def generate_embedding(text: str) -> Optional[List[float]]:
    """Generate OpenAI embedding for retrieval (PRD Feature 4)."""
    if not OPENAI_API_KEY:
        return None

    try:
        import numpy as np
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text,
        )
        return response.data[0].embedding
    except Exception:
        return None


def embed_for_search(text: str) -> Optional[List[float]]:
    """Alias for generate_embedding — used by search flow."""
    return generate_embedding(text)


# === DB Helpers ===

def save_event(conn: sqlite3.Connection, event: EventLog):
    """Log a behavioral event (per event-tracking.md)."""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO events (id, user_id, session_id, event_type, event_data, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), event.user_id, None, event.event_type, json.dumps(event.event_data), datetime.utcnow().isoformat())
    )
    conn.commit()


def save_reflection(conn: sqlite3.Connection, reflection: ReflectionCreate) -> str:
    """Save a reflection to the database."""
    cursor = conn.cursor()
    rid = str(uuid.uuid4())

    cursor.execute(
        """INSERT INTO reflections (id, user_id, audio_file_url, transcript, summary, key_ideas, action_items, themes, unresolved_tensions, strategic_observations, tags, metadata, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""",
        (
            rid,
            reflection.user_id,
            reflection.audio_file_url,
            reflection.transcript,
            reflection.summary,
            json.dumps(reflection.key_ideas),
            json.dumps(reflection.action_items),
            json.dumps(reflection.themes),
            json.dumps(reflection.unresolved_tensions),
            json.dumps(reflection.strategic_observations),
            json.dumps(reflection.tags),
            "{}",  # metadata
        )
    )
    conn.commit()
    return rid


def get_timeline(conn: sqlite3.Connection, user_id: str, page: int = 1, per_page: int = 20) -> dict:
    """Get chronological reflection feed (PRD Feature 5)."""
    cursor = conn.cursor()
    offset = (page - 1) * per_page

    cursor.execute(
        "SELECT * FROM reflections WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (user_id, per_page, offset)
    )
    rows = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) as cnt FROM reflections WHERE user_id = ?",
        (user_id,)
    )
    total = cursor.fetchone()["cnt"]

    # Group by date
    date_groups = {}
    for row in rows:
        date_str = row["created_at"][:10]
        date_groups[date_str] = date_groups.get(date_str, 0) + 1

    reflections = []
    for row in rows:
        reflections.append(ReflectionResponse(
            id=row["id"],
            user_id=row["user_id"],
            audio_file_url=row["audio_file_url"],
            transcript=row["transcript"],
            summary=row["summary"],
            key_ideas=json.loads(row["key_ideas"]) if row["key_ideas"] else [],
            action_items=json.loads(row["action_items"]) if row["action_items"] else [],
            themes=json.loads(row["themes"]) if row["themes"] else [],
            unresolved_tensions=json.loads(row["unresolved_tensions"]) if row["unresolved_tensions"] else [],
            strategic_observations=json.loads(row["strategic_observations"]) if row["strategic_observations"] else [],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            created_at=row["created_at"],
        ))

    return {"reflections": reflections, "total": total, "date_groups": date_groups}


def search_reflections(conn: sqlite3.Connection, user_id: str, query: str) -> List[ReflectionResponse]:
    """Vector-based semantic retrieval (PRD Feature 4)."""
    cursor = conn.cursor()

    # Try embedding-based search first
    embedding = embed_for_search(query)
    if embedding:
        # SQLite doesn't support cosine distance natively, so we use a simple approach
        query_str = " ".join(embedding)
        # For MVP: full-text search as fallback with vector index placeholder
        # In production, use pgvector (PRD §12) with this HNSW index:
        # CREATE INDEX ON reflection_embeddings USING hnsw (embedding vector_cosine_ops);

    # MVP fallback: FTS-like search (works without pgvector)
    cursor.execute(
        """SELECT * FROM reflections
           WHERE user_id = ?
           AND (
               transcript LIKE ? OR
               summary LIKE ? OR
               tags LIKE ? OR
               key_ideas LIKE ? OR
               themes LIKE ?
           )
           ORDER BY created_at DESC
           LIMIT 20""",
        (
            user_id,
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
            f"%{query}%",
        )
    )
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append(ReflectionResponse(
            id=row["id"],
            user_id=row["user_id"],
            audio_file_url=row["audio_file_url"],
            transcript=row["transcript"],
            summary=row["summary"],
            key_ideas=json.loads(row["key_ideas"]) if row["key_ideas"] else [],
            action_items=json.loads(row["action_items"]) if row["action_items"] else [],
            themes=json.loads(row["themes"]) if row["themes"] else [],
            unresolved_tensions=json.loads(row["unresolved_tensions"]) if row["unresolved_tensions"] else [],
            strategic_observations=json.loads(row["strategic_observations"]) if row["strategic_observations"] else [],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            created_at=row["created_at"],
        ))

    # Log search event
    cursor.executemany(
        "INSERT INTO search_history (id, user_id, query, results_count, quality_score, created_at) VALUES (?, ?, ?, ?, NULL, CURRENT_TIMESTAMP)",
        [(str(uuid.uuid4()), user_id, query, len(results))]
    )
    conn.commit()

    return results


def get_reflection(conn: sqlite3.Connection, reflection_id: str, user_id: str) -> Optional[ReflectionResponse]:
    """Get a single reflection."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM reflections WHERE id = ? AND user_id = ?",
        (reflection_id, user_id)
    )
    row = cursor.fetchone()
    if not row:
        return None

    return ReflectionResponse(
        id=row["id"],
        user_id=row["user_id"],
        audio_file_url=row["audio_file_url"],
        transcript=row["transcript"],
        summary=row["summary"],
        key_ideas=json.loads(row["key_ideas"]) if row["key_ideas"] else [],
        action_items=json.loads(row["action_items"]) if row["action_items"] else [],
        themes=json.loads(row["themes"]) if row["themes"] else [],
        unresolved_tensions=json.loads(row["unresolved_tensions"]) if row["unresolved_tensions"] else [],
        strategic_observations=json.loads(row["strategic_observations"]) if row["strategic_observations"] else [],
        tags=json.loads(row["tags"]) if row["tags"] else [],
        created_at=row["created_at"],
    )


# === FastAPI App ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB on startup."""
    init_db()
    yield


app = FastAPI(
    title="Pilot Voice Assistant",
    description="AI-assisted reflective memory system. Capture → Transcribe → Summarize → Retrieve.",
    version="0.1.0",
    lifespan=lifespan,
)


# --- Capture (PRD §9 Feature 1) ---

@app.post("/api/v1/capture")
async def capture_audio(audio: UploadFile = File(...)):
    """
    Feature 1 — Voice Capture (per PRD §9 Feature 1)
    One-tap recording → upload → returns reflection ID
    """
    # Save uploaded audio to temp
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Generate reflection ID
    reflection_id = str(uuid.uuid4())

    save_event(
        get_db(),
        EventLog(
            user_id="anonymous",
            event_type="capture_completed",
            event_data={"file_size": len(content), "filename": audio.filename},
        ),
    )

    return {
        "reflection_id": reflection_id,
        "status": "uploaded",
        "message": "Audio captured. Call /transcribe/{id} to transcribe.",
        "auto_transcribe_hint": True,
    }


# --- Transcribe (PRD §9 Feature 2) ---

@app.post("/api/v1/transcribe/{reflection_id}")
async def transcribe_audio(
    reflection_id: str,
    user_id: str = Query("anonymous"),
    file_path: str = Query(None),
):
    """
    Feature 2 — AI Transcription (per PRD §9 Feature 2)
    Whisper transcription with confidence scoring
    """
    conn = get_db()

    # Find the audio file
    if file_path:
        audio_path = file_path
    else:
        # Look for uploaded audio
        audio_path = None
        import glob
        for f in glob.glob("/tmp/*.mp3"):
            audio_path = f
            break

    if not audio_path:
        return HTTPException(status_code=404, detail="No audio file found for this reflection")

    # Transcribe
    result = await transcribe_audio(audio_path)

    # Save to DB
    save_event(conn, EventLog(user_id=user_id, event_type="transcribe_completed", event_data=result))

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE reflections SET transcript = ?, transcript_status = ?, transcription_confidence = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (result["text"], "success", result["confidence"], reflection_id),
    )
    conn.commit()

    # Auto-summarize if transcription successful
    if result["confidence"] > 0.5 and result["text"]:
        summary = await summarize_transcript(result["text"])
        cursor.execute(
            "UPDATE reflections SET summary = ?, key_ideas = ?, action_items = ?, themes = ?, unresolved_tensions = ?, strategic_observations = ?, tags = ?, transcript_status = 'completed' WHERE id = ?",
            (
                json.dumps(summary["summary"]),
                json.dumps(summary.get("key_ideas", ["no key ideas"])),
                json.dumps(summary.get("action_items", ["no action items"])),
                json.dumps(summary.get("themes", ["no themes"])),
                json.dumps(summary.get("unresolved_tensions", ["no unresolved tensions"])),
                json.dumps(summary.get("strategic_observations", ["no observations"])),
                json.dumps(list(set(
                    [t for t in summary.get("themes", [])] +
                    [t for t in summary.get("strategic_observations", [])] +
                    ["auto-generated"]
                ))),
                reflection_id,
            ),
        )
        conn.commit()

        return {
            "reflection_id": reflection_id,
            "transcript": result["text"],
            "confidence": result["confidence"],
            "word_count": result["word_count"],
            "summary": summary["summary"],
            "key_ideas": summary.get("key_ideas", []),
            "action_items": summary.get("action_items", []),
            "themes": summary.get("themes", []),
            "unresolved_tensions": summary.get("unresolved_tensions", []),
            "strategic_observations": summary.get("strategic_observations", []),
            "transcription_completed": True,
            "summary_completed": True,
            "status": "ready",
            "next_steps": ["Call /retrieve to search", "Timeline: GET /api/v1/timeline"],
        }

    return {
        "reflection_id": reflection_id,
        "transcript": result["text"],
        "confidence": result["confidence"],
        "status": "transcribed_no_summary",
        "message": "Low confidence — summary skipped. Review transcript manually.",
    }


# --- Summarize (PRD §9 Feature 3) ---

@app.post("/api/v1/summarize/{reflection_id}")
async def manually_summarize(reflection_id: str):
    """
    Feature 3 — AI Synthesis (per PRD §9 Feature 3)
    Manual summarization trigger for already-transcribed reflections
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reflections WHERE id = ?", (reflection_id,))
    row = cursor.fetchone()
    if not row:
        return HTTPException(status_code=404, detail="Reflection not found")

    if not row["transcript"]:
        return HTTPException(status_code=400, detail="No transcript to summarize. Transcribe first.")

    summary = await summarize_transcript(row["transcript"])

    cursor.execute(
        "UPDATE reflections SET summary = ?, key_ideas = ?, action_items = ?, themes = ?, unresolved_tensions = ?, strategic_observations = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (
            json.dumps(summary["summary"]),
            json.dumps(summary.get("key_ideas", [])),
            json.dumps(summary.get("action_items", [])),
            json.dumps(summary.get("themes", [])),
            json.dumps(summary.get("unresolved_tensions", [])),
            json.dumps(summary.get("strategic_observations", [])),
            reflection_id,
        ),
    )
    conn.commit()

    save_event(conn, EventLog(user_id="anonymous", event_type="summarize_completed", event_data={"reflection_id": reflection_id}))

    return {
        "reflection_id": reflection_id,
        "summary": summary["summary"],
        "key_ideas": summary.get("key_ideas", []),
        "action_items": summary.get("action_items", []),
        "themes": summary.get("themes", []),
        "unresolved_tensions": summary.get("unresolved_tensions", []),
        "strategic_observations": summary.get("strategic_observations", []),
    }


# --- Retrieve (PRD §9 Feature 4) ---

@app.post("/api/v1/retrieve")
async def retrieve(query_data: SearchRequest, user_id: str = Query("anonymous")):
    """
    Feature 4 — Retrieval (per PRD §9 Feature 4)
    Natural language search with embeddings
    """
    conn = get_db()

    # Log search start
    save_event(conn, EventLog(user_id=user_id, event_type="search_started", event_data={"query": query_data.query}))

    results = search_reflections(conn, user_id, query_data.query)

    # Log search complete
    save_event(conn, EventLog(user_id=user_id, event_type="search_completed", event_data={"results": len(results)}))

    return SearchResponse(
        query=query_data.query,
        results=results,
        total=len(results),
    )


# --- Timeline (PRD §9 Feature 5) ---

@app.get("/api/v1/timeline")
async def get_timeline_endpoint(
    user_id: str = Query("anonymous"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
):
    """
    Feature 5 — Reflective Timeline (per PRD §9 Feature 5)
    Chronological memory feed
    """
    conn = get_db()

    timeline = get_timeline(conn, user_id, page, per_page)

    save_event(conn, EventLog(
        user_id=user_id,
        event_type="timeline_viewed",
        event_data={"page": page, "total": timeline["total"], "per_page": per_page},
    ))

    return timeline


# --- Individual Reflection ---

@app.get("/api/v1/reflections/{reflection_id}")
async def get_reflection_endpoint(reflection_id: str, user_id: str = Query("anonymous")):
    """Get a single reflection by ID."""
    conn = get_db()
    reflection = get_reflection(conn, reflection_id, user_id)
    if not reflection:
        return HTTPException(status_code=404, detail="Reflection not found")
    return reflection


# --- Health & Status ---

@app.get("/api/v1/health")
async def health_check():
    return {
        "service": "Pilot Voice Assistant",
        "status": "running",
        "version": "0.1.0",
        "openai_configured": bool(OPENAI_API_KEY),
        "db": "initialized",
    }


# --- Database Management ---

@app.post("/api/v1/db/init")
async def db_init():
    """Initialize DB (POST, not auto-triggered in prod)."""
    init_db()
    return {"status": "db_initialized"}
