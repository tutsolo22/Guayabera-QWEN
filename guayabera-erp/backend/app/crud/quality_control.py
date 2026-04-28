"""
Quality Control CRUD Operations: Quality inspections, standards, and tracking
Specialized for textile manufacturing quality control
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.quality_control import (
    PlanMuestreo, InspeccionCalidad, RegistroDefecto,
    EstandarCalidad, Certificacion, ProductoEstandar, ProductoCertificacion
)
from app.schemas.quality_control import (
    PlanMuestreoCreate, PlanMuestreoUpdate,
    InspeccionCalidadCreate, InspeccionCalidadUpdate,
    RegistroDefectoCreate, RegistroDefectoUpdate,
    EstandarCalidadCreate, EstandarCalidadUpdate,
    CertificacionCreate, CertificacionUpdate,
    ProductoEstandarCreate, ProductoEstandarUpdate,
    ProductoCertificacionCreate, ProductoCertificacionUpdate
)


# ============================================================================
# SAMPLING PLAN CRUD
# ============================================================================

def create_plan_muestreo(db: Session, plan_data: PlanMuestreoCreate) -> PlanMuestreo:
    """Create a new sampling plan"""
    # Check if code already exists
    existing_plan = db.query(PlanMuestreo).filter(PlanMuestreo.codigo == plan_data.codigo).first()
    if existing_plan:
        raise ValueError(f"A sampling plan with code {plan_data.codigo} already exists")
    
    db_plan = PlanMuestreo(**plan_data.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_plan_muestreo(db: Session, plan_id: UUID) -> Optional[PlanMuestreo]:
    """Get a sampling plan by ID"""
    return db.query(PlanMuestreo).filter(PlanMuestreo.id == plan_id).first()


def get_plan_muestreo_by_codigo(db: Session, codigo: str) -> Optional[PlanMuestreo]:
    """Get a sampling plan by code"""
    return db.query(PlanMuestreo).filter(PlanMuestreo.codigo == codigo).first()


def get_planes_muestreo(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[PlanMuestreo]:
    """Get list of sampling plans, optionally filtered"""
    query = db.query(PlanMuestreo)
    
    if activo is not None:
        query = query.filter(PlanMuestreo.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_plan_muestreo(db: Session, plan_id: UUID, plan_data: PlanMuestreoUpdate) -> Optional[PlanMuestreo]:
    """Update a sampling plan"""
    db_plan = get_plan_muestreo(db, plan_id)
    if db_plan:
        update_data = plan_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_plan, field, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan


def delete_plan_muestreo(db: Session, plan_id: UUID) -> bool:
    """Delete a sampling plan"""
    db_plan = get_plan_muestreo(db, plan_id)
    if db_plan:
        db.delete(db_plan)
        db.commit()
        return True
    return False


# ============================================================================
# QUALITY INSPECTION CRUD
# ============================================================================

def create_inspeccion_calidad(db: Session, inspeccion_data: InspeccionCalidadCreate) -> InspeccionCalidad:
    """Create a new quality inspection"""
    # Generate unique code if not provided
    if not inspeccion_data.codigo:
        from datetime import datetime
        year = datetime.now().year
        count = db.query(InspeccionCalidad).count() + 1
        inspeccion_data.codigo = f"QC-{year}-{count:04d}"
    
    db_inspeccion = InspeccionCalidad(**inspeccion_data.model_dump())
    db.add(db_inspeccion)
    db.commit()
    db.refresh(db_inspeccion)
    return db_inspeccion


def get_inspeccion_calidad(db: Session, inspeccion_id: UUID) -> Optional[InspeccionCalidad]:
    """Get a quality inspection by ID"""
    return db.query(InspeccionCalidad).filter(InspeccionCalidad.id == inspeccion_id).first()


def get_inspeccion_calidad_by_codigo(db: Session, codigo: str) -> Optional[InspeccionCalidad]:
    """Get a quality inspection by code"""
    return db.query(InspeccionCalidad).filter(InspeccionCalidad.codigo == codigo).first()


def get_inspecciones_by_tipo(db: Session, tipo: str, skip: int = 0, limit: int = 100) -> List[InspeccionCalidad]:
    """Get inspections by type"""
    return db.query(InspeccionCalidad).filter(InspeccionCalidad.tipo_inspeccion == tipo).offset(skip).limit(limit).all()


def get_inspecciones_by_producto(db: Session, producto_id: UUID, skip: int = 0, limit: int = 100) -> List[InspeccionCalidad]:
    """Get inspections for a specific product"""
    return db.query(InspeccionCalidad).filter(InspeccionCalidad.producto_id == producto_id).offset(skip).limit(limit).all()


def update_inspeccion_calidad(db: Session, inspeccion_id: UUID, inspeccion_data: InspeccionCalidadUpdate) -> Optional[InspeccionCalidad]:
    """Update a quality inspection"""
    db_inspeccion = get_inspeccion_calidad(db, inspeccion_id)
    if db_inspeccion:
        update_data = inspeccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inspeccion, field, value)
        db.commit()
        db.refresh(db_inspeccion)
    return db_inspeccion


def delete_inspeccion_calidad(db: Session, inspeccion_id: UUID) -> bool:
    """Delete a quality inspection"""
    db_inspeccion = get_inspeccion_calidad(db, inspeccion_id)
    if db_inspeccion:
        db.delete(db_inspeccion)
        db.commit()
        return True
    return False


# ============================================================================
# DEFECT RECORD CRUD
# ============================================================================

def create_registro_defecto(db: Session, defecto_data: RegistroDefectoCreate) -> RegistroDefecto:
    """Create a new defect record"""
    db_defecto = RegistroDefecto(**defecto_data.model_dump())
    db.add(db_defecto)
    db.commit()
    db.refresh(db_defecto)
    return db_defecto


def get_registro_defecto(db: Session, defecto_id: UUID) -> Optional[RegistroDefecto]:
    """Get a defect record by ID"""
    return db.query(RegistroDefecto).filter(RegistroDefecto.id == defecto_id).first()


def get_registros_defecto_by_inspeccion(db: Session, inspeccion_id: UUID) -> List[RegistroDefecto]:
    """Get all defect records for a specific inspection"""
    return db.query(RegistroDefecto).filter(RegistroDefecto.inspeccion_id == inspeccion_id).all()


def update_registro_defecto(db: Session, defecto_id: UUID, defecto_data: RegistroDefectoUpdate) -> Optional[RegistroDefecto]:
    """Update a defect record"""
    db_defecto = get_registro_defecto(db, defecto_id)
    if db_defecto:
        update_data = defecto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_defecto, field, value)
        db.commit()
        db.refresh(db_defecto)
    return db_defecto


def delete_registro_defecto(db: Session, defecto_id: UUID) -> bool:
    """Delete a defect record"""
    db_defecto = get_registro_defecto(db, defecto_id)
    if db_defecto:
        db.delete(db_defecto)
        db.commit()
        return True
    return False


# ============================================================================
# QUALITY STANDARD CRUD
# ============================================================================

def create_estandar_calidad(db: Session, estandar_data: EstandarCalidadCreate) -> EstandarCalidad:
    """Create a new quality standard"""
    # Check if code already exists
    existing_estandar = db.query(EstandarCalidad).filter(EstandarCalidad.codigo == estandar_data.codigo).first()
    if existing_estandar:
        raise ValueError(f"A quality standard with code {estandar_data.codigo} already exists")
    
    db_estandar = EstandarCalidad(**estandar_data.model_dump())
    db.add(db_estandar)
    db.commit()
    db.refresh(db_estandar)
    return db_estandar


def get_estandar_calidad(db: Session, estandar_id: UUID) -> Optional[EstandarCalidad]:
    """Get a quality standard by ID"""
    return db.query(EstandarCalidad).filter(EstandarCalidad.id == estandar_id).first()


def get_estandar_calidad_by_codigo(db: Session, codigo: str) -> Optional[EstandarCalidad]:
    """Get a quality standard by code"""
    return db.query(EstandarCalidad).filter(EstandarCalidad.codigo == codigo).first()


def get_estandares_calidad(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[EstandarCalidad]:
    """Get list of quality standards, optionally filtered"""
    query = db.query(EstandarCalidad)
    
    if activo is not None:
        query = query.filter(EstandarCalidad.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_estandar_calidad(db: Session, estandar_id: UUID, estandar_data: EstandarCalidadUpdate) -> Optional[EstandarCalidad]:
    """Update a quality standard"""
    db_estandar = get_estandar_calidad(db, estandar_id)
    if db_estandar:
        update_data = estandar_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_estandar, field, value)
        db.commit()
        db.refresh(db_estandar)
    return db_estandar


def delete_estandar_calidad(db: Session, estandar_id: UUID) -> bool:
    """Delete a quality standard"""
    db_estandar = get_estandar_calidad(db, estandar_id)
    if db_estandar:
        db.delete(db_estandar)
        db.commit()
        return True
    return False


# ============================================================================
# CERTIFICATION CRUD
# ============================================================================

def create_certificacion(db: Session, certificacion_data: CertificacionCreate) -> Certificacion:
    """Create a new certification"""
    # Check if certificate number already exists
    existing_cert = db.query(Certificacion).filter(Certificacion.numero_certificado == certificacion_data.numero_certificado).first()
    if existing_cert:
        raise ValueError(f"A certification with number {certificacion_data.numero_certificado} already exists")
    
    db_cert = Certificacion(**certificacion_data.model_dump())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert


def get_certificacion(db: Session, certificacion_id: UUID) -> Optional[Certificacion]:
    """Get a certification by ID"""
    return db.query(Certificacion).filter(Certificacion.id == certificacion_id).first()


def get_certificacion_by_numero(db: Session, numero: str) -> Optional[Certificacion]:
    """Get a certification by certificate number"""
    return db.query(Certificacion).filter(Certificacion.numero_certificado == numero).first()


def get_certificaciones(db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[Certificacion]:
    """Get list of certifications, optionally filtered"""
    query = db.query(Certificacion)
    
    if estado is not None:
        query = query.filter(Certificacion.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def update_certificacion(db: Session, certificacion_id: UUID, certificacion_data: CertificacionUpdate) -> Optional[Certificacion]:
    """Update a certification"""
    db_cert = get_certificacion(db, certificacion_id)
    if db_cert:
        update_data = certificacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cert, field, value)
        db.commit()
        db.refresh(db_cert)
    return db_cert


def delete_certificacion(db: Session, certificacion_id: UUID) -> bool:
    """Delete a certification"""
    db_cert = get_certificacion(db, certificacion_id)
    if db_cert:
        db.delete(db_cert)
        db.commit()
        return True
    return False


# ============================================================================
# PRODUCT-STANDARD ASSOCIATION CRUD
# ============================================================================

def create_producto_estandar(db: Session, assoc_data: ProductoEstandarCreate) -> ProductoEstandar:
    """Create a new product-standard association"""
    db_assoc = ProductoEstandar(**assoc_data.model_dump())
    db.add(db_assoc)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc


def get_producto_estandar(db: Session, assoc_id: UUID) -> Optional[ProductoEstandar]:
    """Get a product-standard association by ID"""
    return db.query(ProductoEstandar).filter(ProductoEstandar.id == assoc_id).first()


def get_estandares_by_producto(db: Session, producto_id: UUID) -> List[ProductoEstandar]:
    """Get all standards for a specific product"""
    return db.query(ProductoEstandar).filter(ProductoEstandar.producto_id == producto_id, ProductoEstandar.activo == True).all()


def get_productos_by_estandar(db: Session, estandar_id: UUID) -> List[ProductoEstandar]:
    """Get all products for a specific standard"""
    return db.query(ProductoEstandar).filter(ProductoEstandar.estandar_id == estandar_id, ProductoEstandar.activo == True).all()


def update_producto_estandar(db: Session, assoc_id: UUID, assoc_data: ProductoEstandarUpdate) -> Optional[ProductoEstandar]:
    """Update a product-standard association"""
    db_assoc = get_producto_estandar(db, assoc_id)
    if db_assoc:
        update_data = assoc_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_assoc, field, value)
        db.commit()
        db.refresh(db_assoc)
    return db_assoc


def delete_producto_estandar(db: Session, assoc_id: UUID) -> bool:
    """Delete a product-standard association"""
    db_assoc = get_producto_estandar(db, assoc_id)
    if db_assoc:
        db.delete(db_assoc)
        db.commit()
        return True
    return False


# ============================================================================
# PRODUCT-CERTIFICATION ASSOCIATION CRUD
# ============================================================================

def create_producto_certificacion(db: Session, assoc_data: ProductoCertificacionCreate) -> ProductoCertificacion:
    """Create a new product-certification association"""
    db_assoc = ProductoCertificacion(**assoc_data.model_dump())
    db.add(db_assoc)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc


def get_producto_certificacion(db: Session, assoc_id: UUID) -> Optional[ProductoCertificacion]:
    """Get a product-certification association by ID"""
    return db.query(ProductoCertificacion).filter(ProductoCertificacion.id == assoc_id).first()


def get_certificaciones_by_producto(db: Session, producto_id: UUID) -> List[ProductoCertificacion]:
    """Get all certifications for a specific product"""
    return db.query(ProductoCertificacion).filter(ProductoCertificacion.producto_id == producto_id, ProductoCertificacion.activo == True).all()


def get_productos_by_certificacion(db: Session, certificacion_id: UUID) -> List[ProductoCertificacion]:
    """Get all products for a specific certification"""
    return db.query(ProductoCertificacion).filter(ProductoCertificacion.certificacion_id == certificacion_id, ProductoCertificacion.activo == True).all()


def update_producto_certificacion(db: Session, assoc_id: UUID, assoc_data: ProductoCertificacionUpdate) -> Optional[ProductoCertificacion]:
    """Update a product-certification association"""
    db_assoc = get_producto_certificacion(db, assoc_id)
    if db_assoc:
        update_data = assoc_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_assoc, field, value)
        db.commit()
        db.refresh(db_assoc)
    return db_assoc


def delete_producto_certificacion(db: Session, assoc_id: UUID) -> bool:
    """Delete a product-certification association"""
    db_assoc = get_producto_certificacion(db, assoc_id)
    if db_assoc:
        db.delete(db_assoc)
        db.commit()
        return True
    return False