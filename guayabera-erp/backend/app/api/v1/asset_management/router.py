"""
Asset Management API Router: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.asset_management import (
    CategoriaActivoCreate, CategoriaActivoUpdate, CategoriaActivoResponse,
    ActivoCreate, ActivoUpdate, ActivoResponse,
    MantenimientoActivoCreate, MantenimientoActivoUpdate, MantenimientoActivoResponse,
    DepreciacionActivoCreate, DepreciacionActivoUpdate, DepreciacionActivoResponse,
    HistorialAsignacionCreate, HistorialAsignacionUpdate, HistorialAsignacionResponse
)
from app.crud.asset_management import (
    create_categoria_activo, get_categoria_activo, get_categoria_activo_by_codigo,
    get_categorias_activos, update_categoria_activo, delete_categoria_activo,
    create_activo, get_activo, get_activo_by_codigo,
    get_activos, update_activo, delete_activo,
    create_mantenimiento_activo, get_mantenimiento_activo, get_mantenimientos_by_activo,
    get_mantenimientos_programados, update_mantenimiento_activo, delete_mantenimiento_activo,
    create_depreciacion_activo, get_depreciacion_activo, get_depreciaciones_by_activo,
    get_depreciaciones_by_fecha, update_depreciacion_activo, delete_depreciacion_activo,
    create_historial_asignacion, get_historial_asignacion, get_historial_by_activo,
    get_activos_by_empleado, update_historial_asignacion, delete_historial_asignacion
)

router = APIRouter(prefix="/asset-management", tags=["Asset Management"])

# ============================================================================
# ASSET CATEGORY ENDPOINTS
# ============================================================================

@router.post("/categories/", response_model=CategoriaActivoResponse)
def create_asset_category(categoria: CategoriaActivoCreate, db: Session = Depends(get_db)):
    """Create a new asset category"""
    try:
        return create_categoria_activo(db=db, categoria_data=categoria)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/categories/{categoria_id}", response_model=CategoriaActivoResponse)
def get_asset_category(categoria_id: str, db: Session = Depends(get_db)):
    """Get an asset category by ID"""
    categoria = get_categoria_activo(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset category not found"
        )
    return categoria


@router.get("/categories/code/{codigo}", response_model=CategoriaActivoResponse)
def get_asset_category_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get an asset category by code"""
    categoria = get_categoria_activo_by_codigo(db, codigo)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset category not found"
        )
    return categoria


@router.get("/categories/", response_model=List[CategoriaActivoResponse])
def get_asset_categories(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of asset categories, optionally filtered"""
    return get_categorias_activos(db, skip, limit, activo)


@router.put("/categories/{categoria_id}", response_model=CategoriaActivoResponse)
def update_asset_category(
    categoria_id: str, 
    categoria_data: CategoriaActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an asset category"""
    updated_categoria = update_categoria_activo(
        db=db, 
        categoria_id=categoria_id, 
        categoria_data=categoria_data
    )
    if not updated_categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset category not found"
        )
    return updated_categoria


@router.delete("/categories/{categoria_id}")
def delete_asset_category(categoria_id: str, db: Session = Depends(get_db)):
    """Soft delete an asset category"""
    success = delete_categoria_activo(db=db, categoria_id=categoria_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset category not found"
        )
    return {"message": "Asset category deactivated successfully"}


# ============================================================================
# ASSET ENDPOINTS
# ============================================================================

@router.post("/assets/", response_model=ActivoResponse)
def create_asset(activo: ActivoCreate, db: Session = Depends(get_db)):
    """Create a new fixed asset"""
    try:
        return create_activo(db=db, activo_data=activo)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/assets/{activo_id}", response_model=ActivoResponse)
def get_asset(activo_id: str, db: Session = Depends(get_db)):
    """Get a fixed asset by ID"""
    activo = get_activo(db, activo_id)
    if not activo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixed asset not found"
        )
    return activo


@router.get("/assets/code/{codigo}", response_model=ActivoResponse)
def get_asset_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a fixed asset by code"""
    activo = get_activo_by_codigo(db, codigo)
    if not activo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    cat_uuid = UUID(categoria_id) if categoria_id else None
    dept_uuid = UUID(departamento_id) if departamento_id else None
    return get_activos(db, skip, limit, estado, tipo, cat_uuid, dept_uuid)


@router.put("/assets/{activo_id}", response_model=ActivoResponse)
def update_asset(
    activo_id: str, 
    activo_data: ActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a fixed asset"""
    updated_activo = update_activo(
        db=db, 
        activo_id=activo_id, 
        activo_data=activo_data
    )
    if not updated_activo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixed asset not found"
        )
    return updated_activo


@router.delete("/assets/{activo_id}")
def delete_asset(activo_id: str, db: Session = Depends(get_db)):
    """Soft delete a fixed asset"""
    success = delete_activo(db=db, activo_id=activo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fixed asset not found"
        )
    return {"message": "Fixed asset deactivated successfully"}


# ============================================================================
# ASSET MAINTENANCE ENDPOINTS
# ============================================================================

@router.post("/maintenance/", response_model=MantenimientoActivoResponse)
def create_asset_maintenance(mantenimiento: MantenimientoActivoCreate, db: Session = Depends(get_db)):
    """Create a new asset maintenance record"""
    return create_mantenimiento_activo(db=db, mantenimiento_data=mantenimiento)


@router.get("/maintenance/{mantenimiento_id}", response_model=MantenimientoActivoResponse)
def get_asset_maintenance(mantenimiento_id: str, db: Session = Depends(get_db)):
    """Get an asset maintenance record by ID"""
    mantenimiento = get_mantenimiento_activo(db, mantenimiento_id)
    if not mantenimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset maintenance record not found"
        )
    return mantenimiento


