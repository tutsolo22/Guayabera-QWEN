"""
Invoice CRUD Operations: Electronic invoicing according to Mexican SAT regulations
Integration with Facturama for CFDI issuance
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.invoice import (
    Emisor, Receptor, ComprobanteFiscal, ConceptoFactura, 
    ImpuestoConcepto, ComplementoPago, ComplementoFiscal, 
    CancelacionCFDI, ValidacionRFC
)
from app.schemas.invoice import (
    EmisorCreate, EmisorUpdate,
    ReceptorCreate, ReceptorUpdate,
    ComprobanteFiscalCreate, ComprobanteFiscalUpdate,
    ConceptoFacturaCreate, ConceptoFacturaUpdate,
    ImpuestoConceptoCreate, ImpuestoConceptoUpdate,
    ComplementoPagoCreate, ComplementoPagoUpdate,
    ComplementoFiscalCreate, ComplementoFiscalUpdate,
    CancelacionCFDICreate, CancelacionCFDIUpdate,
    ValidacionRFCCreate, ValidacionRFCUpdate
)


# ============================================================================
# EMITTER CRUD
# ============================================================================

def create_emisor(db: Session, emisor_data: EmisorCreate) -> Emisor:
    """Create a new emitter (issuer)"""
    # Validate RFC format
    rfc = emisor_data.rfc.upper().strip()
    if len(rfc) not in [12, 13]:
        raise ValueError("RFC must have 12 or 13 characters")
    
    # Check if RFC already exists
    existing_emisor = db.query(Emisor).filter(Emisor.rfc == rfc).first()
    if existing_emisor:
        raise ValueError(f"An emitter with RFC {rfc} already exists")
    
    db_emisor = Emisor(**emisor_data.model_dump())
    db_emisor.rfc = rfc
    db.add(db_emisor)
    db.commit()
    db.refresh(db_emisor)
    return db_emisor


def get_emisor(db: Session, emisor_id: UUID) -> Optional[Emisor]:
    """Get an emitter by ID"""
    return db.query(Emisor).filter(Emisor.id == emisor_id).first()


def get_emisor_by_rfc(db: Session, rfc: str) -> Optional[Emisor]:
    """Get an emitter by RFC"""
    return db.query(Emisor).filter(Emisor.rfc == rfc.upper()).first()


def get_emisores(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[Emisor]:
    """Get list of emitters, optionally filtered"""
    query = db.query(Emisor)
    
    if activo is not None:
        query = query.filter(Emisor.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_emisor(db: Session, emisor_id: UUID, emisor_data: EmisorUpdate) -> Optional[Emisor]:
    """Update an emitter"""
    db_emisor = get_emisor(db, emisor_id)
    if db_emisor:
        update_data = emisor_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_emisor, field, value)
        db.commit()
        db.refresh(db_emisor)
    return db_emisor


def delete_emisor(db: Session, emisor_id: UUID) -> bool:
    """Soft delete an emitter"""
    db_emisor = get_emisor(db, emisor_id)
    if db_emisor:
        db_emisor.activo = False
        db_emisor.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# RECEIVER CRUD
# ============================================================================

def create_receptor(db: Session, receptor_data: ReceptorCreate) -> Receptor:
    """Create a new receiver"""
    # Validate RFC format
    rfc = receptor_data.rfc.upper().strip()
    if len(rfc) not in [12, 13]:
        raise ValueError("RFC must have 12 or 13 characters")
    
    # Check if RFC already exists
    existing_receptor = db.query(Receptor).filter(Receptor.rfc == rfc).first()
    if existing_receptor:
        raise ValueError(f"A receiver with RFC {rfc} already exists")
    
    db_receptor = Receptor(**receptor_data.model_dump())
    db_receptor.rfc = rfc
    db.add(db_receptor)
    db.commit()
    db.refresh(db_receptor)
    return db_receptor


def get_receptor(db: Session, receptor_id: UUID) -> Optional[Receptor]:
    """Get a receiver by ID"""
    return db.query(Receptor).filter(Receptor.id == receptor_id).first()


def get_receptor_by_rfc(db: Session, rfc: str) -> Optional[Receptor]:
    """Get a receiver by RFC"""
    return db.query(Receptor).filter(Receptor.rfc == rfc.upper()).first()


def get_receptores(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[Receptor]:
    """Get list of receivers, optionally filtered"""
    query = db.query(Receptor)
    
    if activo is not None:
        query = query.filter(Receptor.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_receptor(db: Session, receptor_id: UUID, receptor_data: ReceptorUpdate) -> Optional[Receptor]:
    """Update a receiver"""
    db_receptor = get_receptor(db, receptor_id)
    if db_receptor:
        update_data = receptor_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_receptor, field, value)
        db.commit()
        db.refresh(db_receptor)
    return db_receptor


def delete_receptor(db: Session, receptor_id: UUID) -> bool:
    """Soft delete a receiver"""
    db_receptor = get_receptor(db, receptor_id)
    if db_receptor:
        db_receptor.activo = False
        db_receptor.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# FISCAL RECEIPT CRUD
# ============================================================================

def create_comprobante_fiscal(db: Session, comprobante_data: ComprobanteFiscalCreate) -> ComprobanteFiscal:
    """Create a new fiscal receipt (CFDI)"""
    # Verify emitter and receiver exist
    emitter = get_emisor(db, comprobante_data.emisor_id)
    if not emitter:
        raise ValueError(f"Emitter with ID {comprobante_data.emisor_id} does not exist")
    
    receiver = get_receptor(db, comprobante_data.receptor_id)
    if not receiver:
        raise ValueError(f"Receiver with ID {comprobante_data.receptor_id} does not exist")
    
    # Check if internal folio already exists
    existing_comprobante = db.query(ComprobanteFiscal).filter(
        ComprobanteFiscal.folio_interno == comprobante_data.folio_interno
    ).first()
    if existing_comprobante:
        raise ValueError(f"A fiscal receipt with internal folio {comprobante_data.folio_interno} already exists")
    
    db_comprobante = ComprobanteFiscal(**comprobante_data.model_dump())
    db.add(db_comprobante)
    db.commit()
    db.refresh(db_comprobante)
    return db_comprobante


def get_comprobante_fiscal(db: Session, comprobante_id: UUID) -> Optional[ComprobanteFiscal]:
    """Get a fiscal receipt by ID"""
    return db.query(ComprobanteFiscal).filter(ComprobanteFiscal.id == comprobante_id).first()


def get_comprobante_fiscal_by_folio_interno(db: Session, folio_interno: str) -> Optional[ComprobanteFiscal]:
    """Get a fiscal receipt by internal folio"""
    return db.query(ComprobanteFiscal).filter(ComprobanteFiscal.folio_interno == folio_interno).first()


def get_comprobante_fiscal_by_folio_fiscal(db: Session, folio_fiscal: str) -> Optional[ComprobanteFiscal]:
    """Get a fiscal receipt by fiscal folio (UUID)"""
    return db.query(ComprobanteFiscal).filter(ComprobanteFiscal.folio_fiscal == folio_fiscal).first()


def get_comprobantes_fiscales(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    tipo_comprobante: Optional[str] = None,
    emisor_id: Optional[UUID] = None,
    receptor_id: Optional[UUID] = None
) -> List[ComprobanteFiscal]:
    """Get list of fiscal receipts, optionally filtered"""
    query = db.query(ComprobanteFiscal)
    
    if estado:
        query = query.filter(ComprobanteFiscal.estado == estado)
    if tipo_comprobante:
        query = query.filter(ComprobanteFiscal.tipo_comprobante == tipo_comprobante)
    if emisor_id:
        query = query.filter(ComprobanteFiscal.emisor_id == emisor_id)
    if receptor_id:
        query = query.filter(ComprobanteFiscal.receptor_id == receptor_id)
    
    return query.offset(skip).limit(limit).all()


def update_comprobante_fiscal(
    db: Session, 
    comprobante_id: UUID, 
    comprobante_data: ComprobanteFiscalUpdate
) -> Optional[ComprobanteFiscal]:
    """Update a fiscal receipt"""
    db_comprobante = get_comprobante_fiscal(db, comprobante_id)
    if db_comprobante:
        update_data = comprobante_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comprobante, field, value)
        db.commit()
        db.refresh(db_comprobante)
    return db_comprobante


def delete_comprobante_fiscal(db: Session, comprobante_id: UUID) -> bool:
    """Soft delete a fiscal receipt"""
    db_comprobante = get_comprobante_fiscal(db, comprobante_id)
    if db_comprobante:
        db_comprobante.estado = "cancelado"
        db_comprobante.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# INVOICE CONCEPT CRUD
# ============================================================================

def create_concepto_factura(db: Session, concepto_data: ConceptoFacturaCreate) -> ConceptoFactura:
    """Create a new invoice concept"""
    # Verify the comprobante exists
    comprobante = get_comprobante_fiscal(db, concepto_data.comprobante_id)
    if not comprobante:
        raise ValueError(f"Comprobante with ID {concepto_data.comprobante_id} does not exist")
    
    db_concepto = ConceptoFactura(**concepto_data.model_dump())
    db.add(db_concepto)
    db.commit()
    db.refresh(db_concepto)
    return db_concepto


def get_concepto_factura(db: Session, concepto_id: UUID) -> Optional[ConceptoFactura]:
    """Get an invoice concept by ID"""
    return db.query(ConceptoFactura).filter(ConceptoFactura.id == concepto_id).first()


def get_conceptos_by_comprobante(db: Session, comprobante_id: UUID) -> List[ConceptoFactura]:
    """Get all concepts for a specific fiscal receipt"""
    return db.query(ConceptoFactura).filter(
        ConceptoFactura.comprobante_id == comprobante_id
    ).all()


def update_concepto_factura(
    db: Session, 
    concepto_id: UUID, 
    concepto_data: ConceptoFacturaUpdate
) -> Optional[ConceptoFactura]:
    """Update an invoice concept"""
    db_concepto = get_concepto_factura(db, concepto_id)
    if db_concepto:
        update_data = concepto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_concepto, field, value)
        db.commit()
        db.refresh(db_concepto)
    return db_concepto


def delete_concepto_factura(db: Session, concepto_id: UUID) -> bool:
    """Soft delete an invoice concept"""
    db_concepto = get_concepto_factura(db, concepto_id)
    if db_concepto:
        db_concepto.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# TAX CONCEPT CRUD
# ============================================================================

def create_impuesto_concepto(db: Session, impuesto_data: ImpuestoConceptoCreate) -> ImpuestoConcepto:
    """Create a new tax concept"""
    # Verify the concept exists
    concepto = get_concepto_factura(db, impuesto_data.concepto_id)
    if not concepto:
        raise ValueError(f"Concept with ID {impuesto_data.concepto_id} does not exist")
    
    db_impuesto = ImpuestoConcepto(**impuesto_data.model_dump())
    db.add(db_impuesto)
    db.commit()
    db.refresh(db_impuesto)
    return db_impuesto


def get_impuesto_concepto(db: Session, impuesto_id: UUID) -> Optional[ImpuestoConcepto]:
    """Get a tax concept by ID"""
    return db.query(ImpuestoConcepto).filter(ImpuestoConcepto.id == impuesto_id).first()


def get_impuestos_by_concepto(db: Session, concepto_id: UUID) -> List[ImpuestoConcepto]:
    """Get all taxes for a specific concept"""
    return db.query(ImpuestoConcepto).filter(
        ImpuestoConcepto.concepto_id == concepto_id
    ).all()


def update_impuesto_concepto(
    db: Session, 
    impuesto_id: UUID, 
    impuesto_data: ImpuestoConceptoUpdate
) -> Optional[ImpuestoConcepto]:
    """Update a tax concept"""
    db_impuesto = get_impuesto_concepto(db, impuesto_id)
    if db_impuesto:
        update_data = impuesto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_impuesto, field, value)
        db.commit()
        db.refresh(db_impuesto)
    return db_impuesto


def delete_impuesto_concepto(db: Session, impuesto_id: UUID) -> bool:
    """Delete a tax concept"""
    db_impuesto = get_impuesto_concepto(db, impuesto_id)
    if db_impuesto:
        db.delete(db_impuesto)
        db.commit()
        return True
    return False


# ============================================================================
# PAYMENT COMPLEMENT CRUD
# ============================================================================

def create_complemento_pago(db: Session, complemento_data: ComplementoPagoCreate) -> ComplementoPago:
    """Create a new payment complement"""
    # Verify the comprobante exists
    comprobante = get_comprobante_fiscal(db, complemento_data.comprobante_id)
    if not comprobante:
        raise ValueError(f"Comprobante with ID {complemento_data.comprobante_id} does not exist")
    
    # If there's a related document, verify it exists
    if complemento_data.documento_relacionado_id:
        doc_relacionado = get_comprobante_fiscal(db, complemento_data.documento_relacionado_id)
        if not doc_relacionado:
            raise ValueError(f"Related document with ID {complemento_data.documento_relacionado_id} does not exist")
    
    db_complemento = ComplementoPago(**complemento_data.model_dump())
    db.add(db_complemento)
    db.commit()
    db.refresh(db_complemento)
    return db_complemento


def get_complemento_pago(db: Session, complemento_id: UUID) -> Optional[ComplementoPago]:
    """Get a payment complement by ID"""
    return db.query(ComplementoPago).filter(ComplementoPago.id == complemento_id).first()


def get_complementos_pago_by_comprobante(db: Session, comprobante_id: UUID) -> List[ComplementoPago]:
    """Get all payment complements for a specific fiscal receipt"""
    return db.query(ComplementoPago).filter(
        ComplementoPago.comprobante_id == comprobante_id
    ).all()


def update_complemento_pago(
    db: Session, 
    complemento_id: UUID, 
    complemento_data: ComplementoPagoUpdate
) -> Optional[ComplementoPago]:
    """Update a payment complement"""
    db_complemento = get_complemento_pago(db, complemento_id)
    if db_complemento:
        update_data = complemento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_complemento, field, value)
        db.commit()
        db.refresh(db_complemento)
    return db_complemento


def delete_complemento_pago(db: Session, complemento_id: UUID) -> bool:
    """Delete a payment complement"""
    db_complemento = get_complemento_pago(db, complemento_id)
    if db_complemento:
        db.delete(db_complemento)
        db.commit()
        return True
    return False


# ============================================================================
# FISCAL COMPLEMENT CRUD
# ============================================================================

def create_complemento_fiscal(db: Session, complemento_data: ComplementoFiscalCreate) -> ComplementoFiscal:
    """Create a new fiscal complement"""
    # Verify the comprobante exists
    comprobante = get_comprobante_fiscal(db, complemento_data.comprobante_id)
    if not comprobante:
        raise ValueError(f"Comprobante with ID {complemento_data.comprobante_id} does not exist")
    
    db_complemento = ComplementoFiscal(**complemento_data.model_dump())
    db.add(db_complemento)
    db.commit()
    db.refresh(db_complemento)
    return db_complemento


def get_complemento_fiscal(db: Session, complemento_id: UUID) -> Optional[ComplementoFiscal]:
    """Get a fiscal complement by ID"""
    return db.query(ComplementoFiscal).filter(ComplementoFiscal.id == complemento_id).first()


def get_complementos_fiscales_by_comprobante(db: Session, comprobante_id: UUID) -> List[ComplementoFiscal]:
    """Get all fiscal complements for a specific fiscal receipt"""
    return db.query(ComplementoFiscal).filter(
        ComplementoFiscal.comprobante_id == comprobante_id
    ).all()


def update_complemento_fiscal(
    db: Session, 
    complemento_id: UUID, 
    complemento_data: ComplementoFiscalUpdate
) -> Optional[ComplementoFiscal]:
    """Update a fiscal complement"""
    db_complemento = get_complemento_fiscal(db, complemento_id)
    if db_complemento:
        update_data = complemento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_complemento, field, value)
        db.commit()
        db.refresh(db_complemento)
    return db_complemento


def delete_complemento_fiscal(db: Session, complemento_id: UUID) -> bool:
    """Delete a fiscal complement"""
    db_complemento = get_complemento_fiscal(db, complemento_id)
    if db_complemento:
        db_complemento.activo = False
        db.commit()
        return True
    return False


# ============================================================================
# CFDI CANCELLATION CRUD
# ============================================================================

def create_cancelacion_cfdi(db: Session, cancelacion_data: CancelacionCFDICreate) -> CancelacionCFDI:
    """Create a new CFDI cancellation record"""
    # Verify the comprobante exists
    comprobante = get_comprobante_fiscal(db, cancelacion_data.comprobante_id)
    if not comprobante:
        raise ValueError(f"Comprobante with ID {cancelacion_data.comprobante_id} does not exist")
    
    db_cancelacion = CancelacionCFDI(**cancelacion_data.model_dump())
    db.add(db_cancelacion)
    db.commit()
    db.refresh(db_cancelacion)
    return db_cancelacion


def get_cancelacion_cfdi(db: Session, cancelacion_id: UUID) -> Optional[CancelacionCFDI]:
    """Get a CFDI cancellation record by ID"""
    return db.query(CancelacionCFDI).filter(CancelacionCFDI.id == cancelacion_id).first()


def get_cancelaciones_by_comprobante(db: Session, comprobante_id: UUID) -> List[CancelacionCFDI]:
    """Get all cancellation records for a specific fiscal receipt"""
    return db.query(CancelacionCFDI).filter(
        CancelacionCFDI.comprobante_id == comprobante_id
    ).all()


def update_cancelacion_cfdi(
    db: Session, 
    cancelacion_id: UUID, 
    cancelacion_data: CancelacionCFDIUpdate
) -> Optional[CancelacionCFDI]:
    """Update a CFDI cancellation record"""
    db_cancelacion = get_cancelacion_cfdi(db, cancelacion_id)
    if db_cancelacion:
        update_data = cancelacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cancelacion, field, value)
        db.commit()
        db.refresh(db_cancelacion)
    return db_cancelacion


def delete_cancelacion_cfdi(db: Session, cancelacion_id: UUID) -> bool:
    """Delete a CFDI cancellation record"""
    db_cancelacion = get_cancelacion_cfdi(db, cancelacion_id)
    if db_cancelacion:
        db.delete(db_cancelacion)
        db.commit()
        return True
    return False


# ============================================================================
# RFC VALIDATION CRUD
# ============================================================================

def create_validacion_rfc(db: Session, validacion_data: ValidacionRFCCreate) -> ValidacionRFC:
    """Create a new RFC validation record"""
    # Check if RFC validation already exists
    existing_validation = db.query(ValidacionRFC).filter(
        ValidacionRFC.rfc == validacion_data.rfc.upper()
    ).first()
    if existing_validation:
        # Update existing validation
        update_data = validacion_data.model_dump()
        for field, value in update_data.items():
            setattr(existing_validation, field, value)
        db.commit()
        db.refresh(existing_validation)
        return existing_validation
    
    db_validacion = ValidacionRFC(**validacion_data.model_dump())
    db_validacion.rfc = db_validacion.rfc.upper()
    db.add(db_validacion)
    db.commit()
    db.refresh(db_validacion)
    return db_validacion


def get_validacion_rfc(db: Session, rfc: str) -> Optional[ValidacionRFC]:
    """Get an RFC validation by RFC"""
    return db.query(ValidacionRFC).filter(ValidacionRFC.rfc == rfc.upper()).first()


def get_validaciones_rfc(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    en_lista_negra: Optional[bool] = None
) -> List[ValidacionRFC]:
    """Get list of RFC validations, optionally filtered"""
    query = db.query(ValidacionRFC)
    
    if en_lista_negra is not None:
        query = query.filter(ValidacionRFC.en_lista_negra == en_lista_negra)
    
    return query.offset(skip).limit(limit).all()


def update_validacion_rfc(
    db: Session, 
    rfc: str, 
    validacion_data: ValidacionRFCUpdate
) -> Optional[ValidacionRFC]:
    """Update an RFC validation"""
    db_validacion = get_validacion_rfc(db, rfc)
    if db_validacion:
        update_data = validacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_validacion, field, value)
        db.commit()
        db.refresh(db_validacion)
    return db_validacion