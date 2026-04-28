"""
Quality Control API Router: Quality inspections, standards, and tracking
Specialized for textile manufacturing quality control
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.quality_control import (
    PlanMuestreoCreate, PlanMuestreoUpdate, PlanMuestreoResponse,
    InspeccionCalidadCreate, InspeccionCalidadUpdate, InspeccionCalidadResponse,
    RegistroDefectoCreate, RegistroDefectoUpdate, RegistroDefectoResponse,
    EstandarCalidadCreate, EstandarCalidadUpdate, EstandarCalidadResponse,
    CertificacionCreate, CertificacionUpdate, CertificacionResponse,
    ProductoEstandarCreate, ProductoEstandarUpdate, ProductoEstandarResponse,
    ProductoCertificacionCreate, ProductoCertificacionUpdate, ProductoCertificacionResponse
)
from app.crud.quality_control import (
    create_plan_muestreo, get_plan_muestreo, get_plan_muestreo_by_codigo,
    get_planes_muestreo, update_plan_muestreo, delete_plan_muestreo,
    create_inspeccion_calidad, get_inspeccion_calidad, get_inspeccion_calidad_by_codigo,
    get_inspecciones_by_tipo, get_inspecciones_by_producto, update_inspeccion_calidad,
    delete_inspeccion_calidad,
    create_registro_defecto, get_registro_defecto, get_registros_defecto_by_inspeccion,
    update_registro_defecto, delete_registro_defecto,
    create_estandar_calidad, get_estandar_calidad, get_estandar_calidad_by_codigo,
    get_estandares_calidad, update_estandar_calidad, delete_estandar_calidad,
    create_certificacion, get_certificacion, get_certificacion_by_numero,
    get_certificaciones, update_certificacion, delete_certificacion,
    create_producto_estandar, get_producto_estandar, get_estandares_by_producto,
    get_productos_by_estandar, update_producto_estandar, delete_producto_estandar,
    create_producto_certificacion, get_producto_certificacion, get_certificaciones_by_producto,
    get_productos_by_certificacion, update_producto_certificacion, delete_producto_certificacion
)

router = APIRouter(prefix="/quality-control", tags=["Quality Control"])

# ============================================================================
# SAMPLING PLAN ENDPOINTS
# ============================================================================

@router.post("/sampling-plans/", response_model=PlanMuestreoResponse)
def create_sampling_plan(plan: PlanMuestreoCreate, db: Session = Depends(get_db)):
    """Create a new sampling plan"""
    try:
        return create_plan_muestreo(db=db, plan_data=plan)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/sampling-plans/{plan_id}", response_model=PlanMuestreoResponse)
def get_sampling_plan(plan_id: str, db: Session = Depends(get_db)):
    """Get a sampling plan by ID"""
    plan = get_plan_muestreo(db, plan_id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sampling plan not found"
        )
    return plan


@router.get("/sampling-plans/code/{codigo}", response_model=PlanMuestreoResponse)
def get_sampling_plan_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a sampling plan by code"""
    plan = get_plan_muestreo_by_codigo(db, codigo)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sampling plan not found"
        )
    return plan


@router.get("/sampling-plans/", response_model=List[PlanMuestreoResponse])
def get_sampling_plans(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of sampling plans, optionally filtered"""
    return get_planes_muestreo(db, skip, limit, activo)


@router.put("/sampling-plans/{plan_id}", response_model=PlanMuestreoResponse)
def update_sampling_plan(
    plan_id: str, 
    plan_data: PlanMuestreoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a sampling plan"""
    updated_plan = update_plan_muestreo(
        db=db, 
        plan_id=plan_id, 
        plan_data=plan_data
    )
    if not updated_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sampling plan not found"
        )
    return updated_plan


@router.delete("/sampling-plans/{plan_id}")
def delete_sampling_plan(plan_id: str, db: Session = Depends(get_db)):
    """Delete a sampling plan"""
    success = delete_plan_muestreo(db=db, plan_id=plan_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sampling plan not found"
        )
    return {"message": "Sampling plan deleted successfully"}


