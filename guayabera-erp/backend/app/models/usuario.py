"""
Usuario models
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Usuario(Base):
    """Usuario model representing a system user"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100))
    telefono = Column(String(20))
    avatar = Column(String(255))  # Path to profile image
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)  # For temporary blocks
    
    # Role and permissions
    rol_id = Column(Integer, ForeignKey("roles.id"))
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))
    
    # Security
    failed_login_attempts = Column(Integer, default=0)
    last_failed_login = Column(DateTime(timezone=True))
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(32))  # For TOTP
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    rol = relationship("Rol", back_populates="usuarios")
    departamento = relationship("Departamento", back_populates="usuarios")
    sesiones = relationship("Sesion", back_populates="usuario")
    configuraciones_correo = relationship("ConfiguracionCorreo", back_populates="usuario_responsable")


class Rol(Base):
    """Rol model for user permissions"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, index=True, nullable=False)
    descripcion = Column(Text)
    permisos = Column(Text)  # JSON string of permissions
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="rol")


class Departamento(Base):
    """Departamento model for organizational structure"""
    __tablename__ = "departamentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True, nullable=False)
    descripcion = Column(Text)
    jefe_departamento_id = Column(Integer, ForeignKey("usuarios.id"))  # Self-referencing
    codigo = Column(String(20), unique=True, index=True)  # Dept code
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuarios = relationship("Usuario", back_populates="departamento")
    jefe = relationship("Usuario")


class Sesion(Base):
    """Sesion model for tracking user sessions"""
    __tablename__ = "sesiones"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    ip_address = Column(String(45))  # Support for IPv6 addresses
    user_agent = Column(Text)
    inicio_sesion = Column(DateTime(timezone=True), server_default=func.now())
    fin_sesion = Column(DateTime(timezone=True))  # Null if still active
    activa = Column(Boolean, default=True)  # True if session is still valid
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuario = relationship("Usuario", back_populates="sesiones")