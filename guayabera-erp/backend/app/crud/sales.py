"""
Sales CRUD Operations
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID
from datetime import date
from decimal import Decimal

from app.models.sales import (
    Cliente, DireccionEntrega, 
    Pedido, DetallePedido,
    Venta, Pago, BusquedaAvanzada, SalesConfiguration, DiscountRule,
    LoyaltyProgram, PriceList, PriceListItem
)
# Importar clases desde el módulo correcto
from app.models.supply_chain import Almacen, MovimientoInventario, OrdenCompra, OrdenCompraDetalle, Proveedor, TransferenciaInventario, DetalleTransferencia
from app.schemas.sales import (
    ClienteCreate, ClienteUpdate,
    DireccionEntregaCreate, DireccionEntregaUpdate,
    AlmacenCreate, AlmacenUpdate,
    MovimientoInventarioCreate, MovimientoInventarioUpdate,
    TransferenciaInventarioCreate, TransferenciaInventarioUpdate,
    DetalleTransferenciaCreate, DetalleTransferenciaUpdate,
    PedidoCreate, PedidoUpdate,
    DetallePedidoCreate, DetallePedidoUpdate,
    VentaCreate, VentaUpdate,
    PagoCreate, PagoUpdate,
    BusquedaAvanzadaCreate, BusquedaAvanzadaUpdate,
    SalesConfigurationCreate, SalesConfigurationUpdate,
    DiscountRuleCreate, DiscountRuleUpdate,
    LoyaltyProgramCreate, LoyaltyProgramUpdate,
    PriceListCreate, PriceListUpdate,
    PriceListItemCreate, PriceListItemUpdate
)


# ============================================================================
# CUSTOMER CRUD
# ============================================================================

def create_cliente(db: Session, cliente_data: ClienteCreate) -> Cliente:
    """Create a new customer"""
    db_cliente = Cliente(**cliente_data.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_cliente(db: Session, cliente_id: UUID) -> Optional[Cliente]:
    """Get a customer by ID"""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_cliente_by_codigo(db: Session, codigo: str) -> Optional[Cliente]:
    """Get a customer by code"""
    return db.query(Cliente).filter(Cliente.codigo == codigo).first()


def get_cliente_by_rfc(db: Session, rfc: str) -> Optional[Cliente]:
    """Get a customer by RFC"""
    return db.query(Cliente).filter(Cliente.rfc == rfc).first()


def get_clientes(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tipo_cliente: Optional[str] = None,
    activo: Optional[bool] = None
) -> List[Cliente]:
    """Get list of customers, optionally filtered"""
    query = db.query(Cliente)
    
    if tipo_cliente:
        query = query.filter(Cliente.tipo_cliente == tipo_cliente)
    if activo is not None:
        query = query.filter(Cliente.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_cliente(
    db: Session, 
    cliente_id: UUID, 
    cliente_data: ClienteUpdate
) -> Optional[Cliente]:
    """Update a customer"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        update_data = cliente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, cliente_id: UUID) -> bool:
    """Delete a customer"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return True
    return False


# ============================================================================
# DELIVERY ADDRESS CRUD
# ============================================================================

def create_direccion_entrega(db: Session, direccion_data: DireccionEntregaCreate) -> DireccionEntrega:
    """Create a new delivery address"""
    db_direccion = DireccionEntrega(**direccion_data.model_dump())
    db.add(db_direccion)
    db.commit()
    db.refresh(db_direccion)
    return db_direccion


def get_direccion_entrega(db: Session, direccion_id: UUID) -> Optional[DireccionEntrega]:
    """Get a delivery address by ID"""
    return db.query(DireccionEntrega).filter(DireccionEntrega.id == direccion_id).first()


def get_direcciones_entrega_by_cliente(db: Session, cliente_id: UUID) -> List[DireccionEntrega]:
    """Get all delivery addresses for a specific customer"""
    return db.query(DireccionEntrega).filter(DireccionEntrega.cliente_id == cliente_id).all()


def update_direccion_entrega(
    db: Session, 
    direccion_id: UUID, 
    direccion_data: DireccionEntregaUpdate
) -> Optional[DireccionEntrega]:
    """Update a delivery address"""
    db_direccion = get_direccion_entrega(db, direccion_id)
    if db_direccion:
        update_data = direccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_direccion, field, value)
        db.commit()
        db.refresh(db_direccion)
    return db_direccion


def delete_direccion_entrega(db: Session, direccion_id: UUID) -> bool:
    """Delete a delivery address"""
    db_direccion = get_direccion_entrega(db, direccion_id)
    if db_direccion:
        db.delete(db_direccion)
        db.commit()
        return True
    return False


# ============================================================================
# WAREHOUSE CRUD
# ============================================================================

def create_almacen(db: Session, almacen_data: AlmacenCreate) -> Almacen:
    """Create a new warehouse"""
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


def get_almacenes(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tipo: Optional[str] = None,
    activo: Optional[bool] = None,
    empresa_id: Optional[UUID] = None
) -> List[Almacen]:
    """Get list of warehouses, optionally filtered"""
    query = db.query(Almacen)
    
    if tipo:
        query = query.filter(Almacen.tipo == tipo)
    if activo is not None:
        query = query.filter(Almacen.activo == activo)
    if empresa_id:
        query = query.filter(Almacen.empresa_id == empresa_id)
    
    return query.offset(skip).limit(limit).all()


def update_almacen(
    db: Session, 
    almacen_id: UUID, 
    almacen_data: AlmacenUpdate
) -> Optional[Almacen]:
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
# INVENTORY MOVEMENT CRUD
# ============================================================================

def create_movimiento_inventario(db: Session, movimiento_data: MovimientoInventarioCreate) -> MovimientoInventario:
    """Create a new inventory movement"""
    db_movimiento = MovimientoInventario(**movimiento_data.model_dump())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def get_movimiento_inventario(db: Session, movimiento_id: UUID) -> Optional[MovimientoInventario]:
    """Get an inventory movement by ID"""
    return db.query(MovimientoInventario).filter(MovimientoInventario.id == movimiento_id).first()


def get_movimientos_by_almacen_fecha(
    db: Session, 
    almacen_id: UUID, 
    fecha_inicio: date, 
    fecha_fin: date
) -> List[MovimientoInventario]:
    """Get inventory movements for a warehouse within a date range"""
    return db.query(MovimientoInventario).filter(
        MovimientoInventario.almacen_id == almacen_id,
        MovimientoInventario.fecha_movimiento >= fecha_inicio,
        MovimientoInventario.fecha_movimiento <= fecha_fin
    ).all()


def get_movimientos_by_producto(db: Session, producto_id: UUID) -> List[MovimientoInventario]:
    """Get all movements for a specific product"""
    return db.query(MovimientoInventario).filter(MovimientoInventario.producto_id == producto_id).all()


def update_movimiento_inventario(
    db: Session, 
    movimiento_id: UUID, 
    movimiento_data: MovimientoInventarioUpdate
) -> Optional[MovimientoInventario]:
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


# ============================================================================
# INVENTORY TRANSFER CRUD
# ============================================================================

def create_transferencia_inventario(db: Session, transferencia_data: TransferenciaInventarioCreate) -> TransferenciaInventario:
    """Create a new inventory transfer"""
    # Check if folio already exists
    existing_transferencia = get_transferencia_by_folio(db, transferencia_data.folio)
    if existing_transferencia:
        raise ValueError(f"A transfer with folio {transferencia_data.folio} already exists")
    
    db_transferencia = TransferenciaInventario(**transferencia_data.model_dump())
    db.add(db_transferencia)
    db.commit()
    db.refresh(db_transferencia)
    return db_transferencia


def get_transferencia(db: Session, transferencia_id: UUID) -> Optional[TransferenciaInventario]:
    """Get an inventory transfer by ID"""
    return db.query(TransferenciaInventario).filter(TransferenciaInventario.id == transferencia_id).first()


def get_transferencia_by_folio(db: Session, folio: str) -> Optional[TransferenciaInventario]:
    """Get an inventory transfer by folio"""
    return db.query(TransferenciaInventario).filter(TransferenciaInventario.folio == folio).first()


def get_transferencias_by_almacen_origen(
    db: Session, 
    almacen_origen_id: UUID,
    estado: Optional[str] = None
) -> List[TransferenciaInventario]:
    """Get all transfers from a specific warehouse, optionally filtered by state"""
    query = db.query(TransferenciaInventario).filter(TransferenciaInventario.almacen_origen_id == almacen_origen_id)
    if estado:
        query = query.filter(TransferenciaInventario.estado == estado)
    return query.all()


def get_transferencias_by_almacen_destino(
    db: Session, 
    almacen_destino_id: UUID,
    estado: Optional[str] = None
) -> List[TransferenciaInventario]:
    """Get all transfers to a specific warehouse, optionally filtered by state"""
    query = db.query(TransferenciaInventario).filter(TransferenciaInventario.almacen_destino_id == almacen_destino_id)
    if estado:
        query = query.filter(TransferenciaInventario.estado == estado)
    return query.all()


def update_transferencia_inventario(
    db: Session, 
    transferencia_id: UUID, 
    transferencia_data: TransferenciaInventarioUpdate
) -> Optional[TransferenciaInventario]:
    """Update an inventory transfer"""
    db_transferencia = get_transferencia(db, transferencia_id)
    if db_transferencia:
        update_data = transferencia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_transferencia, field, value)
        db.commit()
        db.refresh(db_transferencia)
    return db_transferencia


def delete_transferencia_inventario(db: Session, transferencia_id: UUID) -> bool:
    """Delete an inventory transfer"""
    db_transferencia = get_transferencia(db, transferencia_id)
    if db_transferencia:
        db.delete(db_transferencia)
        db.commit()
        return True
    return False


# ============================================================================
# TRANSFER DETAIL CRUD
# ============================================================================

def create_detalle_transferencia(db: Session, detalle_data: DetalleTransferenciaCreate) -> DetalleTransferencia:
    """Create a new transfer detail"""
    db_detalle = DetalleTransferencia(**detalle_data.model_dump())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def get_detalle_transferencia(db: Session, detalle_id: UUID) -> Optional[DetalleTransferencia]:
    """Get a transfer detail by ID"""
    return db.query(DetalleTransferencia).filter(DetalleTransferencia.id == detalle_id).first()


def get_detalles_by_transferencia(db: Session, transferencia_id: UUID) -> List[DetalleTransferencia]:
    """Get all details for a specific transfer"""
    return db.query(DetalleTransferencia).filter(DetalleTransferencia.transferencia_id == transferencia_id).all()


def update_detalle_transferencia(
    db: Session, 
    detalle_id: UUID, 
    detalle_data: DetalleTransferenciaUpdate
) -> Optional[DetalleTransferencia]:
    """Update a transfer detail"""
    db_detalle = get_detalle_transferencia(db, detalle_id)
    if db_detalle:
        update_data = detalle_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_transferencia(db: Session, detalle_id: UUID) -> bool:
    """Delete a transfer detail"""
    db_detalle = get_detalle_transferencia(db, detalle_id)
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
        return True
    return False


# ============================================================================
# SALES ORDER CRUD
# ============================================================================

def create_pedido(db: Session, pedido_data: PedidoCreate) -> Pedido:
    """Create a new sales order"""
    # Check if folio already exists
    existing_pedido = get_pedido_by_folio(db, pedido_data.folio)
    if existing_pedido:
        raise ValueError(f"An order with folio {pedido_data.folio} already exists")
    
    db_pedido = Pedido(**pedido_data.model_dump())
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def get_pedido(db: Session, pedido_id: UUID) -> Optional[Pedido]:
    """Get a sales order by ID"""
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()


def get_pedido_by_folio(db: Session, folio: str) -> Optional[Pedido]:
    """Get a sales order by folio"""
    return db.query(Pedido).filter(Pedido.folio == folio).first()


def get_pedidos_by_cliente(
    db: Session, 
    cliente_id: UUID,
    estado: Optional[str] = None
) -> List[Pedido]:
    """Get all orders for a specific client, optionally filtered by state"""
    query = db.query(Pedido).filter(Pedido.cliente_id == cliente_id)
    if estado:
        query = query.filter(Pedido.estado == estado)
    return query.all()


def update_pedido(
    db: Session, 
    pedido_id: UUID, 
    pedido_data: PedidoUpdate
) -> Optional[Pedido]:
    """Update a sales order"""
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        update_data = pedido_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pedido, field, value)
        db.commit()
        db.refresh(db_pedido)
    return db_pedido


def delete_pedido(db: Session, pedido_id: UUID) -> bool:
    """Delete a sales order"""
    db_pedido = get_pedido(db, pedido_id)
    if db_pedido:
        db.delete(db_pedido)
        db.commit()
        return True
    return False


# ============================================================================
# ORDER DETAIL CRUD
# ============================================================================

def create_detalle_pedido(db: Session, detalle_data: DetallePedidoCreate) -> DetallePedido:
    """Create a new order detail"""
    db_detalle = DetallePedido(**detalle_data.model_dump())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def get_detalle_pedido(db: Session, detalle_id: UUID) -> Optional[DetallePedido]:
    """Get an order detail by ID"""
    return db.query(DetallePedido).filter(DetallePedido.id == detalle_id).first()


def get_detalles_by_pedido(db: Session, pedido_id: UUID) -> List[DetallePedido]:
    """Get all details for a specific order"""
    return db.query(DetallePedido).filter(DetallePedido.pedido_id == pedido_id).all()


def update_detalle_pedido(
    db: Session, 
    detalle_id: UUID, 
    detalle_data: DetallePedidoUpdate
) -> Optional[DetallePedido]:
    """Update an order detail"""
    db_detalle = get_detalle_pedido(db, detalle_id)
    if db_detalle:
        update_data = detalle_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_pedido(db: Session, detalle_id: UUID) -> bool:
    """Delete an order detail"""
    db_detalle = get_detalle_pedido(db, detalle_id)
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
        return True
    return False


# ============================================================================
# SALE CRUD
# ============================================================================

def create_venta(db: Session, venta_data: VentaCreate) -> Venta:
    """Create a new sale"""
    # Check if folio already exists
    existing_venta = get_venta_by_folio(db, venta_data.folio_venta)
    if existing_venta:
        raise ValueError(f"A sale with folio {venta_data.folio_venta} already exists")
    
    db_venta = Venta(**venta_data.model_dump())
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta


def get_venta(db: Session, venta_id: UUID) -> Optional[Venta]:
    """Get a sale by ID"""
    return db.query(Venta).filter(Venta.id == venta_id).first()


def get_venta_by_folio(db: Session, folio_venta: str) -> Optional[Venta]:
    """Get a sale by folio"""
    return db.query(Venta).filter(Venta.folio_venta == folio_venta).first()


def get_ventas_by_cliente(
    db: Session, 
    cliente_id: UUID,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None
) -> List[Venta]:
    """Get all sales for a specific client, optionally filtered by date range"""
    query = db.query(Venta).filter(Venta.cliente_id == cliente_id)
    
    if fecha_inicio:
        query = query.filter(Venta.fecha_venta >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Venta.fecha_venta <= fecha_fin)
    
    return query.all()


def update_venta(
    db: Session, 
    venta_id: UUID, 
    venta_data: VentaUpdate
) -> Optional[Venta]:
    """Update a sale"""
    db_venta = get_venta(db, venta_id)
    if db_venta:
        update_data = venta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_venta, field, value)
        db.commit()
        db.refresh(db_venta)
    return db_venta


def delete_venta(db: Session, venta_id: UUID) -> bool:
    """Delete a sale"""
    db_venta = get_venta(db, venta_id)
    if db_venta:
        db.delete(db_venta)
        db.commit()
        return True
    return False


# ============================================================================
# PAYMENT CRUD
# ============================================================================

def create_pago(db: Session, pago_data: PagoCreate) -> Pago:
    """Create a new payment"""
    db_pago = Pago(**pago_data.model_dump())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago


def get_pago(db: Session, pago_id: UUID) -> Optional[Pago]:
    """Get a payment by ID"""
    return db.query(Pago).filter(Pago.id == pago_id).first()


def get_pagos_by_venta(db: Session, venta_id: UUID) -> List[Pago]:
    """Get all payments for a specific sale"""
    return db.query(Pago).filter(Pago.venta_id == venta_id).all()


def update_pago(
    db: Session, 
    pago_id: UUID, 
    pago_data: PagoUpdate
) -> Optional[Pago]:
    """Update a payment"""
    db_pago = get_pago(db, pago_id)
    if db_pago:
        update_data = pago_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_pago, field, value)
        db.commit()
        db.refresh(db_pago)
    return db_pago


def delete_pago(db: Session, pago_id: UUID) -> bool:
    """Delete a payment"""
    db_pago = get_pago(db, pago_id)
    if db_pago:
        db.delete(db_pago)
        db.commit()
        return True
    return False


# ============================================================================
# ADVANCED SEARCH CRUD
# ============================================================================


# ============================================================================
# SALES CONFIGURATION CRUD
# ============================================================================
def create_sales_configuration(db: Session, config: SalesConfigurationCreate) -> SalesConfiguration:
    db_config = SalesConfiguration(**config.dict(exclude_unset=True))
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_sales_configuration(db: Session, company_id: int) -> Optional[SalesConfiguration]:
    return db.query(SalesConfiguration).filter(SalesConfiguration.company_id == company_id).first()


def update_sales_configuration(
    db: Session, 
    company_id: int, 
    config_update: SalesConfigurationUpdate
) -> Optional[SalesConfiguration]:
    db_config = db.query(SalesConfiguration).filter(SalesConfiguration.company_id == company_id).first()
    if db_config:
        update_data = config_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_config, field, value)
        db.commit()
        db.refresh(db_config)
    return db_config


def delete_sales_configuration(db: Session, company_id: int) -> bool:
    db_config = db.query(SalesConfiguration).filter(SalesConfiguration.company_id == company_id).first()
    if db_config:
        db.delete(db_config)
        db.commit()
        return True
    return False


# ============================================================================
# DISCOUNT RULE CRUD
# ============================================================================
def create_discount_rule(db: Session, rule: DiscountRuleCreate) -> DiscountRule:
    db_rule = DiscountRule(**rule.dict(exclude_unset=True))
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def get_discount_rule(db: Session, rule_id: int) -> Optional[DiscountRule]:
    return db.query(DiscountRule).filter(DiscountRule.id == rule_id).first()


def get_discount_rules_by_company(
    db: Session, 
    company_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[DiscountRule]:
    return (
        db.query(DiscountRule)
        .filter(DiscountRule.company_id == company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_discount_rule(
    db: Session, 
    rule_id: int, 
    rule_update: DiscountRuleUpdate
) -> Optional[DiscountRule]:
    db_rule = db.query(DiscountRule).filter(DiscountRule.id == rule_id).first()
    if db_rule:
        update_data = rule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)
        db.commit()
        db.refresh(db_rule)
    return db_rule


def delete_discount_rule(db: Session, rule_id: int) -> bool:
    db_rule = db.query(DiscountRule).filter(DiscountRule.id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
        return True
    return False


def get_active_discount_rules(db: Session, company_id: int) -> List[DiscountRule]:
    now = datetime.utcnow()
    return (
        db.query(DiscountRule)
        .filter(
            and_(
                DiscountRule.company_id == company_id,
                DiscountRule.is_active == True,
                or_(
                    DiscountRule.start_date <= now,
                    DiscountRule.start_date.is_(None)
                ),
                or_(
                    DiscountRule.end_date >= now,
                    DiscountRule.end_date.is_(None)
                )
            )
        )
        .order_by(DiscountRule.priority.desc())
        .all()
    )


# ============================================================================
# LOYALTY PROGRAM CRUD
# ============================================================================
def create_loyalty_program(db: Session, program: LoyaltyProgramCreate) -> LoyaltyProgram:
    db_program = LoyaltyProgram(**program.dict(exclude_unset=True))
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


def get_loyalty_program(db: Session, program_id: int) -> Optional[LoyaltyProgram]:
    return db.query(LoyaltyProgram).filter(LoyaltyProgram.id == program_id).first()


def get_loyalty_programs_by_company(
    db: Session, 
    company_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[LoyaltyProgram]:
    return (
        db.query(LoyaltyProgram)
        .filter(LoyaltyProgram.company_id == company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_default_loyalty_program(db: Session, company_id: int) -> Optional[LoyaltyProgram]:
    return (
        db.query(LoyaltyProgram)
        .filter(
            and_(
                LoyaltyProgram.company_id == company_id,
                LoyaltyProgram.is_default == True,
                LoyaltyProgram.is_active == True
            )
        )
        .first()
    )


def update_loyalty_program(
    db: Session, 
    program_id: int, 
    program_update: LoyaltyProgramUpdate
) -> Optional[LoyaltyProgram]:
    db_program = db.query(LoyaltyProgram).filter(LoyaltyProgram.id == program_id).first()
    if db_program:
        update_data = program_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_program, field, value)
        
        # Si se está activando como predeterminado, desactivar otros
        if update_data.get('is_default'):
            db.query(LoyaltyProgram).filter(
                and_(
                    LoyaltyProgram.company_id == db_program.company_id,
                    LoyaltyProgram.id != program_id
                )
            ).update({"is_default": False})
        
        db.commit()
        db.refresh(db_program)
    return db_program


def delete_loyalty_program(db: Session, program_id: int) -> bool:
    db_program = db.query(LoyaltyProgram).filter(LoyaltyProgram.id == program_id).first()
    if db_program:
        db.delete(db_program)
        db.commit()
        return True
    return False


# ============================================================================
# PRICE LIST CRUD
# ============================================================================
def create_price_list(db: Session, price_list: PriceListCreate) -> PriceList:
    db_price_list = PriceList(**price_list.dict(exclude_unset=True))
    
    # Si se está creando como predeterminada, desactivar otras
    if price_list.is_default:
        db.query(PriceList).filter(
            and_(
                PriceList.company_id == price_list.company_id,
                PriceList.id != getattr(price_list, 'id', None)
            )
        ).update({"is_default": False})
    
    db.add(db_price_list)
    db.commit()
    db.refresh(db_price_list)
    return db_price_list


def get_price_list(db: Session, price_list_id: int) -> Optional[PriceList]:
    return db.query(PriceList).filter(PriceList.id == price_list_id).first()


def get_price_lists_by_company(
    db: Session, 
    company_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[PriceList]:
    return (
        db.query(PriceList)
        .filter(PriceList.company_id == company_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_default_price_list(db: Session, company_id: int) -> Optional[PriceList]:
    return (
        db.query(PriceList)
        .filter(
            and_(
                PriceList.company_id == company_id,
                PriceList.is_default == True,
                PriceList.is_active == True
            )
        )
        .first()
    )


def update_price_list(
    db: Session, 
    price_list_id: int, 
    price_list_update: PriceListUpdate
) -> Optional[PriceList]:
    db_price_list = db.query(PriceList).filter(PriceList.id == price_list_id).first()
    if db_price_list:
        update_data = price_list_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_price_list, field, value)
        
        # Si se está activando como predeterminada, desactivar otras
        if update_data.get('is_default'):
            db.query(PriceList).filter(
                and_(
                    PriceList.company_id == db_price_list.company_id,
                    PriceList.id != price_list_id
                )
            ).update({"is_default": False})
        
        db.commit()
        db.refresh(db_price_list)
    return db_price_list


def delete_price_list(db: Session, price_list_id: int) -> bool:
    db_price_list = db.query(PriceList).filter(PriceList.id == price_list_id).first()
    
    # No permitir eliminar la lista predeterminada si no hay otras
    other_lists = db.query(PriceList).filter(
        and_(
            PriceList.company_id == db_price_list.company_id,
            PriceList.id != price_list_id
        )
    ).count()
    
    if db_price_list and (not db_price_list.is_default or other_lists > 0):
        db.delete(db_price_list)
        db.commit()
        return True
    return False


# ============================================================================
# PRICE LIST ITEM CRUD
# ============================================================================
def create_price_list_item(db: Session, item: PriceListItemCreate) -> PriceListItem:
    db_item = PriceListItem(**item.dict(exclude_unset=True))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_price_list_item(db: Session, item_id: int) -> Optional[PriceListItem]:
    return db.query(PriceListItem).filter(PriceListItem.id == item_id).first()


def get_price_list_items_by_list(
    db: Session, 
    price_list_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[PriceListItem]:
    return (
        db.query(PriceListItem)
        .filter(PriceListItem.price_list_id == price_list_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_price_list_item_by_product_and_list(
    db: Session, 
    price_list_id: int, 
    product_variant_id: int
) -> Optional[PriceListItem]:
    return (
        db.query(PriceListItem)
        .filter(
            and_(
                PriceListItem.price_list_id == price_list_id,
                PriceListItem.product_variant_id == product_variant_id
            )
        )
        .first()
    )


def update_price_list_item(
    db: Session, 
    item_id: int, 
    item_update: PriceListItemUpdate
) -> Optional[PriceListItem]:
    db_item = db.query(PriceListItem).filter(PriceListItem.id == item_id).first()
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_price_list_item(db: Session, item_id: int) -> bool:
    db_item = db.query(PriceListItem).filter(PriceListItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False


def get_current_price_for_product(
    db: Session, 
    price_list_id: int, 
    product_variant_id: int
) -> Optional[Decimal]:
    """Obtiene el precio actual para un producto en una lista de precios específica"""
    now = datetime.utcnow()
    item = (
        db.query(PriceListItem)
        .filter(
            and_(
                PriceListItem.price_list_id == price_list_id,
                PriceListItem.product_variant_id == product_variant_id,
                or_(
                    PriceListItem.valid_from <= now,
                    PriceListItem.valid_from.is_(None)
                ),
                or_(
                    PriceListItem.valid_until >= now,
                    PriceListItem.valid_until.is_(None)
                )
            )
        )
        .first()
    )
    return item.price if item else None

def create_busqueda_avanzada(db: Session, busqueda_data: BusquedaAvanzadaCreate) -> BusquedaAvanzada:
    """Create a new advanced search record"""
    db_busqueda = BusquedaAvanzada(**busqueda_data.model_dump())
    db.add(db_busqueda)
    db.commit()
    db.refresh(db_busqueda)
    return db_busqueda


def get_busqueda_avanzada(db: Session, busqueda_id: UUID) -> Optional[BusquedaAvanzada]:
    """Get an advanced search record by ID"""
    return db.query(BusquedaAvanzada).filter(BusquedaAvanzada.id == busqueda_id).first()


def get_busquedas_avanzadas_by_producto(db: Session, producto_id: UUID) -> List[BusquedaAvanzada]:
    """Get all advanced searches for a specific product"""
    return db.query(BusquedaAvanzada).filter(BusquedaAvanzada.producto_id == producto_id).all()


def update_busqueda_avanzada(
    db: Session, 
    busqueda_id: UUID, 
    busqueda_data: BusquedaAvanzadaUpdate
) -> Optional[BusquedaAvanzada]:
    """Update an advanced search record"""
    db_busqueda = get_busqueda_avanzada(db, busqueda_id)
    if db_busqueda:
        update_data = busqueda_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_busqueda, field, value)
        db.commit()
        db.refresh(db_busqueda)
    return db_busqueda


def delete_busqueda_avanzada(db: Session, busqueda_id: UUID) -> bool:
    """Delete an advanced search record"""
    db_busqueda = get_busqueda_avanzada(db, busqueda_id)
    if db_busqueda:
        db.delete(db_busqueda)
        db.commit()
        return True
    return False