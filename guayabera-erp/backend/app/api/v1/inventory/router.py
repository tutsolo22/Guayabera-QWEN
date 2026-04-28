from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.core.database import get_db
from app.models.inventory import ProductoTextil
from app.schemas.inventory import (
    ProductoTextilCreate, ProductoTextilUpdate, ProductoTextilResponse,
    CategoriaProductoTextilCreate, CategoriaProductoTextilUpdate,
    CategoriaProductoTextilResponse, LoteProductoCreate,
    LoteProductoUpdate, LoteProductoResponse, RecepcionCompraCreate,
    RecepcionCompraUpdate, RecepcionCompraResponse,
    EtiquetaProductoCreate, EtiquetaProductoUpdate,
    EtiquetaProductoResponse, BusquedaProductoTextil, ResultadoBusquedaAvanzada,
    TomaInventarioCreate, TomaInventarioUpdate, TomaInventarioResponse,
    RegistroTomaInventarioCreate, RegistroTomaInventarioResponse,
    DiferenciaInventarioCreate, DiferenciaInventarioUpdate, DiferenciaInventarioResponse,
    MovimientoInventarioCreate, MovimientoInventarioResponse
)
from app.crud.inventory import (
    create_producto_textil, get_producto_textil, get_productos_textiles,
    update_producto_textil, delete_producto_textil,
    create_categoria_producto_textil, get_categoria_producto_textil,
    get_categorias_producto_textil, update_categoria_producto_textil,
    delete_categoria_producto_textil, create_lote_producto,
    get_lote_producto, update_lote_producto, delete_lote_producto,
    get_lotes_by_producto_textil, get_lotes_by_proveedor,
    create_recepcion_compra, get_recepcion_compra,
    update_recepcion_compra, delete_recepcion_compra,
    get_recepciones_by_orden_compra, get_recepciones_by_estado,
    create_etiqueta_producto, get_etiqueta_producto,
    update_etiqueta_producto, delete_etiqueta_producto,
    get_etiquetas_by_lote_producto, get_etiquetas_by_producto_textil,
    buscar_productos_textiles_avanzada,
    create_toma_inventario, get_toma_inventario, get_tomas_inventario,
    update_toma_inventario, create_registro_toma_inventario,
    get_registros_toma_inventario, create_diferencia_inventario,
    get_diferencias_inventario, update_diferencia_inventario,
    create_movimiento_inventario, get_movimientos_inventario_by_tipo
)

router = APIRouter()


