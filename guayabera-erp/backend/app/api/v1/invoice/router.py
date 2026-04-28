"""
Invoice API Router: Electronic invoicing according to Mexican SAT regulations
Integration with Facturama for CFDI issuance
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID as UUIDType

from app.core.config import settings
from app.core.database import get_db
from app.services.facturama_service import FacturamaService, CfdiData
from app.schemas.invoice import (
    EmisorCreate, EmisorUpdate, EmisorResponse,
    ReceptorCreate, ReceptorUpdate, ReceptorResponse,
    ComprobanteFiscalCreate, ComprobanteFiscalUpdate, ComprobanteFiscalResponse,
    ConceptoFacturaCreate, ConceptoFacturaUpdate, ConceptoFacturaResponse,
    ImpuestoConceptoCreate, ImpuestoConceptoUpdate, ImpuestoConceptoResponse,
    ComplementoPagoCreate, ComplementoPagoUpdate, ComplementoPagoResponse,
    ComplementoFiscalCreate, ComplementoFiscalUpdate, ComplementoFiscalResponse,
    CancelacionCFDICreate, CancelacionCFDIUpdate, CancelacionCFDIResponse,
    ValidacionRFCCreate, ValidacionRFCUpdate, ValidacionRFCResponse,
    InvoiceRequest
)
from app.crud.invoice import (
    create_emisor, get_emisor, get_emisor_by_rfc, get_emisores, update_emisor, delete_emisor,
    create_receptor, get_receptor, get_receptor_by_rfc, get_receptores, update_receptor, delete_receptor,
    create_comprobante_fiscal, get_comprobante_fiscal, get_comprobante_fiscal_by_folio_interno,
    get_comprobante_fiscal_by_folio_fiscal, get_comprobantes_fiscales, update_comprobante_fiscal,
    delete_comprobante_fiscal,
    create_concepto_factura, get_concepto_factura, get_conceptos_by_comprobante,
    update_concepto_factura, delete_concepto_factura,
    create_impuesto_concepto, get_impuesto_concepto, get_impuestos_by_concepto,
    update_impuesto_concepto, delete_impuesto_concepto,
    create_complemento_pago, get_complemento_pago, get_complementos_pago_by_comprobante,
    update_complemento_pago, delete_complemento_pago,
    create_complemento_fiscal, get_complemento_fiscal, get_complementos_fiscales_by_comprobante,
    update_complemento_fiscal, delete_complemento_fiscal,
    create_cancelacion_cfdi, get_cancelacion_cfdi, get_cancelaciones_by_comprobante,
    update_cancelacion_cfdi, delete_cancelacion_cfdi,
    create_validacion_rfc, get_validacion_rfc, get_validaciones_rfc, update_validacion_rfc
)

router = APIRouter(prefix="/invoices", tags=["Electronic Invoicing"])

# Configuration for Facturama service (now using environment variables)
FACTURAMA_API_KEY = ""
FACTURAMA_EMAIL = ""
USE_PRODUCTION = False  # Change to True for production

# Validate that required environment variables are set
if not FACTURAMA_API_KEY or not FACTURAMA_EMAIL:
    print("⚠️ Warning: Facturama API credentials not configured in environment variables")


def stamp_invoice_with_facturama(comprobante_id: str, db: Session):
    """
    Background task to stamp an invoice with Facturama
    """
    try:
        # Initialize Facturama service
        facturama = FacturamaService(
            api_key=FACTURAMA_API_KEY,
            api_login=FACTURAMA_EMAIL,
            is_production=USE_PRODUCTION
        )

        # Get the fiscal receipt from DB
        comprobante = get_comprobante_fiscal(db, UUIDType(comprobante_id))
        if not comprobante:
            raise ValueError(f"Comprobante with ID {comprobante_id} not found")

        # Prepare CFDI data from the comprobante
        # This would involve mapping the database fields to Facturama's expected format
        # For now, we'll use placeholder data
        cfdi_data = CfdiData(
            Rfc=comprobante.receptor.rfc,
            RazonSocial=comprobante.receptor.nombre_o_razon_social,
            CfdiType=comprobante.tipo_comprobante,
            PaymentForm=comprobante.forma_pago,
            PaymentMethod=comprobante.metodo_pago,
            ExpeditionPlace=comprobante.emisor.codigo_postal or "78238",  # Default to San Luis Potosí if not specified
            Receiver={
                "Rfc": comprobante.receptor.rfc,
                "Name": comprobante.receptor.nombre_o_razon_social,
                "CfdiUsage": comprobante.uso_cfdi
            },
            Items=[]
        )

        # Add items to the invoice
        conceptos = get_conceptos_by_comprobante(db, UUIDType(comprobante_id))
        for concepto in conceptos:
            item = {
                "ProductCode": concepto.clave_producto,
                "IdentificationNumber": concepto.no_identificacion or "",
                "Description": concepto.descripcion,
                "Unit": concepto.unidad_medida,
                "UnitCode": concepto.clave_unidad,
                "Quantity": float(concepto.cantidad),
                "Price": float(concepto.valor_unitario),
                "Subtotal": float(concepto.importe),
                "TaxObject": concepto.objeto_imp,
                "Taxes": []
            }

            # Add taxes to the item
            impuestos = get_impuestos_by_concepto(db, concepto.id)
            for impuesto in impuestos:
                item["Taxes"].append({
                    "Total": float(impuesto.importe),
                    "Name": impuesto.nombre,
                    "Base": float(concepto.importe),
                    "Rate": float(impuesto.tasa_cuota) if impuesto.tasa_cuota else 0.0,
                    "Type": "Tasa" if impuesto.tipo == "Traslado" else "Cuota",
                    "IsRetention": impuesto.tipo == "Retencion"
                })

            # Calculate total for the item considering taxes
            total = float(concepto.importe)
            for impuesto in impuestos:
                if impuesto.tipo == "Traslado":
                    total += float(impuesto.importe)
                elif impuesto.tipo == "Retencion":
                    total -= float(impuesto.importe)
            
            item["Total"] = total
            cfdi_data.Items.append(item)

        # Create invoice via Facturama
        result = facturama.create_invoice(cfdi_data)

        # Update the comprobante in DB with the returned data
        comprobante.folio_fiscal = result.get('Id')
        comprobante.facturama_id = result.get('Id')
        comprobante.estatus_facturama = result.get('Status', 'success')
        comprobante.estado = 'activo'
        comprobante.fecha_certificacion = result.get('Date')

        # Save the XML and PDF files
        try:
            xml_content = facturama.get_invoice_xml(result['Id'])
            pdf_content = facturama.get_invoice_pdf(result['Id'])

            # Store files in the appropriate location
            import os
            from datetime import datetime
            folder_path = f"static/invoices/{datetime.now().strftime('%Y/%m')}"
            os.makedirs(folder_path, exist_ok=True)

            xml_filename = f"{folder_path}/{result['Id']}.xml"
            pdf_filename = f"{folder_path}/{result['Id']}.pdf"

            with open(xml_filename, 'wb') as f:
                f.write(xml_content)
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_content)

            comprobante.ruta_xml = xml_filename
            comprobante.ruta_pdf = pdf_filename
        except Exception as e:
            print(f"Error downloading invoice files: {str(e)}")

        # Commit changes to the database
        db.commit()

    except Exception as e:
        print(f"Error stamping invoice {comprobante_id}: {str(e)}")
        # Here you might want to update the comprobante status to reflect the error
        comprobante = get_comprobante_fiscal(db, UUIDType(comprobante_id))
        if comprobante:
            comprobante.estado = 'error_timbrado'
            comprobante.estatus_facturama = f'Error: {str(e)}'
            db.commit()


# ============================================================================
# EMITTER ENDPOINTS
# ============================================================================

@router.post("/emitters/", response_model=EmisorResponse)
def create_emitter(emisor: EmisorCreate, db: Session = Depends(get_db)):
    """Create a new emitter (issuer)"""
    try:
        return create_emisor(db=db, emisor_data=emisor)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/emitters/{emisor_id}", response_model=EmisorResponse)
def get_emitter_by_id(emisor_id: str, db: Session = Depends(get_db)):
    """Get an emitter by ID"""
    emisor = get_emisor(db, UUIDType(emisor_id))
    if not emisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emitter not found"
        )
    return emisor


@router.get("/emitters/rfc/{rfc}", response_model=EmisorResponse)
def get_emitter_by_rfc(rfc: str, db: Session = Depends(get_db)):
    """Get an emitter by RFC"""
    emisor = get_emisor_by_rfc(db, rfc)
    if not emisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emitter not found"
        )
    return emisor


@router.get("/emitters/", response_model=List[EmisorResponse])
def get_emitters(
    skip: int = 0, 
    limit: int = 100, 
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of emitters, optionally filtered"""
    return get_emisores(db, skip, limit, activo)


