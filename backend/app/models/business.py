from datetime import datetime, date, timezone
from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base
from backend.app.models.base import TimestampMixin

class BusinessOpportunity(Base, TimestampMixin):
    __tablename__ = "business_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    problem_statement = Column(Text, nullable=False)
    target_customer = Column(Text, nullable=False)
    revenue_model = Column(String(64), default="B2B SaaS", nullable=False)
    stage = Column(String(32), default="Ideation", nullable=False, index=True) # Ideation, Validation, Prototype, GTM, Revenue, Archived
    estimated_tam = Column(String(128), nullable=True)
    competitive_advantage = Column(Text, nullable=True)
    
    experiments = relationship("Experiment", back_populates="opportunity", cascade="all, delete-orphan")

class Experiment(Base, TimestampMixin):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("business_opportunities.id", ondelete="CASCADE"), nullable=False, index=True)
    hypothesis = Column(Text, nullable=False)
    validation_method = Column(String(128), default="Customer Interviews", nullable=False) # Cold Outreach, Landing Page, Prototype Testing, Customer Interviews
    budget_allocated = Column(Float, default=0.0, nullable=False)
    budget_spent = Column(Float, default=0.0, nullable=False)
    success_criteria = Column(Text, nullable=False)
    actual_outcome = Column(Text, nullable=True)
    decision = Column(String(32), default="In Progress", nullable=False) # In Progress, Validated, Invalidated, Pivoted
    start_date = Column(Date, default=date.today, nullable=False)
    end_date = Column(Date, nullable=True)
    
    opportunity = relationship("BusinessOpportunity", back_populates="experiments")

