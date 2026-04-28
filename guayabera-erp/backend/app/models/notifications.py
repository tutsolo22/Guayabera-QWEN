"""
Notification System Models: User notifications, tasks, and tracking
Specialized for ERP system notifications
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

class TipoNotificacion(enum.Enum):
    TAREA = "tarea"
    ALERTA = "alerta"
    AVISO = "aviso"
    SOLICITUD = "solicitud"
    AUTORIZACION = "autorizacion"
    ESTADO_CAMBIO = "estado_cambio"
    SISTEMA = "sistema"


class PrioridadNotificacion(enum.Enum):
    BAJA = "baja"
    NORMAL = "normal"
    ALTA = "alta"
    URGENTE = "urgente"


class EstadoNotificacion(enum.Enum):
    PENDIENTE = "pendiente"
    LEIDA = "leida"
    PROCESADA = "procesada"
    CERRADA = "cerrada"
    CANCELADA = "cancelada"


class CanalNotificacion(enum.Enum):
    INTERNO = "interno"
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


# ============================================================================
# NOTIFICATION MODELS
# ============================================================================

class Notificacion(Base):
    """Notification management - Gestión de notificaciones"""
    __tablename__ = "not_notificacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Notification identification
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    
    # Classification
    tipo = Column(SQLEnum(TipoNotificacion), nullable=False)
    prioridad = Column(SQLEnum(PrioridadNotificacion), default=PrioridadNotificacion.NORMAL)
    canal = Column(SQLEnum(CanalNotificacion), default=CanalNotificacion.INTERNO)
    
    # Recipient and sender
    destinatario_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Employee receiving notification
    remitente_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Employee sending notification
    departamento_destinatario_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # Department if for all employees
    
    # Link to related records
    tipo_relacion = Column(String(50))  # Type of related record (ticket, requisition, etc.)
    id_relacion = Column(UUID(as_uuid=True))  # ID of related record
    
    # Status and tracking
    estado = Column(SQLEnum(EstadoNotificacion), default=EstadoNotificacion.PENDIENTE)
    fecha_envio = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_leido = Column(DateTime(timezone=True))
    fecha_procesado = Column(DateTime(timezone=True))
    fecha_cierre = Column(DateTime(timezone=True))
    
    # Task completion tracking
    requiere_confirmacion = Column(Boolean, default=False)  # Does this require user action?
    fecha_vencimiento = Column(DateTime(timezone=True))  # Deadline for action
    intentos_envio = Column(Integer, default=0)  # Number of delivery attempts
    
    # Additional data
    datos_adicionales = Column(JSONB)  # Additional data for the notification
    metadata = Column(JSONB)  # Metadata for audit trail
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    destinatario = relationship("Empleado", foreign_keys=[destinatario_id])
    remitente = relationship("Empleado", foreign_keys=[remitente_id])
    departamento_destinatario = relationship("Departamento")
    comentarios = relationship("ComentarioNotificacion", back_populates="notificacion")


class ComentarioNotificacion(Base):
    """Comments for notifications - Comentarios para notificaciones"""
    __tablename__ = "not_comentario_notificacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notificacion_id = Column(UUID(as_uuid=True), ForeignKey("not_notificacion.id"), nullable=False)
    autor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Comment content
    contenido = Column(Text, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    notificacion = relationship("Notificacion", back_populates="comentarios")
    autor = relationship("Empleado")


class ConfiguracionNotificacion(Base):
    """Notification settings per user - Configuración de notificaciones por usuario"""
    __tablename__ = "not_configuracion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Notification preferences
    notificar_tareas = Column(Boolean, default=True)
    notificar_alertas = Column(Boolean, default=True)
    notificar_solicitudes = Column(Boolean, default=True)
    notificar_autorizaciones = Column(Boolean, default=True)
    
    # Channel preferences
    recibir_email = Column(Boolean, default=True)
    recibir_push = Column(Boolean, default=True)
    recibir_sms = Column(Boolean, default=False)
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    empleado = relationship("Empleado")


class HistorialNotificacion(Base):
    """Notification history for audit trail - Historial de notificaciones para auditoría"""
    __tablename__ = "not_historial"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notificacion_id = Column(UUID(as_uuid=True), ForeignKey("not_notificacion.id"), nullable=False)
    
    # Action details
    accion = Column(String(50), nullable=False)  # "enviado", "leido", "procesado", "cerrado", etc.
    descripcion_accion = Column(Text)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Employee who performed the action
    
    # Timestamps
    fecha_accion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relationships
    notificacion = relationship("Notificacion")
    responsable = relationship("Empleado")