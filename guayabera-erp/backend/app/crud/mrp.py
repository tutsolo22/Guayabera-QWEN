from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.mrp import (
    Receta, IngredienteReceta, OrdenProduccion, 
    ConsumoMaterial, PrevisionDemanda, ProgramaMaestroProduccion
)
from app.schemas.mrp import (
    RecetaCreate, RecetaUpdate, RecetaResponse,
    IngredienteRecetaCreate, IngredienteRecetaUpdate, IngredienteRecetaResponse,
    OrdenProduccionCreate, OrdenProduccionUpdate, OrdenProduccionResponse,
    ConsumoMaterialCreate, ConsumoMaterialUpdate, ConsumoMaterialResponse,
    PrevisionDemandaCreate, PrevisionDemandaUpdate, PrevisionDemandaResponse,
    ProgramaMaestroProduccionCreate, ProgramaMaestroProduccionUpdate, ProgramaMaestroProduccionResponse
)


def create_receta(db: Session, receta_data: RecetaCreate) -> Receta:
    """Create a new recipe"""
    db_receta = Receta(**receta_data.model_dump())
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta


def get_receta(db: Session, receta_id: UUID) -> Optional[Receta]:
    """Get a recipe by ID"""
    return db.query(Receta).filter(Receta.id == receta_id).first()


def get_recetas_activas(db: Session, skip: int = 0, limit: int = 100) -> List[Receta]:
    """Get active recipes"""
    return db.query(Receta).filter(
        Receta.activa == True
    ).order_by(Receta.created_at.desc()).offset(skip).limit(limit).all()


def update_receta(
    db: Session, 
    receta_id: UUID, 
    receta_data: RecetaUpdate
) -> Optional[Receta]:
    """Update a recipe"""
    db_receta = get_receta(db, receta_id)
    if db_receta:
        update_data = receta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_receta, field, value)
        db.commit()
        db.refresh(db_receta)
    return db_receta


def delete_receta(db: Session, receta_id: UUID) -> bool:
    """Delete a recipe (soft delete by deactivation)"""
    db_receta = get_receta(db, receta_id)
    if db_receta:
        db_receta.activa = False
        db.commit()
        return True
    return False


def create_ingrediente_receta(db: Session, ingrediente_data: IngredienteRecetaCreate) -> IngredienteReceta:
    """Create a new recipe ingredient"""
    db_ingrediente = IngredienteReceta(**ingrediente_data.model_dump())
    db.add(db_ingrediente)
    db.commit()
    db.refresh(db_ingrediente)
    return db_ingrediente


def get_ingrediente_receta(db: Session, ingrediente_id: UUID) -> Optional[IngredienteReceta]:
    """Get a recipe ingredient by ID"""
    return db.query(IngredienteReceta).filter(IngredienteReceta.id == ingrediente_id).first()


def get_ingredientes_by_receta(db: Session, receta_id: UUID, skip: int = 0, limit: int = 100) -> List[IngredienteReceta]:
    """Get ingredients by recipe ID"""
    return db.query(IngredienteReceta).filter(
        IngredienteReceta.receta_id == receta_id
    ).order_by(IngredienteReceta.secuencia).offset(skip).limit(limit).all()


def update_ingrediente_receta(
    db: Session, 
    ingrediente_id: UUID, 
    ingrediente_data: IngredienteRecetaUpdate
) -> Optional[IngredienteReceta]:
    """Update a recipe ingredient"""
    db_ingrediente = get_ingrediente_receta(db, ingrediente_id)
    if db_ingrediente:
        update_data = ingrediente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ingrediente, field, value)
        db.commit()
        db.refresh(db_ingrediente)
    return db_ingrediente


def delete_ingrediente_receta(db: Session, ingrediente_id: UUID) -> bool:
    """Delete a recipe ingredient"""
    db_ingrediente = get_ingrediente_receta(db, ingrediente_id)
    if db_ingrediente:
        db.delete(db_ingrediente)
        db.commit()
        return True
    return False


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


