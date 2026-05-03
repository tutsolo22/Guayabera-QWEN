"""
Inventory Management CRUD Operations
Specialized for textile manufacturing companies
"""

from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.inventory import (
    CategoriaProductoTextil as Categoria, 
    ProductoTextil, 
    LoteProducto,
    RecepcionCompra as RecepcionCompraInventario,
    EtiquetaProducto,
    TomaInventario, 
    RegistroTomaInventario, 
    DiferenciaInventario,
    MovimientoInventario as MovimientoInventarioModel,
    UnidadMedida
)
from app.models.supply_chain import (
    Producto, 
    Almacen as AlmacenSC,
    Inventario as Existencia,
    MovimientoInventario
)
from app.models.admin import Empresa
from app.schemas.inventory import (
    CategoriaProductoTextilCreate as CategoriaCreate, 
    CategoriaProductoTextilUpdate as CategoriaUpdate, 
    CategoriaProductoTextilResponse as CategoriaResponse,
    ProductoTextilCreate, ProductoTextilUpdate, ProductoTextilResponse,
    UnidadMedidaCreate, UnidadMedidaUpdate, UnidadMedidaResponse,
    TomaInventarioCreate, TomaInventarioUpdate, TomaInventarioResponse,
    RegistroTomaInventarioCreate, RegistroTomaInventarioResponse,
    DiferenciaInventarioCreate, DiferenciaInventarioUpdate, DiferenciaInventarioResponse,
    MovimientoInventarioCreate, MovimientoInventarioResponse,
    BusquedaProductoTextil, ResultadoBusquedaProducto, ResultadoBusquedaAvanzada,
    LoteProductoCreate, LoteProductoUpdate, LoteProductoResponse,
    RecepcionCompraCreate, RecepcionCompraUpdate, RecepcionCompraResponse,
    EtiquetaProductoCreate, EtiquetaProductoUpdate, EtiquetaProductoResponse
)
from app.schemas.supply_chain import ProductoCreate, ProductoUpdate, ProductoResponse, InventarioResponse as ExistenciaResponse
from app.schemas.logistics import AlmacenCreate, AlmacenUpdate, AlmacenResponse


# ============================================================================
# CATEGORY CRUD
# ============================================================================