# ============================================================================
# QUALITY INSPECTION ENDPOINTS
# ============================================================================

@router.post("/inspections/", response_model=InspeccionCalidadResponse)
def create_quality_inspection(inspeccion: InspeccionCalidadCreate, db: Session = Depends(get_db)):
    """Create a new quality inspection"""
    return create_inspeccion_calidad(db=db, inspeccion_data=inspeccion)


@router.get("/inspections/{inspeccion_id}", response_model=InspeccionCalidadResponse)
def get_quality_inspection(inspeccion_id: str, db: Session = Depends(get_db)):
    """Get a quality inspection by ID"""
    inspeccion = get_inspeccion_calidad(db, inspeccion_id)
    if not inspeccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality inspection not found"
        )
    return inspeccion


@router.get("/inspections/code/{codigo}", response_model=InspeccionCalidadResponse)
def get_inspection_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a quality inspection by code"""
    inspeccion = get_inspeccion_calidad_by_codigo(db, codigo)
    if not inspeccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality inspection not found"
        )
    return inspeccion


@router.get("/inspections/type/{tipo}", response_model=List[InspeccionCalidadResponse])
def get_inspections_by_type(
    tipo: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get inspections by type"""
    return get_inspecciones_by_tipo(db, tipo, skip, limit)


@router.get("/inspections/product/{producto_id}", response_model=List[InspeccionCalidadResponse])
def get_inspections_by_product(
    producto_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get inspections for a specific product"""
    return get_inspecciones_by_producto(db, producto_id, skip, limit)


@router.put("/inspections/{inspeccion_id}", response_model=InspeccionCalidadResponse)
def update_quality_inspection(
    inspeccion_id: str, 
    inspeccion_data: InspeccionCalidadUpdate, 
    db: Session = Depends(get_db)
):
    """Update a quality inspection"""
    updated_inspeccion = update_inspeccion_calidad(
        db=db, 
        inspeccion_id=inspeccion_id, 
        inspeccion_data=inspeccion_data
    )
    if not updated_inspeccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality inspection not found"
        )
    return updated_inspeccion


@router.delete("/inspections/{inspeccion_id}")
def delete_quality_inspection(inspeccion_id: str, db: Session = Depends(get_db)):
    """Delete a quality inspection"""
    success = delete_inspeccion_calidad(db=db, inspeccion_id=inspeccion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality inspection not found"
        )
    return {"message": "Quality inspection deleted successfully"}


# ============================================================================
# DEFECT RECORD ENDPOINTS
# ============================================================================

@router.post("/defects/", response_model=RegistroDefectoResponse)
def create_defect_record(defecto: RegistroDefectoCreate, db: Session = Depends(get_db)):
    """Create a new defect record"""
    return create_registro_defecto(db=db, defecto_data=defecto)


@router.get("/defects/{defecto_id}", response_model=RegistroDefectoResponse)
def get_defect_record(defecto_id: str, db: Session = Depends(get_db)):
    """Get a defect record by ID"""
    defecto = get_registro_defecto(db, defecto_id)
    if not defecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect record not found"
        )
    return defecto


@router.get("/defects/inspection/{inspeccion_id}", response_model=List[RegistroDefectoResponse])
def get_defects_by_inspection(inspeccion_id: str, db: Session = Depends(get_db)):
    """Get all defect records for a specific inspection"""
    return get_registros_defecto_by_inspeccion(db, inspeccion_id)


@router.put("/defects/{defecto_id}", response_model=RegistroDefectoResponse)
def update_defect_record(
    defecto_id: str, 
    defecto_data: RegistroDefectoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a defect record"""
    updated_defecto = update_registro_defecto(
        db=db, 
        defecto_id=defecto_id, 
        defecto_data=defecto_data
    )
    if not updated_defecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect record not found"
        )
    return updated_defecto


