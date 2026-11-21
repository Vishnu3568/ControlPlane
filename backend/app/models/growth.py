from datetime import datetime, date, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

class DailyReview(Base, TimestampMixin):
    __tablename__ = "daily_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    review_date = Column(Date, default=date.today, unique=True, nullable=False, index=True)
    priority_1 = Column(String(255), nullable=False)
    priority_1_done = Column(Boolean, default=False, nullable=False)
    priority_2 = Column(String(255), nullable=True)
    priority_2_done = Column(Boolean, default=False, nullable=False)
    priority_3 = Column(String(255), nullable=True)
    priority_3_done = Column(Boolean, default=False, nullable=False)
    biggest_win = Column(Text, nullable=True)
    biggest_blocker = Column(Text, nullable=True)
    reflection = Column(Text, nullable=True)

class Habit(Base, TimestampMixin):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(64), default="Engineering", nullable=False) # Academics, Coding, Health, Career
    target_days_per_week = Column(Integer, default=7, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date = Column(Date, default=date.today, nullable=False, index=True)
    is_completed = Column(Boolean, default=True, nullable=False)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    habit = relationship("Habit", back_populates="logs")
    __table_args__ = (UniqueConstraint("habit_id", "log_date", name="uq_habit_date"),)

