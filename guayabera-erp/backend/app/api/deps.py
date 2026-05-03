"""
API Dependencies Module
"""

from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.usuario import Usuario


def get_current_usuario_activo(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """Dependency to get the currently authenticated user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return current_user


def check_permiso(usuario: Usuario = Depends(get_current_usuario_activo)):
    """Dependency to check permissions for accessing protected endpoints"""
    # Placeholder for permission checking logic
    # This would typically check roles/permissions against the route being accessed
    return usuario