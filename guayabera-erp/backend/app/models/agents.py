"""
Agent models: Local agents for CAD operations and printing
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class AgentTipo(Base):
    """Types of local agents"""
    __tablename__ = "agt_tipo"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), unique=True, nullable=False)  # "CAD", "PRINT", "DESIGN", etc.
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AgentInstalado(Base):
    """Installed local agents on client machines"""
    __tablename__ = "agt_instalado"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tipo_agente_id = Column(PostgresUUID(as_uuid=True), ForeignKey("agt_tipo.id"), nullable=False)
    
    # Client identification
    nombre_maquina = Column(String(200), nullable=False)
    direccion_ip = Column(String(45))  # IPv4 or IPv6
    sistema_operativo = Column(String(100))
    version_sistema = Column(String(50))
    
    # Agent details
    version_agente = Column(String(50), default="1.0.0")
    token_acceso = Column(String(255), unique=True)  # For secure communication
    puerto_servicio = Column(String(10))  # Port where the agent runs
    
    # Status
    activo = Column(Boolean, default=True)
    ultima_conexion = Column(DateTime(timezone=True))
    ultima_heartbeat = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    tipo_agente = relationship("AgentTipo")


class AgentTarea(Base):
    """Tasks sent to local agents"""
    __tablename__ = "agt_tarea"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agente_id = Column(PostgresUUID(as_uuid=True), ForeignKey("agt_instalado.id"), nullable=False)
    
    # Task details
    tipo_tarea = Column(String(100), nullable=False)  # "generate_pattern", "print_document", "render_design", etc.
    parametros = Column(Text)  # JSON string with task parameters
    estado = Column(String(20), default="pending")  # pending, processing, completed, failed
    progreso = Column(String(10))  # Percentage as string
    
    # Results
    resultado_url = Column(String(500))  # URL to result file
    error_detalle = Column(Text)  # Error details if failed
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True))

    # Relationships
    agente = relationship("AgentInstalado")