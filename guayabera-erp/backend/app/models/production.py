"""
Textile Production Models: Patterns, garments, manufacturing processes
Specialized for guayabera production and textile manufacturing
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoPrenda(enum.Enum):
    GUAYABERA = "guayabera"
    CAMISA = "camisa"
    PANTALON = "pantalon"
    CHALECO = "chaleco"
    VESTIDO = "vestido"
    OTRO = "otro"


class TipoComponente(enum.Enum):
    ALFORZA = "alforza"
    CUELLO = "cuello"
    MANGA = "manga"
    BOLSILLO = "bolsillo"
    BOTON = "boton"
    OJUELO = "ojuelo"
    TELA = "tela"
    HILO = "hilo"


class TipoTela(enum.Enum):
    ALGODON = "algodon"
    LINEN = "linen"
    SEDA = "seda"
    POLIESTER = "poliester"
    MEZCLA = "mezcla"


class EstadoOrdenProduccion(enum.Enum):
    BORRADOR = "borrador"
    AUTORIZADA = "autorizada"
    EN_PROCESO = "en_proceso"
    PAUSADA = "pausada"
    TERMINADA = "terminada"
    CANCELADA = "cancelada"


class TipoProceso(enum.Enum):
    CORTE = "corte"
    CONFECCION = "confeccion"
    ACABADO = "acabado"
    EMPAQUE = "empaque"


# ============================================================================
# TEXTILE DESIGN (DISEÑO TEXTIL)
# ============================================================================

class PatronPrenda(Base):
    """Pattern for garments - Patrón de prenda"""
    __tablename__ = "prod_patron_prenda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic identification
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    tipo_prenda = Column(SQLEnum(TipoPrenda), nullable=False)
    
    # Design details
    caracteristicas_especiales = Column(Text)
    estilo = Column(String(100))  # clásico, moderno, infantil, etc.
    temporada = Column(String(50))  # primavera-verano, otoño-invierno
    genero = Column(String(20))  # masculino, femenino, unisex
    imagen_diseno = Column(String(500))  # URL de la imagen del diseño
    ficha_tecnica = Column(String(500))  # URL de la ficha técnica
    
    # Status
    activo = Column(Boolean, default=True)
    es_plantilla = Column(Boolean, default=False)  # Puede usarse como base para nuevas variantes
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    componentes = relationship("ComponentePatron", back_populates="patron")
    variantes = relationship("VariantePrenda", back_populates="patron")


class ComponentePatron(Base):
    """Components of a garment pattern - Componentes del patrón de prenda"""
    __tablename__ = "prod_componente_patron"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patron_id = Column(UUID(as_uuid=True), ForeignKey("prod_patron_prenda.id"), nullable=False)
    
    # Component identification
    nombre = Column(String(100), nullable=False)  # alforza, cuello, manga, etc.
    tipo = Column(SQLEnum(TipoComponente), nullable=False)
    descripcion = Column(Text)
    
    # Physical characteristics
    cantidad_por_prenda = Column(Integer, default=1)
    posicion_x = Column(Float)  # Posición en el patrón (cm)
    posicion_y = Column(Float)  # Posición en el patrón (cm)
    dimension_ancho = Column(Float)  # Ancho del componente (cm)
    dimension_alto = Column(Float)  # Alto del componente (cm)
    tolerancia = Column(Float, default=0.5)  # Tolerancia de corte (cm)
    
    # Special features
    tiene_boton = Column(Boolean, default=False)
    tiene_ojuelo = Column(Boolean, default=False)
    tiene_costura_decorativa = Column(Boolean, default=False)
    instrucciones_especiales = Column(Text)
    
    # Material requirements
    material_requerido_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patron = relationship("PatronPrenda", back_populates="componentes")
    material_requerido = relationship("Producto", foreign_keys=[material_requerido_id])


# ============================================================================
# GARMENT VARIANTS (VARIANTES DE PRENDAS)
# ============================================================================

class VariantePrenda(Base):
    """Garment variants with specific measurements - Variantes de prenda con medidas específicas"""
    __tablename__ = "prod_variante_prenda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patron_id = Column(UUID(as_uuid=True), ForeignKey("prod_patron_prenda.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"))  # Si es diseño personalizado
    
    # Variant identification
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Size and measurements
    talla = Column(String(10))  # S, M, L, XL, 32, 34, etc.
    medidas_especificas = Column(JSONB)  # Medidas personalizadas en formato JSON
    # Ejemplo: {"pecho": 100, "cintura": 85, "cadera": 95, "largo": 75}
    
    # Customization options
    color = Column(String(50))
    tipo_tela = Column(SQLEnum(TipoTela))
    tipo_hilo = Column(String(50))
    tipo_boton = Column(String(100))
    caracteristicas_adicionales = Column(Text)
    
    # Production info
    tiempo_estimado_produccion = Column(Integer)  # En horas
    costo_estimado = Column(Numeric(15, 2))
    
    # Status
    activo = Column(Boolean, default=True)
    es_personalizada = Column(Boolean, default=False)  # Para pedidos especiales
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    patron = relationship("PatronPrenda", back_populates="variantes")
    cliente = relationship("Cliente")  # Asumiendo que existe un modelo Cliente


# ============================================================================
# PRODUCTION ORDERS (ÓRDENES DE PRODUCCIÓN)
# ============================================================================

class OrdenProduccion(Base):
    """Production orders - Órdenes de producción"""
    __tablename__ = "prod_orden_produccion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variante_prenda_id = Column(UUID(as_uuid=True), ForeignKey("prod_variante_prenda.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("ventas_cliente.id"))  # Changed from com_cliente to ventas_cliente
    almacen_salida_id = Column(UUID(as_uuid=True), ForeignKey("alm_almacen.id"))
    
    # Order identification
    folio = Column(String(30), unique=True, nullable=False, index=True)
    descripcion = Column(Text)
    
    # Production details
    cantidad = Column(Integer, nullable=False)
    fecha_inicio = Column(Date)
    fecha_entrega = Column(Date)
    prioridad = Column(Integer, default=1)  # 1-5, 5 más alta prioridad
    
    # Status
    estado = Column(SQLEnum(EstadoOrdenProduccion), default=EstadoOrdenProduccion.BORRADOR)
    porcentaje_completado = Column(Numeric(5, 2), default=0.00)  # 0.00 a 100.00%
    fecha_estado_actual = Column(DateTime(timezone=True), server_default=func.now())
    
    # Costs
    costo_estimado_total = Column(Numeric(15, 2))
    costo_real_total = Column(Numeric(15, 2))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    variante_prenda = relationship("VariantePrenda")
    cliente = relationship("Cliente", back_populates="ordenes_produccion")
    almacen_salida = relationship("Almacen")  # Asumiendo que existe un modelo Almacen
    procesos = relationship("ProcesoProduccion", back_populates="orden_produccion")


class ProcesoProduccion(Base):
    """Production processes - Procesos de producción"""
    __tablename__ = "prod_proceso_produccion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orden_produccion_id = Column(UUID(as_uuid=True), ForeignKey("prod_orden_produccion.id"), nullable=False)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Asumiendo modelo RH
    
    # Process details
    tipo = Column(SQLEnum(TipoProceso), nullable=False)
    descripcion = Column(Text)
    numero_secuencia = Column(Integer)  # Orden del proceso en la secuencia
    
    # Timing
    fecha_inicio_planificada = Column(Date)
    fecha_fin_planificada = Column(Date)
    fecha_inicio_real = Column(DateTime(timezone=True))
    fecha_fin_real = Column(DateTime(timezone=True))
    
    # Status
    estado = Column(String(20), default="pendiente")  # pendiente, en_progreso, completado, cancelado
    observaciones = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orden_produccion = relationship("OrdenProduccion", back_populates="procesos")
    responsable = relationship("Empleado")  # Asumiendo modelo RH


# ============================================================================
# BILL OF MATERIALS (LISTA DE MATERIALES)
# ============================================================================

class ListaMateriales(Base):
    """Bill of Materials - Lista de materiales para producción"""
    __tablename__ = "prod_lista_materiales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    variante_prenda_id = Column(UUID(as_uuid=True), ForeignKey("prod_variante_prenda.id"), nullable=False)
    
    # Identification
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    variante_prenda = relationship("VariantePrenda")
    materiales = relationship("MaterialLista", back_populates="lista_materiales")


class MaterialLista(Base):
    """Materials in bill of materials - Materiales en la lista de materiales"""
    __tablename__ = "prod_material_lista"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lista_materiales_id = Column(UUID(as_uuid=True), ForeignKey("prod_lista_materiales.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    
    # Material details
    cantidad_requerida = Column(Numeric(10, 4), nullable=False)
    unidad_medida = Column(String(10))  # metros, piezas, litros, etc.
    desperdicio_porcentaje = Column(Numeric(5, 2), default=0.00)  # Porcentaje de desperdicio esperado
    notas = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    lista_materiales = relationship("ListaMateriales", back_populates="materiales")
    producto = relationship("Producto")