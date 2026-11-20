import os
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List, Optional
from pathlib import Path

from backend.app.models.project import Project, ProjectTask, ArchitectureDecision
from backend.app.schemas.project import ProjectCreate, ProjectUpdate, ProjectTaskCreate, ProjectTaskUpdate, ArchitectureDecisionCreate

class ProjectService:
    @staticmethod
    def get_projects(db: Session) -> List[Project]:
        projects = db.query(Project).order_by(Project.updated_at.desc()).all()
        for p in projects:
            p.local_path_exists = bool(p.local_path and os.path.exists(p.local_path))
        return projects

    @staticmethod
    def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
        p = db.query(Project).filter(Project.id == project_id).first()
        if p:
            p.local_path_exists = bool(p.local_path and os.path.exists(p.local_path))
        return p

    @staticmethod
    def create_project(db: Session, data: ProjectCreate) -> Project:
        p = Project(**data.model_dump())
        db.add(p)
        db.commit()
        db.refresh(p)
        p.local_path_exists = bool(p.local_path and os.path.exists(p.local_path))
        return p

    @staticmethod
    def update_project(db: Session, project_id: int, data: ProjectUpdate) -> Optional[Project]:
        p = db.query(Project).filter(Project.id == project_id).first()
        if not p:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(p, key, val)
        db.commit()
        db.refresh(p)
        p.local_path_exists = bool(p.local_path and os.path.exists(p.local_path))
        return p

    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        p = db.query(Project).filter(Project.id == project_id).first()
        if not p:
            return False
        db.delete(p)
        db.commit()
        return True

    @staticmethod
    def create_task(db: Session, data: ProjectTaskCreate) -> ProjectTask:
        task = ProjectTask(**data.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update_task(db: Session, task_id: int, data: ProjectTaskUpdate) -> Optional[ProjectTask]:
        task = db.query(ProjectTask).filter(ProjectTask.id == task_id).first()
        if not task:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(task, key, val)
        if data.status == "Done" and not task.completed_at:
            task.completed_at = datetime.now(timezone.utc)
        elif data.status and data.status != "Done":
            task.completed_at = None
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        task = db.query(ProjectTask).filter(ProjectTask.id == task_id).first()
        if not task:
            return False
        db.delete(task)
        db.commit()
        return True

    @staticmethod
    def create_adr(db: Session, data: ArchitectureDecisionCreate) -> ArchitectureDecision:
        adr = ArchitectureDecision(**data.model_dump())
        db.add(adr)
        db.commit()
        db.refresh(adr)
        return adr

    @staticmethod
    def auto_import_existing_projects(db: Session) -> int:
        r"""
        Inspects E:\Project Folder\ and registers Billing 2.0, Sentinel-NLP, and venturebot if not already registered.
        """
        parent_dir = Path("E:/Project Folder")
        candidates = [
            {
                "name": "Billing 2.0",
                "slug": "billing-2-0",
                "tagline": "Travel billing, invoicing & ERP system",
                "problem_statement": "Streamline complex agency travel invoicing, GST computations and client accounting.",
                "local_path": str(parent_dir / "Billing 2.0"),
                "tech_stack_json": '["FastAPI", "MongoDB", "React", "Docker"]',
                "status": "Active",
                "portfolio_ready": True
            },
            {
                "name": "Sentinel-NLP",
                "slug": "sentinel-nlp",
                "tagline": "NLP-based spam classification and feature engineering",
                "problem_statement": "Real-time classification and intent detection for adversarial spam messages.",
                "local_path": str(parent_dir / "Sentinel-NLP"),
                "tech_stack_json": '["Python", "NLP", "Scikit-Learn", "Pytest"]',
                "status": "Active",
                "portfolio_ready": False
            },
            {
                "name": "VentureBot",
                "slug": "venturebot",
                "tagline": "Autonomous business opportunity evaluation & validation agent",
                "problem_statement": "Discover, score and validate SaaS and AI micro-business opportunities.",
                "local_path": str(parent_dir / "venturebot"),
                "tech_stack_json": '["Python", "FastAPI", "Workers", "SQLite"]',
                "status": "Active",
                "portfolio_ready": False
            }
        ]

        imported_count = 0
        for item in candidates:
            exists = db.query(Project).filter(Project.slug == item["slug"]).first()
            if not exists and os.path.exists(item["local_path"]):
                p = Project(**item)
                db.add(p)
                imported_count += 1
        if imported_count > 0:
            db.commit()
        return imported_count
