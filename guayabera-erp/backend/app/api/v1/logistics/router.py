"""
Logistics and Distribution API Router: Warehouse management, shipping, and order tracking
Specialized for textile manufacturing distribution
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.logistics import (
    AlmacenCreate, AlmacenUpdate, AlmacenResponse,
    UbicacionAlmacenCreate, UbicacionAlmacenUpdate, UbicacionAlmacenResponse,
    InventarioUbicacionCreate, InventarioUbicacionUpdate, InventarioUbicacionResponse,
    MovimientoInventarioCreate, MovimientoInventarioUpdate, MovimientoInventarioResponse,
    EnvioCreate, EnvioUpdate, EnvioResponse,
    DetalleEnvioCreate, DetalleEnvioUpdate, DetalleEnvioResponse,
    HistorialEnvioCreate, HistorialEnvioResponse
)
from app.crud.logistics import (
    create_almacen, get_almacen, get_almacen_by_codigo,
    get_almacenes, update_almacen, delete_almacen,
    create_ubicacion_almacen, get_ubicacion_almacen, get_ubicaciones_by_almacen,
    update_ubicacion_almacen, delete_ubicacion_almacen,
    create_inventario_ubicacion, get_inventario_ubicacion, get_inventario_by_location_and_product,
    get_inventario_by_location, update_inventario_ubicacion, delete_inventario_ubicacion,
    create_movimiento_inventario, get_movimiento_inventario, get_movimientos_by_almacen,
    get_movimientos_by_producto, update_movimiento_inventario, delete_movimiento_inventario,
    create_envio, get_envio, get_envio_by_tracking_code,
    get_envios, update_envio, delete_envio,
    create_detalle_envio, get_detalle_envio, get_detalles_by_envio,
    update_detalle_envio, delete_detalle_envio,
    create_historial_envio, get_historial_envio, get_historial_by_envio
)

router = APIRouter(prefix="/logistics", tags=["Logistics"])

# ============================================================================
# WAREHOUSE ENDPOINTS
# ============================================================================

@router.post("/warehouses/", response_model=AlmacenResponse)
def create_warehouse(almacen: AlmacenCreate, db: Session = Depends(get_db)):
    """Create a new warehouse"""
    try:
        return create_almacen(db=db, almacen_data=almacen)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/warehouses/{almacen_id}", response_model=AlmacenResponse)
def get_warehouse(almacen_id: str, db: Session = Depends(get_db)):
    """Get a warehouse by ID"""
    almacen = get_almacen(db, almacen_id)
    if not almacen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    return almacen


@router.get("/warehouses/code/{codigo}", response_model=AlmacenResponse)
def get_warehouse_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a warehouse by code"""
    almacen = get_almacen_by_codigo(db, codigo)
    if not almacen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    return almacen