@router.put("/emitters/{emisor_id}", response_model=EmisorResponse)
def update_emitter(
    emisor_id: str, 
    emisor_data: EmisorUpdate, 
    db: Session = Depends(get_db)
):
    """Update an emitter"""
    updated_emisor = update_emisor(
        db=db, 
        emisor_id=UUIDType(emisor_id), 
        emisor_data=emisor_data
    )
    if not updated_emisor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emitter not found"
        )
    return updated_emisor


@router.delete("/emitters/{emisor_id}")
def delete_emitter(emisor_id: str, db: Session = Depends(get_db)):
    """Soft delete an emitter"""
    success = delete_emisor(db=db, emisor_id=UUIDType(emisor_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emitter not found"
        )
    return {"message": "Emitter deactivated successfully"}


# ============================================================================
# RECEIVER ENDPOINTS
# ============================================================================

@router.post("/receivers/", response_model=ReceptorResponse)
def create_receiver(receptor: ReceptorCreate, db: Session = Depends(get_db)):
    """Create a new receiver"""
    try:
        return create_receptor(db=db, receptor_data=receptor)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/receivers/{receptor_id}", response_model=ReceptorResponse)
def get_receiver_by_id(receptor_id: str, db: Session = Depends(get_db)):
    """Get a receiver by ID"""
    receptor = get_receptor(db, UUIDType(receptor_id))
    if not receptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    return receptor


@router.get("/receivers/rfc/{rfc}", response_model=ReceptorResponse)
def get_receiver_by_rfc(rfc: str, db: Session = Depends(get_db)):
    """Get a receiver by RFC"""
    receptor = get_receptor_by_rfc(db, rfc)
    if not receptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    return receptor


@router.get("/receivers/", response_model=List[ReceptorResponse])
def get_receivers(
    skip: int = 0, 
    limit: int = 100, 
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of receivers, optionally filtered"""
    return get_receptores(db, skip, limit, activo)


@router.put("/receivers/{receptor_id}", response_model=ReceptorResponse)
def update_receiver(
    receptor_id: str, 
    receptor_data: ReceptorUpdate, 
    db: Session = Depends(get_db)
):
    """Update a receiver"""
    updated_receptor = update_receptor(
        db=db, 
        receptor_id=UUIDType(receptor_id), 
        receptor_data=receptor_data
    )
    if not updated_receptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    return updated_receptor


@router.delete("/receivers/{receptor_id}")
def delete_receiver(receptor_id: str, db: Session = Depends(get_db)):
    """Soft delete a receiver"""
    success = delete_receptor(db=db, receptor_id=UUIDType(receptor_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receiver not found"
        )
    return {"message": "Receiver deactivated successfully"}


# ============================================================================
# FISCAL RECEIPT ENDPOINTS
# ============================================================================

@router.post("/", response_model=ComprobanteFiscalResponse)
def create_fiscal_receipt(
    comprobante: ComprobanteFiscalCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new fiscal receipt (CFDI)"""
    try:
        created_comprobante = create_comprobante_fiscal(db=db, comprobante_data=comprobante)
        
        # Schedule background task to stamp with Facturama if state is pending
        if created_comprobante.estado == "pendiente_timbrado":
            background_tasks.add_task(
                stamp_invoice_with_facturama, 
                str(created_comprobante.id), 
                db
            )
        
        return created_comprobante
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{comprobante_id}", response_model=ComprobanteFiscalResponse)
def get_fiscal_receipt_by_id(comprobante_id: str, db: Session = Depends(get_db)):
    """Get a fiscal receipt by ID"""
    comprobante = get_comprobante_fiscal(db, UUIDType(comprobante_id))
    if not comprobante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal receipt not found"
        )
    return comprobante


@router.get("/internal-folio/{folio_interno}", response_model=ComprobanteFiscalResponse)
def get_fiscal_receipt_by_internal_folio(folio_interno: str, db: Session = Depends(get_db)):
    """Get a fiscal receipt by internal folio"""
    comprobante = get_comprobante_fiscal_by_folio_interno(db, folio_interno)
    if not comprobante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal receipt not found"
        )
    return comprobante


