"""
Requisition Management Schemas: Purchase requisitions, approvals, and tracking
Specialized for ERP system procurement
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
# REQUISITION SCHEMAS
# ============================================================================

class RequisicionBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único de la requisición")
    titulo: str = Field(..., max_length=200, description="Título de la requisición")
    descripcion: Optional[str] = Field(None, description="Descripción de la requisición")
    tipo_requisicion: str = Field(..., description="Tipo de requisición")
    solicitante_id: UUID4 = Field(..., description="ID del empleado solicitante")
    supervisor_id: Optional[UUID4] = Field(None, description="ID del supervisor del solicitante")
    aprobador_finanzas_id: Optional[UUID4] = Field(None, description="ID del aprobador de finanzas")
    autorizado_supervisor: Optional[bool] = Field(default=False, description="¿Fue autorizado por el supervisor?")
    fecha_autorizacion_supervisor: Optional[datetime] = Field(None, description="Fecha de autorización del supervisor")
    motivo_rechazo_supervisor: Optional[str] = Field(None, description="Motivo del rechazo del supervisor")
    autorizado_finanzas: Optional[bool] = Field(default=False, description="¿Fue autorizado por finanzas?")
    fecha_autorizacion_finanzas: Optional[datetime] = Field(None, description="Fecha de autorización por finanzas")
    motivo_rechazo_finanzas: Optional[str] = Field(None, description="Motivo del rechazo por finanzas")
    estado: Optional[str] = Field(default="borrador", description="Estado de la requisición")
    fecha_solicitud: Optional[datetime] = Field(None, description="Fecha de solicitud")
    fecha_aprobacion_supervisor: Optional[datetime] = Field(None, description="Fecha de aprobación del supervisor")
    fecha_aprobacion_finanzas: Optional[datetime] = Field(None, description="Fecha de aprobación por finanzas")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento")
    subtotal: Optional[Decimal] = Field(default=Decimal('0.00'), description="Subtotal de la requisición")
    impuestos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Impuestos")
    total: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de la requisición")
    ticket_soporte_id: Optional[UUID4] = Field(None, description="ID del ticket de soporte relacionado")
    orden_compra_id: Optional[UUID4] = Field(None, description="ID de la orden de compra generada")
    activa: bool = Field(default=True, description="¿Está activa la requisición?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class RequisicionCreate(RequisicionBase):
    pass


class RequisicionUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo_requisicion: Optional[str] = None
    supervisor_id: Optional[UUID4] = None
    aprobador_finanzas_id: Optional[UUID4] = None
    autorizado_supervisor: Optional[bool] = None
    fecha_autorizacion_supervisor: Optional[datetime] = None
    motivo_rechazo_supervisor: Optional[str] = None
    autorizado_finanzas: Optional[bool] = None
    fecha_autorizacion_finanzas: Optional[datetime] = None
    motivo_rechazo_finanzas: Optional[str] = None
    estado: Optional[str] = None
    fecha_aprobacion_supervisor: Optional[datetime] = None
    fecha_aprobacion_finanzas: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    subtotal: Optional[Decimal] = None
    impuestos: Optional[Decimal] = None
    total: Optional[Decimal] = None
    ticket_soporte_id: Optional[UUID4] = None
    orden_compra_id: Optional[UUID4] = None
    activa: Optional[bool] = None
    comentarios: Optional[str] = None


class RequisicionResponse(RequisicionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REQUISITION DETAIL SCHEMAS
# ============================================================================

class DetalleRequisicionBase(BaseModel):
    requisicion_id: UUID4
    producto_id: Optional[UUID4] = Field(None, description="ID del producto relacionado")
    descripcion: str = Field(..., description="Descripción del artículo")
    cantidad: int = Field(..., ge=1, description="Cantidad solicitada")
    unidad_medida: Optional[str] = Field(default="unidad", max_length=20, description="Unidad de medida")
    precio_unitario_estimado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Precio unitario estimado")
    precio_total_estimado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Precio total estimado")


class DetalleRequisicionCreate(DetalleRequisicionBase):
    pass


class DetalleRequisicionUpdate(BaseModel):
    descripcion: Optional[str] = None
    cantidad: Optional[int] = Field(None, ge=1)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    precio_unitario_estimado: Optional[Decimal] = None
    precio_total_estimado: Optional[Decimal] = None


class DetalleRequisicionResponse(DetalleRequisicionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SUPPLIER QUOTATION SCHEMAS
# ============================================================================

class ProveedorCotizacionBase(BaseModel):
    requisicion_id: UUID4
    proveedor_id: UUID4
    archivo_cotizacion: Optional[str] = Field(None, max_length=500, description="Archivo de cotización")
    comentarios: Optional[str] = Field(None, description="Comentarios sobre la cotización")
    es_ganador: Optional[bool] = Field(default=False, description="¿Es la cotización ganadora?")
    subtotal: Optional[Decimal] = Field(default=Decimal('0.00'), description="Subtotal de la cotización")
    impuestos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Impuestos")
    total: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de la cotización")
    activa: bool = Field(default=True, description="¿Está activa la cotización?")


class ProveedorCotizacionCreate(ProveedorCotizacionBase):
    pass


class ProveedorCotizacionUpdate(BaseModel):
    archivo_cotizacion: Optional[str] = Field(None, max_length=500)
    comentarios: Optional[str] = None
    es_ganador: Optional[bool] = None
    subtotal: Optional[Decimal] = None
    impuestos: Optional[Decimal] = None
    total: Optional[Decimal] = None
    activa: Optional[bool] = None


class ProveedorCotizacionResponse(ProveedorCotizacionBase):
    id: UUID4
    fecha_envio: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# REQUISITION FORM SCHEMAS
# ============================================================================

class FormatoRequisicionBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del formato")
    descripcion: Optional[str] = Field(None, description="Descripción del formato")
    codigo: str = Field(..., max_length=30, description="Código único del formato")
    campos_formulario: Optional[Dict[str, Any]] = Field(None, description="Campos del formulario")
    campos_obligatorios: Optional[Dict[str, Any]] = Field(None, description="Campos obligatorios")
    firma_autorizacion: Optional[bool] = Field(default=True, description="¿Requiere firma de autorización?")
    activo: bool = Field(default=True, description="¿Está activo el formato?")


class FormatoRequisicionCreate(FormatoRequisicionBase):
    pass


class FormatoRequisicionUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, max_length=30)
    campos_formulario: Optional[Dict[str, Any]] = None
    campos_obligatorios: Optional[Dict[str, Any]] = None
    firma_autorizacion: Optional[bool] = None
    activo: Optional[bool] = None


class FormatoRequisicionResponse(FormatoRequisicionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True