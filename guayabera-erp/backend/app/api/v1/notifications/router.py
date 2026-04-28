"""
Notification System API Router: User notifications, tasks, and tracking
Specialized for ERP system notifications
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.notifications import (
    NotificacionCreate, NotificacionUpdate, NotificacionResponse,
    ComentarioNotificacionCreate, ComentarioNotificacionResponse,
    ConfiguracionNotificacionCreate, ConfiguracionNotificacionUpdate, ConfiguracionNotificacionResponse,
    HistorialNotificacionCreate, HistorialNotificacionResponse
)
from app.crud.notifications import (
    create_notificacion, get_notificacion, get_notificaciones_by_destinatario,
    get_notificaciones_by_estado, get_notificaciones_pendientes, update_notificacion,
    marcar_notificacion_leida, marcar_notificacion_procesada, marcar_notificacion_cerrada,
    delete_notificacion,
    create_comentario_notificacion, get_comentario_notificacion, get_comentarios_by_notificacion,
    update_comentario_notificacion, delete_comentario_notificacion,
    create_configuracion_notificacion, get_configuracion_notificacion, update_configuracion_notificacion,
    delete_configuracion_notificacion,
    create_historial_notificacion, get_historial_notificacion, get_historial_by_notificacion
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

@router.post("/", response_model=NotificacionResponse)
def create_notification(notificacion: NotificacionCreate, db: Session = Depends(get_db)):
    """Create a new notification"""
    return create_notificacion(db=db, notificacion_data=notificacion)


@router.get("/{notificacion_id}", response_model=NotificacionResponse)
def get_notification(notificacion_id: str, db: Session = Depends(get_db)):
    """Get a notification by ID"""
    notificacion = get_notificacion(db, notificacion_id)
    if not notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return notificacion


@router.get("/user/{destinatario_id}", response_model=List[NotificacionResponse])
def get_notifications_by_user(
    destinatario_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get notifications for a specific user"""
    return get_notificaciones_by_destinatario(db, destinatario_id, skip, limit)


