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


# Nuevo enum para estados de transferencia
class EstadoTransferencia(enum.Enum):
    SOLICITADA = "solicitada"
    AUTORIZADA = "autorizada"
    EN_TRANSITO = "en_transito"
    RECIBIDA = "recibida"
    CANCELADA = "cancelada"


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
    producto_precios = relationship("ProductoPrecio", back_populates="proveedor")  # Added for sc_producto_precio


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
    # Cambiar unidad_medida de String a relación con UnidadMedida
    unidad_medida_id = Column(UUID(as_uuid=True), ForeignKey("inv_unidad_medida.id"))
    
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
    unidad_medida = relationship("UnidadMedida", back_populates="productos")
    movimientos = relationship("MovimientoInventario", back_populates="producto")
    detalles_orden = relationship("OrdenCompraDetalle", back_populates="producto")
    precios = relationship("ProductoPrecio", back_populates="producto")
    precios_compra = relationship("ProductoPrecio", back_populates="producto")  # Added for sc_producto_precio
    numeros_serie = relationship("ProductoNumeroSerie", back_populates="producto")
    lotes = relationship("ProductoLote", back_populates="producto")
    producto_textil_detalle = relationship("ProductoTextil", back_populates="producto", uselist=False, cascade="all, delete-orphan")


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
    """Modelo para precios de productos en la cadena de suministro"""
    __tablename__ = "sc_producto_precio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed to UUID to match other tables
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)  # Changed to match Producto table
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"), nullable=False)  # Changed to match Proveedor table
    precio_compra = Column(Numeric(12, 4), nullable=False)
    moneda_id = Column(UUID(as_uuid=True), ForeignKey("admin_moneda.id"))  # Changed to match Moneda table
    fecha_inicio = Column(DateTime(timezone=True), server_default=func.now())
    fecha_fin = Column(DateTime(timezone=True), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relaciones
    producto = relationship("Producto", back_populates="precios_compra")
    proveedor = relationship("Proveedor", back_populates="producto_precios")
    moneda = relationship("Moneda")


class ProductoNumeroSerie(Base):
    """Product serial numbers - Números de serie de productos"""
    __tablename__ = "alm_producto_numero_serie"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    numero_serie = Column(String(100), unique=True, nullable=False, index=True)
    numero_lote = Column(String(100), index=True)  # Optional batch number
    fecha_fabricacion = Column(Date)
    fecha_vencimiento = Column(Date)  # For products with shelf life
    
    # Status
    estado = Column(String(20), default="disponible")  # disponible, vendido, devuelto, defectuoso
    garantia_inicio = Column(Date)
    garantia_fin = Column(Date)
    
    # Location tracking
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"))
    ubicacion_detalle = Column(String(100))  # Specific location within warehouse
    
    # Metadata
    notas = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    producto = relationship("Producto", back_populates="numeros_serie")
    almacen = relationship("Almacen")


class ProductoLote(Base):
    """Product batches - Lotes de productos"""
    __tablename__ = "alm_producto_lote"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    numero_lote = Column(String(100), nullable=False, index=True)
    cantidad_total = Column(Integer, nullable=False)
    cantidad_disponible = Column(Integer, nullable=False)
    
    fecha_fabricacion = Column(Date)
    fecha_vencimiento = Column(Date)
    
    # Status
    estado = Column(String(20), default="activo")  # activo, vencido, cancelado
    
    # Metadata
    notas = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    producto = relationship("Producto", back_populates="lotes")


class Almacen(Base):
    """Warehouse management - Administración de almacenes"""
    __tablename__ = "alm_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo = Column(String(20), unique=True, nullable=False, index=True)  # ALM-001
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Location information
    direccion = Column(String(500))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    
    # Warehouse specifications
    capacidad_maxima = Column(Integer)  # Maximum capacity in units
    capacidad_utilizada = Column(Integer, default=0)
    tipo_almacen = Column(String(50))  # principal, secundario, temporal, tercerizado
    temperatura_controlada = Column(Boolean, default=False)
    humedad_controlada = Column(Boolean, default=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    ubicaciones = relationship("UbicacionAlmacen", back_populates="almacen")
    movimientos = relationship("MovimientoInventario", back_populates="almacen")


class UbicacionAlmacen(Base):
    """Warehouse location - Ubicación específica dentro de un almacén"""
    __tablename__ = "alm_ubicacion_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # EJ: A-01-01-01
    descripcion = Column(String(200))
    tipo_ubicacion = Column(String(50))  # estante, anaquel, caja, refrigerado, etc.
    capacidad_maxima = Column(Integer)  # Maximum capacity in units
    capacidad_utilizada = Column(Integer, default=0)
    activa = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    almacen = relationship("Almacen", back_populates="ubicaciones")


class MovimientoInventario(Base):
    """Inventory movements - Movimientos de inventario"""
    __tablename__ = "alm_movimiento_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Movement identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # MOV-0000001
    tipo_movimiento = Column(SQLEnum(TipoMovimientoInventario), nullable=False)
    fecha_movimiento = Column(Date, nullable=False)
    
    # Product and quantities
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    cantidad_disponible_anterior = Column(Integer, default=0)  # Available before movement
    cantidad_disponible_nueva = Column(Integer, default=0)  # Available after movement
    
    # Warehouse
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    # Related documents
    documento_tipo = Column(String(50))  # orden_compra, factura_venta, ajuste_inventario, etc.
    documento_id = Column(UUID(as_uuid=True))  # ID of the related document
    
    # Reason for movement
    motivo = Column(String(200))
    observaciones = Column(Text)
    
    # Status
    estado_documento = Column(SQLEnum(EstadoDocumento), default=EstadoDocumento.ACTIVO)
    
    # User responsible
    usuario_registro_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    producto = relationship("Producto", back_populates="movimientos")
    almacen = relationship("Almacen", back_populates="movimientos")
    usuario_registro = relationship("Usuario")


class Inventario(Base):
    """Inventory tracking - Seguimiento de inventario"""
    __tablename__ = "alm_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # INV-0000001
    nombre = Column(String(200), nullable=False)  # Nombre del inventario o ajuste
    descripcion = Column(Text)
    
    # References
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    
    # Current stock
    cantidad_existente = Column(Integer, default=0)  # Cantidad actual en inventario
    cantidad_comprometida = Column(Integer, default=0)  # Cantidad comprometida en órdenes
    cantidad_disponible = Column(Integer, default=0)  # Cantidad disponible para venta
    
    # Cost information
    costo_unitario = Column(Numeric(15, 4))
    valor_total_inventario = Column(Numeric(18, 4))
    
    # Status
    estado = Column(String(20), default="activo")  # activo, inactivo, obsoleto
    fecha_ultima_revision = Column(DateTime(timezone=True))
    
    # Metadata
    notas = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    producto = relationship("Producto")
    almacen = relationship("Almacen")


class AlmacenListaPrecios(Base):
    """Price lists for warehouses - Listas de precios para almacenes"""
    __tablename__ = "alm_lista_precios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # LP-001
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    precios_producto = relationship("ProductoPrecio", back_populates="lista_precios")


# Agregar las relaciones faltantes a otras clases
# En la clase ProductoPrecio, agregar la relación con AlmacenListaPrecios
# ProductoPrecio ya está definido anteriormente, así que actualizamos la relación:
# producto_precios = relationship("ProductoPrecio", back_populates="producto")


class OrdenCompra(Base):
    """Purchase orders - Órdenes de compra"""
    __tablename__ = "com_orden_compra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    folio = Column(String(20), unique=True, nullable=False, index=True)  # OC-0000001
    descripcion = Column(Text)
    
    # References
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"), nullable=False)
    solicitante_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Who requested the order
    
    # Status and dates
    estado = Column(SQLEnum(EstadoOrdenCompra), default=EstadoOrdenCompra.BORRADOR)
    fecha_elaboracion = Column(Date, nullable=False)
    fecha_estimada_entrega = Column(Date)
    fecha_real_entrega = Column(Date)
    
    # Financial information
    subtotal = Column(Numeric(15, 2), default=0)
    impuestos = Column(Numeric(15, 2), default=0)
    descuento = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), nullable=False)
    
    # Metadata
    moneda = Column(String(3), default="MXN")  # Currency
    condiciones_pago = Column(Text)  # Payment conditions
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    proveedor = relationship("Proveedor", back_populates="ordenes_compra")
    solicitante = relationship("Empleado")
    detalles = relationship("OrdenCompraDetalle", back_populates="orden_compra")