@router.post("/productos-textiles", response_model=ProductoTextilResponse)
def create_producto_textil_endpoint(
    producto_data: ProductoTextilCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_producto_textil(db, producto_data)


@router.get("/productos-textiles/{producto_id}", response_model=ProductoTextilResponse)
def get_producto_textil_endpoint(
    producto_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    producto = get_producto_textil(db, UUID(producto_id))
    if not producto:
        raise HTTPException(status_code=404, detail="Producto textil no encontrado")
    return producto


@router.get("/productos-textiles", response_model=List[ProductoTextilResponse])
def get_productos_textiles_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_productos_textiles(db, skip, limit)


@router.put("/productos-textiles/{producto_id}", response_model=ProductoTextilResponse)
def update_producto_textil_endpoint(
    producto_id: str,
    producto_data: ProductoTextilUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_producto = update_producto_textil(db, UUID(producto_id), producto_data)
    if not updated_producto:
        raise HTTPException(status_code=404, detail="Producto textil no encontrado")
    return updated_producto


@router.delete("/productos-textiles/{producto_id}")
def delete_producto_textil_endpoint(
    producto_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_producto_textil(db, UUID(producto_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto textil no encontrado")
    return {"message": "Producto textil eliminado exitosamente"}


@router.post("/categorias-producto-textil", response_model=CategoriaProductoTextilResponse)
def create_categoria_producto_textil_endpoint(
    categoria_data: CategoriaProductoTextilCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_categoria_producto_textil(db, categoria_data)


@router.get("/categorias-producto-textil/{categoria_id}", response_model=CategoriaProductoTextilResponse)
def get_categoria_producto_textil_endpoint(
    categoria_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    categoria = get_categoria_producto_textil(db, UUID(categoria_id))
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría de producto textil no encontrada")
    return categoria


@router.get("/categorias-producto-textil", response_model=List[CategoriaProductoTextilResponse])
def get_categorias_producto_textil_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_categorias_producto_textil(db, skip, limit)


@router.put("/categorias-producto-textil/{categoria_id}", response_model=CategoriaProductoTextilResponse)
def update_categoria_producto_textil_endpoint(
    categoria_id: str,
    categoria_data: CategoriaProductoTextilUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_categoria = update_categoria_producto_textil(db, UUID(categoria_id), categoria_data)
    if not updated_categoria:
        raise HTTPException(status_code=404, detail="Categoría de producto textil no encontrada")
    return updated_categoria


@router.delete("/categorias-producto-textil/{categoria_id}")
def delete_categoria_producto_textil_endpoint(
    categoria_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_categoria_producto_textil(db, UUID(categoria_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría de producto textil no encontrada")
    return {"message": "Categoría de producto textil eliminada exitosamente"}


@router.post("/lotes-producto", response_model=LoteProductoResponse)
def create_lote_producto_endpoint(
    lote_data: LoteProductoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_lote_producto(db, lote_data)


@router.get("/lotes-producto/{lote_id}", response_model=LoteProductoResponse)
def get_lote_producto_endpoint(
    lote_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    lote = get_lote_producto(db, UUID(lote_id))
    if not lote:
        raise HTTPException(status_code=404, detail="Lote de producto no encontrado")
    return lote


@router.get("/lotes-producto", response_model=List[LoteProductoResponse])
def get_lotes_producto_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_productos_textiles(db, skip, limit)  # Note: This should be replaced with a proper get_lotes function


@router.put("/lotes-producto/{lote_id}", response_model=LoteProductoResponse)
def update_lote_producto_endpoint(
    lote_id: str,
    lote_data: LoteProductoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_lote = update_lote_producto(db, UUID(lote_id), lote_data)
    if not updated_lote:
        raise HTTPException(status_code=404, detail="Lote de producto no encontrado")
    return updated_lote


@router.delete("/lotes-producto/{lote_id}")
def delete_lote_producto_endpoint(
    lote_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_lote_producto(db, UUID(lote_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Lote de producto no encontrado")
    return {"message": "Lote de producto eliminado exitosamente"}


@router.get("/lotes-producto-textil/{producto_textil_id}")
def get_lotes_by_producto_textil_endpoint(
    producto_textil_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_lotes_by_producto_textil(db, UUID(producto_textil_id))


@router.get("/lotes-proveedor/{proveedor_id}")
def get_lotes_by_proveedor_endpoint(
    proveedor_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_lotes_by_proveedor(db, UUID(proveedor_id))


@router.post("/recepciones-compra", response_model=RecepcionCompraResponse)
def create_recepcion_compra_endpoint(
    recepcion_data: RecepcionCompraCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_recepcion_compra(db, recepcion_data)


@router.get("/recepciones-compra/{recepcion_id}", response_model=RecepcionCompraResponse)
def get_recepcion_compra_endpoint(
    recepcion_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    recepcion = get_recepcion_compra(db, UUID(recepcion_id))
    if not recepcion:
        raise HTTPException(status_code=404, detail="Recepción de compra no encontrada")
    return recepcion


@router.put("/recepciones-compra/{recepcion_id}", response_model=RecepcionCompraResponse)
def update_recepcion_compra_endpoint(
    recepcion_id: str,
    recepcion_data: RecepcionCompraUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_recepcion = update_recepcion_compra(db, UUID(recepcion_id), recepcion_data)
    if not updated_recepcion:
        raise HTTPException(status_code=404, detail="Recepción de compra no encontrada")
    return updated_recepcion


@router.delete("/recepciones-compra/{recepcion_id}")
def delete_recepcion_compra_endpoint(
    recepcion_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_recepcion_compra(db, UUID(recepcion_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Recepción de compra no encontrada")
    return {"message": "Recepción de compra eliminada exitosamente"}


@router.get("/recepciones-orden-compra/{orden_compra_id}")
def get_recepciones_by_orden_compra_endpoint(
    orden_compra_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_recepciones_by_orden_compra(db, UUID(orden_compra_id))


@router.get("/recepciones-estado/{estado}")
def get_recepciones_by_estado_endpoint(
    estado: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_recepciones_by_estado(db, estado)


@router.post("/etiquetas-producto", response_model=EtiquetaProductoResponse)
def create_etiqueta_producto_endpoint(
    etiqueta_data: EtiquetaProductoCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_etiqueta_producto(db, etiqueta_data)


@router.get("/etiquetas-producto/{etiqueta_id}", response_model=EtiquetaProductoResponse)
def get_etiqueta_producto_endpoint(
    etiqueta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    etiqueta = get_etiqueta_producto(db, UUID(etiqueta_id))
    if not etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta de producto no encontrada")
    return etiqueta


@router.put("/etiquetas-producto/{etiqueta_id}", response_model=EtiquetaProductoResponse)
def update_etiqueta_producto_endpoint(
    etiqueta_id: str,
    etiqueta_data: EtiquetaProductoUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_etiqueta = update_etiqueta_producto(db, UUID(etiqueta_id), etiqueta_data)
    if not updated_etiqueta:
        raise HTTPException(status_code=404, detail="Etiqueta de producto no encontrada")
    return updated_etiqueta


@router.delete("/etiquetas-producto/{etiqueta_id}")
def delete_etiqueta_producto_endpoint(
    etiqueta_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    deleted = delete_etiqueta_producto(db, UUID(etiqueta_id))
    if not deleted:
        raise HTTPException(status_code=404, detail="Etiqueta de producto no encontrada")
    return {"message": "Etiqueta de producto eliminada exitosamente"}


@router.get("/etiquetas-lote-producto/{lote_producto_id}")
def get_etiquetas_by_lote_producto_endpoint(
    lote_producto_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_etiquetas_by_lote_producto(db, UUID(lote_producto_id))


@router.get("/etiquetas-producto-textil/{producto_textil_id}")
def get_etiquetas_by_producto_textil_endpoint(
    producto_textil_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_etiquetas_by_producto_textil(db, UUID(producto_textil_id))


# Nuevo endpoint para búsqueda avanzada de productos textiles
@router.post("/buscar-productos-avanzada", response_model=ResultadoBusquedaAvanzada)
def buscar_productos_textiles_avanzada_endpoint(
    busqueda: BusquedaProductoTextil,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resultados, total = buscar_productos_textiles_avanzada(db, busqueda, skip, limit)
    return ResultadoBusquedaAvanzada(
        resultados=resultados,
        total_resultados=total
    )


# ============================================================================
# ENDPOINTS PARA TOMA DE INVENTARIO
# ============================================================================

@router.post("/toma-inventario", response_model=TomaInventarioResponse)
def create_toma_inventario_endpoint(
    toma_data: TomaInventarioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_toma_inventario(db, toma_data)


@router.get("/toma-inventario/{toma_id}", response_model=TomaInventarioResponse)
def get_toma_inventario_endpoint(
    toma_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    toma = get_toma_inventario(db, UUID(toma_id))
    if not toma:
        raise HTTPException(status_code=404, detail="Toma de inventario no encontrada")
    return toma


@router.get("/toma-inventario", response_model=List[TomaInventarioResponse])
def get_tomas_inventario_endpoint(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_tomas_inventario(db, skip, limit)


@router.put("/toma-inventario/{toma_id}", response_model=TomaInventarioResponse)
def update_toma_inventario_endpoint(
    toma_id: str,
    toma_data: TomaInventarioUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_toma = update_toma_inventario(db, UUID(toma_id), toma_data)
    if not updated_toma:
        raise HTTPException(status_code=404, detail="Toma de inventario no encontrada")
    return updated_toma


@router.post("/registro-toma-inventario", response_model=RegistroTomaInventarioResponse)
def create_registro_toma_inventario_endpoint(
    registro_data: RegistroTomaInventarioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_registro_toma_inventario(db, registro_data)


@router.get("/registro-toma-inventario/{toma_id}", response_model=List[RegistroTomaInventarioResponse])
def get_registros_toma_inventario_endpoint(
    toma_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_registros_toma_inventario(db, UUID(toma_id))


@router.post("/diferencia-inventario", response_model=DiferenciaInventarioResponse)
def create_diferencia_inventario_endpoint(
    diferencia_data: DiferenciaInventarioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_diferencia_inventario(db, diferencia_data)


@router.get("/diferencia-inventario/{toma_id}", response_model=List[DiferenciaInventarioResponse])
def get_diferencias_inventario_endpoint(
    toma_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    return get_diferencias_inventario(db, UUID(toma_id))


@router.put("/diferencia-inventario/{diferencia_id}", response_model=DiferenciaInventarioResponse)
def update_diferencia_inventario_endpoint(
    diferencia_id: str,
    diferencia_data: DiferenciaInventarioUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from uuid import UUID
    updated_diferencia = update_diferencia_inventario(db, UUID(diferencia_id), diferencia_data)
    if not updated_diferencia:
        raise HTTPException(status_code=404, detail="Diferencia de inventario no encontrada")
    return updated_diferencia


@router.post("/movimiento-inventario", response_model=MovimientoInventarioResponse)
def create_movimiento_inventario_endpoint(
    movimiento_data: MovimientoInventarioCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_movimiento_inventario(db, movimiento_data)


@router.get("/movimiento-inventario/tipo/{tipo_movimiento}", response_model=List[MovimientoInventarioResponse])
def get_movimientos_inventario_by_tipo_endpoint(
    tipo_movimiento: str,
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_movimientos_inventario_by_tipo(db, tipo_movimiento, skip, limit)
