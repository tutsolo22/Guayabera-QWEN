"""
Inventory Management Schemas: Products, categories, attributes
Specialized for textile manufacturing companies
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Any
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from enum import Enum

# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CATEGORY SCHEMAS
# ============================================================================

class CategoriaProductoTextilBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    codigo: str = Field(..., max_length=20, description="Código único de la categoría")
    parent_id: Optional[UUID] = Field(None, description="ID de la categoría padre")
    activa: bool = Field(default=True, description="¿Categoría activa?")


class CategoriaProductoTextilCreate(CategoriaProductoTextilBase):
    pass


class CategoriaProductoTextilUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, max_length=20)
    parent_id: Optional[UUID] = None
    activa: Optional[bool] = None


class CategoriaProductoTextilResponse(CategoriaProductoTextilBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TEXTILE PRODUCT SCHEMAS
# ============================================================================

class ProductoTextilBase(BaseModel):
    producto_id: UUID
    categoria_id: UUID
    categoria_producto: str = Field(..., description="Categoría del producto")
    tipo_uso: Optional[str] = Field(default="venta", description="Uso del producto")
    es_tela: Optional[bool] = Field(default=False, description="¿Es un producto de tela?")
    tipo_tela: Optional[str] = Field(None, description="Tipo de tela")
    codigo_color_pantone: Optional[str] = Field(None, max_length=20, description="Código de color Pantone")
    nombre_color_pantone: Optional[str] = Field(None, max_length=100, description="Nombre del color Pantone")
    sobrenombre_color_1: Optional[str] = Field(None, max_length=50, description="Primer sobrenombre del color")
    sobrenombre_color_2: Optional[str] = Field(None, max_length=50, description="Segundo sobrenombre del color")
    sobrenombre_color_3: Optional[str] = Field(None, max_length=50, description="Tercer sobrenombre del color")
    colores_patron: Optional[Dict[str, Any]] = Field(None, description="Colores usados en patrones")
    tipo_avio: Optional[str] = Field(None, description="Tipo de avío")
    sobrenombre_avio_1: Optional[str] = Field(None, max_length=50, description="Primer sobrenombre del avío")
    sobrenombre_avio_2: Optional[str] = Field(None, max_length=50, description="Segundo sobrenombre del avío")
    sobrenombre_avio_3: Optional[str] = Field(None, max_length=50, description="Tercer sobrenombre del avío")
    composicion: Optional[str] = Field(None, max_length=100, description="Composición del material")
    gramaje: Optional[Decimal] = Field(None, description="Gramaje del material")
    ancho: Optional[Decimal] = Field(None, description="Ancho del material")
    textura: Optional[str] = Field(None, max_length=100, description="Textura del material")
    activo: bool = Field(default=True, description="¿Producto activo?")
    comentarios: Optional[str] = Field(None, description="Comentarios del producto")


class ProductoTextilCreate(ProductoTextilBase):
    pass


class ProductoTextilUpdate(BaseModel):
    categoria_id: Optional[UUID] = None
    categoria_producto: Optional[str] = None
    tipo_uso: Optional[str] = None
    es_tela: Optional[bool] = None
    tipo_tela: Optional[str] = None
    codigo_color_pantone: Optional[str] = Field(None, max_length=20)
    nombre_color_pantone: Optional[str] = Field(None, max_length=100)
    sobrenombre_color_1: Optional[str] = Field(None, max_length=50)
    sobrenombre_color_2: Optional[str] = Field(None, max_length=50)
    sobrenombre_color_3: Optional[str] = Field(None, max_length=50)
    colores_patron: Optional[Dict[str, Any]] = None
    tipo_avio: Optional[str] = None
    sobrenombre_avio_1: Optional[str] = Field(None, max_length=50)
    sobrenombre_avio_2: Optional[str] = Field(None, max_length=50)
    sobrenombre_avio_3: Optional[str] = Field(None, max_length=50)
    composicion: Optional[str] = None
    gramaje: Optional[Decimal] = None
    ancho: Optional[Decimal] = None
    textura: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None
    comentarios: Optional[str] = None


class ProductoTextilResponse(ProductoTextilBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# LOT SCHEMAS
# ============================================================================

class LoteProductoBase(BaseModel):
    producto_textil_id: UUID
    proveedor_id: Optional[UUID] = Field(None, description="ID del proveedor")
    numero_lote: str = Field(..., max_length=50, description="Número del lote")
    fecha_elaboracion: Optional[date] = Field(None, description="Fecha de elaboración del lote")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de vencimiento del lote")
    variacion_tono: Optional[str] = Field(None, max_length=200, description="Variación de tono")
    grado_variacion: Optional[int] = Field(None, ge=1, le=10, description="Grado de variación del tono (1-10)")
    responsable_evaluacion_id: Optional[UUID] = Field(None, description="ID del responsable de evaluación")
    ubicacion_almacen: Optional[str] = Field(None, max_length=100, description="Ubicación en el almacén")
    estado: Optional[str] = Field(default="activo", description="Estado del lote")
    observaciones: Optional[str] = Field(None, description="Observaciones del lote")


class LoteProductoCreate(LoteProductoBase):
    pass


class LoteProductoUpdate(BaseModel):
    numero_lote: Optional[str] = Field(None, max_length=50)
    fecha_elaboracion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    variacion_tono: Optional[str] = Field(None, max_length=200)
    grado_variacion: Optional[int] = Field(None, ge=1, le=10)
    responsable_evaluacion_id: Optional[UUID] = None
    ubicacion_almacen: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = None
    observaciones: Optional[str] = None


class LoteProductoResponse(LoteProductoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PURCHASE RECEIPT SCHEMAS
# ============================================================================

class RecepcionCompraBase(BaseModel):
    orden_compra_id: UUID
    lote_producto_id: UUID
    responsable_recepcion_id: UUID
    folio_compra: str = Field(..., max_length=50, description="Folio de la compra")
    numero_proveedor: str = Field(..., max_length=50, description="Número del proveedor")
    cantidad_verificada: Optional[int] = Field(default=0, ge=0, description="Cantidad verificada")
    estado_recepcion: Optional[str] = Field(default="pendiente", description="Estado de la recepción")
    qr_registro: Optional[str] = Field(None, max_length=200, description="Código QR del registro")
    fecha_revision: Optional[datetime] = Field(None, description="Fecha de revisión")
    responsable_revision_id: Optional[UUID] = Field(None, description="ID del responsable de revisión")
    cantidad_aprobada: Optional[int] = Field(default=0, ge=0, description="Cantidad aprobada")
    variaciones_detectadas: Optional[str] = Field(None, description="Variaciones detectadas")
    inspeccion_calidad: Optional[str] = Field(None, description="Inspección de calidad")
    fecha_aprobacion: Optional[datetime] = Field(None, description="Fecha de aprobación")
    responsable_aprobacion_id: Optional[UUID] = Field(None, description="ID del responsable de aprobación")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class RecepcionCompraCreate(RecepcionCompraBase):
    pass


class RecepcionCompraUpdate(BaseModel):
    cantidad_verificada: Optional[int] = Field(None, ge=0)
    estado_recepcion: Optional[str] = None
    qr_registro: Optional[str] = Field(None, max_length=200)
    fecha_revision: Optional[datetime] = None
    responsable_revision_id: Optional[UUID] = None
    cantidad_aprobada: Optional[int] = Field(None, ge=0)
    variaciones_detectadas: Optional[str] = None
    inspeccion_calidad: Optional[str] = None
    fecha_aprobacion: Optional[datetime] = None
    responsable_aprobacion_id: Optional[UUID] = None
    comentarios: Optional[str] = None


class RecepcionCompraResponse(RecepcionCompraBase):
    id: UUID
    fecha_recepcion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PRODUCT SEARCH SCHEMAS
# ============================================================================

class BusquedaProductoTextil(BaseModel):
    modelo: Optional[str] = Field(None, description="Modelo del producto")
    color: Optional[str] = Field(None, description="Color del producto")
    talla: Optional[str] = Field(None, description="Talla del producto")
    almacen_id: Optional[UUID] = Field(None, description="ID del almacén")
    empresa_id: Optional[UUID] = Field(None, description="ID de la empresa (para búsquedas multiempresa)")
    categoria_producto: Optional[str] = Field(None, description="Categoría del producto")
    codigo_producto: Optional[str] = Field(None, description="Código del producto")
    nombre_producto: Optional[str] = Field(None, description="Nombre del producto")
    sobrenombre_1: Optional[str] = Field(None, description="Primer sobrenombre para búsqueda")
    sobrenombre_2: Optional[str] = Field(None, description="Segundo sobrenombre para búsqueda")


class ResultadoBusquedaProducto(BaseModel):
    producto_id: UUID
    codigo_producto: str
    nombre_producto: str
    modelo: Optional[str]
    color: Optional[str]
    talla: Optional[str]
    almacen_id: UUID
    almacen_nombre: str
    empresa_id: Optional[UUID]
    empresa_nombre: Optional[str]
    cantidad_disponible: Decimal
    categoria_producto: Optional[str]
    sobrenombre_1: Optional[str]
    sobrenombre_2: Optional[str]


class ResultadoBusquedaAvanzada(BaseModel):
    resultados: List[ResultadoBusquedaProducto]
    total_resultados: int
    almacen_solicitud: Optional[UUID] = None
    otros_almacenes_disponibles: List[Dict[str, Any]] = []


# ============================================================================
# PRODUCT LABEL SCHEMAS
# ============================================================================

class EtiquetaProductoBase(BaseModel):
    lote_producto_id: UUID
    producto_textil_id: UUID
    codigo_qr: str = Field(..., max_length=200, description="Código QR de la etiqueta")
    contenido_etiqueta: Optional[Dict[str, Any]] = Field(None, description="Contenido de la etiqueta")
    impresa: Optional[bool] = Field(default=False, description="¿Etiqueta impresa?")
    fecha_impresion: Optional[datetime] = Field(None, description="Fecha de impresión")
    responsable_impresion_id: Optional[UUID] = Field(None, description="ID del responsable de impresión")
    activa: Optional[bool] = Field(default=True, description="¿Etiqueta activa?")


class EtiquetaProductoCreate(EtiquetaProductoBase):
    pass


class EtiquetaProductoUpdate(BaseModel):
    contenido_etiqueta: Optional[Dict[str, Any]] = None
    impresa: Optional[bool] = None
    fecha_impresion: Optional[datetime] = None
    responsable_impresion_id: Optional[UUID] = None
    activa: Optional[bool] = None


class EtiquetaProductoResponse(EtiquetaProductoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS ESPECÍFICOS DE INVENTARIO
# ============================================================================

class TomaInventarioBase(BaseModel):
    almacen_id: UUID
    responsable_id: UUID
    comentarios: Optional[str] = None


class TomaInventarioCreate(TomaInventarioBase):
    pass


class TomaInventarioUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado de la toma de inventario")
    comentarios: Optional[str] = None


class TomaInventarioResponse(TomaInventarioBase):
    id: UUID
    folio: str
    fecha_toma: date
    estado: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RegistroTomaInventarioBase(BaseModel):
    toma_inventario_id: UUID
    producto_id: UUID
    cantidad_escaneada: int
    modelo: Optional[str] = None
    color: Optional[str] = None
    talla: Optional[str] = None


class RegistroTomaInventarioCreate(RegistroTomaInventarioBase):
    pass


class RegistroTomaInventarioResponse(RegistroTomaInventarioBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiferenciaInventarioBase(BaseModel):
    toma_inventario_id: UUID
    producto_id: UUID
    modelo: Optional[str] = None
    color: Optional[str] = None
    talla: Optional[str] = None
    cantidad_sistema: int
    cantidad_fisica: int
    diferencia: int
    estado: str = "pendiente"


class DiferenciaInventarioCreate(DiferenciaInventarioBase):
    pass


class DiferenciaInventarioUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado de la diferencia")


class DiferenciaInventarioResponse(DiferenciaInventarioBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MovimientoInventarioBase(BaseModel):
    tipo_movimiento: str = Field(..., description="Tipo de movimiento de inventario")
    almacen_id: UUID
    producto_id: UUID
    cantidad: int
    responsable_id: UUID
    motivo: Optional[str] = None
    referencia: Optional[str] = None


class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass


class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# UNIT OF MEASURE SCHEMAS
# ============================================================================

class UnidadMedidaBase(BaseModel):
    codigo: str = Field(..., max_length=20, description="Código único de la unidad de medida")
    nombre: str = Field(..., max_length=100, description="Nombre de la unidad de medida")
    descripcion: Optional[str] = Field(None, description="Descripción de la unidad de medida")
    abreviatura: str = Field(..., max_length=10, description="Abreviatura de la unidad de medida")
    factor_base: Optional[Decimal] = Field(default=1.0, description="Factor para convertir a unidad base")
    unidad_base_id: Optional[UUID] = Field(None, description="ID de la unidad base para conversiones")
    activa: bool = Field(default=True, description="¿Unidad de medida activa?")
    es_predeterminada: bool = Field(default=False, description="¿Es la unidad predeterminada?")


class UnidadMedidaCreate(UnidadMedidaBase):
    pass


class UnidadMedidaUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=20)
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    abreviatura: Optional[str] = Field(None, max_length=10)
    factor_base: Optional[Decimal] = None
    unidad_base_id: Optional[UUID] = None
    activa: Optional[bool] = None
    es_predeterminada: Optional[bool] = None


class UnidadMedidaResponse(UnidadMedidaBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
