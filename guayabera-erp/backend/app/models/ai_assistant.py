from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class AIAssistantSession(Base):
    """Sesiones de asistencia del agente de IA - AI Assistant Sessions"""
    __tablename__ = "ai_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    titulo = Column(String(200), nullable=False)  # Título de la sesión
    activa = Column(Boolean, default=True)  # Si la sesión está activa
    contexto = Column(JSONB)  # Contexto actual de la conversación
    ultima_interaccion = Column(DateTime(timezone=True), server_default=func.now())  # Última interacción
    
    usuario = relationship("Empleado")
    mensajes = relationship("AIAssistantMessage", back_populates="sesion")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AIAssistantMessage(Base):
    """Mensajes del agente de IA - AI Assistant Messages"""
    __tablename__ = "ai_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    sesion_id = Column(UUID(as_uuid=True), ForeignKey("ai_sessions.id"), nullable=False)
    emisor = Column(String(20), nullable=False)  # "usuario" o "ia"
    contenido = Column(Text, nullable=False)  # Contenido del mensaje
    tipo = Column(String(30), default="texto")  # texto, imagen, archivo, etc.
    metadata_extra = Column(JSONB)  # Metadatos adicionales del mensaje
    
    sesion = relationship("AIAssistantSession", back_populates="mensajes")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AIAssistantKnowledge(Base):
    """Conocimiento del agente de IA - AI Assistant Knowledge Base"""
    __tablename__ = "ai_knowledge"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)  # Contenido del conocimiento
    categoria = Column(String(50), nullable=False)  # ventas, inventario, rh, etc.
    etiquetas = Column(JSONB)  # Etiquetas para clasificación
    prioridad = Column(Integer, default=1)  # Prioridad del conocimiento (1-10)
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())