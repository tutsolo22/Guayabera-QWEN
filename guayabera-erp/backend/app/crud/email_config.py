"""
Email Configuration CRUD Operations: SMTP settings for sending invoices, quotes, etc.
Integrated with company configuration and includes test functionality
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.email_config import ConfiguracionCorreo, HistorialCorreo
from app.schemas.email_config import (
    ConfiguracionCorreoCreate, 
    ConfiguracionCorreoUpdate,
    EnviarCorreoRequest
)


def create_configuracion_correo(db: Session, config_data: ConfiguracionCorreoCreate) -> ConfiguracionCorreo:
    """Create a new email configuration"""
    # Check if there's already an active configuration for this company
    existing_active = db.query(ConfiguracionCorreo).filter(
        and_(
            ConfiguracionCorreo.empresa_id == config_data.empresa_id,
            ConfiguracionCorreo.activo == True
        )
    ).first()
    
    # If we're creating a new active config, deactivate the old one
    if config_data.activo and existing_active:
        existing_active.activo = False
    
    db_config = ConfiguracionCorreo(**config_data.model_dump(exclude={'contrasena_smtp'}))
    # Encrypt the password before storing it
    from cryptography.fernet import Fernet
    from app.core.config import settings
    f = Fernet(settings.SECRET_KEY.encode()[:44] + b'=')
    encrypted_password = f.encrypt(config_data.contrasena_smtp.encode()).decode()
    db_config.contrasena_smtp = encrypted_password
    
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_configuracion_correo(db: Session, config_id: UUID) -> Optional[ConfiguracionCorreo]:
    """Get an email configuration by ID"""
    return db.query(ConfiguracionCorreo).filter(ConfiguracionCorreo.id == config_id).first()


def get_configuracion_correo_by_empresa(db: Session, empresa_id: UUID) -> List[ConfiguracionCorreo]:
    """Get all email configurations for a specific company"""
    return db.query(ConfiguracionCorreo).filter(
        ConfiguracionCorreo.empresa_id == empresa_id
    ).all()


def get_configuracion_activa_by_empresa(db: Session, empresa_id: UUID) -> Optional[ConfiguracionCorreo]:
    """Get the active email configuration for a specific company"""
    return db.query(ConfiguracionCorreo).filter(
        and_(
            ConfiguracionCorreo.empresa_id == empresa_id,
            ConfiguracionCorreo.activo == True
        )
    ).first()


def update_configuracion_correo(
    db: Session, 
    config_id: UUID, 
    config_data: ConfiguracionCorreoUpdate
) -> Optional[ConfiguracionCorreo]:
    """Update an email configuration"""
    db_config = get_configuracion_correo(db, config_id)
    if db_config:
        # Handle password encryption if it's being updated
        update_data = config_data.model_dump(exclude_unset=True)
        if 'contrasena_smtp' in update_data:
            from cryptography.fernet import Fernet
            from app.core.config import settings
            f = Fernet(settings.SECRET_KEY.encode()[:44] + b'=')
            encrypted_password = f.encrypt(update_data['contrasena_smtp'].encode()).decode()
            update_data['contrasena_smtp'] = encrypted_password
            
            # Remove the plain password from update data
            del update_data['contrasena_smtp']
            
            # Since password changed, mark as unverified
            db_config.verificado = False
            db_config.ultima_prueba_fecha = None
            db_config.ultima_prueba_resultado = None
            db_config.ultima_prueba_detalle = None
        
        # If activating this config, deactivate others for the same company
        if update_data.get('activo', False):
            db.query(ConfiguracionCorreo).filter(
                and_(
                    ConfiguracionCorreo.empresa_id == db_config.empresa_id,
                    ConfiguracionCorreo.activo == True
                )
            ).update({"activo": False})
        
        for field, value in update_data.items():
            setattr(db_config, field, value)
        
        db.commit()
        db.refresh(db_config)
    return db_config


def delete_configuracion_correo(db: Session, config_id: UUID) -> bool:
    """Soft delete an email configuration"""
    db_config = get_configuracion_correo(db, config_id)
    if db_config:
        db_config.deleted_at = func.now()
        db_config.activo = False
        db.commit()
        return True
    return False


def update_test_result(
    db: Session, 
    config_id: UUID, 
    result: str, 
    details: Optional[str] = None
) -> Optional[ConfiguracionCorreo]:
    """Update the test result for an email configuration"""
    db_config = get_configuracion_correo(db, config_id)
    if db_config:
        db_config.ultima_prueba_fecha = func.now()
        db_config.ultima_prueba_resultado = result
        db_config.ultima_prueba_detalle = details
        if result == "success":
            db_config.verificado = True
        else:
            db_config.verificado = False
        db.commit()
        db.refresh(db_config)
    return db_config


def create_historial_correo(db: Session, request: EnviarCorreoRequest) -> HistorialCorreo:
    """Create an email history record"""
    historial = HistorialCorreo(
        configuracion_id=request.configuracion_id,
        destinatarios=", ".join(request.destinatarios),
        copia=", ".join(request.copia) if request.copia else None,
        copia_oculta=", ".join(request.copia_oculta) if request.copia_oculta else None,
        asunto=request.asunto,
        cuerpo=request.cuerpo,
        adjuntos=", ".join(request.adjuntos) if request.adjuntos else None,
        tipo_documento=request.tipo_documento,
        referencia_documento=request.referencia_documento
    )
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial


def get_historial_correo(db: Session, skip: int = 0, limit: int = 100, empresa_id: Optional[UUID] = None) -> List[HistorialCorreo]:
    """Get email history, optionally filtered by company"""
    query = db.query(HistorialCorreo).join(ConfiguracionCorreo)
    
    if empresa_id:
        query = query.filter(ConfiguracionCorreo.empresa_id == empresa_id)
    
    return query.order_by(HistorialCorreo.created_at.desc()).offset(skip).limit(limit).all()