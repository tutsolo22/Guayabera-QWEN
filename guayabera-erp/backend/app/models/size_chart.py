"""
Size Chart Models: Standard Mexican sizing for clothing
Including sizes for men, women, boys, girls with standard measurements
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class Genero(enum.Enum):
    HOMBRE = "hombre"
    MUJER = "mujer"
    NINO = "nino"
    NINA = "nina"
    UNISEX = "unisex"


class GrupoEtario(enum.Enum):
    ADULTO = "adulto"
    INFANTIL = "infantil"
    JUVENIL = "juvenil"


class TipoPrenda(enum.Enum):
    CAMISA = "camisa"
    PANTALON = "pantalon"
    POLO = "polo"
    CHAMARRA = "chamarra"
    BLUSA = "blusa"
    FALDA = "falda"
    VESTIDO = "vestido"
    SHORT = "short"
    PLAYERA = "playera"
    SUETER = "sueter"
    CALCETIN = "calcetin"
    CALZADO = "calzado"
    ACCESORIO = "accesorio"


# ============================================================================
# SIZE CHART MODELS
# ============================================================================

class TablaTalla(Base):
    """Standard size chart - Tabla de tallas estándar"""
    __tablename__ = "size_tabla_talla"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Chart identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)  # Ej: "Tabla Tallas Camisas Hombre"
    descripcion = Column(Text)
    
    # Classification
    tipo_prenda = Column(SQLEnum(TipoPrenda), nullable=False)
    genero = Column(SQLEnum(Genero), nullable=False)
    grupo_etario = Column(SQLEnum(GrupoEtario), default=GrupoEtario.ADULTO)
    
    # Status
    activa = Column(Boolean, default=True)
    es_estandar_mexicano = Column(Boolean, default=True)  # Indicates if it's a standard Mexican size chart
    
    # Metadata
    creador_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Creator
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    creador = relationship("Empleado")
    tallas = relationship("Talla", back_populates="tabla_talla")


class Talla(Base):
    """Individual size in a chart - Talla individual en una tabla"""
    __tablename__ = "size_talla"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tabla_talla_id = Column(UUID(as_uuid=True), ForeignKey("size_tabla_talla.id"), nullable=False)
    
    # Size identification
    codigo = Column(String(10), nullable=False)  # Ej: "CH", "M", "G", "EG", "1X", "2X", etc.
    nombre = Column(String(30), nullable=False)  # Ej: "Chica", "Mediana", "Grande", "Extra Grande"
    
    # Standard Mexican sizes
    posicion_orden = Column(Integer)  # Order position for display (CH=1, M=2, G=3, etc.)
    
    # Measurements (in cm)
    pecho_bust = Column(Numeric(6, 2))  # Chest/bust measurement
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
    cuello = Column(Numeric(6, 2))  # Neck circumference
    puño = Column(Numeric(6, 2))  # Wrist circumference
    largo_pantalon = Column(Numeric(6, 2))  # Pants length
    
    # Age recommendations
    edad_minima = Column(Integer)  # Minimum recommended age
    edad_maxima = Column(Integer)  # Maximum recommended age
    
    # Notes
    notas = Column(Text)  # Additional notes about this size
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    tabla_talla = relationship("TablaTalla", back_populates="tallas")


class ReferenciaTalla(Base):
    """Reference mapping between different size systems - Mapeo entre diferentes sistemas de tallas"""
    __tablename__ = "size_referencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    talla_id = Column(UUID(as_uuid=True), ForeignKey("size_talla.id"), nullable=False)
    
    # Reference system
    sistema_referencia = Column(String(50), nullable=False)  # "US", "EU", "UK", etc.
    codigo_referencia = Column(String(10), nullable=False)  # "S", "M", "L", "38", "12", etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    talla = relationship("Talla")