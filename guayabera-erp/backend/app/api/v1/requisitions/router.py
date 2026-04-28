"""
Requisition Management API Router: Purchase requisitions, approvals, and tracking
Specialized for ERP system procurement
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.requisitions import (
    RequisicionCreate, RequisicionUpdate, RequisicionResponse,
    DetalleRequisicionCreate, DetalleRequisicionUpdate, DetalleRequisicionResponse,
    ProveedorCotizacionCreate, ProveedorCotizacionUpdate, ProveedorCotizacionResponse,
    FormatoRequisicionCreate, FormatoRequisicionUpdate, FormatoRequisicionResponse
)
from app.crud.requisitions import (
    create_requisicion, get_requisicion, get_requisicion_by_codigo,
    get_requisiciones_by_estado, get_requisiciones_by_solicitante, get_requisiciones_by_supervisor,
    update_requisicion, delete_requisicion,
    create_detalle_requisicion, get_detalle_requisicion, get_detalles_by_requisicion,
    update_detalle_requisicion, delete_detalle_requisicion,
    create_proveedor_cotizacion, get_proveedor_cotizacion, get_cotizaciones_by_requisicion,
    get_cotizaciones_by_proveedor, update_proveedor_cotizacion, delete_proveedor_cotizacion,
    create_formato_requisicion, get_formato_requisicion, get_formato_requisicion_by_codigo,
    get_formatos_requisicion, update_formato_requisicion, delete_formato_requisicion
)

router = APIRouter(prefix="/requisitions", tags=["Requisitions"])

# ============================================================================
# REQUISITION ENDPOINTS
# ============================================================================

@router.post("/", response_model=RequisicionResponse)
def create_requisition(requisicion: RequisicionCreate, db: Session = Depends(get_db)):
    """Create a new requisition"""
    # Check if requisition code already exists
    if requisicion.codigo:
        existing_req = get_requisicion_by_codigo(db, requisicion.codigo)
        if existing_req:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requisition with this code already exists"
            )
    
    return create_requisicion(db=db, requisicion_data=requisicion)


@router.get("/{requisicion_id}", response_model=RequisicionResponse)
def get_requisition(requisicion_id: str, db: Session = Depends(get_db)):
    """Get a requisition by ID"""
    requisicion = get_requisicion(db, requisicion_id)
    if not requisicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition not found"
        )
    return requisicion


@router.get("/code/{codigo}", response_model=RequisicionResponse)
def get_requisition_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a requisition by code"""
    requisicion = get_requisicion_by_codigo(db, codigo)
    if not requisicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition not found"
        )
    return requisicion


@router.get("/", response_model=List[RequisicionResponse])
def get_requisitions(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    solicitante_id: Optional[str] = None,
    supervisor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of requisitions, optionally filtered"""
    if estado:
        return get_requisiciones_by_estado(db, estado, skip, limit)
    elif solicitante_id:
        return get_requisiciones_by_solicitante(db, solicitante_id, skip, limit)
    elif supervisor_id:
        return get_requisiciones_by_supervisor(db, supervisor_id, skip, limit)
    else:
        return get_requisiciones_by_estado(db, "borrador", skip, limit)


@router.put("/{requisicion_id}", response_model=RequisicionResponse)
def update_requisition(
    requisicion_id: str, 
    requisicion_data: RequisicionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a requisition"""
    updated_requisicion = update_requisicion(
        db=db, 
        requisicion_id=requisicion_id, 
        requisicion_data=requisicion_data
    )
    if not updated_requisicion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition not found"
        )
    return updated_requisicion


@router.delete("/{requisicion_id}")
def delete_requisition(requisicion_id: str, db: Session = Depends(get_db)):
    """Delete a requisition"""
    success = delete_requisicion(db=db, requisicion_id=requisicion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition not found"
        )
    return {"message": "Requisition deleted successfully"}


# ============================================================================
# REQUISITION DETAIL ENDPOINTS
# ============================================================================

@router.post("/details/", response_model=DetalleRequisicionResponse)
def create_requisition_detail(detalle: DetalleRequisicionCreate, db: Session = Depends(get_db)):
    """Create a new requisition detail"""
    return create_detalle_requisicion(db=db, detalle_data=detalle)


@router.get("/details/{detalle_id}", response_model=DetalleRequisicionResponse)
def get_requisition_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Get a requisition detail by ID"""
    detalle = get_detalle_requisicion(db, detalle_id)
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition detail not found"
        )
    return detalle


@router.get("/{requisicion_id}/details", response_model=List[DetalleRequisicionResponse])
def get_requisition_details(requisicion_id: str, db: Session = Depends(get_db)):
    """Get all details for a specific requisition"""
    return get_detalles_by_requisicion(db, requisicion_id)


@router.put("/details/{detalle_id}", response_model=DetalleRequisicionResponse)
def update_requisition_detail(
    detalle_id: str, 
    detalle_data: DetalleRequisicionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a requisition detail"""
    updated_detalle = update_detalle_requisicion(
        db=db, 
        detalle_id=detalle_id, 
        detalle_data=detalle_data
    )
    if not updated_detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition detail not found"
        )
    return updated_detalle


