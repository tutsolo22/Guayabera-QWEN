from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.permissions import Rol, Permiso
from app.schemas.permissions import (
    RolCreate, RolUpdate, RolResponse,
    PermisoCreate, PermisoUpdate, PermisoResponse,
    PermisoRolCreate, PermisoRolUpdate, PermisoRolResponse,
    UsuarioRolCreate, UsuarioRolUpdate, UsuarioRolResponse,
    NotificacionCreate, NotificacionUpdate, NotificacionResponse
)
from app.crud.permissions import (
    create_rol, get_rol, get_rol_by_nombre, get_roles,
    update_rol, delete_rol,
    create_permiso, get_permiso, get_permiso_by_nombre, get_permisos,
    update_permiso, delete_permiso,
    create_permiso_rol, get_permiso_rol, get_permisos_by_rol, get_roles_by_permiso,
    update_permiso_rol, delete_permiso_rol,
    create_usuario_rol, get_usuario_rol, get_roles_by_usuario, get_usuarios_by_rol,
    update_usuario_rol, delete_usuario_rol,
    create_notificacion, get_notificacion, get_notificaciones_by_usuario, get_notificaciones_by_rol,
    update_notificacion, marcar_notificacion_leida, delete_notificacion
)

router = APIRouter()


# ============================================================================
# ROLE ENDPOINTS
# ============================================================================

