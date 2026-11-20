from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List, Optional
from backend.app.models.learning import Semester, Subject, Topic, Subtopic, StudySession, Note, Assessment
from backend.app.schemas.learning import (
    SubjectCreate, SubjectUpdate, TopicCreate, TopicUpdate, 
    StudySessionCreate, NoteCreate, NoteUpdate, SemesterCreate
)

class LearningService:
    @staticmethod
    def get_semesters(db: Session) -> List[Semester]:
        return db.query(Semester).order_by(Semester.created_at.desc()).all()

    @staticmethod
    def create_semester(db: Session, data: SemesterCreate) -> Semester:
        if data.is_current:
            # Unset is_current on all other semesters
            db.query(Semester).update({Semester.is_current: False})
        sem = Semester(**data.model_dump())
        db.add(sem)
        db.commit()
        db.refresh(sem)
        return sem

    @staticmethod
    def get_subjects(db: Session, semester_id: Optional[int] = None) -> List[Subject]:
        query = db.query(Subject)
        if semester_id:
            query = query.filter(Subject.semester_id == semester_id)
        subjects = query.order_by(Subject.priority.asc(), Subject.name.asc()).all()
        
        # Calculate total study minutes for each subject
        for sub in subjects:
            total_mins = db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))\
                .filter(StudySession.subject_id == sub.id).scalar()
            sub.total_study_minutes = total_mins
        return subjects

    @staticmethod
    def get_subject_by_id(db: Session, subject_id: int) -> Optional[Subject]:
        sub = db.query(Subject).filter(Subject.id == subject_id).first()
        if sub:
            total_mins = db.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))\
                .filter(StudySession.subject_id == sub.id).scalar()
            sub.total_study_minutes = total_mins
        return sub

    @staticmethod
    def create_subject(db: Session, data: SubjectCreate) -> Subject:
        sub = Subject(**data.model_dump())
        db.add(sub)
        db.commit()
        db.refresh(sub)
        sub.total_study_minutes = 0
        return sub

    @staticmethod
    def update_subject(db: Session, subject_id: int, data: SubjectUpdate) -> Optional[Subject]:
        sub = db.query(Subject).filter(Subject.id == subject_id).first()
        if not sub:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(sub, key, val)
        db.commit()
        db.refresh(sub)
        return sub

    @staticmethod
    def delete_subject(db: Session, subject_id: int) -> bool:
        sub = db.query(Subject).filter(Subject.id == subject_id).first()
        if not sub:
            return False
        db.delete(sub)
        db.commit()
        return True

    @staticmethod
    def create_topic(db: Session, data: TopicCreate) -> Topic:
        topic = Topic(**data.model_dump())
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return topic

    @staticmethod
    def update_topic(db: Session, topic_id: int, data: TopicUpdate) -> Optional[Topic]:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return None
        for key, val in data.model_dump(exclude_unset=True).items():
            setattr(topic, key, val)
        db.commit()
        db.refresh(topic)
        return topic

    @staticmethod
    def delete_topic(db: Session, topic_id: int) -> bool:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return False
        db.delete(topic)
        db.commit()
        return True

    @staticmethod
    def log_study_session(db: Session, data: StudySessionCreate) -> StudySession:
        session = StudySession(**data.model_dump())
        if not session.session_date:
            session.session_date = date.today()
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def get_study_sessions(db: Session, limit: int = 50) -> List[StudySession]:
        return db.query(StudySession).order_by(StudySession.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_notes(db: Session, subject_id: Optional[int] = None) -> List[Note]:
        q = db.query(Note)
        if subject_id:
            q = q.filter(Note.subject_id == subject_id)
        return q.order_by(Note.updated_at.desc()).all()

    @staticmethod
    def create_note(db: Session, data: NoteCreate) -> Note:
        note = Note(**data.model_dump())
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

