"""
Sales API Router
Specialized for textile manufacturing companies
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.sales import (
    ClienteCreate, ClienteUpdate, ClienteResponse,
    DireccionEntregaCreate, DireccionEntregaUpdate, DireccionEntregaResponse,
    AlmacenCreate, AlmacenUpdate, AlmacenResponse,
    MovimientoInventarioCreate, MovimientoInventarioUpdate, MovimientoInventarioResponse,
    TransferenciaInventarioCreate, TransferenciaInventarioUpdate, TransferenciaInventarioResponse,
    DetalleTransferenciaCreate, DetalleTransferenciaUpdate, DetalleTransferenciaResponse,
    PedidoCreate, PedidoUpdate, PedidoResponse,
    DetallePedidoCreate, DetallePedidoUpdate, DetallePedidoResponse,
    VentaCreate, VentaUpdate, VentaResponse,
    PagoCreate, PagoUpdate, PagoResponse,
    BusquedaAvanzadaCreate, BusquedaAvanzadaUpdate, BusquedaAvanzadaResponse
)
from app.crud.sales import (
    create_cliente, get_cliente, get_cliente_by_codigo, get_cliente_by_rfc,
    get_clientes, update_cliente, delete_cliente,
    create_direccion_entrega, get_direccion_entrega, get_direcciones_entrega_by_cliente,
    update_direccion_entrega, delete_direccion_entrega,
    create_almacen, get_almacen, get_almacen_by_codigo,
    get_almacenes, update_almacen, delete_almacen,
    create_movimiento_inventario, get_movimiento_inventario, get_movimientos_by_almacen_fecha,
    get_movimientos_by_producto, update_movimiento_inventario, delete_movimiento_inventario,
    create_transferencia_inventario, get_transferencia, get_transferencia_by_folio,
    get_transferencias_by_almacen_origen, get_transferencias_by_almacen_destino,
    update_transferencia_inventario, delete_transferencia_inventario,
    create_detalle_transferencia, get_detalle_transferencia, get_detalles_by_transferencia,
    update_detalle_transferencia, delete_detalle_transferencia,
    create_pedido, get_pedido, get_pedido_by_folio,
    get_pedidos_by_cliente, update_pedido, delete_pedido,
    create_detalle_pedido, get_detalle_pedido, get_detalles_by_pedido,
    update_detalle_pedido, delete_detalle_pedido,
    create_venta, get_venta, get_venta_by_folio,
    get_ventas_by_cliente, update_venta, delete_venta,
    create_pago, get_pago, get_pagos_by_venta,
    update_pago, delete_pago,
    create_busqueda_avanzada, get_busqueda_avanzada, get_busquedas_avanzadas_by_producto,
    update_busqueda_avanzada, delete_busqueda_avanzada
)

router = APIRouter(prefix="/sales", tags=["Sales"])

# ============================================================================
# CUSTOMER ENDPOINTS
# ============================================================================

@router.post("/customers/", response_model=ClienteResponse)
def create_customer(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    # Check if customer code already exists
    existing_cliente = get_cliente_by_codigo(db, cliente.codigo)
    if existing_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this code already exists"
        )
    
    # Check if RFC already exists
    existing_rfc = get_cliente_by_rfc(db, cliente.rfc)
    if existing_rfc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this RFC already exists"
        )
    
    return create_cliente(db=db, cliente_data=cliente)


@router.get("/customers/{cliente_id}", response_model=ClienteResponse)
def get_customer(cliente_id: str, db: Session = Depends(get_db)):
    """Get a customer by ID"""
    cliente = get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return cliente


@router.get("/customers/", response_model=List[ClienteResponse])
def get_customers(
    skip: int = 0, 
    limit: int = 100,
    tipo_cliente: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of customers, optionally filtered"""
    return get_clientes(
        db, 
        skip=skip, 
        limit=limit, 
        tipo_cliente=tipo_cliente, 
        activo=activo
    )


