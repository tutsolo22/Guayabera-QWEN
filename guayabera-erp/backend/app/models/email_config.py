"""
Email Configuration Models: SMTP settings for sending invoices, quotes, etc.
Integrated with company configuration and includes test functionality
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Integer, CheckConstraint)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ConfiguracionCorreo(Base):
    """Email configuration - Configuración de correo electrónico"""
    __tablename__ = "conf_correo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Company association
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("admin_empresa.id"), nullable=False)
    
    # SMTP configuration
    servidor_smtp = Column(String(255), nullable=False)  # e.g., smtp.gmail.com
    puerto_smtp = Column(Integer, default=587)  # Common ports: 587, 465, 25
    seguridad_smtp = Column(String(20), default="TLS")  # TLS, SSL, None
    nombre_remitente = Column(String(255))  # Display name for sender
    correo_remitente = Column(String(255), nullable=False)  # Sender email address
    usuario_smtp = Column(String(255), nullable=False)  # SMTP username
    contrasena_smtp = Column(String(255), nullable=False)  # Encrypted SMTP password
    
    # Configuration status
    activo = Column(Boolean, default=True)  # Whether this config is active
    verificado = Column(Boolean, default=False)  # Whether the config was tested successfully
    
    # Test tracking
    ultima_prueba_fecha = Column(DateTime(timezone=True))
    ultima_prueba_resultado = Column(String(50))  # Success, failure, error
    ultima_prueba_detalle = Column(Text)  # Details about the test result
    
    # Templates
    asunto_predeterminado = Column(String(500))  # Default subject for emails
    cuerpo_predeterminado = Column(Text)  # Default body for emails
    
    # Usage flags
    habilitado_para_facturas = Column(Boolean, default=True)  # Enable for invoices
    habilitado_para_cotizaciones = Column(Boolean, default=True)  # Enable for quotes
    habilitado_para_notificaciones = Column(Boolean, default=True)  # Enable for notifications
    habilitado_para_documentos = Column(Boolean, default=True)  # Enable for documents
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    empresa = relationship("Empresa", back_populates="configuraciones_correo")


class HistorialCorreo(Base):
    """Email sending history - Historial de envío de correos"""
    __tablename__ = "hist_correo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Configuration used
    configuracion_id = Column(UUID(as_uuid=True), ForeignKey("conf_correo.id"), nullable=False)
    
    # Recipients
    destinatarios = Column(Text, nullable=False)  # Comma-separated email addresses
    copia = Column(Text)  # CC recipients
    copia_oculta = Column(Text)  # BCC recipients
    
    # Email content
    asunto = Column(String(500), nullable=False)
    cuerpo = Column(Text, nullable=False)
    adjuntos = Column(Text)  # Paths to attachments (comma-separated)
    
    # Sending status
    enviado = Column(Boolean, default=False)
    fecha_envio = Column(DateTime(timezone=True))
    error_detalle = Column(Text)
    
    # Tracking
    tipo_documento = Column(String(50))  # invoice, quote, notification, etc.
    referencia_documento = Column(String(100))  # ID of the related document
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    configuracion = relationship("ConfiguracionCorreo")