@router.get("/fiscal-folio/{folio_fiscal}", response_model=ComprobanteFiscalResponse)
def get_fiscal_receipt_by_fiscal_folio(folio_fiscal: str, db: Session = Depends(get_db)):
    """Get a fiscal receipt by fiscal folio (UUID)"""
    comprobante = get_comprobante_fiscal_by_folio_fiscal(db, folio_fiscal)
    if not comprobante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal receipt not found"
        )
    return comprobante


@router.get("/", response_model=List[ComprobanteFiscalResponse])
def get_fiscal_receipts(
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    tipo_comprobante: Optional[str] = None,
    emisor_id: Optional[str] = None,
    receptor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of fiscal receipts, optionally filtered"""
    emitter_uuid = UUIDType(emisor_id) if emisor_id else None
    receptor_uuid = UUIDType(receptor_id) if receptor_id else None
    return get_comprobantes_fiscales(
        db, skip, limit, estado, tipo_comprobante, emitter_uuid, receptor_uuid
    )


@router.put("/{comprobante_id}", response_model=ComprobanteFiscalResponse)
def update_fiscal_receipt(
    comprobante_id: str, 
    comprobante_data: ComprobanteFiscalUpdate, 
    db: Session = Depends(get_db)
):
    """Update a fiscal receipt"""
    updated_comprobante = update_comprobante_fiscal(
        db=db, 
        comprobante_id=UUIDType(comprobante_id), 
        comprobante_data=comprobante_data
    )
    if not updated_comprobante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal receipt not found"
        )
    return updated_comprobante


@router.delete("/{comprobante_id}")
def delete_fiscal_receipt(comprobante_id: str, db: Session = Depends(get_db)):
    """Soft delete a fiscal receipt"""
    success = delete_comprobante_fiscal(db=db, comprobante_id=UUIDType(comprobante_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fiscal receipt not found"
        )
    return {"message": "Fiscal receipt cancelled successfully"}


# ============================================================================
# INVOICE CONCEPT ENDPOINTS
# ============================================================================

@router.post("/concepts/", response_model=ConceptoFacturaResponse)
def create_invoice_concept(concepto: ConceptoFacturaCreate, db: Session = Depends(get_db)):
    """Create a new invoice concept"""
    try:
        return create_concepto_factura(db=db, concepto_data=concepto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/concepts/{concepto_id}", response_model=ConceptoFacturaResponse)
def get_invoice_concept_by_id(concepto_id: str, db: Session = Depends(get_db)):
    """Get an invoice concept by ID"""
    concepto = get_concepto_factura(db, UUIDType(concepto_id))
    if not concepto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice concept not found"
        )
    return concepto


@router.get("/receipts/{comprobante_id}/concepts", response_model=List[ConceptoFacturaResponse])
def get_concepts_by_receipt(comprobante_id: str, db: Session = Depends(get_db)):
    """Get all concepts for a specific fiscal receipt"""
    return get_conceptos_by_comprobante(db, UUIDType(comprobante_id))


@router.put("/concepts/{concepto_id}", response_model=ConceptoFacturaResponse)
def update_invoice_concept(
    concepto_id: str, 
    concepto_data: ConceptoFacturaUpdate, 
    db: Session = Depends(get_db)
):
    """Update an invoice concept"""
    updated_concepto = update_concepto_factura(
        db=db, 
        concepto_id=UUIDType(concepto_id), 
        concepto_data=concepto_data
    )
    if not updated_concepto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice concept not found"
        )
    return updated_concepto


@router.delete("/concepts/{concepto_id}")
def delete_invoice_concept(concepto_id: str, db: Session = Depends(get_db)):
    """Soft delete an invoice concept"""
    success = delete_concepto_factura(db=db, concepto_id=UUIDType(concepto_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice concept not found"
        )
    return {"message": "Invoice concept deleted successfully"}


# ============================================================================
# TAX CONCEPT ENDPOINTS
# ============================================================================

@router.post("/tax-concepts/", response_model=ImpuestoConceptoResponse)
def create_tax_concept(impuesto: ImpuestoConceptoCreate, db: Session = Depends(get_db)):
    """Create a new tax concept"""
    try:
        return create_impuesto_concepto(db=db, impuesto_data=impuesto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tax-concepts/{impuesto_id}", response_model=ImpuestoConceptoResponse)
def get_tax_concept_by_id(impuesto_id: str, db: Session = Depends(get_db)):
    """Get a tax concept by ID"""
    impuesto = get_impuesto_concepto(db, UUIDType(impuesto_id))
    if not impuesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax concept not found"
        )
    return impuesto


@router.get("/concepts/{concepto_id}/taxes", response_model=List[ImpuestoConceptoResponse])
def get_taxes_by_concept(concepto_id: str, db: Session = Depends(get_db)):
    """Get all taxes for a specific concept"""
    return get_impuestos_by_concepto(db, UUIDType(concepto_id))


@router.put("/tax-concepts/{impuesto_id}", response_model=ImpuestoConceptoResponse)
def update_tax_concept(
    impuesto_id: str, 
    impuesto_data: ImpuestoConceptoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a tax concept"""
    updated_impuesto = update_impuesto_concepto(
        db=db, 
        impuesto_id=UUIDType(impuesto_id), 
        impuesto_data=impuesto_data
    )
    if not updated_impuesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax concept not found"
        )
    return updated_impuesto


@router.delete("/tax-concepts/{impuesto_id}")
def delete_tax_concept(impuesto_id: str, db: Session = Depends(get_db)):
    """Delete a tax concept"""
    success = delete_impuesto_concepto(db=db, impuesto_id=UUIDType(impuesto_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax concept not found"
        )
    return {"message": "Tax concept deleted successfully"}


# ============================================================================
# PAYMENT COMPLEMENT ENDPOINTS
# ============================================================================

@router.post("/payment-complements/", response_model=ComplementoPagoResponse)
def create_payment_complement(complemento: ComplementoPagoCreate, db: Session = Depends(get_db)):
    """Create a new payment complement"""
    try:
        return create_complemento_pago(db=db, complemento_data=complemento)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/payment-complements/{complemento_id}", response_model=ComplementoPagoResponse)
def get_payment_complement_by_id(complemento_id: str, db: Session = Depends(get_db)):
    """Get a payment complement by ID"""
    complemento = get_complemento_pago(db, UUIDType(complemento_id))
    if not complemento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment complement not found"
        )
    return complemento


@router.get("/receipts/{comprobante_id}/payment-complements", response_model=List[ComplementoPagoResponse])
def get_payment_complements_by_receipt(comprobante_id: str, db: Session = Depends(get_db)):
    """Get all payment complements for a specific fiscal receipt"""
    return get_complementos_pago_by_comprobante(db, UUIDType(comprobante_id))


@router.put("/payment-complements/{complemento_id}", response_model=ComplementoPagoResponse)
def update_payment_complement(
    complemento_id: str, 
    complemento_data: ComplementoPagoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a payment complement"""
    updated_complemento = update_complemento_pago(
        db=db, 
        complemento_id=UUIDType(complemento_id), 
        complemento_data=complemento_data
    )
    if not updated_complemento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment complement not found"
        )
    return updated_complemento


@router.delete("/payment-complements/{complemento_id}")
def delete_payment_complement(complemento_id: str, db: Session = Depends(get_db)):
    """Delete a payment complement"""
    success = delete_complemento_pago(db=db, complemento_id=UUIDType(complemento_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment complement not found"
        )
    return {"message": "Payment complement deleted successfully"}