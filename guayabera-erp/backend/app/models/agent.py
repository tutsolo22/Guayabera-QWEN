"""
Agent models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class AgentTipo(Base):
    """Agent type model"""
    __tablename__ = "agentes_tipos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    icono = Column(String(50))
    color = Column(String(7))  # Hex color code
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AgentInstalado(Base):
    """Installed agent model"""
    __tablename__ = "agentes_instalados"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo_agente_id = Column(UUID(as_uuid=True), ForeignKey("agentes_tipos.id"), nullable=False)
    
    # Machine identification
    nombre_maquina = Column(String(100), nullable=False)
    direccion_ip = Column(String(45), nullable=False)  # IPv4 or IPv6
    sistema_operativo = Column(String(50), nullable=False)
    version_sistema = Column(String(20))
    version_agente = Column(String(20))
    
    # Service configuration
    puerto_servicio = Column(Integer, default=8080)
    token_acceso = Column(String(64), unique=True)  # Secure token for authentication
    
    # Status
    activo = Column(Boolean, default=True)
    ultima_conexion = Column(DateTime(timezone=True))
    ultima_heartbeat = Column(DateTime(timezone=True))
    
    # Metadata
    notas = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tipo_agente = relationship("AgentTipo", backref="agentes_instalados")


class AgentTarea(Base):
    """Agent task model"""
    __tablename__ = "agentes_tareas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agente_id = Column(UUID(as_uuid=True), ForeignKey("agentes_instalados.id"), nullable=False)
    
    # Task specification
    tipo_tarea = Column(String(100), nullable=False)  # backup, report, sync, etc.
    parametros = Column(Text)  # JSON string with task parameters
    
    # Execution
    estado = Column(String(20), default="pending")  # pending, running, completed, failed
    resultado = Column(Text)  # Output or error message
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True))
    
    # Metadata
    creado_por = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from users to seg_usuario - Who created the task
    creado_para = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from users to seg_usuario - Who the task is for
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    agente = relationship("AgentInstalado", backref="tareas")
