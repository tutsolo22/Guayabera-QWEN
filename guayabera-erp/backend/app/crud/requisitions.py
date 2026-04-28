"""
Requisition Management CRUD Operations: Purchase requisitions, approvals, and tracking
Specialized for ERP system procurement
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from uuid import UUID

from app.models.requisitions import Requisicion, DetalleRequisicion, ProveedorCotizacion, FormatoRequisicion
from app.schemas.requisitions import (
    RequisicionCreate, RequisicionUpdate,
    DetalleRequisicionCreate, DetalleRequisicionUpdate,
    ProveedorCotizacionCreate, ProveedorCotizacionUpdate,
    FormatoRequisicionCreate, FormatoRequisicionUpdate
)


# ============================================================================
# REQUISITION CRUD
# ============================================================================

def create_requisicion(db: Session, requisicion_data: RequisicionCreate) -> Requisicion:
    """Create a new requisition"""
    # Generate unique code if not provided
    if not requisicion_data.codigo:
        last_req = db.query(Requisicion).order_by(Requisicion.fecha_solicitud.desc()).first()
        last_number = 1
        if last_req:
            try:
                last_number = int(last_req.codigo.split('-')[2]) + 1
            except:
                last_number = 1
        from datetime import datetime
        year = datetime.now().year
        requisicion_data.codigo = f"REQ-{year}-{last_number:04d}"
    
    db_requisicion = Requisicion(**requisicion_data.model_dump())
    db.add(db_requisicion)
    db.commit()
    db.refresh(db_requisicion)
    return db_requisicion


def get_requisicion(db: Session, requisicion_id: UUID) -> Optional[Requisicion]:
    """Get a requisition by ID"""
    return db.query(Requisicion).filter(Requisicion.id == requisicion_id).first()


def get_requisicion_by_codigo(db: Session, codigo: str) -> Optional[Requisicion]:
    """Get a requisition by code"""
    return db.query(Requisicion).filter(Requisicion.codigo == codigo).first()


def get_requisiciones_by_estado(db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[Requisicion]:
    """Get requisitions by state"""
    return db.query(Requisicion).filter(Requisicion.estado == estado).offset(skip).limit(limit).all()


def get_requisiciones_by_solicitante(db: Session, solicitante_id: UUID, skip: int = 0, limit: int = 100) -> List[Requisicion]:
    """Get requisitions by requester"""
    return db.query(Requisicion).filter(Requisicion.solicitante_id == solicitante_id).offset(skip).limit(limit).all()


def get_requisiciones_by_supervisor(db: Session, supervisor_id: UUID, skip: int = 0, limit: int = 100) -> List[Requisicion]:
    """Get requisitions pending approval by supervisor"""
    return db.query(Requisicion).filter(
        Requisicion.supervisor_id == supervisor_id,
        Requisicion.autorizado_supervisor == False,
        Requisicion.estado.in_(['borrador', 'pendiente_autorizacion'])
    ).offset(skip).limit(limit).all()


def update_requisicion(db: Session, requisicion_id: UUID, requisicion_data: RequisicionUpdate) -> Optional[Requisicion]:
    """Update a requisition"""
    db_requisicion = get_requisicion(db, requisicion_id)
    if db_requisicion:
        update_data = requisicion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_requisicion, field, value)
        
        # Update approval dates
        if 'autorizado_supervisor' in update_data and update_data['autorizado_supervisor'] and not db_requisicion.fecha_aprobacion_supervisor:
            from datetime import datetime
            db_requisicion.fecha_aprobacion_supervisor = datetime.now()
        
        if 'autorizado_finanzas' in update_data and update_data['autorizado_finanzas'] and not db_requisicion.fecha_aprobacion_finanzas:
            from datetime import datetime
            db_requisicion.fecha_aprobacion_finanzas = datetime.now()
        
        db.commit()
        db.refresh(db_requisicion)
    return db_requisicion


def delete_requisicion(db: Session, requisicion_id: UUID) -> bool:
    """Delete a requisition"""
    db_requisicion = get_requisicion(db, requisicion_id)
    if db_requisicion:
        db.delete(db_requisicion)
        db.commit()
        return True
    return False


# ============================================================================
# REQUISITION DETAIL CRUD
# ============================================================================

def create_detalle_requisicion(db: Session, detalle_data: DetalleRequisicionCreate) -> DetalleRequisicion:
    """Create a new requisition detail"""
    # Calculate total if not provided
    if not detalle_data.precio_total_estimado and detalle_data.precio_unitario_estimado:
        detalle_data.precio_total_estimado = detalle_data.precio_unitario_estimado * detalle_data.cantidad
    
    db_detalle = DetalleRequisicion(**detalle_data.model_dump())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


def get_detalle_requisicion(db: Session, detalle_id: UUID) -> Optional[DetalleRequisicion]:
    """Get a requisition detail by ID"""
    return db.query(DetalleRequisicion).filter(DetalleRequisicion.id == detalle_id).first()


def get_detalles_by_requisicion(db: Session, requisicion_id: UUID) -> List[DetalleRequisicion]:
    """Get all details for a specific requisition"""
    return db.query(DetalleRequisicion).filter(DetalleRequisicion.requisicion_id == requisicion_id).all()


def update_detalle_requisicion(db: Session, detalle_id: UUID, detalle_data: DetalleRequisicionUpdate) -> Optional[DetalleRequisicion]:
    """Update a requisition detail"""
    db_detalle = get_detalle_requisicion(db, detalle_id)
    if db_detalle:
        update_data = detalle_data.model_dump(exclude_unset=True)
        
        # Calculate total if unit price changes
        if 'precio_unitario_estimado' in update_data and update_data['precio_unitario_estimado']:
            new_price = update_data['precio_unitario_estimado']
            quantity = db_detalle.cantidad if 'cantidad' not in update_data else update_data['cantidad']
            update_data['precio_total_estimado'] = new_price * quantity
        
        # Calculate total if quantity changes
        if 'cantidad' in update_data and update_data['cantidad']:
            quantity = update_data['cantidad']
            unit_price = db_detalle.precio_unitario_estimado if 'precio_unitario_estimado' not in update_data else update_data['precio_unitario_estimado']
            update_data['precio_total_estimado'] = unit_price * quantity
        
        for field, value in update_data.items():
            setattr(db_detalle, field, value)
        
        db.commit()
        db.refresh(db_detalle)
    return db_detalle


def delete_detalle_requisicion(db: Session, detalle_id: UUID) -> bool:
    """Delete a requisition detail"""
    db_detalle = get_detalle_requisicion(db, detalle_id)
    if db_detalle:
        db.delete(db_detalle)
        db.commit()
        return True
    return False


# ============================================================================
# SUPPLIER QUOTATION CRUD
# ============================================================================

def create_proveedor_cotizacion(db: Session, cotizacion_data: ProveedorCotizacionCreate) -> ProveedorCotizacion:
    """Create a new supplier quotation"""
    db_cotizacion = ProveedorCotizacion(**cotizacion_data.model_dump())
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)
    return db_cotizacion


def get_proveedor_cotizacion(db: Session, cotizacion_id: UUID) -> Optional[ProveedorCotizacion]:
    """Get a supplier quotation by ID"""
    return db.query(ProveedorCotizacion).filter(ProveedorCotizacion.id == cotizacion_id).first()


def get_cotizaciones_by_requisicion(db: Session, requisicion_id: UUID) -> List[ProveedorCotizacion]:
    """Get all quotations for a specific requisition"""
    return db.query(ProveedorCotizacion).filter(ProveedorCotizacion.requisicion_id == requisicion_id).all()


def get_cotizaciones_by_proveedor(db: Session, proveedor_id: UUID) -> List[ProveedorCotizacion]:
    """Get all quotations from a specific supplier"""
    return db.query(ProveedorCotizacion).filter(ProveedorCotizacion.proveedor_id == proveedor_id).all()


def update_proveedor_cotizacion(db: Session, cotizacion_id: UUID, cotizacion_data: ProveedorCotizacionUpdate) -> Optional[ProveedorCotizacion]:
    """Update a supplier quotation"""
    db_cotizacion = get_proveedor_cotizacion(db, cotizacion_id)
    if db_cotizacion:
        update_data = cotizacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cotizacion, field, value)
        db.commit()
        db.refresh(db_cotizacion)
    return db_cotizacion


def delete_proveedor_cotizacion(db: Session, cotizacion_id: UUID) -> bool:
    """Delete a supplier quotation"""
    db_cotizacion = get_proveedor_cotizacion(db, cotizacion_id)
    if db_cotizacion:
        db.delete(db_cotizacion)
        db.commit()
        return True
    return False


# ============================================================================
# REQUISITION FORM CRUD
# ============================================================================

def create_formato_requisicion(db: Session, formato_data: FormatoRequisicionCreate) -> FormatoRequisicion:
    """Create a new requisition form"""
    db_formato = FormatoRequisicion(**formato_data.model_dump())
    db.add(db_formato)
    db.commit()
    db.refresh(db_formato)
    return db_formato


def get_formato_requisicion(db: Session, formato_id: UUID) -> Optional[FormatoRequisicion]:
    """Get a requisition form by ID"""
    return db.query(FormatoRequisicion).filter(FormatoRequisicion.id == formato_id).first()


def get_formato_requisicion_by_codigo(db: Session, codigo: str) -> Optional[FormatoRequisicion]:
    """Get a requisition form by code"""
    return db.query(FormatoRequisicion).filter(FormatoRequisicion.codigo == codigo).first()


def get_formatos_requisicion(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[FormatoRequisicion]:
    """Get list of requisition forms, optionally filtered"""
    query = db.query(FormatoRequisicion)
    
    if activo is not None:
        query = query.filter(FormatoRequisicion.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_formato_requisicion(db: Session, formato_id: UUID, formato_data: FormatoRequisicionUpdate) -> Optional[FormatoRequisicion]:
    """Update a requisition form"""
    db_formato = get_formato_requisicion(db, formato_id)
    if db_formato:
        update_data = formato_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_formato, field, value)
        db.commit()
        db.refresh(db_formato)
    return db_formato


def delete_formato_requisicion(db: Session, formato_id: UUID) -> bool:
    """Delete a requisition form"""
    db_formato = get_formato_requisicion(db, formato_id)
    if db_formato:
        db.delete(db_formato)
        db.commit()
        return True
    return False