from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas.mrp import (
    RecetaCreate, RecetaUpdate, RecetaResponse,
    IngredienteRecetaCreate, IngredienteRecetaUpdate, IngredienteRecetaResponse,
    OrdenProduccionCreate, OrdenProduccionUpdate, OrdenProduccionResponse,
    ConsumoMaterialCreate, ConsumoMaterialUpdate, ConsumoMaterialResponse,
    PrevisionDemandaCreate, PrevisionDemandaUpdate, PrevisionDemandaResponse,
    ProgramaMaestroProduccionCreate, ProgramaMaestroProduccionUpdate, ProgramaMaestroProduccionResponse
)
from app.crud.mrp import (
    create_receta, get_receta, get_recetas_activas, update_receta, delete_receta,
    create_ingrediente_receta, get_ingrediente_receta, get_ingredientes_by_receta,
    update_ingrediente_receta, delete_ingrediente_receta,
    create_orden_produccion, get_orden_produccion, get_ordenes_by_estado,
    get_ordenes_by_producto, update_orden_produccion, delete_orden_produccion,
    create_consumo_material, get_consumo_material, get_consumos_by_orden,
    update_consumo_material,
    create_prevision_demanda, get_prevision_demanda, get_previsiones_by_producto,
    update_prevision_demanda,
    create_programa_maestro_produccion, get_programa_maestro_produccion,
    get_programas_by_estado, update_programa_maestro_produccion
)

router = APIRouter()


# ============================================================================
# ENDPOINTS PARA RECETAS
# ============================================================================

