from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from uuid import UUID
from enum import Enum


# Esquema para la configuración general de ventas
class SalesConfigurationBase(BaseModel):
    company_id: int
    price_update_approval_required: bool = False
    allow_manual_discounts: bool = True
    max_discount_percentage: Decimal = Field(default=Decimal("10.00"), description="Porcentaje máximo de descuento")
    enable_promotions: bool = True
    promotion_approval_required: bool = True
    enable_customer_loyalty: bool = True
    loyalty_points_per_currency: Decimal = Field(default=Decimal("1.00"), description="Puntos por unidad monetaria")
    points_to_currency_ratio: Decimal = Field(default=Decimal("0.01"), description="Valor de cada punto en unidad monetaria")
    require_sales_order_approval: bool = True
    allow_backorders: bool = True
    default_sales_terms: Optional[str] = None
    default_tax_rate: Decimal = Field(default=Decimal("16.00"), description="Tasa de impuesto predeterminada")


class SalesConfigurationCreate(SalesConfigurationBase):
    created_by: Optional[int] = None


class SalesConfigurationUpdate(BaseModel):
    price_update_approval_required: Optional[bool] = None
    allow_manual_discounts: Optional[bool] = None
    max_discount_percentage: Optional[Decimal] = Field(default=None, description="Porcentaje máximo de descuento")
    enable_promotions: Optional[bool] = None
    promotion_approval_required: Optional[bool] = None
    enable_customer_loyalty: Optional[bool] = None
    loyalty_points_per_currency: Optional[Decimal] = Field(default=None, description="Puntos por unidad monetaria")
    points_to_currency_ratio: Optional[Decimal] = Field(default=None, description="Valor de cada punto en unidad monetaria")
    require_sales_order_approval: Optional[bool] = None
    allow_backorders: Optional[bool] = None
    default_sales_terms: Optional[str] = None
    default_tax_rate: Optional[Decimal] = Field(default=None, description="Tasa de impuesto predeterminada")


