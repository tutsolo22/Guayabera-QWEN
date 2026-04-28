"""
Payroll CRUD Operations: Electronic payroll according to Mexican SAT regulations
Integration with CFDI payroll complement
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.payroll import (
    PeriodoNomina, Nomina, Percepcion, 
    Deduccion, Incapacidad, OtroPago
)
from app.schemas.payroll import (
    PeriodoNominaCreate, PeriodoNominaUpdate,
    NominaCreate, NominaUpdate,
    PercepcionCreate, PercepcionUpdate,
    DeduccionCreate, DeduccionUpdate,
    IncapacidadCreate, IncapacidadUpdate,
    OtroPagoCreate, OtroPagoUpdate
)


# ============================================================================
# PAYROLL PERIOD CRUD
# ============================================================================

def create_periodo_nomina(db: Session, periodo_data: PeriodoNominaCreate) -> PeriodoNomina:
    """Create a new payroll period"""
    # Check if period code already exists
    existing_periodo = db.query(PeriodoNomina).filter(
        PeriodoNomina.codigo == periodo_data.codigo
    ).first()
    if existing_periodo:
        raise ValueError(f"A payroll period with code {periodo_data.codigo} already exists")
    
    db_periodo = PeriodoNomina(**periodo_data.model_dump())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo


def get_periodo_nomina(db: Session, periodo_id: UUID) -> Optional[PeriodoNomina]:
    """Get a payroll period by ID"""
    return db.query(PeriodoNomina).filter(PeriodoNomina.id == periodo_id).first()


def get_periodo_nomina_by_codigo(db: Session, codigo: str) -> Optional[PeriodoNomina]:
    """Get a payroll period by code"""
    return db.query(PeriodoNomina).filter(PeriodoNomina.codigo == codigo).first()


def get_periodos_nomina(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    empresa_id: Optional[UUID] = None,
    cerrado: Optional[bool] = None
) -> List[PeriodoNomina]:
    """Get list of payroll periods, optionally filtered"""
    query = db.query(PeriodoNomina)
    
    if empresa_id:
        query = query.filter(PeriodoNomina.empresa_id == empresa_id)
    if cerrado is not None:
        query = query.filter(PeriodoNomina.cerrado == cerrado)
    
    return query.offset(skip).limit(limit).all()


def update_periodo_nomina(
    db: Session, 
    periodo_id: UUID, 
    periodo_data: PeriodoNominaUpdate
) -> Optional[PeriodoNomina]:
    """Update a payroll period"""
    db_periodo = get_periodo_nomina(db, periodo_id)
    if db_periodo:
        update_data = periodo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_periodo, field, value)
        db.commit()
        db.refresh(db_periodo)
    return db_periodo


def delete_periodo_nomina(db: Session, periodo_id: UUID) -> bool:
    """Soft delete a payroll period"""
    db_periodo = get_periodo_nomina(db, periodo_id)
    if db_periodo:
        db_periodo.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# PAYROLL RECEIPT CRUD
# ============================================================================

def create_nomina(db: Session, nomina_data: NominaCreate) -> Nomina:
    """Create a new payroll receipt"""
    # Check if folio already exists
    existing_nomina = db.query(Nomina).filter(
        Nomina.folio == nomina_data.folio
    ).first()
    if existing_nomina:
        raise ValueError(f"A payroll receipt with folio {nomina_data.folio} already exists")
    
    db_nomina = Nomina(**nomina_data.model_dump())
    db.add(db_nomina)
    db.commit()
    db.refresh(db_nomina)
    return db_nomina


def get_nomina(db: Session, nomina_id: UUID) -> Optional[Nomina]:
    """Get a payroll receipt by ID"""
    return db.query(Nomina).filter(Nomina.id == nomina_id).first()


def get_nomina_by_folio(db: Session, folio: str) -> Optional[Nomina]:
    """Get a payroll receipt by folio"""
    return db.query(Nomina).filter(Nomina.folio == folio).first()


def get_nominas_by_periodo(db: Session, periodo_id: UUID) -> List[Nomina]:
    """Get all payroll receipts for a specific period"""
    return db.query(Nomina).filter(Nomina.periodo_id == periodo_id).all()


def get_nominas_by_empleado(
    db: Session, 
    empleado_id: UUID,
    skip: int = 0, 
    limit: int = 100
) -> List[Nomina]:
    """Get all payroll receipts for a specific employee"""
    return db.query(Nomina).filter(
        Nomina.empleado_id == empleado_id
    ).offset(skip).limit(limit).all()


def update_nomina(
    db: Session, 
    nomina_id: UUID, 
    nomina_data: NominaUpdate
) -> Optional[Nomina]:
    """Update a payroll receipt"""
    db_nomina = get_nomina(db, nomina_id)
    if db_nomina:
        update_data = nomina_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_nomina, field, value)
        db.commit()
        db.refresh(db_nomina)
    return db_nomina


def delete_nomina(db: Session, nomina_id: UUID) -> bool:
    """Soft delete a payroll receipt"""
    db_nomina = get_nomina(db, nomina_id)
    if db_nomina:
        db_nomina.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# PERCEPTION CRUD
# ============================================================================

def create_percepcion(db: Session, percepcion_data: PercepcionCreate) -> Percepcion:
    """Create a new payroll perception"""
    # Verify the payroll receipt exists
    nomina = get_nomina(db, percepcion_data.nomina_id)
    if not nomina:
        raise ValueError(f"Payroll receipt with ID {percepcion_data.nomina_id} does not exist")
    
    db_percepcion = Percepcion(**percepcion_data.model_dump())
    db.add(db_percepcion)
    db.commit()
    db.refresh(db_percepcion)
    return db_percepcion


def get_percepcion(db: Session, percepcion_id: UUID) -> Optional[Percepcion]:
    """Get a payroll perception by ID"""
    return db.query(Percepcion).filter(Percepcion.id == percepcion_id).first()


def get_percepciones_by_nomina(db: Session, nomina_id: UUID) -> List[Percepcion]:
    """Get all perceptions for a specific payroll receipt"""
    return db.query(Percepcion).filter(
        Percepcion.nomina_id == nomina_id
    ).all()


def update_percepcion(
    db: Session, 
    percepcion_id: UUID, 
    percepcion_data: PercepcionUpdate
) -> Optional[Percepcion]:
    """Update a payroll perception"""
    db_percepcion = get_percepcion(db, percepcion_id)
    if db_percepcion:
        update_data = percepcion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_percepcion, field, value)
        db.commit()
        db.refresh(db_percepcion)
    return db_percepcion


def delete_percepcion(db: Session, percepcion_id: UUID) -> bool:
    """Delete a payroll perception"""
    db_percepcion = get_percepcion(db, percepcion_id)
    if db_percepcion:
        db.delete(db_percepcion)
        db.commit()
        return True
    return False


# ============================================================================
# DEDUCTION CRUD
# ============================================================================

def create_deduccion(db: Session, deduccion_data: DeduccionCreate) -> Deduccion:
    """Create a new payroll deduction"""
    # Verify the payroll receipt exists
    nomina = get_nomina(db, deduccion_data.nomina_id)
    if not nomina:
        raise ValueError(f"Payroll receipt with ID {deduccion_data.nomina_id} does not exist")
    
    db_deduccion = Deduccion(**deduccion_data.model_dump())
    db.add(db_deduccion)
    db.commit()
    db.refresh(db_deduccion)
    return db_deduccion


def get_deduccion(db: Session, deduccion_id: UUID) -> Optional[Deduccion]:
    """Get a payroll deduction by ID"""
    return db.query(Deduccion).filter(Deduccion.id == deduccion_id).first()


def get_deducciones_by_nomina(db: Session, nomina_id: UUID) -> List[Deduccion]:
    """Get all deductions for a specific payroll receipt"""
    return db.query(Deduccion).filter(
        Deduccion.nomina_id == nomina_id
    ).all()


def update_deduccion(
    db: Session, 
    deduccion_id: UUID, 
    deduccion_data: DeduccionUpdate
) -> Optional[Deduccion]:
    """Update a payroll deduction"""
    db_deduccion = get_deduccion(db, deduccion_id)
    if db_deduccion:
        update_data = deduccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_deduccion, field, value)
        db.commit()
        db.refresh(db_deduccion)
    return db_deduccion


def delete_deduccion(db: Session, deduccion_id: UUID) -> bool:
    """Delete a payroll deduction"""
    db_deduccion = get_deduccion(db, deduccion_id)
    if db_deduccion:
        db.delete(db_deduccion)
        db.commit()
        return True
    return False


# ============================================================================
# INCAPACITY CRUD
# ============================================================================

def create_incapacidad(db: Session, incapacidad_data: IncapacidadCreate) -> Incapacidad:
    """Create a new employee incapacity"""
    # Verify the payroll receipt exists
    nomina = get_nomina(db, incapacidad_data.nomina_id)
    if not nomina:
        raise ValueError(f"Payroll receipt with ID {incapacidad_data.nomina_id} does not exist")
    
    db_incapacidad = Incapacidad(**incapacidad_data.model_dump())
    db.add(db_incapacidad)
    db.commit()
    db.refresh(db_incapacidad)
    return db_incapacidad


def get_incapacidad(db: Session, incapacidad_id: UUID) -> Optional[Incapacidad]:
    """Get an employee incapacity by ID"""
    return db.query(Incapacidad).filter(Incapacidad.id == incapacidad_id).first()


def get_incapacidades_by_nomina(db: Session, nomina_id: UUID) -> List[Incapacidad]:
    """Get all incapacities for a specific payroll receipt"""
    return db.query(Incapacidad).filter(
        Incapacidad.nomina_id == nomina_id
    ).all()


def update_incapacidad(
    db: Session, 
    incapacidad_id: UUID, 
    incapacidad_data: IncapacidadUpdate
) -> Optional[Incapacidad]:
    """Update an employee incapacity"""
    db_incapacidad = get_incapacidad(db, incapacidad_id)
    if db_incapacidad:
        update_data = incapacidad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_incapacidad, field, value)
        db.commit()
        db.refresh(db_incapacidad)
    return db_incapacidad


def delete_incapacidad(db: Session, incapacidad_id: UUID) -> bool:
    """Delete an employee incapacity"""
    db_incapacidad = get_incapacidad(db, incapacidad_id)
    if db_incapacidad:
        db.delete(db_incapacidad)
        db.commit()
        return True
    return False


# ============================================================================
# OTHER PAYMENT CRUD
# ============================================================================

def create_otro_pago(db: Session, otro_pago_data: OtroPagoCreate) -> OtroPago:
    """Create a new other payment"""
    # Verify the payroll receipt exists
    nomina = get_nomina(db, otro_pago_data.nomina_id)
    if not nomina:
        raise ValueError(f"Payroll receipt with ID {otro_pago_data.nomina_id} does not exist")
    
    db_otro_pago = OtroPago(**otro_pago_data.model_dump())
    db.add(db_otro_pago)
    db.commit()
    db.refresh(db_otro_pago)
    return db_otro_pago


def get_otro_pago(db: Session, otro_pago_id: UUID) -> Optional[OtroPago]:
    """Get an other payment by ID"""
    return db.query(OtroPago).filter(OtroPago.id == otro_pago_id).first()


def get_otros_pagos_by_nomina(db: Session, nomina_id: UUID) -> List[OtroPago]:
    """Get all other payments for a specific payroll receipt"""
    return db.query(OtroPago).filter(
        OtroPago.nomina_id == nomina_id
    ).all()


def update_otro_pago(
    db: Session, 
    otro_pago_id: UUID, 
    otro_pago_data: OtroPagoUpdate
) -> Optional[OtroPago]:
    """Update an other payment"""
    db_otro_pago = get_otro_pago(db, otro_pago_id)
    if db_otro_pago:
        update_data = otro_pago_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_otro_pago, field, value)
        db.commit()
        db.refresh(db_otro_pago)
    return db_otro_pago


def delete_otro_pago(db: Session, otro_pago_id: UUID) -> bool:
    """Delete an other payment"""
    db_otro_pago = get_otro_pago(db, otro_pago_id)
    if db_otro_pago:
        db.delete(db_otro_pago)
        db.commit()
        return True
    return False