@router.put("/customers/{cliente_id}", response_model=ClienteResponse)
def update_customer(
    cliente_id: str, 
    cliente_data: ClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a customer"""
    updated_cliente = update_cliente(
        db=db, 
        cliente_id=cliente_id, 
        cliente_data=cliente_data
    )
    if not updated_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return updated_cliente


@router.delete("/customers/{cliente_id}")
def delete_customer(cliente_id: str, db: Session = Depends(get_db)):
    """Delete a customer"""
    success = delete_cliente(db=db, cliente_id=cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return {"message": "Customer deleted successfully"}


# ============================================================================
# DELIVERY ADDRESS ENDPOINTS
# ============================================================================

@router.post("/delivery-addresses/", response_model=DireccionEntregaResponse)
def create_delivery_address(direccion: DireccionEntregaCreate, db: Session = Depends(get_db)):
    """Create a new delivery address"""
    return create_direccion_entrega(db=db, direccion_data=direccion)


@router.get("/delivery-addresses/{direccion_id}", response_model=DireccionEntregaResponse)
def get_delivery_address(direccion_id: str, db: Session = Depends(get_db)):
    """Get a delivery address by ID"""
    direccion = get_direccion_entrega(db, direccion_id)
    if not direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery address not found"
        )
    return direccion


@router.get("/customers/{cliente_id}/delivery-addresses", response_model=List[DireccionEntregaResponse])
def get_customer_delivery_addresses(cliente_id: str, db: Session = Depends(get_db)):
    """Get all delivery addresses for a specific customer"""
    return get_direcciones_entrega_by_cliente(db, cliente_id)


@router.put("/delivery-addresses/{direccion_id}", response_model=DireccionEntregaResponse)
def update_delivery_address(
    direccion_id: str, 
    direccion_data: DireccionEntregaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a delivery address"""
    updated_direccion = update_direccion_entrega(
        db=db, 
        direccion_id=direccion_id, 
        direccion_data=direccion_data
    )
    if not updated_direccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery address not found"
        )
    return updated_direccion


@router.delete("/delivery-addresses/{direccion_id}")
def delete_delivery_address(direccion_id: str, db: Session = Depends(get_db)):
    """Delete a delivery address"""
    success = delete_direccion_entrega(db=db, direccion_id=direccion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery address not found"
        )
    return {"message": "Delivery address deleted successfully"}


# ============================================================================
# WAREHOUSE ENDPOINTS
# ============================================================================

@router.post("/warehouses/", response_model=AlmacenResponse)
def create_warehouse(almacen: AlmacenCreate, db: Session = Depends(get_db)):
    """Create a new warehouse"""
    # Check if warehouse code already exists
    existing_almacen = get_almacen_by_codigo(db, almacen.codigo)
    if existing_almacen:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Warehouse with this code already exists"
        )
    
    return create_almacen(db=db, almacen_data=almacen)


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


