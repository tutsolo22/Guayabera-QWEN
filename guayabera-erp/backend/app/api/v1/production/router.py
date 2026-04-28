"""
Textile Production API Router
Specialized for guayabera production and textile manufacturing
"""

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.production import (
    PatronPrendaCreate, PatronPrendaUpdate, PatronPrendaResponse,
    ComponentePatronCreate, ComponentePatronUpdate, ComponentePatronResponse,
    VariantePrendaCreate, VariantePrendaUpdate, VariantePrendaResponse,
    OrdenProduccionCreate, OrdenProduccionUpdate, OrdenProduccionResponse,
    ProcesoProduccionCreate, ProcesoProduccionUpdate, ProcesoProduccionResponse,
    ListaMaterialesCreate, ListaMaterialesUpdate, ListaMaterialesResponse,
    MaterialListaCreate, MaterialListaUpdate, MaterialListaResponse
)
from app.crud.production import (
    create_patron_prenda, get_patron_prenda, get_patron_prenda_by_codigo,
    get_patrones_prenda, update_patron_prenda, delete_patron_prenda,
    create_componente_patron, get_componente_patron, get_componentes_patron,
    update_componente_patron, delete_componente_patron,
    create_variante_prenda, get_variante_prenda, get_variante_prenda_by_codigo,
    get_variantes_prenda, update_variante_prenda, delete_variante_prenda,
    create_orden_produccion, get_orden_produccion, get_orden_produccion_by_folio,
    get_ordenes_produccion, update_orden_produccion, delete_orden_produccion,
    create_proceso_produccion, get_proceso_produccion, get_procesos_by_orden_produccion,
    update_proceso_produccion, delete_proceso_produccion,
    create_lista_materiales, get_lista_materiales, get_lista_materiales_by_codigo,
    get_listas_materiales, update_lista_materiales, delete_lista_materiales,
    create_material_lista, get_material_lista, get_materiales_by_lista,
    update_material_lista, delete_material_lista
)

router = APIRouter(prefix="/production", tags=["Production"])

# ============================================================================
# PATRON PRENDA ENDPOINTS
# ============================================================================

@router.post("/patterns/", response_model=PatronPrendaResponse)
def create_pattern(patron: PatronPrendaCreate, db: Session = Depends(get_db)):
    """Create a new garment pattern"""
    # Check if code already exists
    existing_patron = get_patron_prenda_by_codigo(db, patron.codigo)
    if existing_patron:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pattern with this code already exists"
        )
    return create_patron_prenda(db=db, patron_data=patron)


@router.get("/patterns/{patron_id}", response_model=PatronPrendaResponse)
def get_pattern(patron_id: str, db: Session = Depends(get_db)):
    """Get a garment pattern by ID"""
    patron = get_patron_prenda(db, patron_id)
    if not patron:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pattern not found"
        )
    return patron


@router.get("/patterns/", response_model=List[PatronPrendaResponse])
def get_patterns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of garment patterns"""
    return get_patrones_prenda(db, skip=skip, limit=limit)


@router.put("/patterns/{patron_id}", response_model=PatronPrendaResponse)
def update_pattern(
    patron_id: str, 
    patron_data: PatronPrendaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a garment pattern"""
    updated_patron = update_patron_prenda(
        db=db, 
        patron_id=patron_id, 
        patron_data=patron_data
    )
    if not updated_patron:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pattern not found"
        )
    return updated_patron


@router.delete("/patterns/{patron_id}")
def delete_pattern(patron_id: str, db: Session = Depends(get_db)):
    """Delete a garment pattern"""
    success = delete_patron_prenda(db=db, patron_id=patron_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pattern not found"
        )
    return {"message": "Pattern deleted successfully"}


# ============================================================================
# COMPONENTE PATRON ENDPOINTS
# ============================================================================

@router.post("/pattern-components/", response_model=ComponentePatronResponse)
def create_pattern_component(componente: ComponentePatronCreate, db: Session = Depends(get_db)):
    """Create a new pattern component"""
    return create_componente_patron(db=db, componente_data=componente)


@router.get("/pattern-components/{componente_id}", response_model=ComponentePatronResponse)
def get_pattern_component(componente_id: str, db: Session = Depends(get_db)):
    """Get a pattern component by ID"""
    componente = get_componente_patron(db, componente_id)
    if not componente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found"
        )
    return componente


@router.get("/patterns/{patron_id}/components", response_model=List[ComponentePatronResponse])
def get_pattern_components(patron_id: str, db: Session = Depends(get_db)):
    """Get all components for a specific pattern"""
    return get_componentes_patron(db, patron_id)


