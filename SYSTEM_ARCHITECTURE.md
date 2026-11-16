# SYSTEM ARCHITECTURE — FOUNDER OS
**Architecture Style:** Modular Monolith (Local-First Decoupled Client-Server)  
**Version:** 1.0.0  

---

## 1. High-Level Architectural Diagram

```
+--------------------------------------------------------------------------+
|                            USER WORKSTATION                              |
|                                                                          |
|  +--------------------------------------------------------------------+  |
|  |             FRONTEND: React 18 + Vite + Tailwind CSS              |  |
|  |  - Dashboard View   - Learning Module UI    - Project Workspace    |  |
|  |  - Growth / Habits  - Business Kanban       - Socratic AI Chat     |  |
|  |  - State: React Query / Context API         - Visuals: Recharts    |  |
|  +-----------------------------------+--------------------------------+  |
|                                      | HTTP / JSON (Axios)               |
|                                      v                                   |
|  +--------------------------------------------------------------------+  |
|  |                 BACKEND: FastAPI (Python 3.11)                     |  |
|  |                                                                    |  |
|  |  [API Routers] (Thin, Pydantic In/Out Validation)                  |  |
|  |        |                                                           |  |
|  |  [Service Layer] (Business Rules, Aggregations, Evidence Verification|
|  |        |                                \                          |  |
|  |  [Repository Layer] (SQLAlchemy 2.0)     [AI Orchestration Engine] |  |
|  |        |                                      |                    |  |
|  |  [SQLite Engine + WAL Mode]              [Gemini Client Provider]  |  |
|  +--------+--------------------------------------+--------------------+  |
|           |                                      |                       |
|           v                                      v (HTTPS, Optional)     |
|   +---------------+                      +---------------+               |
|   | Local Storage |                      |  Google Cloud |               |
|   | - founder.db  |                      |  Gemini API   |               |
|   | - /data/notes |                      +---------------+               |
|   | - /backups    |                                                      |
|   +---------------+                                                      |
+--------------------------------------------------------------------------+
```

---

## 2. Component Design & Responsibilities

### 2.1 Frontend (Presentation Layer)
- **Framework:** React 19 / 18 + Vite.
- **Styling:** Tailwind CSS with CSS Variables for seamless Dark/Light mode switching.
- **State Management:**
  - Server state caching & synchronization: TanStack Query (React Query) or custom lightweight fetch hooks.
  - UI state (themes, active sidebar, modals): React Context.
- **Component Strategy:** Functional components with strict PropTypes or TypeScript-ready structures. UI primitives modeled for reusability (Card, Modal, Badge, Button, Tabs, DataTable).
- **Visualization:** Recharts for study velocity, weekly task completion, and milestone burn-down.

### 2.2 Backend (Application & Domain Layer)
- **Framework:** FastAPI.
- **Layering Principle:**
  1. `api/`: Route definitions, parameter parsing, dependency injection of DB session, HTTP status codes.
  2. `schemas/`: Pydantic V2 models for input validation, sanitization, and output serialization.
  3. `services/`: Core business logic, cross-module aggregations (e.g., generating weekly review from tasks + study logs), validation rules.
  4. `repositories/`: Pure data access logic, query optimization, handling filters and pagination.
  5. `models/`: SQLAlchemy 2.0 ORM models with explicit column constraints, indices, and foreign keys.
  6. `ai/`: Model-agnostic LLM interface (`BaseAIProvider`), prompt templates, selective context assemblers.

### 2.3 Persistence Layer (Local-First Storage)
- **Engine:** SQLite 3 with Write-Ahead Logging (`PRAGMA journal_mode=WAL;`) enabled for high-concurrency read/write operations without locking the UI.
- **Foreign Keys:** Strictly enforced (`PRAGMA foreign_keys=ON;`).
- **Migrations:** Alembic. Every database schema change is recorded as a versioned migration script (`alembic/versions/`).
- **File System Storage:** Subject attachments, exported JSON/Markdown notes, and database backups are kept in the `data/` directory.

