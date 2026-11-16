# DATABASE DESIGN & SCHEMA SPECIFICATION — FOUNDER OS
**Engine:** SQLite 3 (with `PRAGMA foreign_keys = ON;` and `PRAGMA journal_mode = WAL;`)  
**ORM:** SQLAlchemy 2.0  
**Migration Tool:** Alembic  
**Version:** 1.0.0  

---

## 1. Schema Phasing Strategy

To avoid premature schema bloating and maintain high architectural discipline, database tables are phased incrementally:
- **Phase 1 (Foundation):** `app_settings`, `system_health_logs`
- **Phase 2 (Learning Command Center):** `semesters`, `subjects`, `topics`, `subtopics`, `study_sessions`, `notes`, `assessments`
- **Phase 3 (Project Intelligence):** `projects`, `project_features`, `project_tasks`, `project_bugs`, `architecture_decisions`
- **Phase 4 (Personal Growth Engine):** `goals`, `habits`, `habit_logs`, `daily_reviews`, `weekly_reviews`
- **Phase 5 (Business Lab):** `business_opportunities`, `experiments`, `business_transactions`
- **Phase 6 (AI & Knowledge Intelligence):** `ai_conversations`, `ai_messages`, `knowledge_snippets`

---

## 2. Entity-Relationship Model (Relational Specification)

### 2.1 Core & Settings (Phase 1)
```sql
CREATE TABLE app_settings (
    key VARCHAR(64) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 2.2 Learning Command Center (Phase 2)
```sql
CREATE TABLE semesters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL, -- e.g. "Semester 5 (Fall 2026)"
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester_id INTEGER REFERENCES semesters(id) ON DELETE SET NULL,
    name VARCHAR(128) NOT NULL, -- e.g. "Operating Systems", "Distributed Systems"
    code VARCHAR(32),           -- e.g. "CS502"
    category VARCHAR(64) DEFAULT 'Core Academic' NOT NULL, -- 'Core Academic', 'Engineering Fundamental', 'AI/ML'
    difficulty VARCHAR(32) DEFAULT 'Medium', -- 'Beginner', 'Medium', 'Hard', 'Advanced'
    priority VARCHAR(16) DEFAULT 'P1',     -- 'P0', 'P1', 'P2'
    target_completion_date DATE,
    status VARCHAR(32) DEFAULT 'Not Started' NOT NULL, -- 'Not Started', 'Learning', 'Practicing', 'Revision Required', 'Mastered'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_subjects_status ON subjects(status);
CREATE INDEX idx_subjects_semester ON subjects(semester_id);

CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    order_index INTEGER DEFAULT 0 NOT NULL,
    status VARCHAR(32) DEFAULT 'Not Started' NOT NULL, -- 'Not Started', 'Learning', 'Practicing', 'Revision Required', 'Mastered'
    mastery_score INTEGER DEFAULT 0, -- 0 to 100 based on assessments
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_topics_subject ON topics(subject_id);

CREATE TABLE subtopics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    is_completed BOOLEAN DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,
    duration_minutes INTEGER NOT NULL,
    session_type VARCHAR(32) DEFAULT 'Study' NOT NULL, -- 'Study', 'Coding Practice', 'Revision', 'Quiz'
    notes TEXT,
    session_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_study_sessions_date ON study_sessions(session_date);