class OrdenCompraDetalle(Base):
    """Purchase order details - Detalles de órdenes de compra"""
    __tablename__ = "com_orden_compra_detalle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Item details
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(15, 4), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)
    impuestos = Column(Numeric(15, 2), default=0)
    descuento = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), nullable=False)
    
    # Tracking
    cantidad_recibida = Column(Integer, default=0)  # Quantity received so far
    estado_detalle = Column(String(20), default="pendiente")  # pending, partial, completed
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orden_compra = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_orden")


class RecepcionCompra(Base):
    """Purchase receipts - Recepciones de compra"""
    __tablename__ = "com_recepcion_compra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    folio = Column(String(20), unique=True, nullable=False, index=True)  # RC-0000001
    descripcion = Column(Text)
    
    # References
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"))
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    recibido_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Who received
    
    # Status
    fecha_recepcion = Column(Date, nullable=False)
    estado = Column(String(20), default="completa")  # completa, parcial, pendiente
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orden_compra = relationship("OrdenCompra")
    almacen = relationship("Almacen")
    recibido_por = relationship("Empleado", foreign_keys=[recibido_por_id])
    detalles = relationship("RecepcionCompraDetalle", back_populates="recepcion")


class RecepcionCompraDetalle(Base):
    """Purchase receipt details - Detalles de recepciones de compra"""
    __tablename__ = "com_recepcion_compra_detalle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recepcion_id = Column(UUID(as_uuid=True), ForeignKey("com_recepcion_compra.id"), nullable=False)
    orden_detalle_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra_detalle.id"))  # Related order detail
    
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    cantidad_recibida = Column(Integer, nullable=False)
    cantidad_aceptada = Column(Integer, nullable=False)  # Accepted quantity after inspection
    cantidad_rechazada = Column(Integer, default=0)  # Rejected quantity
    
    # Quality control
    inspeccion_realizada = Column(Boolean, default=False)
    resultado_inspeccion = Column(String(20))  # aceptado, rechazado, parcialmente_aceptado
    comentarios_calidad = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recepcion = relationship("RecepcionCompra", back_populates="detalles")
    orden_detalle = relationship("OrdenCompraDetalle")
    producto = relationship("Producto")


