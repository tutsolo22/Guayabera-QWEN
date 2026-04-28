"""
Notification System Schemas: User notifications, tasks, and tracking
Specialized for ERP system notifications
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# NOTIFICATION SCHEMAS
# ============================================================================

class NotificacionBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título de la notificación")
    descripcion: str = Field(..., description="Descripción detallada de la notificación")
    tipo: str = Field(..., description="Tipo de notificación")
    prioridad: Optional[str] = Field(default="normal", description="Prioridad de la notificación")
    canal: Optional[str] = Field(default="interno", description="Canal de notificación")
    destinatario_id: UUID4 = Field(..., description="ID del empleado destinatario")
    remitente_id: Optional[UUID4] = Field(None, description="ID del empleado remitente")
    departamento_destinatario_id: Optional[UUID4] = Field(None, description="ID del departamento destinatario")
    tipo_relacion: Optional[str] = Field(None, max_length=50, description="Tipo de registro relacionado")
    id_relacion: Optional[UUID4] = Field(None, description="ID del registro relacionado")
    estado: Optional[str] = Field(default="pendiente", description="Estado de la notificación")
    fecha_envio: Optional[datetime] = Field(None, description="Fecha de envío")
    fecha_leido: Optional[datetime] = Field(None, description="Fecha de lectura")
    fecha_procesado: Optional[datetime] = Field(None, description="Fecha de procesamiento")
    fecha_cierre: Optional[datetime] = Field(None, description="Fecha de cierre")
    requiere_confirmacion: Optional[bool] = Field(default=False, description="¿Requiere confirmación del usuario?")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento para acción")
    intentos_envio: Optional[int] = Field(default=0, description="Número de intentos de envío")
    datos_adicionales: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales de la notificación")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadatos para auditoría")
    activa: bool = Field(default=True, description="¿Está activa la notificación?")


class NotificacionCreate(NotificacionBase):
    pass


class NotificacionUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    prioridad: Optional[str] = None
    canal: Optional[str] = None
    estado: Optional[str] = None
    fecha_leido: Optional[datetime] = None
    fecha_procesado: Optional[datetime] = None
    fecha_cierre: Optional[datetime] = None
    requiere_confirmacion: Optional[bool] = None
    fecha_vencimiento: Optional[datetime] = None
    intentos_envio: Optional[int] = None
    datos_adicionales: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    activa: Optional[bool] = None


class NotificacionResponse(NotificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# NOTIFICATION COMMENT SCHEMAS
# ============================================================================

class ComentarioNotificacionBase(BaseModel):
    notificacion_id: UUID4
    autor_id: UUID4
    contenido: str = Field(..., description="Contenido del comentario")


class ComentarioNotificacionCreate(ComentarioNotificacionBase):
    pass


class ComentarioNotificacionUpdate(BaseModel):
    contenido: Optional[str] = None


class ComentarioNotificacionResponse(ComentarioNotificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# NOTIFICATION CONFIGURATION SCHEMAS
# ============================================================================

class ConfiguracionNotificacionBase(BaseModel):
    empleado_id: UUID4
    notificar_tareas: Optional[bool] = Field(default=True, description="¿Notificar tareas?")
    notificar_alertas: Optional[bool] = Field(default=True, description="¿Notificar alertas?")
    notificar_solicitudes: Optional[bool] = Field(default=True, description="¿Notificar solicitudes?")
    notificar_autorizaciones: Optional[bool] = Field(default=True, description="¿Notificar autorizaciones?")
    recibir_email: Optional[bool] = Field(default=True, description="¿Recibir por email?")
    recibir_push: Optional[bool] = Field(default=True, description="¿Recibir notificaciones push?")
    recibir_sms: Optional[bool] = Field(default=False, description="¿Recibir por SMS?")


class ConfiguracionNotificacionCreate(ConfiguracionNotificacionBase):
    pass


class ConfiguracionNotificacionUpdate(BaseModel):
    notificar_tareas: Optional[bool] = None
    notificar_alertas: Optional[bool] = None
    notificar_solicitudes: Optional[bool] = None
    notificar_autorizaciones: Optional[bool] = None
    recibir_email: Optional[bool] = None
    recibir_push: Optional[bool] = None
    recibir_sms: Optional[bool] = None


class ConfiguracionNotificacionResponse(ConfiguracionNotificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# NOTIFICATION HISTORY SCHEMAS
# ============================================================================

class HistorialNotificacionBase(BaseModel):
    notificacion_id: UUID4
    accion: str = Field(..., max_length=50, description="Acción realizada")
    descripcion_accion: Optional[str] = Field(None, description="Descripción de la acción")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable de la acción")


class HistorialNotificacionCreate(HistorialNotificacionBase):
    pass


class HistorialNotificacionResponse(HistorialNotificacionBase):
    id: UUID4
    fecha_accion: datetime

    class Config:
        from_attributes = True