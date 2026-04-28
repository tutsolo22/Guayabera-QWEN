"""
Permission Models: User permissions and role management for all ERP modules
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

class TipoPermiso(enum.Enum):
    CONSULTA = "consulta"
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    EXPORTAR = "exportar"
    IMPORTAR = "importar"


class TipoRol(enum.Enum):
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    SUPERVISOR = "supervisor"
    OPERADOR = "operador"
    CONTADOR = "contador"
    RECURSOS_HUMANOS = "recursos_humanos"
    VENTAS = "ventas"
    PRODUCCION = "produccion"
    INVENTARIO = "inventario"


# ============================================================================
# PERMISSIONS MODELS
# ============================================================================

class Rol(Base):
    """User roles for permission management - Roles de usuario para gestión de permisos"""
    __tablename__ = "perm_rol"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Role details
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    tipo_rol = Column(SQLEnum(TipoRol), nullable=False)
    es_predeterminado = Column(Boolean, default=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    permisos = relationship("PermisoRol", back_populates="rol")
    usuarios = relationship("UsuarioRol", back_populates="rol")


class Permiso(Base):
    """System permissions - Permisos del sistema"""
    __tablename__ = "perm_permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Permission details
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    modulo = Column(String(50), nullable=False)  # rh, production, sales, etc.
    tipo = Column(SQLEnum(TipoPermiso), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    roles = relationship("PermisoRol", back_populates="permiso")


class PermisoRol(Base):
    """Role-permission association - Asociación rol-permiso"""
    __tablename__ = "perm_rol_permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rol_id = Column(UUID(as_uuid=True), ForeignKey("perm_rol.id"), nullable=False)
    permiso_id = Column(UUID(as_uuid=True), ForeignKey("perm_permiso.id"), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class UsuarioRol(Base):
    """User-role association - Asociación usuario-rol"""
    __tablename__ = "perm_usuario_rol"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    rol_id = Column(UUID(as_uuid=True), ForeignKey("perm_rol.id"), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    rol = relationship("Rol", back_populates="usuarios")
    usuario = relationship("Empleado")


class Notificacion(Base):
    """System notifications - Notificaciones del sistema"""
    __tablename__ = "perm_notificacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Notification details
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), default="informacion")  # informacion, advertencia, error, exito
    
    # Target users
    destinatarios_tipo = Column(String(20), default="usuario")  # usuario, rol
    destinatario_usuario_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # If targeted to specific user
    destinatario_rol_id = Column(UUID(as_uuid=True), ForeignKey("perm_rol.id"))  # If targeted to specific role
    
    # Status
    leido = Column(Boolean, default=False)
    enviado_correo = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    usuario_destinatario = relationship("Empleado")
    rol_destinatario = relationship("Rol")