def create_categoria(db: Session, categoria_data: CategoriaCreate) -> Categoria:
    """Create a new category"""
    db_categoria = Categoria(**categoria_data.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def get_categoria(db: Session, categoria_id: UUID) -> Optional[Categoria]:
    """Get a category by ID"""
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def get_categoria_by_codigo(db: Session, codigo: str) -> Optional[Categoria]:
    """Get a category by code"""
    return db.query(Categoria).filter(Categoria.codigo == codigo).first()


def get_categorias(db: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
    """Get list of categories"""
    return db.query(Categoria).offset(skip).limit(limit).all()


def update_categoria(
    db: Session, 
    categoria_id: UUID, 
    categoria_data: CategoriaUpdate
) -> Optional[Categoria]:
    """Update a category"""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_categoria, field, value)
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def delete_categoria(db: Session, categoria_id: UUID) -> bool:
    """Delete a category"""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return True
    return False


# ============================================================================
# PRODUCT CRUD
# ============================================================================

def create_producto(db: Session, producto_data: ProductoCreate) -> Producto:
    """Create a new product"""
    db_producto = Producto(**producto_data.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def get_producto(db: Session, producto_id: UUID) -> Optional[Producto]:
    """Get a product by ID"""
    return db.query(Producto).filter(Producto.id == producto_id).first()


def get_productos(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
    """Get list of products"""
    return db.query(Producto).offset(skip).limit(limit).all()


def update_producto(
    db: Session, 
    producto_id: UUID, 
    producto_data: ProductoUpdate
) -> Optional[Producto]:
    """Update a product"""
    db_producto = get_producto(db, producto_id)
    if db_producto:
        update_data = producto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto


def delete_producto(db: Session, producto_id: UUID) -> bool:
    """Delete a product"""
    db_producto = get_producto(db, producto_id)
    if db_producto:
        db.delete(db_producto)
        db.commit()
        return True
    return False


# ============================================================================
# PRODUCTO TEXTIL CRUD
# ============================================================================

def create_producto_textil(db: Session, producto_textil_data: ProductoTextilCreate) -> ProductoTextil:
    """Create a new textile product"""
    db_producto_textil = ProductoTextil(**producto_textil_data.model_dump())
    db.add(db_producto_textil)
    db.commit()
    db.refresh(db_producto_textil)
    return db_producto_textil


def get_producto_textil(db: Session, producto_textil_id: UUID) -> Optional[ProductoTextil]:
    """Get a textile product by ID"""
    return db.query(ProductoTextil).filter(ProductoTextil.id == producto_textil_id).first()


def get_productos_textiles(db: Session, skip: int = 0, limit: int = 100) -> List[ProductoTextil]:
    """Get list of textile products"""
    return db.query(ProductoTextil).offset(skip).limit(limit).all()


def update_producto_textil(
    db: Session, 
    producto_textil_id: UUID, 
    producto_textil_data: ProductoTextilUpdate
) -> Optional[ProductoTextil]:
    """Update a textile product"""
    db_producto_textil = get_producto_textil(db, producto_textil_id)
    if db_producto_textil:
        update_data = producto_textil_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto_textil, field, value)
        db.commit()
        db.refresh(db_producto_textil)
    return db_producto_textil


def delete_producto_textil(db: Session, producto_textil_id: UUID) -> bool:
    """Delete a textile product"""
    db_producto_textil = get_producto_textil(db, producto_textil_id)
    if db_producto_textil:
        db.delete(db_producto_textil)
        db.commit()
        return True
    return False


# ============================================================================
# CATEGORIA PRODUCTO TEXTIL CRUD
# ============================================================================

def create_categoria_producto_textil(db: Session, categoria_data: CategoriaCreate) -> Categoria:
    """Create a new textile product category"""
    db_categoria = Categoria(**categoria_data.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def get_categoria_producto_textil(db: Session, categoria_id: UUID) -> Optional[Categoria]:
    """Get a textile product category by ID"""
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def get_categorias_producto_textil(db: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
    """Get list of textile product categories"""
    return db.query(Categoria).offset(skip).limit(limit).all()


def update_categoria_producto_textil(
    db: Session, 
    categoria_id: UUID, 
    categoria_data: CategoriaUpdate
) -> Optional[Categoria]:
    """Update a textile product category"""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_categoria, field, value)
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def delete_categoria_producto_textil(db: Session, categoria_id: UUID) -> bool:
    """Delete a textile product category"""
    db_categoria = get_categoria(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return True
    return False


# ============================================================================
# LOTE PRODUCTO CRUD
# ============================================================================

def create_lote_producto(db: Session, lote_data: LoteProductoCreate) -> LoteProducto:
    """Create a new product batch"""
    db_lote = LoteProducto(**lote_data.model_dump())
    db.add(db_lote)
    db.commit()
    db.refresh(db_lote)
    return db_lote


def get_lote_producto(db: Session, lote_id: UUID) -> Optional[LoteProducto]:
    """Get a product batch by ID"""
    return db.query(LoteProducto).filter(LoteProducto.id == lote_id).first()


def update_lote_producto(
    db: Session, 
    lote_id: UUID, 
    lote_data: LoteProductoUpdate
) -> Optional[LoteProducto]:
    """Update a product batch"""
    db_lote = get_lote_producto(db, lote_id)
    if db_lote:
        update_data = lote_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lote, field, value)
        db.commit()
        db.refresh(db_lote)
    return db_lote


def delete_lote_producto(db: Session, lote_id: UUID) -> bool:
    """Delete a product batch"""
    db_lote = get_lote_producto(db, lote_id)
    if db_lote:
        db.delete(db_lote)
        db.commit()
        return True
    return False


def get_lotes_by_producto_textil(db: Session, producto_textil_id: UUID) -> List[LoteProducto]:
    """Get all batches for a textile product"""
    return db.query(LoteProducto).filter(
        LoteProducto.producto_textil_id == producto_textil_id
    ).all()


def get_lotes_by_proveedor(db: Session, proveedor_id: UUID) -> List[LoteProducto]:
    """Get all batches from a specific supplier"""
    return db.query(LoteProducto).filter(
        LoteProducto.proveedor_id == proveedor_id
    ).all()


# ============================================================================
# RECEPCION COMPRA CRUD
# ============================================================================

def create_recepcion_compra(db: Session, recepcion_data: RecepcionCompraCreate) -> RecepcionCompraInventario:
    """Create a new purchase reception"""
    db_recepcion = RecepcionCompraInventario(**recepcion_data.model_dump())
    db.add(db_recepcion)
    db.commit()
    db.refresh(db_recepcion)
    return db_recepcion


def get_recepcion_compra(db: Session, recepcion_id: UUID) -> Optional[RecepcionCompraInventario]:
    """Get a purchase reception by ID"""
    return db.query(RecepcionCompraInventario).filter(RecepcionCompraInventario.id == recepcion_id).first()


def update_recepcion_compra(
    db: Session, 
    recepcion_id: UUID, 
    recepcion_data: RecepcionCompraUpdate
) -> Optional[RecepcionCompraInventario]:
    """Update a purchase reception"""
    db_recepcion = get_recepcion_compra(db, recepcion_id)
    if db_recepcion:
        update_data = recepcion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recepcion, field, value)
        db.commit()
        db.refresh(db_recepcion)
    return db_recepcion


def delete_recepcion_compra(db: Session, recepcion_id: UUID) -> bool:
    """Delete a purchase reception"""
    db_recepcion = get_recepcion_compra(db, recepcion_id)
    if db_recepcion:
        db.delete(db_recepcion)
        db.commit()
        return True
    return False


def get_recepciones_by_orden_compra(db: Session, orden_compra_id: UUID) -> List[RecepcionCompraInventario]:
    """Get all receptions for a specific purchase order"""
    return db.query(RecepcionCompraInventario).filter(
        RecepcionCompraInventario.orden_compra_id == orden_compra_id
    ).all()


def get_recepciones_by_estado(db: Session, estado: str) -> List[RecepcionCompraInventario]:
    """Get all receptions by state"""
    return db.query(RecepcionCompraInventario).filter(
        RecepcionCompraInventario.estado == estado
    ).all()


# ============================================================================
# ETIQUETA PRODUCTO CRUD
# ============================================================================

def create_etiqueta_producto(db: Session, etiqueta_data: EtiquetaProductoCreate) -> EtiquetaProducto:
    """Create a new product label"""
    db_etiqueta = EtiquetaProducto(**etiqueta_data.model_dump())
    db.add(db_etiqueta)
    db.commit()
    db.refresh(db_etiqueta)
    return db_etiqueta


def get_etiqueta_producto(db: Session, etiqueta_id: UUID) -> Optional[EtiquetaProducto]:
    """Get a product label by ID"""
    return db.query(EtiquetaProducto).filter(EtiquetaProducto.id == etiqueta_id).first()


def update_etiqueta_producto(
    db: Session, 
    etiqueta_id: UUID, 
    etiqueta_data: EtiquetaProductoUpdate
) -> Optional[EtiquetaProducto]:
    """Update a product label"""
    db_etiqueta = get_etiqueta_producto(db, etiqueta_id)
    if db_etiqueta:
        update_data = etiqueta_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_etiqueta, field, value)
        db.commit()
        db.refresh(db_etiqueta)
    return db_etiqueta


def delete_etiqueta_producto(db: Session, etiqueta_id: UUID) -> bool:
    """Delete a product label"""
    db_etiqueta = get_etiqueta_producto(db, etiqueta_id)
    if db_etiqueta:
        db.delete(db_etiqueta)
        db.commit()
        return True
    return False


def get_etiquetas_by_lote_producto(db: Session, lote_producto_id: UUID) -> List[EtiquetaProducto]:
    """Get all labels for a specific product batch"""
    return db.query(EtiquetaProducto).filter(
        EtiquetaProducto.lote_producto_id == lote_producto_id
    ).all()


def get_etiquetas_by_producto_textil(db: Session, producto_textil_id: UUID) -> List[EtiquetaProducto]:
    """Get all labels for a specific textile product"""
    return db.query(EtiquetaProducto).filter(
        EtiquetaProducto.producto_textil_id == producto_textil_id
    ).all()


# ============================================================================
# UNIT OF MEASURE CRUD
# ============================================================================

def create_unidad_medida(db: Session, unidad_data: UnidadMedidaCreate) -> UnidadMedida:
    """Create a new unit of measure"""
    db_unidad = UnidadMedida(**unidad_data.model_dump())
    db.add(db_unidad)
    db.commit()
    db.refresh(db_unidad)
    return db_unidad


def get_unidad_medida(db: Session, unidad_id: UUID) -> Optional[UnidadMedida]:
    """Get a unit of measure by ID"""
    return db.query(UnidadMedida).filter(UnidadMedida.id == unidad_id).first()


def get_unidad_medida_by_codigo(db: Session, codigo: str) -> Optional[UnidadMedida]:
    """Get a unit of measure by code"""
    return db.query(UnidadMedida).filter(UnidadMedida.codigo == codigo).first()


def get_unidades_medida(db: Session, skip: int = 0, limit: int = 100) -> List[UnidadMedida]:
    """Get list of units of measure"""
    return db.query(UnidadMedida).offset(skip).limit(limit).all()


def update_unidad_medida(
    db: Session, 
    unidad_id: UUID, 
    unidad_data: UnidadMedidaUpdate
) -> Optional[UnidadMedida]:
    """Update a unit of measure"""
    db_unidad = get_unidad_medida(db, unidad_id)
    if db_unidad:
        update_data = unidad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_unidad, field, value)
        db.commit()
        db.refresh(db_unidad)
    return db_unidad


