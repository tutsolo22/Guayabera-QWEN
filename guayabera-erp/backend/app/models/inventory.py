"""
Inventory Management Models: Products, categories, attributes
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

class CategoriaProducto(enum.Enum):
    TELA = "tela"
    AVIO = "avio"
    INSUMO = "insumo"
    PRODUCTO_TERMINADO = "producto_terminado"


class TipoTela(enum.Enum):
    LISA = "lisa"
    A_RAYAS = "a_rayas"
    A_CUADROS = "a_cuadros"
    ESTAMPADA = "estampada"
    CON_DIBUJO = "con_dibujo"
    PUNTEADA = "punteada"


class TipoAvio(enum.Enum):
    BOTON = "boton"
    CIERRE = "cierre"
    CINTA = "cinta"
    ELASTICO = "elastico"
    LAZO = "lazo"
    CUELLO = "cuello"
    MANGA = "manga"
    OJAL = "ojal"
    OTRO = "otro"


class UsoProducto(enum.Enum):
    AUTOCONSUMO = "autoconsumo"
    VENTA = "venta"
    ALMACENABLE = "almacenable"


class EstadoRecepcion(enum.Enum):
    PENDIENTE = "pendiente"
    VERIFICADO = "verificado"
    REVISION_COMPLETA = "revision_completa"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"


# ============================================================================
# PRODUCT CATEGORIES AND ATTRIBUTES (CATEGORÍAS Y ATRIBUTOS DE PRODUCTOS)
# ============================================================================

class CategoriaProductoTextil(Base):
    """Textile product categories - Categorías de productos textiles"""
    __tablename__ = "inv_categoria_producto_textil"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Category details
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    
    # Parent category (for hierarchical structure)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("inv_categoria_producto_textil.id"))
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    parent = relationship("CategoriaProductoTextil", remote_side=[id])
    subcategorias = relationship("CategoriaProductoTextil")
    productos = relationship("ProductoTextil", back_populates="categoria")


class ProductoTextil(Base):
    """Textile product with extended attributes - Producto textil con atributos extendidos"""
    __tablename__ = "inv_producto_textil"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("inv_categoria_producto_textil.id"), nullable=False)
    
    # Product classification
    categoria_producto = Column(SQLEnum(CategoriaProducto), nullable=False)
    tipo_uso = Column(SQLEnum(UsoProducto), default=UsoProducto.VENTA)
    
    # Specific textile attributes
    es_tela = Column(Boolean, default=False)
    tipo_tela = Column(SQLEnum(TipoTela))
    
    # For plain fabrics (lisa)
    codigo_color_pantone = Column(String(20))  # Pantone color code
    nombre_color_pantone = Column(String(100))  # Pantone color name
    sobrenombre_color_1 = Column(String(50))  # Nickname for color
    sobrenombre_color_2 = Column(String(50))  # Second nickname for color
    sobrenombre_color_3 = Column(String(50))  # Third nickname for color
    
    # For patterned fabrics (a rayas, a cuadros, estampadas)
    colores_patron = Column(JSONB)  # Colors used in pattern (for stripes, checks, prints)
    # Example: [{"codigo": "PANTONE-123", "nombre": "Rojo Brillante", "sobrenombres": ["Rojo fuego", "Rojo sangre"]}]
    
    # For avios
    tipo_avio = Column(SQLEnum(TipoAvio))
    sobrenombre_avio_1 = Column(String(50))  # Nickname for avio
    sobrenombre_avio_2 = Column(String(50))  # Second nickname for avio
    sobrenombre_avio_3 = Column(String(50))  # Third nickname for avio
    
    # Material properties
    composicion = Column(String(100))  # Cotton, polyester, etc.
    gramaje = Column(Numeric(8, 2))  # Weight in grams per square meter
    ancho = Column(Numeric(8, 2))  # Width in cm
    textura = Column(String(100))  # Smooth, rough, etc.
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    producto = relationship("Producto", back_populates="producto_textil_detalle")
    categoria = relationship("CategoriaProductoTextil", back_populates="productos")
    lotes = relationship("LoteProducto", back_populates="producto_textil")


class LoteProducto(Base):
    """Product lots with detailed variations - Lotes de producto con variaciones detalladas"""
    __tablename__ = "inv_lote_producto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_textil_id = Column(UUID(as_uuid=True), ForeignKey("inv_producto_textil.id"), nullable=False)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"))
    
    # Lot details
    numero_lote = Column(String(50), nullable=False)
    fecha_elaboracion = Column(Date)
    fecha_vencimiento = Column(Date)
    
    # Color variations (especially important for textiles)
    variacion_tono = Column(String(200))  # Description of tone variation
    grado_variacion = Column(Integer)  # Scale 1-10, how much the tone varies
    responsable_evaluacion_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Storage location
    ubicacion_almacen = Column(String(100))  # Specific location in warehouse
    
    # Status
    estado = Column(String(20), default="activo")  # activo, usado, agotado
    
    # Metadata
    observaciones = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    producto_textil = relationship("ProductoTextil", back_populates="lotes")
    proveedor = relationship("Proveedor")
    responsable_evaluacion = relationship("Empleado")
    recepciones = relationship("RecepcionCompra", back_populates="lote_producto")


class RecepcionCompra(Base):
    """Quick purchase reception with detailed review - Recepción rápida de compra con revisión detallada"""
    __tablename__ = "inv_recepcion_compra"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"))
    lote_producto_id = Column(UUID(as_uuid=True), ForeignKey("inv_lote_producto.id"))
    responsable_recepcion_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Reception details
    fecha_recepcion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    folio_compra = Column(String(50), nullable=False)  # Purchase order number
    numero_proveedor = Column(String(50), nullable=False)  # Supplier number
    
    # Quick verification (first stage)
    cantidad_verificada = Column(Integer, default=0)
    estado_recepcion = Column(SQLEnum(EstadoRecepcion), default=EstadoRecepcion.PENDIENTE)
    qr_registro = Column(String(200))  # QR code for quick identification
    
    # Detailed review (second stage)
    fecha_revision = Column(DateTime(timezone=True))
    responsable_revision_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    cantidad_aprobada = Column(Integer, default=0)
    variaciones_detectadas = Column(Text)  # Description of detected variations
    inspeccion_calidad = Column(Text)  # Quality inspection notes
    
    # Final approval
    fecha_aprobacion = Column(DateTime(timezone=True))
    responsable_aprobacion_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orden_compra = relationship("OrdenCompra")
    lote_producto = relationship("LoteProducto", back_populates="recepciones")
    responsable_recepcion = relationship("Empleado", foreign_keys=[responsable_recepcion_id])
    responsable_revision = relationship("Empleado", foreign_keys=[responsable_revision_id])
    responsable_aprobacion = relationship("Empleado", foreign_keys=[responsable_aprobacion_id])


class EtiquetaProducto(Base):
    """Product labels with QR codes for traceability - Etiquetas de producto con códigos QR para trazabilidad"""
    __tablename__ = "inv_etiqueta_producto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lote_producto_id = Column(UUID(as_uuid=True), ForeignKey("inv_lote_producto.id"), nullable=False)
    producto_textil_id = Column(UUID(as_uuid=True), ForeignKey("inv_producto_textil.id"), nullable=False)
    
    # Label details
    codigo_qr = Column(String(200), unique=True, nullable=False, index=True)  # Unique QR code
    contenido_etiqueta = Column(JSONB)  # Content to be printed on label
    # Example: {
    #   "producto": "Camisa Guayabera",
    #   "color": "Azul Marino",
    #   "variacion_tono": "Ligera diferencia en intensidad",
    #   "lote": "LOT-2023-001",
    #   "fecha_elaboracion": "2023-05-15",
    #   "ubicacion": "Estante A-5"
    # }
    
    # Print status
    impresa = Column(Boolean, default=False)
    fecha_impresion = Column(DateTime(timezone=True))
    responsable_impresion_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lote_producto = relationship("LoteProducto")
    producto_textil = relationship("ProductoTextil")
    responsable_impresion = relationship("Empleado")


# ============================================================================
# MODELOS ESPECÍFICOS DE INVENTARIO
# ============================================================================

class TomaInventario(Base):
    """Registro de tomas de inventario - Inventory count records"""
    __tablename__ = "inv_toma_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    folio = Column(String(15), unique=True, nullable=False, index=True)  # Ej: ALM-0000001
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    fecha_toma = Column(Date, nullable=False, default=func.current_date())
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    estado = Column(String(20), default="en_progreso")  # en_progreso, consolidado, comparado, ajustado
    comentarios = Column(Text)
    
    almacen = relationship("Almacen")
    responsable = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RegistroTomaInventario(Base):
    """Registros individuales de la toma de inventario - Individual inventory count records"""
    __tablename__ = "inv_registro_toma"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    toma_inventario_id = Column(UUID(as_uuid=True), ForeignKey("inv_toma_inventario.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    cantidad_escaneada = Column(Integer, default=0)  # Cantidad física contada
    modelo = Column(String(100))
    color = Column(String(50))
    talla = Column(String(20))
    
    toma_inventario = relationship("TomaInventario", back_populates="registros")
    producto = relationship("Producto")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DiferenciaInventario(Base):
    """Diferencias encontradas en la comparación de inventarios - Differences found in inventory comparison"""
    __tablename__ = "inv_diferencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    toma_inventario_id = Column(UUID(as_uuid=True), ForeignKey("inv_toma_inventario.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    modelo = Column(String(100))
    color = Column(String(50))
    talla = Column(String(20))
    cantidad_sistema = Column(Integer, default=0)  # Cantidad según sistema
    cantidad_fisica = Column(Integer, default=0)   # Cantidad física contada
    diferencia = Column(Integer, default=0)        # Diferencia (física - sistema)
    estado = Column(String(20), default="pendiente")  # pendiente, ajustado, verificado
    
    toma_inventario = relationship("TomaInventario")
    producto = relationship("Producto")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MovimientoInventario(Base):
    """Movimientos diversos de inventario - Various inventory movements"""
    __tablename__ = "inv_movimiento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tipo_movimiento = Column(String(50), nullable=False)  # ajuste_positivo, ajuste_negativo, otro_entrada, otro_salida
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    motivo = Column(Text)  # Descripción del motivo del movimiento
    referencia = Column(String(100))  # Referencia externa si aplica
    
    almacen = relationship("Almacen")
    producto = relationship("Producto")
    responsable = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


TomaInventario.registros = relationship("RegistroTomaInventario", back_populates="toma_inventario")

