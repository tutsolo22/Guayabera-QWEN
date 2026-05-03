"""
Asset Management API Router: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from uuid import UUID
import uuid

from app.core.security import get_current_user
from app.core.database import get_db
from app.api.deps import get_current_usuario_activo, check_permiso
from app.models.asset_management import Activo, HistorialMantenimientoActivo, AsignacionActivo, ProveedorActivo, ContratoMantenimiento
from app.schemas.asset_management import (
    ActivoCreate, ActivoUpdate, ActivoResponse,
    MantenimientoActivoCreate, MantenimientoActivoUpdate, MantenimientoActivoResponse,
    HistorialAsignacionCreate, HistorialAsignacionUpdate, HistorialAsignacionResponse,
    ProveedorActivoCreate, ProveedorActivoUpdate, ProveedorActivoResponse,
    ContratoMantenimientoCreate, ContratoMantenimientoUpdate, ContratoMantenimientoResponse,
    MantenimientoRequest, MantenimientoResponse,
    DepreciacionResponse
)
from app.crud import asset_management as crud

router = APIRouter()

# ============================================================================
# ASSET ENDPOINTS
# ============================================================================

@router.post("/assets/", response_model=ActivoResponse)
def create_asset(activo: ActivoCreate, db: Session = Depends(get_db)):
    """Create a new fixed asset"""
    try:
        return crud.create_activo(db=db, activo_data=activo)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/assets/{activo_id}", response_model=ActivoResponse)
def get_asset(activo_id: str, db: Session = Depends(get_db)):
    """Get a fixed asset by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    activo = crud.get_activo(db, uuid_obj)
    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Fixed asset not found"
        )
    return activo


