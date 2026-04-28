"""
Textile Production CRUD Operations
Specialized for guayabera production and textile manufacturing
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.production import (
    PatronPrenda, ComponentePatron, VariantePrenda, 
    OrdenProduccion, ProcesoProduccion, 
    ListaMateriales, MaterialLista
)
from app.schemas.production import (
    PatronPrendaCreate, PatronPrendaUpdate,
    ComponentePatronCreate, ComponentePatronUpdate,
    VariantePrendaCreate, VariantePrendaUpdate,
    OrdenProduccionCreate, OrdenProduccionUpdate,
    ProcesoProduccionCreate, ProcesoProduccionUpdate,
    ListaMaterialesCreate, ListaMaterialesUpdate,
    MaterialListaCreate, MaterialListaUpdate
)


# ============================================================================
# PATRON PRENDA CRUD
# ============================================================================

def create_patron_prenda(db: Session, patron_data: PatronPrendaCreate) -> PatronPrenda:
    """Create a new garment pattern"""
    db_patron = PatronPrenda(**patron_data.model_dump())
    db.add(db_patron)
    db.commit()
    db.refresh(db_patron)
    return db_patron


def get_patron_prenda(db: Session, patron_id: UUID) -> Optional[PatronPrenda]:
    """Get a garment pattern by ID"""
    return db.query(PatronPrenda).filter(PatronPrenda.id == patron_id).first()


def get_patron_prenda_by_codigo(db: Session, codigo: str) -> Optional[PatronPrenda]:
    """Get a garment pattern by code"""
    return db.query(PatronPrenda).filter(PatronPrenda.codigo == codigo).first()


def get_patrones_prenda(db: Session, skip: int = 0, limit: int = 100) -> List[PatronPrenda]:
    """Get list of garment patterns"""
    return db.query(PatronPrenda).offset(skip).limit(limit).all()


def update_patron_prenda(
    db: Session, 
    patron_id: UUID, 
    patron_data: PatronPrendaUpdate
) -> Optional[PatronPrenda]:
    """Update a garment pattern"""
    db_patron = get_patron_prenda(db, patron_id)
    if db_patron:
        update_data = patron_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_patron, field, value)
        db.commit()
        db.refresh(db_patron)
    return db_patron


def delete_patron_prenda(db: Session, patron_id: UUID) -> bool:
    """Delete a garment pattern"""
    db_patron = get_patron_prenda(db, patron_id)
    if db_patron:
        db.delete(db_patron)
        db.commit()
        return True
    return False


# ============================================================================
# COMPONENTE PATRON CRUD
# ============================================================================

def create_componente_patron(db: Session, componente_data: ComponentePatronCreate) -> ComponentePatron:
    """Create a new pattern component"""
    db_componente = ComponentePatron(**componente_data.model_dump())
    db.add(db_componente)
    db.commit()
    db.refresh(db_componente)
    return db_componente


def get_componente_patron(db: Session, componente_id: UUID) -> Optional[ComponentePatron]:
    """Get a pattern component by ID"""
    return db.query(ComponentePatron).filter(ComponentePatron.id == componente_id).first()


def get_componentes_patron(db: Session, patron_id: UUID) -> List[ComponentePatron]:
    """Get all components for a specific pattern"""
    return db.query(ComponentePatron).filter(ComponentePatron.patron_id == patron_id).all()


def update_componente_patron(
    db: Session, 
    componente_id: UUID, 
    componente_data: ComponentePatronUpdate
) -> Optional[ComponentePatron]:
    """Update a pattern component"""
    db_componente = get_componente_patron(db, componente_id)
    if db_componente:
        update_data = componente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_componente, field, value)
        db.commit()
        db.refresh(db_componente)
    return db_componente


def delete_componente_patron(db: Session, componente_id: UUID) -> bool:
    """Delete a pattern component"""
    db_componente = get_componente_patron(db, componente_id)
    if db_componente:
        db.delete(db_componente)
        db.commit()
        return True
    return False


# ============================================================================
# VARIANTE PRENDA CRUD
# ============================================================================

def create_variante_prenda(db: Session, variante_data: VariantePrendaCreate) -> VariantePrenda:
    """Create a new garment variant"""
    db_variante = VariantePrenda(**variante_data.model_dump())
    db.add(db_variante)
    db.commit()
    db.refresh(db_variante)
    return db_variante


def get_variante_prenda(db: Session, variante_id: UUID) -> Optional[VariantePrenda]:
    """Get a garment variant by ID"""
    return db.query(VariantePrenda).filter(VariantePrenda.id == variante_id).first()


def get_variante_prenda_by_codigo(db: Session, codigo: str) -> Optional[VariantePrenda]:
    """Get a garment variant by code"""
    return db.query(VariantePrenda).filter(VariantePrenda.codigo == codigo).first()


def get_variantes_prenda(db: Session, skip: int = 0, limit: int = 100) -> List[VariantePrenda]:
    """Get list of garment variants"""
    return db.query(VariantePrenda).offset(skip).limit(limit).all()


def update_variante_prenda(
    db: Session, 
    variante_id: UUID, 
    variante_data: VariantePrendaUpdate
) -> Optional[VariantePrenda]:
    """Update a garment variant"""
    db_variante = get_variante_prenda(db, variante_id)
    if db_variante:
        update_data = variante_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_variante, field, value)
        db.commit()
        db.refresh(db_variante)
    return db_variante


def delete_variante_prenda(db: Session, variante_id: UUID) -> bool:
    """Delete a garment variant"""
    db_variante = get_variante_prenda(db, variante_id)
    if db_variante:
        db.delete(db_variante)
        db.commit()
        return True
    return False


# ============================================================================
# ORDEN PRODUCCION CRUD
# ============================================================================

def create_orden_produccion(db: Session, orden_data: OrdenProduccionCreate) -> OrdenProduccion:
    """Create a new production order"""
    db_orden = OrdenProduccion(**orden_data.model_dump())
    db.add(db_orden)
    db.commit()
    db.refresh(db_orden)
    return db_orden


def get_orden_produccion(db: Session, orden_id: UUID) -> Optional[OrdenProduccion]:
    """Get a production order by ID"""
    return db.query(OrdenProduccion).filter(OrdenProduccion.id == orden_id).first()


def get_orden_produccion_by_folio(db: Session, folio: str) -> Optional[OrdenProduccion]:
    """Get a production order by folio"""
    return db.query(OrdenProduccion).filter(OrdenProduccion.folio == folio).first()


def get_ordenes_produccion(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None
) -> List[OrdenProduccion]:
    """Get list of production orders, optionally filtered by state"""
    query = db.query(OrdenProduccion)
    if estado:
        query = query.filter(OrdenProduccion.estado == estado)
    return query.offset(skip).limit(limit).all()


def update_orden_produccion(
    db: Session, 
    orden_id: UUID, 
    orden_data: OrdenProduccionUpdate
) -> Optional[OrdenProduccion]:
    """Update a production order"""
    db_orden = get_orden_produccion(db, orden_id)
    if db_orden:
        update_data = orden_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_orden, field, value)
        db.commit()
        db.refresh(db_orden)
    return db_orden


def delete_orden_produccion(db: Session, orden_id: UUID) -> bool:
    """Delete a production order"""
    db_orden = get_orden_produccion(db, orden_id)
    if db_orden:
        db.delete(db_orden)
        db.commit()
        return True
    return False


# ============================================================================
# PROCESO PRODUCCION CRUD
# ============================================================================

def create_proceso_produccion(db: Session, proceso_data: ProcesoProduccionCreate) -> ProcesoProduccion:
    """Create a new production process"""
    db_proceso = ProcesoProduccion(**proceso_data.model_dump())
    db.add(db_proceso)
    db.commit()
    db.refresh(db_proceso)
    return db_proceso


def get_proceso_produccion(db: Session, proceso_id: UUID) -> Optional[ProcesoProduccion]:
    """Get a production process by ID"""
    return db.query(ProcesoProduccion).filter(ProcesoProduccion.id == proceso_id).first()


def get_procesos_by_orden_produccion(
    db: Session, 
    orden_produccion_id: UUID
) -> List[ProcesoProduccion]:
    """Get all processes for a specific production order"""
    return db.query(ProcesoProduccion).filter(
        ProcesoProduccion.orden_produccion_id == orden_produccion_id
    ).order_by(ProcesoProduccion.numero_secuencia).all()


def update_proceso_produccion(
    db: Session, 
    proceso_id: UUID, 
    proceso_data: ProcesoProduccionUpdate
) -> Optional[ProcesoProduccion]:
    """Update a production process"""
    db_proceso = get_proceso_produccion(db, proceso_id)
    if db_proceso:
        update_data = proceso_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_proceso, field, value)
        db.commit()
        db.refresh(db_proceso)
    return db_proceso


def delete_proceso_produccion(db: Session, proceso_id: UUID) -> bool:
    """Delete a production process"""
    db_proceso = get_proceso_produccion(db, proceso_id)
    if db_proceso:
        db.delete(db_proceso)
        db.commit()
        return True
    return False


# ============================================================================
# LISTA MATERIALES CRUD
# ============================================================================

def create_lista_materiales(db: Session, lista_data: ListaMaterialesCreate) -> ListaMateriales:
    """Create a new bill of materials"""
    db_lista = ListaMateriales(**lista_data.model_dump())
    db.add(db_lista)
    db.commit()
    db.refresh(db_lista)
    return db_lista


def get_lista_materiales(db: Session, lista_id: UUID) -> Optional[ListaMateriales]:
    """Get a bill of materials by ID"""
    return db.query(ListaMateriales).filter(ListaMateriales.id == lista_id).first()


def get_lista_materiales_by_codigo(db: Session, codigo: str) -> Optional[ListaMateriales]:
    """Get a bill of materials by code"""
    return db.query(ListaMateriales).filter(ListaMateriales.codigo == codigo).first()


def get_listas_materiales(db: Session, skip: int = 0, limit: int = 100) -> List[ListaMateriales]:
    """Get list of bills of materials"""
    return db.query(ListaMateriales).offset(skip).limit(limit).all()


def update_lista_materiales(
    db: Session, 
    lista_id: UUID, 
    lista_data: ListaMaterialesUpdate
) -> Optional[ListaMateriales]:
    """Update a bill of materials"""
    db_lista = get_lista_materiales(db, lista_id)
    if db_lista:
        update_data = lista_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lista, field, value)
        db.commit()
        db.refresh(db_lista)
    return db_lista


def delete_lista_materiales(db: Session, lista_id: UUID) -> bool:
    """Delete a bill of materials"""
    db_lista = get_lista_materiales(db, lista_id)
    if db_lista:
        db.delete(db_lista)
        db.commit()
        return True
    return False


# ============================================================================
# MATERIAL LISTA CRUD
# ============================================================================

def create_material_lista(db: Session, material_data: MaterialListaCreate) -> MaterialLista:
    """Create a new material in bill of materials"""
    db_material = MaterialLista(**material_data.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_material_lista(db: Session, material_id: UUID) -> Optional[MaterialLista]:
    """Get a material in bill of materials by ID"""
    return db.query(MaterialLista).filter(MaterialLista.id == material_id).first()


def get_materiales_by_lista(
    db: Session, 
    lista_materiales_id: UUID
) -> List[MaterialLista]:
    """Get all materials for a specific bill of materials"""
    return db.query(MaterialLista).filter(
        MaterialLista.lista_materiales_id == lista_materiales_id
    ).all()


def update_material_lista(
    db: Session, 
    material_id: UUID, 
    material_data: MaterialListaUpdate
) -> Optional[MaterialLista]:
    """Update a material in bill of materials"""
    db_material = get_material_lista(db, material_id)
    if db_material:
        update_data = material_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_material, field, value)
        db.commit()
        db.refresh(db_material)
    return db_material


def delete_material_lista(db: Session, material_id: UUID) -> bool:
    """Delete a material in bill of materials"""
    db_material = get_material_lista(db, material_id)
    if db_material:
        db.delete(db_material)
        db.commit()
        return True
    return False