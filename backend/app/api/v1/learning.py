from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.services.learning_service import LearningService
from backend.app.schemas.learning import (
    SemesterCreate, SemesterResponse,
    SubjectCreate, SubjectUpdate, SubjectResponse,
    TopicCreate, TopicUpdate, TopicResponse,
    StudySessionCreate, StudySessionResponse,
    NoteCreate, NoteUpdate, NoteResponse
)

router = APIRouter(prefix="/learning", tags=["Learning Command Center"])

# --- SEMESTERS ---
@router.get("/semesters", response_model=List[SemesterResponse])
def get_semesters(db: Session = Depends(get_db)):
    return LearningService.get_semesters(db)

@router.post("/semesters", response_model=SemesterResponse, status_code=status.HTTP_201_CREATED)
def create_semester(data: SemesterCreate, db: Session = Depends(get_db)):
    return LearningService.create_semester(db, data)

# --- SUBJECTS ---
@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(semester_id: Optional[int] = None, db: Session = Depends(get_db)):
    return LearningService.get_subjects(db, semester_id)

@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    sub = LearningService.get_subject_by_id(db, subject_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Subject not found")
    return sub

@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):
    return LearningService.create_subject(db, data)

@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: int, data: SubjectUpdate, db: Session = Depends(get_db)):
    sub = LearningService.update_subject(db, subject_id, data)
    if not sub:
        raise HTTPException(status_code=404, detail="Subject not found")
    return sub

@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    success = LearningService.delete_subject(db, subject_id)
    if not success:
        raise HTTPException(status_code=404, detail="Subject not found")
    return {"message": "Subject deleted successfully"}

# --- TOPICS ---
@router.post("/topics", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(data: TopicCreate, db: Session = Depends(get_db)):
    return LearningService.create_topic(db, data)

@router.put("/topics/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, data: TopicUpdate, db: Session = Depends(get_db)):
    top = LearningService.update_topic(db, topic_id, data)
    if not top:
        raise HTTPException(status_code=404, detail="Topic not found")
    return top

@router.delete("/topics/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    success = LearningService.delete_topic(db, topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return {"message": "Topic deleted successfully"}

# --- STUDY SESSIONS ---
@router.post("/sessions", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def log_study_session(data: StudySessionCreate, db: Session = Depends(get_db)):
    return LearningService.log_study_session(db, data)

@router.get("/sessions", response_model=List[StudySessionResponse])
def get_study_sessions(limit: int = 50, db: Session = Depends(get_db)):
    return LearningService.get_study_sessions(db, limit)

# --- NOTES ---
@router.get("/notes", response_model=List[NoteResponse])
def get_notes(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    return LearningService.get_notes(db, subject_id)

@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    return LearningService.create_note(db, data)

