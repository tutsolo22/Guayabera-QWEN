"""
Email Configuration Schemas: SMTP settings for sending invoices, quotes, etc.
Integrated with company configuration and includes test functionality
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from datetime import datetime
import uuid


class ConfiguracionCorreoBase(BaseModel):
    empresa_id: UUID4 = Field(..., description="ID de la empresa asociada")
    servidor_smtp: str = Field(..., max_length=255, description="Servidor SMTP (ej. smtp.gmail.com)")
    puerto_smtp: int = Field(default=587, ge=1, le=65535, description="Puerto SMTP (comúnmente 587, 465, 25)")
    seguridad_smtp: str = Field(default="TLS", description="Tipo de seguridad (TLS, SSL, None)")
    nombre_remitente: Optional[str] = Field(None, max_length=255, description="Nombre del remitente")
    correo_remitente: str = Field(..., max_length=255, description="Correo del remitente")
    usuario_smtp: str = Field(..., max_length=255, description="Usuario SMTP")
    contrasena_smtp: str = Field(..., max_length=255, description="Contraseña SMTP")
    activo: bool = Field(default=True, description="¿Está activa la configuración?")
    asunto_predeterminado: Optional[str] = Field(None, max_length=500, description="Asunto predeterminado para correos")
    cuerpo_predeterminado: Optional[str] = Field(None, description="Cuerpo predeterminado para correos")
    habilitado_para_facturas: bool = Field(default=True, description="¿Habilitado para envío de facturas?")
    habilitado_para_cotizaciones: bool = Field(default=True, description="¿Habilitado para envío de cotizaciones?")
    habilitado_para_notificaciones: bool = Field(default=True, description="¿Habilitado para notificaciones?")
    habilitado_para_documentos: bool = Field(default=True, description="¿Habilitado para documentos?")


class ConfiguracionCorreoCreate(ConfiguracionCorreoBase):
    pass


class ConfiguracionCorreoUpdate(BaseModel):
    servidor_smtp: Optional[str] = Field(None, max_length=255)
    puerto_smtp: Optional[int] = Field(None, ge=1, le=65535)
    seguridad_smtp: Optional[str] = Field(None)
    nombre_remitente: Optional[str] = Field(None, max_length=255)
    correo_remitente: Optional[str] = Field(None, max_length=255)
    usuario_smtp: Optional[str] = Field(None, max_length=255)
    contrasena_smtp: Optional[str] = Field(None, max_length=255)
    activo: Optional[bool] = None
    asunto_predeterminado: Optional[str] = Field(None, max_length=500)
    cuerpo_predeterminado: Optional[str] = None
    habilitado_para_facturas: Optional[bool] = None
    habilitado_para_cotizaciones: Optional[bool] = None
    habilitado_para_notificaciones: Optional[bool] = None
    habilitado_para_documentos: Optional[bool] = None


class ConfiguracionCorreoResponse(ConfiguracionCorreoBase):
    id: UUID4
    verificado: bool
    ultima_prueba_fecha: Optional[datetime] = None
    ultima_prueba_resultado: Optional[str] = None
    ultima_prueba_detalle: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConfiguracionCorreoTest(BaseModel):
    id: UUID4 = Field(..., description="ID de la configuración a probar")
    destinatario_prueba: str = Field(..., description="Dirección de correo para la prueba")


class HistorialCorreoResponse(BaseModel):
    id: UUID4
    configuracion_id: UUID4
    destinatarios: str
    copia: Optional[str] = None
    copia_oculta: Optional[str] = None
    asunto: str
    cuerpo: str
    adjuntos: Optional[str] = None
    enviado: bool
    fecha_envio: Optional[datetime] = None
    error_detalle: Optional[str] = None
    tipo_documento: Optional[str] = None
    referencia_documento: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class EnviarCorreoRequest(BaseModel):
    configuracion_id: UUID4
    destinatarios: List[str] = Field(..., description="Lista de direcciones de correo destino")
    asunto: str = Field(..., description="Asunto del correo")
    cuerpo: str = Field(..., description="Cuerpo del correo")
    copia: Optional[List[str]] = Field(None, description="Direcciones CC")
    copia_oculta: Optional[List[str]] = Field(None, description="Direcciones BCC")
    adjuntos: Optional[List[str]] = Field(None, description="Rutas de archivos adjuntos")
    tipo_documento: Optional[str] = Field(None, description="Tipo de documento adjunto (invoice, quote, etc.)")
    referencia_documento: Optional[str] = Field(None, description="Referencia al documento relacionado")