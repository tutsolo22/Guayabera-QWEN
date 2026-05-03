"""
Notification System CRUD Operations: User notifications, tasks, and tracking
Specialized for ERP system notifications
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.notifications import (
    Notificacion, ComentarioNotificacion, 
    ConfiguracionNotificacion, HistorialNotificacion
)
from app.schemas.notifications import (
    NotificacionCreate, NotificacionUpdate,
    ComentarioNotificacionCreate,
    ConfiguracionNotificacionCreate, ConfiguracionNotificacionUpdate,
    HistorialNotificacionCreate
)


# ============================================================================
# NOTIFICATION CRUD
# ============================================================================

def create_notificacion(db: Session, notificacion_data: NotificacionCreate) -> Notificacion:
    """Create a new notification"""
    db_notificacion = Notificacion(**notificacion_data.model_dump())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    
    # Add to history
    create_historial_notificacion(
        db,
        {
            'notificacion_id': db_notificacion.id,
            'accion': 'enviado',
            'descripcion_accion': 'Notificación creada y enviada',
            'responsable_id': notificacion_data.remitente_id
        }
    )
    
    return db_notificacion


def get_notificacion(db: Session, notificacion_id: UUID) -> Optional[Notificacion]:
    """Get a notification by ID"""
    return db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()


def get_notificaciones_by_destinatario(db: Session, destinatario_id: UUID, skip: int = 0, limit: int = 100) -> List[Notificacion]:
    """Get notifications by recipient"""
    return db.query(Notificacion).filter(
        Notificacion.destinatario_id == destinatario_id,
        Notificacion.activa == True
    ).order_by(Notificacion.fecha_envio.desc()).offset(skip).limit(limit).all()


def get_notificaciones_by_estado(db: Session, destinatario_id: UUID, estado: str, skip: int = 0, limit: int = 100) -> List[Notificacion]:
    """Get notifications by recipient and state"""
    return db.query(Notificacion).filter(
        Notificacion.destinatario_id == destinatario_id,
        Notificacion.estado == estado,
        Notificacion.activa == True
    ).order_by(Notificacion.fecha_envio.desc()).offset(skip).limit(limit).all()


def get_notificaciones_pendientes(db: Session, destinatario_id: UUID, skip: int = 0, limit: int = 100) -> List[Notificacion]:
    """Get pending notifications for a recipient"""
    return db.query(Notificacion).filter(
        Notificacion.destinatario_id == destinatario_id,
        Notificacion.estado.in_(['pendiente', 'leida']),
        Notificacion.activa == True
    ).order_by(Notificacion.fecha_envio.desc()).offset(skip).limit(limit).all()


def update_notificacion(db: Session, notificacion_id: UUID, notificacion_data: NotificacionUpdate) -> Optional[Notificacion]:
    """Update a notification"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        update_data = notificacion_data.model_dump(exclude_unset=True)
        
        # Track state changes
        if 'estado' in update_data and update_data['estado'] != db_notificacion.estado:
            accion_descripcion = ""
            if update_data['estado'] == 'leida':
                accion_descripcion = 'Notificación marcada como leída'
                update_data['fecha_leido'] = func.now()
            elif update_data['estado'] == 'procesada':
                accion_descripcion = 'Notificación procesada'
                update_data['fecha_procesado'] = func.now()
            elif update_data['estado'] == 'cerrada':
                accion_descripcion = 'Notificación cerrada'
                update_data['fecha_cierre'] = func.now()
            
            # Add to history
            create_historial_notificacion(
                db,
                {
                    'notificacion_id': notificacion_id,
                    'accion': update_data['estado'],
                    'descripcion_accion': accion_descripcion,
                    'responsable_id': db_notificacion.destinatario_id
                }
            )
        
        for field, value in update_data.items():
            setattr(db_notificacion, field, value)
        
        db.commit()
        db.refresh(db_notificacion)
    return db_notificacion


def marcar_notificacion_leida(db: Session, notificacion_id: UUID, usuario_id: UUID) -> Optional[Notificacion]:
    """Mark a notification as read"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db_notificacion.estado = 'leida'
        db_notificacion.fecha_leido = func.now()
        db.commit()
        db.refresh(db_notificacion)
        
        # Add to history
        create_historial_notificacion(
            db,
            {
                'notificacion_id': notificacion_id,
                'accion': 'leida',
                'descripcion_accion': 'Notificación marcada como leída por el usuario',
                'responsable_id': usuario_id
            }
        )
    
    return db_notificacion


def marcar_notificacion_procesada(db: Session, notificacion_id: UUID, usuario_id: UUID) -> Optional[Notificacion]:
    """Mark a notification as processed"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db_notificacion.estado = 'procesada'
        db_notificacion.fecha_procesado = func.now()
        db.commit()
        db.refresh(db_notificacion)
        
        # Add to history
        create_historial_notificacion(
            db,
            {
                'notificacion_id': notificacion_id,
                'accion': 'procesada',
                'descripcion_accion': 'Notificación procesada por el usuario',
                'responsable_id': usuario_id
            }
        )
    
    return db_notificacion


