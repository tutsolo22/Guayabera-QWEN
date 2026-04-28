"""
Helpdesk/Ticketing System Schemas: Support tickets, assignments, and tracking
Specialized for ERP system support
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TICKET SCHEMAS
# ============================================================================

class TicketSoporteBase(BaseModel):
    folio: str = Field(..., max_length=20, description="Folio único del ticket")
    titulo: str = Field(..., max_length=200, description="Título del ticket")
    descripcion: str = Field(..., description="Descripción detallada del problema")
    categoria: str = Field(..., description="Categoría del ticket")
    prioridad: Optional[str] = Field(default="media", description="Prioridad del ticket")
    canal_entrada: Optional[str] = Field(default="web", description="Canal por el que entró el ticket")
    solicitante_id: UUID4 = Field(..., description="ID del empleado que abre el ticket")
    supervisor_id: Optional[UUID4] = Field(None, description="ID del supervisor del solicitante")
    asignado_a_id: Optional[UUID4] = Field(None, description="ID del empleado asignado")
    departamento_id: Optional[UUID4] = Field(None, description="ID del departamento responsable")
    autorizado_por_supervisor: Optional[bool] = Field(default=False, description="¿Fue autorizado por el supervisor?")
    fecha_autorizacion_supervisor: Optional[datetime] = Field(None, description="Fecha de autorización del supervisor")
    fecha_notificacion_supervisor: Optional[datetime] = Field(None, description="Fecha de notificación al supervisor")
    estado: Optional[str] = Field(default="abierto", description="Estado actual del ticket")
    fecha_apertura: Optional[datetime] = Field(None, description="Fecha de apertura del ticket")
    fecha_asignacion: Optional[datetime] = Field(None, description="Fecha de asignación")
    fecha_resolucion: Optional[datetime] = Field(None, description="Fecha de resolución")
    fecha_cierre: Optional[datetime] = Field(None, description="Fecha de cierre")
    fecha_limite_respuesta: Optional[datetime] = Field(None, description="Fecha límite para primera respuesta")
    fecha_limite_resolucion: Optional[datetime] = Field(None, description="Fecha límite para resolución")
    fecha_limite_cierre: Optional[datetime] = Field(None, description="Fecha límite para cierre por usuario")
    horas_acumuladas: Optional[float] = Field(default=0.0, description="Horas acumuladas trabajando en el ticket")
    etiquetas: Optional[Dict[str, Any]] = Field(None, description="Etiquetas para el ticket")
    datos_adicionales: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales del ticket")
    tipo_solicitud: Optional[str] = Field(default="soporte", description="Tipo de solicitud: soporte, requisicion, compra")
    numero_requisicion: Optional[str] = Field(None, max_length=30, description="Número de requisición")
    proveedor_id: Optional[UUID4] = Field(None, description="ID del proveedor para requisiciones/compras")
    cotizaciones: Optional[Dict[str, Any]] = Field(None, description="Cotizaciones recibidas")
    autorizado_finanzas: Optional[bool] = Field(default=False, description="¿Fue autorizado por finanzas?")
    fecha_autorizacion_finanzas: Optional[datetime] = Field(None, description="Fecha de autorización por finanzas")
    activo: bool = Field(default=True, description="¿Está activo el ticket?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class TicketSoporteCreate(TicketSoporteBase):
    pass


class TicketSoporteUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    prioridad: Optional[str] = None
    canal_entrada: Optional[str] = None
    asignado_a_id: Optional[UUID4] = None
    departamento_id: Optional[UUID4] = None
    estado: Optional[str] = None
    fecha_asignacion: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    fecha_limite_respuesta: Optional[datetime] = None
    fecha_limite_resolucion: Optional[datetime] = None
    horas_acumuladas: Optional[float] = None
    etiquetas: Optional[Dict[str, Any]] = None
    datos_adicionales: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None


class TicketSoporteResponse(TicketSoporteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# COMMENT SCHEMAS
# ============================================================================

class ComentarioTicketBase(BaseModel):
    ticket_id: UUID4
    autor_id: UUID4
    contenido: str = Field(..., description="Contenido del comentario")
    es_interno: Optional[bool] = Field(default=False, description="¿Es un comentario interno?")


class ComentarioTicketCreate(ComentarioTicketBase):
    pass


class ComentarioTicketUpdate(BaseModel):
    contenido: Optional[str] = None
    es_interno: Optional[bool] = None


class ComentarioTicketResponse(ComentarioTicketBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# STATE HISTORY SCHEMAS
# ============================================================================

class HistorialEstadoBase(BaseModel):
    ticket_id: UUID4
    estado_anterior: Optional[str] = Field(None, description="Estado anterior del ticket")
    estado_nuevo: str = Field(..., description="Nuevo estado del ticket")
    cambiado_por_id: UUID4
    motivo_cambio: Optional[str] = Field(None, description="Motivo del cambio de estado")


class HistorialEstadoCreate(HistorialEstadoBase):
    pass


class HistorialEstadoUpdate(BaseModel):
    motivo_cambio: Optional[str] = None


class HistorialEstadoResponse(HistorialEstadoBase):
    id: UUID4
    fecha_cambio: datetime

    class Config:
        from_attributes = True


# ============================================================================
# SUPPORT CATEGORY SCHEMAS
# ============================================================================

class CategoriaSoporteBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    codigo: str = Field(..., max_length=30, description="Código único de la categoría")
    color_hex: Optional[str] = Field(None, max_length=7, description="Color hexadecimal para UI")
    parent_id: Optional[UUID4] = Field(None, description="ID de la categoría padre")
    horas_respuesta: Optional[int] = Field(None, description="Horas para primera respuesta")
    horas_resolucion: Optional[int] = Field(None, description="Horas para resolución")
    activa: bool = Field(default=True, description="¿Está activa la categoría?")


class CategoriaSoporteCreate(CategoriaSoporteBase):
    pass


class CategoriaSoporteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, max_length=30)
    color_hex: Optional[str] = Field(None, max_length=7)
    parent_id: Optional[UUID4] = None
    horas_respuesta: Optional[int] = None
    horas_resolucion: Optional[int] = None
    activa: Optional[bool] = None


class CategoriaSoporteResponse(CategoriaSoporteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SLA SCHEMAS
# ============================================================================

class SLABase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del SLA")
    descripcion: Optional[str] = Field(None, description="Descripción del SLA")
    codigo: str = Field(..., max_length=30, description="Código único del SLA")
    horas_para_respuesta: int = Field(..., gt=0, description="Horas para primera respuesta")
    horas_para_resolucion: int = Field(..., gt=0, description="Horas para resolución")
    nivel_objetivo: Optional[float] = Field(default=95.0, description="Porcentaje objetivo de cumplimiento")
    prioridad_aplicable: Optional[str] = Field(None, description="Prioridad a la que aplica")
    categoria_aplicable: Optional[str] = Field(None, description="Categoría a la que aplica")
    activo: bool = Field(default=True, description="¿Está activo el SLA?")


class SLACreate(SLABase):
    pass


class SLAUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, max_length=30)
    horas_para_respuesta: Optional[int] = Field(None, gt=0)
    horas_para_resolucion: Optional[int] = Field(None, gt=0)
    nivel_objetivo: Optional[float] = None
    prioridad_aplicable: Optional[str] = None
    categoria_aplicable: Optional[str] = None
    activo: Optional[bool] = None


class SLAResponse(SLABase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SUPPORT DEPARTMENT SCHEMAS
# ============================================================================

class DepartamentoSoporteBase(BaseModel):
    departamento_id: UUID4
    es_grupo_soporte: Optional[bool] = Field(default=False, description="¿Es este departamento un grupo de soporte?")
    horario_atencion: Optional[Dict[str, Any]] = Field(None, description="Horario de atención del departamento")
    tiempo_respuesta_promedio: Optional[float] = Field(None, description="Tiempo promedio de respuesta en horas")
    activo: bool = Field(default=True, description="¿Está activo el departamento de soporte?")


class DepartamentoSoporteCreate(DepartamentoSoporteBase):
    pass


class DepartamentoSoporteUpdate(BaseModel):
    es_grupo_soporte: Optional[bool] = None
    horario_atencion: Optional[Dict[str, Any]] = None
    tiempo_respuesta_promedio: Optional[float] = None
    activo: Optional[bool] = None


class DepartamentoSoporteResponse(DepartamentoSoporteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# AGENT DEPARTMENT LINK SCHEMAS
# ============================================================================

class AgenteDepartamentoBase(BaseModel):
    empleado_id: UUID4
    departamento_soporte_id: UUID4
    nivel_experiencia: Optional[int] = Field(default=1, ge=1, le=5, description="Nivel de experiencia del agente (1-5)")
    especialidades: Optional[Dict[str, Any]] = Field(None, description="Especialidades del agente")
    activo: bool = Field(default=True, description="¿Está activo el vínculo?")


class AgenteDepartamentoCreate(AgenteDepartamentoBase):
    pass


class AgenteDepartamentoUpdate(BaseModel):
    nivel_experiencia: Optional[int] = Field(None, ge=1, le=5)
    especialidades: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class AgenteDepartamentoResponse(AgenteDepartamentoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True