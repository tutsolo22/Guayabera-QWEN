"""
Reports CRUD Operations: Generic reporting system for all ERP modules
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.reports import (
    Reporte, ReporteRH, ReporteProduccion, ReporteVentas, 
    ReporteInventario, ReporteFinanzas
)
from app.schemas.reports import (
    ReporteCreate, ReporteUpdate, ReporteResponse,
    ReporteRHCreate, ReporteRHUpdate, ReporteRHResponse,
    ReporteProduccionCreate, ReporteProduccionUpdate, ReporteProduccionResponse,
    ReporteVentasCreate, ReporteVentasUpdate, ReporteVentasResponse,
    ReporteInventarioCreate, ReporteInventarioUpdate, ReporteInventarioResponse,
    ReporteFinanzasCreate, ReporteFinanzasUpdate, ReporteFinanzasResponse
)


# ============================================================================
# REPORTES GENERALES CRUD
# ============================================================================

def create_reporte(db: Session, reporte_data: ReporteCreate) -> Reporte:
    """Create a new generic report"""
    db_reporte = Reporte(**reporte_data.model_dump())
    db.add(db_reporte)
    db.commit()
    db.refresh(db_reporte)
    return db_reporte


def get_reporte(db: Session, reporte_id: UUID) -> Optional[Reporte]:
    """Get a report by ID"""
    return db.query(Reporte).filter(Reporte.id == reporte_id).first()


def get_reporte_by_codigo(db: Session, codigo: str) -> Optional[Reporte]:
    """Get a report by code"""
    return db.query(Reporte).filter(Reporte.codigo == codigo).first()


def get_reportes(db: Session, skip: int = 0, limit: int = 100) -> List[Reporte]:
    """Get list of reports"""
    return db.query(Reporte).offset(skip).limit(limit).all()


def update_reporte(
    db: Session, 
    reporte_id: UUID, 
    reporte_data: ReporteUpdate
) -> Optional[Reporte]:
    """Update a report"""
    db_reporte = get_reporte(db, reporte_id)
    if db_reporte:
        update_data = reporte_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte, field, value)
        db.commit()
        db.refresh(db_reporte)
    return db_reporte


def delete_reporte(db: Session, reporte_id: UUID) -> bool:
    """Delete a report"""
    db_reporte = get_reporte(db, reporte_id)
    if db_reporte:
        db.delete(db_reporte)
        db.commit()
        return True
    return False


# ============================================================================
# REPORTES ESPECÍFICOS DE RH CRUD
# ============================================================================

def create_reporte_rh(db: Session, reporte_rh_data: ReporteRHCreate) -> ReporteRH:
    """Create a new HR report"""
    db_reporte_rh = ReporteRH(**reporte_rh_data.model_dump())
    db.add(db_reporte_rh)
    db.commit()
    db.refresh(db_reporte_rh)
    return db_reporte_rh


def get_reporte_rh(db: Session, reporte_rh_id: UUID) -> Optional[ReporteRH]:
    """Get an HR report by ID"""
    return db.query(ReporteRH).filter(ReporteRH.id == reporte_rh_id).first()


def get_reportes_rh_by_reporte(db: Session, reporte_id: UUID) -> List[ReporteRH]:
    """Get all HR reports for a specific report"""
    return db.query(ReporteRH).filter(ReporteRH.reporte_id == reporte_id).all()


def update_reporte_rh(
    db: Session, 
    reporte_rh_id: UUID, 
    reporte_rh_data: ReporteRHUpdate
) -> Optional[ReporteRH]:
    """Update an HR report"""
    db_reporte_rh = get_reporte_rh(db, reporte_rh_id)
    if db_reporte_rh:
        update_data = reporte_rh_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte_rh, field, value)
        db.commit()
        db.refresh(db_reporte_rh)
    return db_reporte_rh


def delete_reporte_rh(db: Session, reporte_rh_id: UUID) -> bool:
    """Delete an HR report"""
    db_reporte_rh = get_reporte_rh(db, reporte_rh_id)
    if db_reporte_rh:
        db.delete(db_reporte_rh)
        db.commit()
        return True
    return False


# ============================================================================
# REPORTES ESPECÍFICOS DE PRODUCCIÓN CRUD
# ============================================================================

def create_reporte_produccion(db: Session, reporte_prod_data: ReporteProduccionCreate) -> ReporteProduccion:
    """Create a new production report"""
    db_reporte_prod = ReporteProduccion(**reporte_prod_data.model_dump())
    db.add(db_reporte_prod)
    db.commit()
    db.refresh(db_reporte_prod)
    return db_reporte_prod


def get_reporte_produccion(db: Session, reporte_prod_id: UUID) -> Optional[ReporteProduccion]:
    """Get a production report by ID"""
    return db.query(ReporteProduccion).filter(ReporteProduccion.id == reporte_prod_id).first()


def get_reportes_produccion_by_reporte(db: Session, reporte_id: UUID) -> List[ReporteProduccion]:
    """Get all production reports for a specific report"""
    return db.query(ReporteProduccion).filter(ReporteProduccion.reporte_id == reporte_id).all()


def update_reporte_produccion(
    db: Session, 
    reporte_prod_id: UUID, 
    reporte_prod_data: ReporteProduccionUpdate
) -> Optional[ReporteProduccion]:
    """Update a production report"""
    db_reporte_prod = get_reporte_produccion(db, reporte_prod_id)
    if db_reporte_prod:
        update_data = reporte_prod_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte_prod, field, value)
        db.commit()
        db.refresh(db_reporte_prod)
    return db_reporte_prod


def delete_reporte_produccion(db: Session, reporte_prod_id: UUID) -> bool:
    """Delete a production report"""
    db_reporte_prod = get_reporte_produccion(db, reporte_prod_id)
    if db_reporte_prod:
        db.delete(db_reporte_prod)
        db.commit()
        return True
    return False


# ============================================================================
# REPORTES ESPECÍFICOS DE VENTAS CRUD
# ============================================================================

def create_reporte_ventas(db: Session, reporte_venta_data: ReporteVentasCreate) -> ReporteVentas:
    """Create a new sales report"""
    db_reporte_venta = ReporteVentas(**reporte_venta_data.model_dump())
    db.add(db_reporte_venta)
    db.commit()
    db.refresh(db_reporte_venta)
    return db_reporte_venta


def get_reporte_ventas(db: Session, reporte_venta_id: UUID) -> Optional[ReporteVentas]:
    """Get a sales report by ID"""
    return db.query(ReporteVentas).filter(ReporteVentas.id == reporte_venta_id).first()


def get_reportes_ventas_by_reporte(db: Session, reporte_id: UUID) -> List[ReporteVentas]:
    """Get all sales reports for a specific report"""
    return db.query(ReporteVentas).filter(ReporteVentas.reporte_id == reporte_id).all()


def update_reporte_ventas(
    db: Session, 
    reporte_venta_id: UUID, 
    reporte_venta_data: ReporteVentasUpdate
) -> Optional[ReporteVentas]:
    """Update a sales report"""
    db_reporte_venta = get_reporte_ventas(db, reporte_venta_id)
    if db_reporte_venta:
        update_data = reporte_venta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte_venta, field, value)
        db.commit()
        db.refresh(db_reporte_venta)
    return db_reporte_venta


def delete_reporte_ventas(db: Session, reporte_venta_id: UUID) -> bool:
    """Delete a sales report"""
    db_reporte_venta = get_reporte_ventas(db, reporte_venta_id)
    if db_reporte_venta:
        db.delete(db_reporte_venta)
        db.commit()
        return True
    return False


# ============================================================================
# REPORTES ESPECÍFICOS DE INVENTARIO CRUD
# ============================================================================

def create_reporte_inventario(db: Session, reporte_inv_data: ReporteInventarioCreate) -> ReporteInventario:
    """Create a new inventory report"""
    db_reporte_inv = ReporteInventario(**reporte_inv_data.model_dump())
    db.add(db_reporte_inv)
    db.commit()
    db.refresh(db_reporte_inv)
    return db_reporte_inv


def get_reporte_inventario(db: Session, reporte_inv_id: UUID) -> Optional[ReporteInventario]:
    """Get an inventory report by ID"""
    return db.query(ReporteInventario).filter(ReporteInventario.id == reporte_inv_id).first()


def get_reportes_inventario_by_reporte(db: Session, reporte_id: UUID) -> List[ReporteInventario]:
    """Get all inventory reports for a specific report"""
    return db.query(ReporteInventario).filter(ReporteInventario.reporte_id == reporte_id).all()


def update_reporte_inventario(
    db: Session, 
    reporte_inv_id: UUID, 
    reporte_inv_data: ReporteInventarioUpdate
) -> Optional[ReporteInventario]:
    """Update an inventory report"""
    db_reporte_inv = get_reporte_inventario(db, reporte_inv_id)
    if db_reporte_inv:
        update_data = reporte_inv_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte_inv, field, value)
        db.commit()
        db.refresh(db_reporte_inv)
    return db_reporte_inv


def delete_reporte_inventario(db: Session, reporte_inv_id: UUID) -> bool:
    """Delete an inventory report"""
    db_reporte_inv = get_reporte_inventario(db, reporte_inv_id)
    if db_reporte_inv:
        db.delete(db_reporte_inv)
        db.commit()
        return True
    return False


# ============================================================================
# REPORTES ESPECÍFICOS DE FINANZAS CRUD
# ============================================================================

def create_reporte_finanzas(db: Session, reporte_fin_data: ReporteFinanzasCreate) -> ReporteFinanzas:
    """Create a new financial report"""
    db_reporte_fin = ReporteFinanzas(**reporte_fin_data.model_dump())
    db.add(db_reporte_fin)
    db.commit()
    db.refresh(db_reporte_fin)
    return db_reporte_fin


def get_reporte_finanzas(db: Session, reporte_fin_id: UUID) -> Optional[ReporteFinanzas]:
    """Get a financial report by ID"""
    return db.query(ReporteFinanzas).filter(ReporteFinanzas.id == reporte_fin_id).first()


def get_reportes_finanzas_by_reporte(db: Session, reporte_id: UUID) -> List[ReporteFinanzas]:
    """Get all financial reports for a specific report"""
    return db.query(ReporteFinanzas).filter(ReporteFinanzas.reporte_id == reporte_id).all()


def update_reporte_finanzas(
    db: Session, 
    reporte_fin_id: UUID, 
    reporte_fin_data: ReporteFinanzasUpdate
) -> Optional[ReporteFinanzas]:
    """Update a financial report"""
    db_reporte_fin = get_reporte_finanzas(db, reporte_fin_id)
    if db_reporte_fin:
        update_data = reporte_fin_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reporte_fin, field, value)
        db.commit()
        db.refresh(db_reporte_fin)
    return db_reporte_fin


def delete_reporte_finanzas(db: Session, reporte_fin_id: UUID) -> bool:
    """Delete a financial report"""
    db_reporte_fin = get_reporte_finanzas(db, reporte_fin_id)
    if db_reporte_fin:
        db.delete(db_reporte_fin)
        db.commit()
        return True
    return False