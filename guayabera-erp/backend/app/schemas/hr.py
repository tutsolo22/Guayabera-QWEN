"""
Human Resources Schemas: Employees, payroll, attendance, contracts
Specialized for textile manufacturing companies
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
# EMPLOYEE SCHEMAS
# ============================================================================

class EmpleadoBase(BaseModel):
    codigo: str = Field(..., max_length=20, description="Código único del empleado")
    nombre: str = Field(..., max_length=100, description="Nombre del empleado")
    apellido_paterno: str = Field(..., max_length=100, description="Apellido paterno del empleado")
    apellido_materno: Optional[str] = Field(None, max_length=100, description="Apellido materno del empleado")
    nombre_completo: str = Field(..., max_length=300, description="Nombre completo del empleado")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento")
    sexo: Optional[str] = Field(None, description="Sexo del empleado")
    estado_civil: Optional[str] = Field(None, description="Estado civil del empleado")
    nacionalidad: Optional[str] = Field(default="Mexicana", max_length=50, description="Nacionalidad")
    lugar_nacimiento: Optional[str] = Field(None, max_length=100, description="Lugar de nacimiento")
    email_personal: Optional[str] = Field(None, max_length=100, description="Email personal")
    email_corporativo: Optional[str] = Field(None, max_length=100, description="Email corporativo")
    telefono_personal: Optional[str] = Field(None, max_length=20, description="Teléfono personal")
    telefono_corporativo: Optional[str] = Field(None, max_length=20, description="Teléfono corporativo")
    celular: Optional[str] = Field(None, max_length=20, description="Número de celular")
    calle: Optional[str] = Field(None, max_length=200, description="Calle")
    numero_exterior: Optional[str] = Field(None, max_length=20, description="Número exterior")
    numero_interior: Optional[str] = Field(None, max_length=20, description="Número interior")
    colonia: Optional[str] = Field(None, max_length=100, description="Colonia")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad")
    estado: Optional[str] = Field(None, max_length=100, description="Estado")
    pais: Optional[str] = Field(default="México", max_length=100, description="País")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    tipo_empleado: Optional[str] = Field(None, description="Tipo de empleado")
    departamento: str = Field(..., description="Departamento del empleado")
    puesto: str = Field(..., max_length=100, description="Puesto del empleado")
    jefe_inmediato_id: Optional[UUID4] = Field(None, description="ID del jefe inmediato")
    fecha_contratacion: date = Field(..., description="Fecha de contratación")
    fecha_inicio_labores: Optional[date] = Field(None, description="Fecha de inicio de labores")
    fecha_baja: Optional[date] = Field(None, description="Fecha de baja")
    rfc: Optional[str] = Field(None, max_length=13, description="RFC del empleado")
    curp: Optional[str] = Field(None, max_length=18, description="CURP del empleado")
    numero_seguro_social: Optional[str] = Field(None, max_length=11, description="NSS del empleado")
    clabe_bancaria: Optional[str] = Field(None, max_length=18, description="CLABE bancaria")
    banco_pago: Optional[str] = Field(None, max_length=100, description="Banco de pago")
    salario_diario: Optional[Decimal] = Field(None, description="Salario diario")
    salario_integrado: Optional[Decimal] = Field(None, description="Salario integrado")
    riesgo_puesto: Optional[int] = Field(default=1, ge=1, le=5, description="Riesgo del puesto (1-5)")
    tipo_contrato: Optional[str] = Field(None, description="Tipo de contrato")
    regimen_contratacion: Optional[str] = Field(default="Base", max_length=100, description="Régimen de contratación")
    sindicalizado: Optional[bool] = Field(default=False, description="¿Es sindicalizado?")
    activo: bool = Field(default=True, description="¿Empleado activo?")
    comentarios: Optional[str] = Field(None, description="Comentarios")
    foto_perfil: Optional[str] = Field(None, max_length=500, description="URL de la foto de perfil")


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido_paterno: Optional[str] = Field(None, max_length=100)
    apellido_materno: Optional[str] = Field(None, max_length=100)
    nombre_completo: Optional[str] = Field(None, max_length=300)
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = None
    estado_civil: Optional[str] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)
    lugar_nacimiento: Optional[str] = None
    email_personal: Optional[str] = None
    email_corporativo: Optional[str] = None
    telefono_personal: Optional[str] = None
    telefono_corporativo: Optional[str] = None
    celular: Optional[str] = None
    calle: Optional[str] = None
    numero_exterior: Optional[str] = None
    numero_interior: Optional[str] = None
    colonia: Optional[str] = None
    ciudad: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = None
    tipo_empleado: Optional[str] = None
    departamento: Optional[str] = None
    puesto: Optional[str] = Field(None, max_length=100)
    jefe_inmediato_id: Optional[UUID4] = None
    fecha_contratacion: Optional[date] = None
    fecha_inicio_labores: Optional[date] = None
    fecha_baja: Optional[date] = None
    rfc: Optional[str] = Field(None, max_length=13)
    curp: Optional[str] = Field(None, max_length=18)
    numero_seguro_social: Optional[str] = Field(None, max_length=11)
    clabe_bancaria: Optional[str] = None
    banco_pago: Optional[str] = None
    salario_diario: Optional[Decimal] = None
    salario_integrado: Optional[Decimal] = None
    riesgo_puesto: Optional[int] = Field(None, ge=1, le=5)
    tipo_contrato: Optional[str] = None
    regimen_contratacion: Optional[str] = Field(None, max_length=100)
    sindicalizado: Optional[bool] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None
    foto_perfil: Optional[str] = Field(None, max_length=500)


class EmpleadoResponse(EmpleadoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CONTRACT SCHEMAS
# ============================================================================

class ContratoBase(BaseModel):
    empleado_id: UUID4
    numero_contrato: str = Field(..., max_length=50, description="Número de contrato")
    tipo_contrato: str = Field(..., description="Tipo de contrato")
    fecha_inicio: date = Field(..., description="Fecha de inicio del contrato")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin del contrato")
    salario_diario: Decimal = Field(..., description="Salario diario")
    descripcion_funciones: Optional[str] = Field(None, description="Descripción de funciones")
    lugar_trabajo: Optional[str] = Field(None, max_length=200, description="Lugar de trabajo")
    horario_trabajo: Optional[str] = Field(None, max_length=100, description="Horario de trabajo")
    estado: Optional[str] = Field(default="activo", description="Estado del contrato")
    archivo_contrato: Optional[str] = Field(None, max_length=500, description="Archivo del contrato")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class ContratoCreate(ContratoBase):
    pass


class ContratoUpdate(BaseModel):
    tipo_contrato: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    salario_diario: Optional[Decimal] = None
    descripcion_funciones: Optional[str] = None
    lugar_trabajo: Optional[str] = None
    horario_trabajo: Optional[str] = None
    estado: Optional[str] = None
    archivo_contrato: Optional[str] = None
    comentarios: Optional[str] = None


class ContratoResponse(ContratoBase):
    id: UUID4
    duracion_dias: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# POSITION ASSIGNMENT SCHEMAS
# ============================================================================

class EmpleadoPuestoBase(BaseModel):
    empleado_id: UUID4
    puesto_id: UUID4
    fecha_inicio: date = Field(..., description="Fecha de inicio en el puesto")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin en el puesto")
    descripcion_responsabilidades: Optional[str] = Field(None, description="Responsabilidades del puesto")
    activo: bool = Field(default=True, description="¿Asignación activa?")


class EmpleadoPuestoCreate(EmpleadoPuestoBase):
    pass


class EmpleadoPuestoUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    descripcion_responsabilidades: Optional[str] = None
    activo: Optional[bool] = None


class EmpleadoPuestoResponse(EmpleadoPuestoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# POSITION SCHEMAS
# ============================================================================

class PuestoBase(BaseModel):
    codigo: str = Field(..., max_length=20, description="Código único del puesto")
    nombre: str = Field(..., max_length=100, description="Nombre del puesto")
    descripcion: Optional[str] = Field(None, description="Descripción del puesto")
    departamento: str = Field(..., description="Departamento del puesto")
    nivel_autoridad: Optional[int] = Field(default=1, ge=1, le=10, description="Nivel de autoridad (1-10)")
    nivel_responsabilidad: Optional[int] = Field(default=1, ge=1, le=10, description="Nivel de responsabilidad (1-10)")
    habilidades_requeridas: Optional[Dict[str, Any]] = Field(None, description="Habilidades requeridas en JSON")
    experiencia_requerida: Optional[int] = Field(None, ge=0, description="Años de experiencia requeridos")
    salario_minimo: Optional[Decimal] = Field(None, description="Salario mínimo")
    salario_maximo: Optional[Decimal] = Field(None, description="Salario máximo")
    activo: bool = Field(default=True, description="¿Puesto activo?")


class PuestoCreate(PuestoBase):
    pass


class PuestoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    departamento: Optional[str] = None
    nivel_autoridad: Optional[int] = Field(None, ge=1, le=10)
    nivel_responsabilidad: Optional[int] = Field(None, ge=1, le=10)
    habilidades_requeridas: Optional[Dict[str, Any]] = None
    experiencia_requerida: Optional[int] = Field(None, ge=0)
    salario_minimo: Optional[Decimal] = None
    salario_maximo: Optional[Decimal] = None
    activo: Optional[bool] = None


class PuestoResponse(PuestoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ATTENDANCE SCHEMAS
# ============================================================================

class AsistenciaBase(BaseModel):
    empleado_id: UUID4
    fecha: date = Field(..., description="Fecha de la asistencia")
    hora_entrada: Optional[datetime] = Field(None, description="Hora de entrada")
    hora_salida: Optional[datetime] = Field(None, description="Hora de salida")
    estado: Optional[str] = Field(default="presente", description="Estado de asistencia")
    hora_entrada_comida: Optional[datetime] = Field(None, description="Hora de entrada después de comida")
    hora_salida_comida: Optional[datetime] = Field(None, description="Hora de salida para comida")
    horas_extras: Optional[float] = Field(default=0.0, ge=0, description="Horas extras trabajadas")
    minutos_tarde: Optional[int] = Field(default=0, ge=0, description="Minutos tarde")
    minutos_temprano: Optional[int] = Field(default=0, ge=0, description="Minutos de salida temprana")
    verificada: Optional[bool] = Field(default=False, description="¿Asistencia verificada?")
    autorizada: Optional[bool] = Field(default=False, description="¿Asistencia autorizada?")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class AsistenciaCreate(AsistenciaBase):
    pass


class AsistenciaUpdate(BaseModel):
    hora_entrada: Optional[datetime] = None
    hora_salida: Optional[datetime] = None
    estado: Optional[str] = None
    hora_entrada_comida: Optional[datetime] = None
    hora_salida_comida: Optional[datetime] = None
    horas_extras: Optional[float] = Field(None, ge=0)
    minutos_tarde: Optional[int] = Field(None, ge=0)
    minutos_temprano: Optional[int] = Field(None, ge=0)
    verificada: Optional[bool] = None
    autorizada: Optional[bool] = None
    comentarios: Optional[str] = None


class AsistenciaResponse(AsistenciaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# MEDICAL LEAVE SCHEMAS
# ============================================================================

class IncapacidadBase(BaseModel):
    empleado_id: UUID4
    fecha_inicio: date = Field(..., description="Fecha de inicio de la incapacidad")
    fecha_fin: date = Field(..., description="Fecha de fin de la incapacidad")
    duracion_dias: int = Field(..., ge=1, description="Duración en días")
    tipo_incapacidad: str = Field(..., max_length=50, description="Tipo de incapacidad")
    causa: Optional[str] = Field(None, max_length=200, description="Causa de la incapacidad")
    clave_tipo_incapacidad: Optional[str] = Field(None, max_length=10, description="Clave SAT de incapacidad")
    numero_documento: Optional[str] = Field(None, max_length=50, description="Número de documento")
    institucion_emisora: Optional[str] = Field(None, max_length=100, description="Institución emisora")
    firma_autorizada: Optional[str] = Field(None, max_length=100, description="Firma autorizada")
    estado: Optional[str] = Field(default="activa", description="Estado de la incapacidad")
    verificada: Optional[bool] = Field(default=False, description="¿Incapacidad verificada?")
    comentarios: Optional[str] = Field(None, description="Comentarios")
    archivo_documento: Optional[str] = Field(None, max_length=500, description="Archivo del documento")


class IncapacidadCreate(IncapacidadBase):
    pass


class IncapacidadUpdate(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    duracion_dias: Optional[int] = Field(None, ge=1)
    tipo_incapacidad: Optional[str] = Field(None, max_length=50)
    causa: Optional[str] = Field(None, max_length=200)
    clave_tipo_incapacidad: Optional[str] = Field(None, max_length=10)
    numero_documento: Optional[str] = None
    institucion_emisora: Optional[str] = None
    firma_autorizada: Optional[str] = None
    estado: Optional[str] = None
    verificada: Optional[bool] = None
    comentarios: Optional[str] = None
    archivo_documento: Optional[str] = None


class IncapacidadResponse(IncapacidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# VACATION SCHEMAS
# ============================================================================

class VacacionBase(BaseModel):
    empleado_id: UUID4
    anio: int = Field(..., ge=2000, le=2100, description="Año del periodo de vacaciones")
    periodo_inicio: date = Field(..., description="Inicio del periodo vacacional")
    periodo_fin: date = Field(..., description="Fin del periodo vacacional")
    dias_correspondientes: int = Field(..., ge=0, description="Días correspondientes")
    dias_disfrutados: Optional[int] = Field(default=0, ge=0, description="Días disfrutados")
    dias_pendientes: int = Field(..., ge=0, description="Días pendientes")
    fecha_solicitud: date = Field(..., description="Fecha de solicitud")
    fecha_inicio_disfrute: date = Field(..., description="Fecha de inicio del disfrute")
    fecha_fin_disfrute: date = Field(..., description="Fecha de fin del disfrute")
    dias_a_disfrutar: int = Field(..., ge=1, description="Días a disfrutar")
    motivo: Optional[str] = Field(None, max_length=200, description="Motivo de las vacaciones")
    autorizado_por_id: Optional[UUID4] = Field(None, description="ID del autorizador")
    fecha_autorizacion: Optional[datetime] = Field(None, description="Fecha de autorización")
    estado: Optional[str] = Field(default="pendiente", description="Estado de la solicitud")
    pago_calculado: Optional[Decimal] = Field(None, description="Pago calculado")
    pago_real: Optional[Decimal] = Field(None, description="Pago real")
    fecha_pago: Optional[date] = Field(None, description="Fecha de pago")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class VacacionCreate(VacacionBase):
    pass


class VacacionUpdate(BaseModel):
    dias_disfrutados: Optional[int] = Field(None, ge=0)
    dias_pendientes: Optional[int] = Field(None, ge=0)
    fecha_inicio_disfrute: Optional[date] = None
    fecha_fin_disfrute: Optional[date] = None
    dias_a_disfrutar: Optional[int] = Field(None, ge=1)
    motivo: Optional[str] = Field(None, max_length=200)
    autorizado_por_id: Optional[UUID4] = None
    fecha_autorizacion: Optional[datetime] = None
    estado: Optional[str] = None
    pago_calculado: Optional[Decimal] = None
    pago_real: Optional[Decimal] = None
    fecha_pago: Optional[date] = None
    comentarios: Optional[str] = None


class VacacionResponse(VacacionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PAYROLL SCHEMAS
# ============================================================================

class NominaBase(BaseModel):
    empleado_id: UUID4
    periodo_pago_id: UUID4
    tipo_nomina: Optional[str] = Field(default="ordinaria", description="Tipo de nómina")
    numero_nota: Optional[str] = Field(None, max_length=50, description="Número de nota")
    fecha_pago: date = Field(..., description="Fecha de pago")
    fecha_inicial_pago: date = Field(..., description="Fecha inicial de pago")
    fecha_final_pago: date = Field(..., description="Fecha final de pago")
    percepciones_totales: Optional[Decimal] = Field(default=Decimal('0.00'), description="Percepciones totales")
    horas_extras_pagadas: Optional[Decimal] = Field(default=Decimal('0.00'), description="Horas extras pagadas")
    bonos_pagados: Optional[Decimal] = Field(default=Decimal('0.00'), description="Bonos pagados")
    deducciones_totales: Optional[Decimal] = Field(default=Decimal('0.00'), description="Deducciones totales")
    isr_retencion: Optional[Decimal] = Field(default=Decimal('0.00'), description="ISR retenido")
    seguridad_social_descuento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Descuento seguridad social")
    infonavit_descuento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Descuento Infonavit")
    otros_descuentos: Optional[Decimal] = Field(default=Decimal('0.00'), description="Otros descuentos")
    subsidio_causado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Subsidio causado")
    subsidio_entregado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Subsidio entregado")
    total_otro_pago: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total otro pago")
    importe_total_neto: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe total neto")
    uuid_cfdi: Optional[str] = Field(None, max_length=36, description="UUID del CFDI")
    folio_fiscal: Optional[str] = Field(None, max_length=36, description="Folio fiscal")
    fecha_timbrado: Optional[datetime] = Field(None, description="Fecha de timbrado")
    sello_digital_cfdi: Optional[str] = Field(None, description="Sello digital CFDI")
    cadena_original: Optional[str] = Field(None, description="Cadena original")
    estado: Optional[str] = Field(default="emitida", description="Estado de la nómina")
    fecha_cancelacion: Optional[datetime] = Field(None, description="Fecha de cancelación")
    motivo_cancelacion: Optional[str] = Field(None, max_length=200, description="Motivo de cancelación")
    comentarios: Optional[str] = Field(None, description="Comentarios")
    archivo_xml: Optional[str] = Field(None, max_length=500, description="Archivo XML")
    archivo_pdf: Optional[str] = Field(None, max_length=500, description="Archivo PDF")


class NominaCreate(NominaBase):
    pass


class NominaUpdate(BaseModel):
    tipo_nomina: Optional[str] = None
    numero_nota: Optional[str] = Field(None, max_length=50)
    fecha_pago: Optional[date] = None
    fecha_inicial_pago: Optional[date] = None
    fecha_final_pago: Optional[date] = None
    percepciones_totales: Optional[Decimal] = None
    horas_extras_pagadas: Optional[Decimal] = None
    bonos_pagados: Optional[Decimal] = None
    deducciones_totales: Optional[Decimal] = None
    isr_retencion: Optional[Decimal] = None
    seguridad_social_descuento: Optional[Decimal] = None
    infonavit_descuento: Optional[Decimal] = None
    otros_descuentos: Optional[Decimal] = None
    subsidio_causado: Optional[Decimal] = None
    subsidio_entregado: Optional[Decimal] = None
    total_otro_pago: Optional[Decimal] = None
    importe_total_neto: Optional[Decimal] = None
    uuid_cfdi: Optional[str] = Field(None, max_length=36)
    folio_fiscal: Optional[str] = Field(None, max_length=36)
    fecha_timbrado: Optional[datetime] = None
    sello_digital_cfdi: Optional[str] = None
    cadena_original: Optional[str] = None
    estado: Optional[str] = None
    fecha_cancelacion: Optional[datetime] = None
    motivo_cancelacion: Optional[str] = Field(None, max_length=200)
    comentarios: Optional[str] = None
    archivo_xml: Optional[str] = None
    archivo_pdf: Optional[str] = None


class NominaResponse(NominaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# PAYROLL PERIOD SCHEMAS
# ============================================================================

class PeriodoPagoBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del periodo")
    codigo: str = Field(..., max_length=30, description="Código único del periodo")
    descripcion: Optional[str] = Field(None, description="Descripción del periodo")
    fecha_inicio_periodo: date = Field(..., description="Fecha de inicio del periodo")
    fecha_fin_periodo: date = Field(..., description="Fecha de fin del periodo")
    fecha_pago_nomina: date = Field(..., description="Fecha de pago de nómina")
    tipo_periodo: str = Field(..., max_length=20, description="Tipo de periodo")
    frecuencia_pago: Optional[int] = Field(default=2, ge=1, description="Frecuencia de pago")
    cerrado: Optional[bool] = Field(default=False, description="¿Periodo cerrado?")
    fecha_cierre: Optional[datetime] = Field(None, description="Fecha de cierre")
    comentarios: Optional[str] = Field(None, description="Comentarios")


class PeriodoPagoCreate(PeriodoPagoBase):
    pass


class PeriodoPagoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    fecha_inicio_periodo: Optional[date] = None
    fecha_fin_periodo: Optional[date] = None
    fecha_pago_nomina: Optional[date] = None
    tipo_periodo: Optional[str] = Field(None, max_length=20)
    frecuencia_pago: Optional[int] = Field(None, ge=1)
    cerrado: Optional[bool] = None
    fecha_cierre: Optional[datetime] = None
    comentarios: Optional[str] = None


class PeriodoPagoResponse(PeriodoPagoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# EARNINGS SCHEMAS
# ============================================================================

class PercepcionBase(BaseModel):
    nomina_id: UUID4
    tipo_percepcion: str = Field(..., description="Tipo de percepción")
    clave: str = Field(..., max_length=20, description="Clave SAT")
    concepto: str = Field(..., max_length=200, description="Concepto de percepción")
    importe_gravado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe gravado")
    importe_exento: Optional[Decimal] = Field(default=Decimal('0.00'), description="Importe exento")


class PercepcionCreate(PercepcionBase):
    pass


class PercepcionUpdate(BaseModel):
    tipo_percepcion: Optional[str] = None
    clave: Optional[str] = Field(None, max_length=20)
    concepto: Optional[str] = Field(None, max_length=200)
    importe_gravado: Optional[Decimal] = None
    importe_exento: Optional[Decimal] = None


class PercepcionResponse(PercepcionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DEDUCTIONS SCHEMAS
# ============================================================================

class DeduccionBase(BaseModel):
    nomina_id: UUID4
    tipo_deduccion: str = Field(..., description="Tipo de deducción")
    clave: str = Field(..., max_length=20, description="Clave SAT")
    concepto: str = Field(..., max_length=200, description="Concepto de deducción")
    importe: Decimal = Field(..., description="Importe de la deducción")


class DeduccionCreate(DeduccionBase):
    pass


class DeduccionUpdate(BaseModel):
    tipo_deduccion: Optional[str] = None
    clave: Optional[str] = Field(None, max_length=20)
    concepto: Optional[str] = Field(None, max_length=200)
    importe: Optional[Decimal] = None


class DeduccionResponse(DeduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SCHEMAS ESPECÍFICOS DE RECURSOS HUMANOS
# ============================================================================

class AnuncioBase(BaseModel):
    titulo: str = Field(..., max_length=200, description="Título del anuncio")
    contenido: str = Field(..., description="Contenido del anuncio")
    tipo: str = Field(..., max_length=50, description="Tipo de anuncio")
    fecha_expiracion: Optional[date] = Field(None, description="Fecha de expiración del anuncio")
    publico: bool = Field(default=True, description="¿Es visible para todos?")


class AnuncioCreate(AnuncioBase):
    pass


class AnuncioUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    contenido: Optional[str] = None
    tipo: Optional[str] = Field(None, max_length=50)
    fecha_expiracion: Optional[date] = None
    publico: Optional[bool] = None


class AnuncioResponse(AnuncioBase):
    id: UUID4
    fecha_publicacion: date
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VistaAnuncioBase(BaseModel):
    anuncio_id: UUID4
    empleado_id: UUID4


class VistaAnuncioCreate(VistaAnuncioBase):
    pass


class VistaAnuncioResponse(VistaAnuncioBase):
    id: UUID4
    fecha_vista: datetime

    class Config:
        from_attributes = True


class VacacionBase(BaseModel):
    empleado_id: UUID4
    fecha_inicio: date
    fecha_fin: date
    dias_solicitados: int
    estado: str = Field(default="pendiente", description="Estado de la solicitud de vacaciones")
    comentarios: Optional[str] = None


class VacacionCreate(VacacionBase):
    pass


class VacacionUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado de la vacación")
    comentarios: Optional[str] = None


class VacacionResponse(VacacionBase):
    id: UUID4
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[UUID4] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IncapacidadBase(BaseModel):
    empleado_id: UUID4
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    tipo_incapacidad: str = Field(..., max_length=50, description="Tipo de incapacidad")
    documento_soporte: Optional[str] = Field(None, max_length=500, description="Ruta al documento de soporte")
    estado: str = Field(default="registrado", description="Estado de la incapacidad")
    comentarios: Optional[str] = None


class IncapacidadCreate(IncapacidadBase):
    pass


class IncapacidadUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado de la incapacidad")
    comentarios: Optional[str] = None


class IncapacidadResponse(IncapacidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SolicitudEquipoBase(BaseModel):
    empleado_id: UUID4
    tipo_equipo: str = Field(..., max_length=100, description="Tipo de equipo solicitado")
    descripcion_equipo: Optional[str] = None
    estado_equipo: str = Field(default="nuevo", description="Estado del equipo")
    necesita_correo: bool = Field(default=False, description="¿Necesita cuenta de correo?")
    tipo_correo: str = Field(default="nuevo", description="Tipo de correo")
    departamento_destino: str = Field(..., max_length=100, description="Departamento destino")
    empleado_asignado_nombre: str = Field(..., max_length=200, description="Nombre del empleado asignado")
    jefe_departamento_id: UUID4
    carpetas_compartidas: bool = Field(default=False, description="¿Necesita carpetas compartidas?")
    descripcion_carpetas: Optional[str] = None
    estado: str = Field(default="pendiente", description="Estado de la solicitud")


class SolicitudEquipoCreate(SolicitudEquipoBase):
    pass


class SolicitudEquipoUpdate(BaseModel):
    estado: Optional[str] = Field(None, description="Nuevo estado de la solicitud")
    descripcion_equipo: Optional[str] = None
    carpetas_compartidas: Optional[bool] = None
    descripcion_carpetas: Optional[str] = None


class SolicitudEquipoResponse(SolicitudEquipoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
