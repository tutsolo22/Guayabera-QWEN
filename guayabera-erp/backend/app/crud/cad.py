"""
CAD Integration CRUD Operations: Designs, patterns, and technical sheets
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.cad import (
    Diseno, DisenoTalla, ComponenteDiseno, 
    FichaTecnica, HistoricoDiseno
)
from app.schemas.cad import (
    DisenoCreate, DisenoUpdate,
    DisenoTallaCreate, DisenoTallaUpdate,
    ComponenteDisenoCreate, ComponenteDisenoUpdate,
    FichaTecnicaCreate, FichaTecnicaUpdate,
    HistoricoDisenoCreate, HistoricoDisenoUpdate
)


# ============================================================================
# DESIGN CRUD
# ============================================================================

def create_diseno(db: Session, diseno_data: DisenoCreate) -> Diseno:
    """Create a new design"""
    db_diseno = Diseno(**diseno_data.model_dump())
    db.add(db_diseno)
    db.commit()
    db.refresh(db_diseno)
    return db_diseno


def get_diseno(db: Session, diseno_id: UUID) -> Optional[Diseno]:
    """Get a design by ID"""
    return db.query(Diseno).filter(Diseno.id == diseno_id).first()


def get_diseno_by_codigo(db: Session, codigo: str) -> Optional[Diseno]:
    """Get a design by code"""
    return db.query(Diseno).filter(Diseno.codigo == codigo).first()


def get_diseños(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None, tipo_diseno: Optional[str] = None) -> List[Diseno]:
    """Get list of designs, optionally filtered"""
    query = db.query(Diseno)
    
    if activo is not None:
        query = query.filter(Diseno.activo == activo)
    if tipo_diseno:
        query = query.filter(Diseno.tipo_diseno == tipo_diseno)
    
    return query.offset(skip).limit(limit).all()


def update_diseno(db: Session, diseno_id: UUID, diseno_data: DisenoUpdate) -> Optional[Diseno]:
    """Update a design"""
    db_diseno = get_diseno(db, diseno_id)
    if db_diseno:
        update_data = diseno_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_diseno, field, value)
        db.commit()
        db.refresh(db_diseno)
    return db_diseno


def delete_diseno(db: Session, diseno_id: UUID) -> bool:
    """Delete a design"""
    db_diseno = get_diseno(db, diseno_id)
    if db_diseno:
        db.delete(db_diseno)
        db.commit()
        return True
    return False


# ============================================================================
# DESIGN SIZE CRUD
# ============================================================================

def create_diseno_talla(db: Session, diseno_talla_data: DisenoTallaCreate) -> DisenoTalla:
    """Create a new design size specification"""
    db_diseno_talla = DisenoTalla(**diseno_talla_data.model_dump())
    db.add(db_diseno_talla)
    db.commit()
    db.refresh(db_diseno_talla)
    return db_diseno_talla


def get_diseno_talla(db: Session, diseno_talla_id: UUID) -> Optional[DisenoTalla]:
    """Get a design size specification by ID"""
    return db.query(DisenoTalla).filter(DisenoTalla.id == diseno_talla_id).first()


def get_diseños_tallas_by_diseno(db: Session, diseno_id: UUID) -> List[DisenoTalla]:
    """Get all sizes for a specific design"""
    return db.query(DisenoTalla).filter(DisenoTalla.diseno_id == diseno_id).all()


def update_diseno_talla(db: Session, diseno_talla_id: UUID, diseno_talla_data: DisenoTallaUpdate) -> Optional[DisenoTalla]:
    """Update a design size specification"""
    db_diseno_talla = get_diseno_talla(db, diseno_talla_id)
    if db_diseno_talla:
        update_data = diseno_talla_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_diseno_talla, field, value)
        db.commit()
        db.refresh(db_diseno_talla)
    return db_diseno_talla


def delete_diseno_talla(db: Session, diseno_talla_id: UUID) -> bool:
    """Delete a design size specification"""
    db_diseno_talla = get_diseno_talla(db, diseno_talla_id)
    if db_diseno_talla:
        db.delete(db_diseno_talla)
        db.commit()
        return True
    return False


# ============================================================================
# DESIGN COMPONENT CRUD
# ============================================================================

def create_componente_diseno(db: Session, componente_data: ComponenteDisenoCreate) -> ComponenteDiseno:
    """Create a new design component"""
    db_componente = ComponenteDiseno(**componente_data.model_dump())
    db.add(db_componente)
    db.commit()
    db.refresh(db_componente)
    return db_componente


def get_componente_diseno(db: Session, componente_id: UUID) -> Optional[ComponenteDiseno]:
    """Get a design component by ID"""
    return db.query(ComponenteDiseno).filter(ComponenteDiseno.id == componente_id).first()


def get_componentes_by_diseno(db: Session, diseno_id: UUID) -> List[ComponenteDiseno]:
    """Get all components for a specific design"""
    return db.query(ComponenteDiseno).filter(ComponenteDiseno.diseno_id == diseno_id).all()


def update_componente_diseno(db: Session, componente_id: UUID, componente_data: ComponenteDisenoUpdate) -> Optional[ComponenteDiseno]:
    """Update a design component"""
    db_componente = get_componente_diseno(db, componente_id)
    if db_componente:
        update_data = componente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_componente, field, value)
        db.commit()
        db.refresh(db_componente)
    return db_componente


def delete_componente_diseno(db: Session, componente_id: UUID) -> bool:
    """Delete a design component"""
    db_componente = get_componente_diseno(db, componente_id)
    if db_componente:
        db.delete(db_componente)
        db.commit()
        return True
    return False


# ============================================================================
# TECHNICAL SHEET CRUD
# ============================================================================

def create_ficha_tecnica(db: Session, ficha_data: FichaTecnicaCreate) -> FichaTecnica:
    """Create a new technical sheet"""
    # Check if code already exists
    existing_ficha = get_ficha_tecnica_by_codigo(db, ficha_data.codigo)
    if existing_ficha:
        raise ValueError(f"A technical sheet with code {ficha_data.codigo} already exists")
    
    db_ficha = FichaTecnica(**ficha_data.model_dump())
    db.add(db_ficha)
    db.commit()
    db.refresh(db_ficha)
    return db_ficha


def get_ficha_tecnica(db: Session, ficha_id: UUID) -> Optional[FichaTecnica]:
    """Get a technical sheet by ID"""
    return db.query(FichaTecnica).filter(FichaTecnica.id == ficha_id).first()


def get_ficha_tecnica_by_codigo(db: Session, codigo: str) -> Optional[FichaTecnica]:
    """Get a technical sheet by code"""
    return db.query(FichaTecnica).filter(FichaTecnica.codigo == codigo).first()


def get_fichas_tecnicas_by_diseno(db: Session, diseno_id: UUID) -> List[FichaTecnica]:
    """Get all technical sheets for a specific design"""
    return db.query(FichaTecnica).filter(FichaTecnica.diseno_id == diseno_id).all()


def update_ficha_tecnica(db: Session, ficha_id: UUID, ficha_data: FichaTecnicaUpdate) -> Optional[FichaTecnica]:
    """Update a technical sheet"""
    db_ficha = get_ficha_tecnica(db, ficha_id)
    if db_ficha:
        update_data = ficha_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ficha, field, value)
        db.commit()
        db.refresh(db_ficha)
    return db_ficha


def delete_ficha_tecnica(db: Session, ficha_id: UUID) -> bool:
    """Delete a technical sheet"""
    db_ficha = get_ficha_tecnica(db, ficha_id)
    if db_ficha:
        db.delete(db_ficha)
        db.commit()
        return True
    return False


# ============================================================================
# DESIGN HISTORY CRUD
# ============================================================================

def create_historico_diseno(db: Session, historico_data: HistoricoDisenoCreate) -> HistoricoDiseno:
    """Create a new design history entry"""
    db_historico = HistoricoDiseno(**historico_data.model_dump())
    db.add(db_historico)
    db.commit()
    db.refresh(db_historico)
    return db_historico


def get_historico_diseno(db: Session, historico_id: UUID) -> Optional[HistoricoDiseno]:
    """Get a design history entry by ID"""
    return db.query(HistoricoDiseno).filter(HistoricoDiseno.id == historico_id).first()


def get_historicos_by_diseno(db: Session, diseno_id: UUID) -> List[HistoricoDiseno]:
    """Get all history entries for a specific design"""
    return db.query(HistoricoDiseno).filter(HistoricoDiseno.diseno_id == diseno_id).all()


def update_historico_diseno(db: Session, historico_id: UUID, historico_data: HistoricoDisenoUpdate) -> Optional[HistoricoDiseno]:
    """Update a design history entry"""
    db_historico = get_historico_diseno(db, historico_id)
    if db_historico:
        update_data = historico_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_historico, field, value)
        db.commit()
        db.refresh(db_historico)
    return db_historico