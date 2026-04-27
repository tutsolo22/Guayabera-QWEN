"""
API routes for Supply Chain module
Purchases, Suppliers, Inventory, Warehouse
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal

from app.core.database import get_db
from app.schemas.supply_chain import (
    ProveedorCreate, ProveedorUpdate, ProveedorResponse, ProveedorContactoResponse,
    ProductoCreate, ProductoUpdate, ProductoResponse,
    AlmacenCategoriaCreate, AlmacenCategoriaResponse, AlmacenCategoriaTree,
    AlmacenCreate, AlmacenUpdate, AlmacenResponse,
    InventarioResponse, InventarioConDetalles,
    MovimientoInventarioCreate, MovimientoInventarioResponse,
    ListaPreciosCreate, ListaPreciosResponse,
    OrdenCompraCreate, OrdenCompraUpdate, OrdenCompraResponse, OrdenCompraConDetalles,
    RecepcionCompraCreate, RecepcionCompraResponse, RecepcionCompraConDetalles,
    DashboardInventario, DashboardCompras, ReporteStockMinimo
)
from app.crud import supply_chain as crud
from app.core.security import get_current_user

router = APIRouter()


# ============= PROVEEDORES =============

@router.post("/proveedores", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
async def crear_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new supplier"""
    # Check if RFC already exists
    existing = crud.get_proveedor_by_rfc(db, proveedor.rfc)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"RFC '{proveedor.rfc}' ya está registrado"
        )
    
    return crud.create_proveedor(db, proveedor)


@router.get("/proveedores", response_model=List[ProveedorResponse])
async def listar_proveedores(
    activo: bool = True,
    tipo_proveedor: str = None,
    db: Session = Depends(get_db)
):
    """List all suppliers"""
    return crud.get_proveedores(db, activo=activo, tipo_proveedor=tipo_proveedor)


