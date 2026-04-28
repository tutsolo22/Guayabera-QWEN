"""
Payroll API Router: Electronic payroll according to Mexican SAT regulations
Integration with CFDI payroll complement
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID as UUIDType

from app.core.database import get_db
from app.services.facturama_service import FacturamaService, CfdiData
from app.schemas.payroll import (
    PeriodoNominaCreate, PeriodoNominaUpdate, PeriodoNominaResponse,
    NominaCreate, NominaUpdate, NominaResponse,
    PercepcionCreate, PercepcionUpdate, PercepcionResponse,
    DeduccionCreate, DeduccionUpdate, DeduccionResponse,
    IncapacidadCreate, IncapacidadUpdate, IncapacidadResponse,
    OtroPagoCreate, OtroPagoUpdate, OtroPagoResponse
)
from app.crud.payroll import (
    create_periodo_nomina, get_periodo_nomina, get_periodo_nomina_by_codigo,
    get_periodos_nomina, update_periodo_nomina, delete_periodo_nomina,
    create_nomina, get_nomina, get_nomina_by_folio, get_nominas_by_periodo,
    get_nominas_by_empleado, update_nomina, delete_nomina,
    create_percepcion, get_percepcion, get_percepciones_by_nomina,
    update_percepcion, delete_percepcion,
    create_deduccion, get_deduccion, get_deducciones_by_nomina,
    update_deduccion, delete_deduccion,
    create_incapacidad, get_incapacidad, get_incapacidades_by_nomina,
    update_incapacidad, delete_incapacidad,
    create_otro_pago, get_otro_pago, get_otros_pagos_by_nomina,
    update_otro_pago, delete_otro_pago
)

router = APIRouter(prefix="/payroll", tags=["Electronic Payroll"])

# Configuration for Facturama service (now using environment variables)
FACTURAMA_API_KEY = ""
FACTURAMA_EMAIL = ""
USE_PRODUCTION = False  # Change to True for production


def stamp_payroll_with_facturama(nomina_id: str, db: Session):
    """
    Background task to stamp a payroll receipt with Facturama
    """
    try:
        # Initialize Facturama service
        facturama = FacturamaService(
            api_key=FACTURAMA_API_KEY,
            api_login=FACTURAMA_EMAIL,
            is_production=USE_PRODUCTION
        )

        # Get the payroll receipt from DB
        nomina = get_nomina(db, UUIDType(nomina_id))
        if not nomina:
            raise ValueError(f"Payroll receipt with ID {nomina_id} not found")

        # Prepare CFDI payroll data from the nomina
        # This is a simplified representation - in reality, payroll CFDI requires more detailed data
        cfdi_data = CfdiData(
            Rfc=nomina.empleado.rfc,  # Employee's RFC
            RazonSocial=nomina.empleado.nombre + " " + nomina.empleado.apellido_paterno + " " + nomina.empleado.apellido_materno,
            CfdiType="N",  # Nómina
            PaymentForm="99",  # Por definir (for payroll)
            PaymentMethod="PUE",  # Pago en una sola exhibición
            ExpeditionPlace=nomina.empleado.empresa.codigo_postal or "78238",  # From company's postal code
            Receiver={
                "Rfc": nomina.empleado.rfc,
                "Name": nomina.empleado.nombre + " " + nomina.empleado.apellido_paterno + " " + nomina.empleado.apellido_materno,
                "CfdiUsage": "P01"  # Por definir (for payroll)
            },
            Items=[]  # Payroll CFDI doesn't typically use standard items
        )

        # For payroll CFDI, we would need to format the data differently
        # This is a simplified approach - real implementation would require more detailed mapping
        # to Facturama's payroll CFDI format

        # Create payroll invoice via Facturama
        result = facturama.create_invoice(cfdi_data)

        # Update the payroll receipt in DB with the returned data
        nomina.folio_fiscal = result.get('Id')
        nomina.facturama_id = result.get('Id')
        nomina.estatus_facturama = result.get('Status', 'success')
        nomina.estado = 'activo'
        nomina.fecha_certificacion = result.get('Date')

        # Save the XML and PDF files
        try:
            xml_content = facturama.get_invoice_xml(result['Id'])
            pdf_content = facturama.get_invoice_pdf(result['Id'])

            # Store files in the appropriate location
            import os
            from datetime import datetime
            folder_path = f"static/payroll/{datetime.now().strftime('%Y/%m')}"
            os.makedirs(folder_path, exist_ok=True)

            xml_filename = f"{folder_path}/{result['Id']}.xml"
            pdf_filename = f"{folder_path}/{result['Id']}.pdf"

            with open(xml_filename, 'wb') as f:
                f.write(xml_content)
            with open(pdf_filename, 'wb') as f:
                f.write(pdf_content)

            nomina.ruta_xml = xml_filename
            nomina.ruta_pdf = pdf_filename
        except Exception as e:
            print(f"Error downloading payroll files: {str(e)}")

        # Commit changes to the database
        db.commit()

    except Exception as e:
        print(f"Error stamping payroll receipt {nomina_id}: {str(e)}")
        # Here you might want to update the nomina status to reflect the error
        nomina = get_nomina(db, UUIDType(nomina_id))
        if nomina:
            nomina.estado = 'error_timbrado'
            nomina.estatus_facturama = f'Error: {str(e)}'
            db.commit()


# ============================================================================
# PAYROLL PERIOD ENDPOINTS
# ============================================================================

@router.post("/periods/", response_model=PeriodoNominaResponse)
def create_payroll_period(
    periodo: PeriodoNominaCreate,
    db: Session = Depends(get_db)
):
    """Create a new payroll period"""
    try:
        return create_periodo_nomina(db=db, periodo_data=periodo)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/periods/{periodo_id}", response_model=PeriodoNominaResponse)
def get_payroll_period_by_id(periodo_id: str, db: Session = Depends(get_db)):
    """Get a payroll period by ID"""
    periodo = get_periodo_nomina(db, UUIDType(periodo_id))
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return periodo


@router.get("/periods/code/{codigo}", response_model=PeriodoNominaResponse)
def get_payroll_period_by_codigo(codigo: str, db: Session = Depends(get_db)):
    """Get a payroll period by code"""
    periodo = get_periodo_nomina_by_codigo(db, codigo)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return periodo


@router.get("/periods/", response_model=List[PeriodoNominaResponse])
def get_payroll_periods(
    skip: int = 0,
    limit: int = 100,
    empresa_id: Optional[str] = None,
    cerrado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of payroll periods, optionally filtered"""
    empresa_uuid = UUIDType(empresa_id) if empresa_id else None
    return get_periodos_nomina(db, skip, limit, empresa_uuid, cerrado)


