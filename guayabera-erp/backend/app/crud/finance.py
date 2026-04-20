"""
CRUD operations for accounting module
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal

from app.models.finance import (
    CuentaContable, CentroCosto, PolizaContable, MovimientoPoliza,
    Banco, MovimientoBancario, AsientoContable, PeriodoContable
)
from app.schemas.finance import (
    CuentaContableCreate, CuentaContableUpdate,
    PolizaContableCreate, PolizaContableUpdate,
    BancoCreate, BancoUpdate,
    BalanzaComprobacionRequest
)


# ============= CUENTAS CONTABLES =============

def get_cuenta_by_id(db: Session, cuenta_id: UUID) -> Optional[CuentaContable]:
    """Get account by ID"""
    return db.query(CuentaContable).filter(CuentaContable.id == cuenta_id).first()


def get_cuenta_by_codigo(db: Session, codigo: str) -> Optional[CuentaContable]:
    """Get account by code"""
    return db.query(CuentaContable).filter(CuentaContable.codigo == codigo).first()


def get_cuentas(db: Session, tipo: str = None, solo_mayor: bool = False, 
                activas_only: bool = True) -> List[CuentaContable]:
    """Get chart of accounts with optional filters"""
    query = db.query(CuentaContable)
    
    if tipo:
        query = query.filter(CuentaContable.tipo == tipo)
    if solo_mayor:
        query = query.filter(CuentaContable.es_cuenta_mayor == True)
    if activas_only:
        query = query.filter(CuentaContable.activa == True)
    
    return query.order_by(CuentaContable.codigo).all()


def get_cuentas_tree(db: Session, activas_only: bool = True) -> List[CuentaContable]:
    """Get accounts as hierarchical tree"""
    query = db.query(CuentaContable)
    if activas_only:
        query = query.filter(CuentaContable.activa == True)
    return query.order_by(CuentaContable.codigo).all()


def create_cuenta(db: Session, cuenta: CuentaContableCreate) -> CuentaContable:
    """Create new account"""
    db_cuenta = CuentaContable(**cuenta.dict())
    db.add(db_cuenta)
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


def update_cuenta(db: Session, cuenta_id: UUID, cuenta: CuentaContableUpdate) -> Optional[CuentaContable]:
    """Update account"""
    db_cuenta = get_cuenta_by_id(db, cuenta_id)
    if not db_cuenta:
        return None
    
    update_data = cuenta.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cuenta, key, value)
    
    db.commit()
    db.refresh(db_cuenta)
    return db_cuenta


def bulk_create_cuentas(db: Session, cuentas: List[dict]) -> int:
    """Bulk create accounts (for SAT catalog import)"""
    count = 0
    for cuenta_data in cuentas:
        existing = get_cuenta_by_codigo(db, cuenta_data['codigo'])
        if not existing:
            db_cuenta = CuentaContable(**cuenta_data)
            db.add(db_cuenta)
            count += 1
    
    db.commit()
    return count


# ============= CENTROS DE COSTO =============

def get_centro_costo_by_id(db: Session, centro_id: UUID) -> Optional[CentroCosto]:
    return db.query(CentroCosto).filter(CentroCosto.id == centro_id).first()


def get_centros_costo(db: Session, activos_only: bool = True) -> List[CentroCosto]:
    query = db.query(CentroCosto)
    if activos_only:
        query = query.filter(CentroCosto.activo == True)
    return query.order_by(CentroCosto.codigo).all()


def create_centro_costo(db: Session, codigo: str, nombre: str, 
                        descripcion: str = None) -> CentroCosto:
    db_centro = CentroCosto(codigo=codigo, nombre=nombre, descripcion=descripcion)
    db.add(db_centro)
    db.commit()
    db.refresh(db_centro)
    return db_centro


# ============= POLIZAS CONTABLES =============

def get_poliza_by_id(db: Session, poliza_id: UUID) -> Optional[PolizaContable]:
    """Get policy by ID with movements"""
    return db.query(PolizaContable).filter(PolizaContable.id == poliza_id).first()


def get_poliza_by_numero(db: Session, numero: int, tipo: str, 
                         fecha: date) -> Optional[PolizaContable]:
    """Get policy by number, type and date"""
    return db.query(PolizaContable).filter(
        and_(
            PolizaContable.numero == numero,
            PolizaContable.tipo == tipo,
            PolizaContable.fecha == fecha
        )
    ).first()


def get_polizas(db: Session, fecha_desde: date = None, fecha_hasta: date = None,
                tipo: str = None, estado: str = None, 
                skip: int = 0, limit: int = 100) -> List[PolizaContable]:
    """Get policies with filters"""
    query = db.query(PolizaContable)
    
    if fecha_desde:
        query = query.filter(PolizaContable.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(PolizaContable.fecha <= fecha_hasta)
    if tipo:
        query = query.filter(PolizaContable.tipo == tipo)
    if estado:
        query = query.filter(PolizaContable.estado == estado)
    
    return query.order_by(PolizaContable.fecha.desc(), PolizaContable.numero.desc())\
                .offset(skip).limit(limit).all()


def get_next_poliza_numero(db: Session, tipo: str, fecha: date) -> int:
    """Get next policy number for type and date"""
    last_poliza = db.query(PolizaContable).filter(
        and_(
            PolizaContable.tipo == tipo,
            func.extract('year', PolizaContable.fecha) == fecha.year
        )
    ).order_by(PolizaContable.numero.desc()).first()
    
    return (last_poliza.numero + 1) if last_poliza else 1


def create_poliza(db: Session, poliza: PolizaContableCreate, 
                  preparado_por: UUID = None) -> PolizaContable:
    """Create new policy with movements"""
    # Get next number
    numero = get_next_poliza_numero(db, poliza.tipo, poliza.fecha)
    
    # Create policy
    total_cargos = sum(m.cargo for m in poliza.movimientos)
    total_abonos = sum(m.abono for m in poliza.movimientos)
    
    db_poliza = PolizaContable(
        numero=numero,
        tipo=poliza.tipo,
        fecha=poliza.fecha,
        descripcion=poliza.descripcion,
        comentario_adicional=poliza.comentario_adicional,
        modulo_origen=poliza.modulo_origen,
        referencia_externa=poliza.referencia_externa,
        total_cargos=total_cargos,
        total_abonos=total_abonos,
        esta_cuadrada=(total_cargos == total_abonos),
        preparado_por=preparado_por
    )
    db.add(db_poliza)
    db.flush()
    
    # Create movements
    for mov in poliza.movimientos:
        db_movimiento = MovimientoPoliza(
            poliza_id=db_poliza.id,
            cuenta_id=mov.cuenta_id,
            centro_costo_id=mov.centro_costo_id,
            cargo=mov.cargo,
            abono=mov.abono,
            concepto=mov.concepto,
            referencia=mov.referencia,
            documento_referencia=mov.documento_referencia,
            fecha_documento=mov.fecha_documento
        )
        db.add(db_movimiento)
    
    db.commit()
    db.refresh(db_poliza)
    return db_poliza


def update_poliza_estado(db: Session, poliza_id: UUID, nuevo_estado: str,
                         usuario_id: UUID = None) -> Optional[PolizaContable]:
    """Update policy status (revisada, aprobada, cancelada)"""
    db_poliza = get_poliza_by_id(db, poliza_id)
    if not db_poliza:
        return None
    
    db_poliza.estado = nuevo_estado
    if nuevo_estado == 'aprobada':
        from datetime import datetime
        db_poliza.fecha_aprobacion = datetime.utcnow()
        db_poliza.aprobado_por = usuario_id
    
    db.commit()
    db.refresh(db_poliza)
    return db_poliza


def cancel_poliza(db: Session, poliza_id: UUID, 
                  motivo: str = None) -> Optional[PolizaContable]:
    """Cancel policy"""
    db_poliza = get_poliza_by_id(db, poliza_id)
    if not db_poliza:
        return None
    
    if db_poliza.estado == 'aprobada':
        raise ValueError("No se puede cancelar una póliza aprobada")
    
    db_poliza.estado = 'cancelada'
    db_poliza.comentario_adicional = f"Cancelada: {motivo}" if motivo else "Cancelada"
    
    db.commit()
    db.refresh(db_poliza)
    return db_poliza


# ============= BANCOS =============

def get_banco_by_id(db: Session, banco_id: UUID) -> Optional[Banco]:
    return db.query(Banco).filter(Banco.id == banco_id).first()


def get_banco_by_cuenta(db: Session, cuenta: str) -> Optional[Banco]:
    return db.query(Banco).filter(Banco.cuenta == cuenta).first()


def get_bancos(db: Session, activos_only: bool = True) -> List[Banco]:
    query = db.query(Banco)
    if activos_only:
        query = query.filter(Banco.activo == True)
    return query.all()


def create_banco(db: Session, banco: BancoCreate) -> Banco:
    db_banco = Banco(**banco.dict())
    db.add(db_banco)
    db.commit()
    db.refresh(db_banco)
    return db_banco


def update_banco_saldo(db: Session, banco_id: UUID, 
                       nuevo_saldo: Decimal) -> Optional[Banco]:
    """Update bank balance"""
    db_banco = get_banco_by_id(db, banco_id)
    if not db_banco:
        return None
    
    db_banco.saldo_actual = nuevo_saldo
    db.commit()
    db.refresh(db_banco)
    return db_banco


# ============= MOVIMIENTOS BANCARIOS =============

def get_movimientos_bancarios(db: Session, banco_id: UUID, 
                              fecha_desde: date = None, fecha_hasta: date = None,
                              solo_pendientes: bool = False) -> List[MovimientoBancario]:
    """Get bank statement lines"""
    query = db.query(MovimientoBancario).filter(MovimientoBancario.banco_id == banco_id)
    
    if fecha_desde:
        query = query.filter(MovimientoBancario.fecha >= fecha_desde)
    if fecha_hasta:
        query = query.filter(MovimientoBancario.fecha <= fecha_hasta)
    if solo_pendientes:
        query = query.filter(MovimientoBancario.conciliado == False)
    
    return query.order_by(MovimientoBancario.fecha).all()


def create_movimiento_bancario(db: Session, banco_id: UUID, fecha: date,
                               descripcion: str, cargo: Decimal = 0, 
                               abono: Decimal = 0, **kwargs) -> MovimientoBancario:
    """Create bank movement"""
    db_mov = MovimientoBancario(
        banco_id=banco_id,
        fecha=fecha,
        descripcion=descripcion,
        cargo=cargo,
        abono=abono,
        **kwargs
    )
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov


def conciliar_movimiento(db: Session, movimiento_id: UUID, 
                         poliza_id: UUID = None) -> Optional[MovimientoBancario]:
    """Reconcile bank movement"""
    db_mov = db.query(MovimientoBancario).filter(
        MovimientoBancario.id == movimiento_id
    ).first()
    
    if not db_mov:
        return None
    
    from datetime import datetime
    db_mov.conciliado = True
    db_mov.fecha_conciliacion = datetime.utcnow()
    if poliza_id:
        db_mov.poliza_id = poliza_id
    
    db.commit()
    db.refresh(db_mov)
    return db_mov


# ============= BALANZA DE COMPROBACIÓN =============

def get_balanza_comprobacion(db: Session, request: BalanzaComprobacionRequest) -> List[dict]:
    """Generate trial balance"""
    # Get all accounts
    cuentas = get_cuentas(db, activas_only=True)
    
    balanza = []
    for cuenta in cuentas:
        if request.solo_movimientos:
            # Only accounts with movements
            mov_count = db.query(func.count(MovimientoPoliza.id)).join(
                PolizaContable
            ).filter(
                MovimientoPoliza.cuenta_id == cuenta.id,
                PolizaContable.fecha >= request.fecha_desde,
                PolizaContable.fecha <= request.fecha_hasta,
                PolizaContable.estado != 'cancelada'
            ).scalar()
            
            if mov_count == 0:
                continue
        
        # Get initial balance (before period)
        initial_query = db.query(
            func.coalesce(func.sum(MovimientoPoliza.cargo), 0),
            func.coalesce(func.sum(MovimientoPoliza.abono), 0)
        ).join(PolizaContable).filter(
            MovimientoPoliza.cuenta_id == cuenta.id,
            PolizaContable.fecha < request.fecha_desde,
            PolizaContable.estado != 'cancelada'
        )
        
        initial_cargos, initial_abonos = initial_query.first()
        
        # Calculate initial balance based on account nature
        if cuenta.naturaleza == 'deudora':
            saldo_inicial = initial_cargos - initial_abonos
        else:
            saldo_inicial = initial_abonos - initial_cargos
        
        # Get movements in period
        period_query = db.query(
            func.coalesce(func.sum(MovimientoPoliza.cargo), 0),
            func.coalesce(func.sum(MovimientoPoliza.abono), 0)
        ).join(PolizaContable).filter(
            MovimientoPoliza.cuenta_id == cuenta.id,
            PolizaContable.fecha >= request.fecha_desde,
            PolizaContable.fecha <= request.fecha_hasta,
            PolizaContable.estado != 'cancelada'
        )
        
        cargos_periodo, abonos_periodo = period_query.first()
        
        # Calculate final balance
        if cuenta.naturaleza == 'deudora':
            saldo_final = saldo_inicial + cargos_periodo - abonos_periodo
        else:
            saldo_final = saldo_inicial + abonos_periodo - cargos_periodo
        
        balanza.append({
            'cuenta_id': cuenta.id,
            'cuenta_codigo': cuenta.codigo,
            'cuenta_nombre': cuenta.nombre,
            'nivel': cuenta.nivel,
            'tipo': cuenta.tipo,
            'saldo_inicial': Decimal(str(saldo_inicial)),
            'cargos': Decimal(str(cargos_periodo)),
            'abonos': Decimal(str(abonos_periodo)),
            'saldo_final': Decimal(str(saldo_final))
        })
    
    return balanza


# ============= PERIODOS CONTABLES =============

def get_periodo_by_id(db: Session, periodo_id: UUID) -> Optional[PeriodoContable]:
    return db.query(PeriodoContable).filter(PeriodoContable.id == periodo_id).first()


def get_periodo_by_fecha(db: Session, fecha: date) -> Optional[PeriodoContable]:
    """Get accounting period for a date"""
    return db.query(PeriodoContable).filter(
        and_(
            PeriodoContable.fecha_inicio <= fecha,
            PeriodoContable.fecha_fin >= fecha
        )
    ).first()


def get_periodos(db: Session, year: int = None) -> List[PeriodoContable]:
    query = db.query(PeriodoContable)
    if year:
        query = query.filter(func.extract('year', PeriodoContable.fecha_inicio) == year)
    return query.order_by(PeriodoContable.fecha_inicio).all()


def cerrar_periodo(db: Session, periodo_id: UUID) -> Optional[PeriodoContable]:
    """Close accounting period"""
    db_periodo = get_periodo_by_id(db, periodo_id)
    if not db_periodo:
        return None
    
    from datetime import datetime
    db_periodo.estado = 'cerrado'
    db_periodo.fecha_cierre = datetime.utcnow()
    
    db.commit()
    db.refresh(db_periodo)
    return db_periodo
