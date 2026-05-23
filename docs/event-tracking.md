# Event Tracking Strategy

> Per PRD Phase 0 deliverable.

## Core Principle

Pilot's success is measured by **behavioral signals**, not functional capability. We track what users do, not what they can do.

## Event Taxonomy

### Capture Events

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `capture_start` | User opens recording interface | timestamp |
| `capture_initiated` | First microphone activation | elapsed_since_open_ms |
| `captured` | User stops recording | duration_ms, total_duration |
| `capture_abandoned` | User closes recording without saving | elapsed_ms (how long they hesitated) |
| `capture_failed` | Audio recording error | error_code |

**Key Insight:** Capture friction directly impacts Phase 1 validation. Every millisecond of delay between intent and recording is lost cognition.

### Transcription Events

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `transcribe_started` | Audio sent to backend | file_size_bytes |
| `transcribe_completed` | Transcript returned | transcription_time_ms, word_count, whisper_model |
| `transcription_quality_low` | Whisper confidence below threshold | confidence_score |

**Key Insight:** Transcription quality drives trust. Low-quality transcriptions = users don't trust the system = they stop using it.

### Summarization Events

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `summarize_started` | Transcript sent to AI | transcript_length |
| `summarize_completed` | Summary returned | summary_length, token_count, model_used |
| `summary_quality_low` | Summary < 3 key ideas or < 50 words | issue_type |

**Key Insight:** Shallow summaries collapse trust. We must track "summary richness" as a quality signal.

### Retrieval Events

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `search_started` | User begins query | query_length, is_timed_query |
| `search_completed` | Results rendered | results_count, query_time_ms, search_type |
| `search_result_viewed` | User opens a reflection from results | reflection_id |
| `search_result_adopted` | User takes action on result (edit, act on, share) | action_type |
| `search_quality_submitted` | User rates retrieval | quality_score (1-10), query |
| `search_reset` | User clears search and starts over | query_length (how far did they get?) |

**Key Insight:** Retrieval is THE core metric. If users can't retrieve what matters, Pilot fails. The "search_reset" event is critical — it means the system failed.

### Timeline Events

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `timeline_viewed` | User opens the timeline | scroll_depth_days (how far back do they scroll?) |
| `timeline_reflection_tapped` | User taps on a timeline item | days_ago, reflection_length |
| `timeline_filter_applied` | User applies a filter | filter_type |
| `timeline_empty` | Timeline has no reflections yet | days_since_first_capture |

**Key Insight:** How far back users scroll tells us if Pilot creates longitudinal value or if thoughts become stale too quickly.

### Behavioral Signals

| Event Name | Trigger | Data Captured |
|--------------|---------|---------------|
| `session_start` | App opens | days_since_last_session |
| `session_end` | App closes | session_duration_ms |
| `daily_streak_updated` | User returns consecutive day | streak_length |
| `weekly_retention` | User active in current week | weeks_active (total) |
| `feature_explored` | User tries unfamiliar UI element | element_id, time_on_page |

### Critical Composite Metrics

These are computed from events, not single events:

1. **Capture Latency** = `capture_initiated` - `capture_start` (target: <1000ms)
2. **Daily Active Users** = unique users with `captured` events per day
3. **Retrieval Success Rate** = `search_result_adopted` / `search_completed` (target: >50%)
4. **Abandonment Rate** = `capture_abandoned` / (`captured` + `capture_abandoned`) (target: <10%)
5. **Longitudinal Depth** = average `scroll_depth_days` on timeline (target: >14 days)
6. **Trust Index** = average `search_quality_submitted` score (target: >7/10)

## Privacy Notice

- All events are tied to user_id only (no PII in events)
- No transcription content is stored in events
- Events are anonymized after 90 days if user is inactive
- Users can export and delete all event data at any time

## Event Schema

```json
{
  "event_id": "<uuid>",
  "user_id": "<uuid>",
  "event_type": "capture_completed",
  "event_data": {
    "duration_ms": 123000,
    "word_count": 284,
    "timestamp": "2026-05-23T14:30:00Z"
  },
  "session_id": "<uuid>",
  "created_at": "2026-05-23T14:30:00Z"
}
```

## Analytics Strategy

### Week-by-Week Milestones

- **Week 1:** Are people capturing at all? (capture volume trend)
- **Week 2:** Are they returning? (retention curve)
- **Week 3:** Are they retrieving? (search volume vs capture volume)
- **Week 4:** Are they staying? (week 4 retention target: 40%+)

### Failure Signals

| Signal | Threshold | Action |
|--------|-----------|--------|
| No captures in 7 days | <5% of DAU | PIVOT capture UX |
| Retention drops by 50% week-over-week | WoW >50% drop | INVESTIGATE immediately |
| Search quality avg <5/10 | <5 | REVIEW retrieval algorithm |
| Timeline never scrolled beyond 3 days | <3 average | CONSIDER: no longitudinal value yet |
| Capture abandoned >30% | >30% | REDUCE capture friction |

### What We DON'T Track (Deliberately)

- Screen views / page views (vanity metric)
- "Time spent in app" (could be confusion, not engagement)
- Feature adoption rates (premature for MVP)
- Export/sharing metrics (not in MVP scope)
- A/B test results (not A/B testing in MVP)

Per PRD Phase 0: **Behavioral validation over vanity metrics.**
