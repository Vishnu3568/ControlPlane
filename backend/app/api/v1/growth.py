from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from backend.app.core.database import get_db
from backend.app.services.growth_service import GrowthService
from backend.app.schemas.growth import (
    DailyReviewCreate, DailyReviewUpdate, DailyReviewResponse,
    HabitCreate, HabitResponse, HabitLogResponse, WeeklyRetrospectiveResponse
)

router = APIRouter(prefix="/growth", tags=["Personal Growth Engine"])

# --- DAILY REVIEWS & PRIORITIES ---
@router.get("/daily/today", response_model=DailyReviewResponse)
def get_today_review(db: Session = Depends(get_db)):
    return GrowthService.get_or_create_today_review(db)

@router.put("/daily/{review_id}", response_model=DailyReviewResponse)
def update_daily_review(review_id: int, data: DailyReviewUpdate, db: Session = Depends(get_db)):
    review = GrowthService.update_daily_review(db, review_id, data)
    if not review:
        raise HTTPException(status_code=404, detail="Daily review not found")
    return review

@router.get("/daily/history", response_model=List[DailyReviewResponse])
def get_review_history(limit: int = 14, db: Session = Depends(get_db)):
    return GrowthService.get_all_reviews(db, limit)

# --- HABITS ---
@router.get("/habits", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    return GrowthService.get_habits(db)

@router.post("/habits", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(data: HabitCreate, db: Session = Depends(get_db)):
    return GrowthService.create_habit(db, data)

@router.post("/habits/{habit_id}/toggle", response_model=HabitLogResponse)
def toggle_habit_log(habit_id: int, target_date: Optional[date] = None, db: Session = Depends(get_db)):
    return GrowthService.toggle_habit_log(db, habit_id, target_date)

# --- RETROSPECTIVE ---
@router.get("/retrospective/weekly", response_model=WeeklyRetrospectiveResponse)
def get_weekly_retrospective(db: Session = Depends(get_db)):
    return GrowthService.generate_weekly_retrospective(db)

