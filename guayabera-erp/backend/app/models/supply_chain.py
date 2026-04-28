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