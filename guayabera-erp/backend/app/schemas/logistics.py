"""
Logistics and Distribution Schemas: Warehouse management, shipping, and order tracking
Specialized for textile manufacturing distribution
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
# WAREHOUSE SCHEMAS
# ============================================================================

class AlmacenBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del almacén")
    nombre: str = Field(..., max_length=100, description="Nombre del almacén")
    descripcion: Optional[str] = Field(None, description="Descripción del almacén")
    direccion: str = Field(..., description="Dirección del almacén")
    ciudad: str = Field(..., max_length=100, description="Ciudad del almacén")
    estado: str = Field(..., max_length=100, description="Estado del almacén")
    pais: Optional[str] = Field(default="México", max_length=100, description="País del almacén")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del almacén")
    capacidad_maxima: Optional[Decimal] = Field(None, description="Capacidad máxima del almacén")
    coordenadas_gps: Optional[str] = Field(None, max_length=50, description="Coordenadas GPS del almacén")
    tipo_almacen: Optional[str] = Field(None, max_length=50, description="Tipo de almacén")
    temperatura_controlada: Optional[bool] = Field(default=False, description="¿Tiene temperatura controlada?")
    estado: Optional[str] = Field(default="activo", description="Estado del almacén")
    encargado_id: Optional[UUID4] = Field(None, description="ID del encargado del almacén")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class AlmacenCreate(AlmacenBase):
    pass


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    telefono: Optional[str] = Field(None, max_length=20)
    capacidad_maxima: Optional[Decimal] = None
    coordenadas_gps: Optional[str] = Field(None, max_length=50)
    tipo_almacen: Optional[str] = Field(None, max_length=50)
    temperatura_controlada: Optional[bool] = None
    estado: Optional[str] = None
    encargado_id: Optional[UUID4] = None
    comentarios: Optional[str] = None


class AlmacenResponse(AlmacenBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# WAREHOUSE LOCATION SCHEMAS
# ============================================================================

class UbicacionAlmacenBase(BaseModel):
    almacen_id: UUID4
    codigo: str = Field(..., max_length=30, description="Código de la ubicación")
    nombre: str = Field(..., max_length=100, description="Nombre de la ubicación")
    descripcion: Optional[str] = Field(None, description="Descripción de la ubicación")
    capacidad_maxima: Optional[Decimal] = Field(None, description="Capacidad máxima de la ubicación")
    coordenadas_x: Optional[int] = Field(None, description="Coordenada X en el layout del almacén")
    coordenadas_y: Optional[int] = Field(None, description="Coordenada Y en el layout del almacén")
    nivel_altura: Optional[int] = Field(None, description="Nivel de altura de la ubicación")
    tipo_ubicacion: Optional[str] = Field(None, max_length=50, description="Tipo de ubicación")
    activa: Optional[bool] = Field(default=True, description="¿Está activa la ubicación?")


class UbicacionAlmacenCreate(UbicacionAlmacenBase):
    pass


class UbicacionAlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    capacidad_maxima: Optional[Decimal] = None
    coordenadas_x: Optional[int] = None
    coordenadas_y: Optional[int] = None
    nivel_altura: Optional[int] = None
    tipo_ubicacion: Optional[str] = Field(None, max_length=50)
    activa: Optional[bool] = None


class UbicacionAlmacenResponse(UbicacionAlmacenBase):
    id: UUID4
    disponible: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVENTORY BY LOCATION SCHEMAS
# ============================================================================

class InventarioUbicacionBase(BaseModel):
    ubicacion_id: UUID4
    producto_id: UUID4
    cantidad_disponible: Optional[int] = Field(default=0, ge=0, description="Cantidad disponible")
    cantidad_reservada: Optional[int] = Field(default=0, ge=0, description="Cantidad reservada")
    cantidad_dañada: Optional[int] = Field(default=0, ge=0, description="Cantidad dañada")
    fecha_ultima_revision: Optional[date] = Field(None, description="Fecha de última revisión física")
    lote_id: Optional[UUID4] = Field(None, description="ID del lote si aplica")


class InventarioUbicacionCreate(InventarioUbicacionBase):
    pass


class InventarioUbicacionUpdate(BaseModel):
    cantidad_disponible: Optional[int] = Field(None, ge=0)
    cantidad_reservada: Optional[int] = Field(None, ge=0)
    cantidad_dañada: Optional[int] = Field(None, ge=0)
    fecha_ultima_revision: Optional[date] = None
    lote_id: Optional[UUID4] = None


class InventarioUbicacionResponse(InventarioUbicacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVENTORY MOVEMENT SCHEMAS
# ============================================================================

class MovimientoInventarioBase(BaseModel):
    almacen_id: UUID4
    producto_id: UUID4
    ubicacion_origen_id: Optional[UUID4] = Field(None, description="ID de la ubicación origen")
    ubicacion_destino_id: Optional[UUID4] = Field(None, description="ID de la ubicación destino")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable del movimiento")
    tipo_movimiento: str = Field(..., description="Tipo de movimiento")
    estado: Optional[str] = Field(default="pendiente", description="Estado del movimiento")
    cantidad: int = Field(..., gt=0, description="Cantidad del movimiento")
    referencia_documento: Optional[str] = Field(None, max_length=100, description="Referencia del documento relacionado")
    fecha_movimiento: date = Field(..., description="Fecha del movimiento")
    observaciones: Optional[str] = Field(None, description="Observaciones del movimiento")


class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass


class MovimientoInventarioUpdate(BaseModel):
    estado: Optional[str] = None
    observaciones: Optional[str] = None


class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: UUID4
    fecha_registro: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SHIPPING SCHEMAS
# ============================================================================

class EnvioBase(BaseModel):
    numero_guia: str = Field(..., max_length=50, description="Número de guía del envío")
    codigo_seguimiento: str = Field(..., max_length=30, description="Código de seguimiento")
    descripcion: Optional[str] = Field(None, description="Descripción del envío")
    venta_id: Optional[UUID4] = Field(None, description="ID de la venta relacionada")
    orden_compra_id: Optional[UUID4] = Field(None, description="ID de la orden de compra relacionada")
    metodo_envio: str = Field(..., description="Método de envío")
    estado: Optional[str] = Field(default="preparacion", description="Estado del envío")
    almacen_origen_id: UUID4 = Field(..., description="ID del almacén de origen")
    direccion_entrega: str = Field(..., description="Dirección de entrega")
    contacto_entrega: Optional[str] = Field(None, max_length=100, description="Contacto para la entrega")
    telefono_contacto: Optional[str] = Field(None, max_length=20, description="Teléfono del contacto")
    peso_total: Optional[Decimal] = Field(None, description="Peso total del envío")
    volumen_total: Optional[Decimal] = Field(None, description="Volumen total del envío")
    numero_paquetes: Optional[int] = Field(default=1, ge=1, description="Número de paquetes")
    fecha_envio: Optional[datetime] = Field(None, description="Fecha de envío")
    fecha_estimada_entrega: Optional[date] = Field(None, description="Fecha estimada de entrega")
    fecha_entrega_real: Optional[datetime] = Field(None, description="Fecha real de entrega")
    costo_envio: Optional[Decimal] = Field(None, description="Costo del envío")
    seguro: Optional[Decimal] = Field(None, description="Monto del seguro")
    empresa_envio: Optional[str] = Field(None, max_length=100, description="Empresa de envío")
    url_seguimiento: Optional[str] = Field(None, max_length=255, description="URL de seguimiento")
    firma_entrega: Optional[str] = Field(None, max_length=100, description="Firma de entrega")
    foto_entrega: Optional[str] = Field(None, max_length=255, description="Foto de entrega")
    entregado: Optional[bool] = Field(default=False, description="¿Fue entregado?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class EnvioCreate(EnvioBase):
    pass


class EnvioUpdate(BaseModel):
    estado: Optional[str] = None
    metodo_envio: Optional[str] = None
    direccion_entrega: Optional[str] = None
    contacto_entrega: Optional[str] = Field(None, max_length=100)
    telefono_contacto: Optional[str] = Field(None, max_length=20)
    peso_total: Optional[Decimal] = None
    volumen_total: Optional[Decimal] = None
    numero_paquetes: Optional[int] = Field(None, ge=1)
    fecha_envio: Optional[datetime] = None
    fecha_estimada_entrega: Optional[date] = None
    fecha_entrega_real: Optional[datetime] = None
    costo_envio: Optional[Decimal] = None
    seguro: Optional[Decimal] = None
    empresa_envio: Optional[str] = Field(None, max_length=100)
    url_seguimiento: Optional[str] = Field(None, max_length=255)
    firma_entrega: Optional[str] = Field(None, max_length=100)
    foto_entrega: Optional[str] = Field(None, max_length=255)
    entregado: Optional[bool] = None
    comentarios: Optional[str] = None


class EnvioResponse(EnvioBase):
    id: UUID4
    fecha_creacion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SHIPPING DETAILS SCHEMAS
# ============================================================================

class DetalleEnvioBase(BaseModel):
    envio_id: UUID4
    producto_id: UUID4
    cantidad: int = Field(..., gt=0, description="Cantidad del producto en el envío")
    descripcion: Optional[str] = Field(None, description="Descripción del detalle")
    lote_id: Optional[UUID4] = Field(None, description="ID del lote si aplica")


class DetalleEnvioCreate(DetalleEnvioBase):
    pass


class DetalleEnvioUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    descripcion: Optional[str] = None
    lote_id: Optional[UUID4] = None


class DetalleEnvioResponse(DetalleEnvioBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SHIPPING HISTORY SCHEMAS
# ============================================================================

class HistorialEnvioBase(BaseModel):
    envio_id: UUID4
    estado_anterior: Optional[str] = Field(None, description="Estado anterior del envío")
    estado_nuevo: str = Field(..., description="Nuevo estado del envío")
    descripcion: Optional[str] = Field(None, description="Descripción del cambio")
    ubicacion_gps: Optional[str] = Field(None, max_length=50, description="Ubicación GPS del cambio")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    usuario_id: Optional[UUID4] = Field(None, description="ID del usuario que realizó el cambio")


class HistorialEnvioCreate(HistorialEnvioBase):
    pass


class HistorialEnvioResponse(HistorialEnvioBase):
    id: UUID4
    fecha_cambio: datetime

    class Config:
        from_attributes = True