from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime

class SubtopicBase(BaseModel):
    title: str
    is_completed: bool = False

class SubtopicCreate(SubtopicBase):
    topic_id: int

class SubtopicResponse(SubtopicBase):
    id: int
    topic_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int = 0
    status: str = "Not Started"
    mastery_score: int = 0

class TopicCreate(TopicBase):
    subject_id: int

class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    status: Optional[str] = None
    mastery_score: Optional[int] = None

class TopicResponse(TopicBase):
    id: int
    subject_id: int
    subtopics: List[SubtopicResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SubjectBase(BaseModel):
    name: str
    code: Optional[str] = None
    category: str = "Core Academic"
    difficulty: str = "Medium"
    priority: str = "P1"
    target_completion_date: Optional[date] = None
    status: str = "Not Started"
    semester_id: Optional[int] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    priority: Optional[str] = None
    target_completion_date: Optional[date] = None
    status: Optional[str] = None
    semester_id: Optional[int] = None

class StudySessionBase(BaseModel):
    subject_id: int
    topic_id: Optional[int] = None
    duration_minutes: int
    session_type: str = "Study"
    notes: Optional[str] = None
    session_date: Optional[date] = None

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionResponse(StudySessionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class NoteBase(BaseModel):
    subject_id: int
    topic_id: Optional[int] = None
    title: str
    content_markdown: str
    tags: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content_markdown: Optional[str] = None
    tags: Optional[str] = None

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SubjectResponse(SubjectBase):
    id: int
    topics: List[TopicResponse] = []
    total_study_minutes: int = 0
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class SemesterBase(BaseModel):
    name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: bool = False

class SemesterCreate(SemesterBase):
    pass

class SemesterResponse(SemesterBase):
    id: int
    subjects: List[SubjectResponse] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

