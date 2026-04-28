"""
Sales Models: Customers, orders, shipments, POS, inventory transfers
Specialized for textile manufacturing companies
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoCliente(enum.Enum):
    MAYOREO = "mayoreo"
    MENOREO = "menoreo"
    EMPLEADO = "empleado"
    CORPORATIVO = "corporativo"


class TipoAlmacen(enum.Enum):
    PRINCIPAL = "principal"
    PUNTO_VENTA = "punto_venta"
    PRODUCCION = "produccion"
    MATRIZ = "matriz"
    FILIAL = "filial"


class EstadoPedido(enum.Enum):
    BORRADOR = "borrador"
    AUTORIZADO = "autorizado"
    PENDIENTE_PAGO = "pendiente_pago"
    PAGADO = "pagado"
    EN_PROCESO = "en_proceso"
    PARCIALMENTE_ENVIADO = "parcialmente_enviado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class EstadoTransferencia(enum.Enum):
    SOLICITADA = "solicitada"
    AUTORIZADA = "autorizada"
    EN_TRANSITO = "en_transito"
    RECIBIDA = "recibida"
    CANCELADA = "cancelada"


class TipoMovimiento(enum.Enum):
    ENTRADA_TRANSFERENCIA = "entrada_transferencia"
    SALIDA_TRANSFERENCIA = "salida_transferencia"
    VENTA = "venta"
    DEVOLUCION_VENTA = "devolucion_venta"
    AJUSTE_POSITIVO = "ajuste_positivo"
    AJUSTE_NEGATIVO = "ajuste_negativo"


class TipoVenta(enum.Enum):
    PUNTO_VENTA = "punto_venta"
    EN_LINEA = "en_linea"
    MAYOREO = "mayoreo"
    SERVICIO = "servicio"


class MetodoPago(enum.Enum):
    EFECTIVO = "efectivo"
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA = "transferencia"
    CHEQUE = "cheque"
    CREDITO = "credito"


# ============================================================================
# CUSTOMER MANAGEMENT (GESTIÓN DE CLIENTES)
# ============================================================================

class Cliente(Base):
    """Customer management - Gestión de clientes"""
    __tablename__ = "ventas_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre_comercial = Column(String(200), nullable=False)
    razon_social = Column(String(200))
    
    # Tax information (SAT Mexico)
    rfc = Column(String(13), unique=True, nullable=False, index=True)
    regimen_fiscal = Column(String(50))
    uso_cfdi = Column(String(10), default="G03")  # Gastos en general
    
    # Contact information
    correo_electronico = Column(String(100))
    telefono = Column(String(20))
    celular = Column(String(20))
    pagina_web = Column(String(100))
    
    # Address
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    
    # Classification
    tipo_cliente = Column(SQLEnum(TipoCliente), default=TipoCliente.MENOREO)
    industria = Column(String(100))
    segmento = Column(String(50))  # premium, estandar, etc.
    
    # Financial terms
    credito_maximo = Column(Numeric(15, 2), default=0)
    dias_credito = Column(Integer, default=0)
    moneda_principal = Column(String(3), default="MXN")
    forma_pago_predeterminada = Column(SQLEnum(MetodoPago), default=MetodoPago.EFECTIVO)
    
    # Status
    activo = Column(Boolean, default=True)
    es_cliente_tambien = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    contacto_principal = Column(String(200))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    direcciones_entrega = relationship("DireccionEntrega", back_populates="cliente")
    pedidos = relationship("Pedido", back_populates="cliente")


class DireccionEntrega(Base):
    """Delivery addresses - Direcciones de entrega"""
    __tablename__ = "ventas_direccion_entrega"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"), nullable=False)
    
    # Address details
    nombre_referencia = Column(String(200), nullable=False)
    calle = Column(String(200), nullable=False)
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    telefono_contacto = Column(String(20))
    contacto_nombre = Column(String(100))
    
    # Status
    es_principal = Column(Boolean, default=False)
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    cliente = relationship("Cliente", back_populates="direcciones_entrega")


# ============================================================================
# INVENTORY AND WAREHOUSE (INVENTARIO Y ALMACÉN)
# ============================================================================

class Almacen(Base):
    """Warehouse management - Gestión de almacenes"""
    __tablename__ = "alm_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Location
    tipo = Column(SQLEnum(TipoAlmacen), nullable=False)
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    
    # Company association
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("admin_empresa.id"), nullable=False)
    sucursal_id = Column(UUID(as_uuid=True), ForeignKey("admin_sucursal.id"))
    
    # Status
    activo = Column(Boolean, default=True)
    es_principal = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    movimientos = relationship("MovimientoInventario", back_populates="almacen")
    transferencias_origen = relationship("TransferenciaInventario", 
                                       foreign_keys="TransferenciaInventario.almacen_origen_id",
                                       back_populates="almacen_origen")
    transferencias_destino = relationship("TransferenciaInventario", 
                                        foreign_keys="TransferenciaInventario.almacen_destino_id",
                                        back_populates="almacen_destino")


class MovimientoInventario(Base):
    """Inventory movements - Movimientos de inventario"""
    __tablename__ = "alm_movimiento_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Movement details
    tipo_movimiento = Column(SQLEnum(TipoMovimiento), nullable=False)
    cantidad = Column(Integer, nullable=False)
    costo_promedio = Column(Numeric(15, 4))  # Cost at the time of movement
    
    # Related documents
    documento_relacionado_tipo = Column(String(50))  # Pedido, Factura, Transferencia, etc.
    documento_relacionado_id = Column(UUID(as_uuid=True))
    
    # Status
    fecha_movimiento = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    autorizado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    almacen = relationship("Almacen", back_populates="movimientos")
    producto = relationship("Producto")
    autorizado_por = relationship("Empleado")


class TransferenciaInventario(Base):
    """Inventory transfers between warehouses - Transferencias de inventario"""
    __tablename__ = "alm_transferencia_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    almacen_origen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    almacen_destino_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Transfer details
    folio = Column(String(30), unique=True, nullable=False, index=True)
    descripcion = Column(Text)
    fecha_solicitud = Column(Date, nullable=False)
    fecha_autorizacion = Column(DateTime(timezone=True))
    fecha_envio = Column(DateTime(timezone=True))
    fecha_recepcion = Column(DateTime(timezone=True))
    
    # Status
    estado = Column(SQLEnum(EstadoTransferencia), default=EstadoTransferencia.SOLICITADA)
    
    # Metadata
    motivo_transferencia = Column(Text)
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    almacen_origen = relationship("Almacen", 
                                foreign_keys=[almacen_origen_id], 
                                back_populates="transferencias_origen")
    almacen_destino = relationship("Almacen", 
                                 foreign_keys=[almacen_destino_id], 
                                 back_populates="transferencias_destino")
    responsable = relationship("Empleado")
    detalles = relationship("DetalleTransferencia", back_populates="transferencia")


class DetalleTransferencia(Base):
    """Details of inventory transfers - Detalles de transferencias"""
    __tablename__ = "alm_detalle_transferencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transferencia_id = Column(UUID(as_uuid=True), ForeignKey("alm_transferencia_inventario.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Detail information
    cantidad_solicitada = Column(Integer, nullable=False)
    cantidad_autorizada = Column(Integer)
    cantidad_enviada = Column(Integer, default=0)
    cantidad_recibida = Column(Integer, default=0)
    costo_unitario = Column(Numeric(15, 4))
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    transferencia = relationship("TransferenciaInventario", back_populates="detalles")
    producto = relationship("Producto")


# ============================================================================
# SALES ORDERS AND POS (PEDIDOS DE VENTA Y PUNTO DE VENTA)
# ============================================================================

class Pedido(Base):
    """Sales orders - Pedidos de venta"""
    __tablename__ = "ventas_pedido"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Order details
    folio = Column(String(30), unique=True, nullable=False, index=True)
    descripcion = Column(Text)
    tipo_venta = Column(SQLEnum(TipoVenta), default=TipoVenta.PUNTO_VENTA)
    
    # Financial details
    subtotal = Column(Numeric(15, 2), default=0)
    descuento_total = Column(Numeric(15, 2), default=0)
    iva_total = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), default=0)
    
    # Dates
    fecha_pedido = Column(Date, nullable=False)
    fecha_entrega = Column(Date)
    fecha_autorizacion = Column(DateTime(timezone=True))
    
    # Status
    estado = Column(SQLEnum(EstadoPedido), default=EstadoPedido.BORRADOR)
    porcentaje_completado = Column(Numeric(5, 2), default=0.00)  # 0.00 a 100.00%
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    cliente = relationship("Cliente", back_populates="pedidos")
    almacen = relationship("Almacen")
    vendedor = relationship("Empleado")
    detalles = relationship("DetallePedido", back_populates="pedido")


class DetallePedido(Base):
    """Details of sales orders - Detalles de pedidos"""
    __tablename__ = "ventas_detalle_pedido"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("ventas_pedido.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Detail information
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(15, 2), nullable=False)
    descuento_unitario = Column(Numeric(15, 2), default=0)
    subtotal = Column(Numeric(15, 2), nullable=False)
    iva = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), nullable=False)
    
    # Tracking
    cantidad_enviada = Column(Integer, default=0)
    cantidad_facturada = Column(Integer, default=0)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto")


class Venta(Base):
    """Sales transactions - Transacciones de venta"""
    __tablename__ = "ventas_venta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("ventas_pedido.id"))
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Sale details
    folio_venta = Column(String(30), unique=True, nullable=False, index=True)
    tipo_venta = Column(SQLEnum(TipoVenta), default=TipoVenta.PUNTO_VENTA)
    
    # Financial details
    subtotal = Column(Numeric(15, 2), default=0)
    descuento_total = Column(Numeric(15, 2), default=0)
    iva_total = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), default=0)
    
    # Payment details
    metodo_pago = Column(SQLEnum(MetodoPago), default=MetodoPago.EFECTIVO)
    cambio = Column(Numeric(15, 2), default=0)
    
    # Dates
    fecha_venta = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_entrega = Column(Date)
    
    # Status
    estado = Column(String(20), default="completada")  # completada, cancelada
    
    # CFDI fields (Mexican tax receipt)
    uuid_cfdi = Column(String(36))  # UUID of the tax receipt
    folio_fiscal = Column(String(36))  # Fiscal folio number
    fecha_timbrado = Column(DateTime(timezone=True))  # Date of tax stamp
    sello_digital_cfdi = Column(Text)  # Digital seal
    cadena_original = Column(Text)  # Original string for validation
    
    # Metadata
    comentarios = Column(Text)
    archivo_xml = Column(String(500))  # Path to XML file
    archivo_pdf = Column(String(500))  # Path to PDF file
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    pedido = relationship("Pedido")
    cliente = relationship("Cliente")
    almacen = relationship("Almacen")
    vendedor = relationship("Empleado")
    pagos = relationship("Pago", back_populates="venta")


class Pago(Base):
    """Payment records - Registros de pagos"""
    __tablename__ = "ventas_pago"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venta_id = Column(UUID(as_uuid=True), ForeignKey("ventas_venta.id"), nullable=False)
    metodo_pago = Column(SQLEnum(MetodoPago), nullable=False)
    
    # Payment details
    monto = Column(Numeric(15, 2), nullable=False)
    referencia_pago = Column(String(100))  # Transaction number, check number, etc.
    
    # Status
    fecha_pago = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    estado = Column(String(20), default="completado")  # completado, pendiente, fallido
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    venta = relationship("Venta", back_populates="pagos")


# ============================================================================
# ADVANCED SEARCH (BÚSQUEDA AVANZADA)
# ============================================================================

class BusquedaAvanzada(Base):
    """Advanced search for products across warehouses - Búsqueda avanzada de productos"""
    __tablename__ = "ventas_busqueda_avanzada"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_solicitud_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    # Search details
    fecha_solicitud = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    termino_busqueda = Column(String(200), nullable=False)  # Product code, name, etc.
    
    # Results
    resultados_disponibles = Column(JSONB)  # Stores available products in other warehouses
    # Example: [{"almacen_id": "uuid", "almacen_nombre": "nombre", "cantidad": 10}, ...]
    
    # Status
    procesada = Column(Boolean, default=False)
    fecha_procesamiento = Column(DateTime(timezone=True))
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    producto = relationship("Producto")
    almacen_solicitud = relationship("Almacen")