@router.get("/warehouses/", response_model=List[AlmacenResponse])
def get_warehouses(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of warehouses, optionally filtered"""
    return get_almacenes(db, skip, limit, estado)


@router.put("/warehouses/{almacen_id}", response_model=AlmacenResponse)
def update_warehouse(
    almacen_id: str, 
    almacen_data: AlmacenUpdate, 
    db: Session = Depends(get_db)
):
    """Update a warehouse"""
    updated_almacen = update_almacen(
        db=db, 
        almacen_id=almacen_id, 
        almacen_data=almacen_data
    )
    if not updated_almacen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    return updated_almacen


@router.delete("/warehouses/{almacen_id}")
def delete_warehouse(almacen_id: str, db: Session = Depends(get_db)):
    """Delete a warehouse"""
    success = delete_almacen(db=db, almacen_id=almacen_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found"
        )
    return {"message": "Warehouse deleted successfully"}


# ============================================================================
# WAREHOUSE LOCATION ENDPOINTS
# ============================================================================

@router.post("/locations/", response_model=UbicacionAlmacenResponse)
def create_warehouse_location(ubicacion: UbicacionAlmacenCreate, db: Session = Depends(get_db)):
    """Create a new warehouse location"""
    try:
        return create_ubicacion_almacen(db=db, ubicacion_data=ubicacion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/locations/{ubicacion_id}", response_model=UbicacionAlmacenResponse)
def get_warehouse_location(ubicacion_id: str, db: Session = Depends(get_db)):
    """Get a warehouse location by ID"""
    ubicacion = get_ubicacion_almacen(db, ubicacion_id)
    if not ubicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse location not found"
        )
    return ubicacion


@router.get("/warehouses/{almacen_id}/locations", response_model=List[UbicacionAlmacenResponse])
def get_locations_by_warehouse(almacen_id: str, db: Session = Depends(get_db)):
    """Get all locations in a specific warehouse"""
    return get_ubicaciones_by_almacen(db, almacen_id)


@router.put("/locations/{ubicacion_id}", response_model=UbicacionAlmacenResponse)
def update_warehouse_location(
    ubicacion_id: str, 
    ubicacion_data: UbicacionAlmacenUpdate, 
    db: Session = Depends(get_db)
):
    """Update a warehouse location"""
    updated_ubicacion = update_ubicacion_almacen(
        db=db, 
        ubicacion_id=ubicacion_id, 
        ubicacion_data=ubicacion_data
    )
    if not updated_ubicacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse location not found"
        )
    return updated_ubicacion


@router.delete("/locations/{ubicacion_id}")
def delete_warehouse_location(ubicacion_id: str, db: Session = Depends(get_db)):
    """Delete a warehouse location"""
    success = delete_ubicacion_almacen(db=db, ubicacion_id=ubicacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse location not found"
        )
    return {"message": "Warehouse location deleted successfully"}


# ============================================================================
# INVENTORY BY LOCATION ENDPOINTS
# ============================================================================

@router.post("/inventory-by-location/", response_model=InventarioUbicacionResponse)
def create_inventory_location(inventario: InventarioUbicacionCreate, db: Session = Depends(get_db)):
    """Create a new inventory by location entry"""
    try:
        return create_inventario_ubicacion(db=db, inventario_data=inventario)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/inventory-by-location/{inventario_id}", response_model=InventarioUbicacionResponse)
def get_inventory_location(inventario_id: str, db: Session = Depends(get_db)):
    """Get an inventory by location entry by ID"""
    inventario = get_inventario_ubicacion(db, inventario_id)
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory by location not found"
        )
    return inventario


@router.get("/locations/{ubicacion_id}/inventory", response_model=List[InventarioUbicacionResponse])
def get_inventory_by_location(ubicacion_id: str, db: Session = Depends(get_db)):
    """Get all inventory in a specific location"""
    return get_inventario_by_location(db, ubicacion_id)


@router.get("/locations/{ubicacion_id}/products/{producto_id}", response_model=InventarioUbicacionResponse)
def get_inventory_by_location_and_product(
    ubicacion_id: str, 
    producto_id: str, 
    db: Session = Depends(get_db)
):
    """Get inventory for a specific product in a specific location"""
    inventario = get_inventario_by_location_and_product(db, ubicacion_id, producto_id)
    if not inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory for this product in this location not found"
        )
    return inventario


@router.put("/inventory-by-location/{inventario_id}", response_model=InventarioUbicacionResponse)
def update_inventory_location(
    inventario_id: str, 
    inventario_data: InventarioUbicacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update an inventory by location entry"""
    updated_inventario = update_inventario_ubicacion(
        db=db, 
        inventario_id=inventario_id, 
        inventario_data=inventario_data
    )
    if not updated_inventario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory by location not found"
        )
    return updated_inventario


@router.delete("/inventory-by-location/{inventario_id}")
def delete_inventory_location(inventario_id: str, db: Session = Depends(get_db)):
    """Delete an inventory by location entry"""
    success = delete_inventario_ubicacion(db=db, inventario_id=inventario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory by location not found"
        )
    return {"message": "Inventory by location deleted successfully"}


# ============================================================================
# INVENTORY MOVEMENT ENDPOINTS
# ============================================================================

@router.post("/movements/", response_model=MovimientoInventarioResponse)
def create_inventory_movement(movimiento: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    """Create a new inventory movement"""
    return create_movimiento_inventario(db=db, movimiento_data=movimiento)


@router.get("/movements/{movimiento_id}", response_model=MovimientoInventarioResponse)
def get_inventory_movement(movimiento_id: str, db: Session = Depends(get_db)):
    """Get an inventory movement by ID"""
    movimiento = get_movimiento_inventario(db, movimiento_id)
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory movement not found"
        )
    return movimiento


@router.get("/warehouses/{almacen_id}/movements", response_model=List[MovimientoInventarioResponse])
def get_movements_by_warehouse(
    almacen_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all movements for a specific warehouse"""
    return get_movimientos_by_almacen(db, almacen_id, skip, limit)


@router.get("/products/{producto_id}/movements", response_model=List[MovimientoInventarioResponse])
def get_movements_by_product(
    producto_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all movements for a specific product"""
    return get_movimientos_by_producto(db, producto_id, skip, limit)


@router.put("/movements/{movimiento_id}", response_model=MovimientoInventarioResponse)
def update_inventory_movement(
    movimiento_id: str, 
    movimiento_data: MovimientoInventarioUpdate, 
    db: Session = Depends(get_db)
):
    """Update an inventory movement"""
    updated_movimiento = update_movimiento_inventario(
        db=db, 
        movimiento_id=movimiento_id, 
        movimiento_data=movimiento_data
    )
    if not updated_movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory movement not found"
        )
    return updated_movimiento


