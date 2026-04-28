from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.maintenance import Equipo, OrdenMantenimiento, HistorialMantenimiento, PlanMantenimiento
from app.schemas.maintenance import (
    EquipoCreate, EquipoUpdate, EquipoResponse,
    OrdenMantenimientoCreate, OrdenMantenimientoUpdate, OrdenMantenimientoResponse,
    HistorialMantenimientoCreate, HistorialMantenimientoUpdate, HistorialMantenimientoResponse,
    PlanMantenimientoCreate, PlanMantenimientoUpdate, PlanMantenimientoResponse
)


def create_equipo(db: Session, equipo_data: EquipoCreate) -> Equipo:
    """Crear un nuevo equipo"""
    db_equipo = Equipo(**equipo_data.model_dump())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo


def get_equipo(db: Session, equipo_id: UUID) -> Optional[Equipo]:
    """Obtener un equipo por ID"""
    return db.query(Equipo).filter(Equipo.id == equipo_id).first()


def get_equipos(db: Session, skip: int = 0, limit: int = 100) -> List[Equipo]:
    """Obtener una lista de equipos"""
    return db.query(Equipo).filter(Equipo.activo == True).offset(skip).limit(limit).all()


def update_equipo(db: Session, equipo_id: UUID, equipo_data: EquipoUpdate) -> Optional[Equipo]:
    """Actualizar un equipo"""
    db_equipo = get_equipo(db, equipo_id)
    if db_equipo:
        update_data = equipo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_equipo, field, value)
        db.commit()
        db.refresh(db_equipo)
    return db_equipo


def delete_equipo(db: Session, equipo_id: UUID) -> bool:
    """Eliminar (desactivar) un equipo"""
    db_equipo = get_equipo(db, equipo_id)
    if db_equipo:
        db_equipo.activo = False
        db.commit()
        return True
    return False


def create_orden_mantenimiento(db: Session, orden_data: OrdenMantenimientoCreate) -> OrdenMantenimiento:
    """Crear una nueva orden de mantenimiento"""
    db_orden = OrdenMantenimiento(**orden_data.model_dump())
    db.add(db_orden)
    db.commit()
    db.refresh(db_orden)
    return db_orden


def get_orden_mantenimiento(db: Session, orden_id: UUID) -> Optional[OrdenMantenimiento]:
    """Obtener una orden de mantenimiento por ID"""
    return db.query(OrdenMantenimiento).filter(OrdenMantenimiento.id == orden_id).first()


def get_ordenes_mantenimiento(db: Session, skip: int = 0, limit: int = 100) -> List[OrdenMantenimiento]:
    """Obtener una lista de órdenes de mantenimiento"""
    return db.query(OrdenMantenimiento).offset(skip).limit(limit).all()


def update_orden_mantenimiento(
    db: Session, 
    orden_id: UUID, 
    orden_data: OrdenMantenimientoUpdate
) -> Optional[OrdenMantenimiento]:
    """Actualizar una orden de mantenimiento"""
    db_orden = get_orden_mantenimiento(db, orden_id)
    if db_orden:
        update_data = orden_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_orden, field, value)
        db.commit()
        db.refresh(db_orden)
    return db_orden


def create_historial_mantenimiento(
    db: Session, 
    historial_data: HistorialMantenimientoCreate
) -> HistorialMantenimiento:
    """Crear un nuevo registro en el historial de mantenimiento"""
    db_historial = HistorialMantenimiento(**historial_data.model_dump())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


def get_historial_mantenimiento(db: Session, historial_id: UUID) -> Optional[HistorialMantenimiento]:
    """Obtener un registro del historial de mantenimiento por ID"""
    return db.query(HistorialMantenimiento).filter(HistorialMantenimiento.id == historial_id).first()


def get_historial_mantenimiento_by_orden(
    db: Session, 
    orden_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[HistorialMantenimiento]:
    """Obtener historial de mantenimiento por orden"""
    return db.query(HistorialMantenimiento).filter(
        HistorialMantenimiento.orden_id == orden_id
    ).offset(skip).limit(limit).all()


def create_plan_mantenimiento(db: Session, plan_data: PlanMantenimientoCreate) -> PlanMantenimiento:
    """Crear un nuevo plan de mantenimiento"""
    db_plan = PlanMantenimiento(**plan_data.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_plan_mantenimiento(db: Session, plan_id: UUID) -> Optional[PlanMantenimiento]:
    """Obtener un plan de mantenimiento por ID"""
    return db.query(PlanMantenimiento).filter(PlanMantenimiento.id == plan_id).first()


def get_planes_mantenimiento_activos(db: Session, skip: int = 0, limit: int = 100) -> List[PlanMantenimiento]:
    """Obtener planes de mantenimiento activos"""
    return db.query(PlanMantenimiento).filter(PlanMantenimiento.activo == True).offset(skip).limit(limit).all()


def update_plan_mantenimiento(
    db: Session, 
    plan_id: UUID, 
    plan_data: PlanMantenimientoUpdate
) -> Optional[PlanMantenimiento]:
    """Actualizar un plan de mantenimiento"""
    db_plan = get_plan_mantenimiento(db, plan_id)
    if db_plan:
        update_data = plan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_plan, field, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan