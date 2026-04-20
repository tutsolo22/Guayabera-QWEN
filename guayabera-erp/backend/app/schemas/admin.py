"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ============= ADMIN SCHEMAS =============

class EmpresaBase(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13)
    nombre_fiscal: str = Field(..., min_length=3, max_length=200)
    nombre_comercial: Optional[str] = None
    regimen_fiscal: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: str = "México"
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nombre_comercial: Optional[str] = None
    regimen_fiscal: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None


class EmpresaResponse(EmpresaBase):
    id: UUID
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SucursalBase(BaseModel):
    nombre: str
    codigo: Optional[str] = None
    es_principal: bool = False
    calle: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None


class SucursalCreate(SucursalBase):
    empresa_id: UUID


class SucursalResponse(SucursalBase):
    id: UUID
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConfiguracionBase(BaseModel):
    clave: str
    valor: str
    tipo: str = "string"
    descripcion: Optional[str] = None
    modulo: str


class ConfiguracionResponse(ConfiguracionBase):
    id: UUID
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============= SECURITY SCHEMAS =============

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nombre: str
    apellidos: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = None
    apellidos: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    ultimo_acceso: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UsuarioResponse


class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class RolCreate(RolBase):
    permisos_ids: Optional[List[UUID]] = []


class RolResponse(RolBase):
    id: UUID
    es_sistema: bool
    activo: bool
    
    class Config:
        from_attributes = True


class PermisoBase(BaseModel):
    modulo: str
    accion: str
    descripcion: Optional[str] = None


class PermisoResponse(PermisoBase):
    id: UUID
    
    class Config:
        from_attributes = True


class AuditoriaResponse(BaseModel):
    id: UUID
    usuario_id: Optional[UUID] = None
    usuario_nombre: Optional[str] = None
    accion: str
    modulo: str
    entidad: str
    entidad_id: Optional[UUID] = None
    datos_anteriores: Optional[dict] = None
    datos_nuevos: Optional[dict] = None
    ip_address: Optional[str] = None
    nombre_maquina: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