@router.delete("/movements/{movimiento_id}")
def delete_inventory_movement(movimiento_id: str, db: Session = Depends(get_db)):
    """Delete an inventory movement"""
    success = delete_movimiento_inventario(db=db, movimiento_id=movimiento_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory movement not found"
        )
    return {"message": "Inventory movement deleted successfully"}


# ============================================================================
# SHIPPING ENDPOINTS
# ============================================================================

@router.post("/shipments/", response_model=EnvioResponse)
def create_shipment(envio: EnvioCreate, db: Session = Depends(get_db)):
    """Create a new shipment"""
    try:
        return create_envio(db=db, envio_data=envio)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/shipments/{envio_id}", response_model=EnvioResponse)
def get_shipment(envio_id: str, db: Session = Depends(get_db)):
    """Get a shipment by ID"""
    envio = get_envio(db, envio_id)
    if not envio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return envio


@router.get("/shipments/tracking/{codigo_seguimiento}", response_model=EnvioResponse)
def get_shipment_by_tracking_code(codigo_seguimiento: str, db: Session = Depends(get_db)):
    """Get a shipment by tracking code"""
    envio = get_envio_by_tracking_code(db, codigo_seguimiento)
    if not envio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return envio


@router.get("/shipments/", response_model=List[EnvioResponse])
def get_shipments(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of shipments, optionally filtered"""
    return get_envios(db, skip, limit, estado)


@router.put("/shipments/{envio_id}", response_model=EnvioResponse)
def update_shipment(
    envio_id: str, 
    envio_data: EnvioUpdate, 
    db: Session = Depends(get_db)
):
    """Update a shipment"""
    updated_envio = update_envio(
        db=db, 
        envio_id=envio_id, 
        envio_data=envio_data
    )
    if not updated_envio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return updated_envio


@router.delete("/shipments/{envio_id}")
def delete_shipment(envio_id: str, db: Session = Depends(get_db)):
    """Delete a shipment"""
    success = delete_envio(db=db, envio_id=envio_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    return {"message": "Shipment deleted successfully"}


# ============================================================================
# SHIPPING DETAILS ENDPOINTS
# ============================================================================

@router.post("/shipment-details/", response_model=DetalleEnvioResponse)
def create_shipment_detail(detalle: DetalleEnvioCreate, db: Session = Depends(get_db)):
    """Create a new shipping detail"""
    return create_detalle_envio(db=db, detalle_data=detalle)


@router.get("/shipment-details/{detalle_id}", response_model=DetalleEnvioResponse)
def get_shipment_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Get a shipping detail by ID"""
    detalle = get_detalle_envio(db, detalle_id)
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment detail not found"
        )
    return detalle


@router.get("/shipments/{envio_id}/details", response_model=List[DetalleEnvioResponse])
def get_shipment_details(envio_id: str, db: Session = Depends(get_db)):
    """Get all details for a specific shipment"""
    return get_detalles_by_envio(db, envio_id)


@router.put("/shipment-details/{detalle_id}", response_model=DetalleEnvioResponse)
def update_shipment_detail(
    detalle_id: str, 
    detalle_data: DetalleEnvioUpdate, 
    db: Session = Depends(get_db)
):
    """Update a shipping detail"""
    updated_detalle = update_detalle_envio(
        db=db, 
        detalle_id=detalle_id, 
        detalle_data=detalle_data
    )
    if not updated_detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment detail not found"
        )
    return updated_detalle


@router.delete("/shipment-details/{detalle_id}")
def delete_shipment_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Delete a shipping detail"""
    success = delete_detalle_envio(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment detail not found"
        )
    return {"message": "Shipment detail deleted successfully"}


# ============================================================================
# SHIPPING HISTORY ENDPOINTS
# ============================================================================

@router.post("/shipping-history/", response_model=HistorialEnvioResponse)
def create_shipping_history(historial: HistorialEnvioCreate, db: Session = Depends(get_db)):
    """Create a new shipping history entry"""
    return create_historial_envio(db=db, historial_data=historial)


@router.get("/shipping-history/{historial_id}", response_model=HistorialEnvioResponse)
def get_shipping_history(historial_id: str, db: Session = Depends(get_db)):
    """Get a shipping history entry by ID"""
    historial = get_historial_envio(db, historial_id)
    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipping history entry not found"
        )
    return historial


@router.get("/shipments/{envio_id}/history", response_model=List[HistorialEnvioResponse])
def get_shipping_history_by_shipment(envio_id: str, db: Session = Depends(get_db)):
    """Get all history entries for a specific shipment"""
    return get_historial_by_envio(db, envio_id)