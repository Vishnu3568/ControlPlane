from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ArchitectureDecisionBase(BaseModel):
    adr_number: int
    title: str
    status: str = "Accepted"
    context: str
    decision: str
    consequences: str

class ArchitectureDecisionCreate(ArchitectureDecisionBase):
    project_id: int

class ArchitectureDecisionResponse(ArchitectureDecisionBase):
    id: int
    project_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    task_type: str = "Feature"
    priority: str = "Medium"
    status: str = "Todo"
    estimated_hours: Optional[float] = 1.0
    actual_hours: Optional[float] = 0.0

class ProjectTaskCreate(ProjectTaskBase):
    project_id: int

class ProjectTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    task_type: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None

class ProjectTaskResponse(ProjectTaskBase):
    id: int
    project_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    name: str
    slug: str
    tagline: Optional[str] = None
    problem_statement: Optional[str] = None
    local_path: Optional[str] = None
    repository_url: Optional[str] = None
    tech_stack_json: str = "[]"
    status: str = "Active"
    portfolio_ready: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    tagline: Optional[str] = None
    problem_statement: Optional[str] = None
    local_path: Optional[str] = None
    repository_url: Optional[str] = None
    tech_stack_json: Optional[str] = None
    status: Optional[str] = None
    portfolio_ready: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: int
    local_path_exists: bool = False
    tasks: List[ProjectTaskResponse] = []
    architecture_decisions: List[ArchitectureDecisionResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

