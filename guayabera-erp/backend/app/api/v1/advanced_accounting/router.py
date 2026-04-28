"""
Advanced Accounting API Router: Comprehensive accounting system with journal entries, financial statements, and reporting
Specialized for Mexican accounting compliance (SAT/NIF)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.advanced_accounting import (
    PeriodoFiscalCreate, PeriodoFiscalUpdate, PeriodoFiscalResponse,
    PolizaContableCreate, PolizaContableUpdate, PolizaContableResponse,
    MovimientoContableCreate, MovimientoContableUpdate, MovimientoContableResponse,
    EstadoFinancieroCreate, EstadoFinancieroUpdate, EstadoFinancieroResponse,
    CentroCostoCreate, CentroCostoUpdate, CentroCostoResponse,
    PartidaPresupuestalCreate, PartidaPresupuestalUpdate, PartidaPresupuestalResponse
)
from app.crud.advanced_accounting import (
    create_periodo_fiscal, get_periodo_fiscal, get_periodo_fiscal_by_codigo,
    get_periodos_fiscales, update_periodo_fiscal, delete_periodo_fiscal,
    create_poliza_contable, get_poliza_contable, get_poliza_contable_by_folio,
    get_polizas_by_tipo, get_polizas_by_periodo, update_poliza_contable,
    delete_poliza_contable, calculate_voucher_totals,
    create_movimiento_contable, get_movimiento_contable, get_movimientos_by_poliza,
    update_movimiento_contable, delete_movimiento_contable,
    create_estado_financiero, get_estado_financiero, get_estados_financieros_by_tipo,
    update_estado_financiero, delete_estado_financiero,
    create_centro_costo, get_centro_costo, get_centro_costo_by_codigo,
    get_centros_costo, update_centro_costo, delete_centro_costo,
    create_partida_presupuestal, get_partida_presupuestal, get_partida_presupuestal_by_codigo,
    get_partidas_presupuestales, update_partida_presupuestal, delete_partida_presupuestal
)

router = APIRouter(prefix="/advanced-accounting", tags=["Advanced Accounting"])

# ============================================================================
# FISCAL PERIOD ENDPOINTS
# ============================================================================

@router.post("/fiscal-periods/", response_model=PeriodoFiscalResponse)
def create_fiscal_period(periodo: PeriodoFiscalCreate, db: Session = Depends(get_db)):
    """Create a new fiscal period"""
    try:
        return create_periodo_fiscal(db=db, periodo_data=periodo)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/fiscal-periods/{periodo_id}", response_model=PeriodoFiscalResponse)
def get_fiscal_period(periodo_id: str, db: Session = Depends(get_db)):
    """Get a fiscal period by ID"""
    periodo = get_periodo_fiscal(db, periodo_id)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal period not found"
        )
    return periodo


@router.get("/fiscal-periods/code/{codigo}", response_model=PeriodoFiscalResponse)
def get_fiscal_period_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a fiscal period by code"""
    periodo = get_periodo_fiscal_by_codigo(db, codigo)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal period not found"
        )
    return periodo