### 2.4 AI Mentoring & Intelligence Layer
- **Provider:** Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`).
- **Architectural Safeguards:**
  - **Provider Pattern:** `ai/providers/base.py` defines an abstract interface. If model providers change (e.g. local Ollama/Llama 3 or Claude), only the provider adapter changes.
  - **Selective Context Retrieval:** Instead of dumping the entire database, the context builder selectively retrieves the specific active subject, recent test results, and active project tasks relevant to the prompt.
  - **Token & Cost Protection:** Strict character/token caps on prompt injection to guarantee low latency and zero budget blowouts.
  - **Graceful Offline Degradation:** If `GEMINI_API_KEY` is missing or network is unavailable, the application functions at 100% capacity for all learning, project, and habit features, showing a clear offline badge in the AI Mentor tab.

---

## 3. Directory Layout

```
FOUNDER-OS/
├── backend/
│   ├── alembic/                      # Database migration scripts
│   │   ├── versions/
│   │   └── env.py
│   ├── app/
│   │   ├── api/                      # REST endpoints
│   │   │   ├── v1/
│   │   │   │   ├── learning.py
│   │   │   │   ├── projects.py
│   │   │   │   ├── growth.py
│   │   │   │   ├── business.py
│   │   │   │   ├── ai_mentor.py
│   │   │   │   └── system.py
│   │   │   └── deps.py               # Dependency injection (DB session, settings)
│   │   ├── core/                     # Application configuration & logging
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/                   # SQLAlchemy ORM entities
│   │   │   ├── base.py
│   │   │   ├── learning.py
│   │   │   ├── project.py
│   │   │   ├── growth.py
│   │   │   └── business.py
│   │   ├── schemas/                  # Pydantic DTOs
│   │   │   ├── learning.py
│   │   │   ├── project.py
│   │   │   ├── growth.py
│   │   │   ├── business.py
│   │   │   └── ai.py
│   │   ├── repositories/             # Data access patterns
│   │   ├── services/                 # Business logic & aggregators
│   │   └── ai/                       # AI orchestration & prompt engineering
│   │       ├── providers/
│   │       │   ├── base.py
│   │       │   └── gemini.py
│   │       └── context_builder.py
│   ├── main.py                       # FastAPI entrypoint
│   ├── requirements.txt
│   └── alembic.ini
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/               # Atomic & composite UI components
│   │   │   ├── common/               # Button, Modal, Card, Badge, Alert
│   │   │   ├── layout/               # Header, Sidebar, Navigation
│   │   │   └── charts/               # Recharts wrappers
│   │   ├── pages/                    # Routed Page Views
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── LearningPage.jsx
│   │   │   ├── ProjectsPage.jsx
│   │   │   ├── GrowthPage.jsx
│   │   │   ├── BusinessPage.jsx
│   │   │   ├── AIMentorPage.jsx
│   │   │   └── SettingsPage.jsx
│   │   ├── services/                 # Axios API clients
│   │   │   ├── api.js
│   │   │   ├── learningService.js
│   │   │   ├── projectService.js
│   │   │   └── growthService.js
│   │   ├── context/                  # ThemeContext, NotificationContext
│   │   ├── hooks/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── data/
│   ├── database/                     # Local SQLite DB location
│   ├── notes/                        # Markdown study & tech notes
│   └── backups/                      # Periodic DB snapshots
│
├── tests/
│   ├── backend/
│   │   ├── test_learning_api.py
│   │   ├── test_project_api.py
│   │   └── test_growth_api.py
│   └── frontend/
│
├── docs/
│   ├── architecture/
│   └── decisions/                    # ADRs (Architecture Decision Records)
│
├── scripts/
│   ├── setup_dev.ps1                 # One-click environment bootstrap
│   ├── run_backend.ps1               # PowerShell startup script
│   ├── run_frontend.ps1
│   └── backup_db.ps1
│
├── .env.example
├── .gitignore
├── README.md
├── PRODUCT_REQUIREMENTS.md
├── SYSTEM_ARCHITECTURE.md
├── DATABASE_DESIGN.md
├── DEVELOPMENT_ROADMAP.md
├── PROJECT_STATE.md
└── IMPLEMENTATION_LOG.md
```

---

## 4. Key Architectural Tradeoffs & Decisions

| Decision | Chosen Solution | Rejected Alternatives | Rational Engineering Justification |
|---|---|---|---|
| **Storage Engine** | SQLite (WAL mode) | PostgreSQL, MongoDB | Single-user local app does not require a running TCP daemon. Zero network hops, zero config, instant backups by copying 1 file. |
| **Backend Framework** | FastAPI (Python 3.11) | Spring Boot, Express/NestJS | Python enables native integration with future local AI/ML pipelines (SentenceTransformers, NumPy, Pandas) without polyglot microservice bloat. |
| **Frontend Framework** | React + Vite | Next.js, Electron | Next.js SSR adds unnecessary Node server complexity for a local app. Standard SPA on Vite has instant HMR and minimal build overhead. |
| **Database Migrations** | Alembic | Manual SQL scripts | Critical for evolving relational schemas across development phases without losing user data or dropping tables. |
| **AI Integration** | Google Gemini API with Provider Pattern | Local 8B Ollama model as mandatory | Running an 8B/14B model locally consumes 8-16GB VRAM, choking IDEs, compilers, and browser tabs on a dev laptop. Gemini API is fast, lightweight, and requires 0 local RAM. |