def get_ordenes_by_estado(db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[OrdenProduccion]:
    """Get production orders by status"""
    return db.query(OrdenProduccion).filter(
        OrdenProduccion.estado == estado
    ).order_by(OrdenProduccion.fecha_inicio).offset(skip).limit(limit).all()


def get_ordenes_by_producto(db: Session, producto_id: UUID, skip: int = 0, limit: int = 100) -> List[OrdenProduccion]:
    """Get production orders by product"""
    return db.query(OrdenProduccion).filter(
        OrdenProduccion.producto_id == producto_id
    ).order_by(OrdenProduccion.fecha_inicio).offset(skip).limit(limit).all()


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
    """Delete a production order (soft delete by changing status to cancelled)"""
    db_orden = get_orden_produccion(db, orden_id)
    if db_orden:
        db_orden.estado = 'cancelada'
        db.commit()
        return True
    return False


def create_consumo_material(db: Session, consumo_data: ConsumoMaterialCreate) -> ConsumoMaterial:
    """Create a new material consumption record"""
    db_consumo = ConsumoMaterial(**consumo_data.model_dump())
    db.add(db_consumo)
    db.commit()
    db.refresh(db_consumo)
    return db_consumo


def get_consumo_material(db: Session, consumo_id: UUID) -> Optional[ConsumoMaterial]:
    """Get a material consumption record by ID"""
    return db.query(ConsumoMaterial).filter(ConsumoMaterial.id == consumo_id).first()


def get_consumos_by_orden(db: Session, orden_id: UUID, skip: int = 0, limit: int = 100) -> List[ConsumoMaterial]:
    """Get material consumption records by production order"""
    return db.query(ConsumoMaterial).filter(
        ConsumoMaterial.orden_produccion_id == orden_id
    ).order_by(ConsumoMaterial.created_at).offset(skip).limit(limit).all()


def update_consumo_material(
    db: Session, 
    consumo_id: UUID, 
    consumo_data: ConsumoMaterialUpdate
) -> Optional[ConsumoMaterial]:
    """Update a material consumption record"""
    db_consumo = get_consumo_material(db, consumo_id)
    if db_consumo:
        update_data = consumo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_consumo, field, value)
        db.commit()
        db.refresh(db_consumo)
    return db_consumo


def create_prevision_demanda(db: Session, prevision_data: PrevisionDemandaCreate) -> PrevisionDemanda:
    """Create a new demand forecast"""
    db_prevision = PrevisionDemanda(**prevision_data.model_dump())
    db.add(db_prevision)
    db.commit()
    db.refresh(db_prevision)
    return db_prevision


def get_prevision_demanda(db: Session, prevision_id: UUID) -> Optional[PrevisionDemanda]:
    """Get a demand forecast by ID"""
    return db.query(PrevisionDemanda).filter(PrevisionDemanda.id == prevision_id).first()


def get_previsiones_by_producto(db: Session, producto_id: UUID, skip: int = 0, limit: int = 100) -> List[PrevisionDemanda]:
    """Get demand forecasts by product"""
    return db.query(PrevisionDemanda).filter(
        PrevisionDemanda.producto_id == producto_id
    ).order_by(PrevisionDemanda.periodo_inicio).offset(skip).limit(limit).all()


def update_prevision_demanda(
    db: Session, 
    prevision_id: UUID, 
    prevision_data: PrevisionDemandaUpdate
) -> Optional[PrevisionDemanda]:
    """Update a demand forecast"""
    db_prevision = get_prevision_demanda(db, prevision_id)
    if db_prevision:
        update_data = prevision_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_prevision, field, value)
        db.commit()
        db.refresh(db_prevision)
    return db_prevision


def create_programa_maestro_produccion(db: Session, programa_data: ProgramaMaestroProduccionCreate) -> ProgramaMaestroProduccion:
    """Create a new master production schedule"""
    db_programa = ProgramaMaestroProduccion(**programa_data.model_dump())
    db.add(db_programa)
    db.commit()
    db.refresh(db_programa)
    return db_programa


def get_programa_maestro_produccion(db: Session, programa_id: UUID) -> Optional[ProgramaMaestroProduccion]:
    """Get a master production schedule by ID"""
    return db.query(ProgramaMaestroProduccion).filter(ProgramaMaestroProduccion.id == programa_id).first()


def get_programas_by_estado(db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[ProgramaMaestroProduccion]:
    """Get master production schedules by status"""
    return db.query(ProgramaMaestroProduccion).filter(
        ProgramaMaestroProduccion.estado == estado
    ).order_by(ProgramaMaestroProduccion.periodo_inicio).offset(skip).limit(limit).all()


def update_programa_maestro_produccion(
    db: Session, 
    programa_id: UUID, 
    programa_data: ProgramaMaestroProduccionUpdate
) -> Optional[ProgramaMaestroProduccion]:
    """Update a master production schedule"""
    db_programa = get_programa_maestro_produccion(db, programa_id)
    if db_programa:
        update_data = programa_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_programa, field, value)
        db.commit()
        db.refresh(db_programa)
    return db_programa