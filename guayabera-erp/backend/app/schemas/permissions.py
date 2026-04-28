"""
Permission Schemas: User permissions and role management for all ERP modules
Specialized for textile manufacturing companies
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMA
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ROLE SCHEMAS
# ============================================================================

class RolBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del rol")
    descripcion: Optional[str] = Field(None, description="Descripción del rol")
    tipo_rol: str = Field(..., description="Tipo de rol")
    es_predeterminado: bool = Field(default=False, description="¿Es un rol predeterminado?")
    activo: bool = Field(default=True, description="¿Está activo el rol?")


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    tipo_rol: Optional[str] = None
    es_predeterminado: Optional[bool] = None
    activo: Optional[bool] = None


class RolResponse(RolBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PERMISSION SCHEMAS
# ============================================================================

class PermisoBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del permiso")
    descripcion: Optional[str] = Field(None, description="Descripción del permiso")
    modulo: str = Field(..., max_length=50, description="Módulo al que pertenece el permiso")
    tipo: str = Field(..., description="Tipo de permiso")
    activo: bool = Field(default=True, description="¿Está activo el permiso?")


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    modulo: Optional[str] = Field(None, max_length=50)
    tipo: Optional[str] = None
    activo: Optional[bool] = None


class PermisoResponse(PermisoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ROLE-PERMISSION ASSOCIATION SCHEMAS
# ============================================================================

class PermisoRolBase(BaseModel):
    rol_id: UUID4
    permiso_id: UUID4
    activo: bool = Field(default=True, description="¿Está activa la asociación?")


class PermisoRolCreate(PermisoRolBase):
    pass


class PermisoRolUpdate(BaseModel):
    activo: Optional[bool] = None


class PermisoRolResponse(PermisoRolBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# USER-ROLE ASSOCIATION SCHEMAS
# ============================================================================

class UsuarioRolBase(BaseModel):
    usuario_id: UUID4
    rol_id: UUID4
    activo: bool = Field(default=True, description="¿Está activa la asociación?")


class UsuarioRolCreate(UsuarioRolBase):
    pass


class UsuarioRolUpdate(BaseModel):
    activo: Optional[bool] = None


class UsuarioRolResponse(UsuarioRolBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# NOTIFICATION SCHEMAS
# ============================================================================

class NotificacionBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título de la notificación")
    contenido: str = Field(..., description="Contenido de la notificación")
    tipo: str = Field(default="informacion", description="Tipo de notificación")
    destinatarios_tipo: str = Field(default="usuario", description="Tipo de destinatarios")
    destinatario_usuario_id: Optional[UUID4] = Field(None, description="ID del usuario destinatario")
    destinatario_rol_id: Optional[UUID4] = Field(None, description="ID del rol destinatario")
    leido: bool = Field(default=False, description="¿Ha sido leída la notificación?")
    enviado_correo: bool = Field(default=False, description="¿Se ha enviado por correo?")


class NotificacionCreate(NotificacionBase):
    pass


class NotificacionUpdate(BaseModel):
    leido: Optional[bool] = None
    enviado_correo: Optional[bool] = None


class NotificacionResponse(NotificacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True