@router.post("/roles", response_model=RolResponse)
def create_role_endpoint(
    rol_data: RolCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_rol(db, rol_data)


@router.get("/roles/{rol_id}", response_model=RolResponse)
def get_role_endpoint(
    rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    rol = get_rol(db, UUID(rol_id))
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol


@router.get("/roles", response_model=List[RolResponse])
def get_roles_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_roles(db, skip, limit)


@router.put("/roles/{rol_id}", response_model=RolResponse)
def update_role_endpoint(
    rol_id: str,
    rol_data: RolUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_rol = update_rol(db, UUID(rol_id), rol_data)
    if not updated_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return updated_rol


@router.delete("/roles/{rol_id}")
def delete_role_endpoint(
    rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_rol(db, UUID(rol_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado exitosamente"}


# ============================================================================
# PERMISSION ENDPOINTS
# ============================================================================

@router.post("/permisos", response_model=PermisoResponse)
def create_permission_endpoint(
    permiso_data: PermisoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_permiso(db, permiso_data)


@router.get("/permisos/{permiso_id}", response_model=PermisoResponse)
def get_permission_endpoint(
    permiso_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    permiso = get_permiso(db, UUID(permiso_id))
    if not permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso


@router.get("/permisos", response_model=List[PermisoResponse])
def get_permissions_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_permisos(db, skip, limit)


@router.put("/permisos/{permiso_id}", response_model=PermisoResponse)
def update_permission_endpoint(
    permiso_id: str,
    permiso_data: PermisoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_permiso = update_permiso(db, UUID(permiso_id), permiso_data)
    if not updated_permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return updated_permiso


@router.delete("/permisos/{permiso_id}")
def delete_permission_endpoint(
    permiso_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_permiso(db, UUID(permiso_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return {"message": "Permiso eliminado exitosamente"}


# ============================================================================
# ROLE-PERMISSION ASSOCIATION ENDPOINTS
# ============================================================================

@router.post("/permisos-roles", response_model=PermisoRolResponse)
def create_permission_role_endpoint(
    permiso_rol_data: PermisoRolCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_permiso_rol(db, permiso_rol_data)


@router.get("/permisos-roles/{permiso_rol_id}", response_model=PermisoRolResponse)
def get_permission_role_endpoint(
    permiso_rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    permiso_rol = get_permiso_rol(db, UUID(permiso_rol_id))
    if not permiso_rol:
        raise HTTPException(status_code=404, detail="Asociación permiso-rol no encontrada")
    return permiso_rol


@router.get("/permisos-roles/rol/{rol_id}", response_model=List[PermisoRolResponse])
def get_permissions_by_role_endpoint(
    rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_permisos_by_rol(db, UUID(rol_id))


@router.get("/permisos-roles/permiso/{permiso_id}", response_model=List[PermisoRolResponse])
def get_roles_by_permission_endpoint(
    permiso_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_roles_by_permiso(db, UUID(permiso_id))


@router.put("/permisos-roles/{permiso_rol_id}", response_model=PermisoRolResponse)
def update_permission_role_endpoint(
    permiso_rol_id: str,
    permiso_rol_data: PermisoRolUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_permiso_rol = update_permiso_rol(db, UUID(permiso_rol_id), permiso_rol_data)
    if not updated_permiso_rol:
        raise HTTPException(status_code=404, detail="Asociación permiso-rol no encontrada")
    return updated_permiso_rol


@router.delete("/permisos-roles/{permiso_rol_id}")
def delete_permission_role_endpoint(
    permiso_rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_permiso_rol(db, UUID(permiso_rol_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Asociación permiso-rol no encontrada")
    return {"message": "Asociación permiso-rol eliminada exitosamente"}


# ============================================================================
# USER-ROLE ASSOCIATION ENDPOINTS
# ============================================================================

@router.post("/usuarios-roles", response_model=UsuarioRolResponse)
def create_user_role_endpoint(
    usuario_rol_data: UsuarioRolCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_usuario_rol(db, usuario_rol_data)


@router.get("/usuarios-roles/{usuario_rol_id}", response_model=UsuarioRolResponse)
def get_user_role_endpoint(
    usuario_rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    usuario_rol = get_usuario_rol(db, UUID(usuario_rol_id))
    if not usuario_rol:
        raise HTTPException(status_code=404, detail="Asociación usuario-rol no encontrada")
    return usuario_rol


@router.get("/usuarios-roles/usuario/{usuario_id}", response_model=List[UsuarioRolResponse])
def get_roles_by_user_endpoint(
    usuario_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_roles_by_usuario(db, UUID(usuario_id))


@router.get("/usuarios-roles/rol/{rol_id}", response_model=List[UsuarioRolResponse])
def get_users_by_role_endpoint(
    rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_usuarios_by_rol(db, UUID(rol_id))


@router.put("/usuarios-roles/{usuario_rol_id}", response_model=UsuarioRolResponse)
def update_user_role_endpoint(
    usuario_rol_id: str,
    usuario_rol_data: UsuarioRolUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_usuario_rol = update_usuario_rol(db, UUID(usuario_rol_id), usuario_rol_data)
    if not updated_usuario_rol:
        raise HTTPException(status_code=404, detail="Asociación usuario-rol no encontrada")
    return updated_usuario_rol


@router.delete("/usuarios-roles/{usuario_rol_id}")
def delete_user_role_endpoint(
    usuario_rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_usuario_rol(db, UUID(usuario_rol_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Asociación usuario-rol no encontrada")
    return {"message": "Asociación usuario-rol eliminada exitosamente"}


# ============================================================================
# NOTIFICATION ENDPOINTS
# ============================================================================

@router.post("/notificaciones", response_model=NotificacionResponse)
def create_notification_endpoint(
    notificacion_data: NotificacionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_notificacion(db, notificacion_data)


@router.get("/notificaciones/{notificacion_id}", response_model=NotificacionResponse)
def get_notification_endpoint(
    notificacion_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    notificacion = get_notificacion(db, UUID(notificacion_id))
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return notificacion


@router.get("/notificaciones/usuario/{usuario_id}", response_model=List[NotificacionResponse])
def get_notifications_by_user_endpoint(
    usuario_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_notificaciones_by_usuario(db, UUID(usuario_id))


@router.get("/notificaciones/rol/{rol_id}", response_model=List[NotificacionResponse])
def get_notifications_by_role_endpoint(
    rol_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_notificaciones_by_rol(db, UUID(rol_id))


@router.put("/notificaciones/{notificacion_id}", response_model=NotificacionResponse)
def update_notification_endpoint(
    notificacion_id: str,
    notificacion_data: NotificacionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_notificacion = update_notificacion(db, UUID(notificacion_id), notificacion_data)
    if not updated_notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return updated_notificacion


@router.put("/notificaciones/{notificacion_id}/marcar-leida")
def mark_notification_read_endpoint(
    notificacion_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    notificacion = marcar_notificacion_leida(db, UUID(notificacion_id))
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"message": "Notificación marcada como leída"}


@router.delete("/notificaciones/{notificacion_id}")
def delete_notification_endpoint(
    notificacion_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_notificacion(db, UUID(notificacion_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    return {"message": "Notificación eliminada exitosamente"}