CREATE INDEX idx_study_sessions_subject ON study_sessions(subject_id);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER REFERENCES subjects(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    content_markdown TEXT NOT NULL,
    tags VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    total_score INTEGER NOT NULL,
    score_achieved INTEGER NOT NULL,
    evaluation_feedback TEXT,
    assessed_by VARCHAR(32) DEFAULT 'Self' NOT NULL, -- 'Self', 'AI Mentor', 'College Exam'
    assessment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 2.3 Project Intelligence (Phase 3)
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL UNIQUE,       -- e.g. "Sentinel-NLP", "Billing 2.0"
    slug VARCHAR(64) NOT NULL UNIQUE,
    tagline VARCHAR(255),
    problem_statement TEXT,
    local_path VARCHAR(512),                 -- e.g. "E:\Project Folder\Billing 2.0"
    repository_url VARCHAR(512),
    tech_stack_json TEXT,                    -- JSON array of tech badges e.g. ["FastAPI", "MongoDB", "React"]
    status VARCHAR(32) DEFAULT 'Active' NOT NULL, -- 'Idea', 'Planning', 'Active', 'Shipped', 'Maintenance', 'Archived'
    portfolio_ready BOOLEAN DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE project_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    task_type VARCHAR(32) DEFAULT 'Feature' NOT NULL, -- 'Feature', 'Bug', 'Refactor', 'Chore', 'Doc'
    priority VARCHAR(16) DEFAULT 'Medium' NOT NULL,   -- 'Low', 'Medium', 'High', 'Critical'
    status VARCHAR(32) DEFAULT 'Todo' NOT NULL,       -- 'Todo', 'In Progress', 'In Review', 'Done'
    estimated_hours REAL,
    actual_hours REAL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_project_tasks_status ON project_tasks(status);
CREATE INDEX idx_project_tasks_project ON project_tasks(project_id);

CREATE TABLE architecture_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    adr_number INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(32) DEFAULT 'Accepted' NOT NULL, -- 'Proposed', 'Accepted', 'Superseded', 'Rejected'
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    consequences TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(project_id, adr_number)
);
```

### 2.4 Personal Growth Engine (Phase 4)
```sql
CREATE TABLE daily_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    review_date DATE NOT NULL UNIQUE,
    priority_1 VARCHAR(255) NOT NULL,
    priority_1_done BOOLEAN DEFAULT 0 NOT NULL,
    priority_2 VARCHAR(255),
    priority_2_done BOOLEAN DEFAULT 0 NOT NULL,
    priority_3 VARCHAR(255),
    priority_3_done BOOLEAN DEFAULT 0 NOT NULL,
    biggest_win TEXT,
    biggest_blocker TEXT,
    reflection TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(128) NOT NULL,
    description TEXT,
    category VARCHAR(64) DEFAULT 'Engineering' NOT NULL, -- 'Academics', 'Coding', 'Health', 'Career'
    target_days_per_week INTEGER DEFAULT 7 NOT NULL,
    is_active BOOLEAN DEFAULT 1 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
    log_date DATE NOT NULL,
    is_completed BOOLEAN DEFAULT 1 NOT NULL,
    notes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE(habit_id, log_date)
);
```

### 2.5 Business Lab (Phase 5)
```sql
CREATE TABLE business_opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    problem_statement TEXT NOT NULL,
    target_customer TEXT NOT NULL,
    revenue_model VARCHAR(64) DEFAULT 'B2B SaaS',
    stage VARCHAR(32) DEFAULT 'Ideation' NOT NULL, -- 'Ideation', 'Validation', 'Prototype', 'GTM', 'Revenue', 'Killed'
    estimated_tam TEXT,
    competitive_advantage TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL REFERENCES business_opportunities(id) ON DELETE CASCADE,
    hypothesis TEXT NOT NULL,
    validation_method TEXT NOT NULL, -- 'Cold Outreach', 'Landing Page', 'Prototype Testing', 'Customer Interviews'
    budget_allocated REAL DEFAULT 0.0,
    budget_spent REAL DEFAULT 0.0,
    success_criteria TEXT NOT NULL,
    actual_outcome TEXT,
    decision VARCHAR(32) DEFAULT 'In Progress' NOT NULL, -- 'In Progress', 'Validated', 'Invalidated', 'Pivoted'
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

### 2.6 AI Mentor & Conversations (Phase 6)
```sql
CREATE TABLE ai_conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    context_type VARCHAR(64) DEFAULT 'General Mentor', -- 'Subject Tutor', 'Project Architecture Review', 'Business Evaluator'
    subject_id INTEGER REFERENCES subjects(id) ON DELETE SET NULL,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE ai_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL REFERENCES ai_conversations(id) ON DELETE CASCADE,
    role VARCHAR(16) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

---

## 3. Data Integrity & Indexing Rules
1. **Foreign Key Enforcement:** SQLite defaults to ignoring foreign keys unless explicitly turned on. Every database session must issue `PRAGMA foreign_keys = ON;`.
2. **Timestamps:** Standard ISO-8601 UTC timestamps stored in `TIMESTAMP` / `TEXT`.
3. **No Phantom Deletions:** Critical entities (`subjects`, `projects`, `opportunities`) use CASCADE deletion only on strictly owned child entities (`topics`, `tasks`, `experiments`), while keeping notes or reviews intact or disassociated (`ON DELETE SET NULL`).

