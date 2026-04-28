"""
Payroll Models: Electronic payroll according to Mexican SAT regulations
Integration with CFDI payroll complement
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoNomina(enum.Enum):
    ORDINARIA = "O"      # Ordinaria
    EXTRAORDINARIA = "E"  # Extraordinaria


class TipoPercepcion(enum.Enum):
    SALARIO_BASE_COTIZACION = "001"
    SALARIO_BASE_CALCULO = "002"
    ANTIGUEDAD = "003"
    GRATIFICACION_ANUAL = "004"
    PARTICIPACION_UTILIDAD = "005"
    REEMBOLSO_GASTOS = "006"
    FONDO_AHORRO = "007"
    CAJA_COMPENSACION = "008"
    SUELDOS = "009"
    JUBILACION_PENSION_RETIRO = "010"
    OTROS_CONCEPTOS = "011"
    SEGUROS = "012"
    LICENCIAS = "013"
    GRUATIFICACIONES = "014"
    HORIZAS_EXTRA = "015"
    PRIMA_DOMINICAL = "016"
    PRIMA_VACACIONAL = "017"
    PRIMA_ANTIGUEDAD = "018"
    PAGO_DISTINTO_FORMA = "019"
    COMPENSACION_SALARIOS_ACUMULADOS = "020"
    VIATICOS = "021"
    APLICACION_SUBSIDIO = "022"
    APLICACION_RECOMPENSA = "023"
    INDEMNIZACION = "024"
    PAGOS_TERCEROS = "025"
    INCAPACIDAD = "026"
    CUENTA_RETIRO = "027"
    RETROACTIVO = "028"
    BECAS_DESARROLLO_HUMANO = "029"
    AYUDAS_AUTORIDAD = "030"
    AYUDAS_INSTITUCIONES = "031"
    DEPOSITO_FONDO_AHORRO = "032"
    DEPOSITO_CUENTA_RETIRO = "033"
    DEPOSITO_VIVIENDA = "034"
    HORAS_EXTRA = "035"
    PRIMA_VIGENCIA = "036"
    SEGURO_LARGO_PLAZO = "037"
    SEPARACION_INDIVIDUAL = "038"
    SEPARACION_CONJUNTA = "039"
    SEPARACION_VOLUNTARIA = "040"
    SEPARACION_PENSION_ALIMENTICIA = "041"
    SEPARACION_JUBILACION = "042"
    SEPARACION_PENSION = "043"
    SEPARACION_OTROS = "044"
    SEPARACION_PENSION_OTROS = "045"
    SEPARACION_JUBILACION_OTROS = "046"
    SEPARACION_JUBILACION_PENSION = "047"
    SEPARACION_JUBILACION_PENSION_OTROS = "048"


class TipoDeduccion(enum.Enum):
    IRR = "001"
    IRR_EXENTO = "002"
    APORTACION_SEGURIDAD_SOCIAL = "003"
    CARGAS_FAMILIARES = "004"
    OTROS = "005"
    APORTACION_SAR = "006"
    APORTE_INDIVIDUAL_CUOTA_SINDICAL = "007"
    CREDITO_INSTITUCION_VIVIENDA = "008"
    PENSION_ALIMENTICIA = "009"
    RENTA = "010"
    PRESTAMOS_QUINCENA = "011"
    PAGOS_HECHOS_CON_RECURSOS_PROP_DEL_TRABAJADOR = "012"
    APORTACION_VOLUNTARIA = "013"
    APORTACION_FONDO_VIVIENDA = "014"
    DESCUENTO_POR_INCAPACIDAD = "015"
    VISTAS_O_SUBSIDIOS = "016"
    APOYO_ANUAL_INFANCIA_ADOLESCENCIA = "017"
    PRESTAMOS_GUBERNAMENTALES_VIVIENDA = "018"
    APORTACIONES_ADICIONALES = "019"
    OTROS_DESCUENTOS = "020"
    APORTACION_EMPLEADOR_AFORE = "021"
    APORTACION_EMPLEADOR_CESANTIA = "022"
    APORTACION_EMPLEADOR_INVDAD = "023"
    APORTACION_EMPLEADOR_VIVIENDA = "024"
    IVA_TRASLADADO_CARGO_SUBSECUENTE = "025"
    ISR_RETENIDO_CARGO_SUBSECUENTE = "026"
    CUOTA_FIJA = "027"
    EXCEDENTE_SALARIO_MINIMO = "028"
    PRIMA_SEGURO_LARGO_PLAZO = "029"
    CUOTAS_WORKERS = "030"
    APORTACION_SINDICAL = "031"
    APORTACION_ARBITRIOS = "032"
    DESCUENTOS_IMPOSES = "033"
    IMPUESTOS_LOCALES = "034"
    DEDUCCION_FONHA = "035"
    APORTACION_VOLUNTARIA_PENSIONES = "036"
    APORTACION_VOLUNTARIA_CESANTIA = "037"
    APORTACION_VOLUNTARIA_INVDAD = "038"
    APORTACION_VOLUNTARIA_VIVIENDA = "039"
    APORTACION_VOLUNTARIA_AFORE = "040"
    APORTACION_VOLUNTARIA_SUBSIDIO = "041"
    APORTACION_VOLUNTARIA_OTROS = "042"
    APORTACION_VOLUNTARIA_SUBSIDIO_EMPLEO = "043"
    APORTACION_VOLUNTARIA_SUBSIDIO_CAPACITACION = "044"
    APORTACION_VOLUNTARIA_SUBSIDIO_VIVIENDA = "045"
    APORTACION_VOLUNTARIA_SUBSIDIO_OTROS = "046"
    APORTACION_VOLUNTARIA_SUBSIDIO_INVDAD = "047"
    APORTACION_VOLUNTARIA_SUBSIDIO_EDUCACION = "048"
    APORTACION_VOLUNTARIA_SUBSIDIO_SALUD = "049"
    APORTACION_VOLUNTARIA_SUBSIDIO_DESARROLLO = "050"


class TipoIncapacidad(enum.Enum):
    RIESGO_DE_TRABAJO = "01"
    ENFERMEDAD_EN_GENERAL = "02"
    MATERNIDAD = "03"
    LICENCIA_POR_CUARENTENA = "04"
    RIESGO_DE_COVID = "05"
    LICENCIAS_POR_CONTINGENCIAS = "06"
    OTROS = "07"


class PeriodicidadPago(enum.Enum):
    DIARIO = "01"
    SEMANAL = "02"
    CATORCENAL = "03"
    QUINCENAL = "04"
    MENSUAL = "05"
    BIMESTRAL = "06"
    TRIMESTRAL = "07"
    CUATRIMESTRAL = "08"
    SEMESTRAL = "09"
    ANUAL = "10"
    DECENAL = "11"
    OTRAS_PERIODICIDADES = "12"


# ============================================================================
# PAYROLL MODELS
# ============================================================================

class PeriodoNomina(Base):
    """Payroll period - Periodo de nómina"""
    __tablename__ = "nom_periodo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Period identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # PER-2023-01
    nombre = Column(String(100), nullable=False)  # Enero 2023
    descripcion = Column(Text)
    
    # Period dates
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    fecha_pago = Column(Date, nullable=False)  # Date when payment is made
    
    # Payroll type
    tipo_nomina = Column(SQLEnum(TipoNomina), default=TipoNomina.ORDINARIA)
    periodicidad_pago = Column(SQLEnum(PeriodicidadPago), nullable=False)
    
    # Company
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("admin_empresa.id"), nullable=False)
    
    # Status
    cerrado = Column(Boolean, default=False)  # If the period is closed for modifications
    procesado = Column(Boolean, default=False)  # If payroll has been processed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    empresa = relationship("Empresa")
    nominas = relationship("Nomina", back_populates="periodo")


class Nomina(Base):
    """Payroll receipt - Recibo de nómina"""
    __tablename__ = "nom_nomina"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document identification
    folio = Column(String(50), unique=True, nullable=False, index=True)  # NOM-EMP-001-2023
    numero_empleado = Column(String(30), nullable=False)  # Employee number
    fecha_pago = Column(Date, nullable=False)  # Date of payment
    
    # Employee
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Period
    periodo_id = Column(UUID(as_uuid=True), ForeignKey("nom_periodo.id"), nullable=False)
    
    # Payroll details
    tipo_nomina = Column(SQLEnum(TipoNomina), nullable=False)
    fecha_inicio_pago = Column(Date, nullable=False)  # Start date of payment period
    fecha_fin_pago = Column(Date, nullable=False)  # End date of payment period
    
    # Totals
    percepciones_total_gravado = Column(Numeric(12, 2), default=0.00)
    percepciones_total_exento = Column(Numeric(12, 2), default=0.00)
    deducciones_total_otras = Column(Numeric(12, 2), default=0.00)
    deducciones_total_impuestos = Column(Numeric(12, 2), default=0.00)
    total_percepciones = Column(Numeric(12, 2), default=0.00)
    total_deducciones = Column(Numeric(12, 2), default=0.00)
    total_otros_pagos = Column(Numeric(12, 2), default=0.00)
    neto_a_pagar = Column(Numeric(12, 2), default=0.00)
    
    # Fiscal data
    tipo_contrato = Column(String(100))  # Type of contract
    tipo_regimen = Column(String(10))  # SAT regime code
    regimen_contratacion = Column(String(100))  # Contract regime
    numero_seguridad_social = Column(String(15))  # Social security number
    riesgo_puesto = Column(String(10))  # Risk level of position
    banco = Column(String(50))  # Bank code
    fecha_inicio_rel_laboral = Column(Date)  # Start date of employment
    antiguedad_bimestres = Column(Integer)  # Antiquity in bimesters
    salario_base_cotizacion = Column(Numeric(10, 2))  # Base salary for contributions
    salario_diario_integrado = Column(Numeric(10, 2))  # Integrated daily salary
    
    # Facturama integration
    folio_fiscal = Column(String(36))  # SAT UUID (after stamping)
    facturama_id = Column(String(50))  # ID from Facturama API
    estatus_facturama = Column(String(20))  # Status from Facturama
    estatus_sat = Column(String(20))  # Status from SAT
    cadena_original = Column(Text)  # Original string from SAT
    sello_digital = Column(String(250))  # Digital seal
    sello_sat = Column(String(250))  # SAT seal
    no_certificado = Column(String(20))  # Certificate number
    no_certificado_sat = Column(String(20))  # SAT certificate number
    
    # Status
    estado = Column(String(20), default="pendiente_timbrado")  # State of the payroll receipt
    
    # Files
    ruta_pdf = Column(String(255))  # Path to PDF file
    ruta_xml = Column(String(255))  # Path to XML file
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    empleado = relationship("Empleado")
    periodo = relationship("PeriodoNomina", back_populates="nominas")
    percepciones = relationship("Percepcion", back_populates="nomina")
    deducciones = relationship("Deduccion", back_populates="nomina")
    incapacidades = relationship("Incapacidad", back_populates="nomina")
    otros_pagos = relationship("OtroPago", back_populates="nomina")


class Percepcion(Base):
    """Payroll perception - Percepción de nómina"""
    __tablename__ = "nom_percepcion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("nom_nomina.id"), nullable=False)
    
    # Perception details
    tipo_percepcion = Column(SQLEnum(TipoPercepcion), nullable=False)
    clave = Column(String(10), nullable=False)  # Perception code
    concepto = Column(String(250), nullable=False)  # Description
    importe_gravado = Column(Numeric(12, 2), default=0.00)  # Taxable amount
    importe_exento = Column(Numeric(12, 2), default=0.00)  # Exempt amount
    
    # Hours for extra pay
    horas_extra_dias = Column(Integer, default=0)  # Days of extra hours worked
    horas_extra_tipo = Column(String(50))  # Type of extra hours
    horas_extra_importe_pagado = Column(Numeric(12, 2), default=0.00)  # Amount paid for extra hours
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    nomina = relationship("Nomina", back_populates="percepciones")


class Deduccion(Base):
    """Payroll deduction - Deducción de nómina"""
    __tablename__ = "nom_deduccion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("nom_nomina.id"), nullable=False)
    
    # Deduction details
    tipo_deduccion = Column(SQLEnum(TipoDeduccion), nullable=False)
    clave = Column(String(10), nullable=False)  # Deduction code
    concepto = Column(String(250), nullable=False)  # Description
    importe = Column(Numeric(12, 2), nullable=False)  # Amount deducted
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    nomina = relationship("Nomina", back_populates="deducciones")


class Incapacidad(Base):
    """Employee incapacity - Incapacidad del empleado"""
    __tablename__ = "nom_incapacidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("nom_nomina.id"), nullable=False)
    
    # Incapacity details
    tipo_incapacidad = Column(SQLEnum(TipoIncapacidad), nullable=False)
    dias_incapacidad = Column(Integer, nullable=False)  # Number of days
    descuento = Column(Numeric(12, 2), default=0.00)  # Amount discounted
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    nomina = relationship("Nomina", back_populates="incapacidades")


class OtroPago(Base):
    """Other payment - Otro pago"""
    __tablename__ = "nom_otro_pago"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("nom_nomina.id"), nullable=False)
    
    # Other payment details
    tipo_otro_pago = Column(String(10), nullable=False)  # SAT code for other payment
    clave = Column(String(10), nullable=False)  # Payment code
    concepto = Column(String(250), nullable=False)  # Description
    importe = Column(Numeric(12, 2), nullable=False)  # Amount
    
    # Subsidy details if applicable
    subsidio_causado = Column(Numeric(12, 2), default=0.00)  # Subsidy caused
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    nomina = relationship("Nomina", back_populates="otros_pagos")