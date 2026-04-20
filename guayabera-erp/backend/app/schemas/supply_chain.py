"""
Supply Chain schemas for request/response validation
Purchases, Suppliers, Inventory, Warehouse
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal
from enum import Enum


# ============= ENUMS =============

class TipoProveedorEnum(str, Enum):
    NACIONAL = "nacional"
    EXTRANJERO = "extranjero"
    CLIENTE_PROVEEDOR = "cliente_proveedor"


class EstadoOrdenCompraEnum(str, Enum):
    BORRADOR = "borrador"
    AUTORIZADA = "autorizada"
    EN_PROCESO = "en_proceso"
    PARCIALMENTE_RECIBIDA = "parcialmente_recibida"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class TipoMovimientoInventarioEnum(str, Enum):
    ENTRADA_COMPRA = "entrada_compra"
    SALIDA_VENTA = "salida_venta"
    ENTRADA_DEVOLUCION = "entrada_devolucion"
    SALIDA_MERMAS = "salida_mermas"
    TRANSFERENCIA = "transferencia"
    AJUSTE_POSITIVO = "ajuste_positivo"
    AJUSTE_NEGATIVO = "ajuste_negativo"
    PRODUCCION = "produccion"


# ============= PROVEEDORES =============

class ProveedorBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre_comercial: str = Field(..., min_length=3, max_length=200)
    razon_social: Optional[str] = None
    rfc: str = Field(..., min_length=12, max_length=13)
    regimen_fiscal: Optional[str] = None
    correo_electronico: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    tipo_proveedor: TipoProveedorEnum = TipoProveedorEnum.NACIONAL
    credito_maximo: Decimal = Field(default=0, ge=0)
    dias_credito: int = Field(default=0, ge=0)
    activo: bool = True


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None
    credito_maximo: Optional[Decimal] = None
    activo: Optional[bool] = None


class ProveedorResponse(ProveedorBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ProveedorContactoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200)
    cargo: Optional[str] = None
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None
    celular: Optional[str] = None
    es_principal: bool = False


class ProveedorContactoCreate(ProveedorContactoBase):
    proveedor_id: UUID


class ProveedorContactoResponse(ProveedorContactoBase):
    id: UUID
    proveedor_id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============= PRODUCTOS =============

class ProductoBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    codigo_barras: Optional[str] = Field(None, max_length=50)
    sku: Optional[str] = Field(None, max_length=50)
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    clave_sat: Optional[str] = Field(None, max_length=20)
    clave_unidad: Optional[str] = Field(None, max_length=10)
    unidad_medida: Optional[str] = None
    familia: Optional[str] = None
    marca: Optional[str] = None
    costo_promedio: Decimal = Field(default=0, ge=0)
    precio_venta_base: Decimal = Field(default=0, ge=0)
    iva_trasladado: Decimal = Field(default=16.0, ge=0, le=100)
    stock_minimo: int = Field(default=0, ge=0)
    activo: bool = True
    es_servicio: bool = False
    requiere_numero_serie: bool = False
    requiere_lote: bool = False


class ProductoCreate(ProductoBase):
    categoria_id: Optional[UUID] = None


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio_venta_base: Optional[Decimal] = None
    costo_promedio: Optional[Decimal] = None
    stock_minimo: Optional[int] = None
    activo: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: UUID
    categoria_id: Optional[UUID] = None
    cantidad_disponible: Decimal = Field(default=0)
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class AlmacenCategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    codigo: Optional[str] = Field(None, max_length=20)
    activa: bool = True


class AlmacenCategoriaCreate(AlmacenCategoriaBase):
    categoria_padre_id: Optional[UUID] = None


class AlmacenCategoriaResponse(AlmacenCategoriaBase):
    id: UUID
    nivel: int = 1
    categoria_padre_id: Optional[UUID] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AlmacenCategoriaTree(AlmacenCategoriaResponse):
    categorias_hijas: List['AlmacenCategoriaTree'] = []
    productos: List[ProductoResponse] = []


AlmacenCategoriaTree.model_rebuild()


# ============= ALMACÉN =============

class AlmacenBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    tipo: str = "general"
    es_principal: bool = False
    activo: bool = True


class AlmacenCreate(AlmacenBase):
    sucursal_id: Optional[UUID] = None


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[bool] = None


class AlmacenResponse(AlmacenBase):
    id: UUID
    sucursal_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class InventarioBase(BaseModel):
    producto_id: UUID
    almacen_id: UUID
    cantidad_disponible: Decimal = Field(default=0, ge=0)
    cantidad_reservada: Decimal = Field(default=0, ge=0)
    costo_promedio: Decimal = Field(default=0, ge=0)


class InventarioResponse(InventarioBase):
    id: UUID
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class InventarioConDetalles(InventarioResponse):
    producto: ProductoResponse
    almacen: AlmacenResponse


class MovimientoInventarioBase(BaseModel):
    producto_id: UUID
    almacen_id: UUID
    tipo_movimiento: TipoMovimientoInventarioEnum
    cantidad: Decimal = Field(..., gt=0)
    costo_unitario: Decimal = Field(..., ge=0)
    referencia: Optional[str] = None
    notas: Optional[str] = None


class MovimientoInventarioCreate(MovimientoInventarioBase):
    documento_tipo: Optional[str] = None
    documento_id: Optional[UUID] = None


class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: UUID
    documento_tipo: Optional[str] = None
    documento_folio: Optional[str] = None
    usuario_id: Optional[UUID] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ListaPreciosBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    moneda: str = "MXN"
    es_predeterminada: bool = False
    activa: bool = True


class ListaPreciosCreate(ListaPreciosBase):
    pass


class ListaPreciosResponse(ListaPreciosBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============= ÓRDENES DE COMPRA =============

class OrdenCompraDetalleBase(BaseModel):
    producto_id: UUID
    cantidad_pedida: Decimal = Field(..., gt=0)
    costo_unitario: Decimal = Field(..., ge=0)
    descuento_porcentaje: Decimal = Field(default=0, ge=0, le=100)
    iva_porcentaje: Decimal = Field(default=16.0, ge=0, le=100)
    notas: Optional[str] = None


class OrdenCompraDetalleCreate(OrdenCompraDetalleBase):
    pass


class OrdenCompraDetalleResponse(OrdenCompraDetalleBase):
    id: UUID
    orden_compra_id: UUID
    cantidad_recibida: Decimal = Field(default=0)
    cantidad_pendiente: Decimal = Field(default=0)
    costo_total: Decimal
    descuento_importe: Decimal = Field(default=0)
    iva_importe: Decimal = Field(default=0)
    total_renglon: Decimal
    codigo_producto: Optional[str] = None
    nombre_producto: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class OrdenCompraBase(BaseModel):
    proveedor_id: UUID
    fecha_emision: date
    fecha_requerida: Optional[date] = None
    direccion_entrega: Optional[str] = None
    condiciones_pago: Optional[str] = None
    notas_internas: Optional[str] = None
    almacen_id: Optional[UUID] = None


class OrdenCompraCreate(OrdenCompraBase):
    detalles: List[OrdenCompraDetalleCreate]


class OrdenCompraUpdate(BaseModel):
    estado: Optional[EstadoOrdenCompraEnum] = None
    fecha_requerida: Optional[date] = None
    notas_internas: Optional[str] = None


class OrdenCompraResponse(OrdenCompraBase):
    id: UUID
    folio: str
    serie: Optional[str] = None
    estado: EstadoOrdenCompraEnum
    subtotal: Decimal = Field(default=0)
    descuento: Decimal = Field(default=0)
    total_iva: Decimal = Field(default=0)
    total: Decimal = Field(default=0)
    moneda: str = "MXN"
    elaboro_id: Optional[UUID] = None
    autorizo_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class OrdenCompraConDetalles(OrdenCompraResponse):
    detalles: List[OrdenCompraDetalleResponse] = []
    proveedor: ProveedorResponse


# ============= RECEPCIONES =============

class RecepcionCompraDetalleBase(BaseModel):
    producto_id: UUID
    cantidad_recibida: Decimal = Field(..., gt=0)
    lote_codigo: Optional[str] = None
    numero_serie: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    observaciones_calidad: Optional[str] = None


class RecepcionCompraDetalleCreate(RecepcionCompraDetalleBase):
    orden_detalle_id: Optional[UUID] = None


class RecepcionCompraDetalleResponse(RecepcionCompraDetalleBase):
    id: UUID
    recepcion_id: UUID
    orden_detalle_id: Optional[UUID] = None
    cantidad_aceptada: Decimal = Field(default=0)
    cantidad_rechazada: Decimal = Field(default=0)
    estado_calidad: str = "aceptado"
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RecepcionCompraBase(BaseModel):
    orden_compra_id: UUID
    almacen_id: UUID
    fecha_recepcion: date
    factura_proveedor: Optional[str] = None
    guia_remision: Optional[str] = None


class RecepcionCompraCreate(RecepcionCompraBase):
    detalles: List[RecepcionCompraDetalleCreate]


class RecepcionCompraResponse(RecepcionCompraBase):
    id: UUID
    folio: str
    serie: Optional[str] = None
    estado: str = "registrada"
    subtotal: Decimal = Field(default=0)
    total_iva: Decimal = Field(default=0)
    total: Decimal = Field(default=0)
    recibio_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class RecepcionCompraConDetalles(RecepcionCompraResponse):
    detalles: List[RecepcionCompraDetalleResponse] = []
    orden_compra: OrdenCompraResponse


# ============= DASHBOARD & REPORTS =============

class DashboardInventario(BaseModel):
    total_productos: int
    productos_activos: int
    productos_bajo_stock: int
    productos_sin_stock: int
    valor_total_inventario: Decimal
    movimientos_mes: int


class DashboardCompras(BaseModel):
    ordenes_mes: int
    ordenes_pendientes: int
    proveedores_activos: int
    compras_mes_total: Decimal
    recepciones_pendientes: int


class ReporteStockMinimo(BaseModel):
    producto_id: UUID
    producto_nombre: str
    producto_codigo: str
    almacen_id: UUID
    almacen_nombre: str
    cantidad_disponible: Decimal
    stock_minimo: int
    punto_reorden: int
    diferencia: Decimal


class ReporteMovimientosInventario(BaseModel):
    movimiento_id: UUID
    fecha: datetime
    producto_codigo: str
    producto_nombre: str
    almacen_nombre: str
    tipo_movimiento: str
    cantidad: Decimal
    costo_total: Decimal
    documento_folio: Optional[str] = None
    usuario_nombre: Optional[str] = None