def delete_unidad_medida(db: Session, unidad_id: UUID) -> bool:
    """Delete a unit of measure"""
    db_unidad = get_unidad_medida(db, unidad_id)
    if db_unidad:
        db.delete(db_unidad)
        db.commit()
        return True
    return False


# ============================================================================
# WAREHOUSE CRUD
# ============================================================================

def create_almacen(db: Session, almacen_data: AlmacenCreate) -> AlmacenSC:
    """Create a new warehouse"""
    db_almacen = AlmacenSC(**almacen_data.model_dump())
    db.add(db_almacen)
    db.commit()
    db.refresh(db_almacen)
    return db_almacen


def get_almacen(db: Session, almacen_id: UUID) -> Optional[AlmacenSC]:
    """Get a warehouse by ID"""
    return db.query(AlmacenSC).filter(AlmacenSC.id == almacen_id).first()


def get_almacen_by_codigo(db: Session, codigo: str) -> Optional[AlmacenSC]:
    """Get a warehouse by code"""
    return db.query(AlmacenSC).filter(AlmacenSC.codigo == codigo).first()


def get_almacenes(db: Session, skip: int = 0, limit: int = 100) -> List[AlmacenSC]:
    """Get list of warehouses"""
    return db.query(AlmacenSC).offset(skip).limit(limit).all()