@router.delete("/defects/{defecto_id}")
def delete_defect_record(defecto_id: str, db: Session = Depends(get_db)):
    """Delete a defect record"""
    success = delete_registro_defecto(db=db, defecto_id=defecto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Defect record not found"
        )
    return {"message": "Defect record deleted successfully"}


# ============================================================================
# QUALITY STANDARD ENDPOINTS
# ============================================================================

@router.post("/standards/", response_model=EstandarCalidadResponse)
def create_quality_standard(estandar: EstandarCalidadCreate, db: Session = Depends(get_db)):
    """Create a new quality standard"""
    try:
        return create_estandar_calidad(db=db, estandar_data=estandar)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/standards/{estandar_id}", response_model=EstandarCalidadResponse)
def get_quality_standard(estandar_id: str, db: Session = Depends(get_db)):
    """Get a quality standard by ID"""
    estandar = get_estandar_calidad(db, estandar_id)
    if not estandar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality standard not found"
        )
    return estandar


@router.get("/standards/code/{codigo}", response_model=EstandarCalidadResponse)
def get_standard_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a quality standard by code"""
    estandar = get_estandar_calidad_by_codigo(db, codigo)
    if not estandar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality standard not found"
        )
    return estandar


@router.get("/standards/", response_model=List[EstandarCalidadResponse])
def get_quality_standards(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of quality standards, optionally filtered"""
    return get_estandares_calidad(db, skip, limit, activo)


@router.put("/standards/{estandar_id}", response_model=EstandarCalidadResponse)
def update_quality_standard(
    estandar_id: str, 
    estandar_data: EstandarCalidadUpdate, 
    db: Session = Depends(get_db)
):
    """Update a quality standard"""
    updated_estandar = update_estandar_calidad(
        db=db, 
        estandar_id=estandar_id, 
        estandar_data=estandar_data
    )
    if not updated_estandar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality standard not found"
        )
    return updated_estandar


@router.delete("/standards/{estandar_id}")
def delete_quality_standard(estandar_id: str, db: Session = Depends(get_db)):
    """Delete a quality standard"""
    success = delete_estandar_calidad(db=db, estandar_id=estandar_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quality standard not found"
        )
    return {"message": "Quality standard deleted successfully"}


# ============================================================================
# CERTIFICATION ENDPOINTS
# ============================================================================

@router.post("/certifications/", response_model=CertificacionResponse)
def create_certification(certificacion: CertificacionCreate, db: Session = Depends(get_db)):
    """Create a new certification"""
    try:
        return create_certificacion(db=db, certificacion_data=certificacion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/certifications/{certificacion_id}", response_model=CertificacionResponse)
def get_certification(certificacion_id: str, db: Session = Depends(get_db)):
    """Get a certification by ID"""
    certificacion = get_certificacion(db, certificacion_id)
    if not certificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    return certificacion


@router.get("/certifications/number/{numero}", response_model=CertificacionResponse)
def get_certification_by_number(numero: str, db: Session = Depends(get_db)):
    """Get a certification by certificate number"""
    certificacion = get_certificacion_by_numero(db, numero)
    if not certificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    return certificacion


@router.get("/certifications/", response_model=List[CertificacionResponse])
def get_certifications(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of certifications, optionally filtered"""
    return get_certificaciones(db, skip, limit, estado)


@router.put("/certifications/{certificacion_id}", response_model=CertificacionResponse)
def update_certification(
    certificacion_id: str, 
    certificacion_data: CertificacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a certification"""
    updated_certificacion = update_certificacion(
        db=db, 
        certificacion_id=certificacion_id, 
        certificacion_data=certificacion_data
    )
    if not updated_certificacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    return updated_certificacion


@router.delete("/certifications/{certificacion_id}")
def delete_certification(certificacion_id: str, db: Session = Depends(get_db)):
    """Delete a certification"""
    success = delete_certificacion(db=db, certificacion_id=certificacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certification not found"
        )
    return {"message": "Certification deleted successfully"}


# ============================================================================
# PRODUCT-STANDARD ASSOCIATION ENDPOINTS
# ============================================================================

@router.post("/product-standards/", response_model=ProductoEstandarResponse)
def create_product_standard_association(assoc: ProductoEstandarCreate, db: Session = Depends(get_db)):
    """Create a new product-standard association"""
    return create_producto_estandar(db=db, assoc_data=assoc)


@router.get("/product-standards/{assoc_id}", response_model=ProductoEstandarResponse)
def get_product_standard_association(assoc_id: str, db: Session = Depends(get_db)):
    """Get a product-standard association by ID"""
    assoc = get_producto_estandar(db, assoc_id)
    if not assoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-standard association not found"
        )
    return assoc


@router.get("/products/{producto_id}/standards", response_model=List[ProductoEstandarResponse])
def get_standards_by_product(producto_id: str, db: Session = Depends(get_db)):
    """Get all standards for a specific product"""
    return get_estandares_by_producto(db, producto_id)


@router.get("/standards/{estandar_id}/products", response_model=List[ProductoEstandarResponse])
def get_products_by_standard(estandar_id: str, db: Session = Depends(get_db)):
    """Get all products for a specific standard"""
    return get_productos_by_estandar(db, estandar_id)


@router.put("/product-standards/{assoc_id}", response_model=ProductoEstandarResponse)
def update_product_standard_association(
    assoc_id: str, 
    assoc_data: ProductoEstandarUpdate, 
    db: Session = Depends(get_db)
):
    """Update a product-standard association"""
    updated_assoc = update_producto_estandar(
        db=db, 
        assoc_id=assoc_id, 
        assoc_data=assoc_data
    )
    if not updated_assoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-standard association not found"
        )
    return updated_assoc


