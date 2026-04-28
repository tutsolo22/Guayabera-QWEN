"""
Agent schemas: Pydantic schemas for local agents
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Agent Type Schemas
class AgentTipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class AgentTipoCreate(AgentTipoBase):
    pass


class AgentTipoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class AgentTipo(AgentTipoBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Installed Agent Schemas
class AgentInstaladoBase(BaseModel):
    tipo_agente_id: UUID
    nombre_maquina: str
    direccion_ip: Optional[str] = None
    sistema_operativo: Optional[str] = None
    version_sistema: Optional[str] = None
    version_agente: Optional[str] = "1.0.0"
    puerto_servicio: Optional[str] = None
    activo: bool = True


class AgentInstaladoCreate(AgentInstaladoBase):
    token_acceso: str


class AgentInstaladoUpdate(BaseModel):
    direccion_ip: Optional[str] = None
    sistema_operativo: Optional[str] = None
    version_sistema: Optional[str] = None
    version_agente: Optional[str] = None
    puerto_servicio: Optional[str] = None
    activo: Optional[bool] = None
    token_acceso: Optional[str] = None


class AgentInstalado(AgentInstaladoBase):
    id: UUID
    token_acceso: str
    ultima_conexion: Optional[datetime] = None
    ultima_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    tipo_agente: AgentTipo

    class Config:
        from_attributes = True


# Agent Task Schemas
class AgentTareaBase(BaseModel):
    agente_id: UUID
    tipo_tarea: str
    parametros: Optional[str] = None  # JSON string with task parameters
    estado: str = "pending"  # pending, processing, completed, failed
    progreso: Optional[str] = "0%"  # Percentage as string


class AgentTareaCreate(AgentTareaBase):
    pass


class AgentTareaUpdate(BaseModel):
    estado: Optional[str] = None  # pending, processing, completed, failed
    progreso: Optional[str] = None  # Percentage as string
    resultado_url: Optional[str] = None
    error_detalle: Optional[str] = None


class AgentTarea(AgentTareaBase):
    id: UUID
    resultado_url: Optional[str] = None
    error_detalle: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    agente: AgentInstalado

    class Config:
        from_attributes = True


# Response schemas
class AgentRegistrationResponse(BaseModel):
    success: bool
    message: str
    agent_id: Optional[UUID] = None
    token_acceso: Optional[str] = None


class AgentTaskResponse(BaseModel):
    success: bool
    message: str
    task_id: Optional[UUID] = None
    resultado_url: Optional[str] = None