def update_almacen(
    db: Session, 
    almacen_id: UUID, 
    almacen_data: AlmacenUpdate
) -> Optional[AlmacenSC]:
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
# CRUD ESPECÍFICOS DE INVENTARIO
# ============================================================================

def create_toma_inventario(db: Session, toma_data: TomaInventarioCreate) -> TomaInventario:
    """Create a new inventory count session"""
    # Generar folio con formato: ALM-0000001
    ultimo_folio = db.query(func.max(TomaInventario.folio)).scalar()
    if ultimo_folio:
        # Extraer número y aumentarlo
        numero = int(ultimo_folio.split('-')[1]) + 1
        folio = f"{ultimo_folio.split('-')[0]}-{numero:07d}"
    else:
        # Si no hay registros anteriores, iniciar con ALM-0000001
        folio = "ALM-0000001"
    
    db_toma = TomaInventario(**toma_data.model_dump(), folio=folio)
    db.add(db_toma)
    db.commit()
    db.refresh(db_toma)
    return db_toma


def get_toma_inventario(db: Session, toma_id: UUID) -> Optional[TomaInventario]:
    """Get an inventory count session by ID"""
    return db.query(TomaInventario).filter(TomaInventario.id == toma_id).first()


def get_tomas_inventario(db: Session, skip: int = 0, limit: int = 100) -> List[TomaInventario]:
    """Get list of inventory count sessions"""
    return db.query(TomaInventario).offset(skip).limit(limit).all()


def update_toma_inventario(
    db: Session, 
    toma_id: UUID, 
    toma_data: TomaInventarioUpdate
) -> Optional[TomaInventario]:
    """Update an inventory count session"""
    db_toma = get_toma_inventario(db, toma_id)
    if db_toma:
        update_data = toma_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_toma, field, value)
        db.commit()
        db.refresh(db_toma)
    return db_toma


def create_registro_toma_inventario(db: Session, registro_data: RegistroTomaInventarioCreate) -> RegistroTomaInventario:
    """Create a new inventory count record"""
    db_registro = RegistroTomaInventario(**registro_data.model_dump())
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro


def get_registros_toma_inventario(db: Session, toma_id: UUID) -> List[RegistroTomaInventario]:
    """Get all records for an inventory count session"""
    return db.query(RegistroTomaInventario).filter(
        RegistroTomaInventario.toma_inventario_id == toma_id
    ).all()


def create_diferencia_inventario(db: Session, diferencia_data: DiferenciaInventarioCreate) -> DiferenciaInventario:
    """Create a new inventory difference record"""
    db_diferencia = DiferenciaInventario(**diferencia_data.model_dump())
    db.add(db_diferencia)
    db.commit()
    db.refresh(db_diferencia)
    return db_diferencia


def get_diferencias_inventario(db: Session, toma_id: UUID) -> List[DiferenciaInventario]:
    """Get all differences for an inventory count session"""
    return db.query(DiferenciaInventario).filter(
        DiferenciaInventario.toma_inventario_id == toma_id
    ).all()


