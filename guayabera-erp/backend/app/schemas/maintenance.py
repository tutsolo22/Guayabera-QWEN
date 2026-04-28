from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
import enum


class TipoMantenimiento(str, enum.Enum):
    preventivo = "preventivo"
    correctivo = "correctivo"
    predictivo = "predictivo"


class EstadoMantenimiento(str, enum.Enum):
    programado = "programado"
    en_progreso = "en_progreso"
    completado = "completado"
    cancelado = "cancelado"


class EquipoBase(BaseModel):
    nombre: str = Field(..., max_length=200)
    descripcion: Optional[str] = None
    numero_serie: Optional[str] = Field(None, max_length=100)
    fecha_adquisicion: Optional[date] = None
    proveedor_id: Optional[UUID4] = None
    ubicacion: Optional[str] = Field(None, max_length=200)
    estado: Optional[str] = Field(None, max_length=50)
    responsable_id: Optional[UUID4] = None
    activo: bool = True


class EquipoCreate(EquipoBase):
    nombre: str
    numero_serie: str


class EquipoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    proveedor_id: Optional[UUID4] = None
    ubicacion: Optional[str] = Field(None, max_length=200)
    estado: Optional[str] = Field(None, max_length=50)
    responsable_id: Optional[UUID4] = None
    activo: Optional[bool] = None


class EquipoResponse(EquipoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrdenMantenimientoBase(BaseModel):
    codigo: str = Field(..., max_length=50)
    equipo_id: UUID4
    tipo: TipoMantenimiento
    descripcion: Optional[str] = None
    fecha_solicitud: date
    fecha_programada: Optional[date] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: EstadoMantenimiento = EstadoMantenimiento.programado
    prioridad: Optional[str] = None
    responsable_id: Optional[UUID4] = None
    costo_estimado: Optional[Decimal] = None
    costo_real: Optional[Decimal] = None


class OrdenMantenimientoCreate(OrdenMantenimientoBase):
    codigo: str
    equipo_id: UUID4
    tipo: TipoMantenimiento
    fecha_solicitud: date


class OrdenMantenimientoUpdate(BaseModel):
    tipo: Optional[TipoMantenimiento] = None
    descripcion: Optional[str] = None
    fecha_programada: Optional[date] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[EstadoMantenimiento] = None
    prioridad: Optional[str] = None
    responsable_id: Optional[UUID4] = None
    costo_estimado: Optional[Decimal] = None
    costo_real: Optional[Decimal] = None


class OrdenMantenimientoResponse(OrdenMantenimientoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HistorialMantenimientoBase(BaseModel):
    orden_id: UUID4
    fecha_inicio: datetime
    fecha_fin: datetime
    descripcion_trabajo: Optional[str] = None
    repuestos_utilizados: Optional[str] = None
    horas_trabajadas: Optional[int] = None
    costo_total: Optional[Decimal] = None


class HistorialMantenimientoCreate(HistorialMantenimientoBase):
    orden_id: UUID4
    fecha_inicio: datetime
    fecha_fin: datetime


class HistorialMantenimientoUpdate(BaseModel):
    descripcion_trabajo: Optional[str] = None
    repuestos_utilizados: Optional[str] = None
    horas_trabajadas: Optional[int] = None
    costo_total: Optional[Decimal] = None


class HistorialMantenimientoResponse(HistorialMantenimientoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlanMantenimientoBase(BaseModel):
    equipo_id: UUID4
    descripcion: Optional[str] = None
    frecuencia: int  # en días
    ultimo_mantenimiento: Optional[date] = None
    proximo_mantenimiento: date
    activo: bool = True


class PlanMantenimientoCreate(PlanMantenimientoBase):
    equipo_id: UUID4
    frecuencia: int
    proximo_mantenimiento: date


class PlanMantenimientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    frecuencia: Optional[int] = None
    ultimo_mantenimiento: Optional[date] = None
    proximo_mantenimiento: Optional[date] = None
    activo: Optional[bool] = None


class PlanMantenimientoResponse(PlanMantenimientoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True