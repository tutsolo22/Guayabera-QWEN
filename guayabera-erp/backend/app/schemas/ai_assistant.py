from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


class AIAssistantSessionBase(BaseModel):
    usuario_id: UUID4
    titulo: str = Field(..., max_length=200, description="Título de la sesión")
    contexto: Optional[Dict[str, Any]] = Field(None, description="Contexto de la conversación")


class AIAssistantSessionCreate(AIAssistantSessionBase):
    pass


class AIAssistantSessionUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    contexto: Optional[Dict[str, Any]] = None
    activa: Optional[bool] = None


class AIAssistantSessionResponse(AIAssistantSessionBase):
    id: UUID4
    activa: bool
    ultima_interaccion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AIAssistantMessageBase(BaseModel):
    sesion_id: UUID4
    emisor: str = Field(..., max_length=20, description="Quién emitió el mensaje")
    contenido: str = Field(..., description="Contenido del mensaje")
    tipo: str = Field(default="texto", max_length=30, description="Tipo de mensaje")
    metadata_extra: Optional[Dict[str, Any]] = Field(None, description="Metadatos adicionales")


class AIAssistantMessageCreate(AIAssistantMessageBase):
    pass


class AIAssistantMessageUpdate(BaseModel):
    contenido: Optional[str] = None
    metadata_extra: Optional[Dict[str, Any]] = None


class AIAssistantMessageResponse(AIAssistantMessageBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AIAssistantKnowledgeBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del conocimiento")
    contenido: str = Field(..., description="Contenido del conocimiento")
    categoria: str = Field(..., max_length=50, description="Categoría del conocimiento")
    etiquetas: Optional[Dict[str, Any]] = Field(None, description="Etiquetas para clasificación")
    prioridad: int = Field(default=1, ge=1, le=10, description="Prioridad del conocimiento")


class AIAssistantKnowledgeCreate(AIAssistantKnowledgeBase):
    pass


class AIAssistantKnowledgeUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    contenido: Optional[str] = None
    categoria: Optional[str] = Field(None, max_length=50)
    etiquetas: Optional[Dict[str, Any]] = None
    prioridad: Optional[int] = Field(None, ge=1, le=10)
    activo: Optional[bool] = None


class AIAssistantKnowledgeResponse(AIAssistantKnowledgeBase):
    id: UUID4
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True