@router.get("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def obtener_proveedor(
    proveedor_id: UUID,
    db: Session = Depends(get_db)
):
    """Get supplier by ID"""
    proveedor = crud.get_proveedor_by_id(db, proveedor_id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    return proveedor


@router.put("/proveedores/{proveedor_id}", response_model=ProveedorResponse)
async def actualizar_proveedor(
    proveedor_id: UUID,
    proveedor: ProveedorUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update supplier"""
    updated = crud.update_proveedor(db, proveedor_id, proveedor)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    return updated


@router.delete("/proveedores/{proveedor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proveedor(
    proveedor_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Soft delete supplier"""
    success = crud.delete_proveedor(db, proveedor_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )


@router.get("/proveedores/{proveedor_id}/contactos", response_model=List[ProveedorContactoResponse])
async def listar_contactos_proveedor(
    proveedor_id: UUID,
    db: Session = Depends(get_db)
):
    """Get supplier contacts"""
    proveedor = crud.get_proveedor_by_id(db, proveedor_id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado"
        )
    return crud.get_proveedor_contactos(db, proveedor_id)


# ============= PRODUCTOS =============

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new product"""
    # Check if code already exists
    existing = crud.get_producto_by_codigo(db, producto.codigo)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Código de producto '{producto.codigo}' ya existe"
        )
    
    return crud.create_producto(db, producto)


@router.get("/productos", response_model=List[ProductoResponse])
async def listar_productos(
    activo: bool = True,
    categoria_id: UUID = None,
    busqueda: str = None,
    db: Session = Depends(get_db)
):
    """List all products"""
    return crud.get_productos(db, activo=activo, categoria_id=categoria_id, busqueda=busqueda)


@router.get("/productos/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(
    producto_id: UUID,
    db: Session = Depends(get_db)
):
    """Get product by ID"""
    producto = crud.get_producto_by_id(db, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return producto


@router.put("/productos/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: UUID,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update product"""
    updated = crud.update_producto(db, producto_id, producto)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return updated


@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(
    producto_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Soft delete product"""
    success = crud.delete_producto(db, producto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )


# ============= CATEGORÍAS =============

@router.post("/categorias", response_model=AlmacenCategoriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    categoria: AlmacenCategoriaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new product category"""
    return crud.create_categoria(db, categoria)


@router.get("/categorias", response_model=List[AlmacenCategoriaResponse])
async def listar_categorias(
    activa: bool = True,
    db: Session = Depends(get_db)
):
    """List all categories"""
    return crud.get_categorias(db, activa=activa)


@router.get("/categorias/tree", response_model=List[AlmacenCategoriaTree])
async def listar_categorias_tree(
    db: Session = Depends(get_db)
):
    """List categories as hierarchical tree"""
    categorias = crud.get_categorias(db)
    
    # Build tree structure
    def build_tree(padre_id=None, nivel=1):
        result = []
        for cat in categorias:
            if cat.categoria_padre_id == padre_id:
                cat_dict = {
                    "id": cat.id,
                    "nombre": cat.nombre,
                    "descripcion": cat.descripcion,
                    "codigo": cat.codigo,
                    "nivel": cat.nivel,
                    "categoria_padre_id": cat.categoria_padre_id,
                    "activa": cat.activa,
                    "created_at": cat.created_at,
                    "categorias_hijas": build_tree(cat.id, nivel + 1),
                    "productos": []
                }
                result.append(cat_dict)
        return result
    
    return build_tree()


# ============= ALMACENES =============

@router.post("/almacenes", response_model=AlmacenResponse, status_code=status.HTTP_201_CREATED)
async def crear_almacen(
    almacen: AlmacenCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new warehouse"""
    return crud.create_almacen(db, almacen)


@router.get("/almacenes", response_model=List[AlmacenResponse])
async def listar_almacenes(
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """List all warehouses"""
    return crud.get_almacenes(db, activo=activo)


@router.get("/almacenes/{almacen_id}", response_model=AlmacenResponse)
async def obtener_almacen(
    almacen_id: UUID,
    db: Session = Depends(get_db)
):
    """Get warehouse by ID"""
    almacen = crud.get_almacen_by_id(db, almacen_id)
    if not almacen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Almacén no encontrado"
        )
    return almacen


@router.put("/almacenes/{almacen_id}", response_model=AlmacenResponse)
async def actualizar_almacen(
    almacen_id: UUID,
    almacen: AlmacenUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update warehouse"""
    updated = crud.update_almacen(db, almacen_id, almacen)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Almacén no encontrado"
        )
    return updated


# ============= INVENTARIOS =============

@router.get("/inventarios", response_model=List[InventarioResponse])
async def listar_inventarios(
    almacen_id: UUID = None,
    con_stock: bool = False,
    db: Session = Depends(get_db)
):
    """List inventories"""
    if almacen_id:
        return crud.get_inventarios_by_almacen(db, almacen_id, con_stock=con_stock)
    return crud.get_inventarios_by_almacen(db, almacen_id, con_stock=con_stock)


@router.get("/inventarios/bajo-stock", response_model=List[InventarioConDetalles])
async def listar_bajo_stock(
    db: Session = Depends(get_db)
):
    """List inventories below minimum stock"""
    inventarios = crud.get_inventarios_bajo_stock(db)
    return inventarios


@router.post("/movimientos-inventario", response_model=MovimientoInventarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_movimiento(
    movimiento: MovimientoInventarioCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Register inventory movement"""
    usuario_id = current_user.get("id") if isinstance(current_user, dict) else None
    return crud.registrar_movimiento_inventario(db, movimiento, usuario_id)


# ============= ÓRDENES DE COMPRA =============

@router.post("/ordenes-compra", response_model=OrdenCompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_orden_compra(
    orden: OrdenCompraCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new purchase order"""
    usuario_id = current_user.get("id") if isinstance(current_user, dict) else None
    return crud.crear_orden_compra(db, orden, usuario_id)


@router.get("/ordenes-compra", response_model=List[OrdenCompraResponse])
async def listar_ordenes_compra(
    proveedor_id: UUID = None,
    estado: str = None,
    fecha_desde: date = None,
    fecha_hasta: date = None,
    db: Session = Depends(get_db)
):
    """List purchase orders"""
    return crud.get_ordenes_compra(db, proveedor_id=proveedor_id, estado=estado,
                                   fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)


@router.get("/ordenes-compra/{orden_id}", response_model=OrdenCompraConDetalles)
async def obtener_orden_compra(
    orden_id: UUID,
    db: Session = Depends(get_db)
):
    """Get purchase order with details"""
    orden = crud.get_orden_compra_by_id(db, orden_id)
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )
    return orden


@router.put("/ordenes-compra/{orden_id}/estado", response_model=OrdenCompraResponse)
async def actualizar_estado_orden(
    orden_id: UUID,
    estado: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update purchase order status"""
    from app.models.supply_chain import EstadoOrdenCompra
    
    try:
        estado_enum = EstadoOrdenCompra(estado)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido. Opciones válidas: {[e.value for e in EstadoOrdenCompra]}"
        )
    
    updated = crud.actualizar_estado_orden(db, orden_id, estado_enum)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )
    return updated


# ============= RECEPCIONES =============

@router.post("/recepciones", response_model=RecepcionCompraResponse, status_code=status.HTTP_201_CREATED)
async def crear_recepcion(
    recepcion: RecepcionCompraCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create purchase receipt and update inventory"""
    usuario_id = current_user.get("id") if isinstance(current_user, dict) else None
    return crud.crear_recepcion_compra(db, recepcion, usuario_id)


@router.get("/recepciones/{recepcion_id}", response_model=RecepcionCompraConDetalles)
async def obtener_recepcion(
    recepcion_id: UUID,
    db: Session = Depends(get_db)
):
    """Get purchase receipt with details"""
    recepcion = crud.get_recepcion_by_id(db, recepcion_id)
    if not recepcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recepción no encontrada"
        )
    return recepcion


# ============= DASHBOARD & REPORTS =============

@router.get("/dashboard/inventario", response_model=DashboardInventario)
async def dashboard_inventario(
    db: Session = Depends(get_db)
):
    """Get inventory dashboard metrics"""
    return crud.get_dashboard_inventario(db)


@router.get("/dashboard/compras", response_model=DashboardCompras)
async def dashboard_compras(
    db: Session = Depends(get_db)
):
    """Get purchases dashboard metrics"""
    return crud.get_dashboard_compras(db)


@router.get("/reportes/stock-minimo", response_model=List[ReporteStockMinimo])
async def reporte_stock_minimo(
    db: Session = Depends(get_db)
):
    """Get report of products below minimum stock"""
    inventarios = crud.get_inventarios_bajo_stock(db)
    return inventarios