@router.delete("/product-standards/{assoc_id}")
def delete_product_standard_association(assoc_id: str, db: Session = Depends(get_db)):
    """Delete a product-standard association"""
    success = delete_producto_estandar(db=db, assoc_id=assoc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-standard association not found"
        )
    return {"message": "Product-standard association deleted successfully"}


# ============================================================================
# PRODUCT-CERTIFICATION ASSOCIATION ENDPOINTS
# ============================================================================

@router.post("/product-certifications/", response_model=ProductoCertificacionResponse)
def create_product_certification_association(assoc: ProductoCertificacionCreate, db: Session = Depends(get_db)):
    """Create a new product-certification association"""
    return create_producto_certificacion(db=db, assoc_data=assoc)


@router.get("/product-certifications/{assoc_id}", response_model=ProductoCertificacionResponse)
def get_product_certification_association(assoc_id: str, db: Session = Depends(get_db)):
    """Get a product-certification association by ID"""
    assoc = get_producto_certificacion(db, assoc_id)
    if not assoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-certification association not found"
        )
    return assoc


@router.get("/products/{producto_id}/certifications", response_model=List[ProductoCertificacionResponse])
def get_certifications_by_product(producto_id: str, db: Session = Depends(get_db)):
    """Get all certifications for a specific product"""
    return get_certificaciones_by_producto(db, producto_id)


@router.get("/certifications/{certificacion_id}/products", response_model=List[ProductoCertificacionResponse])
def get_products_by_certification(certificacion_id: str, db: Session = Depends(get_db)):
    """Get all products for a specific certification"""
    return get_productos_by_certificacion(db, certificacion_id)


@router.put("/product-certifications/{assoc_id}", response_model=ProductoCertificacionResponse)
def update_product_certification_association(
    assoc_id: str, 
    assoc_data: ProductoCertificacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a product-certification association"""
    updated_assoc = update_producto_certificacion(
        db=db, 
        assoc_id=assoc_id, 
        assoc_data=assoc_data
    )
    if not updated_assoc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-certification association not found"
        )
    return updated_assoc


@router.delete("/product-certifications/{assoc_id}")
def delete_product_certification_association(assoc_id: str, db: Session = Depends(get_db)):
    """Delete a product-certification association"""
    success = delete_producto_certificacion(db=db, assoc_id=assoc_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product-certification association not found"
        )
    return {"message": "Product-certification association deleted successfully"}