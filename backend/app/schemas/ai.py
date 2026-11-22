from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class AIMessageBase(BaseModel):
    role: str
    content: str
    tokens_used: Optional[int] = 0

class AIMessageCreate(AIMessageBase):
    pass

class AIMessageResponse(AIMessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AIConversationBase(BaseModel):
    title: str
    context_type: str = "General Mentor"
    subject_id: Optional[int] = None
    project_id: Optional[int] = None

class AIConversationCreate(AIConversationBase):
    pass

class AIConversationResponse(AIConversationBase):
    id: int
    messages: List[AIMessageResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AIChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    context_type: str = "General Mentor"
    subject_id: Optional[int] = None
    project_id: Optional[int] = None

class AIChatResponse(BaseModel):
    conversation_id: int
    user_message: AIMessageResponse
    assistant_message: AIMessageResponse
    offline_fallback: bool = False

