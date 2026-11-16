# ControlPlane
**Personal Engineering, Learning & Entrepreneurship Workstation**

A local-first, single-user developer control plane engineered for undergraduate computer science/IT students, software developers, and aspiring technical founders.

---

## Architecture Overview
- **Backend:** Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic V2
- **Database:** SQLite 3 with Write-Ahead Logging (WAL) and foreign keys enabled
- **Frontend:** React 18, Vite, Tailwind CSS, Lucide Icons
- **AI Mentoring (Module E):** Google Gemini API (`gemini-2.5-flash`), with 100% offline-first graceful fallback

---

## Quick Start (Windows 11 / PowerShell)

### 1. One-Time Setup
Run the bootstrap script from the repository root:
```powershell
powershell scripts/setup_dev.ps1
```

### 2. Running the Backend Server
```powershell
powershell scripts/run_backend.ps1
```
- API Base: `http://127.0.0.1:8000`
- Interactive OpenAPI Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/v1/system/health`

### 3. Running the Frontend Dashboard
In a second PowerShell terminal:
```powershell
powershell scripts/run_frontend.ps1
```
- Web Application: `http://localhost:5173`

### 4. Running Automated Tests
```powershell
.\.venv\Scripts\pytest -v tests/backend
```

---

## Engineering Roadmap Status
- [x] **Phase 0:** Product Discovery & Architecture (`PRODUCT_REQUIREMENTS.md`, `SYSTEM_ARCHITECTURE.md`)
- [x] **Phase 1:** Application Foundation (FastAPI, SQLite WAL, Alembic, React Vite Layout, Health API, Automated Tests)
- [ ] **Phase 2:** Learning Command Center (Semesters, Subjects, Topic Trees, Focus Stopwatch, Markdown Notes)
- [ ] **Phase 3:** Project Intelligence (Local Project Registry, Tasks, Bug Tracker, ADRs)
- [ ] **Phase 4:** Personal Growth Engine (Top-3 Daily Priorities, Habit Ledger, Weekly Review Generator)
- [ ] **Phase 5:** Business Lab (Opportunity Pipeline, Experiments & Validation Ledger)
- [ ] **Phase 6:** Socratic AI Mentor & Gemini Provider
- [ ] **Phase 7:** Knowledge Retrieval & Search
- [ ] **Phase 8:** Unified Dashboard & Analytics
- [ ] **Phase 9:** System Hardening, Backups & Polish

