"""
Asset Management Schemas: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
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
# ASSET CATEGORY SCHEMAS
# ============================================================================

class CategoriaActivoBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la categoría de activo")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    codigo: str = Field(..., max_length=30, description="Código único de la categoría")
    vida_util_anios: Optional[int] = Field(None, ge=1, description="Vida útil en años por defecto")
    metodo_depreciacion: Optional[str] = Field(None, description="Método de depreciación por defecto")
    porcentaje_residual: Optional[float] = Field(default=0.0, ge=0.0, le=100.0, description="Porcentaje residual por defecto")
    activo: bool = Field(default=True, description="¿Está activa la categoría?")


class CategoriaActivoCreate(CategoriaActivoBase):
    pass


class CategoriaActivoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    vida_util_anios: Optional[int] = Field(None, ge=1)
    metodo_depreciacion: Optional[str] = None
    porcentaje_residual: Optional[float] = Field(None, ge=0.0, le=100.0)
    activo: Optional[bool] = None


class CategoriaActivoResponse(CategoriaActivoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ASSET SCHEMAS
# ============================================================================

class ActivoBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del activo")
    nombre: str = Field(..., max_length=150, description="Nombre del activo")
    descripcion: Optional[str] = Field(None, description="Descripción del activo")
    tipo: str = Field(..., description="Tipo de activo")
    marca: Optional[str] = Field(None, max_length=100, description="Marca del activo")
    modelo: Optional[str] = Field(None, max_length=100, description="Modelo del activo")
    serie: Optional[str] = Field(None, max_length=100, description="Número de serie del activo")
    color: Optional[str] = Field(None, max_length=50, description="Color del activo")
    caracteristicas: Optional[str] = Field(None, description="Características técnicas del activo")
    ubicacion_actual: Optional[str] = Field(None, max_length=150, description="Ubicación actual del activo")
    departamento_asignado_id: Optional[UUID4] = Field(None, description="ID del departamento asignado")
    empleado_asignado_id: Optional[UUID4] = Field(None, description="ID del empleado asignado")
    categoria_id: UUID4 = Field(..., description="ID de la categoría del activo")
    fecha_adquisicion: date = Field(..., description="Fecha de adquisición del activo")
    valor_adquisicion: Decimal = Field(..., description="Valor de adquisición del activo")
    valor_actual: Optional[Decimal] = Field(None, description="Valor actual en libros del activo")
    vida_util_anios: int = Field(..., ge=1, description="Vida útil en años")
    metodo_depreciacion: str = Field(..., description="Método de depreciación")
    porcentaje_residual: Optional[float] = Field(default=0.0, ge=0.0, le=100.0, description="Porcentaje residual")
    estado: Optional[str] = Field(default="activo", description="Estado del activo")
    fecha_baja: Optional[date] = Field(None, description="Fecha de baja del activo")
    motivo_baja: Optional[str] = Field(None, max_length=200, description="Motivo de baja del activo")
    fecha_ultimo_mantenimiento: Optional[date] = Field(None, description="Fecha del último mantenimiento")
    proximo_mantenimiento: Optional[date] = Field(None, description="Fecha del próximo mantenimiento")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    imagen_url: Optional[str] = Field(None, max_length=255, description="URL de la imagen del activo")
    datos_adicionales: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales del activo")


class ActivoCreate(ActivoBase):
    pass


class ActivoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    serie: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)
    caracteristicas: Optional[str] = None
    ubicacion_actual: Optional[str] = Field(None, max_length=150)
    departamento_asignado_id: Optional[UUID4] = None
    empleado_asignado_id: Optional[UUID4] = None
    categoria_id: Optional[UUID4] = None
    fecha_adquisicion: Optional[date] = None
    valor_adquisicion: Optional[Decimal] = None
    valor_actual: Optional[Decimal] = None
    vida_util_anios: Optional[int] = Field(None, ge=1)
    metodo_depreciacion: Optional[str] = None
    porcentaje_residual: Optional[float] = Field(None, ge=0.0, le=100.0)
    estado: Optional[str] = None
    fecha_baja: Optional[date] = None
    motivo_baja: Optional[str] = Field(None, max_length=200)
    fecha_ultimo_mantenimiento: Optional[date] = None
    proximo_mantenimiento: Optional[date] = None
    comentarios: Optional[str] = None
    imagen_url: Optional[str] = Field(None, max_length=255)
    datos_adicionales: Optional[Dict[str, Any]] = None


class ActivoResponse(ActivoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ASSET MAINTENANCE SCHEMAS
# ============================================================================

class MantenimientoActivoBase(BaseModel):
    activo_id: UUID4
    tecnico_asignado_id: Optional[UUID4] = Field(None, description="ID del técnico asignado")
    tipo_mantenimiento: str = Field(..., description="Tipo de mantenimiento")
    titulo: str = Field(..., max_length=150, description="Título del mantenimiento")
    descripcion: Optional[str] = Field(None, description="Descripción del mantenimiento")
    fecha_programada: date = Field(..., description="Fecha programada del mantenimiento")
    estado: Optional[str] = Field(default="pendiente", description="Estado del mantenimiento")
    costo: Optional[Decimal] = Field(default=Decimal('0.00'), description="Costo del mantenimiento")
    proveedor_servicio_id: Optional[UUID4] = Field(None, description="ID del proveedor de servicio")
    observaciones: Optional[str] = Field(None, description="Observaciones del mantenimiento")
    repuestos_utilizados: Optional[str] = Field(None, description="Repuestos utilizados en el mantenimiento")
    proximo_mantenimiento: Optional[date] = Field(None, description="Fecha del próximo mantenimiento")
    creado_por_id: Optional[UUID4] = Field(None, description="ID del usuario que creó el registro")
    completado_por_id: Optional[UUID4] = Field(None, description="ID del usuario que completó el mantenimiento")


class MantenimientoActivoCreate(MantenimientoActivoBase):
    pass


class MantenimientoActivoUpdate(BaseModel):
    tecnico_asignado_id: Optional[UUID4] = None
    tipo_mantenimiento: Optional[str] = None
    titulo: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    fecha_programada: Optional[date] = None
    estado: Optional[str] = None
    costo: Optional[Decimal] = None
    proveedor_servicio_id: Optional[UUID4] = None
    observaciones: Optional[str] = None
    repuestos_utilizados: Optional[str] = None
    proximo_mantenimiento: Optional[date] = None
    completado_por_id: Optional[UUID4] = None


class MantenimientoActivoResponse(MantenimientoActivoBase):
    id: UUID4
    fecha_solicitud: date
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    fecha_realizacion: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ASSET DEPRECIATION SCHEMAS
# ============================================================================

class DepreciacionActivoBase(BaseModel):
    activo_id: UUID4
    anio: int = Field(..., ge=2000, le=2100, description="Año de depreciación")
    mes: int = Field(..., ge=1, le=12, description="Mes de depreciación")
    metodo: str = Field(..., description="Método de depreciación utilizado")
    valor_entrada: Decimal = Field(..., description="Valor de entrada para este período")
    depreciacion_periodo: Decimal = Field(..., description="Depreciación para este período")
    depreciacion_acumulada: Decimal = Field(..., description="Depreciación acumulada")
    valor_libros: Decimal = Field(..., description="Valor en libros después de depreciación")
    procesado: Optional[bool] = Field(default=False, description="¿Ha sido procesado en contabilidad?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class DepreciacionActivoCreate(DepreciacionActivoBase):
    pass


class DepreciacionActivoUpdate(BaseModel):
    depreciacion_periodo: Optional[Decimal] = None
    depreciacion_acumulada: Optional[Decimal] = None
    valor_libros: Optional[Decimal] = None
    procesado: Optional[bool] = None
    fecha_procesamiento: Optional[datetime] = None
    comentarios: Optional[str] = None


class DepreciacionActivoResponse(DepreciacionActivoBase):
    id: UUID4
    fecha_procesamiento: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ASSIGNMENT HISTORY SCHEMAS
# ============================================================================

class HistorialAsignacionBase(BaseModel):
    activo_id: UUID4
    empleado_anterior_id: Optional[UUID4] = Field(None, description="ID del empleado anterior")
    empleado_nuevo_id: Optional[UUID4] = Field(None, description="ID del nuevo empleado")
    departamento_anterior_id: Optional[UUID4] = Field(None, description="ID del departamento anterior")
    departamento_nuevo_id: Optional[UUID4] = Field(None, description="ID del nuevo departamento")
    ubicacion_anterior: Optional[str] = Field(None, max_length=150, description="Ubicación anterior")
    ubicacion_nueva: Optional[str] = Field(None, max_length=150, description="Nueva ubicación")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la asignación")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin de la asignación")
    motivo_cambio: Optional[str] = Field(None, max_length=200, description="Motivo del cambio")
    realizado_por_id: Optional[UUID4] = Field(None, description="ID del usuario que realizó el cambio")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class HistorialAsignacionCreate(HistorialAsignacionBase):
    pass


class HistorialAsignacionUpdate(BaseModel):
    fecha_fin: Optional[date] = None
    motivo_cambio: Optional[str] = Field(None, max_length=200)
    realizado_por_id: Optional[UUID4] = None
    comentarios: Optional[str] = None


class HistorialAsignacionResponse(HistorialAsignacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True