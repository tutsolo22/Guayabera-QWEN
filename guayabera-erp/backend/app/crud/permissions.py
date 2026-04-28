"""
Permission CRUD Operations: User permissions and role management for all ERP modules
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.permissions import (
    Rol, Permiso, PermisoRol, UsuarioRol, Notificacion
)
from app.schemas.permissions import (
    RolCreate, RolUpdate, RolResponse,
    PermisoCreate, PermisoUpdate, PermisoResponse,
    PermisoRolCreate, PermisoRolUpdate, PermisoRolResponse,
    UsuarioRolCreate, UsuarioRolUpdate, UsuarioRolResponse,
    NotificacionCreate, NotificacionUpdate, NotificacionResponse
)


# ============================================================================
# ROLE CRUD
# ============================================================================

def create_rol(db: Session, rol_data: RolCreate) -> Rol:
    """Create a new role"""
    db_rol = Rol(**rol_data.model_dump())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


def get_rol(db: Session, rol_id: UUID) -> Optional[Rol]:
    """Get a role by ID"""
    return db.query(Rol).filter(Rol.id == rol_id).first()


def get_rol_by_nombre(db: Session, nombre: str) -> Optional[Rol]:
    """Get a role by name"""
    return db.query(Rol).filter(Rol.nombre == nombre).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Rol]:
    """Get list of roles"""
    return db.query(Rol).offset(skip).limit(limit).all()


def update_rol(
    db: Session, 
    rol_id: UUID, 
    rol_data: RolUpdate
) -> Optional[Rol]:
    """Update a role"""
    db_rol = get_rol(db, rol_id)
    if db_rol:
        update_data = rol_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rol, field, value)
        db.commit()
        db.refresh(db_rol)
    return db_rol


def delete_rol(db: Session, rol_id: UUID) -> bool:
    """Delete a role"""
    db_rol = get_rol(db, rol_id)
    if db_rol:
        db.delete(db_rol)
        db.commit()
        return True
    return False


# ============================================================================
# PERMISSION CRUD
# ============================================================================

def create_permiso(db: Session, permiso_data: PermisoCreate) -> Permiso:
    """Create a new permission"""
    db_permiso = Permiso(**permiso_data.model_dump())
    db.add(db_permiso)
    db.commit()
    db.refresh(db_permiso)
    return db_permiso


def get_permiso(db: Session, permiso_id: UUID) -> Optional[Permiso]:
    """Get a permission by ID"""
    return db.query(Permiso).filter(Permiso.id == permiso_id).first()


def get_permiso_by_nombre(db: Session, nombre: str) -> Optional[Permiso]:
    """Get a permission by name"""
    return db.query(Permiso).filter(Permiso.nombre == nombre).first()


def get_permisos(db: Session, skip: int = 0, limit: int = 100) -> List[Permiso]:
    """Get list of permissions"""
    return db.query(Permiso).offset(skip).limit(limit).all()


def update_permiso(
    db: Session, 
    permiso_id: UUID, 
    permiso_data: PermisoUpdate
) -> Optional[Permiso]:
    """Update a permission"""
    db_permiso = get_permiso(db, permiso_id)
    if db_permiso:
        update_data = permiso_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permiso, field, value)
        db.commit()
        db.refresh(db_permiso)
    return db_permiso


def delete_permiso(db: Session, permiso_id: UUID) -> bool:
    """Delete a permission"""
    db_permiso = get_permiso(db, permiso_id)
    if db_permiso:
        db.delete(db_permiso)
        db.commit()
        return True
    return False


# ============================================================================
# ROLE-PERMISSION ASSOCIATION CRUD
# ============================================================================

def create_permiso_rol(db: Session, permiso_rol_data: PermisoRolCreate) -> PermisoRol:
    """Create a new role-permission association"""
    db_permiso_rol = PermisoRol(**permiso_rol_data.model_dump())
    db.add(db_permiso_rol)
    db.commit()
    db.refresh(db_permiso_rol)
    return db_permiso_rol


def get_permiso_rol(db: Session, permiso_rol_id: UUID) -> Optional[PermisoRol]:
    """Get a role-permission association by ID"""
    return db.query(PermisoRol).filter(PermisoRol.id == permiso_rol_id).first()


def get_permisos_by_rol(db: Session, rol_id: UUID) -> List[PermisoRol]:
    """Get all permissions for a specific role"""
    return db.query(PermisoRol).filter(PermisoRol.rol_id == rol_id).all()


def get_roles_by_permiso(db: Session, permiso_id: UUID) -> List[PermisoRol]:
    """Get all roles with a specific permission"""
    return db.query(PermisoRol).filter(PermisoRol.permiso_id == permiso_id).all()


def update_permiso_rol(
    db: Session, 
    permiso_rol_id: UUID, 
    permiso_rol_data: PermisoRolUpdate
) -> Optional[PermisoRol]:
    """Update a role-permission association"""
    db_permiso_rol = get_permiso_rol(db, permiso_rol_id)
    if db_permiso_rol:
        update_data = permiso_rol_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permiso_rol, field, value)
        db.commit()
        db.refresh(db_permiso_rol)
    return db_permiso_rol


def delete_permiso_rol(db: Session, permiso_rol_id: UUID) -> bool:
    """Delete a role-permission association"""
    db_permiso_rol = get_permiso_rol(db, permiso_rol_id)
    if db_permiso_rol:
        db.delete(db_permiso_rol)
        db.commit()
        return True
    return False


# ============================================================================
# USER-ROLE ASSOCIATION CRUD
# ============================================================================

def create_usuario_rol(db: Session, usuario_rol_data: UsuarioRolCreate) -> UsuarioRol:
    """Create a new user-role association"""
    db_usuario_rol = UsuarioRol(**usuario_rol_data.model_dump())
    db.add(db_usuario_rol)
    db.commit()
    db.refresh(db_usuario_rol)
    return db_usuario_rol


def get_usuario_rol(db: Session, usuario_rol_id: UUID) -> Optional[UsuarioRol]:
    """Get a user-role association by ID"""
    return db.query(UsuarioRol).filter(UsuarioRol.id == usuario_rol_id).first()


def get_roles_by_usuario(db: Session, usuario_id: UUID) -> List[UsuarioRol]:
    """Get all roles for a specific user"""
    return db.query(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id).all()


def get_usuarios_by_rol(db: Session, rol_id: UUID) -> List[UsuarioRol]:
    """Get all users with a specific role"""
    return db.query(UsuarioRol).filter(UsuarioRol.rol_id == rol_id).all()


def update_usuario_rol(
    db: Session, 
    usuario_rol_id: UUID, 
    usuario_rol_data: UsuarioRolUpdate
) -> Optional[UsuarioRol]:
    """Update a user-role association"""
    db_usuario_rol = get_usuario_rol(db, usuario_rol_id)
    if db_usuario_rol:
        update_data = usuario_rol_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_usuario_rol, field, value)
        db.commit()
        db.refresh(db_usuario_rol)
    return db_usuario_rol


def delete_usuario_rol(db: Session, usuario_rol_id: UUID) -> bool:
    """Delete a user-role association"""
    db_usuario_rol = get_usuario_rol(db, usuario_rol_id)
    if db_usuario_rol:
        db.delete(db_usuario_rol)
        db.commit()
        return True
    return False


# ============================================================================
# NOTIFICATION CRUD
# ============================================================================

def create_notificacion(db: Session, notificacion_data: NotificacionCreate) -> Notificacion:
    """Create a new notification"""
    db_notificacion = Notificacion(**notificacion_data.model_dump())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion


def get_notificacion(db: Session, notificacion_id: UUID) -> Optional[Notificacion]:
    """Get a notification by ID"""
    return db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()


def get_notificaciones_by_usuario(db: Session, usuario_id: UUID) -> List[Notificacion]:
    """Get all notifications for a specific user"""
    return db.query(Notificacion).filter(Notificacion.destinatario_usuario_id == usuario_id).all()


def get_notificaciones_by_rol(db: Session, rol_id: UUID) -> List[Notificacion]:
    """Get all notifications for a specific role"""
    return db.query(Notificacion).filter(Notificacion.destinatario_rol_id == rol_id).all()


def update_notificacion(
    db: Session, 
    notificacion_id: UUID, 
    notificacion_data: NotificacionUpdate
) -> Optional[Notificacion]:
    """Update a notification"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        update_data = notificacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notificacion, field, value)
        db.commit()
        db.refresh(db_notificacion)
    return db_notificacion


def marcar_notificacion_leida(db: Session, notificacion_id: UUID) -> Optional[Notificacion]:
    """Mark a notification as read"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db_notificacion.leido = True
        db.commit()
        db.refresh(db_notificacion)
    return db_notificacion


def delete_notificacion(db: Session, notificacion_id: UUID) -> bool:
    """Delete a notification"""
    db_notificacion = get_notificacion(db, notificacion_id)
    if db_notificacion:
        db.delete(db_notificacion)
        db.commit()
        return True
    return False