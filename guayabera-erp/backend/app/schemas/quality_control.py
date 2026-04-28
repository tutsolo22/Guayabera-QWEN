"""
Quality Control Schemas: Quality inspections, standards, and tracking
Specialized for textile manufacturing quality control
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
# SAMPLING PLAN SCHEMAS
# ============================================================================

class PlanMuestreoBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del plan de muestreo")
    nombre: str = Field(..., max_length=100, description="Nombre del plan de muestreo")
    descripcion: Optional[str] = Field(None, description="Descripción del plan de muestreo")
    nivel_inspeccion: Optional[str] = Field(default="ii", description="Nivel de inspección (I, II, III)")
    tamano_lote_min: int = Field(..., gt=0, description="Tamaño mínimo de lote")
    tamano_lote_max: Optional[int] = Field(None, description="Tamaño máximo de lote")
    tamano_muestra: int = Field(..., gt=0, description="Tamaño de la muestra")
    numero_aceptacion: int = Field(..., ge=0, description="Número de aceptación")
    numero_rechazo: int = Field(..., gt=0, description="Número de rechazo")
    activo: bool = Field(default=True, description="¿Está activo el plan?")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable del plan")


class PlanMuestreoCreate(PlanMuestreoBase):
    pass


class PlanMuestreoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    nivel_inspeccion: Optional[str] = None
    tamano_lote_min: Optional[int] = Field(None, gt=0)
    tamano_lote_max: Optional[int] = None
    tamano_muestra: Optional[int] = Field(None, gt=0)
    numero_aceptacion: Optional[int] = Field(None, ge=0)
    numero_rechazo: Optional[int] = Field(None, gt=0)
    activo: Optional[bool] = None
    responsable_id: Optional[UUID4] = None


class PlanMuestreoResponse(PlanMuestreoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# QUALITY INSPECTION SCHEMAS
# ============================================================================

class InspeccionCalidadBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único de la inspección")
    nombre: str = Field(..., max_length=100, description="Nombre de la inspección")
    tipo_inspeccion: str = Field(..., description="Tipo de inspección")
    resultado: Optional[str] = Field(None, description="Resultado de la inspección")
    producto_id: Optional[UUID4] = Field(None, description="ID del producto inspeccionado")
    lote_id: Optional[UUID4] = Field(None, description="ID del lote inspeccionado")
    orden_produccion_id: Optional[UUID4] = Field(None, description="ID de la orden de producción")
    plan_muestreo_id: Optional[UUID4] = Field(None, description="ID del plan de muestreo utilizado")
    responsable_id: UUID4 = Field(..., description="ID del responsable de la inspección")
    tamano_lote: int = Field(..., gt=0, description="Tamaño del lote inspeccionado")
    tamano_muestra: int = Field(..., gt=0, description="Tamaño de la muestra inspeccionada")
    defectos_encontrados: Optional[int] = Field(default=0, ge=0, description="Número de defectos encontrados")
    limite_aceptacion: Optional[int] = Field(None, ge=0, description="Límite de aceptación")
    limite_rechazo: Optional[int] = Field(None, gt=0, description="Límite de rechazo")
    aceptado: Optional[bool] = Field(None, description="¿Fue aceptado el lote?")
    observaciones: Optional[str] = Field(None, description="Observaciones de la inspección")
    acciones_correctivas: Optional[str] = Field(None, description="Acciones correctivas requeridas")
    fecha_inspeccion: date = Field(..., description="Fecha de la inspección")
    activo: bool = Field(default=True, description="¿Está activa la inspección?")


class InspeccionCalidadCreate(InspeccionCalidadBase):
    pass


class InspeccionCalidadUpdate(BaseModel):
    resultado: Optional[str] = None
    tipo_inspeccion: Optional[str] = None
    producto_id: Optional[UUID4] = None
    lote_id: Optional[UUID4] = None
    orden_produccion_id: Optional[UUID4] = None
    plan_muestreo_id: Optional[UUID4] = None
    responsable_id: Optional[UUID4] = None
    tamano_lote: Optional[int] = Field(None, gt=0)
    tamano_muestra: Optional[int] = Field(None, gt=0)
    defectos_encontrados: Optional[int] = Field(None, ge=0)
    limite_aceptacion: Optional[int] = None
    limite_rechazo: Optional[int] = None
    aceptado: Optional[bool] = None
    observaciones: Optional[str] = None
    acciones_correctivas: Optional[str] = None
    fecha_inspeccion: Optional[date] = None
    activo: Optional[bool] = None


class InspeccionCalidadResponse(InspeccionCalidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DEFECT RECORD SCHEMAS
# ============================================================================

class RegistroDefectoBase(BaseModel):
    inspeccion_id: UUID4
    tipo_defecto: str = Field(..., max_length=100, description="Tipo de defecto encontrado")
    severidad: Optional[str] = Field(default="baja", max_length=20, description="Severidad del defecto")
    descripcion: Optional[str] = Field(None, description="Descripción del defecto")
    ubicacion_defecto: Optional[str] = Field(None, max_length=100, description="Ubicación donde se encontró el defecto")
    cantidad: Optional[int] = Field(default=1, ge=1, description="Cantidad de defectos encontrados")


class RegistroDefectoCreate(RegistroDefectoBase):
    pass


class RegistroDefectoUpdate(BaseModel):
    tipo_defecto: Optional[str] = Field(None, max_length=100)
    severidad: Optional[str] = Field(None, max_length=20)
    descripcion: Optional[str] = None
    ubicacion_defecto: Optional[str] = Field(None, max_length=100)
    cantidad: Optional[int] = Field(None, ge=1)


class RegistroDefectoResponse(RegistroDefectoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# QUALITY STANDARD SCHEMAS
# ============================================================================

class EstandarCalidadBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del estándar")
    nombre: str = Field(..., max_length=100, description="Nombre del estándar de calidad")
    descripcion: Optional[str] = Field(None, description="Descripción del estándar")
    categoria_producto: Optional[str] = Field(None, max_length=50, description="Categoría de producto")
    especificaciones: Optional[Dict[str, Any]] = Field(None, description="Especificaciones del estándar")
    pruebas_requeridas: Optional[Dict[str, Any]] = Field(None, description="Pruebas requeridas")
    norma_referencia: Optional[str] = Field(None, max_length=50, description="Norma de referencia")
    nivel_cumplimiento: Optional[Decimal] = Field(None, description="Nivel de cumplimiento (%)")
    activo: bool = Field(default=True, description="¿Está activo el estándar?")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable del estándar")


class EstandarCalidadCreate(EstandarCalidadBase):
    pass


class EstandarCalidadUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    categoria_producto: Optional[str] = Field(None, max_length=50)
    especificaciones: Optional[Dict[str, Any]] = None
    pruebas_requeridas: Optional[Dict[str, Any]] = None
    norma_referencia: Optional[str] = Field(None, max_length=50)
    nivel_cumplimiento: Optional[Decimal] = None
    activo: Optional[bool] = None
    responsable_id: Optional[UUID4] = None


class EstandarCalidadResponse(EstandarCalidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CERTIFICATION SCHEMAS
# ============================================================================

class CertificacionBase(BaseModel):
    numero_certificado: str = Field(..., max_length=50, description="Número del certificado")
    nombre: str = Field(..., max_length=100, description="Nombre de la certificación")
    descripcion: Optional[str] = Field(None, description="Descripción de la certificación")
    organismo_certificador: str = Field(..., max_length=100, description="Organismo certificador")
    norma_certificacion: str = Field(..., max_length=50, description="Norma de certificación")
    alcance: Optional[str] = Field(None, description="Alcance de la certificación")
    fecha_emision: date = Field(..., description="Fecha de emisión")
    fecha_vencimiento: date = Field(..., description="Fecha de vencimiento")
    estado: Optional[str] = Field(default="activa", description="Estado de la certificación")
    renovacion_requerida: Optional[bool] = Field(default=True, description="¿Requiere renovación?")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable")


class CertificacionCreate(CertificacionBase):
    pass


class CertificacionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    organismo_certificador: Optional[str] = Field(None, max_length=100)
    norma_certificacion: Optional[str] = Field(None, max_length=50)
    alcance: Optional[str] = None
    fecha_emision: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    estado: Optional[str] = None
    renovacion_requerida: Optional[bool] = None
    responsable_id: Optional[UUID4] = None


class CertificacionResponse(CertificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PRODUCT-STANDARD ASSOCIATION SCHEMAS
# ============================================================================

class ProductoEstandarBase(BaseModel):
    producto_id: UUID4
    estandar_id: UUID4
    activo: bool = Field(default=True, description="¿Está activa la asociación?")


class ProductoEstandarCreate(ProductoEstandarBase):
    pass


class ProductoEstandarUpdate(BaseModel):
    activo: Optional[bool] = None


class ProductoEstandarResponse(ProductoEstandarBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PRODUCT-CERTIFICATION ASSOCIATION SCHEMAS
# ============================================================================

class ProductoCertificacionBase(BaseModel):
    producto_id: UUID4
    certificacion_id: UUID4
    activo: bool = Field(default=True, description="¿Está activa la asociación?")


class ProductoCertificacionCreate(ProductoCertificacionBase):
    pass


class ProductoCertificacionUpdate(BaseModel):
    activo: Optional[bool] = None


class ProductoCertificacionResponse(ProductoCertificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True