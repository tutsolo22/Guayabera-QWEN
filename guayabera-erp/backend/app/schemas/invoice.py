"""
Invoice Schemas: Electronic invoicing according to Mexican SAT regulations
Integration with Facturama for CFDI issuance
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# EMITTER SCHEMAS
# ============================================================================

class EmisorBase(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13, description="RFC del emisor")
    nombre_o_razon_social: str = Field(..., max_length=254, description="Nombre o razón social del emisor")
    regimen_fiscal: str = Field(..., max_length=10, description="Clave del régimen fiscal del emisor")
    calle: Optional[str] = Field(None, max_length=100, description="Calle del domicilio fiscal")
    numero_exterior: Optional[str] = Field(None, max_length=50, description="Número exterior del domicilio fiscal")
    numero_interior: Optional[str] = Field(None, max_length=50, description="Número interior del domicilio fiscal")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia del domicilio fiscal")
    localidad: Optional[str] = Field(None, max_length=100, description="Localidad del domicilio fiscal")
    municipio: Optional[str] = Field(None, max_length=100, description="Municipio del domicilio fiscal")
    estado: Optional[str] = Field(None, max_length=50, description="Estado del domicilio fiscal")
    pais: Optional[str] = Field(default="México", max_length=50, description="País del domicilio fiscal")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal del domicilio fiscal")
    regimen_fiscal_nombre: Optional[str] = Field(None, max_length=150, description="Nombre del régimen fiscal")
    fac_atencion: Optional[str] = Field(None, max_length=50, description="Clave de la fac de atención")
    activo: bool = Field(default=True, description="¿Está activo el emisor?")


class EmisorCreate(EmisorBase):
    pass


class EmisorUpdate(BaseModel):
    nombre_o_razon_social: Optional[str] = Field(None, max_length=254)
    regimen_fiscal: Optional[str] = Field(None, max_length=10)
    calle: Optional[str] = Field(None, max_length=100)
    numero_exterior: Optional[str] = Field(None, max_length=50)
    numero_interior: Optional[str] = Field(None, max_length=50)
    colonia: Optional[str] = Field(None, max_length=100)
    localidad: Optional[str] = Field(None, max_length=100)
    municipio: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    pais: Optional[str] = Field(None, max_length=50)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    regimen_fiscal_nombre: Optional[str] = Field(None, max_length=150)
    fac_atencion: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = None


class EmisorResponse(EmisorBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# RECEIVER SCHEMAS
# ============================================================================

class ReceptorBase(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13, description="RFC del receptor")
    nombre_o_razon_social: str = Field(..., max_length=254, description="Nombre o razón social del receptor")
    calle: Optional[str] = Field(None, max_length=100, description="Calle del domicilio fiscal")
    numero_exterior: Optional[str] = Field(None, max_length=50, description="Número exterior del domicilio fiscal")
    numero_interior: Optional[str] = Field(None, max_length=50, description="Número interior del domicilio fiscal")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia del domicilio fiscal")
    localidad: Optional[str] = Field(None, max_length=100, description="Localidad del domicilio fiscal")
    municipio: Optional[str] = Field(None, max_length=100, description="Municipio del domicilio fiscal")
    estado: Optional[str] = Field(None, max_length=50, description="Estado del domicilio fiscal")
    pais: Optional[str] = Field(default="México", max_length=50, description="País del domicilio fiscal")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal del domicilio fiscal")
    regimen_fiscal: Optional[str] = Field(None, max_length=10, description="Clave del régimen fiscal del receptor")
    uso_cfdi: Optional[str] = Field(default="G01", description="Clave de uso de CFDI")
    cliente_id: Optional[UUID4] = Field(None, description="ID del cliente relacionado")
    activo: bool = Field(default=True, description="¿Está activo el receptor?")


class ReceptorCreate(ReceptorBase):
    pass


class ReceptorUpdate(BaseModel):
    nombre_o_razon_social: Optional[str] = Field(None, max_length=254)
    calle: Optional[str] = Field(None, max_length=100)
    numero_exterior: Optional[str] = Field(None, max_length=50)
    numero_interior: Optional[str] = Field(None, max_length=50)
    colonia: Optional[str] = Field(None, max_length=100)
    localidad: Optional[str] = Field(None, max_length=100)
    municipio: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    pais: Optional[str] = Field(None, max_length=50)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    regimen_fiscal: Optional[str] = Field(None, max_length=10)
    uso_cfdi: Optional[str] = None
    cliente_id: Optional[UUID4] = None
    activo: Optional[bool] = None


class ReceptorResponse(ReceptorBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# FISCAL RECEIPT SCHEMAS
# ============================================================================

class ComprobanteFiscalBase(BaseModel):
    folio_interno: str = Field(..., max_length=50, description="Folio interno del comprobante")
    serie: Optional[str] = Field(default="A", max_length=10, description="Serie del comprobante")
    tipo_comprobante: str = Field(..., description="Tipo de comprobante")
    metodo_pago: str = Field(..., description="Método de pago")
    forma_pago: str = Field(..., description="Forma de pago")
    uso_cfdi: str = Field(..., description="Uso de CFDI")
    subtotal: Decimal = Field(..., description="Subtotal del comprobante")
    descuento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Descuento del comprobante")
    total_impuestos_retenidos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de impuestos retenidos")
    total_impuestos_trasladados: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de impuestos trasladados")
    total: Decimal = Field(..., description="Total del comprobante")
    tipo_relacion: Optional[str] = Field(None, description="Tipo de relación con otros comprobantes")
    emisor_id: UUID4 = Field(..., description="ID del emisor")
    receptor_id: UUID4 = Field(..., description="ID del receptor")
    pedido_venta_id: Optional[UUID4] = Field(None, description="ID del pedido de venta relacionado")
    condiciones_pago: Optional[str] = Field(None, max_length=200, description="Condiciones de pago")
    moneda: Optional[str] = Field(default="MXN", max_length=3, description="Moneda del comprobante")
    tipo_cambio: Optional[Decimal] = Field(default=Decimal('1.000000'), description="Tipo de cambio")
    confirmacion: Optional[str] = Field(None, max_length=6, description="Número de confirmación")
    observaciones: Optional[str] = Field(None, description="Observaciones del comprobante")
    estado: Optional[str] = Field(default="pendiente_timbrado", description="Estado del comprobante")


class ComprobanteFiscalCreate(ComprobanteFiscalBase):
    pass


class ComprobanteFiscalUpdate(BaseModel):
    tipo_relacion: Optional[str] = None
    condiciones_pago: Optional[str] = Field(None, max_length=200)
    moneda: Optional[str] = Field(None, max_length=3)
    tipo_cambio: Optional[Decimal] = None
    confirmacion: Optional[str] = Field(None, max_length=6)
    observaciones: Optional[str] = None
    estado: Optional[str] = None


class ComprobanteFiscalResponse(ComprobanteFiscalBase):
    id: UUID4
    folio_fiscal: Optional[str] = None
    fecha_emision: datetime
    fecha_certificacion: Optional[datetime] = None
    uuid_relacionados: Optional[str] = None
    facturama_id: Optional[str] = None
    estatus_facturama: Optional[str] = None
    estatus_sat: Optional[str] = None
    cadena_original: Optional[str] = None
    sello_digital: Optional[str] = None
    sello_sat: Optional[str] = None
    no_certificado: Optional[str] = None
    no_certificado_sat: Optional[str] = None
    ruta_pdf: Optional[str] = None
    ruta_xml: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVOICE CONCEPT SCHEMAS
# ============================================================================

class ConceptoFacturaBase(BaseModel):
    comprobante_id: UUID4
    clave_producto: str = Field(..., max_length=10, description="Clave del producto según catálogo SAT")
    clave_unidad: Optional[str] = Field(default="H87", max_length=10, description="Clave de la unidad de medida")
    no_identificacion: Optional[str] = Field(None, max_length=100, description="Número de identificación del producto")
    descripcion: str = Field(..., description="Descripción del concepto")
    cantidad: Decimal = Field(..., description="Cantidad del concepto")
    unidad_medida: Optional[str] = Field(default="Pieza", max_length=50, description="Unidad de medida")
    valor_unitario: Decimal = Field(..., description="Valor unitario del concepto")
    importe: Decimal = Field(..., description="Importe del concepto")
    descuento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Descuento del concepto")
    objeto_imp: Optional[str] = Field(default="02", max_length=2, description="Objeto de impuesto")
    producto_id: Optional[UUID4] = Field(None, description="ID del producto relacionado")


class ConceptoFacturaCreate(ConceptoFacturaBase):
    pass


class ConceptoFacturaUpdate(BaseModel):
    clave_producto: Optional[str] = Field(None, max_length=10)
    clave_unidad: Optional[str] = Field(None, max_length=10)
    no_identificacion: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=1000)
    cantidad: Optional[Decimal] = None
    unidad_medida: Optional[str] = Field(None, max_length=10)
    valor_unitario: Optional[Decimal] = None
    importe: Optional[Decimal] = None
    descuento: Optional[Decimal] = Field(None, description="Descuento aplicado al concepto")
    objeto_imp: Optional[str] = Field(None, max_length=2)
    producto_id: Optional[UUID4] = None


class ConceptoFacturaResponse(ConceptoFacturaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TAX CONCEPT SCHEMAS
# ============================================================================

class ImpuestoConceptoBase(BaseModel):
    concepto_id: UUID4
    tipo: str = Field(..., max_length=10, description="Tipo de impuesto (Traslado o Retención)")
    nombre: str = Field(..., max_length=50, description="Nombre del impuesto")
    tasa_cuota: Optional[Decimal] = Field(None, description="Tasa o cuota del impuesto")
    importe: Decimal = Field(..., description="Importe del impuesto")


class ImpuestoConceptoCreate(ImpuestoConceptoBase):
    pass


class ImpuestoConceptoUpdate(BaseModel):
    tipo: Optional[str] = Field(None, max_length=10)
    nombre: Optional[str] = Field(None, max_length=50)
    tasa_cuota: Optional[Decimal] = None
    importe: Optional[Decimal] = None


class ImpuestoConceptoResponse(ImpuestoConceptoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PAYMENT COMPLEMENT SCHEMAS
# ============================================================================

class ComplementoPagoBase(BaseModel):
    comprobante_id: UUID4
    fecha_pago: date = Field(..., description="Fecha del pago")
    forma_pago: str = Field(..., description="Forma de pago")
    moneda_pago: Optional[str] = Field(default="MXN", max_length=3, description="Moneda del pago")
    tipo_cambio_pago: Optional[Decimal] = Field(default=Decimal('1.000000'), description="Tipo de cambio del pago")
    monto: Decimal = Field(..., description="Monto del pago")
    rfc_emisor_cuenta_ord: Optional[str] = Field(None, max_length=13, description="RFC del emisor de la cuenta ordenante")
    banco_ordenante_nombre: Optional[str] = Field(None, max_length=100, description="Nombre del banco ordenante")
    cuenta_ordenante: Optional[str] = Field(None, max_length=50, description="Cuenta ordenante")
    rfc_emisor_cuenta_ben: Optional[str] = Field(None, max_length=13, description="RFC del emisor de la cuenta beneficiaria")
    banco_beneficiario_nombre: Optional[str] = Field(None, max_length=100, description="Nombre del banco beneficiario")
    cuenta_beneficiario: Optional[str] = Field(None, max_length=50, description="Cuenta beneficiaria")
    documento_relacionado_id: Optional[UUID4] = Field(None, description="ID del documento relacionado")
    id_documento: str = Field(..., max_length=36, description="ID del documento relacionado (UUID)")
    serie_documento: Optional[str] = Field(None, max_length=10, description="Serie del documento relacionado")
    folio_documento: Optional[str] = Field(None, max_length=20, description="Folio del documento relacionado")
    moneda_dr: Optional[str] = Field(default="MXN", max_length=3, description="Moneda del documento relacionado")
    tipo_cambio_dr: Optional[Decimal] = Field(default=Decimal('1.000000'), description="Tipo de cambio del documento relacionado")
    metodo_pago_dr: Optional[str] = Field(None, max_length=10, description="Método de pago del documento relacionado")
    num_parcialidad: Optional[int] = Field(None, description="Número de parcialidad")
    saldo_anterior: Optional[Decimal] = Field(None, description="Saldo anterior")
    importe_pagado: Optional[Decimal] = Field(None, description="Importe pagado")
    saldo_insoluto: Optional[Decimal] = Field(None, description="Saldo insoluto")
    activo: bool = Field(default=True, description="¿Está activo el complemento de pago?")


class ComplementoPagoCreate(ComplementoPagoBase):
    pass


class ComplementoPagoUpdate(BaseModel):
    fecha_pago: Optional[datetime] = None
    forma_pago: Optional[str] = Field(None, max_length=10)
    moneda_pago: Optional[str] = Field(None, max_length=10)
    tipo_cambio_pago: Optional[Decimal] = Field(default=None, description="Tipo de cambio para el pago")  # Corregido
    numero_operacion: Optional[str] = Field(None, max_length=100)
    rfc_emisor_cta_ben: Optional[str] = Field(None, max_length=20)
    cta_beneficiario: Optional[str] = Field(None, max_length=50)
    num_parcialidad: Optional[int] = None
    saldo_anterior: Optional[Decimal] = None
    importe_pagado: Optional[Decimal] = None
    saldo_insoluto: Optional[Decimal] = None


class ComplementoPagoResponse(ComplementoPagoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# FISCAL COMPLEMENT SCHEMAS
# ============================================================================

class ComplementoFiscalBase(BaseModel):
    comprobante_id: UUID4
    tipo_complemento: str = Field(..., description="Tipo de complemento fiscal")
    contenido: Optional[Dict[str, Any]] = Field(None, description="Contenido del complemento fiscal en formato JSON")


class ComplementoFiscalCreate(ComplementoFiscalBase):
    pass


class ComplementoFiscalUpdate(BaseModel):
    tipo_complemento: Optional[str] = None
    contenido: Optional[Dict[str, Any]] = None
    activo: Optional[bool] = None


class ComplementoFiscalResponse(ComplementoFiscalBase):
    id: UUID4
    activo: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CFDI CANCELLATION SCHEMAS
# ============================================================================

class CancelacionCFDIBase(BaseModel):
    comprobante_id: UUID4
    motivo_cancelacion: Optional[str] = Field(None, max_length=200, description="Motivo de la cancelación")
    uuid_sustituye: Optional[str] = Field(None, max_length=36, description="UUID del CFDI que sustituye (si aplica)")


class CancelacionCFDICreate(CancelacionCFDIBase):
    pass


class CancelacionCFDIUpdate(BaseModel):
    motivo_cancelacion: Optional[str] = Field(None, max_length=200)
    uuid_sustituye: Optional[str] = Field(None, max_length=36)
    estatus_sat: Optional[str] = Field(None, max_length=20)
    fecha_respuesta_sat: Optional[datetime] = None
    detalle_respuesta: Optional[str] = None
    folio_acuse: Optional[str] = Field(None, max_length=50)
    acuse_cancelacion: Optional[str] = None
    procesada: Optional[bool] = None


class CancelacionCFDIResponse(CancelacionCFDIBase):
    id: UUID4
    fecha_solicitud: datetime
    estatus_sat: Optional[str] = None
    fecha_respuesta_sat: Optional[datetime] = None
    detalle_respuesta: Optional[str] = None
    folio_acuse: Optional[str] = None
    acuse_cancelacion: Optional[str] = None
    procesada: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# RFC VALIDATION SCHEMAS
# ============================================================================

class ValidacionRFCBase(BaseModel):
    rfc: str = Field(..., min_length=12, max_length=13, description="RFC a validar")
    nombre_razon_social: Optional[str] = Field(None, max_length=254, description="Nombre o razón social del RFC")
    en_lista_negra: Optional[bool] = Field(default=False, description="¿Está en lista negra?")
    fuente_lista: Optional[str] = Field(None, max_length=100, description="Fuente de la lista negra")
    estatus_sat: Optional[str] = Field(None, max_length=20, description="Estatus del RFC ante SAT")
    estatus_especial: Optional[str] = Field(None, max_length=20, description="Estatus especial del RFC")


class ValidacionRFCCreate(ValidacionRFCBase):
    pass


class ValidacionRFCUpdate(BaseModel):
    en_lista_negra: Optional[bool] = None
    fuente_lista: Optional[str] = None
    estatus_sat: Optional[str] = None
    estatus_especial: Optional[str] = None
    detalle_verificacion: Optional[str] = None


class ValidacionRFCResponse(ValidacionRFCBase):
    id: UUID4
    fecha_verificacion: datetime
    detalle_verificacion: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INVOICE REQUEST SCHEMAS FOR FACTURAMA INTEGRATION
# ============================================================================

class InvoiceRequest(BaseModel):
    """Request schema for creating an invoice via Facturama integration"""
    rfc_receptor: str
    nombre_receptor: str
    uso_cfdi: str
    metodo_pago: str
    forma_pago: str
    tipo_comprobante: str
    condiciones_pago: Optional[str] = None
    moneda: Optional[str] = "MXN"
    tipo_cambio: Optional[Decimal] = Decimal('1.000000')
    items: List[dict]  # List of items with product details
    complementos: Optional[List[dict]] = None
    confirmacion: Optional[str] = None
    observaciones: Optional[str] = None