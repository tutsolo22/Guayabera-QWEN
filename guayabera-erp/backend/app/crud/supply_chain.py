"""
CRUD operations for Supply Chain module
Purchases, Suppliers, Inventory, Warehouse
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal

from app.models.supply_chain import (
    Proveedor, ProveedorContacto,
    Producto, AlmacenCategoria, ProductoPrecio, ProductoNumeroSerie, ProductoLote,
    Almacen, Inventario, MovimientoInventario, AlmacenListaPrecios,
    OrdenCompra, OrdenCompraDetalle, RecepcionCompra, RecepcionCompraDetalle
)
from app.schemas.supply_chain import (
    ProveedorCreate, ProveedorUpdate,
    ProductoCreate, ProductoUpdate,
    AlmacenCreate, AlmacenUpdate,
    MovimientoInventarioCreate,
    OrdenCompraCreate, OrdenCompraUpdate,
    RecepcionCompraCreate
)


# ============= PROVEEDORES =============

def get_proveedor_by_id(db: Session, proveedor_id: UUID) -> Optional[Proveedor]:
    """Get supplier by ID"""
    return db.query(Proveedor).filter(
        Proveedor.id == proveedor_id,
        Proveedor.deleted_at.is_(None)
    ).first()


def get_proveedor_by_rfc(db: Session, rfc: str) -> Optional[Proveedor]:
    """Get supplier by RFC"""
    return db.query(Proveedor).filter(
        Proveedor.rfc == rfc,
        Proveedor.deleted_at.is_(None)
    ).first()


def get_proveedores(db: Session, activo: bool = True, 
                    tipo_proveedor: str = None) -> List[Proveedor]:
    """Get suppliers with optional filters"""
    query = db.query(Proveedor).filter(Proveedor.deleted_at.is_(None))
    
    if activo is not None:
        query = query.filter(Proveedor.activo == activo)
    if tipo_proveedor:
        query = query.filter(Proveedor.tipo_proveedor == tipo_proveedor)
    
    return query.order_by(Proveedor.nombre_comercial).all()


def create_proveedor(db: Session, proveedor: ProveedorCreate) -> Proveedor:
    """Create new supplier"""
    db_proveedor = Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor


def update_proveedor(db: Session, proveedor_id: UUID, 
                     proveedor: ProveedorUpdate) -> Proveedor:
    """Update supplier"""
    db_proveedor = get_proveedor_by_id(db, proveedor_id)
    if not db_proveedor:
        return None
    
    update_data = proveedor.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_proveedor, field, value)
    
    db_proveedor.updated_at = func.now()
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor


def delete_proveedor(db: Session, proveedor_id: UUID) -> bool:
    """Soft delete supplier"""
    db_proveedor = get_proveedor_by_id(db, proveedor_id)
    if not db_proveedor:
        return False
    
    db_proveedor.deleted_at = func.now()
    db_proveedor.activo = False
    db.commit()
    return True


def get_proveedor_contactos(db: Session, proveedor_id: UUID) -> List[ProveedorContacto]:
    """Get supplier contacts"""
    return db.query(ProveedorContacto).filter(
        ProveedorContacto.proveedor_id == proveedor_id
    ).order_by(ProveedorContacto.es_principal.desc()).all()


# ============= PRODUCTOS =============

def get_producto_by_id(db: Session, producto_id: UUID) -> Optional[Producto]:
    """Get product by ID"""
    return db.query(Producto).filter(
        Producto.id == producto_id,
        Producto.deleted_at.is_(None)
    ).first()


def get_producto_by_codigo(db: Session, codigo: str) -> Optional[Producto]:
    """Get product by code"""
    return db.query(Producto).filter(
        Producto.codigo == codigo,
        Producto.deleted_at.is_(None)
    ).first()


def get_productos(db: Session, activo: bool = True, 
                  categoria_id: UUID = None,
                  busqueda: str = None) -> List[Producto]:
    """Get products with optional filters"""
    query = db.query(Producto).filter(Producto.deleted_at.is_(None))
    
    if activo is not None:
        query = query.filter(Producto.activo == activo)
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    if busqueda:
        query = query.filter(
            or_(
                Producto.nombre.ilike(f"%{busqueda}%"),
                Producto.codigo.ilike(f"%{busqueda}%"),
                Producto.descripcion.ilike(f"%{busqueda}%")
            )
        )
    
    return query.order_by(Producto.nombre).all()


def create_producto(db: Session, producto: ProductoCreate) -> Producto:
    """Create new product"""
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, producto_id: UUID, 
                    producto: ProductoUpdate) -> Producto:
    """Update product"""
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return None
    
    update_data = producto.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_producto, field, value)
    
    db_producto.updated_at = func.now()
    db.commit()
    db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, producto_id: UUID) -> bool:
    """Soft delete product"""
    db_producto = get_producto_by_id(db, producto_id)
    if not db_producto:
        return False
    
    db_producto.deleted_at = func.now()
    db_producto.activo = False
    db.commit()
    return True


# ============= CATEGORÍAS =============

def get_categoria_by_id(db: Session, categoria_id: UUID) -> Optional[AlmacenCategoria]:
    """Get category by ID"""
    return db.query(AlmacenCategoria).filter(
        AlmacenCategoria.id == categoria_id
    ).first()


def get_categorias(db: Session, activa: bool = True) -> List[AlmacenCategoria]:
    """Get categories"""
    query = db.query(AlmacenCategoria)
    if activa:
        query = query.filter(AlmacenCategoria.activa == activa)
    return query.order_by(AlmacenCategoria.nombre).all()


def create_categoria(db: Session, categoria) -> AlmacenCategoria:
    """Create new category"""
    db_categoria = AlmacenCategoria(**categoria.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


# ============= ALMACENES =============

def get_almacen_by_id(db: Session, almacen_id: UUID) -> Optional[Almacen]:
    """Get warehouse by ID"""
    return db.query(Almacen).filter(
        Almacen.id == almacen_id,
        Almacen.deleted_at.is_(None)
    ).first()


def get_almacenes(db: Session, activo: bool = True) -> List[Almacen]:
    """Get warehouses"""
    query = db.query(Almacen).filter(Almacen.deleted_at.is_(None))
    if activo:
        query = query.filter(Almacen.activo == activo)
    return query.order_by(Almacen.nombre).all()


def create_almacen(db: Session, almacen: AlmacenCreate) -> Almacen:
    """Create new warehouse"""
    db_almacen = Almacen(**almacen.model_dump())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


def update_almacen(db: Session, almacen_id: UUID, 
                   almacen: AlmacenUpdate) -> Almacen:
    """Update warehouse"""
    db_almacen = get_almacen_by_id(db, almacen_id)
    if not db_almacen:
        return None
    
    update_data = almacen.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_almacen, field, value)
    
    db_almacen.updated_at = func.now()
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


# ============= INVENTARIOS =============

def get_inventario(db: Session, producto_id: UUID, 
                   almacen_id: UUID) -> Optional[Inventario]:
    """Get inventory for specific product and warehouse"""
    return db.query(Inventario).filter(
        Inventario.producto_id == producto_id,
        Inventario.almacen_id == almacen_id
    ).first()


def get_inventarios_by_almacen(db: Session, almacen_id: UUID, 
                                con_stock: bool = False) -> List[Inventario]:
    """Get all inventories for a warehouse"""
    query = db.query(Inventario).filter(Inventario.almacen_id == almacen_id)
    if con_stock:
        query = query.filter(Inventario.cantidad_disponible > 0)
    return query.all()


def get_inventarios_bajo_stock(db: Session) -> List[Inventario]:
    """Get inventories below minimum stock"""
    return db.query(Inventario).join(Producto).filter(
        Inventario.cantidad_disponible < Producto.stock_minimo
    ).all()


def create_or_update_inventario(db: Session, producto_id: UUID, 
                                 almacen_id: UUID, 
                                 cantidad: Decimal,
                                 costo_promedio: Decimal = None) -> Inventario:
    """Create or update inventory record"""
    inventario = get_inventario(db, producto_id, almacen_id)
    
    if inventario:
        inventario.cantidad_disponible = cantidad
        if costo_promedio:
            inventario.costo_promedio = costo_promedio
        inventario.updated_at = func.now()
    else:
        inventario = Inventario(
            producto_id=producto_id,
            almacen_id=almacen_id,
            cantidad_disponible=cantidad,
            costo_promedio=costo_promedio or 0
        )
        db.add(inventario)
    
    db.commit()
    db.refresh(inventario)
    return inventario


def registrar_movimiento_inventario(db: Session, 
                                     movimiento: MovimientoInventarioCreate,
                                     usuario_id: UUID = None) -> MovimientoInventario:
    """Register inventory movement and update stock"""
    # Create movement record
    db_movimiento = MovimientoInventario(
        **movimiento.model_dump(),
        usuario_id=usuario_id,
        costo_total=movimiento.cantidad * movimiento.costo_unitario
    )
    db.add(db_movimiento)
    db.flush()
    
    # Update inventory
    inventario = get_inventario(db, movimiento.producto_id, movimiento.almacen_id)
    
    if not inventario:
        inventario = Inventario(
            producto_id=movimiento.producto_id,
            almacen_id=movimiento.almacen_id,
            cantidad_disponible=0,
            costo_promedio=movimiento.costo_unitario
        )
        db.add(inventario)
        db.flush()
    
    # Update quantities based on movement type
    from app.models.supply_chain import TipoMovimientoInventario
    
    if movimiento.tipo_movimiento in [
        TipoMovimientoInventario.ENTRADA_COMPRA,
        TipoMovimientoInventario.ENTRADA_DEVOLUCION,
        TipoMovimientoInventario.AJUSTE_POSITIVO,
        TipoMovimientoInventario.PRODUCCION
    ]:
        # Calculate new average cost for entries
        valor_actual = inventario.cantidad_disponible * inventario.costo_promedio
        valor_nuevo = movimiento.cantidad * movimiento.costo_unitario
        nueva_cantidad = inventario.cantidad_disponible + movimiento.cantidad
        
        if nueva_cantidad > 0:
            inventario.costo_promedio = (valor_actual + valor_nuevo) / nueva_cantidad
        
        inventario.cantidad_disponible += movimiento.cantidad
        
    elif movimiento.tipo_movimiento in [
        TipoMovimientoInventario.SALIDA_VENTA,
        TipoMovimientoInventario.SALIDA_MERMAS,
        TipoMovimientoInventario.AJUSTE_NEGATIVO
    ]:
        inventario.cantidad_disponible -= movimiento.cantidad
    
    db_movimiento.movimiento_inventario_id = db_movimiento.id
    db.commit()
    db.refresh(db_movimiento)
    
    return db_movimiento


# ============= ÓRDENES DE COMPRA =============

def get_orden_compra_by_id(db: Session, orden_id: UUID) -> Optional[OrdenCompra]:
    """Get purchase order by ID"""
    return db.query(OrdenCompra).filter(OrdenCompra.id == orden_id).first()


def get_orden_compra_by_folio(db: Session, folio: str) -> Optional[OrdenCompra]:
    """Get purchase order by folio"""
    return db.query(OrdenCompra).filter(OrdenCompra.folio == folio).first()


def get_ordenes_compra(db: Session, proveedor_id: UUID = None,
                       estado: str = None,
                       fecha_desde: date = None,
                       fecha_hasta: date = None) -> List[OrdenCompra]:
    """Get purchase orders with filters"""
    query = db.query(OrdenCompra)
    
    if proveedor_id:
        query = query.filter(OrdenCompra.proveedor_id == proveedor_id)
    if estado:
        query = query.filter(OrdenCompra.estado == estado)
    if fecha_desde:
        query = query.filter(OrdenCompra.fecha_emision >= fecha_desde)
    if fecha_hasta:
        query = query.filter(OrdenCompra.fecha_emision <= fecha_hasta)
    
    return query.order_by(OrdenCompra.fecha_emision.desc()).all()


def generar_folio_orden_compra(db: Session, serie: str = "OC") -> str:
    """Generate next purchase order folio"""
    ultimo_folio = db.query(func.max(OrdenCompra.folio)).filter(
        OrdenCompra.serie == serie
    ).scalar()
    
    if ultimo_folio:
        try:
            numero = int(ultimo_folio.replace(f"{serie}-", "")) + 1
        except:
            numero = 1
    else:
        numero = 1
    
    return f"{serie}-{numero:06d}"


def crear_orden_compra(db: Session, orden: OrdenCompraCreate, 
                       usuario_id: UUID) -> OrdenCompra:
    """Create new purchase order"""
    folio = generar_folio_orden_compra(db)
    
    # Calculate totals
    subtotal = sum(d.cantidad_pedida * d.costo_unitario for d in orden.detalles)
    total_iva = sum(
        d.cantidad_pedida * d.costo_unitario * (d.iva_porcentaje / 100) 
        for d in orden.detalles
    )
    total = subtotal + total_iva
    
    db_orden = OrdenCompra(
        folio=folio,
        serie="OC",
        subtotal=subtotal,
        total_iva=total_iva,
        total=total,
        elaboro_id=usuario_id,
        **orden.model_dump(exclude={'detalles'})
    )
    db.add(db_orden)
    db.flush()
    
    # Create details
    for detalle in orden.detalles:
        producto = db.query(Producto).filter(
            Producto.id == detalle.producto_id
        ).first()
        
        db_detalle = OrdenCompraDetalle(
            orden_compra_id=db_orden.id,
            costo_total=detalle.cantidad_pedida * detalle.costo_unitario,
            descuento_importe=detalle.cantidad_pedida * detalle.costo_unitario * (detalle.descuento_porcentaje / 100),
            iva_importe=detalle.cantidad_pedida * detalle.costo_unitario * (detalle.iva_porcentaje / 100),
            total_renglon=(detalle.cantidad_pedida * detalle.costo_unitario) + 
                         (detalle.cantidad_pedida * detalle.costo_unitario * (detalle.iva_porcentaje / 100)) -
                         (detalle.cantidad_pedida * detalle.costo_unitario * (detalle.descuento_porcentaje / 100)),
            codigo_producto=producto.codigo if producto else None,
            nombre_producto=producto.nombre if producto else None,
            unidad_medida=producto.unidad_medida if producto else None,
            **detalle.model_dump()
        )
        db.add(db_detalle)
    
    db.commit()
    db.refresh(db_orden)
    return db_orden


def actualizar_estado_orden(db: Session, orden_id: UUID, 
                            estado) -> Optional[OrdenCompra]:
    """Update purchase order status"""
    db_orden = get_orden_compra_by_id(db, orden_id)
    if not db_orden:
        return None
    
    db_orden.estado = estado
    db_orden.updated_at = func.now()
    
    if estado.value == 'cancelada':
        db_orden.canceled_at = func.now()
    
    db.commit()
    db.refresh(db_orden)
    return db_orden


# ============= RECEPCIONES =============

def get_recepcion_by_id(db: Session, recepcion_id: UUID) -> Optional[RecepcionCompra]:
    """Get purchase receipt by ID"""
    return db.query(RecepcionCompra).filter(RecepcionCompra.id == recepcion_id).first()


def generar_folio_recepcion(db: Session, serie: str = "REC") -> str:
    """Generate next receipt folio"""
    ultimo_folio = db.query(func.max(RecepcionCompra.folio)).filter(
        RecepcionCompra.serie == serie
    ).scalar()
    
    if ultimo_folio:
        try:
            numero = int(ultimo_folio.replace(f"{serie}-", "")) + 1
        except:
            numero = 1
    else:
        numero = 1
    
    return f"{serie}-{numero:06d}"


def crear_recepcion_compra(db: Session, recepcion: RecepcionCompraCreate,
                           usuario_id: UUID) -> RecepcionCompra:
    """Create purchase receipt and update inventory"""
    folio = generar_folio_recepcion(db)
    
    db_recepcion = RecepcionCompra(
        folio=folio,
        serie="REC",
        recibio_id=usuario_id,
        **recepcion.model_dump(exclude={'detalles'})
    )
    db.add(db_recepcion)
    db.flush()
    
    # Process details
    for detalle in recepcion.detalles:
        db_detalle = RecepcionCompraDetalle(
            recepcion_id=db_recepcion.id,
            cantidad_aceptada=detalle.cantidad_recibida,
            **detalle.model_dump()
        )
        db.add(db_detalle)
        db.flush()
        
        # Register inventory movement
        from app.models.supply_chain import TipoMovimientoInventario
        
        movimiento = MovimientoInventarioCreate(
            producto_id=detalle.producto_id,
            almacen_id=recepcion.almacen_id,
            tipo_movimiento=TipoMovimientoInventario.ENTRADA_COMPRA,
            cantidad=detalle.cantidad_recibida,
            costo_unitario=detalle.costo_unitario or 0,
            documento_tipo="recepcion_compra",
            documento_id=db_recepcion.id,
            documento_folio=folio
        )
        
        registrar_movimiento_inventario(
            db=db,
            movimiento=movimiento,
            usuario_id=usuario_id
        )
    
    # Update order status
    orden = get_orden_compra_by_id(db, recepcion.orden_compra_id)
    if orden:
        # Check if all items received
        todos_recibidos = all(
            d.cantidad_pendiente == 0 for d in orden.detalles
        )
        if todos_recibidos:
            orden.estado = 'completada'
        else:
            orden.estado = 'parcialmente_recibida'
        orden.fecha_recepcion = recepcion.fecha_recepcion
        orden.recibio_id = usuario_id
    
    db.commit()
    db.refresh(db_recepcion)
    return db_recepcion


# ============= DASHBOARD & REPORTS =============

def get_dashboard_inventario(db: Session) -> dict:
    """Get inventory dashboard metrics"""
    total_productos = db.query(func.count(Producto.id)).filter(
        Producto.deleted_at.is_(None)
    ).scalar()
    
    productos_activos = db.query(func.count(Producto.id)).filter(
        Producto.activo == True,
        Producto.deleted_at.is_(None)
    ).scalar()
    
    productos_bajo_stock = db.query(func.count(Inventario.id)).join(Producto).filter(
        Inventario.cantidad_disponible < Producto.stock_minimo,
        Producto.stock_minimo > 0
    ).scalar()
    
    productos_sin_stock = db.query(func.count(Inventario.id)).filter(
        Inventario.cantidad_disponible == 0
    ).scalar()
    
    valor_inventario = db.query(
        func.sum(Inventario.cantidad_disponible * Inventario.costo_promedio)
    ).scalar() or 0
    
    movimientos_mes = db.query(func.count(MovimientoInventario.id)).filter(
        func.date_trunc('month', MovimientoInventario.created_at) == 
        func.date_trunc('month', func.now())
    ).scalar()
    
    return {
        "total_productos": total_productos,
        "productos_activos": productos_activos,
        "productos_bajo_stock": productos_bajo_stock,
        "productos_sin_stock": productos_sin_stock,
        "valor_total_inventario": Decimal(str(valor_inventario)),
        "movimientos_mes": movimientos_mes
    }


def get_dashboard_compras(db: Session) -> dict:
    """Get purchases dashboard metrics"""
    ordenes_mes = db.query(func.count(OrdenCompra.id)).filter(
        func.date_trunc('month', OrdenCompra.fecha_emision) == 
        func.date_trunc('month', func.now())
    ).scalar()
    
    ordenes_pendientes = db.query(func.count(OrdenCompra.id)).filter(
        OrdenCompra.estado.in_(['borrador', 'autorizada', 'en_proceso'])
    ).scalar()
    
    proveedores_activos = db.query(func.count(Proveedor.id)).filter(
        Proveedor.activo == True,
        Proveedor.deleted_at.is_(None)
    ).scalar()
    
    compras_total = db.query(
        func.sum(OrdenCompra.total)
    ).filter(
        func.date_trunc('month', OrdenCompra.fecha_emision) == 
        func.date_trunc('month', func.now()),
        OrdenCompra.estado != 'cancelada'
    ).scalar() or 0
    
    return {
        "ordenes_mes": ordenes_mes,
        "ordenes_pendientes": ordenes_pendientes,
        "proveedores_activos": proveedores_activos,
        "compras_mes_total": Decimal(str(compras_total)),
        "recepciones_pendientes": ordenes_pendientes
    }
