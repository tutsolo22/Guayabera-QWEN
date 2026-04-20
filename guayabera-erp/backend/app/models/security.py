"""
Security models: Users, Roles, Permissions, Audit
"""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Table, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


# Association tables
usuario_rol = Table(
    'seg_usuario_rol',
    Base.metadata,
    Column('usuario_id', UUID(as_uuid=True), ForeignKey('seg_usuario.id')),
    Column('rol_id', UUID(as_uuid=True), ForeignKey('seg_rol.id'))
)

rol_permiso = Table(
    'seg_rol_permiso',
    Base.metadata,
    Column('rol_id', UUID(as_uuid=True), ForeignKey('seg_rol.id')),
    Column('permiso_id', UUID(as_uuid=True), ForeignKey('seg_permiso.id'))
)


class Usuario(Base):
    """System users"""
    __tablename__ = "seg_usuario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100))
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime(timezone=True))
    intentos_fallidos = Column(Integer, default=0)
    bloqueado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    roles = relationship("Rol", secondary=usuario_rol, back_populates="usuarios")

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "activo": self.activo,
            "ultimo_acceso": self.ultimo_acceso
        }


class Rol(Base):
    """User roles"""
    __tablename__ = "seg_rol"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200))
    es_sistema = Column(Boolean, default=False)  # System roles can't be deleted
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    usuarios = relationship("Usuario", secondary=usuario_rol, back_populates="roles")
    permisos = relationship("Permiso", secondary=rol_permiso, back_populates="roles")


class Permiso(Base):
    """System permissions"""
    __tablename__ = "seg_permiso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modulo = Column(String(50), nullable=False)  # admin, finance, inventory
    accion = Column(String(50), nullable=False)  # ver, crear, editar, eliminar
    descripcion = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    roles = relationship("Rol", secondary=rol_permiso, back_populates="permisos")


class Auditoria(Base):
    """Complete audit trail"""
    __tablename__ = "seg_auditoria"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    usuario_nombre = Column(String(200))
    
    # Action details
    accion = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN
    modulo = Column(String(50), nullable=False)
    entidad = Column(String(100), nullable=False)
    entidad_id = Column(UUID(as_uuid=True))
    
    # Data changes
    datos_anteriores = Column(JSONB)
    datos_nuevos = Column(JSONB)
    
    # Technical info
    ip_address = Column(String(45))
    nombre_maquina = Column(String(200))
    user_agent = Column(String(500))
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
