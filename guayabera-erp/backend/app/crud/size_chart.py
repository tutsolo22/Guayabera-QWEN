"""
Size Chart CRUD Operations: Standard Mexican sizing for clothing
Including sizes for men, women, boys, girls with standard measurements
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.size_chart import TablaTalla, Talla, ReferenciaTalla
from app.schemas.size_chart import (
    TablaTallaCreate, TablaTallaUpdate,
    TallaCreate, TallaUpdate,
    ReferenciaTallaCreate, ReferenciaTallaUpdate
)


# ============================================================================
# SIZE CHART CRUD
# ============================================================================

def create_tabla_talla(db: Session, tabla_data: TablaTallaCreate) -> TablaTalla:
    """Create a new size chart"""
    db_tabla = TablaTalla(**tabla_data.model_dump())
    db.add(db_tabla)
    db.commit()
    db.refresh(db_tabla)
    return db_tabla


def get_tabla_talla(db: Session, tabla_id: UUID) -> Optional[TablaTalla]:
    """Get a size chart by ID"""
    return db.query(TablaTalla).filter(TablaTalla.id == tabla_id).first()


def get_tabla_talla_by_codigo(db: Session, codigo: str) -> Optional[TablaTalla]:
    """Get a size chart by code"""
    return db.query(TablaTalla).filter(TablaTalla.codigo == codigo).first()


def get_tablas_talla(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    activa: Optional[bool] = None,
    tipo_prenda: Optional[str] = None,
    genero: Optional[str] = None
) -> List[TablaTalla]:
    """Get list of size charts, optionally filtered"""
    query = db.query(TablaTalla)
    
    if activa is not None:
        query = query.filter(TablaTalla.activa == activa)
    if tipo_prenda:
        query = query.filter(TablaTalla.tipo_prenda == tipo_prenda)
    if genero:
        query = query.filter(TablaTalla.genero == genero)
    
    return query.offset(skip).limit(limit).all()


def update_tabla_talla(
    db: Session, 
    tabla_id: UUID, 
    tabla_data: TablaTallaUpdate
) -> Optional[TablaTalla]:
    """Update a size chart"""
    db_tabla = get_tabla_talla(db, tabla_id)
    if db_tabla:
        update_data = tabla_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tabla, field, value)
        db.commit()
        db.refresh(db_tabla)
    return db_tabla


def delete_tabla_talla(db: Session, tabla_id: UUID) -> bool:
    """Delete a size chart"""
    db_tabla = get_tabla_talla(db, tabla_id)
    if db_tabla:
        db.delete(db_tabla)
        db.commit()
        return True
    return False


# ============================================================================
# SIZE CRUD
# ============================================================================

def create_talla(db: Session, talla_data: TallaCreate) -> Talla:
    """Create a new size"""
    db_talla = Talla(**talla_data.model_dump())
    db.add(db_talla)
    db.commit()
    db.refresh(db_talla)
    return db_talla


def get_talla(db: Session, talla_id: UUID) -> Optional[Talla]:
    """Get a size by ID"""
    return db.query(Talla).filter(Talla.id == talla_id).first()


def get_tallas_by_tabla_talla(db: Session, tabla_talla_id: UUID) -> List[Talla]:
    """Get all sizes for a specific size chart"""
    return db.query(Talla).filter(Talla.tabla_talla_id == tabla_talla_id).order_by(Talla.posicion_orden).all()


def get_talla_by_codigo(db: Session, tabla_talla_id: UUID, codigo: str) -> Optional[Talla]:
    """Get a size by code within a specific chart"""
    return db.query(Talla).filter(
        Talla.tabla_talla_id == tabla_talla_id,
        Talla.codigo == codigo
    ).first()


def update_talla(
    db: Session, 
    talla_id: UUID, 
    talla_data: TallaUpdate
) -> Optional[Talla]:
    """Update a size"""
    db_talla = get_talla(db, talla_id)
    if db_talla:
        update_data = talla_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_talla, field, value)
        db.commit()
        db.refresh(db_talla)
    return db_talla


def delete_talla(db: Session, talla_id: UUID) -> bool:
    """Delete a size"""
    db_talla = get_talla(db, talla_id)
    if db_talla:
        db.delete(db_talla)
        db.commit()
        return True
    return False


# ============================================================================
# SIZE REFERENCE CRUD
# ============================================================================

def create_referencia_talla(db: Session, referencia_data: ReferenciaTallaCreate) -> ReferenciaTalla:
    """Create a new size reference"""
    db_referencia = ReferenciaTalla(**referencia_data.model_dump())
    db.add(db_referencia)
    db.commit()
    db.refresh(db_referencia)
    return db_referencia


def get_referencia_talla(db: Session, referencia_id: UUID) -> Optional[ReferenciaTalla]:
    """Get a size reference by ID"""
    return db.query(ReferenciaTalla).filter(ReferenciaTalla.id == referencia_id).first()


def get_referencias_by_talla(db: Session, talla_id: UUID) -> List[ReferenciaTalla]:
    """Get all references for a specific size"""
    return db.query(ReferenciaTalla).filter(ReferenciaTalla.talla_id == talla_id).all()


def update_referencia_talla(
    db: Session, 
    referencia_id: UUID, 
    referencia_data: ReferenciaTallaUpdate
) -> Optional[ReferenciaTalla]:
    """Update a size reference"""
    db_referencia = get_referencia_talla(db, referencia_id)
    if db_referencia:
        update_data = referencia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_referencia, field, value)
        db.commit()
        db.refresh(db_referencia)
    return db_referencia


def delete_referencia_talla(db: Session, referencia_id: UUID) -> bool:
    """Delete a size reference"""
    db_referencia = get_referencia_talla(db, referencia_id)
    if db_referencia:
        db.delete(db_referencia)
        db.commit()
        return True
    return False