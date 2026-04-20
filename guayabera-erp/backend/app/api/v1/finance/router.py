"""
API routes for accounting module
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal

from app.core.database import get_db
from app.schemas.finance import (
    CuentaContableCreate, CuentaContableUpdate, CuentaContableResponse,
    CentroCostoCreate, CentroCostoUpdate, CentroCostoResponse,
    PolizaContableCreate, PolizaContableUpdate, PolizaContableResponse,
    PolizaContableSummary,
    BancoCreate, BancoUpdate, BancoResponse,
    MovimientoBancarioCreate, MovimientoBancarioResponse,
    PeriodoContableCreate, PeriodoContableUpdate, PeriodoContableResponse,
    BalanzaComprobacionRequest, BalanzaComprobacionResponse, BalanzaComprobacionLinea,
    EstadoResultadosResponse
)
from app.crud import finance as crud
from app.models.finance import PeriodoContable
from app.core.security import get_current_user

router = APIRouter()


# ============= CUENTAS CONTABLES =============

@router.post("/cuentas", response_model=CuentaContableResponse, status_code=status.HTTP_201_CREATED)
async def crear_cuenta_contable(
    cuenta: CuentaContableCreate,
    db: Session = Depends(get_db)
):
    """Create new accounting account"""
    # Check if code already exists
    existing = crud.get_cuenta_by_codigo(db, cuenta.codigo)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Código de cuenta '{cuenta.codigo}' ya existe"
        )
    
    return crud.create_cuenta(db, cuenta)


@router.get("/cuentas", response_model=List[CuentaContableResponse])
async def listar_cuentas_contables(
    tipo: str = None,
    solo_mayor: bool = False,
    db: Session = Depends(get_db)
):
    """List all accounting accounts"""
    return crud.get_cuentas(db, tipo=tipo, solo_mayor=solo_mayor)


@router.get("/cuentas/{cuenta_id}", response_model=CuentaContableResponse)
async def obtener_cuenta_contable(
    cuenta_id: UUID,
    db: Session = Depends(get_db)
):
    """Get account by ID"""
    cuenta = crud.get_cuenta_by_id(db, cuenta_id)
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return cuenta


@router.put("/cuentas/{cuenta_id}", response_model=CuentaContableResponse)
async def actualizar_cuenta_contable(
    cuenta_id: UUID,
    cuenta: CuentaContableUpdate,
    db: Session = Depends(get_db)
):
    """Update account"""
    updated = crud.update_cuenta(db, cuenta_id, cuenta)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return updated


@router.post("/cuentas/importar-sat")
async def importar_catalogo_sat(
    db: Session = Depends(get_db)
):
    """Import SAT Mexico chart of accounts"""
    from app.services.sat_catalog import importar_catalogo_sat
    count = importar_catalogo_sat(db)
    return {
        "message": f"Catálogo importado exitosamente",
        "cuentas_importadas": count
    }


# ============= CENTROS DE COSTO =============

@router.post("/centros-costo", response_model=CentroCostoResponse, status_code=status.HTTP_201_CREATED)
async def crear_centro_costo(
    centro: CentroCostoCreate,
    db: Session = Depends(get_db)
):
    """Create cost center"""
    existing = crud.get_centro_costo_by_id(db, centro.id) if hasattr(centro, 'id') else None
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Centro de costo ya existe"
        )
    
    return crud.create_centro_costo(
        db, centro.codigo, centro.nombre, centro.descripcion
    )


@router.get("/centros-costo", response_model=List[CentroCostoResponse])
async def listar_centros_costo(db: Session = Depends(get_db)):
    """List cost centers"""
    return crud.get_centros_costo(db)


# ============= POLIZAS CONTABLES =============

@router.post("/polizas", response_model=PolizaContableResponse, status_code=status.HTTP_201_CREATED)
async def crear_poliza_contable(
    poliza: PolizaContableCreate,
    db: Session = Depends(get_db)
):
    """Create accounting policy with journal entries"""
    try:
        return crud.create_poliza(db, poliza)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/polizas", response_model=List[PolizaContableSummary])
async def listar_polizas(
    fecha_desde: date = None,
    fecha_hasta: date = None,
    tipo: str = None,
    estado: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List policies with filters"""
    return crud.get_polizas(
        db, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
        tipo=tipo, estado=estado, skip=skip, limit=limit
    )


@router.get("/polizas/{poliza_id}", response_model=PolizaContableResponse)
async def obtener_poliza(
    poliza_id: UUID,
    db: Session = Depends(get_db)
):
    """Get policy by ID"""
    poliza = crud.get_poliza_by_id(db, poliza_id)
    if not poliza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Póliza no encontrada"
        )
    return poliza


@router.put("/polizas/{poliza_id}/estado")
async def actualizar_estado_poliza(
    poliza_id: UUID,
    nuevo_estado: str,
    db: Session = Depends(get_db)
):
    """Update policy status (revisada, aprobada, cancelada)"""
    try:
        poliza = crud.update_poliza_estado(db, poliza_id, nuevo_estado)
        if not poliza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Póliza no encontrada"
            )
        return poliza
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/polizas/{poliza_id}/cancelar")
async def cancelar_poliza(
    poliza_id: UUID,
    motivo: str = None,
    db: Session = Depends(get_db)
):
    """Cancel policy"""
    try:
        poliza = crud.cancel_poliza(db, poliza_id, motivo)
        if not poliza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Póliza no encontrada"
            )
        return poliza
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============= BANCOS =============