# ============================================================================
# INVENTORY TRANSFERS (TRANSFERENCIAS DE INVENTARIO)
# ============================================================================

class TransferenciaInventario(Base):
    """Inventory transfers between warehouses - Transferencias de inventario entre almacenes"""
    __tablename__ = "inv_transferencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identification
    folio = Column(String(20), unique=True, nullable=False, index=True)  # TR-0000001
    descripcion = Column(Text)
    
    # References
    almacen_origen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    almacen_destino_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    solicitante_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Who requested the transfer
    
    # Status and dates
    estado = Column(SQLEnum(EstadoTransferencia), default=EstadoTransferencia.SOLICITADA)
    fecha_solicitud = Column(Date, nullable=False)
    fecha_autorizacion = Column(Date)
    fecha_envio = Column(Date)
    fecha_recepcion = Column(Date)
    
    # Metadata
    motivo_transferencia = Column(Text)  # Reason for transfer
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    almacen_origen = relationship("Almacen", foreign_keys=[almacen_origen_id])
    almacen_destino = relationship("Almacen", foreign_keys=[almacen_destino_id])
    solicitante = relationship("Empleado")
    detalles = relationship("DetalleTransferencia", back_populates="transferencia")


class DetalleTransferencia(Base):
    """Details of inventory transfers - Detalles de transferencias de inventario"""
    __tablename__ = "inv_detalle_transferencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transferencia_id = Column(UUID(as_uuid=True), ForeignKey("inv_transferencia.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Item details
    cantidad = Column(Integer, nullable=False)
    costo_unitario = Column(Numeric(15, 4))
    subtotal = Column(Numeric(15, 2), nullable=False)
    
    # Tracking
    cantidad_transferida = Column(Integer, default=0)  # Quantity actually transferred
    cantidad_pendiente = Column(Integer, default=0)   # Quantity still pending transfer
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    transferencia = relationship("TransferenciaInventario", back_populates="detalles")
    producto = relationship("Producto")
