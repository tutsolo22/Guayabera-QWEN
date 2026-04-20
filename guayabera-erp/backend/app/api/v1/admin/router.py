"""
API routes for admin module
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.schemas.admin import (
    EmpresaCreate, EmpresaUpdate, EmpresaResponse,
    SucursalCreate, SucursalResponse,
    ConfiguracionResponse
)
from app.crud import admin as crud
from app.core.security import get_current_user

router = APIRouter()


# ============= EMPRESAS =============

@router.post("/empresas", response_model=EmpresaResponse, status_code=status.HTTP_201_CREATED)
async def crear_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    """Create new company"""
    # Check if RFC already exists
    existing = crud.get_empresa_by_rfc(db, empresa.rfc)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"RFC {empresa.rfc} ya está registrado"
        )
    
    return crud.create_empresa(db, empresa)


@router.get("/empresas", response_model=List[EmpresaResponse])
async def listar_empresas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all companies"""
    return crud.get_empresas(db, skip=skip, limit=limit)


@router.get("/empresas/{empresa_id}", response_model=EmpresaResponse)
async def obtener_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    """Get company by ID"""
    empresa = crud.get_empresa(db, empresa_id)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return empresa


@router.put("/empresas/{empresa_id}", response_model=EmpresaResponse)
async def actualizar_empresa(
    empresa_id: UUID,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    """Update company"""
    updated = crud.update_empresa(db, empresa_id, empresa)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    return updated


# ============= SUCURSALES =============

@router.post("/sucursales", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
async def crear_sucursal(
    sucursal: SucursalCreate,
    db: Session = Depends(get_db)
):
    """Create new branch"""
    # Verify empresa exists
    empresa = crud.get_empresa(db, sucursal.empresa_id)
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa no encontrada"
        )
    
    return crud.create_sucursal(db, sucursal)


@router.get("/empresas/{empresa_id}/sucursales", response_model=List[SucursalResponse])
async def listar_sucursales(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    """List all branches for a company"""
    return crud.get_sucursales_by_empresa(db, empresa_id)


# ============= CONFIGURACION =============

@router.get("/configuracion", response_model=List[ConfiguracionResponse])
async def listar_configuracion(
    modulo: str = None,
    db: Session = Depends(get_db)
):
    """List configurations"""
    return crud.get_configuraciones(db, modulo=modulo)


@router.get("/configuracion/{clave}", response_model=ConfiguracionResponse)
async def obtener_configuracion(
    clave: str,
    db: Session = Depends(get_db)
):
    """Get configuration by key"""
    config = crud.get_configuracion(db, clave)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuración '{clave}' no encontrada"
        )
    return config


@router.post("/configuracion", response_model=ConfiguracionResponse)
async def guardar_configuracion(
    clave: str,
    valor: str,
    tipo: str = "string",
    descripcion: str = None,
    modulo: str = "admin",
    db: Session = Depends(get_db)
):
    """Create or update configuration"""
    return crud.create_or_update_configuracion(
        db, clave, valor, tipo, descripcion, modulo
    )


# ============= CATÁLOGOS =============

@router.get("/monedas")
async def listar_monedas(db: Session = Depends(get_db)):
    """List active currencies"""
    return crud.get_monedas(db)


@router.get("/impuestos")
async def listar_impuestos(db: Session = Depends(get_db)):
    """List active taxes"""
    return crud.get_impuestos_activos(db)