@router.get("/assets/", response_model=List[ActivoResponse])
def get_assets(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    categoria_id: Optional[str] = None,
    departamento_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of assets, optionally filtered"""
    try:
        cat_uuid = UUID(categoria_id) if categoria_id else None
        dept_uuid = UUID(departamento_id) if departamento_id else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid category or department ID format")
    
    return crud.get_activos(db, skip, limit, estado, tipo, cat_uuid, dept_uuid)


@router.put("/assets/{activo_id}", response_model=ActivoResponse)
def update_asset(
    activo_id: str, 
    activo_data: ActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a fixed asset"""
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    updated_activo = crud.update_activo(
        db=db, 
        activo_id=uuid_obj, 
        activo_data=activo_data
    )
    if not updated_activo:
        raise HTTPException(
            status_code=404,
            detail="Fixed asset not found"
        )
    return updated_activo


@router.delete("/assets/{activo_id}")
def delete_asset(activo_id: str, db: Session = Depends(get_db)):
    """Soft delete a fixed asset"""
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    success = crud.delete_activo(db=db, activo_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Fixed asset not found"
        )
    return {"message": "Fixed asset deactivated successfully"}


# ============================================================================
# ASSET MAINTENANCE ENDPOINTS
# ============================================================================

@router.post("/maintenance/", response_model=MantenimientoActivoResponse)
def create_maintenance(
    mantenimiento: MantenimientoActivoCreate,
    db: Session = Depends(get_db),
    current_usuario: dict = Depends(get_current_usuario_activo)
):
    check_permiso(current_usuario, "crear_mantenimiento")
    return crud.create_historial_mantenimiento(db=db, mantenimiento_data=mantenimiento)


@router.get("/maintenance/{mantenimiento_id}", response_model=MantenimientoActivoResponse)
def get_maintenance(
    mantenimiento_id: str,
    db: Session = Depends(get_db),
    current_usuario: dict = Depends(get_current_usuario_activo)
):
    check_permiso(current_usuario, "leer_mantenimiento")
    try:
        uuid_obj = UUID(mantenimiento_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid maintenance ID format")
    
    result = crud.get_historial_mantenimiento(db=db, mantenimiento_id=uuid_obj)
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return result


@router.get("/assets/{activo_id}/maintenance", response_model=List[MantenimientoActivoResponse])
def get_maintenance_by_asset(
    activo_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_usuario: dict = Depends(get_current_usuario_activo)
):
    check_permiso(current_usuario, "leer_mantenimiento")
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    return crud.get_historiales_by_activo(
        db=db, 
        activo_id=uuid_obj, 
        skip=skip, 
        limit=limit, 
        estado=estado
    )


@router.put("/maintenance/{mantenimiento_id}", response_model=MantenimientoActivoResponse)
def update_maintenance(
    mantenimiento_id: str,
    mantenimiento: MantenimientoActivoUpdate,
    db: Session = Depends(get_db),
    current_usuario: dict = Depends(get_current_usuario_activo)
):
    check_permiso(current_usuario, "actualizar_mantenimiento")
    try:
        uuid_obj = UUID(mantenimiento_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid maintenance ID format")
    
    result = crud.update_historial_mantenimiento(
        db=db, 
        mantenimiento_id=uuid_obj, 
        mantenimiento_data=mantenimiento
    )
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return result


@router.delete("/maintenance/{mantenimiento_id}")
def delete_asset_maintenance(mantenimiento_id: str, db: Session = Depends(get_db)):
    """Delete an asset maintenance record"""
    try:
        uuid_obj = UUID(mantenimiento_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid maintenance ID format")
    
    success = crud.delete_historial_mantenimiento(db=db, mantenimiento_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Asset maintenance record not found"
        )
    return {"message": "Asset maintenance record deleted successfully"}


@router.get("/maintenance/scheduled/", response_model=List[MantenimientoActivoResponse])
def get_scheduled_maintenance(
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_usuario: dict = Depends(get_current_usuario_activo)
):
    check_permiso(current_usuario, "leer_mantenimiento")
    return crud.get_mantenimientos_programados(
        db=db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        skip=skip,
        limit=limit
    )


# ============================================================================
# ASSET ASSIGNMENT ENDPOINTS
# ============================================================================

@router.post("/assignments/", response_model=HistorialAsignacionResponse)
def create_asset_assignment(asignacion: HistorialAsignacionCreate, db: Session = Depends(get_db)):
    """Create a new asset assignment record"""
    return crud.create_asignacion_activo(db=db, asignacion_data=asignacion)


@router.get("/assignments/{asignacion_id}", response_model=HistorialAsignacionResponse)
def get_asset_assignment(asignacion_id: str, db: Session = Depends(get_db)):
    """Get an asset assignment record by ID"""
    try:
        uuid_obj = UUID(asignacion_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assignment ID format")
    
    asignacion = crud.get_asignacion_activo(db, uuid_obj)
    if not asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asset assignment record not found"
        )
    return asignacion


@router.get("/assets/{activo_id}/assignments", response_model=List[HistorialAsignacionResponse])
def get_assignments_by_asset(
    activo_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all assignment records for a specific asset"""
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    return crud.get_asignaciones_by_activo(db, uuid_obj, skip, limit)


@router.get("/users/{usuario_id}/assignments", response_model=List[HistorialAsignacionResponse])
def get_assignments_by_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """Get all assignment records for a specific user"""
    try:
        uuid_obj = UUID(usuario_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    return crud.get_asignaciones_by_usuario(db, uuid_obj)


@router.put("/assignments/{asignacion_id}", response_model=HistorialAsignacionResponse)
def update_asset_assignment(
    asignacion_id: str, 
    asignacion_data: HistorialAsignacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update an asset assignment record"""
    try:
        uuid_obj = UUID(asignacion_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assignment ID format")
    
    updated_asignacion = crud.update_asignacion_activo(
        db=db, 
        asignacion_id=uuid_obj, 
        asignacion_data=asignacion_data
    )
    if not updated_asignacion:
        raise HTTPException(
            status_code=404,
            detail="Asset assignment record not found"
        )
    return updated_asignacion


@router.delete("/assignments/{asignacion_id}")
def delete_asset_assignment(asignacion_id: str, db: Session = Depends(get_db)):
    """Delete an asset assignment record"""
    try:
        uuid_obj = UUID(asignacion_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid assignment ID format")
    
    success = crud.delete_asignacion_activo(db=db, asignacion_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Asset assignment record not found"
        )
    return {"message": "Asset assignment record deleted successfully"}


# ============================================================================
# SUPPLIER ENDPOINTS
# ============================================================================

@router.post("/suppliers/", response_model=ProveedorActivoResponse)
def create_supplier(proveedor: ProveedorActivoCreate, db: Session = Depends(get_db)):
    """Create a new supplier"""
    return crud.create_proveedor(db=db, proveedor_data=proveedor)


@router.get("/suppliers/{proveedor_id}", response_model=ProveedorActivoResponse)
def get_supplier(proveedor_id: str, db: Session = Depends(get_db)):
    """Get a supplier by ID"""
    try:
        uuid_obj = UUID(proveedor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    proveedor = crud.get_proveedor(db, uuid_obj)
    if not proveedor:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )
    return proveedor


@router.get("/suppliers/", response_model=List[ProveedorActivoResponse])
def get_suppliers(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of suppliers"""
    return crud.get_proveedores(db, skip, limit, activo)


@router.put("/suppliers/{proveedor_id}", response_model=ProveedorActivoResponse)
def update_supplier(
    proveedor_id: str, 
    proveedor_data: ProveedorActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a supplier"""
    try:
        uuid_obj = UUID(proveedor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    updated_proveedor = crud.update_proveedor(
        db=db, 
        proveedor_id=uuid_obj, 
        proveedor_data=proveedor_data
    )
    if not updated_proveedor:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )
    return updated_proveedor


@router.delete("/suppliers/{proveedor_id}")
def delete_supplier(proveedor_id: str, db: Session = Depends(get_db)):
    """Delete a supplier"""
    try:
        uuid_obj = UUID(proveedor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    success = crud.delete_proveedor(db=db, proveedor_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )
    return {"message": "Supplier deleted successfully"}


# ============================================================================
# MAINTENANCE CONTRACT ENDPOINTS
# ============================================================================

@router.post("/maintenance-contracts/", response_model=ContratoMantenimientoResponse)
def create_maintenance_contract(contrato: ContratoMantenimientoCreate, db: Session = Depends(get_db)):
    """Create a new maintenance contract"""
    return crud.create_contrato_mantenimiento(db=db, contrato_data=contrato)


@router.get("/maintenance-contracts/{contrato_id}", response_model=ContratoMantenimientoResponse)
def get_maintenance_contract(contrato_id: str, db: Session = Depends(get_db)):
    """Get a maintenance contract by ID"""
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid contract ID format")
    
    contrato = crud.get_contrato_mantenimiento(db, uuid_obj)
    if not contrato:
        raise HTTPException(
            status_code=404,
            detail="Maintenance contract not found"
        )
    return contrato


@router.get("/assets/{activo_id}/maintenance-contracts", response_model=List[ContratoMantenimientoResponse])
def get_contracts_by_asset(
    activo_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all maintenance contracts for a specific asset"""
    try:
        uuid_obj = UUID(activo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid asset ID format")
    
    return crud.get_contratos_by_activo(db, uuid_obj, skip, limit)


@router.get("/suppliers/{proveedor_id}/maintenance-contracts", response_model=List[ContratoMantenimientoResponse])
def get_contracts_by_supplier(
    proveedor_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all maintenance contracts for a specific supplier"""
    try:
        uuid_obj = UUID(proveedor_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid supplier ID format")
    
    return crud.get_contratos_by_proveedor(db, uuid_obj, skip, limit)


@router.put("/maintenance-contracts/{contrato_id}", response_model=ContratoMantenimientoResponse)
def update_maintenance_contract(
    contrato_id: str, 
    contrato_data: ContratoMantenimientoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a maintenance contract"""
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid contract ID format")
    
    updated_contrato = crud.update_contrato_mantenimiento(
        db=db, 
        contrato_id=uuid_obj, 
        contrato_data=contrato_data
    )
    if not updated_contrato:
        raise HTTPException(
            status_code=404,
            detail="Maintenance contract not found"
        )
    return updated_contrato


@router.delete("/maintenance-contracts/{contrato_id}")
def delete_maintenance_contract(contrato_id: str, db: Session = Depends(get_db)):
    """Delete a maintenance contract"""
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid contract ID format")
    
    success = crud.delete_contrato_mantenimiento(db=db, contrato_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Maintenance contract not found"
        )
    return {"message": "Maintenance contract deleted successfully"}


# ============================================================================
# MAINTENANCE REGISTRATION ENDPOINTS
# ============================================================================

@router.post("/maintenance/register/", response_model=MantenimientoResponse)
def register_maintenance(mantenimiento: MantenimientoRequest, db: Session = Depends(get_db)):
    """Register a maintenance event"""
    return crud.registrar_mantenimiento(db=db, mantenimiento_request=mantenimiento)


# ============================================================================
# DEPRECIATION ENDPOINTS
# ============================================================================

@router.get("/depreciation/", response_model=List[DepreciacionResponse])
def get_depreciation(
    anio: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get depreciation records"""
    return crud.calcular_depreciacion_activos(db, anio, mes)