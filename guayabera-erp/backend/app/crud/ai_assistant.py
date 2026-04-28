from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.ai_assistant import AIAssistantSession, AIAssistantMessage, AIAssistantKnowledge
from app.schemas.ai_assistant import (
    AIAssistantSessionCreate, AIAssistantSessionUpdate, AIAssistantSessionResponse,
    AIAssistantMessageCreate, AIAssistantMessageUpdate, AIAssistantMessageResponse,
    AIAssistantKnowledgeCreate, AIAssistantKnowledgeUpdate, AIAssistantKnowledgeResponse
)


def create_ai_session(db: Session, session_data: AIAssistantSessionCreate) -> AIAssistantSession:
    """Create a new AI assistant session"""
    db_session = AIAssistantSession(**session_data.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_ai_session(db: Session, session_id: UUID) -> Optional[AIAssistantSession]:
    """Get an AI assistant session by ID"""
    return db.query(AIAssistantSession).filter(AIAssistantSession.id == session_id).first()


def get_ai_sessions_by_usuario(db: Session, usuario_id: UUID, skip: int = 0, limit: int = 100) -> List[AIAssistantSession]:
    """Get AI assistant sessions by user ID"""
    return db.query(AIAssistantSession).filter(
        AIAssistantSession.usuario_id == usuario_id
    ).order_by(AIAssistantSession.created_at.desc()).offset(skip).limit(limit).all()


def update_ai_session(
    db: Session, 
    session_id: UUID, 
    session_data: AIAssistantSessionUpdate
) -> Optional[AIAssistantSession]:
    """Update an AI assistant session"""
    db_session = get_ai_session(db, session_id)
    if db_session:
        update_data = session_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        db.commit()
        db.refresh(db_session)
    return db_session


def delete_ai_session(db: Session, session_id: UUID) -> bool:
    """Delete an AI assistant session (soft delete by deactivation)"""
    db_session = get_ai_session(db, session_id)
    if db_session:
        db_session.activa = False
        db.commit()
        return True
    return False


def create_ai_message(db: Session, message_data: AIAssistantMessageCreate) -> AIAssistantMessage:
    """Create a new AI assistant message"""
    db_message = AIAssistantMessage(**message_data.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_ai_messages_by_sesion(db: Session, sesion_id: UUID, skip: int = 0, limit: int = 100) -> List[AIAssistantMessage]:
    """Get AI assistant messages by session ID"""
    return db.query(AIAssistantMessage).filter(
        AIAssistantMessage.sesion_id == sesion_id
    ).order_by(AIAssistantMessage.created_at.asc()).offset(skip).limit(limit).all()


def update_ai_message(
    db: Session, 
    message_id: UUID, 
    message_data: AIAssistantMessageUpdate
) -> Optional[AIAssistantMessage]:
    """Update an AI assistant message"""
    db_message = db.query(AIAssistantMessage).filter(AIAssistantMessage.id == message_id).first()
    if db_message:
        update_data = message_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_message, field, value)
        db.commit()
        db.refresh(db_message)
    return db_message


def create_ai_knowledge(db: Session, knowledge_data: AIAssistantKnowledgeCreate) -> AIAssistantKnowledge:
    """Create a new AI knowledge entry"""
    db_knowledge = AIAssistantKnowledge(**knowledge_data.model_dump())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge


def get_ai_knowledge(db: Session, knowledge_id: UUID) -> Optional[AIAssistantKnowledge]:
    """Get an AI knowledge entry by ID"""
    return db.query(AIAssistantKnowledge).filter(AIAssistantKnowledge.id == knowledge_id).first()


def get_ai_knowledge_by_categoria(db: Session, categoria: str, skip: int = 0, limit: int = 100) -> List[AIAssistantKnowledge]:
    """Get AI knowledge entries by category"""
    return db.query(AIAssistantKnowledge).filter(
        AIAssistantKnowledge.categoria == categoria,
        AIAssistantKnowledge.activo == True
    ).order_by(AIAssistantKnowledge.prioridad.desc()).offset(skip).limit(limit).all()


def get_ai_knowledge_all(db: Session, skip: int = 0, limit: int = 100) -> List[AIAssistantKnowledge]:
    """Get all active AI knowledge entries"""
    return db.query(AIAssistantKnowledge).filter(
        AIAssistantKnowledge.activo == True
    ).order_by(AIAssistantKnowledge.prioridad.desc()).offset(skip).limit(limit).all()


def update_ai_knowledge(
    db: Session, 
    knowledge_id: UUID, 
    knowledge_data: AIAssistantKnowledgeUpdate
) -> Optional[AIAssistantKnowledge]:
    """Update an AI knowledge entry"""
    db_knowledge = get_ai_knowledge(db, knowledge_id)
    if db_knowledge:
        update_data = knowledge_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_knowledge, field, value)
        db.commit()
        db.refresh(db_knowledge)
    return db_knowledge


def delete_ai_knowledge(db: Session, knowledge_id: UUID) -> bool:
    """Delete an AI knowledge entry (soft delete by deactivation)"""
    db_knowledge = get_ai_knowledge(db, knowledge_id)
    if db_knowledge:
        db_knowledge.activo = False
        db.commit()
        return True
    return False