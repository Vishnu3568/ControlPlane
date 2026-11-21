from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False, unique=True, index=True)
    slug = Column(String(64), nullable=False, unique=True, index=True)
    tagline = Column(String(255), nullable=True)
    problem_statement = Column(Text, nullable=True)
    local_path = Column(String(512), nullable=True) # e.g. "E:\Project Folder\Billing 2.0"
    repository_url = Column(String(512), nullable=True)
    tech_stack_json = Column(Text, default="[]", nullable=False) # JSON list e.g. '["FastAPI", "React", "MongoDB"]'
    status = Column(String(32), default="Active", nullable=False, index=True) # Idea, Planning, Active, Shipped, Maintenance, Archived
    portfolio_ready = Column(Boolean, default=False, nullable=False)
    
    tasks = relationship("ProjectTask", back_populates="project", cascade="all, delete-orphan")
    architecture_decisions = relationship("ArchitectureDecision", back_populates="project", cascade="all, delete-orphan")

class ProjectTask(Base, TimestampMixin):
    __tablename__ = "project_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(32), default="Feature", nullable=False) # Feature, Bug, Refactor, Chore, Doc
    priority = Column(String(16), default="Medium", nullable=False) # Low, Medium, High, Critical
    status = Column(String(32), default="Todo", nullable=False, index=True) # Todo, In Progress, In Review, Done
    estimated_hours = Column(Float, default=1.0, nullable=True)
    actual_hours = Column(Float, default=0.0, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    project = relationship("Project", back_populates="tasks")

class ArchitectureDecision(Base):
    __tablename__ = "architecture_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    adr_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(String(32), default="Accepted", nullable=False) # Proposed, Accepted, Superseded, Rejected
    context = Column(Text, nullable=False)
    decision = Column(Text, nullable=False)
    consequences = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    project = relationship("Project", back_populates="architecture_decisions")

