from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime

class ExperimentBase(BaseModel):
    hypothesis: str
    validation_method: str = "Customer Interviews"
    budget_allocated: float = 0.0
    budget_spent: float = 0.0
    success_criteria: str
    actual_outcome: Optional[str] = None
    decision: str = "In Progress"
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ExperimentCreate(ExperimentBase):
    opportunity_id: int

class ExperimentUpdate(BaseModel):
    hypothesis: Optional[str] = None
    validation_method: Optional[str] = None
    budget_allocated: Optional[float] = None
    budget_spent: Optional[float] = None
    success_criteria: Optional[str] = None
    actual_outcome: Optional[str] = None
    decision: Optional[str] = None
    end_date: Optional[date] = None

class ExperimentResponse(ExperimentBase):
    id: int
    opportunity_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BusinessOpportunityBase(BaseModel):
    title: str
    problem_statement: str
    target_customer: str
    revenue_model: str = "B2B SaaS"
    stage: str = "Ideation"
    estimated_tam: Optional[str] = None
    competitive_advantage: Optional[str] = None

class BusinessOpportunityCreate(BusinessOpportunityBase):
    pass

class BusinessOpportunityUpdate(BaseModel):
    title: Optional[str] = None
    problem_statement: Optional[str] = None
    target_customer: Optional[str] = None
    revenue_model: Optional[str] = None
    stage: Optional[str] = None
    estimated_tam: Optional[str] = None
    competitive_advantage: Optional[str] = None

class BusinessOpportunityResponse(BusinessOpportunityBase):
    id: int
    experiments: List[ExperimentResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