@router.get("/warehouses/", response_model=List[AlmacenResponse])
def get_warehouses(
    skip: int = 0, 
    limit: int = 100,
    tipo: Optional[str] = None,
    activo: Optional[bool] = None,
    empresa_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of warehouses, optionally filtered"""
    uuid_empresa_id = None
    if empresa_id:
        from uuid import UUID
        try:
            uuid_empresa_id = UUID(empresa_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid company ID format"
            )
    
    return get_almacenes(
        db, 
        skip=skip, 
        limit=limit, 
        tipo=tipo, 
        activo=activo,
        empresa_id=uuid_empresa_id
    )


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
# INVENTORY MOVEMENT ENDPOINTS
# ============================================================================

@router.post("/inventory-movements/", response_model=MovimientoInventarioResponse)
def create_inventory_movement(movimiento: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    """Create a new inventory movement"""
    return create_movimiento_inventario(db=db, movimiento_data=movimiento)


@router.get("/inventory-movements/{movimiento_id}", response_model=MovimientoInventarioResponse)
def get_inventory_movement(movimiento_id: str, db: Session = Depends(get_db)):
    """Get an inventory movement by ID"""
    movimiento = get_movimiento_inventario(db, movimiento_id)
    if not movimiento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory movement not found"
        )
    return movimiento


@router.get("/warehouses/{almacen_id}/inventory-movements", response_model=List[MovimientoInventarioResponse])
def get_warehouse_inventory_movements(
    almacen_id: str, 
    fecha_inicio: str, 
    fecha_fin: str, 
    db: Session = Depends(get_db)
):
    """Get inventory movements for a warehouse within a date range"""
    from datetime import datetime
    try:
        start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        end_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    
    return get_movimientos_by_almacen_fecha(
        db, almacen_id, start_date, end_date
    )


@router.get("/products/{producto_id}/inventory-movements", response_model=List[MovimientoInventarioResponse])
def get_product_inventory_movements(producto_id: str, db: Session = Depends(get_db)):
    """Get all movements for a specific product"""
    return get_movimientos_by_producto(db, producto_id)


@router.put("/inventory-movements/{movimiento_id}", response_model=MovimientoInventarioResponse)
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


@router.delete("/inventory-movements/{movimiento_id}")
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
# INVENTORY TRANSFER ENDPOINTS
# ============================================================================

@router.post("/inventory-transfers/", response_model=TransferenciaInventarioResponse)
def create_inventory_transfer(transferencia: TransferenciaInventarioCreate, db: Session = Depends(get_db)):
    """Create a new inventory transfer"""
    try:
        return create_transferencia_inventario(db=db, transferencia_data=transferencia)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/inventory-transfers/{transferencia_id}", response_model=TransferenciaInventarioResponse)
def get_inventory_transfer(transferencia_id: str, db: Session = Depends(get_db)):
    """Get an inventory transfer by ID"""
    transferencia = get_transferencia(db, transferencia_id)
    if not transferencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory transfer not found"
        )
    return transferencia


@router.get("/inventory-transfers/", response_model=List[TransferenciaInventarioResponse])
def get_inventory_transfers_by_warehouse(
    almacen_origen_id: Optional[str] = None,
    almacen_destino_id: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get inventory transfers by warehouse, optionally filtered by state"""
    if almacen_origen_id:
        return get_transferencias_by_almacen_origen(db, almacen_origen_id, estado)
    elif almacen_destino_id:
        return get_transferencias_by_almacen_destino(db, almacen_destino_id, estado)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either origen or destino warehouse ID must be provided"
        )


@router.put("/inventory-transfers/{transferencia_id}", response_model=TransferenciaInventarioResponse)
def update_inventory_transfer(
    transferencia_id: str, 
    transferencia_data: TransferenciaInventarioUpdate, 
    db: Session = Depends(get_db)
):
    """Update an inventory transfer"""
    updated_transferencia = update_transferencia_inventario(
        db=db, 
        transferencia_id=transferencia_id, 
        transferencia_data=transferencia_data
    )
    if not updated_transferencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory transfer not found"
        )
    return updated_transferencia


@router.delete("/inventory-transfers/{transferencia_id}")
def delete_inventory_transfer(transferencia_id: str, db: Session = Depends(get_db)):
    """Delete an inventory transfer"""
    success = delete_transferencia_inventario(db=db, transferencia_id=transferencia_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory transfer not found"
        )
    return {"message": "Inventory transfer deleted successfully"}


# ============================================================================
# TRANSFER DETAIL ENDPOINTS
# ============================================================================

@router.post("/transfer-details/", response_model=DetalleTransferenciaResponse)
def create_transfer_detail(detalle: DetalleTransferenciaCreate, db: Session = Depends(get_db)):
    """Create a new transfer detail"""
    return create_detalle_transferencia(db=db, detalle_data=detalle)


@router.get("/transfer-details/{detalle_id}", response_model=DetalleTransferenciaResponse)
def get_transfer_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Get a transfer detail by ID"""
    detalle = get_detalle_transferencia(db, detalle_id)
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer detail not found"
        )
    return detalle


@router.get("/inventory-transfers/{transferencia_id}/details", response_model=List[DetalleTransferenciaResponse])
def get_transfer_details(transferencia_id: str, db: Session = Depends(get_db)):
    """Get all details for a specific transfer"""
    return get_detalles_by_transferencia(db, transferencia_id)


@router.put("/transfer-details/{detalle_id}", response_model=DetalleTransferenciaResponse)
def update_transfer_detail(
    detalle_id: str, 
    detalle_data: DetalleTransferenciaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a transfer detail"""
    updated_detalle = update_detalle_transferencia(
        db=db, 
        detalle_id=detalle_id, 
        detalle_data=detalle_data
    )
    if not updated_detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer detail not found"
        )
    return updated_detalle


