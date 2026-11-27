from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.api.v1.system import router as system_router
from backend.app.api.v1.learning import router as learning_router
from backend.app.api.v1.projects import router as projects_router
from backend.app.api.v1.growth import router as growth_router
from backend.app.api.v1.business import router as business_router
from backend.app.api.v1.ai import router as ai_router
from backend.app.models.settings import AppSetting
from backend.app.models.learning import Semester, Subject, Topic, Subtopic, StudySession, Note, Assessment
from backend.app.models.project import Project, ProjectTask, ArchitectureDecision
from backend.app.models.growth import DailyReview, Habit, HabitLog
from backend.app.models.business import BusinessOpportunity, Experiment
from backend.app.models.ai import AIConversation, AIMessage

# Ensure tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="ControlPlane - Personal Engineering, Learning & Entrepreneurship Control Plane",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(system_router, prefix=settings.API_V1_STR)
app.include_router(learning_router, prefix=settings.API_V1_STR)
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(growth_router, prefix=settings.API_V1_STR)
app.include_router(business_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "ControlPlane Core Engine is Running",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/system/health"
    }