@router.get("/assets/{activo_id}/maintenance", response_model=List[MantenimientoActivoResponse])
def get_maintenance_by_asset(
    activo_id: str, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all maintenance records for a specific asset"""
    return get_mantenimientos_by_activo(db, activo_id, skip, limit, estado)


@router.get("/maintenance/scheduled", response_model=List[MantenimientoActivoResponse])
def get_scheduled_maintenance(
    fecha_inicio: date,
    fecha_fin: date,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all scheduled maintenance records within a date range"""
    return get_mantenimientos_programados(db, fecha_inicio, fecha_fin, skip, limit)


@router.put("/maintenance/{mantenimiento_id}", response_model=MantenimientoActivoResponse)
def update_asset_maintenance(
    mantenimiento_id: str, 
    mantenimiento_data: MantenimientoActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an asset maintenance record"""
    updated_mantenimiento = update_mantenimiento_activo(
        db=db, 
        mantenimiento_id=mantenimiento_id, 
        mantenimiento_data=mantenimiento_data
    )
    if not updated_mantenimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset maintenance record not found"
        )
    return updated_mantenimiento


@router.delete("/maintenance/{mantenimiento_id}")
def delete_asset_maintenance(mantenimiento_id: str, db: Session = Depends(get_db)):
    """Delete an asset maintenance record"""
    success = delete_mantenimiento_activo(db=db, mantenimiento_id=mantenimiento_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset maintenance record not found"
        )
    return {"message": "Asset maintenance record deleted successfully"}


# ============================================================================
# ASSET DEPRECIATION ENDPOINTS
# ============================================================================

@router.post("/depreciation/", response_model=DepreciacionActivoResponse)
def create_asset_depreciation(depreciacion: DepreciacionActivoCreate, db: Session = Depends(get_db)):
    """Create a new asset depreciation record"""
    return create_depreciacion_activo(db=db, depreciacion_data=depreciacion)


@router.get("/depreciation/{depreciacion_id}", response_model=DepreciacionActivoResponse)
def get_asset_depreciation(depreciacion_id: str, db: Session = Depends(get_db)):
    """Get an asset depreciation record by ID"""
    depreciacion = get_depreciacion_activo(db, depreciacion_id)
    if not depreciacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset depreciation record not found"
        )
    return depreciacion


@router.get("/assets/{activo_id}/depreciation", response_model=List[DepreciacionActivoResponse])
def get_depreciation_by_asset(
    activo_id: str, 
    anio: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all depreciation records for a specific asset"""
    return get_depreciaciones_by_activo(db, activo_id, anio)


@router.get("/depreciation/by-date", response_model=List[DepreciacionActivoResponse])
def get_depreciation_by_date(
    anio: int, 
    mes: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all depreciation records for a specific month/year"""
    return get_depreciaciones_by_fecha(db, anio, mes)


@router.put("/depreciation/{depreciacion_id}", response_model=DepreciacionActivoResponse)
def update_asset_depreciation(
    depreciacion_id: str, 
    depreciacion_data: DepreciacionActivoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an asset depreciation record"""
    updated_depreciacion = update_depreciacion_activo(
        db=db, 
        depreciacion_id=depreciacion_id, 
        depreciacion_data=depreciacion_data
    )
    if not updated_depreciacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset depreciation record not found"
        )
    return updated_depreciacion


@router.delete("/depreciation/{depreciacion_id}")
def delete_asset_depreciation(depreciacion_id: str, db: Session = Depends(get_db)):
    """Delete an asset depreciation record"""
    success = delete_depreciacion_activo(db=db, depreciacion_id=depreciacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset depreciation record not found"
        )
    return {"message": "Asset depreciation record deleted successfully"}


# ============================================================================
# ASSIGNMENT HISTORY ENDPOINTS
# ============================================================================

@router.post("/assignment-history/", response_model=HistorialAsignacionResponse)
def create_assignment_history(historial: HistorialAsignacionCreate, db: Session = Depends(get_db)):
    """Create a new asset assignment history record"""
    return create_historial_asignacion(db=db, historial_data=historial)


@router.get("/assignment-history/{historial_id}", response_model=HistorialAsignacionResponse)
def get_assignment_history(historial_id: str, db: Session = Depends(get_db)):
    """Get an asset assignment history record by ID"""
    historial = get_historial_asignacion(db, historial_id)
    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset assignment history record not found"
        )
    return historial


@router.get("/assets/{activo_id}/assignment-history", response_model=List[HistorialAsignacionResponse])
def get_assignment_history_by_asset(
    activo_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all assignment history records for a specific asset"""
    return get_historial_by_activo(db, activo_id, skip, limit)


@router.get("/employee-assets/{empleado_id}", response_model=List[ActivoResponse])
def get_assets_by_employee(empleado_id: str, db: Session = Depends(get_db)):
    """Get all assets currently assigned to a specific employee"""
    return get_activos_by_empleado(db, empleado_id)


@router.put("/assignment-history/{historial_id}", response_model=HistorialAsignacionResponse)
def update_assignment_history(
    historial_id: str, 
    historial_data: HistorialAsignacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update an asset assignment history record"""
    updated_historial = update_historial_asignacion(
        db=db, 
        historial_id=historial_id, 
        historial_data=historial_data
    )
    if not updated_historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset assignment history record not found"
        )
    return updated_historial


@router.delete("/assignment-history/{historial_id}")
def delete_assignment_history(historial_id: str, db: Session = Depends(get_db)):
    """Delete an asset assignment history record"""
    success = delete_historial_asignacion(db=db, historial_id=historial_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset assignment history record not found"
        )
    return {"message": "Asset assignment history record deleted successfully"}