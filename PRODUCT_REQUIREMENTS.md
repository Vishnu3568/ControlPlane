# PRODUCT REQUIREMENTS DOCUMENT (PRD) — FOUNDER OS
**Document Version:** 1.0.0  
**Status:** Under Architectural Review  
**Target User:** Nitish (BTech IT Student, Software Engineer, Aspiring Tech Founder)  
**Deployment Target:** Local Windows 11 Desktop  

---

## 1. Executive Summary & Product Vision
FOUNDER OS is an offline-first, single-user Personal Engineering, Learning, and Entrepreneurship Operating System. Its core mission is to replace fragmented tools (Notion, spreadsheets, ad-hoc sticky notes, scattered markdown files) with a unified, high-performance system of record and execution engine that supports:
$$\text{LEARN} \longrightarrow \text{PRACTICE} \longrightarrow \text{BUILD} \longrightarrow \text{SHIP} \longrightarrow \text{VALIDATE} \longrightarrow \text{GROW}$$

The application runs entirely on the user's local machine, stores data in an explicit, version-controlled SQLite database, provides selective AI mentoring via Google Gemini API, and enforces evidence-based progress rather than vanity metrics.

---

## 2. User Persona & Context
- **Role:** BTech Information Technology undergraduate (MLRIT, graduating 2027).
- **Aspirations:** SDE / Full-Stack / AI Engineer -> Independent Product Builder & Tech Entrepreneur.
- **Current Stack:** Java/Spring Boot, Python/FastAPI, React, SQL/PostgreSQL/MongoDB, Git, Docker.
- **Active Projects in Workspace Parent Directory:**
  - `Billing 2.0` (FastAPI + MongoDB + React ERP)
  - `Sentinel-NLP` (NLP-based spam classification and feature engineering)
  - `venturebot` (Business opportunity evaluation)
  - `ExpenseIQ`, `SkillMatrix`, etc.

---

## 3. Scope Definition & Module Boundaries

### In Scope (Core Modules)
1. **Module A — Learning Command Center:**
   - Academic syllabus hierarchy: Semester -> Subject -> Topic -> Subtopic.
   - Mastery states: `Not Started` | `Learning` | `Practicing` | `Revision Required` | `Mastered`.
   - Study focus sessions & active time tracker.
   - Subject notes & technical documentation (Markdown).
   - Knowledge assessments & quiz outcome logging.

2. **Module B — Project Intelligence:**
   - Project registry pointing to local repositories.
   - Architecture Decision Records (ADRs) & tech stack profiles.
   - Milestones, features, task breakdown, and bug logging.
   - Portfolio readiness tracking & technical retrospective logs.

3. **Module C — Personal Growth Engine:**
   - Daily Top-3 execution priorities.
   - Weekly planning & retrospective review (planned vs actual, blockers).
   - Habit tracking with verifiable completion criteria.

4. **Module D — Business Lab (Phase 5):**
   - Business idea pipeline (Hypothesis -> Market Research -> Validation -> Build -> Launch).
   - Structured experiment tracking (Hypotheses, validation budget, metrics, kill/pivot/scale decisions).
   - Unit economics & basic cashflow log (P&L for bootstrapped ventures).

5. **Module E — AI Mentor & Knowledge Intelligence (Phase 6–7):**
   - Contextual AI Assistant using Google Gemini API.
   - Grounded strictly in local database entities (subjects, project ADRs, study notes, past blockers).
   - Socratic, strict mentoring persona (questions assumptions, forces problem solving, flags repeated mistakes).

6. **Unified Central Dashboard:**
   - Daily briefing, high-priority tasks, learning velocity, project health, habit streak, weekly review summary.

### Out of Scope (Explicit Anti-Goals & Eliminated Bloat)
- **No SaaS Multi-Tenancy:** No organization models, no team permissions, no row-level tenant security.
- **No Heavy Vector DB Infrastructure:** No heavy background vector daemons (Pinecone, Milvus, Chroma) running as memory hogs. RAG will leverage structured relational queries and lightweight SQLite full-text search (`FTS5`) or compact selective JSON context.
- **No Complex Cloud Auth:** No OAuth2/Auth0/Firebase cloud dependencies for local access. Local security is handled at the OS file boundary.
- **No Automated Repository Mutation:** The system will never commit, push, or execute arbitrary code in user project repositories without explicit user action and approval.
- **No Faked Metrics or Gamified XP:** No artificial levels, points, or fabricated streaks. Metrics reflect real logged hours, verified commits, and submitted assessments.

---

## 4. Functional Requirements Matrix

| ID | Feature | Priority | Phase | Dependency |
|---|---|---|---|---|
| **REQ-CORE-01** | Local SQLite storage with Alembic migration system | P0 | 1 | None |
| **REQ-CORE-02** | FastAPI REST API layer with Pydantic request/response validation | P0 | 1 | REQ-CORE-01 |
| **REQ-CORE-03** | React + Vite + Tailwind dashboard with Dark/Light mode | P0 | 1 | REQ-CORE-02 |
| **REQ-LEARN-01** | Subject, Topic, Subtopic CRUD with status lifecycle | P0 | 2 | REQ-CORE-03 |
| **REQ-LEARN-02** | Focus study session stopwatch/timer logging actual time | P0 | 2 | REQ-LEARN-01 |
| **REQ-LEARN-03** | Markdown subject notes with local file attachment | P1 | 2 | REQ-LEARN-01 |
| **REQ-PROJ-01** | Project registry with local path verification & tech stack tags | P0 | 3 | REQ-CORE-03 |
| **REQ-PROJ-02** | Feature, Task, and Bug tracker linked to projects | P0 | 3 | REQ-PROJ-01 |
| **REQ-PROJ-03** | Architecture Decision Record (ADR) documentation tool | P1 | 3 | REQ-PROJ-01 |
| **REQ-GROW-01** | Daily Top-3 priority planner & completion ledger | P0 | 4 | REQ-PROJ-02, REQ-LEARN-01 |
| **REQ-GROW-02** | Weekly retrospective generator (planned vs completed, study hours) | P1 | 4 | REQ-GROW-01 |
| **REQ-BIZ-01** | Business idea & experiment lifecycle Kanban | P1 | 5 | REQ-GROW-01 |
| **REQ-AI-01** | Gemini API provider abstraction with selective context packing | P1 | 6 | REQ-CORE-02 |
| **REQ-AI-02** | Socratic Mentor Chat with context injection from Learning/Projects | P1 | 6 | REQ-AI-01 |
| **REQ-INT-01** | Read-only local Git inspector (branch, recent commits) | P2 | 7 | REQ-PROJ-01 |
| **REQ-SYS-01** | Database one-click backup (SQL dump/archive) & restore | P0 | 8 | REQ-CORE-01 |

---

## 5. Non-Functional Requirements
- **Performance:** Local API response latency $< 50\text{ ms}$ for all CRUD endpoints; initial UI load $< 300\text{ ms}$.
- **Reliability:** 100% operational offline (except AI Mentor queries which require internet connection and fail gracefully with clear offline notices).
- **Data Integrity:** ACID-compliant relational transactions with foreign key enforcement enabled in SQLite (`PRAGMA foreign_keys = ON;`).
- **Maintainability:** Modular monolithic architecture with explicit separation: Route -> Service -> Repository -> Database Model.
- **Security:** API keys (Gemini) stored solely in server-side `.env`, never bundled into client-side JS bundles.

