"""
Logistics and Distribution CRUD Operations: Warehouse management, shipping, and order tracking
Specialized for textile manufacturing distribution
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.logistics import (
    Almacen, UbicacionAlmacen, InventarioUbicacion,
    MovimientoInventario, Envio, DetalleEnvio, HistorialEnvio
)
from app.schemas.logistics import (
    AlmacenCreate, AlmacenUpdate,
    UbicacionAlmacenCreate, UbicacionAlmacenUpdate,
    InventarioUbicacionCreate, InventarioUbicacionUpdate,
    MovimientoInventarioCreate, MovimientoInventarioUpdate,
    EnvioCreate, EnvioUpdate,
    DetalleEnvioCreate, DetalleEnvioUpdate,
    HistorialEnvioCreate
)


# ============================================================================
# WAREHOUSE CRUD
# ============================================================================

def create_almacen(db: Session, almacen_data: AlmacenCreate) -> Almacen:
    """Create a new warehouse"""
    # Check if code already exists
    existing_almacen = db.query(Almacen).filter(Almacen.codigo == almacen_data.codigo).first()
    if existing_almacen:
        raise ValueError(f"A warehouse with code {almacen_data.codigo} already exists")
    
    db_almacen = Almacen(**almacen_data.model_dump())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


def get_almacen(db: Session, almacen_id: UUID) -> Optional[Almacen]:
    """Get a warehouse by ID"""
    return db.query(Almacen).filter(Almacen.id == almacen_id).first()


def get_almacen_by_codigo(db: Session, codigo: str) -> Optional[Almacen]:
    """Get a warehouse by code"""
    return db.query(Almacen).filter(Almacen.codigo == codigo).first()


def get_almacenes(db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[Almacen]:
    """Get list of warehouses, optionally filtered"""
    query = db.query(Almacen)
    
    if estado:
        query = query.filter(Almacen.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def update_almacen(db: Session, almacen_id: UUID, almacen_data: AlmacenUpdate) -> Optional[Almacen]:
    """Update a warehouse"""
    db_almacen = get_almacen(db, almacen_id)
    if db_almacen:
        update_data = almacen_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_almacen, field, value)
        db.commit()
        db.refresh(db_almacen)
    return db_almacen


def delete_almacen(db: Session, almacen_id: UUID) -> bool:
    """Delete a warehouse"""
    db_almacen = get_almacen(db, almacen_id)
    if db_almacen:
        db.delete(db_almacen)
        db.commit()
        return True
    return False


# ============================================================================
# WAREHOUSE LOCATION CRUD
# ============================================================================

def create_ubicacion_almacen(db: Session, ubicacion_data: UbicacionAlmacenCreate) -> UbicacionAlmacen:
    """Create a new warehouse location"""
    # Check if code already exists in this warehouse
    existing_ubicacion = db.query(UbicacionAlmacen).filter(
        and_(
            UbicacionAlmacen.codigo == ubicacion_data.codigo,
            UbicacionAlmacen.almacen_id == ubicacion_data.almacen_id
        )
    ).first()
    if existing_ubicacion:
        raise ValueError(f"A location with code {ubicacion_data.codigo} already exists in this warehouse")
    
    db_ubicacion = UbicacionAlmacen(**ubicacion_data.model_dump())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion


def get_ubicacion_almacen(db: Session, ubicacion_id: UUID) -> Optional[UbicacionAlmacen]:
    """Get a warehouse location by ID"""
    return db.query(UbicacionAlmacen).filter(UbicacionAlmacen.id == ubicacion_id).first()


def get_ubicaciones_by_almacen(db: Session, almacen_id: UUID) -> List[UbicacionAlmacen]:
    """Get all locations in a specific warehouse"""
    return db.query(UbicacionAlmacen).filter(UbicacionAlmacen.almacen_id == almacen_id).all()


def update_ubicacion_almacen(db: Session, ubicacion_id: UUID, ubicacion_data: UbicacionAlmacenUpdate) -> Optional[UbicacionAlmacen]:
    """Update a warehouse location"""
    db_ubicacion = get_ubicacion_almacen(db, ubicacion_id)
    if db_ubicacion:
        update_data = ubicacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ubicacion, field, value)
        db.commit()
        db.refresh(db_ubicacion)
    return db_ubicacion


def delete_ubicacion_almacen(db: Session, ubicacion_id: UUID) -> bool:
    """Delete a warehouse location"""
    db_ubicacion = get_ubicacion_almacen(db, ubicacion_id)
    if db_ubicacion:
        db.delete(db_ubicacion)
        db.commit()
        return True
    return False


# ============================================================================
# INVENTORY BY LOCATION CRUD
# ============================================================================

def create_inventario_ubicacion(db: Session, inventario_data: InventarioUbicacionCreate) -> InventarioUbicacion:
    """Create a new inventory by location entry"""
    # Check if inventory already exists for this product in this location
    existing_inventario = db.query(InventarioUbicacion).filter(
        and_(
            InventarioUbicacion.producto_id == inventario_data.producto_id,
            InventarioUbicacion.ubicacion_id == inventario_data.ubicacion_id
        )
    ).first()
    if existing_inventario:
        raise ValueError(f"Inventory for this product already exists in this location")
    
    db_inventario = InventarioUbicacion(**inventario_data.model_dump())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario


def get_inventario_ubicacion(db: Session, inventario_id: UUID) -> Optional[InventarioUbicacion]:
    """Get an inventory by location entry by ID"""
    return db.query(InventarioUbicacion).filter(InventarioUbicacion.id == inventario_id).first()


def get_inventario_by_location_and_product(db: Session, ubicacion_id: UUID, producto_id: UUID) -> Optional[InventarioUbicacion]:
    """Get inventory for a specific product in a specific location"""
    return db.query(InventarioUbicacion).filter(
        and_(
            InventarioUbicacion.ubicacion_id == ubicacion_id,
            InventarioUbicacion.producto_id == producto_id
        )
    ).first()


def get_inventario_by_location(db: Session, ubicacion_id: UUID) -> List[InventarioUbicacion]:
    """Get all inventory in a specific location"""
    return db.query(InventarioUbicacion).filter(InventarioUbicacion.ubicacion_id == ubicacion_id).all()


def update_inventario_ubicacion(db: Session, inventario_id: UUID, inventario_data: InventarioUbicacionUpdate) -> Optional[InventarioUbicacion]:
    """Update an inventory by location entry"""
    db_inventario = get_inventario_ubicacion(db, inventario_id)
    if db_inventario:
        update_data = inventario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inventario, field, value)
        db.commit()
        db.refresh(db_inventario)
    return db_inventario


def delete_inventario_ubicacion(db: Session, inventario_id: UUID) -> bool:
    """Delete an inventory by location entry"""
    db_inventario = get_inventario_ubicacion(db, inventario_id)
    if db_inventario:
        db.delete(db_inventario)
        db.commit()
        return True
    return False


# ============================================================================
# INVENTORY MOVEMENT CRUD
# ============================================================================

def create_movimiento_inventario(db: Session, movimiento_data: MovimientoInventarioCreate) -> MovimientoInventario:
    """Create a new inventory movement"""
    db_movimiento = MovimientoInventario(**movimiento_data.model_dump())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    
    # Update inventory based on movement type
    update_inventory_after_movement(db, db_movimiento)
    
    return db_movimiento


def get_movimiento_inventario(db: Session, movimiento_id: UUID) -> Optional[MovimientoInventario]:
    """Get an inventory movement by ID"""
    return db.query(MovimientoInventario).filter(MovimientoInventario.id == movimiento_id).first()


def get_movimientos_by_almacen(db: Session, almacen_id: UUID, skip: int = 0, limit: int = 100) -> List[MovimientoInventario]:
    """Get all movements for a specific warehouse"""
    return db.query(MovimientoInventario).filter(
        MovimientoInventario.almacen_id == almacen_id
    ).offset(skip).limit(limit).all()


def get_movimientos_by_producto(db: Session, producto_id: UUID, skip: int = 0, limit: int = 100) -> List[MovimientoInventario]:
    """Get all movements for a specific product"""
    return db.query(MovimientoInventario).filter(
        MovimientoInventario.producto_id == producto_id
    ).offset(skip).limit(limit).all()


def update_movimiento_inventario(db: Session, movimiento_id: UUID, movimiento_data: MovimientoInventarioUpdate) -> Optional[MovimientoInventario]:
    """Update an inventory movement"""
    db_movimiento = get_movimiento_inventario(db, movimiento_id)
    if db_movimiento:
        update_data = movimiento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_movimiento, field, value)
        db.commit()
        db.refresh(db_movimiento)
    return db_movimiento


def delete_movimiento_inventario(db: Session, movimiento_id: UUID) -> bool:
    """Delete an inventory movement"""
    db_movimiento = get_movimiento_inventario(db, movimiento_id)
    if db_movimiento:
        db.delete(db_movimiento)
        db.commit()
        return True
    return False


def update_inventory_after_movement(db: Session, movimiento: MovimientoInventario):
    """Update inventory levels after a movement is registered"""
    if movimiento.tipo_movimiento in ['entrada', 'ajuste_positivo', 'traspaso_entrada']:
        # Increase inventory
        inventario = get_inventario_by_location_and_product(db, movimiento.ubicacion_destino_id, movimiento.producto_id)
        if inventario:
            inventario.cantidad_disponible += movimiento.cantidad
            db.commit()
            db.refresh(inventario)
    elif movimiento.tipo_movimiento in ['salida', 'ajuste_negativo', 'traspaso_salida']:
        # Decrease inventory
        inventario = get_inventario_by_location_and_product(db, movimiento.ubicacion_origen_id, movimiento.producto_id)
        if inventario:
            inventario.cantidad_disponible -= movimiento.cantidad
            db.commit()
            db.refresh(inventario)


# ============================================================================
# SHIPPING CRUD
# ============================================================================

def create_envio(db: Session, envio_data: EnvioCreate) -> Envio:
    """Create a new shipment"""
    # Check if tracking code already exists
    existing_envio = db.query(Envio).filter(
        or_(
            Envio.numero_guia == envio_data.numero_guia,
            Envio.codigo_seguimiento == envio_data.codigo_seguimiento
        )
    ).first()
    if existing_envio:
        raise ValueError(f"A shipment with this tracking number or code already exists")
    
    db_envio = Envio(**envio_data.model_dump())
    db.add(db_envio)
    db.commit()
    db.refresh(db_envio)
    return db_envio


def get_envio(db: Session, envio_id: UUID) -> Optional[Envio]:
    """Get a shipment by ID"""
    return db.query(Envio).filter(Envio.id == envio_id).first()


def get_envio_by_tracking_code(db: Session, codigo_seguimiento: str) -> Optional[Envio]:
    """Get a shipment by tracking code"""
    return db.query(Envio).filter(Envio.codigo_seguimiento == codigo_seguimiento).first()


def get_envios(db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[Envio]:
    """Get list of shipments, optionally filtered"""
    query = db.query(Envio)
    
    if estado:
        query = query.filter(Envio.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def update_envio(db: Session, envio_id: UUID, envio_data: EnvioUpdate) -> Optional[Envio]:
    """Update a shipment"""
    db_envio = get_envio(db, envio_id)
    if db_envio:
        update_data = envio_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_envio, field, value)
        db.commit()
        db.refresh(db_envio)
    return db_envio


def delete_envio(db: Session, envio_id: UUID) -> bool:
    """Delete a shipment"""
    db_envio = get_envio(db, envio_id)
    if db_envio:
        db.delete(db_envio)
        db.commit()
        return True
    return False


# ============================================================================
# SHIPPING DETAILS CRUD
# ============================================================================

def create_detalle_envio(db: Session, detalle_data: DetalleEnvioCreate) -> DetalleEnvio:
    """Create a new shipping detail"""
    db_detalle = DetalleEnvio(**detalle_data.model_dump())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def get_detalle_envio(db: Session, detalle_id: UUID) -> Optional[DetalleEnvio]:
    """Get a shipping detail by ID"""
    return db.query(DetalleEnvio).filter(DetalleEnvio.id == detalle_id).first()


def get_detalles_by_envio(db: Session, envio_id: UUID) -> List[DetalleEnvio]:
    """Get all details for a specific shipment"""
    return db.query(DetalleEnvio).filter(DetalleEnvio.envio_id == envio_id).all()


def update_detalle_envio(db: Session, detalle_id: UUID, detalle_data: DetalleEnvioUpdate) -> Optional[DetalleEnvio]:
    """Update a shipping detail"""
    db_detalle = get_detalle_envio(db, detalle_id)
    if db_detalle:
        update_data = detalle_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_envio(db: Session, detalle_id: UUID) -> bool:
    """Delete a shipping detail"""
    db_detalle = get_detalle_envio(db, detalle_id)
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
        return True
    return False


# ============================================================================
# SHIPPING HISTORY CRUD
# ============================================================================

def create_historial_envio(db: Session, historial_data: HistorialEnvioCreate) -> HistorialEnvio:
    """Create a new shipping history entry"""
    db_historial = HistorialEnvio(**historial_data.model_dump())
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


def get_historial_envio(db: Session, historial_id: UUID) -> Optional[HistorialEnvio]:
    """Get a shipping history entry by ID"""
    return db.query(HistorialEnvio).filter(HistorialEnvio.id == historial_id).first()


def get_historial_by_envio(db: Session, envio_id: UUID) -> List[HistorialEnvio]:
    """Get all history entries for a specific shipment"""
    return db.query(HistorialEnvio).filter(HistorialEnvio.envio_id == envio_id).order_by(HistorialEnvio.fecha_cambio).all()