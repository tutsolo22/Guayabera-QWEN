"""
Advanced Accounting CRUD Operations: Comprehensive accounting system with journal entries, financial statements, and reporting
Specialized for Mexican accounting compliance (SAT/NIF)
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.advanced_accounting import (
    PeriodoFiscal, PolizaContable, MovimientoContable,
    EstadoFinanciero, CentroCosto, PartidaPresupuestal
)
from app.schemas.advanced_accounting import (
    PeriodoFiscalCreate, PeriodoFiscalUpdate,
    PolizaContableCreate, PolizaContableUpdate,
    MovimientoContableCreate, MovimientoContableUpdate,
    EstadoFinancieroCreate, EstadoFinancieroUpdate,
    CentroCostoCreate, CentroCostoUpdate,
    PartidaPresupuestalCreate, PartidaPresupuestalUpdate
)


# ============================================================================
# FISCAL PERIOD CRUD
# ============================================================================

def create_periodo_fiscal(db: Session, periodo_data: PeriodoFiscalCreate) -> PeriodoFiscal:
    """Create a new fiscal period"""
    # Check if code already exists
    existing_periodo = db.query(PeriodoFiscal).filter(PeriodoFiscal.codigo == periodo_data.codigo).first()
    if existing_periodo:
        raise ValueError(f"A fiscal period with code {periodo_data.codigo} already exists")
    
    db_periodo = PeriodoFiscal(**periodo_data.model_dump())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo


def get_periodo_fiscal(db: Session, periodo_id: UUID) -> Optional[PeriodoFiscal]:
    """Get a fiscal period by ID"""
    return db.query(PeriodoFiscal).filter(PeriodoFiscal.id == periodo_id).first()


def get_periodo_fiscal_by_codigo(db: Session, codigo: str) -> Optional[PeriodoFiscal]:
    """Get a fiscal period by code"""
    return db.query(PeriodoFiscal).filter(PeriodoFiscal.codigo == codigo).first()


def get_periodos_fiscales(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    ano_fiscal: Optional[int] = None,
    estado: Optional[str] = None
) -> List[PeriodoFiscal]:
    """Get list of fiscal periods, optionally filtered"""
    query = db.query(PeriodoFiscal)
    
    if ano_fiscal:
        query = query.filter(PeriodoFiscal.ano_fiscal == ano_fiscal)
    if estado:
        query = query.filter(PeriodoFiscal.estado == estado)
    
    return query.order_by(PeriodoFiscal.fecha_inicio).offset(skip).limit(limit).all()


def update_periodo_fiscal(db: Session, periodo_id: UUID, periodo_data: PeriodoFiscalUpdate) -> Optional[PeriodoFiscal]:
    """Update a fiscal period"""
    db_periodo = get_periodo_fiscal(db, periodo_id)
    if db_periodo:
        update_data = periodo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_periodo, field, value)
        db.commit()
        db.refresh(db_periodo)
    return db_periodo


def delete_periodo_fiscal(db: Session, periodo_id: UUID) -> bool:
    """Delete a fiscal period"""
    db_periodo = get_periodo_fiscal(db, periodo_id)
    if db_periodo:
        db.delete(db_periodo)
        db.commit()
        return True
    return False


# ============================================================================
# ACCOUNTING VOUCHER CRUD
# ============================================================================

def create_poliza_contable(db: Session, poliza_data: PolizaContableCreate) -> PolizaContable:
    """Create a new accounting voucher"""
    # Generate unique folio if not provided
    if not poliza_data.folio:
        from datetime import datetime
        year = datetime.now().year
        count = db.query(PolizaContable).filter(
            func.extract('year', PolizaContable.fecha_emision) == year
        ).count() + 1
        poliza_data.folio = f"POL-{year}-{count:04d}"
    
    # Check if folio already exists
    existing_poliza = db.query(PolizaContable).filter(PolizaContable.folio == poliza_data.folio).first()
    if existing_poliza:
        raise ValueError(f"An accounting voucher with folio {poliza_data.folio} already exists")
    
    db_poliza = PolizaContable(**poliza_data.model_dump())
    db.add(db_poliza)
    db.commit()
    db.refresh(db_poliza)
    return db_poliza


def get_poliza_contable(db: Session, poliza_id: UUID) -> Optional[PolizaContable]:
    """Get an accounting voucher by ID"""
    return db.query(PolizaContable).filter(PolizaContable.id == poliza_id).first()


def get_poliza_contable_by_folio(db: Session, folio: str) -> Optional[PolizaContable]:
    """Get an accounting voucher by folio"""
    return db.query(PolizaContable).filter(PolizaContable.folio == folio).first()


def get_polizas_by_tipo(db: Session, tipo_poliza: str, skip: int = 0, limit: int = 100) -> List[PolizaContable]:
    """Get vouchers by type"""
    return db.query(PolizaContable).filter(
        PolizaContable.tipo_poliza == tipo_poliza
    ).offset(skip).limit(limit).all()


def get_polizas_by_periodo(db: Session, periodo_fiscal_id: UUID, skip: int = 0, limit: int = 100) -> List[PolizaContable]:
    """Get vouchers by fiscal period"""
    return db.query(PolizaContable).filter(
        PolizaContable.periodo_fiscal_id == periodo_fiscal_id
    ).offset(skip).limit(limit).all()


def update_poliza_contable(db: Session, poliza_id: UUID, poliza_data: PolizaContableUpdate) -> Optional[PolizaContable]:
    """Update an accounting voucher"""
    db_poliza = get_poliza_contable(db, poliza_id)
    if db_poliza:
        update_data = poliza_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_poliza, field, value)
        
        # Recalculate totals after updating
        calculate_voucher_totals(db, db_poliza.id)
        db.commit()
        db.refresh(db_poliza)
    return db_poliza


def calculate_voucher_totals(db: Session, poliza_id: UUID) -> Optional[PolizaContable]:
    """Calculate and update totals for an accounting voucher"""
    db_poliza = get_poliza_contable(db, poliza_id)
    if db_poliza:
        # Calculate totals from movements
        total_debe = db.query(func.sum(MovimientoContable.importe)).filter(
            and_(
                MovimientoContable.poliza_id == poliza_id,
                MovimientoContable.tipo_movimiento == 'debe'
            )
        ).scalar() or 0
        
        total_haber = db.query(func.sum(MovimientoContable.importe)).filter(
            and_(
                MovimientoContable.poliza_id == poliza_id,
                MovimientoContable.tipo_movimiento == 'haber'
            )
        ).scalar() or 0
        
        db_poliza.total_debe = total_debe
        db_poliza.total_haber = total_haber
        
        db.commit()
        db.refresh(db_poliza)
    
    return db_poliza


def delete_poliza_contable(db: Session, poliza_id: UUID) -> bool:
    """Delete an accounting voucher"""
    db_poliza = get_poliza_contable(db, poliza_id)
    if db_poliza:
        # Delete related movements first
        db.query(MovimientoContable).filter(MovimientoContable.poliza_id == poliza_id).delete()
        db.delete(db_poliza)
        db.commit()
        return True
    return False


# ============================================================================
# ACCOUNTING MOVEMENT CRUD
# ============================================================================

def create_movimiento_contable(db: Session, movimiento_data: MovimientoContableCreate) -> MovimientoContable:
    """Create a new accounting movement"""
    db_movimiento = MovimientoContable(**movimiento_data.model_dump())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    
    # Update voucher totals
    calculate_voucher_totals(db, movimiento_data.poliza_id)
    
    return db_movimiento


def get_movimiento_contable(db: Session, movimiento_id: UUID) -> Optional[MovimientoContable]:
    """Get an accounting movement by ID"""
    return db.query(MovimientoContable).filter(MovimientoContable.id == movimiento_id).first()


def get_movimientos_by_poliza(db: Session, poliza_id: UUID) -> List[MovimientoContable]:
    """Get all movements for a specific voucher"""
    return db.query(MovimientoContable).filter(
        MovimientoContable.poliza_id == poliza_id
    ).all()


def update_movimiento_contable(db: Session, movimiento_id: UUID, movimiento_data: MovimientoContableUpdate) -> Optional[MovimientoContable]:
    """Update an accounting movement"""
    db_movimiento = get_movimiento_contable(db, movimiento_id)
    if db_movimiento:
        update_data = movimiento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movimiento, field, value)
        
        # Update voucher totals
        calculate_voucher_totals(db, db_movimiento.poliza_id)
        
        db.commit()
        db.refresh(db_movimiento)
    return db_movimiento


def delete_movimiento_contable(db: Session, movimiento_id: UUID) -> bool:
    """Delete an accounting movement"""
    db_movimiento = get_movimiento_contable(db, movimiento_id)
    if db_movimiento:
        poliza_id = db_movimiento.poliza_id
        db.delete(db_movimiento)
        db.commit()
        
        # Update voucher totals
        calculate_voucher_totals(db, poliza_id)
        
        return True
    return False


# ============================================================================
# FINANCIAL STATEMENT CRUD
# ============================================================================

def create_estado_financiero(db: Session, estado_data: EstadoFinancieroCreate) -> EstadoFinanciero:
    """Create a new financial statement"""
    db_estado = EstadoFinanciero(**estado_data.model_dump())
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado


def get_estado_financiero(db: Session, estado_id: UUID) -> Optional[EstadoFinanciero]:
    """Get a financial statement by ID"""
    return db.query(EstadoFinanciero).filter(EstadoFinanciero.id == estado_id).first()


def get_estados_financieros_by_tipo(db: Session, tipo_estado: str, skip: int = 0, limit: int = 100) -> List[EstadoFinanciero]:
    """Get financial statements by type"""
    return db.query(EstadoFinanciero).filter(
        EstadoFinanciero.tipo_estado == tipo_estado
    ).offset(skip).limit(limit).all()


def update_estado_financiero(db: Session, estado_id: UUID, estado_data: EstadoFinancieroUpdate) -> Optional[EstadoFinanciero]:
    """Update a financial statement"""
    db_estado = get_estado_financiero(db, estado_id)
    if db_estado:
        update_data = estado_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_estado, field, value)
        db.commit()
        db.refresh(db_estado)
    return db_estado


def delete_estado_financiero(db: Session, estado_id: UUID) -> bool:
    """Delete a financial statement"""
    db_estado = get_estado_financiero(db, estado_id)
    if db_estado:
        db.delete(db_estado)
        db.commit()
        return True
    return False


# ============================================================================
# COST CENTER CRUD
# ============================================================================

def create_centro_costo(db: Session, centro_data: CentroCostoCreate) -> CentroCosto:
    """Create a new cost center"""
    # Check if code already exists
    existing_centro = db.query(CentroCosto).filter(CentroCosto.codigo == centro_data.codigo).first()
    if existing_centro:
        raise ValueError(f"A cost center with code {centro_data.codigo} already exists")
    
    db_centro = CentroCosto(**centro_data.model_dump())
    db.add(db_centro)
    db.commit()
    db.refresh(db_centro)
    return db_centro


def get_centro_costo(db: Session, centro_id: UUID) -> Optional[CentroCosto]:
    """Get a cost center by ID"""
    return db.query(CentroCosto).filter(CentroCosto.id == centro_id).first()


def get_centro_costo_by_codigo(db: Session, codigo: str) -> Optional[CentroCosto]:
    """Get a cost center by code"""
    return db.query(CentroCosto).filter(CentroCosto.codigo == codigo).first()


def get_centros_costo(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[CentroCosto]:
    """Get list of cost centers, optionally filtered"""
    query = db.query(CentroCosto)
    
    if activo is not None:
        query = query.filter(CentroCosto.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_centro_costo(db: Session, centro_id: UUID, centro_data: CentroCostoUpdate) -> Optional[CentroCosto]:
    """Update a cost center"""
    db_centro = get_centro_costo(db, centro_id)
    if db_centro:
        update_data = centro_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_centro, field, value)
        db.commit()
        db.refresh(db_centro)
    return db_centro


def delete_centro_costo(db: Session, centro_id: UUID) -> bool:
    """Delete a cost center"""
    db_centro = get_centro_costo(db, centro_id)
    if db_centro:
        db.delete(db_centro)
        db.commit()
        return True
    return False


# ============================================================================
# BUDGETARY ENTRY CRUD
# ============================================================================

def create_partida_presupuestal(db: Session, partida_data: PartidaPresupuestalCreate) -> PartidaPresupuestal:
    """Create a new budgetary entry"""
    # Check if code already exists
    existing_partida = db.query(PartidaPresupuestal).filter(PartidaPresupuestal.codigo == partida_data.codigo).first()
    if existing_partida:
        raise ValueError(f"A budgetary entry with code {partida_data.codigo} already exists")
    
    db_partida = PartidaPresupuestal(**partida_data.model_dump())
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida


def get_partida_presupuestal(db: Session, partida_id: UUID) -> Optional[PartidaPresupuestal]:
    """Get a budgetary entry by ID"""
    return db.query(PartidaPresupuestal).filter(PartidaPresupuestal.id == partida_id).first()


def get_partida_presupuestal_by_codigo(db: Session, codigo: str) -> Optional[PartidaPresupuestal]:
    """Get a budgetary entry by code"""
    return db.query(PartidaPresupuestal).filter(PartidaPresupuestal.codigo == codigo).first()


def get_partidas_presupuestales(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    centro_costo_id: Optional[UUID] = None,
    periodo_fiscal_id: Optional[UUID] = None
) -> List[PartidaPresupuestal]:
    """Get list of budgetary entries, optionally filtered"""
    query = db.query(PartidaPresupuestal)
    
    if centro_costo_id:
        query = query.filter(PartidaPresupuestal.centro_costo_id == centro_costo_id)
    if periodo_fiscal_id:
        query = query.filter(PartidaPresupuestal.periodo_fiscal_id == periodo_fiscal_id)
    
    return query.offset(skip).limit(limit).all()


def update_partida_presupuestal(db: Session, partida_id: UUID, partida_data: PartidaPresupuestalUpdate) -> Optional[PartidaPresupuestal]:
    """Update a budgetary entry"""
    db_partida = get_partida_presupuestal(db, partida_id)
    if db_partida:
        update_data = partida_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_partida, field, value)
        db.commit()
        db.refresh(db_partida)
    return db_partida


def delete_partida_presupuestal(db: Session, partida_id: UUID) -> bool:
    """Delete a budgetary entry"""
    db_partida = get_partida_presupuestal(db, partida_id)
    if db_partida:
        db.delete(db_partida)
        db.commit()
        return True
    return False