@router.put("/periods/{periodo_id}", response_model=PeriodoNominaResponse)
def update_payroll_period(
    periodo_id: str,
    periodo_data: PeriodoNominaUpdate,
    db: Session = Depends(get_db)
):
    """Update a payroll period"""
    updated_periodo = update_periodo_nomina(
        db=db,
        periodo_id=UUIDType(periodo_id),
        periodo_data=periodo_data
    )
    if not updated_periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return updated_periodo


@router.delete("/periods/{periodo_id}")
def delete_payroll_period(periodo_id: str, db: Session = Depends(get_db)):
    """Delete a payroll period"""
    success = delete_periodo_nomina(db=db, periodo_id=UUIDType(periodo_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return {"message": "Payroll period deleted successfully"}


# ============================================================================
# PAYROLL RECEIPT ENDPOINTS
# ============================================================================

@router.post("/", response_model=NominaResponse)
def create_payroll_receipt(
    nomina: NominaCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new payroll receipt"""
    try:
        created_nomina = create_nomina(db=db, nomina_data=nomina)
        
        # Schedule background task to stamp with Facturama if state is pending
        if created_nomina.estado == "pendiente_timbrado":
            background_tasks.add_task(
                stamp_payroll_with_facturama,
                str(created_nomina.id),
                db
            )
        
        return created_nomina
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{nomina_id}", response_model=NominaResponse)
def get_payroll_receipt_by_id(nomina_id: str, db: Session = Depends(get_db)):
    """Get a payroll receipt by ID"""
    nomina = get_nomina(db, UUIDType(nomina_id))
    if not nomina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll receipt not found"
        )
    return nomina


@router.get("/folio/{folio}", response_model=NominaResponse)
def get_payroll_receipt_by_folio(folio: str, db: Session = Depends(get_db)):
    """Get a payroll receipt by folio"""
    nomina = get_nomina_by_folio(db, folio)
    if not nomina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll receipt not found"
        )
    return nomina


@router.get("/period/{periodo_id}", response_model=List[NominaResponse])
def get_payroll_receipts_by_period(periodo_id: str, db: Session = Depends(get_db)):
    """Get all payroll receipts for a specific period"""
    return get_nominas_by_periodo(db, UUIDType(periodo_id))


@router.get("/employee/{empleado_id}", response_model=List[NominaResponse])
def get_payroll_receipts_by_employee(
    empleado_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all payroll receipts for a specific employee"""
    return get_nominas_by_empleado(db, UUIDType(empleado_id), skip, limit)


@router.put("/{nomina_id}", response_model=NominaResponse)
def update_payroll_receipt(
    nomina_id: str,
    nomina_data: NominaUpdate,
    db: Session = Depends(get_db)
):
    """Update a payroll receipt"""
    updated_nomina = update_nomina(
        db=db,
        nomina_id=UUIDType(nomina_id),
        nomina_data=nomina_data
    )
    if not updated_nomina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll receipt not found"
        )
    return updated_nomina


@router.delete("/{nomina_id}")
def delete_payroll_receipt(nomina_id: str, db: Session = Depends(get_db)):
    """Delete a payroll receipt"""
    success = delete_nomina(db=db, nomina_id=UUIDType(nomina_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll receipt not found"
        )
    return {"message": "Payroll receipt deleted successfully"}


# ============================================================================
# PERCEPTION ENDPOINTS
# ============================================================================

@router.post("/perceptions/", response_model=PercepcionResponse)
def create_perception(percepcion: PercepcionCreate, db: Session = Depends(get_db)):
    """Create a new payroll perception"""
    try:
        return create_percepcion(db=db, percepcion_data=percepcion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/perceptions/{percepcion_id}", response_model=PercepcionResponse)
def get_perception_by_id(percepcion_id: str, db: Session = Depends(get_db)):
    """Get a payroll perception by ID"""
    percepcion = get_percepcion(db, UUIDType(percepcion_id))
    if not percepcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll perception not found"
        )
    return percepcion


@router.get("/nominas/{nomina_id}/perceptions", response_model=List[PercepcionResponse])
def get_perceptions_by_nomina(nomina_id: str, db: Session = Depends(get_db)):
    """Get all perceptions for a specific payroll receipt"""
    return get_percepciones_by_nomina(db, UUIDType(nomina_id))


@router.put("/perceptions/{percepcion_id}", response_model=PercepcionResponse)
def update_perception(
    percepcion_id: str,
    percepcion_data: PercepcionUpdate,
    db: Session = Depends(get_db)
):
    """Update a payroll perception"""
    updated_percepcion = update_percepcion(
        db=db,
        percepcion_id=UUIDType(percepcion_id),
        percepcion_data=percepcion_data
    )
    if not updated_percepcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll perception not found"
        )
    return updated_percepcion


@router.delete("/perceptions/{percepcion_id}")
def delete_perception(percepcion_id: str, db: Session = Depends(get_db)):
    """Delete a payroll perception"""
    success = delete_percepcion(db=db, percepcion_id=UUIDType(percepcion_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll perception not found"
        )
    return {"message": "Payroll perception deleted successfully"}


# ============================================================================
# DEDUCTION ENDPOINTS
# ============================================================================

@router.post("/deductions/", response_model=DeduccionResponse)
def create_deduction(deduccion: DeduccionCreate, db: Session = Depends(get_db)):
    """Create a new payroll deduction"""
    try:
        return create_deduccion(db=db, deduccion_data=deduccion)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/deductions/{deduccion_id}", response_model=DeduccionResponse)
def get_deduction_by_id(deduccion_id: str, db: Session = Depends(get_db)):
    """Get a payroll deduction by ID"""
    deduccion = get_deduccion(db, UUIDType(deduccion_id))
    if not deduccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll deduction not found"
        )
    return deduccion


@router.get("/nominas/{nomina_id}/deductions", response_model=List[DeduccionResponse])
def get_deductions_by_nomina(nomina_id: str, db: Session = Depends(get_db)):
    """Get all deductions for a specific payroll receipt"""
    return get_deducciones_by_nomina(db, UUIDType(nomina_id))


@router.put("/deductions/{deduccion_id}", response_model=DeduccionResponse)
def update_deduction(
    deduccion_id: str,
    deduccion_data: DeduccionUpdate,
    db: Session = Depends(get_db)
):
    """Update a payroll deduction"""
    updated_deduccion = update_deduccion(
        db=db,
        deduccion_id=UUIDType(deduccion_id),
        deduccion_data=deduccion_data
    )
    if not updated_deduccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll deduction not found"
        )
    return updated_deduccion


@router.delete("/deductions/{deduccion_id}")
def delete_deduction(deduccion_id: str, db: Session = Depends(get_db)):
    """Delete a payroll deduction"""
    success = delete_deduccion(db=db, deduccion_id=UUIDType(deduccion_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll deduction not found"
        )
    return {"message": "Payroll deduction deleted successfully"}


# ============================================================================
# INCAPACITY ENDPOINTS
# ============================================================================

@router.post("/incapacities/", response_model=IncapacidadResponse)
def create_incapacity(incapacidad: IncapacidadCreate, db: Session = Depends(get_db)):
    """Create a new employee incapacity"""
    try:
        return create_incapacidad(db=db, incapacidad_data=incapacidad)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/incapacities/{incapacidad_id}", response_model=IncapacidadResponse)
def get_incapacity_by_id(incapacidad_id: str, db: Session = Depends(get_db)):
    """Get an employee incapacity by ID"""
    incapacidad = get_incapacidad(db, UUIDType(incapacidad_id))
    if not incapacidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee incapacity not found"
        )
    return incapacidad


@router.get("/nominas/{nomina_id}/incapacities", response_model=List[IncapacidadResponse])
def get_incapacities_by_nomina(nomina_id: str, db: Session = Depends(get_db)):
    """Get all incapacities for a specific payroll receipt"""
    return get_incapacidades_by_nomina(db, UUIDType(nomina_id))


@router.put("/incapacities/{incapacidad_id}", response_model=IncapacidadResponse)
def update_incapacity(
    incapacidad_id: str,
    incapacidad_data: IncapacidadUpdate,
    db: Session = Depends(get_db)
):
    """Update an employee incapacity"""
    updated_incapacidad = update_incapacidad(
        db=db,
        incapacidad_id=UUIDType(incapacidad_id),
        incapacidad_data=incapacidad_data
    )
    if not updated_incapacidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee incapacity not found"
        )
    return updated_incapacidad