@router.delete("/details/{detalle_id}")
def delete_requisition_detail(detalle_id: str, db: Session = Depends(get_db)):
    """Delete a requisition detail"""
    success = delete_detalle_requisicion(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition detail not found"
        )
    return {"message": "Requisition detail deleted successfully"}


# ============================================================================
# SUPPLIER QUOTATION ENDPOINTS
# ============================================================================

@router.post("/quotations/", response_model=ProveedorCotizacionResponse)
def create_supplier_quotation(cotizacion: ProveedorCotizacionCreate, db: Session = Depends(get_db)):
    """Create a new supplier quotation"""
    return create_proveedor_cotizacion(db=db, cotizacion_data=cotizacion)


@router.get("/quotations/{cotizacion_id}", response_model=ProveedorCotizacionResponse)
def get_supplier_quotation(cotizacion_id: str, db: Session = Depends(get_db)):
    """Get a supplier quotation by ID"""
    cotizacion = get_proveedor_cotizacion(db, cotizacion_id)
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier quotation not found"
        )
    return cotizacion


@router.get("/requisitions/{requisicion_id}/quotations", response_model=List[ProveedorCotizacionResponse])
def get_requisition_quotations(requisicion_id: str, db: Session = Depends(get_db)):
    """Get all quotations for a specific requisition"""
    return get_cotizaciones_by_requisicion(db, requisicion_id)


@router.get("/providers/{proveedor_id}/quotations", response_model=List[ProveedorCotizacionResponse])
def get_provider_quotations(proveedor_id: str, db: Session = Depends(get_db)):
    """Get all quotations from a specific supplier"""
    return get_cotizaciones_by_proveedor(db, proveedor_id)


@router.put("/quotations/{cotizacion_id}", response_model=ProveedorCotizacionResponse)
def update_supplier_quotation(
    cotizacion_id: str, 
    cotizacion_data: ProveedorCotizacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a supplier quotation"""
    updated_cotizacion = update_proveedor_cotizacion(
        db=db, 
        cotizacion_id=cotizacion_id, 
        cotizacion_data=cotizacion_data
    )
    if not updated_cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier quotation not found"
        )
    return updated_cotizacion


@router.delete("/quotations/{cotizacion_id}")
def delete_supplier_quotation(cotizacion_id: str, db: Session = Depends(get_db)):
    """Delete a supplier quotation"""
    success = delete_proveedor_cotizacion(db=db, cotizacion_id=cotizacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier quotation not found"
        )
    return {"message": "Supplier quotation deleted successfully"}


# ============================================================================
# REQUISITION FORM ENDPOINTS
# ============================================================================

@router.post("/forms/", response_model=FormatoRequisicionResponse)
def create_requisition_form(form: FormatoRequisicionCreate, db: Session = Depends(get_db)):
    """Create a new requisition form"""
    # Check if form code already exists
    if form.codigo:
        existing_form = get_formato_requisicion_by_codigo(db, form.codigo)
        if existing_form:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requisition form with this code already exists"
            )
    
    return create_formato_requisicion(db=db, formato_data=form)


@router.get("/forms/{formato_id}", response_model=FormatoRequisicionResponse)
def get_requisition_form(formato_id: str, db: Session = Depends(get_db)):
    """Get a requisition form by ID"""
    formato = get_formato_requisicion(db, formato_id)
    if not formato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition form not found"
        )
    return formato


@router.get("/forms/", response_model=List[FormatoRequisicionResponse])
def get_requisition_forms(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of requisition forms, optionally filtered"""
    return get_formatos_requisicion(db, skip, limit, activo)


@router.put("/forms/{formato_id}", response_model=FormatoRequisicionResponse)
def update_requisition_form(
    formato_id: str, 
    formato_data: FormatoRequisicionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a requisition form"""
    updated_form = update_formato_requisicion(
        db=db, 
        formato_id=formato_id, 
        formato_data=formato_data
    )
    if not updated_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition form not found"
        )
    return updated_form


@router.delete("/forms/{formato_id}")
def delete_requisition_form(formato_id: str, db: Session = Depends(get_db)):
    """Delete a requisition form"""
    success = delete_formato_requisicion(db=db, formato_id=formato_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requisition form not found"
        )
    return {"message": "Requisition form deleted successfully"}