"""
Supply Chain Management Models: Purchases, Suppliers, Inventory, Warehouse
Inspired by CONTPAQi and Mexican business standards
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

class TipoProveedor(enum.Enum):
    NACIONAL = "nacional"
    EXTRANJERO = "extranjero"
    CLIENTE_PROVEEDOR = "cliente_proveedor"


class EstadoOrdenCompra(enum.Enum):
    BORRADOR = "borrador"
    AUTORIZADA = "autorizada"
    EN_PROCESO = "en_proceso"
    PARCIALMENTE_RECIBIDA = "parcialmente_recibida"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class TipoMovimientoInventario(enum.Enum):
    ENTRADA_COMPRA = "entrada_compra"
    SALIDA_VENTA = "salida_venta"
    ENTRADA_DEVOLUCION = "entrada_devolucion"
    SALIDA_MERMAS = "salida_mermas"
    TRANSFERENCIA = "transferencia"
    AJUSTE_POSITIVO = "ajuste_positivo"
    AJUSTE_NEGATIVO = "ajuste_negativo"
    PRODUCCION = "produccion"


class EstadoDocumento(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    CANCELADO = "cancelado"


# ============================================================================
# SUPPLIERS (PROVEEDORES)
# ============================================================================

class Proveedor(Base):
    """Supplier management - Catálogo de proveedores"""
    __tablename__ = "com_proveedor"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre_comercial = Column(String(200), nullable=False)
    razon_social = Column(String(200))
    
    # Tax information (SAT Mexico)
    rfc = Column(String(13), unique=True, nullable=False, index=True)
    regimen_fiscal = Column(String(50))
    codigo_postal = Column(String(10))
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
    codigo_postal_direccion = Column(String(10))
    
    # Classification
    tipo_proveedor = Column(SQLEnum(TipoProveedor), default=TipoProveedor.NACIONAL)
    industria = Column(String(100))
    segmento = Column(String(50))  # mayorista, minorista, fabricante
    
    # Financial terms
    credito_maximo = Column(Numeric(15, 2), default=0)
    dias_credito = Column(Integer, default=0)
    moneda_principal = Column(String(3), default="MXN")
    
    # Status
    activo = Column(Boolean, default=True)
    es_cliente_tambien = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    contacto_principal = Column(String(200))
    lista_precios_id = Column(UUID(as_uuid=True), ForeignKey("alm_lista_precios.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    ordenes_compra = relationship("OrdenCompra", back_populates="proveedor")
    contactos = relationship("ProveedorContacto", back_populates="proveedor")


class ProveedorContacto(Base):
    """Supplier contacts - Contactos de proveedor"""
    __tablename__ = "com_proveedor_contacto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"), nullable=False)
    
    nombre = Column(String(200), nullable=False)
    cargo = Column(String(100))
    departamento = Column(String(100))
    
    correo_electronico = Column(String(100))
    telefono = Column(String(20))
    celular = Column(String(20))
    
    es_principal = Column(Boolean, default=False)
    notas = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    proveedor = relationship("Proveedor", back_populates="contactos")


# ============================================================================
# PRODUCTS (PRODUCTOS)
# ============================================================================

class Producto(Base):
    """Product catalog - Catálogo de productos"""
    __tablename__ = "alm_producto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    codigo_barras = Column(String(50), unique=True, index=True)
    sku = Column(String(50), unique=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    descripcion_corta = Column(String(500))
    
    # SAT Mexico - CFDI
    clave_sat = Column(String(20))  # ClaveProdServ del SAT
    clave_unidad = Column(String(10))  # ClaveUnidad del SAT
    unidad_medida = Column(String(50))
    
    # Classification
    familia = Column(String(100))
    linea = Column(String(100))
    marca = Column(String(100))
    modelo = Column(String(100))
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("alm_categoria.id"))
    
    # Pricing
    costo_promedio = Column(Numeric(15, 4), default=0)
    costo_ultimo = Column(Numeric(15, 4), default=0)
    precio_venta_base = Column(Numeric(15, 2), default=0)
    margen_ganancia = Column(Numeric(5, 2), default=0)  # Percentage
    iva_trasladado = Column(Numeric(5, 2), default=16.0)
    ieva_retenido = Column(Numeric(5, 2), default=0)
    
    # Inventory control
    tipo_inventario = Column(String(20), default="permanente")  # permanente, manual
    stock_minimo = Column(Integer, default=0)
    stock_maximo = Column(Integer, default=0)
    punto_reorden = Column(Integer, default=0)
    multiplo_compra = Column(Integer, default=1)
    
    # Physical characteristics
    peso = Column(Numeric(10, 3))
    volumen = Column(Numeric(10, 3))
    altura = Column(Numeric(10, 2))
    ancho = Column(Numeric(10, 2))
    profundidad = Column(Numeric(10, 2))
    unidad_peso = Column(String(10), default="kg")
    
    # Status
    activo = Column(Boolean, default=True)
    es_servicio = Column(Boolean, default=False)
    es_kit = Column(Boolean, default=False)
    requiere_numero_serie = Column(Boolean, default=False)
    requiere_lote = Column(Boolean, default=False)
    
    # Manufacturing
    es_producido = Column(Boolean, default=False)
    tiempo_produccion_dias = Column(Integer, default=0)
    
    # Metadata
    imagen_url = Column(String(500))
    ubicacion_almacen = Column(String(100))
    notas = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    categoria = relationship("AlmacenCategoria", back_populates="productos")
    movimientos = relationship("MovimientoInventario", back_populates="producto")
    detalles_orden = relationship("OrdenCompraDetalle", back_populates="producto")
    precios = relationship("ProductoPrecio", back_populates="producto")
    numeros_serie = relationship("ProductoNumeroSerie", back_populates="producto")
    lotes = relationship("ProductoLote", back_populates="producto")


class AlmacenCategoria(Base):
    """Product categories - Categorías de productos"""
    __tablename__ = "alm_categoria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(20), unique=True)
    
    nivel = Column(Integer, default=1)
    categoria_padre_id = Column(UUID(as_uuid=True), ForeignKey("alm_categoria.id"))
    
    activa = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    categoria_padre = relationship("AlmacenCategoria", remote_side=[id], backref="categorias_hijas")
    productos = relationship("Producto", back_populates="categoria")


class ProductoPrecio(Base):
    """Product pricing by price list - Precios por lista"""
    __tablename__ = "alm_producto_precio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    lista_precios_id = Column(UUID(as_uuid=True), ForeignKey("alm_lista_precios.id"), nullable=False)
    
    precio = Column(Numeric(15, 2), nullable=False)
    costo = Column(Numeric(15, 4))
    
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    
    activa = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    producto = relationship("Producto", back_populates="precios")
    lista_precios = relationship("AlmacenListaPrecios", back_populates="productos")


class ProductoNumeroSerie(Base):
    """Serial number tracking - Control de números de serie"""
    __tablename__ = "alm_producto_numero_serie"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    numero_serie = Column(String(100), nullable=False, index=True)
    fecha_fabricacion = Column(Date)
    fecha_vencimiento = Column(Date)
    
    estado = Column(String(20), default="disponible")  # disponible, vendido, en_garantia, etc.
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    producto = relationship("Producto", back_populates="numeros_serie")
    almacen = relationship("Almacen", back_populates="numeros_serie")


class ProductoLote(Base):
    """Batch/Lot tracking - Control de lotes"""
    __tablename__ = "alm_producto_lote"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    codigo_lote = Column(String(50), nullable=False, index=True)
    cantidad_disponible = Column(Numeric(15, 3), default=0)
    cantidad_reservada = Column(Numeric(15, 3), default=0)
    
    fecha_fabricacion = Column(Date)
    fecha_vencimiento = Column(Date)
    fecha_recepcion = Column(Date)
    
    estado = Column(String(20), default="disponible")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    producto = relationship("Producto", back_populates="lotes")
    almacen = relationship("Almacen", back_populates="lotes")


# ============================================================================
# WAREHOUSE (ALMACÉN)
# ============================================================================

class Almacen(Base):
    """Warehouse management - Gestión de almacenes"""
    __tablename__ = "alm_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Address
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    
    # Configuration
    tipo = Column(String(50), default="general")  # general, sucursal, bodega, virtual
    es_principal = Column(Boolean, default=False)
    permite_costos_negativos = Column(Boolean, default=False)
    permite_ventas_sin_stock = Column(Boolean, default=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    responsable = Column(String(200))
    telefono = Column(String(20))
    correo_electronico = Column(String(100))
    notas = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    sucursal_id = Column(UUID(as_uuid=True), ForeignKey("adm_sucursal.id"))
    inventarios = relationship("Inventario", back_populates="almacen")
    movimientos = relationship("MovimientoInventario", back_populates="almacen")
    numeros_serie = relationship("ProductoNumeroSerie", back_populates="almacen")
    lotes = relationship("ProductoLote", back_populates="almacen")


class Inventario(Base):
    """Current inventory levels - Niveles de inventario actual"""
    __tablename__ = "alm_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    cantidad_disponible = Column(Numeric(15, 3), default=0)
    cantidad_reservada = Column(Numeric(15, 3), default=0)
    cantidad_en_transito = Column(Numeric(15, 3), default=0)
    cantidad_pedida = Column(Numeric(15, 3), default=0)
    
    costo_promedio = Column(Numeric(15, 4), default=0)
    ultimo_costo = Column(Numeric(15, 4), default=0)
    
    # For serialized/lot tracked items
    tiene_numeros_serie = Column(Boolean, default=False)
    tiene_lotes = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        CheckConstraint('cantidad_disponible >= 0', name='check_cantidad_disponible'),
    )
    
    producto = relationship("Producto", back_populates="inventarios")
    almacen = relationship("Almacen", back_populates="inventarios")


class MovimientoInventario(Base):
    """Inventory movement history - Historial de movimientos de inventario"""
    __tablename__ = "alm_movimiento_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    tipo_movimiento = Column(SQLEnum(TipoMovimientoInventario), nullable=False)
    cantidad = Column(Numeric(15, 3), nullable=False)
    costo_unitario = Column(Numeric(15, 4), nullable=False)
    costo_total = Column(Numeric(15, 2), nullable=False)
    
    # Reference documents
    documento_tipo = Column(String(50))  # orden_compra, venta, ajuste, etc.
    documento_id = Column(UUID(as_uuid=True))
    documento_folio = Column(String(50))
    
    # Additional info
    referencia = Column(String(200))
    notas = Column(Text)
    
    # For serialized/lot items
    numero_serie = Column(String(100))
    lote_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto_lote.id"))
    
    # User tracking
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    producto = relationship("Producto", back_populates="movimientos")
    almacen = relationship("Almacen", back_populates="movimientos")
    lote = relationship("ProductoLote", back_populates="movimientos")


class AlmacenListaPrecios(Base):
    """Price lists - Listas de precios"""
    __tablename__ = "alm_lista_precios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    moneda = Column(String(3), default="MXN")
    tipo_impuesto = Column(String(20), default="iva")
    
    es_predeterminada = Column(Boolean, default=False)
    activa = Column(Boolean, default=True)
    
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    
    creada_por_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    productos = relationship("ProductoPrecio", back_populates="lista_precios")


# ============================================================================
# PURCHASE ORDERS (ÓRDENES DE COMPRA)
# ============================================================================

class OrdenCompra(Base):
    """Purchase orders - Órdenes de compra"""
    __tablename__ = "com_orden_compra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document identification
    folio = Column(String(50), unique=True, nullable=False)
    serie = Column(String(10))
    
    # Supplier
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"), nullable=False)
    
    # Dates
    fecha_emision = Column(Date, nullable=False)
    fecha_requerida = Column(Date)
    fecha_entrega_estimada = Column(Date)
    fecha_recepcion = Column(Date)
    
    # Status
    estado = Column(SQLEnum(EstadoOrdenCompra), default=EstadoOrdenCompra.BORRADOR)
    
    # Financial
    subtotal = Column(Numeric(15, 2), default=0)
    descuento = Column(Numeric(15, 2), default=0)
    total_iva = Column(Numeric(15, 2), default=0)
    total_ieps = Column(Numeric(15, 2), default=0)
    total_retenciones = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), default=0)
    
    moneda = Column(String(3), default="MXN")
    tipo_cambio = Column(Numeric(10, 4), default=1)
    
    # Shipping
    direccion_entrega = Column(Text)
    instrucciones_entrega = Column(Text)
    metodo_envio = Column(String(100))
    
    # Payment terms
    condiciones_pago = Column(String(200))
    forma_pago = Column(String(50))
    
    # CFDI (SAT Mexico)
    uso_cfdi = Column(String(10))
    metodo_pago_sat = Column(String(20))
    
    # Tracking
    notas_internas = Column(Text)
    notas_publicas = Column(Text)
    
    # User tracking
    elaboro_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    autorizo_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    recibio_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    # Sucursal
    sucursal_id = Column(UUID(as_uuid=True), ForeignKey("adm_sucursal.id"))
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    canceled_at = Column(DateTime(timezone=True))
    
    # Relationships
    proveedor = relationship("Proveedor", back_populates="ordenes_compra")
    detalles = relationship("OrdenCompraDetalle", back_populates="orden_compra", cascade="all, delete-orphan")
    recepciones = relationship("RecepcionCompra", back_populates="orden_compra")


class OrdenCompraDetalle(Base):
    """Purchase order line items - Detalle de órdenes de compra"""
    __tablename__ = "com_orden_compra_detalle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    cantidad_pedida = Column(Numeric(15, 3), nullable=False)
    cantidad_recibida = Column(Numeric(15, 3), default=0)
    cantidad_pendiente = Column(Numeric(15, 3), default=0)
    
    costo_unitario = Column(Numeric(15, 4), nullable=False)
    costo_total = Column(Numeric(15, 2), nullable=False)
    
    descuento_porcentaje = Column(Numeric(5, 2), default=0)
    descuento_importe = Column(Numeric(15, 2), default=0)
    
    iva_porcentaje = Column(Numeric(5, 2), default=16.0)
    iva_importe = Column(Numeric(15, 2), default=0)
    
    ieps_porcentaje = Column(Numeric(5, 2), default=0)
    ieps_importe = Column(Numeric(15, 2), default=0)
    
    total_renglon = Column(Numeric(15, 2), nullable=False)
    
    # Product info snapshot
    codigo_producto = Column(String(50))
    nombre_producto = Column(String(200))
    unidad_medida = Column(String(50))
    
    # Delivery
    fecha_entrega_estimada = Column(Date)
    notas = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    orden_compra = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_orden")


class RecepcionCompra(Base):
    """Purchase receipt - Recepción de compras"""
    __tablename__ = "com_recepcion_compra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    folio = Column(String(50), unique=True, nullable=False)
    serie = Column(String(10))
    
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    fecha_recepcion = Column(Date, nullable=False)
    
    # Document references
    factura_proveedor = Column(String(100))
    guia_remision = Column(String(100))
    
    # Status
    estado = Column(String(20), default="registrada")  # registrada, cancelada
    
    # Totals
    subtotal = Column(Numeric(15, 2), default=0)
    total_iva = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), default=0)
    
    # User tracking
    recibio_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    canceled_at = Column(DateTime(timezone=True))
    
    orden_compra = relationship("OrdenCompra", back_populates="recepciones")
    detalles = relationship("RecepcionCompraDetalle", back_populates="recepcion", cascade="all, delete-orphan")


class RecepcionCompraDetalle(Base):
    """Purchase receipt line items - Detalle de recepción"""
    __tablename__ = "com_recepcion_compra_detalle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recepcion_id = Column(UUID(as_uuid=True), ForeignKey("com_recepcion_compra.id"), nullable=False)
    orden_detalle_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra_detalle.id"))
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    cantidad_recibida = Column(Numeric(15, 3), nullable=False)
    cantidad_aceptada = Column(Numeric(15, 3), default=0)
    cantidad_rechazada = Column(Numeric(15, 3), default=0)
    
    costo_unitario = Column(Numeric(15, 4))
    costo_total = Column(Numeric(15, 2))
    
    # Lot/Serial tracking
    lote_codigo = Column(String(50))
    numero_serie = Column(String(100))
    fecha_vencimiento = Column(Date)
    
    # Quality control
    estado_calidad = Column(String(20), default="aceptado")
    observaciones_calidad = Column(Text)
    
    movimiento_inventario_id = Column(UUID(as_uuid=True), ForeignKey("alm_movimiento_inventario.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    recepcion = relationship("RecepcionCompra", back_populates="detalles")


# Add back-references to Product model
Producto.inventarios = relationship("Inventario", back_populates="producto")
