"""
Notification System Models: User notifications, tasks, and tracking
Specialized for ERP system notifications
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text, 
    Boolean, Date, Numeric, CheckConstraint, 
    func, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


# ============================================================================
# ENUMS
# ============================================================================

class TipoNotificacion(enum.Enum):
    """Tipos de notificaciones"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    ALERTA = "alerta"
    AVISO = "aviso"
    TAREA = "tarea"
    AUTORIZACION = "autorizacion"
    SOLICITUD = "solicitud"


class PrioridadNotificacion(enum.Enum):
    """Prioridades de notificaciones"""
    BAJA = 1
    NORMAL = 2
    ALTA = 3
    URGENTE = 4


class CanalNotificacion(enum.Enum):
    """Canales de entrega de notificaciones"""
    INTERNO = "interno"  # Dentro del sistema ERP
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


# ============================================================================
# NOTIFICATION MODELS
# ============================================================================

class Notificacion(Base):
    """Modelo para gestionar notificaciones del sistema"""
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # info, warning, error, success
    prioridad = Column(Integer, default=1)  # 1-baja, 2-media, 3-alta
    leido = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_lectura = Column(DateTime(timezone=True), nullable=True)
    
    # Cambiamos 'metadata' por 'datos_adicionales' para evitar conflicto con el nombre reservado
    datos_adicionales = Column(JSON, nullable=True)  # Almacenar datos adicionales en formato JSON
    
    # Relaciones
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from Integer to UUID to match seg_usuario
    usuario = relationship("Usuario", back_populates="notificaciones_recibidas")
    
    # Usuario que enviÃ³ la notificaciÃ³n
    remitente_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=True)  # Changed from Integer to UUID to match seg_usuario
    remitente = relationship("Usuario", foreign_keys=[remitente_id], back_populates="notificaciones_enviadas")
    
    # Relaciones para nuevos modelos
    historial = relationship("HistorialNotificacion", back_populates="notificacion")
    acciones = relationship("AccionNotificacion", back_populates="notificacion")
    comentarios = relationship("ComentarioNotificacion", back_populates="notificacion")




class HistorialNotificacion(Base):
    """Historial de notificaciones enviadas"""
    __tablename__ = "historial_notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    notificacion_id = Column(Integer, ForeignKey("notificaciones.id"), nullable=False)
    autor_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from Integer to UUID to match seg_usuario
    contenido = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    notificacion = relationship("Notificacion", back_populates="historial")
    autor = relationship("Usuario", back_populates="historial_notificaciones")  # Changed from User to Usuario


class ComentarioNotificacion(Base):
    """Modelo para comentarios en notificaciones"""
    __tablename__ = "comentarios_notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    notificacion_id = Column(Integer, ForeignKey("notificaciones.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from Integer to UUID to match seg_usuario
    contenido = Column(Text, nullable=False)
    fecha_comentario = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)

    # Relaciones
    notificacion = relationship("Notificacion", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios_notificaciones")  # Changed from User to Usuario


class ConfiguracionNotificacion(Base):
    """ConfiguraciÃ³n de notificaciones por empleado"""
    __tablename__ = "config_notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Changed from Integer to UUID to match rh_empleado
    
    # Preferencias de notificaciÃ³n
    notificar_tareas = Column(Boolean, default=True)
    notificar_alertas = Column(Boolean, default=True)
    notificar_solicitudes = Column(Boolean, default=True)
    notificar_autorizaciones = Column(Boolean, default=True)
    
    # MÃ©todos de notificaciÃ³n preferidos
    recibir_email = Column(Boolean, default=True)
    recibir_push = Column(Boolean, default=True)
    recibir_sms = Column(Boolean, default=False)
    
    # Estado
    activa = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    empleado = relationship("Empleado", back_populates="config_notificaciones")


class AccionNotificacion(Base):
    """Acciones tomadas en base a notificaciones"""
    __tablename__ = "acciones_notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    notificacion_id = Column(Integer, ForeignKey("notificaciones.id"), nullable=False)
    
    # AcciÃ³n realizada
    accion = Column(String(100), nullable=False)  # aprobada, rechazada, vista, etc.
    descripcion_accion = Column(Text)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=True)  # Changed from Integer to UUID to match seg_usuario
    
    fecha_accion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    notificacion = relationship("Notificacion", back_populates="acciones")
    responsable = relationship("Usuario", back_populates="acciones_notificaciones")  # Changed from User to Usuario
