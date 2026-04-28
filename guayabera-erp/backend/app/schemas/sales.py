"""
Sales Schemas: Customers, orders, shipments, POS, inventory transfers
Specialized for textile manufacturing companies
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
# CUSTOMER SCHEMAS
# ============================================================================

class ClienteBase(BaseModel):
    codigo: str = Field(..., max_length=20, description="Código único del cliente")
    nombre_comercial: str = Field(..., max_length=200, description="Nombre comercial del cliente")
    razon_social: Optional[str] = Field(None, max_length=200, description="Razón social del cliente")
    rfc: str = Field(..., max_length=13, description="RFC del cliente")
    regimen_fiscal: Optional[str] = Field(None, max_length=50, description="Régimen fiscal SAT")
    uso_cfdi: Optional[str] = Field(default="G03", max_length=10, description="Uso CFDI")
    correo_electronico: Optional[str] = Field(None, max_length=100, description="Correo electrónico")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del cliente")
    celular: Optional[str] = Field(None, max_length=20, description="Número de celular")
    pagina_web: Optional[str] = Field(None, max_length=100, description="Página web del cliente")
    calle: Optional[str] = Field(None, max_length=200, description="Calle")
    numero_exterior: Optional[str] = Field(None, max_length=20, description="Número exterior")
    numero_interior: Optional[str] = Field(None, max_length=20, description="Número interior")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad")
    estado: Optional[str] = Field(None, max_length=100, description="Estado")
    pais: Optional[str] = Field(default="México", max_length=100, description="País")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    tipo_cliente: Optional[str] = Field(None, description="Tipo de cliente")
    industria: Optional[str] = Field(None, max_length=100, description="Industria del cliente")
    segmento: Optional[str] = Field(None, max_length=50, description="Segmento del cliente")
    credito_maximo: Optional[Decimal] = Field(default=Decimal('0'), description="Crédito máximo asignado")
    dias_credito: Optional[int] = Field(default=0, ge=0, description="Días de crédito")
    moneda_principal: Optional[str] = Field(default="MXN", max_length=3, description="Moneda principal")
    forma_pago_predeterminada: Optional[str] = Field(None, description="Forma de pago predeterminada")
    activo: bool = Field(default=True, description="¿Cliente activo?")
    es_cliente_tambien: bool = Field(default=False, description="¿También es proveedor?")
    comentarios: Optional[str] = Field(None, description="Comentarios del cliente")
    contacto_principal: Optional[str] = Field(None, max_length=200, description="Contacto principal")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_comercial: Optional[str] = Field(None, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    rfc: Optional[str] = Field(None, max_length=13)
    regimen_fiscal: Optional[str] = Field(None, max_length=50)
    uso_cfdi: Optional[str] = Field(None, max_length=10)
    correo_electronico: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    celular: Optional[str] = Field(None, max_length=20)
    pagina_web: Optional[str] = Field(None, max_length=100)
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = None
    tipo_cliente: Optional[str] = None
    industria: Optional[str] = None
    segmento: Optional[str] = None
    credito_maximo: Optional[Decimal] = None
    dias_credito: Optional[int] = Field(None, ge=0)
    moneda_principal: Optional[str] = Field(None, max_length=3)
    forma_pago_predeterminada: Optional[str] = None
    activo: Optional[bool] = None
    es_cliente_tambien: Optional[bool] = None
    comentarios: Optional[str] = None
    contacto_principal: Optional[str] = Field(None, max_length=200)


class ClienteResponse(ClienteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ADDRESS SCHEMAS
# ============================================================================

class DireccionEntregaBase(BaseModel):
    cliente_id: UUID4
    nombre_referencia: str = Field(..., max_length=200, description="Nombre de referencia para la dirección")
    calle: str = Field(..., max_length=200, description="Calle de la dirección")
    numero_exterior: Optional[str] = Field(None, max_length=20, description="Número exterior")
    numero_interior: Optional[str] = Field(None, max_length=20, description="Número interior")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad")
    estado: Optional[str] = Field(None, max_length=100, description="Estado")
    pais: Optional[str] = Field(default="México", max_length=100, description="País")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    telefono_contacto: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")
    contacto_nombre: Optional[str] = Field(None, max_length=100, description="Nombre del contacto")
    es_principal: bool = Field(default=False, description="¿Es la dirección principal?")
    activa: bool = Field(default=True, description="¿Dirección activa?")


class DireccionEntregaCreate(DireccionEntregaBase):
    pass


class DireccionEntregaUpdate(BaseModel):
    nombre_referencia: Optional[str] = Field(None, max_length=200)
    calle: Optional[str] = Field(None, max_length=200)
    numero_exterior: Optional[str] = Field(None, max_length=20)
    numero_interior: Optional[str] = Field(None, max_length=20)
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = None
    telefono_contacto: Optional[str] = None
    contacto_nombre: Optional[str] = Field(None, max_length=100)
    es_principal: Optional[bool] = None
    activa: Optional[bool] = None


class DireccionEntregaResponse(DireccionEntregaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# WAREHOUSE SCHEMAS
# ============================================================================

class AlmacenBase(BaseModel):
    codigo: str = Field(..., max_length=20, description="Código único del almacén")
    nombre: str = Field(..., max_length=100, description="Nombre del almacén")
    descripcion: Optional[str] = Field(None, description="Descripción del almacén")
    tipo: str = Field(..., description="Tipo de almacén")
    calle: Optional[str] = Field(None, max_length=200, description="Calle del almacén")
    numero_exterior: Optional[str] = Field(None, max_length=20, description="Número exterior")
    numero_interior: Optional[str] = Field(None, max_length=20, description="Número interior")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad")
    estado: Optional[str] = Field(None, max_length=100, description="Estado")
    pais: Optional[str] = Field(default="México", max_length=100, description="País")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    empresa_id: UUID4
    sucursal_id: Optional[UUID4] = Field(None, description="ID de la sucursal")
    activo: bool = Field(default=True, description="¿Almacén activo?")
    es_principal: bool = Field(default=False, description="¿Es el almacén principal?")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class AlmacenCreate(AlmacenBase):
    pass


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = None
    empresa_id: Optional[UUID4] = None
    sucursal_id: Optional[UUID4] = None
    activo: Optional[bool] = None
    es_principal: Optional[bool] = None
    comentarios: Optional[str] = None


class AlmacenResponse(AlmacenBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVENTORY MOVEMENT SCHEMAS
# ============================================================================

class MovimientoInventarioBase(BaseModel):
    almacen_id: UUID4
    producto_id: UUID4
    tipo_movimiento: str = Field(..., description="Tipo de movimiento")
    cantidad: int = Field(..., ge=1, description="Cantidad del movimiento")
    costo_promedio: Optional[Decimal] = Field(None, description="Costo promedio del producto")
    documento_relacionado_tipo: Optional[str] = Field(None, max_length=50, description="Tipo de documento relacionado")
    documento_relacionado_id: Optional[UUID4] = Field(None, description="ID del documento relacionado")
    fecha_movimiento: Optional[datetime] = Field(None, description="Fecha del movimiento")
    autorizado_por_id: Optional[UUID4] = Field(None, description="ID del empleado autorizador")
    comentarios: Optional[str] = Field(None, description="Comentarios del movimiento")


class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass


class MovimientoInventarioUpdate(BaseModel):
    tipo_movimiento: Optional[str] = None
    cantidad: Optional[int] = Field(None, ge=1)
    costo_promedio: Optional[Decimal] = None
    documento_relacionado_tipo: Optional[str] = Field(None, max_length=50)
    documento_relacionado_id: Optional[UUID4] = None
    fecha_movimiento: Optional[datetime] = None
    autorizado_por_id: Optional[UUID4] = None
    comentarios: Optional[str] = None


class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVENTORY TRANSFER SCHEMAS
# ============================================================================

class TransferenciaInventarioBase(BaseModel):
    almacen_origen_id: UUID4
    almacen_destino_id: UUID4
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable de la transferencia")
    folio: str = Field(..., max_length=30, description="Folio de la transferencia")
    descripcion: Optional[str] = Field(None, description="Descripción de la transferencia")
    fecha_solicitud: date = Field(..., description="Fecha de solicitud de la transferencia")
    fecha_autorizacion: Optional[datetime] = Field(None, description="Fecha de autorización")
    fecha_envio: Optional[datetime] = Field(None, description="Fecha de envío")
    fecha_recepcion: Optional[datetime] = Field(None, description="Fecha de recepción")
    estado: Optional[str] = Field(default="solicitada", description="Estado de la transferencia")
    motivo_transferencia: Optional[str] = Field(None, description="Motivo de la transferencia")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class TransferenciaInventarioCreate(TransferenciaInventarioBase):
    pass


class TransferenciaInventarioUpdate(BaseModel):
    responsable_id: Optional[UUID4] = None
    descripcion: Optional[str] = None
    fecha_autorizacion: Optional[datetime] = None
    fecha_envio: Optional[datetime] = None
    fecha_recepcion: Optional[datetime] = None
    estado: Optional[str] = None
    motivo_transferencia: Optional[str] = None
    comentarios: Optional[str] = None


class TransferenciaInventarioResponse(TransferenciaInventarioBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TRANSFER DETAIL SCHEMAS
# ============================================================================

class DetalleTransferenciaBase(BaseModel):
    transferencia_id: UUID4
    producto_id: UUID4
    cantidad_solicitada: int = Field(..., ge=1, description="Cantidad solicitada")
    cantidad_autorizada: Optional[int] = Field(None, ge=0, description="Cantidad autorizada")
    cantidad_enviada: Optional[int] = Field(default=0, ge=0, description="Cantidad enviada")
    cantidad_recibida: Optional[int] = Field(default=0, ge=0, description="Cantidad recibida")
    costo_unitario: Optional[Decimal] = Field(None, description="Costo unitario del producto")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class DetalleTransferenciaCreate(DetalleTransferenciaBase):
    pass


class DetalleTransferenciaUpdate(BaseModel):
    cantidad_autorizada: Optional[int] = Field(None, ge=0)
    cantidad_enviada: Optional[int] = Field(None, ge=0)
    cantidad_recibida: Optional[int] = Field(None, ge=0)
    costo_unitario: Optional[Decimal] = None
    comentarios: Optional[str] = None


class DetalleTransferenciaResponse(DetalleTransferenciaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SALES ORDER SCHEMAS
# ============================================================================

class PedidoBase(BaseModel):
    cliente_id: UUID4
    almacen_id: UUID4
    vendedor_id: Optional[UUID4] = Field(None, description="ID del vendedor")
    folio: str = Field(..., max_length=30, description="Folio del pedido")
    descripcion: Optional[str] = Field(None, description="Descripción del pedido")
    tipo_venta: Optional[str] = Field(default="punto_venta", description="Tipo de venta")
    subtotal: Optional[Decimal] = Field(default=Decimal('0'), description="Subtotal del pedido")
    descuento_total: Optional[Decimal] = Field(default=Decimal('0'), description="Descuento total")
    iva_total: Optional[Decimal] = Field(default=Decimal('0'), description="IVA total")
    total: Optional[Decimal] = Field(default=Decimal('0'), description="Total del pedido")
    fecha_pedido: date = Field(..., description="Fecha del pedido")
    fecha_entrega: Optional[date] = Field(None, description="Fecha de entrega")
    fecha_autorizacion: Optional[datetime] = Field(None, description="Fecha de autorización")
    estado: Optional[str] = Field(default="borrador", description="Estado del pedido")
    porcentaje_completado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Porcentaje completado")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    vendedor_id: Optional[UUID4] = None
    descripcion: Optional[str] = None
    tipo_venta: Optional[str] = None
    subtotal: Optional[Decimal] = None
    descuento_total: Optional[Decimal] = None
    iva_total: Optional[Decimal] = None
    total: Optional[Decimal] = None
    fecha_entrega: Optional[date] = None
    fecha_autorizacion: Optional[datetime] = None
    estado: Optional[str] = None
    porcentaje_completado: Optional[Decimal] = None
    comentarios: Optional[str] = None


class PedidoResponse(PedidoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ORDER DETAIL SCHEMAS
# ============================================================================

class DetallePedidoBase(BaseModel):
    pedido_id: UUID4
    producto_id: UUID4
    cantidad: int = Field(..., ge=1, description="Cantidad del producto")
    precio_unitario: Decimal = Field(..., description="Precio unitario")
    descuento_unitario: Optional[Decimal] = Field(default=Decimal('0'), description="Descuento unitario")
    subtotal: Decimal = Field(..., description="Subtotal del ítem")
    iva: Optional[Decimal] = Field(default=Decimal('0'), description="IVA del ítem")
    total: Decimal = Field(..., description="Total del ítem")
    cantidad_enviada: Optional[int] = Field(default=0, ge=0, description="Cantidad enviada")
    cantidad_facturada: Optional[int] = Field(default=0, ge=0, description="Cantidad facturada")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class DetallePedidoCreate(DetallePedidoBase):
    pass


class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, ge=1)
    precio_unitario: Optional[Decimal] = None
    descuento_unitario: Optional[Decimal] = None
    subtotal: Optional[Decimal] = None
    iva: Optional[Decimal] = None
    total: Optional[Decimal] = None
    cantidad_enviada: Optional[int] = Field(None, ge=0)
    cantidad_facturada: Optional[int] = Field(None, ge=0)
    comentarios: Optional[str] = None


class DetallePedidoResponse(DetallePedidoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SALE SCHEMAS
# ============================================================================

class VentaBase(BaseModel):
    pedido_id: Optional[UUID4] = Field(None, description="ID del pedido relacionado")
    cliente_id: UUID4
    almacen_id: UUID4
    vendedor_id: Optional[UUID4] = Field(None, description="ID del vendedor")
    folio_venta: str = Field(..., max_length=30, description="Folio de la venta")
    tipo_venta: Optional[str] = Field(default="punto_venta", description="Tipo de venta")
    subtotal: Optional[Decimal] = Field(default=Decimal('0'), description="Subtotal de la venta")
    descuento_total: Optional[Decimal] = Field(default=Decimal('0'), description="Descuento total")
    iva_total: Optional[Decimal] = Field(default=Decimal('0'), description="IVA total")
    total: Optional[Decimal] = Field(default=Decimal('0'), description="Total de la venta")
    metodo_pago: Optional[str] = Field(default="efectivo", description="Método de pago")
    cambio: Optional[Decimal] = Field(default=Decimal('0'), description="Cambio a devolver")
    fecha_venta: Optional[datetime] = Field(None, description="Fecha de la venta")
    fecha_entrega: Optional[date] = Field(None, description="Fecha de entrega")
    estado: Optional[str] = Field(default="completada", description="Estado de la venta")
    uuid_cfdi: Optional[str] = Field(None, max_length=36, description="UUID del CFDI")
    folio_fiscal: Optional[str] = Field(None, max_length=36, description="Folio fiscal")
    fecha_timbrado: Optional[datetime] = Field(None, description="Fecha de timbrado")
    sello_digital_cfdi: Optional[str] = Field(None, description="Sello digital CFDI")
    cadena_original: Optional[str] = Field(None, description="Cadena original")
    comentarios: Optional[str] = Field(None, description="Comentarios")
    archivo_xml: Optional[str] = Field(None, max_length=500, description="Archivo XML")
    archivo_pdf: Optional[str] = Field(None, max_length=500, description="Archivo PDF")


class VentaCreate(VentaBase):
    pass


class VentaUpdate(BaseModel):
    pedido_id: Optional[UUID4] = None
    vendedor_id: Optional[UUID4] = None
    tipo_venta: Optional[str] = None
    subtotal: Optional[Decimal] = None
    descuento_total: Optional[Decimal] = None
    iva_total: Optional[Decimal] = None
    total: Optional[Decimal] = None
    metodo_pago: Optional[str] = None
    cambio: Optional[Decimal] = None
    fecha_entrega: Optional[date] = None
    estado: Optional[str] = None
    uuid_cfdi: Optional[str] = Field(None, max_length=36)
    folio_fiscal: Optional[str] = Field(None, max_length=36)
    fecha_timbrado: Optional[datetime] = None
    sello_digital_cfdi: Optional[str] = None
    cadena_original: Optional[str] = None
    comentarios: Optional[str] = None
    archivo_xml: Optional[str] = None
    archivo_pdf: Optional[str] = None


class VentaResponse(VentaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PAYMENT SCHEMAS
# ============================================================================

class PagoBase(BaseModel):
    venta_id: UUID4
    metodo_pago: str = Field(..., description="Método de pago")
    monto: Decimal = Field(..., description="Monto del pago")
    referencia_pago: Optional[str] = Field(None, max_length=100, description="Referencia del pago")
    fecha_pago: Optional[datetime] = Field(None, description="Fecha del pago")
    estado: Optional[str] = Field(default="completado", description="Estado del pago")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    metodo_pago: Optional[str] = None
    monto: Optional[Decimal] = None
    referencia_pago: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = None
    comentarios: Optional[str] = None


class PagoResponse(PagoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ADVANCED SEARCH SCHEMAS
# ============================================================================

class BusquedaAvanzadaBase(BaseModel):
    producto_id: UUID4
    almacen_solicitud_id: UUID4
    termino_busqueda: str = Field(..., max_length=200, description="Término de búsqueda")
    resultados_disponibles: Optional[Dict[str, Any]] = Field(None, description="Resultados disponibles en otros almacenes")
    procesada: Optional[bool] = Field(default=False, description="¿Fue procesada la búsqueda?")
    fecha_procesamiento: Optional[datetime] = Field(None, description="Fecha de procesamiento")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class BusquedaAvanzadaCreate(BusquedaAvanzadaBase):
    pass


class BusquedaAvanzadaUpdate(BaseModel):
    resultados_disponibles: Optional[Dict[str, Any]] = None
    procesada: Optional[bool] = None
    fecha_procesamiento: Optional[datetime] = None
    comentarios: Optional[str] = None


class BusquedaAvanzadaResponse(BusquedaAvanzadaBase):
    id: UUID4
    fecha_solicitud: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True