@router.get("/fiscal-periods/", response_model=List[PeriodoFiscalResponse])
def get_fiscal_periods(
    skip: int = 0, 
    limit: int = 100,
    ano_fiscal: Optional[int] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of fiscal periods, optionally filtered"""
    return get_periodos_fiscales(db, skip, limit, ano_fiscal, estado)


@router.put("/fiscal-periods/{periodo_id}", response_model=PeriodoFiscalResponse)
def update_fiscal_period(
    periodo_id: str, 
    periodo_data: PeriodoFiscalUpdate, 
    db: Session = Depends(get_db)
):
    """Update a fiscal period"""
    updated_periodo = update_periodo_fiscal(
        db=db, 
        periodo_id=periodo_id, 
        periodo_data=periodo_data
    )
    if not updated_periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal period not found"
        )
    return updated_periodo


@router.delete("/fiscal-periods/{periodo_id}")
def delete_fiscal_period(periodo_id: str, db: Session = Depends(get_db)):
    """Delete a fiscal period"""
    success = delete_periodo_fiscal(db=db, periodo_id=periodo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal period not found"
        )
    return {"message": "Fiscal period deleted successfully"}


# ============================================================================
# ACCOUNTING VOUCHER ENDPOINTS
# ============================================================================

@router.post("/vouchers/", response_model=PolizaContableResponse)
def create_accounting_voucher(poliza: PolizaContableCreate, db: Session = Depends(get_db)):
    """Create a new accounting voucher"""
    try:
        return create_poliza_contable(db=db, poliza_data=poliza)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/vouchers/{poliza_id}", response_model=PolizaContableResponse)
def get_accounting_voucher(poliza_id: str, db: Session = Depends(get_db)):
    """Get an accounting voucher by ID"""
    poliza = get_poliza_contable(db, poliza_id)
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting voucher not found"
        )
    return poliza


@router.get("/vouchers/folio/{folio}", response_model=PolizaContableResponse)
def get_voucher_by_folio(folio: str, db: Session = Depends(get_db)):
    """Get an accounting voucher by folio"""
    poliza = get_poliza_contable_by_folio(db, folio)
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting voucher not found"
        )
    return poliza


@router.get("/vouchers/type/{tipo_poliza}", response_model=List[PolizaContableResponse])
def get_vouchers_by_type(
    tipo_poliza: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get vouchers by type"""
    return get_polizas_by_tipo(db, tipo_poliza, skip, limit)


@router.get("/vouchers/period/{periodo_fiscal_id}", response_model=List[PolizaContableResponse])
def get_vouchers_by_period(
    periodo_fiscal_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get vouchers by fiscal period"""
    return get_polizas_by_periodo(db, periodo_fiscal_id, skip, limit)


@router.put("/vouchers/{poliza_id}", response_model=PolizaContableResponse)
def update_accounting_voucher(
    poliza_id: str, 
    poliza_data: PolizaContableUpdate, 
    db: Session = Depends(get_db)
):
    """Update an accounting voucher"""
    updated_poliza = update_poliza_contable(
        db=db, 
        poliza_id=poliza_id, 
        poliza_data=poliza_data
    )
    if not updated_poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting voucher not found"
        )
    return updated_poliza


@router.delete("/vouchers/{poliza_id}")
def delete_accounting_voucher(poliza_id: str, db: Session = Depends(get_db)):
    """Delete an accounting voucher"""
    success = delete_poliza_contable(db=db, poliza_id=poliza_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting voucher not found"
        )
    return {"message": "Accounting voucher deleted successfully"}


# ============================================================================
# ACCOUNTING MOVEMENT ENDPOINTS
# ============================================================================

@router.post("/movements/", response_model=MovimientoContableResponse)
def create_accounting_movement(movimiento: MovimientoContableCreate, db: Session = Depends(get_db)):
    """Create a new accounting movement"""
    return create_movimiento_contable(db=db, movimiento_data=movimiento)


@router.get("/movements/{movimiento_id}", response_model=MovimientoContableResponse)
def get_accounting_movement(movimiento_id: str, db: Session = Depends(get_db)):
    """Get an accounting movement by ID"""
    movimiento = get_movimiento_contable(db, movimiento_id)
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting movement not found"
        )
    return movimiento


@router.get("/movements/voucher/{poliza_id}", response_model=List[MovimientoContableResponse])
def get_movements_by_voucher(poliza_id: str, db: Session = Depends(get_db)):
    """Get all movements for a specific voucher"""
    return get_movimientos_by_poliza(db, poliza_id)


@router.put("/movements/{movimiento_id}", response_model=MovimientoContableResponse)
def update_accounting_movement(
    movimiento_id: str, 
    movimiento_data: MovimientoContableUpdate, 
    db: Session = Depends(get_db)
):
    """Update an accounting movement"""
    updated_movimiento = update_movimiento_contable(
        db=db, 
        movimiento_id=movimiento_id, 
        movimiento_data=movimiento_data
    )
    if not updated_movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting movement not found"
        )
    return updated_movimiento


@router.delete("/movements/{movimiento_id}")
def delete_accounting_movement(movimiento_id: str, db: Session = Depends(get_db)):
    """Delete an accounting movement"""
    success = delete_movimiento_contable(db=db, movimiento_id=movimiento_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accounting movement not found"
        )
    return {"message": "Accounting movement deleted successfully"}


# ============================================================================
# FINANCIAL STATEMENT ENDPOINTS
# ============================================================================

@router.post("/financial-statements/", response_model=EstadoFinancieroResponse)
def create_financial_statement(estado: EstadoFinancieroCreate, db: Session = Depends(get_db)):
    """Create a new financial statement"""
    return create_estado_financiero(db=db, estado_data=estado)


@router.get("/financial-statements/{estado_id}", response_model=EstadoFinancieroResponse)
def get_financial_statement(estado_id: str, db: Session = Depends(get_db)):
    """Get a financial statement by ID"""
    estado = get_estado_financiero(db, estado_id)
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial statement not found"
        )
    return estado


@router.get("/financial-statements/type/{tipo_estado}", response_model=List[EstadoFinancieroResponse])
def get_statements_by_type(
    tipo_estado: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get financial statements by type"""
    return get_estados_financieros_by_tipo(db, tipo_estado, skip, limit)


@router.put("/financial-statements/{estado_id}", response_model=EstadoFinancieroResponse)
def update_financial_statement(
    estado_id: str, 
    estado_data: EstadoFinancieroUpdate, 
    db: Session = Depends(get_db)
):
    """Update a financial statement"""
    updated_estado = update_estado_financiero(
        db=db, 
        estado_id=estado_id, 
        estado_data=estado_data
    )
    if not updated_estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial statement not found"
        )
    return updated_estado


@router.delete("/financial-statements/{estado_id}")
def delete_financial_statement(estado_id: str, db: Session = Depends(get_db)):
    """Delete a financial statement"""
    success = delete_estado_financiero(db=db, estado_id=estado_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial statement not found"
        )
    return {"message": "Financial statement deleted successfully"}


# ============================================================================
# COST CENTER ENDPOINTS
# ============================================================================

@router.post("/cost-centers/", response_model=CentroCostoResponse)
def create_cost_center(centro: CentroCostoCreate, db: Session = Depends(get_db)):
    """Create a new cost center"""
    try:
        return create_centro_costo(db=db, centro_data=centro)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/cost-centers/{centro_id}", response_model=CentroCostoResponse)
def get_cost_center(centro_id: str, db: Session = Depends(get_db)):
    """Get a cost center by ID"""
    centro = get_centro_costo(db, centro_id)
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found"
        )
    return centro


