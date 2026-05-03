"""
Asset Management CRUD Operations: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID
from decimal import Decimal

from app.models.asset_management import (
    CategoriaActivo, Activo, MantenimientoActivo,
    DepreciacionActivo, HistorialAsignacion, ProveedorActivo, ContratoMantenimiento
)
from app.schemas.asset_management import (
    CategoriaActivoCreate, CategoriaActivoUpdate,
    ActivoCreate, ActivoUpdate,
    MantenimientoActivoCreate, MantenimientoActivoUpdate,
    DepreciacionActivoCreate, DepreciacionActivoUpdate,
    HistorialAsignacionCreate, HistorialAsignacionUpdate,
    ProveedorActivoCreate, ProveedorActivoUpdate,
    ContratoMantenimientoCreate, ContratoMantenimientoUpdate,
    MantenimientoRequest, MantenimientoResponse, DepreciacionResponse
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
# ASSET MAINTENANCE HISTORY CRUD (HistorialMantenimientoActivo)
# ============================================================================

def create_historial_mantenimiento(db: Session, mantenimiento_data: MantenimientoActivoCreate) -> MantenimientoActivo:
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


def get_historial_mantenimiento(db: Session, mantenimiento_id: UUID) -> Optional[MantenimientoActivo]:
    """Get an asset maintenance record by ID"""
    return db.query(MantenimientoActivo).filter(
        MantenimientoActivo.id == mantenimiento_id
    ).first()


def get_historiales_by_activo(
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


def update_historial_mantenimiento(
    db: Session, 
    mantenimiento_id: UUID, 
    mantenimiento_data: MantenimientoActivoUpdate
) -> Optional[MantenimientoActivo]:
    """Update an asset maintenance record"""
    db_mantenimiento = get_historial_mantenimiento(db, mantenimiento_id)
    if db_mantenimiento:
        update_data = mantenimiento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_mantenimiento, field, value)
        db.commit()
        db.refresh(db_mantenimiento)
    return db_mantenimiento


# ============================================================================
# ASSET ASSIGNMENT CRUD (AsignacionActivo)
# ============================================================================

def create_asignacion_activo(db: Session, asignacion_data: HistorialAsignacionCreate) -> HistorialAsignacion:
    """Create a new asset assignment record"""
    db_asignacion = HistorialAsignacion(**asignacion_data.model_dump())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    
    # Update the asset with new assignment details
    activo = get_activo(db, asignacion_data.activo_id)
    if activo:
        if asignacion_data.empleado_nuevo_id:
            activo.empleado_asignado_id = asignacion_data.empleado_nuevo_id
        if asignacion_data.departamento_nuevo_id:
            activo.departamento_asignado_id = asignacion_data.departamento_nuevo_id
        if asignacion_data.ubicacion_nueva:
            activo.ubicacion_actual = asignacion_data.ubicacion_nueva
        db.commit()
    
    return db_asignacion


def get_asignacion_activo(db: Session, asignacion_id: UUID) -> Optional[HistorialAsignacion]:
    """Get an asset assignment record by ID"""
    return db.query(HistorialAsignacion).filter(
        HistorialAsignacion.id == asignacion_id
    ).first()


def get_asignaciones_by_activo(
    db: Session, 
    activo_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[HistorialAsignacion]:
    """Get all assignment records for a specific asset"""
    return db.query(HistorialAsignacion).filter(
        HistorialAsignacion.activo_id == activo_id
    ).order_by(HistorialAsignacion.fecha_inicio.desc()).offset(skip).limit(limit).all()


def get_asignaciones_by_usuario(
    db: Session, 
    usuario_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[HistorialAsignacion]:
    """Get all assignments for a specific user (either old or new employee)"""
    return db.query(HistorialAsignacion).filter(
        or_(
            HistorialAsignacion.empleado_anterior_id == usuario_id,
            HistorialAsignacion.empleado_nuevo_id == usuario_id
        )
    ).order_by(HistorialAsignacion.fecha_inicio.desc()).offset(skip).limit(limit).all()


def update_asignacion_activo(
    db: Session, 
    asignacion_id: UUID, 
    asignacion_data: HistorialAsignacionUpdate
) -> Optional[HistorialAsignacion]:
    """Update an asset assignment record"""
    db_asignacion = get_asignacion_activo(db, asignacion_id)
    if db_asignacion:
        update_data = asignacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asignacion, field, value)
        db.commit()
        db.refresh(db_asignacion)
    return db_asignacion


def delete_asignacion_activo(db: Session, asignacion_id: UUID) -> bool:
    """Delete an asset assignment record"""
    db_asignacion = get_asignacion_activo(db, asignacion_id)
    if db_asignacion:
        db.delete(db_asignacion)
        db.commit()
        return True
    return False


# ============================================================================
# ASSET PROVIDER CRUD (ProveedorActivo)
# ============================================================================

def create_proveedor(db: Session, proveedor_data: ProveedorActivoCreate) -> ProveedorActivo:
    """Create a new asset provider"""
    db_proveedor = ProveedorActivo(**proveedor_data.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor


def get_proveedor(db: Session, proveedor_id: UUID) -> Optional[ProveedorActivo]:
    """Get an asset provider by ID"""
    return db.query(ProveedorActivo).filter(ProveedorActivo.id == proveedor_id).first()


def get_proveedores(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[ProveedorActivo]:
    """Get list of asset providers, optionally filtered"""
    query = db.query(ProveedorActivo)
    
    if activo is not None:
        query = query.filter(ProveedorActivo.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_proveedor(
    db: Session, 
    proveedor_id: UUID, 
    proveedor_data: ProveedorActivoUpdate
) -> Optional[ProveedorActivo]:
    """Update an asset provider"""
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        update_data = proveedor_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_proveedor, field, value)
        db.commit()
        db.refresh(db_proveedor)
    return db_proveedor


def delete_proveedor(db: Session, proveedor_id: UUID) -> bool:
    """Delete an asset provider"""
    db_proveedor = get_proveedor(db, proveedor_id)
    if db_proveedor:
        db.delete(db_proveedor)
        db.commit()
        return True
    return False


# ============================================================================
# MAINTENANCE CONTRACT CRUD (ContratoMantenimiento)
# ============================================================================

def create_contrato_mantenimiento(db: Session, contrato_data: ContratoMantenimientoCreate) -> ContratoMantenimiento:
    """Create a new maintenance contract"""
    db_contrato = ContratoMantenimiento(**contrato_data.model_dump())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato


def get_contrato_mantenimiento(db: Session, contrato_id: UUID) -> Optional[ContratoMantenimiento]:
    """Get a maintenance contract by ID"""
    return db.query(ContratoMantenimiento).filter(ContratoMantenimiento.id == contrato_id).first()


def get_contratos_by_activo(db: Session, activo_id: UUID) -> List[ContratoMantenimiento]:
    """Get all contracts for a specific asset"""
    # Since there isn't a direct relationship, we'll return empty for now
    # This would need to be implemented with the many-to-many relationship if needed
    return []


def get_contratos_by_proveedor(db: Session, proveedor_id: UUID) -> List[ContratoMantenimiento]:
    """Get all contracts for a specific provider"""
    return db.query(ContratoMantenimiento).filter(
        ContratoMantenimiento.proveedor_id == proveedor_id
    ).all()


def update_contrato_mantenimiento(
    db: Session, 
    contrato_id: UUID, 
    contrato_data: ContratoMantenimientoUpdate
) -> Optional[ContratoMantenimiento]:
    """Update a maintenance contract"""
    db_contrato = get_contrato_mantenimiento(db, contrato_id)
    if db_contrato:
        update_data = contrato_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contrato, field, value)
        db.commit()
        db.refresh(db_contrato)
    return db_contrato


def delete_contrato_mantenimiento(db: Session, contrato_id: UUID) -> bool:
    """Delete a maintenance contract"""
    db_contrato = get_contrato_mantenimiento(db, contrato_id)
    if db_contrato:
        db.delete(db_contrato)
        db.commit()
        return True
    return False


def registrar_mantenimiento(db: Session, mantenimiento_request) -> MantenimientoResponse:
    """Register a new maintenance for an asset"""
    # Create a new maintenance record
    mantenimiento_data = MantenimientoActivoCreate(
        activo_id=mantenimiento_request.activo_id,
        tipo_mantenimiento=mantenimiento_request.tipo_mantenimiento,
        titulo=f"Mantenimiento de {mantenimiento_request.tipo_mantenimiento}",
        descripcion=mantenimiento_request.descripcion,
        fecha_programada=mantenimiento_request.fecha_programada,
        costo=mantenimiento_request.costo_estimado,
        estado="programado",
        prioridad=mantenimiento_request.prioridad
    )
    
    nuevo_mantenimiento = create_historial_mantenimiento(db, mantenimiento_data)
    
    # Convert to response format
    return MantenimientoResponse(
        id=nuevo_mantenimiento.id,
        activo_id=nuevo_mantenimiento.activo_id,
        tipo_mantenimiento=nuevo_mantenimiento.tipo_mantenimiento,
        estado=nuevo_mantenimiento.estado,
        fecha_programada=nuevo_mantenimiento.fecha_programada,
        created_at=nuevo_mantenimiento.created_at
    )


def calcular_depreciacion_activos(db: Session, activo_id: UUID) -> DepreciacionResponse:
    """Calculate depreciation for an asset"""
    # Get the asset
    activo = get_activo(db, activo_id)
    if not activo:
        raise ValueError(f"Asset with ID {activo_id} not found")
    
    # Calculate depreciation values
    vida_util_anios = activo.vida_util_anios or 0
    anios_transcurridos = 0
    if activo.fecha_adquisicion:
        anios_transcurridos = (func.now() - activo.fecha_adquisicion).days / 365.25
    
    depreciacion_acumulada = Decimal('0')
    valor_actual = activo.valor_adquisicion or Decimal('0')
    tasa_depreciacion = Decimal('0')
    
    if vida_util_anios > 0:
        tasa_depreciacion = Decimal('100.0') / Decimal(str(vida_util_anios))
        
        # Simple straight-line depreciation calculation
        depreciacion_anual = valor_actual / Decimal(str(vida_util_anios))
        depreciacion_acumulada = min(valor_actual, depreciacion_anual * Decimal(str(min(anios_transcurridos, vida_util_anios))))
        valor_actual = valor_actual - depreciacion_acumulada
    
    # Create the response
    return DepreciacionResponse(
        activo_id=activo.id,
        activo_nombre=activo.nombre,
        metodo_depreciacion=activo.metodo_depreciacion or "linea_recta",
        valor_adquisicion=activo.valor_adquisicion or Decimal('0'),
        valor_actual=valor_actual,
        depreciacion_acumulada=depreciacion_acumulada,
        vida_util_anios=vida_util_anios,
        anios_transcurridos=int(anios_transcurridos),
        tasa_depreciacion=float(tasa_depreciacion)
    )

