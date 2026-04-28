"""
Database models for GuayaberaERP
All models use UUID primary keys and timestamps
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


def generate_uuid():
    """Generate UUID string"""
    return str(uuid.uuid4())


class Empresa(Base):
    """Company/Enterprise information"""
    __tablename__ = "admin_empresa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfc = Column(String(13), unique=True, nullable=False, index=True)
    nombre_fiscal = Column(String(200), nullable=False)
    nombre_comercial = Column(String(200))
    regimen_fiscal = Column(String(100))
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(5))
    telefono = Column(String(20))
    email = Column(String(100))
    sitio_web = Column(String(200))
    logo_url = Column(String(500))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sucursales = relationship("Sucursal", back_populates="empresa")
    configuraciones_correo = relationship("ConfiguracionCorreo", back_populates="empresa")


class Sucursal(Base):
    """Branch offices"""
    __tablename__ = "admin_sucursal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("admin_empresa.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True)
    es_principal = Column(Boolean, default=False)
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    codigo_postal = Column(String(5))
    telefono = Column(String(20))
    email = Column(String(100))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    empresa = relationship("Empresa", back_populates="sucursales")


class Configuracion(Base):
    """System configuration key-value pairs"""
    __tablename__ = "admin_configuracion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clave = Column(String(100), unique=True, nullable=False, index=True)
    valor = Column(Text)
    tipo = Column(String(50))  # string, number, boolean, json
    descripcion = Column(String(500))
    modulo = Column(String(50))  # admin, finance, inventory, etc.
    es_publica = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Moneda(Base):
    """Currency configuration"""
    __tablename__ = "admin_moneda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(3), unique=True, nullable=False)  # MXN, USD, EUR
    nombre = Column(String(50), nullable=False)
    simbolo = Column(String(10))
    tasa_cambio = Column(Float, default=1.0)
    es_base = Column(Boolean, default=False)
    activa = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Impuesto(Base):
    """Tax configuration"""
    __tablename__ = "admin_impuesto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)  # IVA, ISR, IEPS
    tasa = Column(Float, nullable=False)  # 0.16 = 16%
    tipo = Column(String(50))  # trasladado, retenido
    vigente_desde = Column(DateTime(timezone=True))
    vigente_hasta = Column(DateTime(timezone=True))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ConfiguracionCorreoTipo(enum.Enum):
    """Email configuration types"""
    SMTP = "smtp"
    OFFICE365 = "office365"
    AMAZON_SES = "amazon_ses"
    GOOGLE_WORKSPACE = "google_workspace"


class ConfiguracionCorreo(Base):
    """Email configuration for a company"""
    __tablename__ = "admin_configuracion_correo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("admin_empresa.id"), nullable=False)
    nombre = Column(String(100), nullable=False)  # Configuration name (e.g., "Correo Principal")
    tipo = Column(String(50), nullable=False)  # See ConfiguracionCorreoTipo enum
    servidor = Column(String(255), nullable=False)
    puerto = Column(Integer, nullable=False)
    correo = Column(String(255), nullable=False)
    usuario = Column(String(255), nullable=False)
    contrasena = Column(String(255), nullable=False)
    seguridad = Column(String(50))  # SSL/TLS, etc.
    activo = Column(Boolean, default=True)
    predeterminado = Column(Boolean, default=False)  # Is this the default configuration?
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())