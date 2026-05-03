"""
Quality Control Models: Quality inspections, standards, and tracking
Specialized for textile manufacturing quality control
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

class TipoInspeccion(enum.Enum):
    RECEPCION = "recepcion"
    PRODUCCION = "produccion"
    TERMINADO = "terminado"
    ENVIO = "envio"


class ResultadoInspeccion(enum.Enum):
    ACEPTADO = "aceptado"
    RECHAZADO = "rechazado"
    CONDICIONAL = "condicional"


class NivelInspeccion(enum.Enum):
    I = "i"
    II = "ii"
    III = "iii"


class EstadoCertificacion(enum.Enum):
    ACTIVA = "activa"
    EXPIRADA = "expirada"
    SUSPENDIDA = "suspendida"
    RETIRADA = "retirada"


# ============================================================================
# QUALITY CONTROL MODELS
# ============================================================================

class PlanMuestreo(Base):
    """Sampling plan for quality control - Plan de muestreo para control de calidad"""
    __tablename__ = "qc_plan_muestreo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Plan identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Sampling characteristics
    nivel_inspeccion = Column(SQLEnum(NivelInspeccion), default=NivelInspeccion.II)
    tamano_lote_min = Column(Integer, nullable=False)  # Minimum lot size
    tamano_lote_max = Column(Integer)  # Maximum lot size (None if unlimited)
    
    # Sampling parameters
    tamano_muestra = Column(Integer, nullable=False)
    numero_aceptacion = Column(Integer, nullable=False)  # Acceptance number
    numero_rechazo = Column(Integer, nullable=False)  # Rejection number
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsible employee
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    responsable = relationship("Empleado")
    inspecciones = relationship("InspeccionCalidad", back_populates="plan_muestreo")


class InspeccionCalidad(Base):
    """Quality inspection - Inspección de calidad"""
    __tablename__ = "qc_inspeccion_calidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Inspection identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    
    # Type and classification
    tipo_inspeccion = Column(SQLEnum(TipoInspeccion), nullable=False)
    resultado = Column(SQLEnum(ResultadoInspeccion))
    
    # Related entities
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))  # Product being inspected
    lote_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto_lote.id"))  # Lot being inspected
    orden_produccion_id = Column(UUID(as_uuid=True), ForeignKey("prod_orden_produccion.id"))  # Production order
    plan_muestreo_id = Column(UUID(as_uuid=True), ForeignKey("qc_plan_muestreo.id"))  # Sampling plan used
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Employee performing inspection
    
    # Inspection data
    tamano_lote = Column(Integer, nullable=False)
    tamano_muestra = Column(Integer, nullable=False)
    defectos_encontrados = Column(Integer, default=0)
    limite_aceptacion = Column(Integer)
    limite_rechazo = Column(Integer)
    
    # Results
    aceptado = Column(Boolean)  # Final acceptance decision
    observaciones = Column(Text)
    acciones_correctivas = Column(Text)
    
    # Dates
    fecha_inspeccion = Column(Date, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    producto = relationship("Producto")
    lote = relationship("ProductoLote")
    orden_produccion = relationship("OrdenProduccion")
    plan_muestreo = relationship("PlanMuestreo", back_populates="inspecciones")
    responsable = relationship("Empleado")
    registros_defectos = relationship("RegistroDefecto", back_populates="inspeccion")


class RegistroDefecto(Base):
    """Defect recording - Registro de defectos encontrados"""
    __tablename__ = "qc_registro_defecto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inspeccion_id = Column(UUID(as_uuid=True), ForeignKey("qc_inspeccion_calidad.id"), nullable=False)
    
    # Defect classification
    tipo_defecto = Column(String(100), nullable=False)  # Ej: "puntada suelta", "mancha", "color incorrecto"
    severidad = Column(String(20), default="baja")  # "baja", "media", "alta", "critica"
    descripcion = Column(Text)
    
    # Location and details
    ubicacion_defecto = Column(String(100))  # Where the defect was found
    cantidad = Column(Integer, default=1)  # Number of occurrences
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    inspeccion = relationship("InspeccionCalidad", back_populates="registros_defectos")


class EstandarCalidad(Base):
    """Quality standard - Estándar de calidad"""
    __tablename__ = "qc_estandar_calidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Standard identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Standard details
    categoria_producto = Column(String(50))  # "camisa", "pantalon", "vestido", etc.
    especificaciones = Column(JSONB)  # Detailed specifications as JSON
    pruebas_requeridas = Column(JSONB)  # Required tests as JSON
    
    # Compliance
    norma_referencia = Column(String(50))  # Ej: "ISO 9001", "OEKO-TEX", etc.
    nivel_cumplimiento = Column(Numeric(5, 2))  # Percentage of compliance
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsible employee
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    responsable = relationship("Empleado")
    productos_asociados = relationship("Producto", secondary="qc_producto_estandar")


class Certificacion(Base):
    """Product/service certification - Certificación de producto/servicio"""
    __tablename__ = "qc_certificacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Certification identification
    numero_certificado = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Certification details
    organismo_certificador = Column(String(100), nullable=False)  # Certifying body
    norma_certificacion = Column(String(50), nullable=False)  # "ISO 9001", "OEKO-TEX", etc.
    alcance = Column(Text)  # Scope of certification
    
    # Dates
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    estado = Column(SQLEnum(EstadoCertificacion), default=EstadoCertificacion.ACTIVA)
    renovacion_requerida = Column(Boolean, default=True)
    
    # Metadata
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsible employee
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    responsable = relationship("Empleado")
    productos_certificados = relationship("Producto", secondary="qc_producto_certificacion")


class ProductoEstandar(Base):
    """Association table between products and quality standards - Tabla de asociación entre productos y estándares de calidad"""
    __tablename__ = "qc_producto_estandar"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    estandar_id = Column(UUID(as_uuid=True), ForeignKey("qc_estandar_calidad.id"), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ProductoCertificacion(Base):
    """Association table between products and certifications - Tabla de asociación entre productos y certificaciones"""
    __tablename__ = "qc_producto_certificacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"), nullable=False)
    certificacion_id = Column(UUID(as_uuid=True), ForeignKey("qc_certificacion.id"), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())