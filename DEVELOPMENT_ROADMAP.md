# DEVELOPMENT ROADMAP — FOUNDER OS
**Methodology:** Incremental Delivery with Automated Testing & Architecture Verification Gate  
**Version:** 1.0.0  

---

## Roadmap Overview & Phases

```
[Phase 0: Discovery & Architecture] ---> [Phase 1: Foundation (Backend + Frontend + DB)]
                                                        |
                                                        v
                                        [Phase 2: Learning Command Center]
                                                        |
                                                        v
                                        [Phase 3: Project Intelligence]
                                                        |
                                                        v
                                        [Phase 4: Personal Growth Engine]
                                                        |
                                                        v
                                        [Phase 5: Business Lab]
                                                        |
                                                        v
                                        [Phase 6: AI Mentor (Gemini API)]
                                                        |
                                                        v
                                        [Phase 7: Knowledge Retrieval & Search]
                                                        |
                                                        v
                                        [Phase 8: Unified Dashboard & Analytics]
                                                        |
                                                        v
                                        [Phase 9: Reliability, Backups & Polish]
```

---

## Phase-by-Phase Breakdown

### Phase 0: Product Discovery & Architecture (CURRENT)
- **Goal:** Comprehensive analysis, elimination of speculative complexity, workspace validation, schema blueprinting, and technical consensus.
- **Deliverables:**
  - `PRODUCT_REQUIREMENTS.md`
  - `SYSTEM_ARCHITECTURE.md`
  - `DATABASE_DESIGN.md`
  - `DEVELOPMENT_ROADMAP.md`
  - `PROJECT_STATE.md`
  - `IMPLEMENTATION_LOG.md`
- **Validation Criteria:** Architecture approved by user before a single line of application code is run.

---

### Phase 1: Application Foundation & Infrastructure
- **Complexity:** Low to Medium | **Dependencies:** None
- **Objectives:**
  1. Initialize Python virtual environment with FastAPI, SQLAlchemy 2.0, Alembic, Pydantic V2, Pytest, Uvicorn.
  2. Configure SQLite with WAL mode, foreign key constraints, and initialize Alembic migrations.
  3. Initialize React + Vite + Tailwind CSS project with modern layout (Collapsible Sidebar, Header, Theme Toggle).
  4. Build health check endpoint (`/api/v1/system/health`) and basic database connection verification.
  5. Provide one-click PowerShell startup scripts (`scripts/run_backend.ps1`, `scripts/run_frontend.ps1`).
- **Verification Gate:**
  - `pytest tests/backend` passes with 100% green.
  - Frontend launches on `http://localhost:5173` and successfully fetches backend health status from `http://127.0.0.1:8000/api/v1/system/health`.

---

### Phase 2: Learning Command Center (Module A)
- **Complexity:** Medium | **Dependencies:** Phase 1
- **Objectives:**
  1. Alembic migration for `semesters`, `subjects`, `topics`, `subtopics`, `study_sessions`, `notes`, `assessments`.
  2. CRUD API endpoints with Pydantic validation:
     - `/api/v1/learning/subjects`
     - `/api/v1/learning/topics`
     - `/api/v1/learning/sessions`
     - `/api/v1/learning/notes`
  3. Interactive UI:
     - Subject Cards with progress rings, difficulty tags, priority badges.
     - Topic tree with 5-state lifecycle toggles (`Not Started` -> `Mastered`).
     - Real-time Study Stopwatch / Pomodoro timer that directly logs focus minutes to `study_sessions`.
     - Markdown note editor with live preview.
- **Verification Gate:**
  - Create a real academic subject (e.g., "Operating Systems" or "Computer Networks"), start a 5-minute study timer, log it, and verify that the session and progress persist after refreshing the browser and restarting the backend.

---

