"""
Payroll Schemas: Electronic payroll according to Mexican SAT regulations
Integration with CFDI payroll complement
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
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
# PAYROLL PERIOD SCHEMAS
# ============================================================================

class PeriodoNominaBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del periodo")
    nombre: str = Field(..., max_length=100, description="Nombre del periodo")
    descripcion: Optional[str] = Field(None, description="Descripción del periodo")
    fecha_inicio: date = Field(..., description="Fecha de inicio del periodo")
    fecha_fin: date = Field(..., description="Fecha de fin del periodo")
    fecha_pago: date = Field(..., description="Fecha de pago del periodo")
    tipo_nomina: Optional[str] = Field(default="O", description="Tipo de nómina (O=Ordinaria, E=Extraordinaria)")
    periodicidad_pago: str = Field(..., description="Periodicidad de pago")
    empresa_id: UUID4 = Field(..., description="ID de la empresa")
    cerrado: bool = Field(default=False, description="¿Está cerrado el periodo?")


class PeriodoNominaCreate(PeriodoNominaBase):
    pass


class PeriodoNominaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    fecha_pago: Optional[date] = None
    tipo_nomina: Optional[str] = None
    periodicidad_pago: Optional[str] = None
    cerrado: Optional[bool] = None
    procesado: Optional[bool] = None


class PeriodoNominaResponse(PeriodoNominaBase):
    id: UUID4
    procesado: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PAYROLL RECEIPT SCHEMAS
# ============================================================================

class NominaBase(BaseModel):
    folio: str = Field(..., max_length=50, description="Folio único del recibo de nómina")
    numero_empleado: str = Field(..., max_length=30, description="Número de empleado")
    fecha_pago: date = Field(..., description="Fecha de pago")
    empleado_id: UUID4 = Field(..., description="ID del empleado")
    periodo_id: UUID4 = Field(..., description="ID del periodo")
    tipo_nomina: str = Field(..., description="Tipo de nómina")
    fecha_inicio_pago: date = Field(..., description="Fecha de inicio del periodo de pago")
    fecha_fin_pago: date = Field(..., description="Fecha de fin del periodo de pago")
    percepciones_total_gravado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total gravado de percepciones")
    percepciones_total_exento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total exento de percepciones")
    deducciones_total_otras: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de otras deducciones")
    deducciones_total_impuestos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de deducciones por impuestos")
    total_percepciones: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de percepciones")
    total_deducciones: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de deducciones")
    total_otros_pagos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total de otros pagos")
    neto_a_pagar: Optional[Decimal] = Field(default=Decimal('0.00'), description="Neto a pagar")
    tipo_contrato: Optional[str] = Field(None, max_length=100, description="Tipo de contrato")
    tipo_regimen: Optional[str] = Field(None, max_length=10, description="Tipo de régimen")
    regimen_contratacion: Optional[str] = Field(None, max_length=100, description="Régimen de contratación")
    numero_seguridad_social: Optional[str] = Field(None, max_length=15, description="Número de seguridad social")
    riesgo_puesto: Optional[str] = Field(None, max_length=10, description="Riesgo del puesto")
    banco: Optional[str] = Field(None, max_length=50, description="Banco")
    fecha_inicio_rel_laboral: Optional[date] = Field(None, description="Fecha de inicio de la relación laboral")
    antiguedad_bimestres: Optional[int] = Field(None, description="Antigüedad en bimestres")
    salario_base_cotizacion: Optional[Decimal] = Field(None, description="Salario base de cotización")
    salario_diario_integrado: Optional[Decimal] = Field(None, description="Salario diario integrado")
    estado: Optional[str] = Field(default="pendiente_timbrado", description="Estado del recibo de nómina")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class NominaCreate(NominaBase):
    pass


class NominaUpdate(BaseModel):
    percepciones_total_gravado: Optional[Decimal] = None
    percepciones_total_exento: Optional[Decimal] = None
    deducciones_total_otras: Optional[Decimal] = None
    deducciones_total_impuestos: Optional[Decimal] = None
    total_percepciones: Optional[Decimal] = None
    total_deducciones: Optional[Decimal] = None
    total_otros_pagos: Optional[Decimal] = None
    neto_a_pagar: Optional[Decimal] = None
    folio_fiscal: Optional[str] = None
    estatus_facturama: Optional[str] = None
    estatus_sat: Optional[str] = None
    estado: Optional[str] = None
    comentarios: Optional[str] = None


class NominaResponse(NominaBase):
    id: UUID4
    folio_fiscal: Optional[str] = None
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
# PERCEPTION SCHEMAS
# ============================================================================

class PercepcionBase(BaseModel):
    nomina_id: UUID4
    tipo_percepcion: str = Field(..., description="Tipo de percepción")
    clave: str = Field(..., max_length=10, description="Clave de la percepción")
    concepto: str = Field(..., max_length=250, description="Concepto de la percepción")
    importe_gravado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe gravado")
    importe_exento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe exento")
    horas_extra_dias: Optional[int] = Field(default=0, description="Días de horas extras trabajadas")
    horas_extra_tipo: Optional[str] = Field(None, description="Tipo de horas extras")
    horas_extra_importe_pagado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe pagado por horas extras")


class PercepcionCreate(PercepcionBase):
    pass


class PercepcionUpdate(BaseModel):
    tipo_percepcion: Optional[str] = None
    clave: Optional[str] = Field(None, max_length=10)
    concepto: Optional[str] = Field(None, max_length=250)
    importe_gravado: Optional[Decimal] = None
    importe_exento: Optional[Decimal] = None
    horas_extra_dias: Optional[int] = None
    horas_extra_tipo: Optional[str] = None
    horas_extra_importe_pagado: Optional[Decimal] = None


class PercepcionResponse(PercepcionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DEDUCTION SCHEMAS
# ============================================================================

class DeduccionBase(BaseModel):
    nomina_id: UUID4
    tipo_deduccion: str = Field(..., description="Tipo de deducción")
    clave: str = Field(..., max_length=10, description="Clave de la deducción")
    concepto: str = Field(..., max_length=250, description="Concepto de la deducción")
    importe: Decimal = Field(..., description="Importe de la deducción")


class DeduccionCreate(DeduccionBase):
    pass


class DeduccionUpdate(BaseModel):
    tipo_deduccion: Optional[str] = None
    clave: Optional[str] = Field(None, max_length=10)
    concepto: Optional[str] = Field(None, max_length=250)
    importe: Optional[Decimal] = None


class DeduccionResponse(DeduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# INCAPACITY SCHEMAS
# ============================================================================

class IncapacidadBase(BaseModel):
    nomina_id: UUID4
    tipo_incapacidad: str = Field(..., description="Tipo de incapacidad")
    dias_incapacidad: int = Field(..., gt=0, description="Número de días de incapacidad")
    descuento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Descuento por incapacidad")


class IncapacidadCreate(IncapacidadBase):
    pass


class IncapacidadUpdate(BaseModel):
    tipo_incapacidad: Optional[str] = None
    dias_incapacidad: Optional[int] = Field(gt=0)
    descuento: Optional[Decimal] = None


class IncapacidadResponse(IncapacidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# OTHER PAYMENT SCHEMAS
# ============================================================================

class OtroPagoBase(BaseModel):
    nomina_id: UUID4
    tipo_otro_pago: str = Field(..., max_length=10, description="Tipo de otro pago")
    clave: str = Field(..., max_length=10, description="Clave del otro pago")
    concepto: str = Field(..., max_length=250, description="Concepto del otro pago")
    importe: Decimal = Field(..., description="Importe del otro pago")
    subsidio_causado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Subsidio causado")


class OtroPagoCreate(OtroPagoBase):
    pass


class OtroPagoUpdate(BaseModel):
    tipo_otro_pago: Optional[str] = Field(None, max_length=10)
    clave: Optional[str] = Field(None, max_length=10)
    concepto: Optional[str] = Field(None, max_length=250)
    importe: Optional[Decimal] = None
    subsidio_causado: Optional[Decimal] = None


class OtroPagoResponse(OtroPagoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True