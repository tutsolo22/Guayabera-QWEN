"""
Email Configuration API Router: SMTP settings for sending invoices, quotes, etc.
Integrated with company configuration and includes test functionality
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID as UUIDType

from app.core.database import get_db
from app.services.email_service import EmailService
from app.schemas.email_config import (
    ConfiguracionCorreoCreate,
    ConfiguracionCorreoUpdate,
    ConfiguracionCorreoResponse,
    ConfiguracionCorreoTest,
    HistorialCorreoResponse,
    EnviarCorreoRequest
)
from app.crud.email_config import (
    create_configuracion_correo,
    get_configuracion_correo,
    get_configuracion_correo_by_empresa,
    get_configuracion_activa_by_empresa,
    update_configuracion_correo,
    delete_configuracion_correo,
    update_test_result,
    create_historial_correo,
    get_historial_correo
)

router = APIRouter(prefix="/email-config", tags=["Email Configuration"])


@router.post("/", response_model=ConfiguracionCorreoResponse)
def create_email_config(
    config: ConfiguracionCorreoCreate,
    db: Session = Depends(get_db)
):
    """Create a new email configuration"""
    try:
        return create_configuracion_correo(db=db, config_data=config)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating email configuration: {str(e)}"
        )


@router.get("/{config_id}", response_model=ConfiguracionCorreoResponse)
def get_email_config(
    config_id: str,
    db: Session = Depends(get_db)
):
    """Get an email configuration by ID"""
    config = get_configuracion_correo(db, UUIDType(config_id))
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    return config


@router.get("/company/{empresa_id}", response_model=List[ConfiguracionCorreoResponse])
def get_configs_by_company(
    empresa_id: str,
    db: Session = Depends(get_db)
):
    """Get all email configurations for a specific company"""
    configs = get_configuracion_correo_by_empresa(db, UUIDType(empresa_id))
    return configs


@router.get("/active/company/{empresa_id}", response_model=Optional[ConfiguracionCorreoResponse])
def get_active_config_by_company(
    empresa_id: str,
    db: Session = Depends(get_db)
):
    """Get the active email configuration for a specific company"""
    config = get_configuracion_activa_by_empresa(db, UUIDType(empresa_id))
    if not config:
        return None
    return config


@router.put("/{config_id}", response_model=ConfiguracionCorreoResponse)
def update_email_config(
    config_id: str,
    config_data: ConfiguracionCorreoUpdate,
    db: Session = Depends(get_db)
):
    """Update an email configuration"""
    updated_config = update_configuracion_correo(
        db=db,
        config_id=UUIDType(config_id),
        config_data=config_data
    )
    if not updated_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    return updated_config


@router.delete("/{config_id}")
def delete_email_config(
    config_id: str,
    db: Session = Depends(get_db)
):
    """Delete an email configuration"""
    success = delete_configuracion_correo(db=db, config_id=UUIDType(config_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    return {"message": "Email configuration deleted successfully"}


@router.post("/test/")
def test_email_config(
    test_data: ConfiguracionCorreoTest,
    db: Session = Depends(get_db)
):
    """Test an email configuration by sending a test email"""
    config = get_configuracion_correo(db, test_data.id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    
    # Create email service instance
    email_service = EmailService(config)
    
    # Run the test
    result = email_service.test_connection(test_data.destinatario_prueba)
    
    # Update test result in database
    update_test_result(
        db=db,
        config_id=test_data.id,
        result=result["status"],
        details=result["message"]
    )
    
    return result


@router.post("/send-email/")
def send_email(
    request: EnviarCorreoRequest,
    db: Session = Depends(get_db)
):
    """Send an email using the specified configuration"""
    config = get_configuracion_correo(db, request.configuracion_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )
    
    # Create email service instance
    email_service = EmailService(config)
    
    # Send the email
    success = email_service.send_email(
        destinatarios=request.destinatarios,
        asunto=request.asunto,
        cuerpo=request.cuerpo,
        copia=request.copia,
        copia_oculta=request.copia_oculta,
        adjuntos=request.adjuntos
    )
    
    # Create history record
    historial = create_historial_correo(db, request)
    historial.enviado = success
    if success:
        historial.fecha_envio = historial.created_at
    else:
        historial.error_detalle = "Failed to send email"
    db.commit()
    
    if success:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email"
        )


@router.get("/history/", response_model=List[HistorialCorreoResponse])
def get_email_history(
    skip: int = 0,
    limit: int = 100,
    empresa_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get email sending history, optionally filtered by company"""
    empresa_uuid = UUIDType(empresa_id) if empresa_id else None
    return get_historial_correo(db, skip, limit, empresa_uuid)