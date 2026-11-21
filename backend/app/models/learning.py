from datetime import datetime, date, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

class Semester(Base, TimestampMixin):
    __tablename__ = "semesters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False) # e.g. "Semester 5 (Fall 2026)"
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)
    
    subjects = relationship("Subject", back_populates="semester", cascade="all, delete-orphan")

class Subject(Base, TimestampMixin):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(128), nullable=False, index=True)
    code = Column(String(32), nullable=True)
    category = Column(String(64), default="Core Academic", nullable=False)
    difficulty = Column(String(32), default="Medium", nullable=False) # Beginner, Medium, Hard, Advanced
    priority = Column(String(16), default="P1", nullable=False) # P0, P1, P2
    target_completion_date = Column(Date, nullable=True)
    status = Column(String(32), default="Not Started", nullable=False, index=True) # Not Started, Learning, Practicing, Revision Required, Mastered
    
    semester = relationship("Semester", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="subject", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="subject", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="subject", cascade="all, delete-orphan")

class Topic(Base, TimestampMixin):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, default=0, nullable=False)
    status = Column(String(32), default="Not Started", nullable=False) # Not Started, Learning, Practicing, Revision Required, Mastered
    mastery_score = Column(Integer, default=0, nullable=False) # 0 to 100
    
    subject = relationship("Subject", back_populates="topics")
    subtopics = relationship("Subtopic", back_populates="topic", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="topic")
    notes = relationship("Note", back_populates="topic")

class Subtopic(Base):
    __tablename__ = "subtopics"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    topic = relationship("Topic", back_populates="subtopics")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    session_type = Column(String(32), default="Study", nullable=False) # Study, Coding Practice, Revision, Quiz
    notes = Column(Text, nullable=True)
    session_date = Column(Date, default=date.today, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    subject = relationship("Subject", back_populates="study_sessions")
    topic = relationship("Topic", back_populates="study_sessions")

class Note(Base, TimestampMixin):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    content_markdown = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
    
    subject = relationship("Subject", back_populates="notes")
    topic = relationship("Topic", back_populates="notes")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    total_score = Column(Integer, nullable=False)
    score_achieved = Column(Integer, nullable=False)
    evaluation_feedback = Column(Text, nullable=True)
    assessed_by = Column(String(32), default="Self", nullable=False) # Self, AI Mentor, College Exam
    assessment_date = Column(Date, default=date.today, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    subject = relationship("Subject", back_populates="assessments")