@router.delete("/transfer-details/{detalle_id}")
def delete_transfer_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Delete a transfer detail"""
    success = delete_detalle_transferencia(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transfer detail not found"
        )
    return {"message": "Transfer detail deleted successfully"}


# ============================================================================
# SALES ORDER ENDPOINTS
# ============================================================================

@router.post("/orders/", response_model=PedidoResponse)
def create_sales_order(pedido: PedidoCreate, db: Session = Depends(get_db)):
    """Create a new sales order"""
    try:
        return create_pedido(db=db, pedido_data=pedido)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/orders/{pedido_id}", response_model=PedidoResponse)
def get_sales_order(pedido_id: str, db: Session = Depends(get_db)):
    """Get a sales order by ID"""
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales order not found"
        )
    return pedido


@router.get("/customers/{cliente_id}/orders", response_model=List[PedidoResponse])
def get_customer_orders(
    cliente_id: str, 
    estado: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """Get all orders for a specific client, optionally filtered by state"""
    return get_pedidos_by_cliente(db, cliente_id, estado)


@router.put("/orders/{pedido_id}", response_model=PedidoResponse)
def update_sales_order(
    pedido_id: str, 
    pedido_data: PedidoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a sales order"""
    updated_pedido = update_pedido(
        db=db, 
        pedido_id=pedido_id, 
        pedido_data=pedido_data
    )
    if not updated_pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales order not found"
        )
    return updated_pedido


@router.delete("/orders/{pedido_id}")
def delete_sales_order(pedido_id: str, db: Session = Depends(get_db)):
    """Delete a sales order"""
    success = delete_pedido(db=db, pedido_id=pedido_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales order not found"
        )
    return {"message": "Sales order deleted successfully"}


# ============================================================================
# ORDER DETAIL ENDPOINTS
# ============================================================================

@router.post("/order-details/", response_model=DetallePedidoResponse)
def create_order_detail(detalle: DetallePedidoCreate, db: Session = Depends(get_db)):
    """Create a new order detail"""
    return create_detalle_pedido(db=db, detalle_data=detalle)


@router.get("/order-details/{detalle_id}", response_model=DetallePedidoResponse)
def get_order_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Get an order detail by ID"""
    detalle = get_detalle_pedido(db, detalle_id)
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found"
        )
    return detalle


@router.get("/orders/{pedido_id}/details", response_model=List[DetallePedidoResponse])
def get_order_details(pedido_id: str, db: Session = Depends(get_db)):
    """Get all details for a specific order"""
    return get_detalles_by_pedido(db, pedido_id)


@router.put("/order-details/{detalle_id}", response_model=DetallePedidoResponse)
def update_order_detail(
    detalle_id: str, 
    detalle_data: DetallePedidoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an order detail"""
    updated_detalle = update_detalle_pedido(
        db=db, 
        detalle_id=detalle_id, 
        detalle_data=detalle_data
    )
    if not updated_detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found"
        )
    return updated_detalle


@router.delete("/order-details/{detalle_id}")
def delete_order_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Delete an order detail"""
    success = delete_detalle_pedido(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found"
        )
    return {"message": "Order detail deleted successfully"}


# ============================================================================
# SALE ENDPOINTS
# ============================================================================

@router.post("/sales/", response_model=VentaResponse)
def create_sale(venta: VentaCreate, db: Session = Depends(get_db)):
    """Create a new sale"""
    try:
        return create_venta(db=db, venta_data=venta)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/sales/{venta_id}", response_model=VentaResponse)
def get_sale(venta_id: str, db: Session = Depends(get_db)):
    """Get a sale by ID"""
    venta = get_venta(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return venta


@router.get("/customers/{cliente_id}/sales", response_model=List[VentaResponse])
def get_customer_sales(
    cliente_id: str, 
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all sales for a specific client, optionally filtered by date range"""
    from datetime import datetime
    start_date = None
    end_date = None
    
    if fecha_inicio:
        try:
            start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid start date format. Use YYYY-MM-DD."
            )
    
    if fecha_fin:
        try:
            end_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid end date format. Use YYYY-MM-DD."
            )
    
    return get_ventas_by_cliente(db, cliente_id, start_date, end_date)


