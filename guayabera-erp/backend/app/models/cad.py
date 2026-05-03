"""
CAD Integration Models: Designs, patterns, and technical sheets
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

class TipoDiseno(enum.Enum):
    GUAYABERA = "guayabera"
    CAMISA = "camisa"
    PANTALON = "pantalon"
    VESTIDO = "vestido"
    CHALECO = "chaleco"
    SACO = "saco"
    OTRO = "otro"


class CategoriaPrenda(enum.Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TRABAJO = "trabajo"
    DEPORTE = "deporte"
    ESPECIAL = "especial"


class EstadoDiseno(enum.Enum):
    BORRADOR = "borrador"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    ACTIVO = "activo"
    DESCONTINUADO = "descontinuado"


# ============================================================================
# CAD DESIGN MODELS
# ============================================================================

class Diseno(Base):
    """Design management - Gestión de diseños CAD"""
    __tablename__ = "cad_diseno"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Design identification
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Design classification
    tipo_diseno = Column(SQLEnum(TipoDiseno), nullable=False)
    categoria = Column(SQLEnum(CategoriaPrenda))
    temporada = Column(String(50))  # Temporada de lanzamiento
    colección = Column(String(100))  # Nombre de la colección
    
    # Technical specifications
    composicion_tela = Column(String(200))  # Ej: "Algodón 100%"
    instrucciones_especiales = Column(Text)
    
    # Dimensions and fit
    holgura_base = Column(Numeric(5, 2), default=3.00)  # Holgura base en cm
    factor_multiplicacion_talla = Column(Numeric(5, 4), default=1.0250)  # Factor para escalado por tallas
    
    # Status
    estado = Column(SQLEnum(EstadoDiseno), default=EstadoDiseno.BORRADOR)
    activo = Column(Boolean, default=True)
    
    # Metadata
    fecha_creacion = Column(Date, nullable=False)
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    # References
    disenador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Designer
    aprobador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Approver
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    disenador = relationship("Empleado", foreign_keys=[disenador_id])
    aprobador = relationship("Empleado", foreign_keys=[aprobador_id])
    tallas = relationship("DisenoTalla", back_populates="diseno")
    componentes = relationship("ComponenteDiseno", back_populates="diseno")
    fichas_tecnicas = relationship("FichaTecnica", back_populates="diseno")
    producciones = relationship("OrdenProduccion", back_populates="diseno")


class DisenoTalla(Base):
    """Size specifications for designs - Especificaciones de tallas para diseños"""
    __tablename__ = "cad_diseno_talla"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diseno_id = Column(UUID(as_uuid=True), ForeignKey("cad_diseno.id"), nullable=False)
    
    # Size identification
    codigo_talla = Column(String(10), nullable=False)  # Ej: "M", "L", "XL"
    nombre_talla = Column(String(50), nullable=False)  # Ej: "Mediana", "Large"
    
    # Gender and age group
    genero = Column(String(20))  # "hombre", "mujer", "niño", "niña", "unisex"
    grupo_etario = Column(String(20))  # "adulto", "infantil", "juvenil"
    
    # Measurements (in cm) - Standard Mexican sizing
    pecho = Column(Numeric(6, 2))  # Chest measurement
    cintura = Column(Numeric(6, 2))  # Waist measurement
    cadera = Column(Numeric(6, 2))  # Hip measurement
    largo_total = Column(Numeric(6, 2))  # Total length
    largo_torso = Column(Numeric(6, 2))  # Torso length
    largo_manga = Column(Numeric(6, 2))  # Sleeve length
    ancho_manga = Column(Numeric(6, 2))  # Sleeve width
    hombros = Column(Numeric(6, 2))  # Shoulder measurement
    entrepierna = Column(Numeric(6, 2))  # Inseam (for pants)
    largo_tiro = Column(Numeric(6, 2))  # Rise length (for pants)
    ancho_cadera = Column(Numeric(6, 2))  # Hip width
    
    # Pattern adjustments specific to this size
    ajuste_especifico = Column(Text)  # Special adjustments for this size
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    diseno = relationship("Diseno", back_populates="tallas")


class ComponenteDiseno(Base):
    """Design components/pattern pieces - Componentes/piezas de patrón del diseño"""
    __tablename__ = "cad_componente_diseno"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diseno_id = Column(UUID(as_uuid=True), ForeignKey("cad_diseno.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))  # Associated product
    
    # Component identification
    nombre = Column(String(100), nullable=False)  # Ej: "Frente", "Manga Derecha"
    tipo_componente = Column(String(50), nullable=False)  # Ej: "frente", "espalda", "manga", "cuello", "bolsillo"
    descripcion = Column(Text)
    
    # Technical specifications
    cantidad_por_talla = Column(Integer, default=1)  # How many pieces per garment
    orientacion_tela = Column(String(20), default="recto")  # "recto", "cruzado"
    margen_costura = Column(Numeric(5, 2), default=1.00)  # Seam allowance in cm
    tiene_grano = Column(Boolean, default=True)  # Has grain direction
    sentido_grano = Column(String(20), default="paralelo")  # "paralelo", "perpendicular"
    
    # Manufacturing instructions
    instrucciones_corte = Column(Text)
    instrucciones_confeccion = Column(Text)
    
    # Pattern data (coordinates, measurements, etc.)
    datos_patron = Column(JSONB)  # Pattern geometry in JSON format
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    diseno = relationship("Diseno", back_populates="componentes")
    producto = relationship("Producto")


class FichaTecnica(Base):
    """Technical sheet for manufacturing - Ficha técnica para manufactura"""
    __tablename__ = "cad_ficha_tecnica"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diseno_id = Column(UUID(as_uuid=True), ForeignKey("cad_diseno.id"), nullable=False)
    
    # Document information
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    version = Column(String(20), default="1.0")
    titulo = Column(String(200), nullable=False)
    
    # Manufacturing specifications
    procesos = Column(JSONB)  # Manufacturing processes in JSON format
    maquinaria_requerida = Column(JSONB)  # Required machinery
    tiempos_estimados = Column(JSONB)  # Estimated times per process
    materiales_adicionales = Column(JSONB)  # Additional materials needed
    calidad_controles = Column(JSONB)  # Quality control checkpoints
    
    # Files
    archivo_pdf = Column(String(500))  # Path to PDF file
    archivo_imagen = Column(String(500))  # Path to image file
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Metadata
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    diseno = relationship("Diseno", back_populates="fichas_tecnicas")
    responsable = relationship("Empleado")


class HistoricoDiseno(Base):
    """History of design changes - Histórico de cambios del diseño"""
    __tablename__ = "cad_historico_diseno"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diseno_id = Column(UUID(as_uuid=True), ForeignKey("cad_diseno.id"), nullable=False)
    
    # Change information
    tipo_cambio = Column(String(50), nullable=False)  # "creacion", "modificacion", "aprobacion", etc.
    descripcion_cambio = Column(Text)
    campos_modificados = Column(JSONB)  # Which fields were modified
    
    # Who made the change
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from auth_usuario to seg_usuario
    
    # Timestamps
    fecha_cambio = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    diseno = relationship("Diseno")
    usuario = relationship("Usuario")