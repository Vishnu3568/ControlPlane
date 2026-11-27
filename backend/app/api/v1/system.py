from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timezone, date

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.schemas.system import HealthResponse, SettingItem
from backend.app.models.settings import AppSetting
from backend.app.models.learning import Subject, StudySession, Topic
from backend.app.models.project import Project, ProjectTask
from backend.app.models.growth import DailyReview, Habit, HabitLog
from backend.app.models.business import BusinessOpportunity, Experiment

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health", response_model=HealthResponse)
def get_system_health(db: Session = Depends(get_db)):
    """
    Returns system status, database connectivity verification, and offline mode indicator.
    """
    db_connected = False
    try:
        # Quick ping on SQLite engine
        result = db.execute(text("SELECT 1;")).scalar()
        if result == 1:
            db_connected = True
    except Exception as e:
        db_connected = False

    # Check whether Gemini AI key is configured
    offline_mode = bool(not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.strip() == "")

    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database_connected=db_connected,
        offline_mode=offline_mode,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@router.get("/dashboard-summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Returns consolidated live workstation metrics across all modules.
    """
    today = date.today()
    
    # 1. Learning metrics
    subjects_count = db.query(Subject).count()
    study_mins_today = db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))\
        .filter(StudySession.session_date == today).scalar()
    
    # 2. Projects & Tasks
    projects_count = db.query(Project).count()
    tasks_done_count = db.query(ProjectTask).filter(ProjectTask.status == "Done").count()
    tasks_pending_count = db.query(ProjectTask).filter(ProjectTask.status != "Done").count()
    
    # 3. Growth / Priorities
    review = db.query(DailyReview).filter(DailyReview.review_date == today).first()
    priorities_done = 0
    if review:
        priorities_done = sum([review.priority_1_done, review.priority_2_done, review.priority_3_done])
    
    # 4. Business
    opportunities_count = db.query(BusinessOpportunity).count()
    experiments_count = db.query(Experiment).count()
    validated_experiments = db.query(Experiment).filter(Experiment.decision == "Validated").count()

    return {
        "subjects_count": subjects_count,
        "study_mins_today": study_mins_today,
        "projects_count": projects_count,
        "tasks_done_count": tasks_done_count,
        "tasks_pending_count": tasks_pending_count,
        "priorities_done": priorities_done,
        "opportunities_count": opportunities_count,
        "experiments_count": experiments_count,
        "validated_experiments": validated_experiments,
        "today_priority_1": review.priority_1 if review else "Set today's focus in Growth Engine",
        "today_priority_1_done": review.priority_1_done if review else False
    }

@router.get("/settings", response_model=list[SettingItem])
def get_all_settings(db: Session = Depends(get_db)):
    """
    Retrieve application settings.
    """
    return db.query(AppSetting).all()

@router.post("/settings", response_model=SettingItem)
def update_or_create_setting(item: SettingItem, db: Session = Depends(get_db)):
    """
    Update or create an application setting.
    """
    setting = db.query(AppSetting).filter(AppSetting.key == item.key).first()
    if setting:
        setting.value = item.value
        setting.description = item.description
    else:
        setting = AppSetting(key=item.key, value=item.value, description=item.description)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting

