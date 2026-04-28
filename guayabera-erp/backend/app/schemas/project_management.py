"""
Project Management Schemas: Project coordination, resource assignment, scheduling and milestones
Specialized for textile product development projects
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
# PROJECT SCHEMAS
# ============================================================================

class ProyectoBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del proyecto")
    nombre: str = Field(..., max_length=150, description="Nombre del proyecto")
    descripcion: Optional[str] = Field(None, description="Descripción del proyecto")
    tipo_proyecto: Optional[str] = Field(None, max_length=50, description="Tipo de proyecto")
    cliente_id: Optional[UUID4] = Field(None, description="ID del cliente asociado")
    responsable_id: UUID4 = Field(..., description="ID del responsable del proyecto")
    fecha_inicio: date = Field(..., description="Fecha de inicio del proyecto")
    fecha_fin_prevista: date = Field(..., description="Fecha de finalización prevista")
    fecha_fin_real: Optional[date] = Field(None, description="Fecha de finalización real")
    presupuesto_total: Optional[Decimal] = Field(default=Decimal('0.00'), description="Presupuesto total del proyecto")
    costo_acumulado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo acumulado del proyecto")
    estado: Optional[str] = Field(default="planificacion", description="Estado del proyecto")
    porcentaje_completado: Optional[int] = Field(default=0, ge=0, le=100, description="Porcentaje de completado del proyecto")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    datos_adicionales: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales del proyecto")


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_proyecto: Optional[str] = Field(None, max_length=50)
    cliente_id: Optional[UUID4] = None
    responsable_id: Optional[UUID4] = None
    fecha_inicio: Optional[date] = None
    fecha_fin_prevista: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    presupuesto_total: Optional[Decimal] = None
    costo_acumulado: Optional[Decimal] = None
    estado: Optional[str] = None
    porcentaje_completado: Optional[int] = Field(None, ge=0, le=100)
    comentarios: Optional[str] = None
    datos_adicionales: Optional[Dict[str, Any]] = None


class ProyectoResponse(ProyectoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TASK SCHEMAS
# ============================================================================

class TareaBase(BaseModel):
    proyecto_id: UUID4
    codigo: str = Field(..., max_length=30, description="Código único de la tarea")
    nombre: str = Field(..., max_length=150, description="Nombre de la tarea")
    descripcion: Optional[str] = Field(None, description="Descripción de la tarea")
    asignado_a_id: Optional[UUID4] = Field(None, description="ID del empleado asignado")
    prioridad: Optional[str] = Field(default="media", description="Prioridad de la tarea")
    estado: Optional[str] = Field(default="pendiente", description="Estado de la tarea")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la tarea")
    fecha_fin_prevista: date = Field(..., description="Fecha de finalización prevista")
    fecha_fin_real: Optional[date] = Field(None, description="Fecha de finalización real")
    porcentaje_completado: Optional[int] = Field(default=0, ge=0, le=100, description="Porcentaje de completado de la tarea")
    duracion_estimada_horas: Optional[int] = Field(None, ge=0, description="Duración estimada en horas")
    duracion_real_horas: Optional[int] = Field(default=0, ge=0, description="Duración real en horas")
    tarea_padre_id: Optional[UUID4] = Field(None, description="ID de la tarea padre")
    depende_de_id: Optional[UUID4] = Field(None, description="ID de la tarea de la que depende")
    costo_estimado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo estimado de la tarea")
    costo_real: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo real de la tarea")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    asignado_a_id: Optional[UUID4] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin_prevista: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    porcentaje_completado: Optional[int] = Field(None, ge=0, le=100)
    duracion_estimada_horas: Optional[int] = Field(None, ge=0)
    duracion_real_horas: Optional[int] = Field(None, ge=0)
    tarea_padre_id: Optional[UUID4] = None
    depende_de_id: Optional[UUID4] = None
    costo_estimado: Optional[Decimal] = None
    costo_real: Optional[Decimal] = None
    comentarios: Optional[str] = None


class TareaResponse(TareaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PROJECT RESOURCE SCHEMAS
# ============================================================================

class RecursoProyectoBase(BaseModel):
    proyecto_id: UUID4
    recurso_id: UUID4
    tipo_recurso: str = Field(..., description="Tipo de recurso")
    cantidad: Optional[int] = Field(default=1, ge=1, description="Cantidad del recurso")
    costo_unitario: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo unitario del recurso")
    costo_total: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo total del recurso")
    fecha_inicio: date = Field(..., description="Fecha de inicio del uso del recurso")
    fecha_fin: date = Field(..., description="Fecha de fin del uso del recurso")
    activo: bool = Field(default=True, description="¿Está activo el recurso?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class RecursoProyectoCreate(RecursoProyectoBase):
    pass


class RecursoProyectoUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, ge=1)
    costo_unitario: Optional[Decimal] = None
    costo_total: Optional[Decimal] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None


class RecursoProyectoResponse(RecursoProyectoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# RESOURCE SCHEMAS
# ============================================================================

class RecursoBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del recurso")
    nombre: str = Field(..., max_length=100, description="Nombre del recurso")
    descripcion: Optional[str] = Field(None, description="Descripción del recurso")
    tipo: str = Field(..., description="Tipo de recurso")
    proveedor_id: Optional[UUID4] = Field(None, description="ID del proveedor del recurso")
    empleado_id: Optional[UUID4] = Field(None, description="ID del empleado asociado al recurso")
    costo_por_unidad: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo por unidad del recurso")
    estado: Optional[str] = Field(default="disponible", description="Estado del recurso")
    capacidad_total: Optional[int] = Field(default=1, ge=1, description="Capacidad total del recurso")
    capacidad_utilizada: Optional[int] = Field(default=0, ge=0, description="Capacidad utilizada del recurso")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    datos_especificos: Optional[Dict[str, Any]] = Field(None, description="Datos específicos del recurso")


class RecursoCreate(RecursoBase):
    pass


class RecursoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    proveedor_id: Optional[UUID4] = None
    empleado_id: Optional[UUID4] = None
    costo_por_unidad: Optional[Decimal] = None
    estado: Optional[str] = None
    capacidad_total: Optional[int] = Field(None, ge=1)
    capacidad_utilizada: Optional[int] = Field(None, ge=0)
    comentarios: Optional[str] = None
    datos_especificos: Optional[Dict[str, Any]] = None


class RecursoResponse(RecursoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TASK RESOURCE ASSIGNMENT SCHEMAS
# ============================================================================

class RecursoTareaBase(BaseModel):
    tarea_id: UUID4
    recurso_id: UUID4
    cantidad: Optional[int] = Field(default=1, ge=1, description="Cantidad del recurso asignado")
    costo_unitario: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo unitario del recurso asignado")
    costo_total: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo total del recurso asignado")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la asignación")
    fecha_fin: date = Field(..., description="Fecha de fin de la asignación")
    activo: bool = Field(default=True, description="¿Está activa la asignación?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class RecursoTareaCreate(RecursoTareaBase):
    pass


class RecursoTareaUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, ge=1)
    costo_unitario: Optional[Decimal] = None
    costo_total: Optional[Decimal] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None


class RecursoTareaResponse(RecursoTareaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PROJECT MILESTONE SCHEMAS
# ============================================================================

class HitoProyectoBase(BaseModel):
    proyecto_id: UUID4
    nombre: str = Field(..., max_length=150, description="Nombre del hito")
    descripcion: Optional[str] = Field(None, description="Descripción del hito")
    tipo_hito: str = Field(..., description="Tipo de hito")
    fecha_programada: date = Field(..., description="Fecha programada del hito")
    fecha_real: Optional[date] = Field(None, description="Fecha real del hito")
    completado: Optional[bool] = Field(default=False, description="¿Está completado el hito?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class HitoProyectoCreate(HitoProyectoBase):
    pass


class HitoProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_hito: Optional[str] = None
    fecha_programada: Optional[date] = None
    fecha_real: Optional[date] = None
    completado: Optional[bool] = None
    comentarios: Optional[str] = None


class HitoProyectoResponse(HitoProyectoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PROJECT ACTIVITY SCHEMAS
# ============================================================================

class ActividadProyectoBase(BaseModel):
    proyecto_id: UUID4
    empleado_id: UUID4
    tarea_id: Optional[UUID4] = Field(None, description="ID de la tarea asociada")
    descripcion: str = Field(..., description="Descripción de la actividad")
    tipo_actividad: Optional[str] = Field(None, max_length=50, description="Tipo de actividad")
    horas_invertidas: Optional[int] = Field(default=0, ge=0, description="Horas invertidas en la actividad")
    fecha_actividad: date = Field(..., description="Fecha de la actividad")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class ActividadProyectoCreate(ActividadProyectoBase):
    pass


class ActividadProyectoUpdate(BaseModel):
    proyecto_id: Optional[UUID4] = None
    empleado_id: Optional[UUID4] = None
    tarea_id: Optional[UUID4] = None
    descripcion: Optional[str] = None
    tipo_actividad: Optional[str] = Field(None, max_length=50)
    horas_invertidas: Optional[int] = Field(None, ge=0)
    fecha_actividad: Optional[date] = None
    comentarios: Optional[str] = None


class ActividadProyectoResponse(ActividadProyectoBase):
    id: UUID4
    fecha_registro: date
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True