@router.post("/bancos", response_model=BancoResponse, status_code=status.HTTP_201_CREATED)
async def crear_banco(
    banco: BancoCreate,
    db: Session = Depends(get_db)
):
    """Create bank account"""
    existing = crud.get_banco_by_cuenta(db, banco.cuenta)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cuenta bancaria '{banco.cuenta}' ya existe"
        )
    
    return crud.create_banco(db, banco)


@router.get("/bancos", response_model=List[BancoResponse])
async def listar_bancos(db: Session = Depends(get_db)):
    """List bank accounts"""
    return crud.get_bancos(db)


@router.get("/bancos/{banco_id}", response_model=BancoResponse)
async def obtener_banco(banco_id: UUID, db: Session = Depends(get_db)):
    """Get bank by ID"""
    banco = crud.get_banco_by_id(db, banco_id)
    if not banco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banco no encontrado"
        )
    return banco


# ============= MOVIMIENTOS BANCARIOS =============

@router.get("/bancos/{banco_id}/movimientos", response_model=List[MovimientoBancarioResponse])
async def listar_movimientos_bancarios(
    banco_id: UUID,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    solo_pendientes: bool = False,
    db: Session = Depends(get_db)
):
    """List bank statement lines"""
    return crud.get_movimientos_bancarios(
        db, banco_id, fecha_desde=fecha_desde, 
        fecha_hasta=fecha_hasta, solo_pendientes=solo_pendientes
    )


@router.post("/bancos/{banco_id}/movimientos", response_model=MovimientoBancarioResponse)
async def crear_movimiento_bancario(
    banco_id: UUID,
    movimiento: MovimientoBancarioCreate,
    db: Session = Depends(get_db)
):
    """Create bank movement"""
    banco = crud.get_banco_by_id(db, banco_id)
    if not banco:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banco no encontrado"
        )
    
    return crud.create_movimiento_bancario(
        db, banco_id, movimiento.fecha, movimiento.descripcion,
        movimiento.cargo, movimiento.abono,
        referencia=movimiento.referencia,
        tipo_movimiento=movimiento.tipo_movimiento,
        saldo=movimiento.saldo
    )


# ============= BALANZA DE COMPROBACIÓN =============

@router.post("/reportes/balanza-comprobacion", response_model=BalanzaComprobacionResponse)
async def generar_balanza_comprobacion(
    request: BalanzaComprobacionRequest,
    db: Session = Depends(get_db)
):
    """Generate trial balance report"""
    balanza_data = crud.get_balanza_comprobacion(db, request)
    
    # Calculate totals
    total_cargos = sum(linea['cargos'] for linea in balanza_data)
    total_abonos = sum(linea['abonos'] for linea in balanza_data)
    
    lineas = [BalanzaComprobacionLinea(**linea) for linea in balanza_data]
    
    return BalanzaComprobacionResponse(
        fecha_desde=request.fecha_desde,
        fecha_hasta=request.fecha_hasta,
        lineas=lineas,
        total_cargos=Decimal(str(total_cargos)),
        total_abonos=Decimal(str(total_abonos)),
        esta_cuadrada=(abs(total_cargos - total_abonos) < Decimal('0.01'))
    )


# ============= ESTADO DE RESULTADOS =============

@router.get("/reportes/estado-resultados", response_model=EstadoResultadosResponse)
async def generar_estado_resultados(
    fecha_desde: date,
    fecha_hasta: date,
    db: Session = Depends(get_db)
):
    """Generate income statement"""
    # Simplified version - in production, query actual account balances
    return EstadoResultadosResponse(
        periodo_inicio=fecha_desde,
        periodo_fin=fecha_hasta,
        ingresos=Decimal('0.00'),
        costos=Decimal('0.00'),
        utilidad_bruta=Decimal('0.00'),
        gastos_operacion=Decimal('0.00'),
        utilidad_operacion=Decimal('0.00'),
        otros_ingresos=Decimal('0.00'),
        otros_gastos=Decimal('0.00'),
        utilidad_neta=Decimal('0.00')
    )


# ============= PERIODOS CONTABLES =============

@router.post("/periodos", response_model=PeriodoContableResponse, status_code=status.HTTP_201_CREATED)
async def crear_periodo_contable(
    periodo: PeriodoContableCreate,
    db: Session = Depends(get_db)
):
    """Create accounting period"""
    existing = crud.get_periodo_by_fecha(db, periodo.fecha_inicio)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un período para la fecha {periodo.fecha_inicio}"
        )
    
    db_periodo = PeriodoContable(**periodo.dict())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo


@router.get("/periodos", response_model=List[PeriodoContableResponse])
async def listar_periodos(year: int = None, db: Session = Depends(get_db)):
    """List accounting periods"""
    return crud.get_periodos(db, year=year)


@router.post("/periodos/{periodo_id}/cerrar")
async def cerrar_periodo(periodo_id: UUID, db: Session = Depends(get_db)):
    """Close accounting period"""
    periodo = crud.cerrar_periodo(db, periodo_id)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Período no encontrado"
        )
    return periodo