@router.get("/user/{destinatario_id}/pending", response_model=List[NotificacionResponse])
def get_pending_notifications(
    destinatario_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get pending notifications for a specific user"""
    return get_notificaciones_pendientes(db, destinatario_id, skip, limit)


@router.get("/user/{destinatario_id}/state/{estado}", response_model=List[NotificacionResponse])
def get_notifications_by_user_and_state(
    destinatario_id: str, 
    estado: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get notifications for a specific user by state"""
    return get_notificaciones_by_estado(db, destinatario_id, estado, skip, limit)


@router.put("/{notificacion_id}", response_model=NotificacionResponse)
def update_notification(
    notificacion_id: str, 
    notificacion_data: NotificacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a notification"""
    updated_notificacion = update_notificacion(
        db=db, 
        notificacion_id=notificacion_id, 
        notificacion_data=notificacion_data
    )
    if not updated_notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return updated_notificacion


@router.put("/{notificacion_id}/mark-read", response_model=NotificacionResponse)
def mark_notification_read(notificacion_id: str, usuario_id: str, db: Session = Depends(get_db)):
    """Mark a notification as read"""
    updated_notificacion = marcar_notificacion_leida(db=db, notificacion_id=notificacion_id, usuario_id=usuario_id)
    if not updated_notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return updated_notificacion


@router.put("/{notificacion_id}/mark-processed", response_model=NotificacionResponse)
def mark_notification_processed(notificacion_id: str, usuario_id: str, db: Session = Depends(get_db)):
    """Mark a notification as processed"""
    updated_notificacion = marcar_notificacion_procesada(db=db, notificacion_id=notificacion_id, usuario_id=usuario_id)
    if not updated_notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return updated_notificacion


@router.put("/{notificacion_id}/mark-closed", response_model=NotificacionResponse)
def mark_notification_closed(notificacion_id: str, usuario_id: str, db: Session = Depends(get_db)):
    """Mark a notification as closed"""
    updated_notificacion = marcar_notificacion_cerrada(db=db, notificacion_id=notificacion_id, usuario_id=usuario_id)
    if not updated_notificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return updated_notificacion


@router.delete("/{notificacion_id}")
def delete_notification(notificacion_id: str, db: Session = Depends(get_db)):
    """Delete a notification (soft delete)"""
    success = delete_notificacion(db=db, notificacion_id=notificacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    return {"message": "Notification deleted successfully"}


# ============================================================================
# NOTIFICATION COMMENT ENDPOINTS
# ============================================================================

@router.post("/comments/", response_model=ComentarioNotificacionResponse)
def create_notification_comment(comentario: ComentarioNotificacionCreate, db: Session = Depends(get_db)):
    """Create a new notification comment"""
    return create_comentario_notificacion(db=db, comentario_data=comentario)


@router.get("/comments/{comentario_id}", response_model=ComentarioNotificacionResponse)
def get_notification_comment(comentario_id: str, db: Session = Depends(get_db)):
    """Get a notification comment by ID"""
    comentario = get_comentario_notificacion(db, comentario_id)
    if not comentario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification comment not found"
        )
    return comentario


@router.get("/notifications/{notificacion_id}/comments", response_model=List[ComentarioNotificacionResponse])
def get_notification_comments(notificacion_id: str, db: Session = Depends(get_db)):
    """Get all comments for a specific notification"""
    return get_comentarios_by_notificacion(db, notificacion_id)


@router.put("/comments/{comentario_id}", response_model=ComentarioNotificacionResponse)
def update_notification_comment(
    comentario_id: str, 
    comentario_data: ComentarioNotificacionCreate, 
    db: Session = Depends(get_db)
):
    """Update a notification comment"""
    updated_comentario = update_comentario_notificacion(
        db=db, 
        comentario_id=comentario_id, 
        comentario_data=comentario_data
    )
    if not updated_comentario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification comment not found"
        )
    return updated_comentario


@router.delete("/comments/{comentario_id}")
def delete_notification_comment(comentario_id: str, db: Session = Depends(get_db)):
    """Delete a notification comment"""
    success = delete_comentario_notificacion(db=db, comentario_id=comentario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification comment not found"
        )
    return {"message": "Notification comment deleted successfully"}


# ============================================================================
# NOTIFICATION CONFIGURATION ENDPOINTS
# ============================================================================

@router.post("/settings/", response_model=ConfiguracionNotificacionResponse)
def create_notification_settings(config: ConfiguracionNotificacionCreate, db: Session = Depends(get_db)):
    """Create notification settings for a user"""
    return create_configuracion_notificacion(db=db, config_data=config)


@router.get("/settings/{empleado_id}", response_model=ConfiguracionNotificacionResponse)
def get_notification_settings(empleado_id: str, db: Session = Depends(get_db)):
    """Get notification settings for a user"""
    config = get_configuracion_notificacion(db, empleado_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification settings not found"
        )
    return config


@router.put("/settings/{empleado_id}", response_model=ConfiguracionNotificacionResponse)
def update_notification_settings(
    empleado_id: str, 
    config_data: ConfiguracionNotificacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update notification settings for a user"""
    updated_config = update_configuracion_notificacion(
        db=db, 
        empleado_id=empleado_id, 
        config_data=config_data
    )
    if not updated_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification settings not found"
        )
    return updated_config


@router.delete("/settings/{empleado_id}")
def delete_notification_settings(empleado_id: str, db: Session = Depends(get_db)):
    """Delete notification settings for a user"""
    success = delete_configuracion_notificacion(db=db, empleado_id=empleado_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification settings not found"
        )
    return {"message": "Notification settings deleted successfully"}


# ============================================================================
# NOTIFICATION HISTORY ENDPOINTS
# ============================================================================

@router.post("/history/", response_model=HistorialNotificacionResponse)
def create_notification_history(historial: HistorialNotificacionCreate, db: Session = Depends(get_db)):
    """Create a new notification history entry"""
    return create_historial_notificacion(db=db, historial_data=historial.dict())


@router.get("/history/{historial_id}", response_model=HistorialNotificacionResponse)
def get_notification_history(historial_id: str, db: Session = Depends(get_db)):
    """Get a notification history entry by ID"""
    historial = get_historial_notificacion(db, historial_id)
    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification history entry not found"
        )
    return historial


@router.get("/notifications/{notificacion_id}/history", response_model=List[HistorialNotificacionResponse])
def get_notification_history_entries(notificacion_id: str, db: Session = Depends(get_db)):
    """Get all history entries for a specific notification"""
    return get_historial_by_notificacion(db, notificacion_id)