@router.put("/pattern-components/{componente_id}", response_model=ComponentePatronResponse)
def update_pattern_component(
    componente_id: str, 
    componente_data: ComponentePatronUpdate, 
    db: Session = Depends(get_db)
):
    """Update a pattern component"""
    updated_componente = update_componente_patron(
        db=db, 
        componente_id=componente_id, 
        componente_data=componente_data
    )
    if not updated_componente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found"
        )
    return updated_componente


@router.delete("/pattern-components/{componente_id}")
def delete_pattern_component(componente_id: str, db: Session = Depends(get_db)):
    """Delete a pattern component"""
    success = delete_componente_patron(db=db, componente_id=componente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Component not found"
        )
    return {"message": "Component deleted successfully"}


# ============================================================================
# VARIANTE PRENDA ENDPOINTS
# ============================================================================

@router.post("/garment-variants/", response_model=VariantePrendaResponse)
def create_garment_variant(variante: VariantePrendaCreate, db: Session = Depends(get_db)):
    """Create a new garment variant"""
    # Check if code already exists
    existing_variante = get_variante_prenda_by_codigo(db, variante.codigo)
    if existing_variante:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Variant with this code already exists"
        )
    return create_variante_prenda(db=db, variante_data=variante)


@router.get("/garment-variants/{variante_id}", response_model=VariantePrendaResponse)
def get_garment_variant(variante_id: str, db: Session = Depends(get_db)):
    """Get a garment variant by ID"""
    variante = get_variante_prenda(db, variante_id)
    if not variante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found"
        )
    return variante


@router.get("/garment-variants/", response_model=List[VariantePrendaResponse])
def get_garment_variants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of garment variants"""
    return get_variantes_prenda(db, skip=skip, limit=limit)


@router.put("/garment-variants/{variante_id}", response_model=VariantePrendaResponse)
def update_garment_variant(
    variante_id: str, 
    variante_data: VariantePrendaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a garment variant"""
    updated_variante = update_variante_prenda(
        db=db, 
        variante_id=variante_id, 
        variante_data=variante_data
    )
    if not updated_variante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found"
        )
    return updated_variante


@router.delete("/garment-variants/{variante_id}")
def delete_garment_variant(variante_id: str, db: Session = Depends(get_db)):
    """Delete a garment variant"""
    success = delete_variante_prenda(db=db, variante_id=variante_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Variant not found"
        )
    return {"message": "Variant deleted successfully"}


# ============================================================================
# ORDEN PRODUCCION ENDPOINTS
# ============================================================================

@router.post("/production-orders/", response_model=OrdenProduccionResponse)
def create_production_order(orden: OrdenProduccionCreate, db: Session = Depends(get_db)):
    """Create a new production order"""
    # Check if folio already exists
    existing_orden = get_orden_produccion_by_folio(db, orden.folio)
    if existing_orden:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Production order with this folio already exists"
        )
    return create_orden_produccion(db=db, orden_data=orden)


@router.get("/production-orders/{orden_id}", response_model=OrdenProduccionResponse)
def get_production_order(orden_id: str, db: Session = Depends(get_db)):
    """Get a production order by ID"""
    orden = get_orden_produccion(db, orden_id)
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found"
        )
    return orden


@router.get("/production-orders/", response_model=List[OrdenProduccionResponse])
def get_production_orders(
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of production orders, optionally filtered by state"""
    return get_ordenes_produccion(db, skip=skip, limit=limit, estado=estado)


@router.put("/production-orders/{orden_id}", response_model=OrdenProduccionResponse)
def update_production_order(
    orden_id: str, 
    orden_data: OrdenProduccionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a production order"""
    updated_orden = update_orden_produccion(
        db=db, 
        orden_id=orden_id, 
        orden_data=orden_data
    )
    if not updated_orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found"
        )
    return updated_orden


@router.delete("/production-orders/{orden_id}")
def delete_production_order(orden_id: str, db: Session = Depends(get_db)):
    """Delete a production order"""
    success = delete_orden_produccion(db=db, orden_id=orden_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Production order not found"
        )
    return {"message": "Production order deleted successfully"}


# ============================================================================
# PROCESO PRODUCCION ENDPOINTS
# ============================================================================

@router.post("/production-processes/", response_model=ProcesoProduccionResponse)
def create_production_process(proceso: ProcesoProduccionCreate, db: Session = Depends(get_db)):
    """Create a new production process"""
    return create_proceso_produccion(db=db, proceso_data=proceso)