@router.delete("/incapacities/{incapacidad_id}")
def delete_incapacity(incapacidad_id: str, db: Session = Depends(get_db)):
    """Delete an employee incapacity"""
    success = delete_incapacidad(db=db, incapacidad_id=UUIDType(incapacidad_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee incapacity not found"
        )
    return {"message": "Employee incapacity deleted successfully"}


# ============================================================================
# OTHER PAYMENT ENDPOINTS
# ============================================================================

@router.post("/other-payments/", response_model=OtroPagoResponse)
def create_other_payment(otro_pago: OtroPagoCreate, db: Session = Depends(get_db)):
    """Create a new other payment"""
    try:
        return create_otro_pago(db=db, otro_pago_data=otro_pago)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/other-payments/{otro_pago_id}", response_model=OtroPagoResponse)
def get_other_payment_by_id(otro_pago_id: str, db: Session = Depends(get_db)):
    """Get an other payment by ID"""
    otro_pago = get_otro_pago(db, UUIDType(otro_pago_id))
    if not otro_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other payment not found"
        )
    return otro_pago


@router.get("/nominas/{nomina_id}/other-payments", response_model=List[OtroPagoResponse])
def get_other_payments_by_nomina(nomina_id: str, db: Session = Depends(get_db)):
    """Get all other payments for a specific payroll receipt"""
    return get_otros_pagos_by_nomina(db, UUIDType(nomina_id))


@router.put("/other-payments/{otro_pago_id}", response_model=OtroPagoResponse)
def update_other_payment(
    otro_pago_id: str,
    otro_pago_data: OtroPagoUpdate,
    db: Session = Depends(get_db)
):
    """Update an other payment"""
    updated_otro_pago = update_otro_pago(
        db=db,
        otro_pago_id=UUIDType(otro_pago_id),
        otro_pago_data=otro_pago_data
    )
    if not updated_otro_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other payment not found"
        )
    return updated_otro_pago


@router.delete("/other-payments/{otro_pago_id}")
def delete_other_payment(otro_pago_id: str, db: Session = Depends(get_db)):
    """Delete an other payment"""
    success = delete_otro_pago(db=db, otro_pago_id=UUIDType(otro_pago_id))
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Other payment not found"
        )
    return {"message": "Other payment deleted successfully"}