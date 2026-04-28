from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.maintenance import (
    EquipoCreate, EquipoUpdate, EquipoResponse,
    OrdenMantenimientoCreate, OrdenMantenimientoUpdate, OrdenMantenimientoResponse,
    HistorialMantenimientoCreate, HistorialMantenimientoUpdate, HistorialMantenimientoResponse,
    PlanMantenimientoCreate, PlanMantenimientoUpdate, PlanMantenimientoResponse
)
from app.crud.maintenance import (
    create_equipo, get_equipo, get_equipos, update_equipo, delete_equipo,
    create_orden_mantenimiento, get_orden_mantenimiento, get_ordenes_mantenimiento, update_orden_mantenimiento,
    create_historial_mantenimiento, get_historial_mantenimiento, get_historial_mantenimiento_by_orden,
    create_plan_mantenimiento, get_plan_mantenimiento, get_planes_mantenimiento_activos, update_plan_mantenimiento
)

router = APIRouter()


# ============================================================================
# ENDPOINTS PARA EQUIPOS
# ============================================================================

@router.post("/equipos", response_model=EquipoResponse)
def create_equipo_endpoint(
    equipo_data: EquipoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_equipo(db, equipo_data)


@router.get("/equipos/{equipo_id}", response_model=EquipoResponse)
def get_equipo_endpoint(
    equipo_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    equipo = get_equipo(db, UUID(equipo_id))
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.get("/equipos", response_model=List[EquipoResponse])
def get_equipos_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_equipos(db, skip, limit)


@router.put("/equipos/{equipo_id}", response_model=EquipoResponse)
def update_equipo_endpoint(
    equipo_id: str,
    equipo_data: EquipoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_equipo = update_equipo(db, UUID(equipo_id), equipo_data)
    if not updated_equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return updated_equipo


@router.delete("/equipos/{equipo_id}")
def delete_equipo_endpoint(
    equipo_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_equipo(db, UUID(equipo_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return {"message": "Equipo eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA ORDENES DE MANTENIMIENTO
# ============================================================================

@router.post("/ordenes-mantenimiento", response_model=OrdenMantenimientoResponse)
def create_orden_mantenimiento_endpoint(
    orden_data: OrdenMantenimientoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_orden_mantenimiento(db, orden_data)


@router.get("/ordenes-mantenimiento/{orden_id}", response_model=OrdenMantenimientoResponse)
def get_orden_mantenimiento_endpoint(
    orden_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    orden = get_orden_mantenimiento(db, UUID(orden_id))
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de mantenimiento no encontrada")
    return orden


@router.get("/ordenes-mantenimiento", response_model=List[OrdenMantenimientoResponse])
def get_ordenes_mantenimiento_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_ordenes_mantenimiento(db, skip, limit)


@router.put("/ordenes-mantenimiento/{orden_id}", response_model=OrdenMantenimientoResponse)
def update_orden_mantenimiento_endpoint(
    orden_id: str,
    orden_data: OrdenMantenimientoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_orden = update_orden_mantenimiento(db, UUID(orden_id), orden_data)
    if not updated_orden:
        raise HTTPException(status_code=404, detail="Orden de mantenimiento no encontrada")
    return updated_orden


# ============================================================================
# ENDPOINTS PARA HISTORIAL DE MANTENIMIENTO
# ============================================================================

@router.post("/historial-mantenimiento", response_model=HistorialMantenimientoResponse)
def create_historial_mantenimiento_endpoint(
    historial_data: HistorialMantenimientoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_historial_mantenimiento(db, historial_data)


@router.get("/historial-mantenimiento/{historial_id}", response_model=HistorialMantenimientoResponse)
def get_historial_mantenimiento_endpoint(
    historial_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    historial = get_historial_mantenimiento(db, UUID(historial_id))
    if not historial:
        raise HTTPException(status_code=404, detail="Registro de historial no encontrado")
    return historial


@router.get("/historial-mantenimiento/orden/{orden_id}", response_model=List[HistorialMantenimientoResponse])
def get_historial_by_orden_endpoint(
    orden_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_historial_mantenimiento_by_orden(db, UUID(orden_id), skip, limit)


# ============================================================================
# ENDPOINTS PARA PLANES DE MANTENIMIENTO
# ============================================================================

@router.post("/planes-mantenimiento", response_model=PlanMantenimientoResponse)
def create_plan_mantenimiento_endpoint(
    plan_data: PlanMantenimientoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_plan_mantenimiento(db, plan_data)


@router.get("/planes-mantenimiento/{plan_id}", response_model=PlanMantenimientoResponse)
def get_plan_mantenimiento_endpoint(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    plan = get_plan_mantenimiento(db, UUID(plan_id))
    if not plan:
        raise HTTPException(status_code=404, detail="Plan de mantenimiento no encontrado")
    return plan


@router.get("/planes-mantenimiento", response_model=List[PlanMantenimientoResponse])
def get_planes_mantenimiento_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_planes_mantenimiento_activos(db, skip, limit)


@router.put("/planes-mantenimiento/{plan_id}", response_model=PlanMantenimientoResponse)
def update_plan_mantenimiento_endpoint(
    plan_id: str,
    plan_data: PlanMantenimientoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_plan = update_plan_mantenimiento(db, UUID(plan_id), plan_data)
    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan de mantenimiento no encontrado")
    return updated_plan