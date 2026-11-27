from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.core.database import get_db
from backend.app.models.ai import AIConversation, AIMessage
from backend.app.schemas.ai import (
    AIConversationCreate, AIConversationResponse,
    AIMessageResponse, AIChatRequest, AIChatResponse
)
from backend.app.ai.providers.gemini import GeminiProvider
from backend.app.ai.context_builder import ContextBuilder
from backend.app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI Mentor & Knowledge Layer"])

provider = GeminiProvider()

@router.get("/conversations", response_model=List[AIConversationResponse])
def get_conversations(db: Session = Depends(get_db)):
    return db.query(AIConversation).order_by(AIConversation.updated_at.desc()).all()

@router.get("/conversations/{conv_id}", response_model=AIConversationResponse)
def get_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(AIConversation).filter(AIConversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.post("/conversations", response_model=AIConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(data: AIConversationCreate, db: Session = Depends(get_db)):
    conv = AIConversation(**data.model_dump())
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.delete("/conversations/{conv_id}")
def delete_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(AIConversation).filter(AIConversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return {"message": "Conversation deleted"}

@router.post("/chat", response_model=AIChatResponse)
async def chat_with_mentor(req: AIChatRequest, db: Session = Depends(get_db)):
    # 1. Retrieve or create conversation
    if req.conversation_id:
        conv = db.query(AIConversation).filter(AIConversation.id == req.conversation_id).first()
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        title = req.message[:40] + ("..." if len(req.message) > 40 else "")
        conv = AIConversation(
            title=title,
            context_type=req.context_type,
            subject_id=req.subject_id,
            project_id=req.project_id
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # 2. Persist user message
    user_msg = AIMessage(
        conversation_id=conv.id,
        role="user",
        content=req.message
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 3. Build selective context and history
    system_instruction = ContextBuilder.build_system_instruction(
        db=db,
        context_type=conv.context_type,
        subject_id=conv.subject_id,
        project_id=conv.project_id
    )

    recent_messages = db.query(AIMessage)\
        .filter(AIMessage.conversation_id == conv.id, AIMessage.id != user_msg.id)\
        .order_by(AIMessage.created_at.desc()).limit(6).all()
    
    history = [{"role": m.role, "content": m.content} for m in reversed(recent_messages)]

    # 4. Generate reply via provider
    is_offline = bool(not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY.strip() == "")
    reply_text = await provider.generate_reply(
        prompt=req.message,
        system_instruction=system_instruction,
        history=history
    )

    # 5. Persist assistant reply
    assistant_msg = AIMessage(
        conversation_id=conv.id,
        role="assistant",
        content=reply_text
    )
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)

    return AIChatResponse(
        conversation_id=conv.id,
        user_message=AIMessageResponse.model_validate(user_msg),
        assistant_message=AIMessageResponse.model_validate(assistant_msg),
        offline_fallback=is_offline
    )