def update_diferencia_inventario(
    db: Session, 
    diferencia_id: UUID, 
    diferencia_data: DiferenciaInventarioUpdate
) -> Optional[DiferenciaInventario]:
    """Update an inventory difference record"""
    db_diferencia = db.query(DiferenciaInventario).filter(DiferenciaInventario.id == diferencia_id).first()
    if db_diferencia:
        update_data = diferencia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_diferencia, field, value)
        db.commit()
        db.refresh(db_diferencia)
    return db_diferencia


def create_movimiento_inventario(db: Session, movimiento_data: MovimientoInventarioCreate) -> MovimientoInventario:
    """Create a new inventory movement record"""
    db_movimiento = MovimientoInventario(**movimiento_data.model_dump())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento


def get_movimientos_inventario_by_tipo(db: Session, tipo_movimiento: str, skip: int = 0, limit: int = 100) -> List[MovimientoInventario]:
    """Get inventory movements by type"""
    return db.query(MovimientoInventario).filter(
        MovimientoInventario.tipo_movimiento == tipo_movimiento
    ).offset(skip).limit(limit).all()


def buscar_productos_textiles_avanzada(
    db: Session,
    busqueda: BusquedaProductoTextil
) -> ResultadoBusquedaAvanzada:
    """Buscar productos textiles con filtros avanzados"""
    query = db.query(
        Producto.id.label("producto_id"),
        Producto.codigo.label("codigo_producto"),
        Producto.nombre.label("nombre_producto"),
        Producto.modelo.label("modelo"),
        Producto.color.label("color"),
        Producto.talla.label("talla"),
        AlmacenSC.id.label("almacen_id"),
        AlmacenSC.nombre.label("almacen_nombre"),
        Empresa.id.label("empresa_id"),
        Empresa.nombre.label("empresa_nombre"),
        Existencia.cantidad.label("cantidad_disponible"),
        Categoria.nombre.label("categoria_producto"),
        Producto.sobrenombre_1.label("sobrenombre_1"),
        Producto.sobrenombre_2.label("sobrenombre_2")
    ).join(
        Existencia, Existencia.producto_id == Producto.id
    ).join(
        AlmacenSC, AlmacenSC.id == Existencia.almacen_id
    ).join(
        Empresa, Empresa.id == AlmacenSC.empresa_id
    ).join(
        Categoria, Categoria.id == Producto.categoria_id
    )

    # Aplicar filtros
    if busqueda.modelo:
        query = query.filter(Producto.modelo.ilike(f"%{busqueda.modelo}%"))
    if busqueda.color:
        query = query.filter(Producto.color.ilike(f"%{busqueda.color}%"))
    if busqueda.talla:
        query = query.filter(Producto.talla.ilike(f"%{busqueda.talla}%"))
    if busqueda.almacen_id:
        query = query.filter(AlmacenSC.id == busqueda.almacen_id)
    if busqueda.empresa_id:
        query = query.filter(Empresa.id == busqueda.empresa_id)
    if busqueda.categoria_producto:
        query = query.filter(Categoria.nombre.ilike(f"%{busqueda.categoria_producto}%"))
    if busqueda.codigo_producto:
        query = query.filter(Producto.codigo.ilike(f"%{busqueda.codigo_producto}%"))
    if busqueda.nombre_producto:
        query = query.filter(Producto.nombre.ilike(f"%{busqueda.nombre_producto}%"))
    if busqueda.sobrenombre_1:
        query = query.filter(Producto.sobrenombre_1.ilike(f"%{busqueda.sobrenombre_1}%"))
    if busqueda.sobrenombre_2:
        query = query.filter(Producto.sobrenombre_2.ilike(f"%{busqueda.sobrenombre_2}%"))

    resultados = query.all()
    
    # Convertir resultados al formato esperado
    resultado_formateado = [
        ResultadoBusquedaProducto(
            producto_id=result.producto_id,
            codigo_producto=result.codigo_producto,
            nombre_producto=result.nombre_producto,
            modelo=result.modelo,
            color=result.color,
            talla=result.talla,
            almacen_id=result.almacen_id,
            almacen_nombre=result.almacen_nombre,
            empresa_id=result.empresa_id,
            empresa_nombre=result.empresa_nombre,
            cantidad_disponible=result.cantidad_disponible,
            categoria_producto=result.categoria_producto,
            sobrenombre_1=result.sobrenombre_1,
            sobrenombre_2=result.sobrenombre_2
        ) for result in resultados
    ]
    
    return ResultadoBusquedaAvanzada(
        resultados=resultado_formateado,
        total_resultados=len(resultado_formateado)
    )

