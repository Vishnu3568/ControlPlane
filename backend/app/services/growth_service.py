from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta, datetime, timezone
from typing import List, Optional

from backend.app.models.growth import DailyReview, Habit, HabitLog
from backend.app.models.learning import StudySession, Subject
from backend.app.models.project import ProjectTask
from backend.app.schemas.growth import DailyReviewCreate, DailyReviewUpdate, HabitCreate, WeeklyRetrospectiveResponse

class GrowthService:
    @staticmethod
    def get_or_create_today_review(db: Session) -> DailyReview:
        today = date.today()
        review = db.query(DailyReview).filter(DailyReview.review_date == today).first()
        if not review:
            review = DailyReview(
                review_date=today,
                priority_1="Set your primary focus for today",
                priority_1_done=False
            )
            db.add(review)
            db.commit()
            db.refresh(review)
        return review

    @staticmethod
    def update_daily_review(db: Session, review_id: int, data: DailyReviewUpdate) -> Optional[DailyReview]:
        review = db.query(DailyReview).filter(DailyReview.id == review_id).first()
        if not review:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(review, key, val)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def get_all_reviews(db: Session, limit: int = 14) -> List[DailyReview]:
        return db.query(DailyReview).order_by(DailyReview.review_date.desc()).limit(limit).all()

    @staticmethod
    def get_habits(db: Session) -> List[Habit]:
        habits = db.query(Habit).filter(Habit.is_active == True).all()
        # Attach recent 7 days of logs to each habit
        seven_days_ago = date.today() - timedelta(days=7)
        for h in habits:
            h.recent_logs = db.query(HabitLog)\
                .filter(HabitLog.habit_id == h.id, HabitLog.log_date >= seven_days_ago)\
                .order_by(HabitLog.log_date.asc()).all()
        return habits

    @staticmethod
    def create_habit(db: Session, data: HabitCreate) -> Habit:
        habit = Habit(**data.model_dump())
        db.add(habit)
        db.commit()
        db.refresh(habit)
        habit.recent_logs = []
        return habit

    @staticmethod
    def toggle_habit_log(db: Session, habit_id: int, target_date: Optional[date] = None) -> HabitLog:
        if not target_date:
            target_date = date.today()
        log = db.query(HabitLog).filter(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date == target_date
        ).first()

        if log:
            log.is_completed = not log.is_completed
        else:
            log = HabitLog(habit_id=habit_id, log_date=target_date, is_completed=True)
            db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def generate_weekly_retrospective(db: Session) -> WeeklyRetrospectiveResponse:
        end_date = date.today()
        start_date = end_date - timedelta(days=7)

        # 1. Total real study minutes & breakdown
        sessions = db.query(StudySession, Subject.name)\
            .join(Subject, StudySession.subject_id == Subject.id)\
            .filter(StudySession.session_date >= start_date, StudySession.session_date <= end_date).all()

        total_mins = sum(s[0].duration_minutes for s in sessions)
        subject_breakdown = {}
        for s, name in sessions:
            subject_breakdown[name] = subject_breakdown.get(name, 0) + s.duration_minutes

        # 2. Tasks completed in project intelligence
        completed_tasks = db.query(ProjectTask)\
            .filter(ProjectTask.status == "Done")\
            .filter(ProjectTask.completed_at >= datetime.combine(start_date, datetime.min.time()))\
            .all()

        task_titles = [t.title for t in completed_tasks]

        # 3. Habit consistency
        total_habits = db.query(Habit).filter(Habit.is_active == True).count()
        total_logs = db.query(HabitLog)\
            .filter(HabitLog.log_date >= start_date, HabitLog.is_completed == True).count()
        
        expected_habit_slots = max(1, total_habits * 7)
        consistency_pct = round((total_logs / expected_habit_slots) * 100, 1)

        summary_text = (
            f"Weekly Performance: {round(total_mins / 60, 1)} hours studied across {len(subject_breakdown)} subjects. "
            f"{len(task_titles)} engineering tasks shipped. Habit consistency score: {consistency_pct}%."
        )

        return WeeklyRetrospectiveResponse(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            total_study_minutes=total_mins,
            total_study_hours=round(total_mins / 60.0, 2),
            study_by_subject=subject_breakdown,
            tasks_completed_count=len(task_titles),
            tasks_completed_list=task_titles,
            habits_consistency_pct=consistency_pct,
            summary=summary_text
        )