def marcar_notificacion_cerrada(db: Session, notificacion_id: UUID, usuario_id: UUID) -> Optional[Notificacion]:
    """Mark a notification as closed"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db_notificacion.estado = 'cerrada'
        db_notificacion.fecha_cierre = func.now()
        db.commit()
        db.refresh(db_notificacion)
        
        # Add to history
        create_historial_notificacion(
            db,
            {
                'notificacion_id': notificacion_id,
                'accion': 'cerrada',
                'descripcion_accion': 'Notificación cerrada por el usuario',
                'responsable_id': usuario_id
            }
        )
    
    return db_notificacion


def delete_notificacion(db: Session, notificacion_id: UUID) -> bool:
    """Delete a notification (soft delete)"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db_notificacion.activa = False
        db_notificacion.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# NOTIFICATION COMMENT CRUD
# ============================================================================

def create_comentario_notificacion(db: Session, comentario_data: ComentarioNotificacionCreate) -> ComentarioNotificacion:
    """Create a new notification comment"""
    db_comentario = ComentarioNotificacion(**comentario_data.model_dump())
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario


def get_comentario_notificacion(db: Session, comentario_id: UUID) -> Optional[ComentarioNotificacion]:
    """Get a notification comment by ID"""
    return db.query(ComentarioNotificacion).filter(ComentarioNotificacion.id == comentario_id).first()


def get_comentarios_by_notificacion(db: Session, notificacion_id: UUID) -> List[ComentarioNotificacion]:
    """Get all comments for a specific notification"""
    return db.query(ComentarioNotificacion).filter(ComentarioNotificacion.notificacion_id == notificacion_id).all()


def update_comentario_notificacion(db: Session, comentario_id: UUID, comentario_data: ComentarioNotificacionCreate) -> Optional[ComentarioNotificacion]:
    """Update a notification comment"""
    db_comentario = get_comentario_notificacion(db, comentario_id)
    if db_comentario:
        update_data = comentario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comentario, field, value)
        db.commit()
        db.refresh(db_comentario)
    return db_comentario


def delete_comentario_notificacion(db: Session, comentario_id: UUID) -> bool:
    """Delete a notification comment"""
    db_comentario = get_comentario_notificacion(db, comentario_id)
    if db_comentario:
        db.delete(db_comentario)
        db.commit()
        return True
    return False


# ============================================================================
# NOTIFICATION CONFIGURATION CRUD
# ============================================================================

def create_configuracion_notificacion(db: Session, config_data: ConfiguracionNotificacionCreate) -> ConfiguracionNotificacion:
    """Create notification settings for a user"""
    db_config = ConfiguracionNotificacion(**config_data.model_dump())
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_configuracion_notificacion(db: Session, empleado_id: UUID) -> Optional[ConfiguracionNotificacion]:
    """Get notification settings for a user"""
    return db.query(ConfiguracionNotificacion).filter(ConfiguracionNotificacion.empleado_id == empleado_id).first()


def update_configuracion_notificacion(db: Session, empleado_id: UUID, config_data: ConfiguracionNotificacionUpdate) -> Optional[ConfiguracionNotificacion]:
    """Update notification settings for a user"""
    db_config = get_configuracion_notificacion(db, empleado_id)
    if db_config:
        update_data = config_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_config, field, value)
        db.commit()
        db.refresh(db_config)
    else:
        # Create new configuration if doesn't exist
        new_config = ConfiguracionNotificacionCreate(empleado_id=empleado_id, **config_data.model_dump(exclude_unset=True))
        db_config = create_configuracion_notificacion(db, new_config)
    return db_config


def delete_configuracion_notificacion(db: Session, empleado_id: UUID) -> bool:
    """Delete notification settings for a user"""
    db_config = get_configuracion_notificacion(db, empleado_id)
    if db_config:
        db.delete(db_config)
        db.commit()
        return True
    return False


# ============================================================================
# NOTIFICATION HISTORY CRUD
# ============================================================================

def create_historial_notificacion(db: Session, historial_data: dict) -> HistorialNotificacion:
    """Create a new notification history entry"""
    db_historial = HistorialNotificacion(**historial_data)
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


def get_historial_notificacion(db: Session, historial_id: UUID) -> Optional[HistorialNotificacion]:
    """Get a notification history entry by ID"""
    return db.query(HistorialNotificacion).filter(HistorialNotificacion.id == historial_id).first()


def get_historial_by_notificacion(db: Session, notificacion_id: UUID) -> List[HistorialNotificacion]:
    """Get all history for a specific notification"""
    return db.query(HistorialNotificacion).filter(HistorialNotificacion.notificacion_id == notificacion_id).order_by(HistorialNotificacion.fecha_accion).all()


def delete_old_notifications(db: Session, cutoff_date):
    """Delete notifications older than the specified date"""
    from datetime import datetime
    try:
        # Find notifications older than the cutoff date
        old_notifications = db.query(Notificacion).filter(
            Notificacion.fecha_envio < cutoff_date,
            Notificacion.activa == True  # Only consider active notifications
        ).all()
        
        deleted_count = 0
        for notification in old_notifications:
            # Soft delete the notification
            notification.activa = False
            notification.deleted_at = datetime.utcnow()
            deleted_count += 1
        
        db.commit()
        print(f"Cleaned up {deleted_count} old notifications")
        return deleted_count
    except Exception as e:
        print(f"Error during notification cleanup: {e}")
        db.rollback()
        return 0
