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
    mfa_enabled = Column(Boolean, default=False)  # Whether MFA is enabled for this user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    roles = relationship("Rol", secondary=usuario_rol, back_populates="usuarios")
    metodos_mfa = relationship("MetodoMFA", back_populates="usuario")
    sesiones_mfa = relationship("SesionMFA", back_populates="usuario")

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "activo": self.activo,
            "ultimo_acceso": self.ultimo_acceso,
            "mfa_enabled": self.mfa_enabled
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


class AuditLog(Base):
    """Complete audit trail with enhanced support for sales operations"""
    __tablename__ = "seg_audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    user_name = Column(String(200))
    
    # Action details
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    module = Column(String(50), nullable=False)  # Sales module or other system modules
    sub_module = Column(String(50))  # Specific sales sub-module (e.g., orders, invoices)
    entity = Column(String(100), nullable=False)  # Entity type affected
    entity_id = Column(UUID(as_uuid=True))  # ID of the entity affected
    
    # Data changes
    previous_data = Column(JSONB)  # Previous values (for updates)
    new_data = Column(JSONB)  # New values (for creates/updates)
    
    # Sales-specific fields
    sale_id = Column(UUID(as_uuid=True))  # Reference to a specific sale if applicable
    customer_id = Column(UUID(as_uuid=True))  # Reference to a customer if applicable
    product_id = Column(UUID(as_uuid=True))  # Reference to a product if applicable
    
    # Technical info
    ip_address = Column(String(45))
    machine_name = Column(String(200))
    user_agent = Column(String(500))
    session_id = Column(String(255))  # Reference to the user session
    
    # Status and metadata
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    status = Column(String(20), default='success')  # success, failed, pending
    notes = Column(Text)  # Additional notes about the operation


class SecurityEvent(Base):
    """Security events for monitoring and compliance"""
    __tablename__ = "seg_security_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    event_type = Column(String(50), nullable=False)  # login_failed, suspicious_activity, etc.
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    description = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
    resolved_by = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    # Relationships
    user = relationship("Usuario", foreign_keys=[user_id])
    resolved_by_user = relationship("Usuario", foreign_keys=[resolved_by])


class MetodoMFA(Base):
    """MFA Methods for users"""
    __tablename__ = "seg_metodo_mfa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)
    
    # Method type (totp, sms, email, backup)
    tipo = Column(String(20), nullable=False)
    
    # Activation status
    activado = Column(Boolean, default=True)
    fecha_activacion = Column(DateTime(timezone=True))
    fecha_desactivacion = Column(DateTime(timezone=True))
    
    # Method-specific details
    secreto = Column(String(255))  # For TOTP or hashed backup codes
    telefono = Column(String(20))  # For SMS
    email = Column(String(100))    # For email-based MFA
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    usuario = relationship("Usuario", back_populates="metodos_mfa")


class SesionMFA(Base):
    """MFA Sessions to track authenticated sessions"""
    __tablename__ = "seg_sesion_mfa"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)
    sesion_id = Column(String(255), unique=True, nullable=False, index=True)  # Reference to auth session
    
    # Session status
    activa = Column(Boolean, default=True)
    fecha_expiracion = Column(DateTime(timezone=True), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    usuario = relationship("Usuario", back_populates="sesiones_mfa")