class SalesConfigurationResponse(SalesConfigurationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquema para reglas de descuento
class DiscountRuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: int
    discount_type: str = "percentage"  # percentage, fixed_amount
    discount_value: Decimal
    min_quantity: int = 1
    min_amount: Decimal = Field(default=Decimal("0.00"))
    applies_to_all_products: bool = False
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True
    priority: int = 1


class DiscountRuleCreate(DiscountRuleBase):
    created_by: Optional[int] = None


class DiscountRuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    min_quantity: Optional[int] = None
    min_amount: Optional[Decimal] = None
    applies_to_all_products: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None
    priority: Optional[int] = None


class DiscountRuleResponse(DiscountRuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquema para programas de lealtad
class LoyaltyProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: int
    earning_method: str = "spending"  # spending, visits, purchases
    points_calculation: str = "percentage"  # percentage, fixed_amount
    earning_rate: Decimal
    redemption_rate: Decimal
    minimum_points_for_redemption: int = 100
    points_expire: bool = False
    points_expiry_months: int = 12
    is_active: bool = True
    is_default: bool = False


class LoyaltyProgramCreate(LoyaltyProgramBase):
    created_by: Optional[int] = None


class LoyaltyProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    earning_method: Optional[str] = None
    points_calculation: Optional[str] = None
    earning_rate: Optional[Decimal] = None
    redemption_rate: Optional[Decimal] = None
    minimum_points_for_redemption: Optional[int] = None
    points_expire: Optional[bool] = None
    points_expiry_months: Optional[int] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class LoyaltyProgramResponse(LoyaltyProgramBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquema para listas de precios
class PriceListBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_id: int
    currency: str = "MXN"
    is_active: bool = True
    is_default: bool = False
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class PriceListCreate(PriceListBase):
    created_by: Optional[int] = None


class PriceListUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class PriceListResponse(PriceListBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquema para ítems de listas de precios
class PriceListItemBase(BaseModel):
    price_list_id: int
    product_variant_id: int
    price: Decimal
    currency: str = "MXN"
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class PriceListItemCreate(PriceListItemBase):
    pass


class PriceListItemUpdate(BaseModel):
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None


class PriceListItemResponse(PriceListItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para respuestas más completas
class PriceListWithItemsResponse(PriceListResponse):
    items: List[PriceListItemResponse] = []
    
    class Config:
        from_attributes = True


# Enums para tipos de cliente y almacén
class TipoClienteEnum(str, Enum):
    MAYOREO = "mayoreo"
    MENOREO = "menoreo"
    EMPLEADO = "empleado"
    CORPORATIVO = "corporativo"


class TipoAlmacenEnum(str, Enum):
    PRINCIPAL = "principal"
    PUNTO_VENTA = "punto_venta"
    PRODUCCION = "produccion"
    MATRIZ = "matriz"
    FILIAL = "filial"


class EstadoPedidoEnum(str, Enum):
    BORRADOR = "borrador"
    AUTORIZADO = "autorizado"
    PENDIENTE_PAGO = "pendiente_pago"
    PAGADO = "pagado"
    EN_PROCESO = "en_proceso"
    PARCIALMENTE_ENVIADO = "parcialmente_enviado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class MetodoPagoEnum(str, Enum):
    EFECTIVO = "efectivo"
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"
    CREDITO = "credito"


# Esquemas para Clientes
class ClienteBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre_comercial: str = Field(..., min_length=3, max_length=200)
    razon_social: Optional[str] = None
    rfc: str = Field(..., min_length=12, max_length=13)
    regimen_fiscal: Optional[str] = None
    correo_electronico: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    tipo_cliente: TipoClienteEnum = TipoClienteEnum.MENOREO
    credito_maximo: Decimal = Field(default=0, ge=0)
    dias_credito: int = Field(default=0, ge=0)
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    correo_electronico: Optional[str] = None
    telefono: Optional[str] = None
    credito_maximo: Optional[Decimal] = None
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Direcciones de Entrega
class DireccionEntregaBase(BaseModel):
    nombre_referencia: str = Field(..., min_length=3, max_length=200)
    calle: str = Field(..., min_length=3, max_length=200)
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: str = "México"
    codigo_postal: Optional[str] = None
    telefono_contacto: Optional[str] = None
    contacto_nombre: Optional[str] = None
    es_principal: bool = False
    activa: bool = True


class DireccionEntregaCreate(DireccionEntregaBase):
    cliente_id: UUID


class DireccionEntregaUpdate(BaseModel):
    nombre_referencia: Optional[str] = None
    calle: Optional[str] = None
    es_principal: Optional[bool] = None
    activa: Optional[bool] = None


class DireccionEntregaResponse(DireccionEntregaBase):
    id: UUID
    cliente_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Almacén
class AlmacenBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=200)
    descripcion: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    tipo_almacen: str = "general"
    es_principal: bool = False
    activo: bool = True


class AlmacenCreate(AlmacenBase):
    pass


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[bool] = None


class AlmacenResponse(AlmacenBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Movimientos de Inventario
class MovimientoInventarioBase(BaseModel):
    producto_id: UUID
    almacen_id: UUID
    tipo_movimiento: str
    cantidad: int
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass


class MovimientoInventarioUpdate(BaseModel):
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


# Esquemas para Transferencias de Inventario
class TransferenciaInventarioBase(BaseModel):
    folio: str
    descripcion: Optional[str] = None
    almacen_origen_id: UUID
    almacen_destino_id: UUID
    estado: str = "solicitada"
    motivo_transferencia: Optional[str] = None


class TransferenciaInventarioCreate(TransferenciaInventarioBase):
    fecha_solicitud: date
    solicitante_id: Optional[UUID] = None


class TransferenciaInventarioUpdate(BaseModel):
    estado: Optional[str] = None
    motivo_transferencia: Optional[str] = None


class TransferenciaInventarioResponse(TransferenciaInventarioBase):
    id: UUID
    fecha_solicitud: date
    solicitante_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Detalles de Transferencia
class DetalleTransferenciaBase(BaseModel):
    transferencia_id: UUID
    producto_id: UUID
    cantidad: int
    costo_unitario: Optional[Decimal] = None


class DetalleTransferenciaCreate(DetalleTransferenciaBase):
    pass


class DetalleTransferenciaUpdate(BaseModel):
    cantidad: Optional[int] = None


class DetalleTransferenciaResponse(DetalleTransferenciaBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Pedidos
class PedidoBase(BaseModel):
    cliente_id: UUID
    almacen_id: UUID
    folio: str
    descripcion: Optional[str] = None
    subtotal: Decimal = Field(default=0)
    descuento_total: Decimal = Field(default=0)
    iva_total: Decimal = Field(default=0)
    total: Decimal = Field(default=0)
    estado: EstadoPedidoEnum = EstadoPedidoEnum.BORRADOR
    comentarios: Optional[str] = None


class PedidoCreate(PedidoBase):
    fecha_pedido: date
    vendedor_id: Optional[UUID] = None


class PedidoUpdate(BaseModel):
    estado: Optional[EstadoPedidoEnum] = None
    comentarios: Optional[str] = None


class PedidoResponse(PedidoBase):
    id: UUID
    fecha_pedido: date
    vendedor_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Detalles de Pedido
class DetallePedidoBase(BaseModel):
    pedido_id: UUID
    producto_id: UUID
    cantidad: int
    precio_unitario: Decimal
    descuento_unitario: Decimal = Field(default=0)
    subtotal: Decimal
    iva: Decimal = Field(default=0)
    total: Decimal


class DetallePedidoCreate(DetallePedidoBase):
    pass


class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int] = None
    precio_unitario: Optional[Decimal] = None


class DetallePedidoResponse(DetallePedidoBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Ventas
class VentaBase(BaseModel):
    pedido_id: Optional[UUID] = None
    cliente_id: UUID
    almacen_id: UUID
    folio_venta: str
    tipo_venta: str = "punto_venta"
    subtotal: Decimal = Field(default=0)
    descuento_total: Decimal = Field(default=0)
    iva_total: Decimal = Field(default=0)
    total: Decimal = Field(default=0)
    metodo_pago: MetodoPagoEnum = MetodoPagoEnum.EFECTIVO
    cambio: Decimal = Field(default=0)
    estado: str = "completada"
    comentarios: Optional[str] = None


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    estado: Optional[str] = None
    comentarios: Optional[str] = None


class VentaResponse(VentaBase):
    id: UUID
    fecha_venta: datetime
    uuid_cfdi: Optional[str] = None
    folio_fiscal: Optional[str] = None
    fecha_timbrado: Optional[datetime] = None
    sello_digital_cfdi: Optional[str] = None
    cadena_original: Optional[str] = None
    archivo_xml: Optional[str] = None
    archivo_pdf: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Pagos
class PagoBase(BaseModel):
    venta_id: UUID
    metodo_pago: MetodoPagoEnum
    monto: Decimal
    referencia_pago: Optional[str] = None
    estado: str = "completado"
    comentarios: Optional[str] = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    estado: Optional[str] = None
    comentarios: Optional[str] = None


class PagoResponse(PagoBase):
    id: UUID
    fecha_pago: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Esquemas para Búsqueda Avanzada
class BusquedaAvanzadaBase(BaseModel):
    producto_id: UUID
    almacen_solicitud_id: UUID
    termino_busqueda: str


class BusquedaAvanzadaCreate(BusquedaAvanzadaBase):
    pass


class BusquedaAvanzadaUpdate(BaseModel):
    procesada: Optional[bool] = None


class BusquedaAvanzadaResponse(BusquedaAvanzadaBase):
    id: UUID
    fecha_solicitud: datetime
    procesada: bool = False
    fecha_procesamiento: Optional[datetime] = None
    resultados_disponibles: Optional[dict] = None
    comentarios: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True