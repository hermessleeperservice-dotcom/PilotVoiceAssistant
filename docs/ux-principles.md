# UX Principles

> Per PRD §15: Pilot should feel like calm memory infrastructure, not productivity software.

## Principle 1 — Capture Must Feel Instant

**Target:** Recording starts within 1 second.

### Implementation Rules:
- One tap = record (no confirmation dialogs)
- Visual feedback on press (pulse animation, color change)
- Tap again = stop recording
- Record immediately when the tap starts (no delay)
- If the user taps and releases quickly (<0.5s), ignore it (prevent accidental recordings)
- Background recording should be seamless (minimal visible change)

### What to Avoid:
- Multi-step recording flows
- "Are you sure?" confirmations
- Loading spinners before recording starts
- Audio permission prompts (handle gracefully in advance)

### Visual Design:
- Large, circular record button (centered)
- Color shift: neutral → red (recording) → neutral (stopped)
- Waveform visualization during recording (subtle)
- Timer display during recording

### Success Criteria:
- Average time from screen open to recording = 1 tap
- No user has to think about "how to record"

---

## Principle 2 — Minimal Cognitive Overhead

**Core idea:** Zero manual organization. Everything is automatic.

### Implementation Rules:
- NO manual tagging
- NO folder management
- NO workflow complexity
- NO categorization screens
- AI generates: themes, topics, action items, key ideas, summaries
- User just speaks → everything else happens automatically

### What to Avoid:
- Tag input fields
- Category pickers
- "Organize this" buttons
- File/folder trees
- Metadata editing screens

### Success Criteria:
- User can go from zero to recording in one action
- No screens between recording and stopping

---

## Principle 3 — Retrieval Over Filing

**Core idea:** Users ask naturally. They don't navigate hierarchies.

### Implementation Rules:
- Search interface: single text field (prominent)
- Query like: "What did I say about omnichannel strategy?"
- Results ranked by semantic similarity (not date relevance alone)
- Show related context (themes, action items) with each result
- Timeline as the default view (chronological is the primary navigation)

### What to Avoid:
- Folders or collections
- Manual tag filters
- Category menus
- Date range pickers (as primary navigation)

### Success Criteria:
- User can find something from their reflections without knowing when they said it
- Query understanding feels "right" not "rigid"

---

## Principle 4 — Calm Interface

**Core idea:** Trustworthy, quiet, reflective, cognitively lightweight.

### Visual Design Principles:

#### Color Palette
```
Background: #FAFAFA (warm white)
Surface: #FFFFFF (pure white)
Text Primary: #1A1A1A (near black)
Text Secondary: #6B6B6B (muted gray)
Accent: #4A5568 (cool blue-gray, not bright)
Accent Active: #2D3748 (darker for active states)
Success: #276749 (muted green)
Warning: #975A16 (warm amber)
Error: #C53030 (muted red)
```

#### Typography
```
Headings: SF Pro Display, 17-24pt
Body: SF Pro Text, 15pt
Captions: SF Pro Text, 13pt
Monospace (for technical/notes): SF Mono, 14pt
```

#### Spacing & Layout
- Generous white space (don't fill every corner)
- Minimum 16pt padding on all screens
- Cards with subtle borders (not shadows)
- Line height: 1.5x body text
- Max line length: 40-70 characters (readability)

### Microinteractions:
- Recording: subtle pulse (not flashing)
- Save state: gentle haptic feedback
- Loading: skeleton screen (not spinner)
- Empty state: helpful copy, not generic message

### What to Avoid:
- Bright/Neon colors
- Productivity aesthetics (kanban boards, progress bars, streaks)
- Gamification elements (badges, levels, leaderboards)
- Cluttered layouts
- Notifications for non-critical events
- Over-optimization (always "add more" mentality)

### Tone of Voice:
- Informative, not excited
- Calm, not urgent
- Direct, not fluffy
- Example: "Your reflection was saved." NOT "🎉 Great job summarizing! Keep going! 🚀"

### Success Criteria:
- User describes the experience as "quiet" and "helpful"
- No UI element draws attention away from the content
- Screen feels less crowded than iOS Notes by default
