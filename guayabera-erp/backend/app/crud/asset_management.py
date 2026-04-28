"""
Asset Management CRUD Operations: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.asset_management import (
    CategoriaActivo, Activo, MantenimientoActivo,
    DepreciacionActivo, HistorialAsignacion
)
from app.schemas.asset_management import (
    CategoriaActivoCreate, CategoriaActivoUpdate,
    ActivoCreate, ActivoUpdate,
    MantenimientoActivoCreate, MantenimientoActivoUpdate,
    DepreciacionActivoCreate, DepreciacionActivoUpdate,
    HistorialAsignacionCreate, HistorialAsignacionUpdate
)


# ============================================================================
# ASSET CATEGORY CRUD
# ============================================================================

def create_categoria_activo(db: Session, categoria_data: CategoriaActivoCreate) -> CategoriaActivo:
    """Create a new asset category"""
    # Check if category code already exists
    existing_categoria = db.query(CategoriaActivo).filter(
        CategoriaActivo.codigo == categoria_data.codigo
    ).first()
    if existing_categoria:
        raise ValueError(f"An asset category with code {categoria_data.codigo} already exists")
    
    db_categoria = CategoriaActivo(**categoria_data.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def get_categoria_activo(db: Session, categoria_id: UUID) -> Optional[CategoriaActivo]:
    """Get an asset category by ID"""
    return db.query(CategoriaActivo).filter(CategoriaActivo.id == categoria_id).first()


def get_categoria_activo_by_codigo(db: Session, codigo: str) -> Optional[CategoriaActivo]:
    """Get an asset category by code"""
    return db.query(CategoriaActivo).filter(CategoriaActivo.codigo == codigo).first()


def get_categorias_activos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    activo: Optional[bool] = None
) -> List[CategoriaActivo]:
    """Get list of asset categories, optionally filtered"""
    query = db.query(CategoriaActivo)
    
    if activo is not None:
        query = query.filter(CategoriaActivo.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_categoria_activo(
    db: Session, 
    categoria_id: UUID, 
    categoria_data: CategoriaActivoUpdate
) -> Optional[CategoriaActivo]:
    """Update an asset category"""
    db_categoria = get_categoria_activo(db, categoria_id)
    if db_categoria:
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_categoria, field, value)
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def delete_categoria_activo(db: Session, categoria_id: UUID) -> bool:
    """Soft delete an asset category"""
    db_categoria = get_categoria_activo(db, categoria_id)
    if db_categoria:
        db_categoria.activo = False
        db_categoria.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# ASSET CRUD
# ============================================================================

def create_activo(db: Session, activo_data: ActivoCreate) -> Activo:
    """Create a new fixed asset"""
    # Check if asset code already exists
    existing_activo = db.query(Activo).filter(Activo.codigo == activo_data.codigo).first()
    if existing_activo:
        raise ValueError(f"An asset with code {activo_data.codigo} already exists")
    
    db_activo = Activo(**activo_data.model_dump())
    db.add(db_activo)
    db.commit()
    db.refresh(db_activo)
    return db_activo


def get_activo(db: Session, activo_id: UUID) -> Optional[Activo]:
    """Get a fixed asset by ID"""
    return db.query(Activo).filter(Activo.id == activo_id).first()


def get_activo_by_codigo(db: Session, codigo: str) -> Optional[Activo]:
    """Get a fixed asset by code"""
    return db.query(Activo).filter(Activo.codigo == codigo).first()


def get_activos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    tipo: Optional[str] = None,
    categoria_id: Optional[UUID] = None,
    departamento_id: Optional[UUID] = None
) -> List[Activo]:
    """Get list of assets, optionally filtered"""
    query = db.query(Activo)
    
    if estado:
        query = query.filter(Activo.estado == estado)
    if tipo:
        query = query.filter(Activo.tipo == tipo)
    if categoria_id:
        query = query.filter(Activo.categoria_id == categoria_id)
    if departamento_id:
        query = query.filter(Activo.departamento_asignado_id == departamento_id)
    
    return query.offset(skip).limit(limit).all()


def update_activo(db: Session, activo_id: UUID, activo_data: ActivoUpdate) -> Optional[Activo]:
    """Update a fixed asset"""
    db_activo = get_activo(db, activo_id)
    if db_activo:
        update_data = activo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_activo, field, value)
        
        # Update current value based on depreciation
        if db_activo.metodo_depreciacion and db_activo.valor_adquisicion:
            # Calculate current book value based on depreciation
            depreciaciones = db.query(DepreciacionActivo).filter(
                and_(
                    DepreciacionActivo.activo_id == activo_id,
                    DepreciacionActivo.anio <= func.date_part('year', func.now()),
                    DepreciacionActivo.mes <= func.date_part('month', func.now())
                )
            ).all()
            
            if depreciaciones:
                total_depreciacion = sum([dep.depreciacion_acumulada for dep in depreciaciones])
                db_activo.valor_actual = db_activo.valor_adquisicion - total_depreciacion
        
        db.commit()
        db.refresh(db_activo)
    return db_activo


def delete_activo(db: Session, activo_id: UUID) -> bool:
    """Soft delete a fixed asset"""
    db_activo = get_activo(db, activo_id)
    if db_activo:
        db_activo.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# ASSET MAINTENANCE CRUD
# ============================================================================

def create_mantenimiento_activo(db: Session, mantenimiento_data: MantenimientoActivoCreate) -> MantenimientoActivo:
    """Create a new asset maintenance record"""
    db_mantenimiento = MantenimientoActivo(**mantenimiento_data.model_dump())
    db.add(db_mantenimiento)
    db.commit()
    db.refresh(db_mantenimiento)
    
    # Update the asset with the next maintenance date
    activo = get_activo(db, mantenimiento_data.activo_id)
    if activo and mantenimiento_data.proximo_mantenimiento:
        activo.proximo_mantenimiento = mantenimiento_data.proximo_mantenimiento
        activo.fecha_ultimo_mantenimiento = mantenimiento_data.fecha_realizacion or mantenimiento_data.fecha_programada
        db.commit()
    
    return db_mantenimiento


def get_mantenimiento_activo(db: Session, mantenimiento_id: UUID) -> Optional[MantenimientoActivo]:
    """Get an asset maintenance record by ID"""
    return db.query(MantenimientoActivo).filter(
        MantenimientoActivo.id == mantenimiento_id
    ).first()


def get_mantenimientos_by_activo(
    db: Session, 
    activo_id: UUID, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None
) -> List[MantenimientoActivo]:
    """Get all maintenance records for a specific asset"""
    query = db.query(MantenimientoActivo).filter(
        MantenimientoActivo.activo_id == activo_id
    ).order_by(MantenimientoActivo.fecha_programada.desc())
    
    if estado:
        query = query.filter(MantenimientoActivo.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def get_mantenimientos_programados(
    db: Session, 
    fecha_inicio: date, 
    fecha_fin: date,
    skip: int = 0, 
    limit: int = 100
) -> List[MantenimientoActivo]:
    """Get all scheduled maintenance records within a date range"""
    return db.query(MantenimientoActivo).filter(
        and_(
            MantenimientoActivo.fecha_programada >= fecha_inicio,
            MantenimientoActivo.fecha_programada <= fecha_fin
        )
    ).offset(skip).limit(limit).all()


def update_mantenimiento_activo(
    db: Session, 
    mantenimiento_id: UUID, 
    mantenimiento_data: MantenimientoActivoUpdate
) -> Optional[MantenimientoActivo]:
    """Update an asset maintenance record"""
    db_mantenimiento = get_mantenimiento_activo(db, mantenimiento_id)
    if db_mantenimiento:
        update_data = mantenimiento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_mantenimiento, field, value)
        db.commit()
        db.refresh(db_mantenimiento)
    return db_mantenimiento


def delete_mantenimiento_activo(db: Session, mantenimiento_id: UUID) -> bool:
    """Delete an asset maintenance record"""
    db_mantenimiento = get_mantenimiento_activo(db, mantenimiento_id)
    if db_mantenimiento:
        db.delete(db_mantenimiento)
        db.commit()
        return True
    return False


# ============================================================================
# ASSET DEPRECIATION CRUD
# ============================================================================

def create_depreciacion_activo(db: Session, depreciacion_data: DepreciacionActivoCreate) -> DepreciacionActivo:
    """Create a new asset depreciation record"""
    db_depreciacion = DepreciacionActivo(**depreciacion_data.model_dump())
    db.add(db_depreciacion)
    db.commit()
    db.refresh(db_depreciacion)
    
    # Update the asset with the new book value
    activo = get_activo(db, depreciacion_data.activo_id)
    if activo:
        activo.valor_actual = depreciacion_data.valor_libros
        db.commit()
    
    return db_depreciacion


def get_depreciacion_activo(db: Session, depreciacion_id: UUID) -> Optional[DepreciacionActivo]:
    """Get an asset depreciation record by ID"""
    return db.query(DepreciacionActivo).filter(
        DepreciacionActivo.id == depreciacion_id
    ).first()


def get_depreciaciones_by_activo(
    db: Session, 
    activo_id: UUID, 
    anio: Optional[int] = None
) -> List[DepreciacionActivo]:
    """Get all depreciation records for a specific asset"""
    query = db.query(DepreciacionActivo).filter(
        DepreciacionActivo.activo_id == activo_id
    ).order_by(DepreciacionActivo.anio, DepreciacionActivo.mes)
    
    if anio:
        query = query.filter(DepreciacionActivo.anio == anio)
    
    return query.all()


def get_depreciaciones_by_fecha(
    db: Session, 
    anio: int, 
    mes: Optional[int] = None
) -> List[DepreciacionActivo]:
    """Get all depreciation records for a specific month/year"""
    query = db.query(DepreciacionActivo).filter(DepreciacionActivo.anio == anio)
    if mes:
        query = query.filter(DepreciacionActivo.mes == mes)
    
    return query.all()


def update_depreciacion_activo(
    db: Session, 
    depreciacion_id: UUID, 
    depreciacion_data: DepreciacionActivoUpdate
) -> Optional[DepreciacionActivo]:
    """Update an asset depreciation record"""
    db_depreciacion = get_depreciacion_activo(db, depreciacion_id)
    if db_depreciacion:
        update_data = depreciacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_depreciacion, field, value)
        
        # Update the asset with the new book value
        activo = get_activo(db, db_depreciacion.activo_id)
        if activo:
            activo.valor_actual = db_depreciacion.valor_libros
            db.commit()
        
        db.commit()
        db.refresh(db_depreciacion)
    return db_depreciacion


def delete_depreciacion_activo(db: Session, depreciacion_id: UUID) -> bool:
    """Delete an asset depreciation record"""
    db_depreciacion = get_depreciacion_activo(db, depreciacion_id)
    if db_depreciacion:
        db.delete(db_depreciacion)
        # Update asset value to remove this depreciation
        activo = get_activo(db, db_depreciacion.activo_id)
        if activo:
            # Need to recalculate the asset value without this depreciation
            other_deps = get_depreciaciones_by_activo(db, db_depreciacion.activo_id)
            remaining_depreciation = sum([
                d.depreciacion_acumulada for d in other_deps 
                if d.id != depreciacion_id
            ])
            activo.valor_actual = activo.valor_adquisicion - remaining_depreciation
            db.commit()
        return True
    return False


# ============================================================================
# ASSIGNMENT HISTORY CRUD
# ============================================================================

def create_historial_asignacion(
    db: Session, 
    historial_data: HistorialAsignacionCreate
) -> HistorialAsignacion:
    """Create a new asset assignment history record"""
    db_historial = HistorialAsignacion(**historial_data.model_dump())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    
    # Update the asset with new assignment details
    activo = get_activo(db, historial_data.activo_id)
    if activo:
        if historial_data.empleado_nuevo_id:
            activo.empleado_asignado_id = historial_data.empleado_nuevo_id
        if historial_data.departamento_nuevo_id:
            activo.departamento_asignado_id = historial_data.departamento_nuevo_id
        if historial_data.ubicacion_nueva:
            activo.ubicacion_actual = historial_data.ubicacion_nueva
        db.commit()
    
    return db_historial


def get_historial_asignacion(db: Session, historial_id: UUID) -> Optional[HistorialAsignacion]:
    """Get an asset assignment history record by ID"""
    return db.query(HistorialAsignacion).filter(
        HistorialAsignacion.id == historial_id
    ).first()


def get_historial_by_activo(
    db: Session, 
    activo_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[HistorialAsignacion]:
    """Get all assignment history records for a specific asset"""
    return db.query(HistorialAsignacion).filter(
        HistorialAsignacion.activo_id == activo_id
    ).order_by(HistorialAsignacion.fecha_inicio.desc()).offset(skip).limit(limit).all()


def get_activos_by_empleado(db: Session, empleado_id: UUID) -> List[Activo]:
    """Get all assets currently assigned to a specific employee"""
    return db.query(Activo).filter(
        Activo.empleado_asignado_id == empleado_id
    ).all()


def update_historial_asignacion(
    db: Session, 
    historial_id: UUID, 
    historial_data: HistorialAsignacionUpdate
) -> Optional[HistorialAsignacion]:
    """Update an asset assignment history record"""
    db_historial = get_historial_asignacion(db, historial_id)
    if db_historial:
        update_data = historial_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_historial, field, value)
        db.commit()
        db.refresh(db_historial)
    return db_historial


def delete_historial_asignacion(db: Session, historial_id: UUID) -> bool:
    """Delete an asset assignment history record"""
    db_historial = get_historial_asignacion(db, historial_id)
    if db_historial:
        db.delete(db_historial)
        db.commit()
        return True
    return False