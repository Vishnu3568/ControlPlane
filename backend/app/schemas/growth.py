from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import date, datetime

class DailyReviewBase(BaseModel):
    review_date: date = date.today()
    priority_1: str
    priority_1_done: bool = False
    priority_2: Optional[str] = None
    priority_2_done: bool = False
    priority_3: Optional[str] = None
    priority_3_done: bool = False
    biggest_win: Optional[str] = None
    biggest_blocker: Optional[str] = None
    reflection: Optional[str] = None

class DailyReviewCreate(DailyReviewBase):
    pass

class DailyReviewUpdate(BaseModel):
    priority_1: Optional[str] = None
    priority_1_done: Optional[bool] = None
    priority_2: Optional[str] = None
    priority_2_done: Optional[bool] = None
    priority_3: Optional[str] = None
    priority_3_done: Optional[bool] = None
    biggest_win: Optional[str] = None
    biggest_blocker: Optional[str] = None
    reflection: Optional[str] = None

class DailyReviewResponse(DailyReviewBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class HabitLogBase(BaseModel):
    habit_id: int
    log_date: date = date.today()
    is_completed: bool = True
    notes: Optional[str] = None

class HabitLogResponse(HabitLogBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str = "Engineering"
    target_days_per_week: int = 7
    is_active: bool = True

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int
    recent_logs: List[HabitLogResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class WeeklyRetrospectiveResponse(BaseModel):
    start_date: str
    end_date: str
    total_study_minutes: int
    total_study_hours: float
    study_by_subject: Dict[str, int]
    tasks_completed_count: int
    tasks_completed_list: List[str]
    habits_consistency_pct: float
    summary: str

