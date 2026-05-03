"""
Agent schemas
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


# =============================================================================
# AGENT TYPE SCHEMAS
# =============================================================================

class AgentTipoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None
    activo: bool = True


class AgentTipoCreate(AgentTipoBase):
    pass


class AgentTipoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None
    activo: Optional[bool] = None


class AgentTipo(AgentTipoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =============================================================================
# INSTALLED AGENT SCHEMAS
# =============================================================================

class AgentInstaladoBase(BaseModel):
    tipo_agente_id: UUID
    
    # Machine identification
    nombre_maquina: str
    direccion_ip: str
    sistema_operativo: str
    version_sistema: Optional[str] = None
    version_agente: Optional[str] = None
    
    # Service configuration
    puerto_servicio: Optional[int] = 8080
    token_acceso: Optional[str] = None
    
    # Status
    activo: bool = True
    ultima_conexion: Optional[datetime] = None
    ultima_heartbeat: Optional[datetime] = None
    
    # Metadata
    notas: Optional[str] = None


class AgentInstaladoCreate(AgentInstaladoBase):
    pass


class AgentInstaladoUpdate(BaseModel):
    tipo_agente_id: Optional[UUID] = None
    
    # Machine identification
    nombre_maquina: Optional[str] = None
    direccion_ip: Optional[str] = None
    sistema_operativo: Optional[str] = None
    version_sistema: Optional[str] = None
    version_agente: Optional[str] = None
    
    # Service configuration
    puerto_servicio: Optional[int] = None
    token_acceso: Optional[str] = None
    
    # Status
    activo: Optional[bool] = None
    ultima_conexion: Optional[datetime] = None
    ultima_heartbeat: Optional[datetime] = None
    
    # Metadata
    notas: Optional[str] = None


class AgentInstalado(AgentInstaladoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# =============================================================================
# AGENT TASK SCHEMAS
# =============================================================================

class AgentTareaBase(BaseModel):
    agente_id: UUID
    
    # Task specification
    tipo_tarea: str
    parametros: Optional[str] = None
    
    # Execution
    estado: str = "pending"
    resultado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    # Metadata
    creado_por: Optional[int] = None
    creado_para: Optional[int] = None


class AgentTareaCreate(AgentTareaBase):
    pass


class AgentTareaUpdate(BaseModel):
    agente_id: Optional[UUID] = None
    
    # Task specification
    tipo_tarea: Optional[str] = None
    parametros: Optional[str] = None
    
    # Execution
    estado: Optional[str] = None
    resultado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    # Metadata
    creado_por: Optional[int] = None
    creado_para: Optional[int] = None


class AgentTarea(AgentTareaBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True