@router.get("/cost-centers/code/{codigo}", response_model=CentroCostoResponse)
def get_cost_center_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a cost center by code"""
    centro = get_centro_costo_by_codigo(db, codigo)
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found"
        )
    return centro


@router.get("/cost-centers/", response_model=List[CentroCostoResponse])
def get_cost_centers(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of cost centers, optionally filtered"""
    return get_centros_costo(db, skip, limit, activo)


@router.put("/cost-centers/{centro_id}", response_model=CentroCostoResponse)
def update_cost_center(
    centro_id: str, 
    centro_data: CentroCostoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a cost center"""
    updated_centro = update_centro_costo(
        db=db, 
        centro_id=centro_id, 
        centro_data=centro_data
    )
    if not updated_centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found"
        )
    return updated_centro


@router.delete("/cost-centers/{centro_id}")
def delete_cost_center(centro_id: str, db: Session = Depends(get_db)):
    """Delete a cost center"""
    success = delete_centro_costo(db=db, centro_id=centro_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cost center not found"
        )
    return {"message": "Cost center deleted successfully"}


# ============================================================================
# BUDGETARY ENTRY ENDPOINTS
# ============================================================================

@router.post("/budgetary-entries/", response_model=PartidaPresupuestalResponse)
def create_budgetary_entry(partida: PartidaPresupuestalCreate, db: Session = Depends(get_db)):
    """Create a new budgetary entry"""
    try:
        return create_partida_presupuestal(db=db, partida_data=partida)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/budgetary-entries/{partida_id}", response_model=PartidaPresupuestalResponse)
def get_budgetary_entry(partida_id: str, db: Session = Depends(get_db)):
    """Get a budgetary entry by ID"""
    partida = get_partida_presupuestal(db, partida_id)
    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budgetary entry not found"
        )
    return partida


@router.get("/budgetary-entries/code/{codigo}", response_model=PartidaPresupuestalResponse)
def get_budgetary_entry_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a budgetary entry by code"""
    partida = get_partida_presupuestal_by_codigo(db, codigo)
    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budgetary entry not found"
        )
    return partida


@router.get("/budgetary-entries/", response_model=List[PartidaPresupuestalResponse])
def get_budgetary_entries(
    skip: int = 0, 
    limit: int = 100,
    centro_costo_id: Optional[str] = None,
    periodo_fiscal_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of budgetary entries, optionally filtered"""
    centro_uuid = UUID(centro_costo_id) if centro_costo_id else None
    periodo_uuid = UUID(periodo_fiscal_id) if periodo_fiscal_id else None
    return get_partidas_presupuestales(db, skip, limit, centro_uuid, periodo_uuid)


@router.put("/budgetary-entries/{partida_id}", response_model=PartidaPresupuestalResponse)
def update_budgetary_entry(
    partida_id: str, 
    partida_data: PartidaPresupuestalUpdate, 
    db: Session = Depends(get_db)
):
    """Update a budgetary entry"""
    updated_partida = update_partida_presupuestal(
        db=db, 
        partida_id=partida_id, 
        partida_data=partida_data
    )
    if not updated_partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budgetary entry not found"
        )
    return updated_partida


@router.delete("/budgetary-entries/{partida_id}")
def delete_budgetary_entry(partida_id: str, db: Session = Depends(get_db)):
    """Delete a budgetary entry"""
    success = delete_partida_presupuestal(db=db, partida_id=partida_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budgetary entry not found"
        )
    return {"message": "Budgetary entry deleted successfully"}