@router.get("/production-processes/{proceso_id}", response_model=ProcesoProduccionResponse)
def get_production_process(proceso_id: str, db: Session = Depends(get_db)):
    """Get a production process by ID"""
    proceso = get_proceso_produccion(db, proceso_id)
    if not proceso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found"
        )
    return proceso


@router.get("/production-orders/{orden_id}/processes", response_model=List[ProcesoProduccionResponse])
def get_processes_by_order(orden_id: str, db: Session = Depends(get_db)):
    """Get all processes for a specific production order"""
    return get_procesos_by_orden_produccion(db, orden_id)


@router.put("/production-processes/{proceso_id}", response_model=ProcesoProduccionResponse)
def update_production_process(
    proceso_id: str, 
    proceso_data: ProcesoProduccionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a production process"""
    updated_proceso = update_proceso_produccion(
        db=db, 
        proceso_id=proceso_id, 
        proceso_data=proceso_data
    )
    if not updated_proceso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found"
        )
    return updated_proceso


@router.delete("/production-processes/{proceso_id}")
def delete_production_process(proceso_id: str, db: Session = Depends(get_db)):
    """Delete a production process"""
    success = delete_proceso_produccion(db=db, proceso_id=proceso_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Process not found"
        )
    return {"message": "Process deleted successfully"}


# ============================================================================
# LISTA MATERIALES ENDPOINTS
# ============================================================================

@router.post("/bills-of-materials/", response_model=ListaMaterialesResponse)
def create_bill_of_materials(lista: ListaMaterialesCreate, db: Session = Depends(get_db)):
    """Create a new bill of materials"""
    # Check if code already exists
    existing_lista = get_lista_materiales_by_codigo(db, lista.codigo)
    if existing_lista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bill of materials with this code already exists"
        )
    return create_lista_materiales(db=db, lista_data=lista)


@router.get("/bills-of-materials/{lista_id}", response_model=ListaMaterialesResponse)
def get_bill_of_materials(lista_id: str, db: Session = Depends(get_db)):
    """Get a bill of materials by ID"""
    lista = get_lista_materiales(db, lista_id)
    if not lista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill of materials not found"
        )
    return lista


@router.get("/bills-of-materials/", response_model=List[ListaMaterialesResponse])
def get_bills_of_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of bills of materials"""
    return get_listas_materiales(db, skip=skip, limit=limit)


@router.put("/bills-of-materials/{lista_id}", response_model=ListaMaterialesResponse)
def update_bill_of_materials(
    lista_id: str, 
    lista_data: ListaMaterialesUpdate, 
    db: Session = Depends(get_db)
):
    """Update a bill of materials"""
    updated_lista = update_lista_materiales(
        db=db, 
        lista_id=lista_id, 
        lista_data=lista_data
    )
    if not updated_lista:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill of materials not found"
        )
    return updated_lista


@router.delete("/bills-of-materials/{lista_id}")
def delete_bill_of_materials(lista_id: str, db: Session = Depends(get_db)):
    """Delete a bill of materials"""
    success = delete_lista_materiales(db=db, lista_id=lista_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bill of materials not found"
        )
    return {"message": "Bill of materials deleted successfully"}


# ============================================================================
# MATERIAL LISTA ENDPOINTS
# ============================================================================

@router.post("/materials-in-list/", response_model=MaterialListaResponse)
def create_material_in_list(material: MaterialListaCreate, db: Session = Depends(get_db)):
    """Create a new material in bill of materials"""
    return create_material_lista(db=db, material_data=material)


@router.get("/materials-in-list/{material_id}", response_model=MaterialListaResponse)
def get_material_in_list(material_id: str, db: Session = Depends(get_db)):
    """Get a material in bill of materials by ID"""
    material = get_material_lista(db, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return material


@router.get("/bills-of-materials/{lista_id}/materials", response_model=List[MaterialListaResponse])
def get_materials_by_list(lista_id: str, db: Session = Depends(get_db)):
    """Get all materials for a specific bill of materials"""
    return get_materiales_by_lista(db, lista_id)


@router.put("/materials-in-list/{material_id}", response_model=MaterialListaResponse)
def update_material_in_list(
    material_id: str, 
    material_data: MaterialListaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a material in bill of materials"""
    updated_material = update_material_lista(
        db=db, 
        material_id=material_id, 
        material_data=material_data
    )
    if not updated_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return updated_material


@router.delete("/materials-in-list/{material_id}")
def delete_material_in_list(material_id: str, db: Session = Depends(get_db)):
    """Delete a material in bill of materials"""
    success = delete_material_lista(db=db, material_id=material_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Material not found"
        )
    return {"message": "Material deleted successfully"}