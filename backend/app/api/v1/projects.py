from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.database import get_db
from backend.app.services.project_service import ProjectService
from backend.app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ProjectTaskCreate, ProjectTaskUpdate, ProjectTaskResponse,
    ArchitectureDecisionCreate, ArchitectureDecisionResponse
)

router = APIRouter(prefix="/projects", tags=["Project Intelligence"])

@router.get("", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return ProjectService.get_projects(db)

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectService.create_project(db, data)

@router.post("/auto-import", response_model=dict)
def auto_import(db: Session = Depends(get_db)):
    count = ProjectService.auto_import_existing_projects(db)
    return {"message": f"Successfully registered {count} projects from local workspace.", "count": count}

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = ProjectService.get_project_by_id(db, project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    p = ProjectService.update_project(db, project_id, data)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    success = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

# --- TASKS ---
@router.post("/tasks", response_model=ProjectTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(data: ProjectTaskCreate, db: Session = Depends(get_db)):
    return ProjectService.create_task(db, data)

@router.put("/tasks/{task_id}", response_model=ProjectTaskResponse)
def update_task(task_id: int, data: ProjectTaskUpdate, db: Session = Depends(get_db)):
    task = ProjectService.update_task(db, task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = ProjectService.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}

# --- ARCHITECTURE DECISIONS (ADRs) ---
@router.post("/adrs", response_model=ArchitectureDecisionResponse, status_code=status.HTTP_201_CREATED)
def create_adr(data: ArchitectureDecisionCreate, db: Session = Depends(get_db)):
    return ProjectService.create_adr(db, data)