@router.post("/recipes", response_model=RecetaResponse)
def create_recipe_endpoint(
    receta_data: RecetaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_receta(db, receta_data)


@router.get("/recipes/{receta_id}", response_model=RecetaResponse)
def get_recipe_endpoint(
    receta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    receta = get_receta(db, UUID(receta_id))
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta


@router.get("/recipes/active", response_model=List[RecetaResponse])
def get_active_recipes_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_recetas_activas(db, skip, limit)


@router.put("/recipes/{receta_id}", response_model=RecetaResponse)
def update_recipe_endpoint(
    receta_id: str,
    receta_data: RecetaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_receta = update_receta(db, UUID(receta_id), receta_data)
    if not updated_receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return updated_receta


@router.delete("/recipes/{receta_id}")
def delete_recipe_endpoint(
    receta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_receta(db, UUID(receta_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"message": "Receta eliminada exitosamente"}


# ============================================================================
# ENDPOINTS PARA INGREDIENTES DE RECETA
# ============================================================================

@router.post("/recipe-ingredients", response_model=IngredienteRecetaResponse)
def create_recipe_ingredient_endpoint(
    ingrediente_data: IngredienteRecetaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_ingrediente_receta(db, ingrediente_data)


@router.get("/recipe-ingredients/{ingrediente_id}", response_model=IngredienteRecetaResponse)
def get_recipe_ingredient_endpoint(
    ingrediente_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    ingrediente = get_ingrediente_receta(db, UUID(ingrediente_id))
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente de receta no encontrado")
    return ingrediente


@router.get("/recipe-ingredients/recipe/{receta_id}", response_model=List[IngredienteRecetaResponse])
def get_ingredients_by_recipe_endpoint(
    receta_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_ingredientes_by_receta(db, UUID(receta_id), skip, limit)


@router.put("/recipe-ingredients/{ingrediente_id}", response_model=IngredienteRecetaResponse)
def update_recipe_ingredient_endpoint(
    ingrediente_id: str,
    ingrediente_data: IngredienteRecetaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_ingrediente = update_ingrediente_receta(db, UUID(ingrediente_id), ingrediente_data)
    if not updated_ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente de receta no encontrado")
    return updated_ingrediente


@router.delete("/recipe-ingredients/{ingrediente_id}")
def delete_recipe_ingredient_endpoint(
    ingrediente_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_ingrediente_receta(db, UUID(ingrediente_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Ingrediente de receta no encontrado")
    return {"message": "Ingrediente de receta eliminado exitosamente"}


# ============================================================================
# ENDPOINTS PARA ÓRDENES DE PRODUCCIÓN
# ============================================================================

@router.post("/production-orders", response_model=OrdenProduccionResponse)
def create_production_order_endpoint(
    orden_data: OrdenProduccionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de producción pueden crear órdenes
    if not current_user.get("rol") in ["admin", "produccion", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear órdenes de producción")
    
    return create_orden_produccion(db, orden_data)


@router.get("/production-orders/{orden_id}", response_model=OrdenProduccionResponse)
def get_production_order_endpoint(
    orden_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    orden = get_orden_produccion(db, UUID(orden_id))
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    return orden


@router.get("/production-orders/status/{estado}", response_model=List[OrdenProduccionResponse])
def get_orders_by_status_endpoint(
    estado: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_ordenes_by_estado(db, estado, skip, limit)


@router.get("/production-orders/product/{producto_id}", response_model=List[OrdenProduccionResponse])
def get_orders_by_product_endpoint(
    producto_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_ordenes_by_producto(db, UUID(producto_id), skip, limit)


@router.put("/production-orders/{orden_id}", response_model=OrdenProduccionResponse)
def update_production_order_endpoint(
    orden_id: str,
    orden_data: OrdenProduccionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de producción pueden actualizar órdenes
    if not current_user.get("rol") in ["admin", "produccion", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar órdenes de producción")
    
    updated_orden = update_orden_produccion(db, UUID(orden_id), orden_data)
    if not updated_orden:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    return updated_orden


@router.delete("/production-orders/{orden_id}")
def delete_production_order_endpoint(
    orden_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de producción pueden eliminar órdenes
    if not current_user.get("rol") in ["admin", "produccion", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar órdenes de producción")
    
    deleted = delete_orden_produccion(db, UUID(orden_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Orden de producción no encontrada")
    return {"message": "Orden de producción cancelada exitosamente"}


# ============================================================================
# ENDPOINTS PARA CONSUMO DE MATERIALES
# ============================================================================

@router.post("/material-consumption", response_model=ConsumoMaterialResponse)
def create_material_consumption_endpoint(
    consumo_data: ConsumoMaterialCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_consumo_material(db, consumo_data)


@router.get("/material-consumption/{consumo_id}", response_model=ConsumoMaterialResponse)
def get_material_consumption_endpoint(
    consumo_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    consumo = get_consumo_material(db, UUID(consumo_id))
    if not consumo:
        raise HTTPException(status_code=404, detail="Consumo de material no encontrado")
    return consumo


@router.get("/material-consumption/order/{orden_id}", response_model=List[ConsumoMaterialResponse])
def get_consumptions_by_order_endpoint(
    orden_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_consumos_by_orden(db, UUID(orden_id), skip, limit)


@router.put("/material-consumption/{consumo_id}", response_model=ConsumoMaterialResponse)
def update_material_consumption_endpoint(
    consumo_id: str,
    consumo_data: ConsumoMaterialUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_consumo = update_consumo_material(db, UUID(consumo_id), consumo_data)
    if not updated_consumo:
        raise HTTPException(status_code=404, detail="Consumo de material no encontrado")
    return updated_consumo


# ============================================================================
# ENDPOINTS PARA PREVISIÓN DE DEMANDA
# ============================================================================

@router.post("/demand-forecasts", response_model=PrevisionDemandaResponse)
def create_demand_forecast_endpoint(
    prevision_data: PrevisionDemandaCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_prevision_demanda(db, prevision_data)


@router.get("/demand-forecasts/{prevision_id}", response_model=PrevisionDemandaResponse)
def get_demand_forecast_endpoint(
    prevision_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    prevision = get_prevision_demanda(db, UUID(prevision_id))
    if not prevision:
        raise HTTPException(status_code=404, detail="Previsión de demanda no encontrada")
    return prevision


@router.get("/demand-forecasts/product/{producto_id}", response_model=List[PrevisionDemandaResponse])
def get_forecasts_by_product_endpoint(
    producto_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_previsiones_by_producto(db, UUID(producto_id), skip, limit)


@router.put("/demand-forecasts/{prevision_id}", response_model=PrevisionDemandaResponse)
def update_demand_forecast_endpoint(
    prevision_id: str,
    prevision_data: PrevisionDemandaUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_prevision = update_prevision_demanda(db, UUID(prevision_id), prevision_data)
    if not updated_prevision:
        raise HTTPException(status_code=404, detail="Previsión de demanda no encontrada")
    return updated_prevision


# ============================================================================
# ENDPOINTS PARA PROGRAMA MAESTRO DE PRODUCCIÓN
# ============================================================================

@router.post("/master-production-schedules", response_model=ProgramaMaestroProduccionResponse)
def create_master_production_schedule_endpoint(
    programa_data: ProgramaMaestroProduccionCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Solo usuarios con permisos de producción o planificación pueden crear programas
    if not current_user.get("rol") in ["admin", "produccion", "planificacion", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para crear programas maestros de producción")
    
    return create_programa_maestro_produccion(db, programa_data)


@router.get("/master-production-schedules/{programa_id}", response_model=ProgramaMaestroProduccionResponse)
def get_master_production_schedule_endpoint(
    programa_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    programa = get_programa_maestro_produccion(db, UUID(programa_id))
    if not programa:
        raise HTTPException(status_code=404, detail="Programa maestro de producción no encontrado")
    return programa


@router.get("/master-production-schedules/status/{estado}", response_model=List[ProgramaMaestroProduccionResponse])
def get_schedules_by_status_endpoint(
    estado: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_programas_by_estado(db, estado, skip, limit)


@router.put("/master-production-schedules/{programa_id}", response_model=ProgramaMaestroProduccionResponse)
def update_master_production_schedule_endpoint(
    programa_id: str,
    programa_data: ProgramaMaestroProduccionUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    # Solo usuarios con permisos de producción o planificación pueden actualizar programas
    if not current_user.get("rol") in ["admin", "produccion", "planificacion", "super_admin"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar programas maestros de producción")
    
    updated_programa = update_programa_maestro_produccion(db, UUID(programa_id), programa_data)
    if not updated_programa:
        raise HTTPException(status_code=404, detail="Programa maestro de producción no encontrado")
    return updated_programa