### Phase 3: Project Intelligence (Module B)
- **Complexity:** Medium | **Dependencies:** Phase 1
- **Objectives:**
  1. Alembic migration for `projects`, `project_tasks`, `architecture_decisions`.
  2. Backend endpoints for project registry, task Kanban/list, and ADR logging.
  3. Inspect existing parent directory projects (`Billing 2.0`, `Sentinel-NLP`, `venturebot`) and register them with their real local paths and tech stacks.
  4. Task management UI with status columns (`Todo`, `In Progress`, `In Review`, `Done`) and priority indicators.
  5. Architecture Decision Record (ADR) viewer and editor (Context, Decision, Consequences).
- **Verification Gate:**
  - Local path verification: app checks if the project folder exists on the machine.
  - Adding a task and moving it across columns persists in SQLite with correct timestamping.

---

### Phase 4: Personal Growth Engine (Module C)
- **Complexity:** Low to Medium | **Dependencies:** Phases 2 & 3
- **Objectives:**
  1. Alembic migration for `daily_reviews`, `habits`, `habit_logs`.
  2. Daily Execution View: Top-3 Daily Priorities with instant toggle.
  3. Habit tracking grid with 7-day visual consistency matrix.
  4. Weekly Retrospective Generator: Service logic that aggregates real study hours from Phase 2 + completed project tasks from Phase 3 to generate an honest, evidence-based review.
- **Verification Gate:**
  - Completing priorities updates the daily review ledger. Weekly review accurately computes total logged study hours without mock data.

---

### Phase 5: Business Lab (Module D)
- **Complexity:** Medium | **Dependencies:** Phase 4
- **Objectives:**
  1. Alembic migration for `business_opportunities`, `experiments`.
  2. Opportunity Pipeline Kanban board (Ideation -> Validation -> Prototype -> GTM -> Revenue).
  3. Experiment tracking cards: Hypothesis, validation method, spent budget, success metric, pivot/persevere decision log.
- **Verification Gate:**
  - Register an opportunity (e.g., an AI developer tool or automation service), attach an experiment, and verify state transitions.

---

### Phase 6: AI Mentor & Gemini Integration (Module E)
- **Complexity:** High | **Dependencies:** Phases 2 & 3
- **Objectives:**
  1. Implement `BaseAIProvider` and `GeminiProvider` using `@google/genai` or Python `google-generativeai`.
  2. Context Builder: Assembles selective context (e.g., currently selected subject, recent quiz results, active project tasks) into a strictly token-budgeted prompt.
  3. System Prompt Engineering: "Strict Technical Mentor & Principal Architect" persona.
  4. Chat UI with message history, markdown code highlighting, and graceful offline fallback when no API key or network is present.
- **Verification Gate:**
  - Asking the AI mentor about a specific subject topic yields a response grounded in the user's recorded notes and status.

---

### Phase 7: Knowledge Retrieval & Contextual Search
- **Complexity:** Medium | **Dependencies:** Phase 6
- **Objectives:**
  1. Full-text search across Notes, ADRs, Project tasks, and Learning topics using SQLite `FTS5` or indexed search.
  2. Quick-find Command Palette (`Ctrl+K`) in frontend for rapid keyboard navigation.

---

### Phase 8: Unified Dashboard & Analytics
- **Complexity:** Medium | **Dependencies:** Phases 2, 3, 4, 5
- **Objectives:**
  1. Central Executive Dashboard combining Top-3 today, active learning subject, top project blocker, habit streak, and quick stats.
  2. Real Recharts data visualizations: Hours studied per subject, tasks completed over time, experiment success rate.
  3. Zero mock data rule: Clean, informative empty states when no data is logged yet.

---

### Phase 9: Reliability, Backups & Polish
- **Complexity:** Low to Medium | **Dependencies:** All
- **Objectives:**
  1. One-click SQLite database backup and export to JSON/Zip.
  2. Database restore capability with safety checks.
  3. End-to-end integration smoke tests.
  4. UI polish, accessibility checks, and performance optimization.

