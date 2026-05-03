"""
Logistics and Distribution Models: Warehouse management, shipping, and order tracking
Specialized for textile manufacturing distribution
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

class EstadoAlmacen(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    MANTENIMIENTO = "mantenimiento"
    CERRADO = "cerrado"


class TipoMovimientoInventario(enum.Enum):
    ENTRADA = "entrada"
    SALIDA = "salida"
    AJUSTE_POSITIVO = "ajuste_positivo"
    AJUSTE_NEGATIVO = "ajuste_negativo"
    TRASPASO_ENTRADA = "traspaso_entrada"
    TRASPASO_SALIDA = "traspaso_salida"


class EstadoMovimiento(enum.Enum):
    PENDIENTE = "pendiente"
    PROCESADO = "procesado"
    CANCELADO = "cancelado"


class EstadoEnvio(enum.Enum):
    PREPARACION = "preparacion"
    EMPAQUETADO = "empaquetado"
    EN_TRANSITO = "en_transito"
    ENTREGADO = "entregado"
    DEVUELTO = "devuelto"
    CANCELADO = "cancelado"


class MetodoEnvio(enum.Enum):
    PAQUETERIA = "paqueteria"
    TRANSPORTE_LOCAL = "transporte_local"
    ENTREGA_DIRECTA = "entrega_directa"
    PICKUP_TIENDA = "pickup_tienda"


# ============================================================================
# LOGISTICS AND DISTRIBUTION MODELS
# ============================================================================

class Almacen(Base):
    """Warehouse management - Gestión de almacenes"""
    __tablename__ = "log_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Warehouse identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # WH-001, MX-CDMX-PRIN
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Location and contact
    direccion = Column(Text, nullable=False)
    ciudad = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    telefono = Column(String(20))
    
    # Characteristics
    capacidad_maxima = Column(Numeric(12, 2))  # Maximum capacity in cubic meters or units
    coordenadas_gps = Column(String(50))  # GPS coordinates
    tipo_almacen = Column(String(50))  # primario, secundario, temporal, crossdock
    temperatura_controlada = Column(Boolean, default=False)
    
    # Status
    estado = Column(SQLEnum(EstadoAlmacen), default=EstadoAlmacen.ACTIVO)
    
    # Management
    encargado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Warehouse manager
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    encargado = relationship("Empleado")
    ubicaciones = relationship("UbicacionAlmacen", back_populates="almacen")
    movimientos = relationship("MovimientoInventario", back_populates="almacen")


class UbicacionAlmacen(Base):
    """Warehouse location/bin - Ubicación/ubicación dentro del almacén"""
    __tablename__ = "log_ubicacion_almacen"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("log_almacen.id"), nullable=False)
    
    # Location identification
    codigo = Column(String(30), nullable=False)  # A-01-01, EST-05, etc.
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Characteristics
    capacidad_maxima = Column(Numeric(10, 2))  # Maximum capacity for this location
    coordenadas_x = Column(Integer)  # X coordinate in warehouse layout
    coordenadas_y = Column(Integer)  # Y coordinate in warehouse layout
    nivel_altura = Column(Integer)  # Height level (1st floor, 2nd floor, etc.)
    tipo_ubicacion = Column(String(50))  # estanteria, paleta, crossdock, etc.
    
    # Status
    activa = Column(Boolean, default=True)
    disponible = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    almacen = relationship("Almacen", back_populates="ubicaciones")
    inventarios = relationship("InventarioUbicacion", back_populates="ubicacion")


class InventarioUbicacion(Base):
    """Inventory by location - Inventario por ubicación"""
    __tablename__ = "log_inventario_ubicacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ubicacion_id = Column(UUID(as_uuid=True), ForeignKey("log_ubicacion_almacen.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Inventory quantities
    cantidad_disponible = Column(Integer, default=0)
    cantidad_reservada = Column(Integer, default=0)  # Reserved for orders
    cantidad_dañada = Column(Integer, default=0)  # Damaged goods
    
    # Tracking
    fecha_ultima_revision = Column(Date)  # Last physical verification
    lote_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto_lote.id"))  # Batch if applicable
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ubicacion = relationship("UbicacionAlmacen", back_populates="inventarios")
    producto = relationship("Producto")
    lote = relationship("ProductoLote")


class MovimientoInventario(Base):
    """Inventory movement - Movimiento de inventario"""
    __tablename__ = "log_movimiento_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("log_almacen.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    ubicacion_origen_id = Column(UUID(as_uuid=True), ForeignKey("log_ubicacion_almacen.id"))  # For transfers
    ubicacion_destino_id = Column(UUID(as_uuid=True), ForeignKey("log_ubicacion_almacen.id"))  # For transfers
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Person responsible
    
    # Movement details
    tipo_movimiento = Column(SQLEnum(TipoMovimientoInventario), nullable=False)
    estado = Column(SQLEnum(EstadoMovimiento), default=EstadoMovimiento.PENDIENTE)
    cantidad = Column(Integer, nullable=False)
    referencia_documento = Column(String(100))  # Reference to related document (sale, purchase, adjustment)
    
    # Tracking
    fecha_movimiento = Column(Date, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    observaciones = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    almacen = relationship("Almacen", back_populates="movimientos")
    producto = relationship("Producto")
    ubicacion_origen = relationship("UbicacionAlmacen", foreign_keys=[ubicacion_origen_id])
    ubicacion_destino = relationship("UbicacionAlmacen", foreign_keys=[ubicacion_destino_id])
    responsable = relationship("Empleado")


class Envio(Base):
    """Shipping management - Gestión de envíos"""
    __tablename__ = "log_envio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Shipping identification
    numero_guia = Column(String(50), unique=True, nullable=False)  # Tracking number
    codigo_seguimiento = Column(String(30), unique=True, nullable=False, index=True)  # Custom tracking code
    descripcion = Column(Text)
    
    # Related documents
    venta_id = Column(UUID(as_uuid=True), ForeignKey("ventas_venta.id"))  # Related sale
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"))  # Related purchase order
    
    # Shipping details
    metodo_envio = Column(SQLEnum(MetodoEnvio), nullable=False)
    estado = Column(SQLEnum(EstadoEnvio), default=EstadoEnvio.PREPARACION)
    
    # Origin and destination
    almacen_origen_id = Column(UUID(as_uuid=True), ForeignKey("log_almacen.id"), nullable=False)
    direccion_entrega = Column(Text, nullable=False)  # Delivery address
    contacto_entrega = Column(String(100))  # Contact person for delivery
    telefono_contacto = Column(String(20))  # Contact phone
    
    # Dimensions and weight
    peso_total = Column(Numeric(8, 2))  # Total weight in kg
    volumen_total = Column(Numeric(10, 2))  # Total volume in cubic meters
    numero_paquetes = Column(Integer, default=1)  # Number of packages
    
    # Dates
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_envio = Column(DateTime(timezone=True))  # Date when shipped
    fecha_estimada_entrega = Column(Date)  # Estimated delivery date
    fecha_entrega_real = Column(DateTime(timezone=True))  # Actual delivery date
    
    # Costs
    costo_envio = Column(Numeric(10, 2))  # Shipping cost
    seguro = Column(Numeric(10, 2))  # Insurance amount
    
    # Tracking
    empresa_envio = Column(String(100))  # Shipping company (FEDEX, DHL, ESTAFETA, etc.)
    url_seguimiento = Column(String(255))  # Tracking URL
    firma_entrega = Column(String(100))  # Name of person who received
    foto_entrega = Column(String(255))  # Path to delivery photo
    
    # Status
    entregado = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    venta = relationship("Venta")
    orden_compra = relationship("OrdenCompra")
    almacen_origen = relationship("Almacen")
    detalles = relationship("DetalleEnvio", back_populates="envio")


class DetalleEnvio(Base):
    """Shipping details - Detalles del envío"""
    __tablename__ = "log_detalle_envio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    envio_id = Column(UUID(as_uuid=True), ForeignKey("log_envio.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Details
    cantidad = Column(Integer, nullable=False)
    descripcion = Column(Text)
    
    # Tracking
    lote_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto_lote.id"))  # Batch if applicable
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    envio = relationship("Envio", back_populates="detalles")
    producto = relationship("Producto")
    lote = relationship("ProductoLote")


class HistorialEnvio(Base):
    """Shipping history - Historial del envío"""
    __tablename__ = "log_historial_envio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    envio_id = Column(UUID(as_uuid=True), ForeignKey("log_envio.id"), nullable=False)
    
    # History details
    estado_anterior = Column(SQLEnum(EstadoEnvio))
    estado_nuevo = Column(SQLEnum(EstadoEnvio), nullable=False)
    descripcion = Column(Text)  # Description of the change
    fecha_cambio = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # User who made the change
    
    # Location during update (for tracking)
    ubicacion_gps = Column(String(50))  # GPS location when status changed
    comentarios = Column(Text)
    
    # Relationships
    envio = relationship("Envio")
    usuario = relationship("Usuario")