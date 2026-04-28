from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.ai_assistant import AIAssistantSession
from app.schemas.ai_assistant import (
    AIAssistantSessionCreate, AIAssistantSessionUpdate, AIAssistantSessionResponse,
    AIAssistantMessageCreate, AIAssistantMessageUpdate, AIAssistantMessageResponse,
    AIAssistantKnowledgeCreate, AIAssistantKnowledgeUpdate, AIAssistantKnowledgeResponse
)
from app.crud.ai_assistant import (
    create_ai_session, get_ai_session, get_ai_sessions_by_usuario,
    update_ai_session, delete_ai_session,
    create_ai_message, get_ai_messages_by_sesion, update_ai_message,
    create_ai_knowledge, get_ai_knowledge, get_ai_knowledge_by_categoria,
    get_ai_knowledge_all, update_ai_knowledge, delete_ai_knowledge
)

router = APIRouter()


# ============================================================================
# ENDPOINTS PARA SESIONES DE ASISTENTE DE IA
# ============================================================================

@router.post("/sessions", response_model=AIAssistantSessionResponse)
def create_ai_session_endpoint(
    session_data: AIAssistantSessionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_ai_session(db, session_data)


@router.get("/sessions/{session_id}", response_model=AIAssistantSessionResponse)
def get_ai_session_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    session = get_ai_session(db, UUID(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Sesión de asistente de IA no encontrada")
    return session


@router.get("/sessions/user/{usuario_id}", response_model=List[AIAssistantSessionResponse])
def get_ai_sessions_by_usuario_endpoint(
    usuario_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_ai_sessions_by_usuario(db, UUID(usuario_id), skip, limit)


@router.put("/sessions/{session_id}", response_model=AIAssistantSessionResponse)
def update_ai_session_endpoint(
    session_id: str,
    session_data: AIAssistantSessionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_session = update_ai_session(db, UUID(session_id), session_data)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Sesión de asistente de IA no encontrada")
    return updated_session


@router.delete("/sessions/{session_id}")
def delete_ai_session_endpoint(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_ai_session(db, UUID(session_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Sesión de asistente de IA no encontrada")
    return {"message": "Sesión de asistente de IA eliminada exitosamente"}


# ============================================================================
# ENDPOINTS PARA MENSAJES DE ASISTENTE DE IA
# ============================================================================

@router.post("/messages", response_model=AIAssistantMessageResponse)
def create_ai_message_endpoint(
    message_data: AIAssistantMessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_ai_message(db, message_data)


@router.get("/messages/session/{sesion_id}", response_model=List[AIAssistantMessageResponse])
def get_ai_messages_by_sesion_endpoint(
    sesion_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_ai_messages_by_sesion(db, UUID(sesion_id), skip, limit)


@router.put("/messages/{message_id}", response_model=AIAssistantMessageResponse)
def update_ai_message_endpoint(
    message_id: str,
    message_data: AIAssistantMessageUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_message = update_ai_message(db, UUID(message_id), message_data)
    if not updated_message:
        raise HTTPException(status_code=404, detail="Mensaje de asistente de IA no encontrado")
    return updated_message


# ============================================================================
# ENDPOINTS PARA CONOCIMIENTO DE ASISTENTE DE IA
# ============================================================================

@router.post("/knowledge", response_model=AIAssistantKnowledgeResponse)
def create_ai_knowledge_endpoint(
    knowledge_data: AIAssistantKnowledgeCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de administrador pueden crear conocimiento
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear conocimiento")
    
    return create_ai_knowledge(db, knowledge_data)


@router.get("/knowledge/{knowledge_id}", response_model=AIAssistantKnowledgeResponse)
def get_ai_knowledge_endpoint(
    knowledge_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    knowledge = get_ai_knowledge(db, UUID(knowledge_id))
    if not knowledge:
        raise HTTPException(status_code=404, detail="Conocimiento de asistente de IA no encontrado")
    return knowledge


@router.get("/knowledge", response_model=List[AIAssistantKnowledgeResponse])
def get_ai_knowledge_all_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_ai_knowledge_all(db, skip, limit)


@router.get("/knowledge/category/{categoria}", response_model=List[AIAssistantKnowledgeResponse])
def get_ai_knowledge_by_categoria_endpoint(
    categoria: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_ai_knowledge_by_categoria(db, categoria, skip, limit)


@router.put("/knowledge/{knowledge_id}", response_model=AIAssistantKnowledgeResponse)
def update_ai_knowledge_endpoint(
    knowledge_id: str,
    knowledge_data: AIAssistantKnowledgeUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador pueden actualizar conocimiento
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar conocimiento")
    
    updated_knowledge = update_ai_knowledge(db, UUID(knowledge_id), knowledge_data)
    if not updated_knowledge:
        raise HTTPException(status_code=404, detail="Conocimiento de asistente de IA no encontrado")
    return updated_knowledge


@router.delete("/knowledge/{knowledge_id}")
def delete_ai_knowledge_endpoint(
    knowledge_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de administrador pueden eliminar conocimiento
    if not current_user.get("rol") in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar conocimiento")
    
    deleted = delete_ai_knowledge(db, UUID(knowledge_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Conocimiento de asistente de IA no encontrado")
    return {"message": "Conocimiento de asistente de IA eliminado exitosamente"}