@router.put("/sales/{venta_id}", response_model=VentaResponse)
def update_sale(
    venta_id: str, 
    venta_data: VentaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a sale"""
    updated_venta = update_venta(
        db=db, 
        venta_id=venta_id, 
        venta_data=venta_data
    )
    if not updated_venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return updated_venta


@router.delete("/sales/{venta_id}")
def delete_sale(venta_id: str, db: Session = Depends(get_db)):
    """Delete a sale"""
    success = delete_venta(db=db, venta_id=venta_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return {"message": "Sale deleted successfully"}


# ============================================================================
# PAYMENT ENDPOINTS
# ============================================================================

@router.post("/payments/", response_model=PagoResponse)
def create_payment(pago: PagoCreate, db: Session = Depends(get_db)):
    """Create a new payment"""
    return create_pago(db=db, pago_data=pago)


@router.get("/payments/{pago_id}", response_model=PagoResponse)
def get_payment(pago_id: str, db: Session = Depends(get_db)):
    """Get a payment by ID"""
    pago = get_pago(db, pago_id)
    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return pago


@router.get("/sales/{venta_id}/payments", response_model=List[PagoResponse])
def get_sale_payments(venta_id: str, db: Session = Depends(get_db)):
    """Get all payments for a specific sale"""
    return get_pagos_by_venta(db, venta_id)


@router.put("/payments/{pago_id}", response_model=PagoResponse)
def update_payment(
    pago_id: str, 
    pago_data: PagoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a payment"""
    updated_pago = update_pago(
        db=db, 
        pago_id=pago_id, 
        pago_data=pago_data
    )
    if not updated_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return updated_pago


@router.delete("/payments/{pago_id}")
def delete_payment(pago_id: str, db: Session = Depends(get_db)):
    """Delete a payment"""
    success = delete_pago(db=db, pago_id=pago_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return {"message": "Payment deleted successfully"}


# ============================================================================
# ADVANCED SEARCH ENDPOINTS
# ============================================================================

@router.post("/advanced-search/", response_model=BusquedaAvanzadaResponse)
def create_advanced_search(busqueda: BusquedaAvanzadaCreate, db: Session = Depends(get_db)):
    """Create a new advanced search record"""
    return create_busqueda_avanzada(db=db, busqueda_data=busqueda)


@router.get("/advanced-search/{busqueda_id}", response_model=BusquedaAvanzadaResponse)
def get_advanced_search(busqueda_id: str, db: Session = Depends(get_db)):
    """Get an advanced search record by ID"""
    busqueda = get_busqueda_avanzada(db, busqueda_id)
    if not busqueda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advanced search record not found"
        )
    return busqueda


@router.get("/products/{producto_id}/advanced-search", response_model=List[BusquedaAvanzadaResponse])
def get_product_advanced_searches(producto_id: str, db: Session = Depends(get_db)):
    """Get all advanced searches for a specific product"""
    return get_busquedas_avanzadas_by_producto(db, producto_id)


@router.put("/advanced-search/{busqueda_id}", response_model=BusquedaAvanzadaResponse)
def update_advanced_search(
    busqueda_id: str, 
    busqueda_data: BusquedaAvanzadaUpdate, 
    db: Session = Depends(get_db)
):
    """Update an advanced search record"""
    updated_busqueda = update_busqueda_avanzada(
        db=db, 
        busqueda_id=busqueda_id, 
        busqueda_data=busqueda_data
    )
    if not updated_busqueda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advanced search record not found"
        )
    return updated_busqueda


@router.delete("/advanced-search/{busqueda_id}")
def delete_advanced_search(busqueda_id: str, db: Session = Depends(get_db)):
    """Delete an advanced search record"""
    success = delete_busqueda_avanzada(db=db, busqueda_id=busqueda_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advanced search record not found"
        )
    return {"message": "Advanced search record deleted successfully"}