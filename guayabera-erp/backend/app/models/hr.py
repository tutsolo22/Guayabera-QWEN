"""
Human Resources Models: Employees, payroll, attendance, contracts
Specialized for textile manufacturing companies
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

class TipoEmpleado(enum.Enum):
    PERMANENTE = "permanente"
    TEMPORAL = "temporal"
    CONTRATISTA = "contratista"
    APRENDIZ = "aprendiz"


class Departamento(enum.Enum):
    PRODUCCION = "produccion"
    DISENO = "diseno"
    ADMINISTRACION = "administracion"
    VENTAS = "ventas"
    ALMACEN = "almacen"
    RECURSOS_HUMANOS = "recursos_humanos"
    CONTABILIDAD = "contabilidad"
    SISTEMAS = "sistemas"


class EstadoCivil(enum.Enum):
    SOLTERO = "soltero"
    CASADO = "casado"
    DIVORCIADO = "divorciado"
    UNION_LIBRE = "union_libre"
    VIUDO = "viudo"


class Sexo(enum.Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"


class TipoContrato(enum.Enum):
    POR_TIEMPO_INDETERMINADO = "por_tiempo_indeterminado"
    POR_TIEMPO_DETERMINADO = "por_tiempo_determinado"
    OBRA_O_SERVICIO = "obra_o_servicio"
    PRACTICAS_PROFESIONALES = "practicas_profesionales"
    FORMACION_ACADDEMICA = "formacion_academica"


class TipoNomina(enum.Enum):
    ORDINARIA = "ordinaria"
    EXTRAORDINARIA = "extraordinaria"
    ESPECIAL = "especial"


class TipoPercepcion(enum.Enum):
    SUELDO_BASE = "sueldo_base"
    SUELDO_VARIABLE = "sueldo_variable"
    HORAS_EXTRA = "horas_extra"
    PRIMA_DOMINICAL = "prima_dominical"
    PRIMA_VACACIONAL = "prima_vacacional"
    AGUINALDO = "aguinaldo"
    BONO_ANUAL = "bono_anual"
    OTROS_INGRESOS = "otros_ingresos"


class TipoDeduccion(enum.Enum):
    ISR = "isr"
    SEGURIDAD_SOCIAL = "seguridad_social"
    AFORE = "afore"
    INFONAVIT = "infonavit"
    PRESTAMOS = "prestamos"
    OTROS = "otros"


class EstadoAsistencia(enum.Enum):
    PRESENTE = "presente"
    AUSENTE = "ausente"
    PERMISO = "permiso"
    VACACIONES = "vacaciones"
    ENFERMEDAD = "enfermedad"
    FESTIVO = "festivo"


# ============================================================================
# EMPLOYEE MANAGEMENT (GESTIÓN DE EMPLEADOS)
# ============================================================================

class Empleado(Base):
    """Employee management - Gestión de empleados"""
    __tablename__ = "rh_empleado"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic identification
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    nombre_completo = Column(String(300), nullable=False)
    
    # Personal information
    fecha_nacimiento = Column(Date)
    sexo = Column(SQLEnum(Sexo))
    estado_civil = Column(SQLEnum(EstadoCivil))
    nacionalidad = Column(String(50), default="Mexicana")
    lugar_nacimiento = Column(String(100))
    
    # Contact information
    email_personal = Column(String(100))
    email_corporativo = Column(String(100))
    telefono_personal = Column(String(20))
    telefono_corporativo = Column(String(20))
    celular = Column(String(20))
    
    # Address
    calle = Column(String(200))
    numero_exterior = Column(String(20))
    numero_interior = Column(String(20))
    colonia = Column(String(100))
    ciudad = Column(String(100))
    estado = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    
    # Job information
    tipo_empleado = Column(SQLEnum(TipoEmpleado), default=TipoEmpleado.PERMANENTE)
    departamento = Column(SQLEnum(Departamento), nullable=False)
    puesto = Column(String(100), nullable=False)
    jefe_inmediato_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    fecha_contratacion = Column(Date, nullable=False)
    fecha_inicio_labores = Column(Date)
    fecha_baja = Column(Date)
    
    # Fiscal information (Mexican tax system)
    rfc = Column(String(13), unique=True, index=True)
    curp = Column(String(18), unique=True, index=True)
    numero_seguro_social = Column(String(11), unique=True)
    clabe_bancaria = Column(String(18))
    banco_pago = Column(String(100))
    
    # Payroll information
    salario_diario = Column(Numeric(10, 2))
    salario_integrado = Column(Numeric(10, 2))
    riesgo_puesto = Column(Integer, default=1)  # Risk level 1-5
    tipo_contrato = Column(SQLEnum(TipoContrato), default=TipoContrato.POR_TIEMPO_INDETERMINADO)
    regimen_contratacion = Column(String(100), default="Base")
    sindicalizado = Column(Boolean, default=False)
    
    # Status
    activo = Column(Boolean, default=True)
    fecha_ultimo_movimiento = Column(DateTime(timezone=True))
    
    # Metadata
    comentarios = Column(Text)
    foto_perfil = Column(String(500))  # URL to employee photo
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    jefe_inmediato = relationship("Empleado", remote_side=[id], backref="subordinados")
    contratos = relationship("Contrato", back_populates="empleado")
    puestos = relationship("EmpleadoPuesto", back_populates="empleado")
    asistencias = relationship("Asistencia", back_populates="empleado")
    incapacidades = relationship("Incapacidad", back_populates="empleado")
    vacaciones = relationship("Vacacion", back_populates="empleado")
    nominas = relationship("Nomina", back_populates="empleado")


class Contrato(Base):
    """Employment contract - Contrato de trabajo"""
    __tablename__ = "rh_contrato"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Contract details
    numero_contrato = Column(String(50), unique=True, nullable=False)
    tipo_contrato = Column(SQLEnum(TipoContrato), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)  # Nullable for indefinite contracts
    duracion_dias = Column(Integer)  # Calculated based on dates
    
    # Labor conditions
    salario_diario = Column(Numeric(10, 2), nullable=False)
    descripcion_funciones = Column(Text)
    lugar_trabajo = Column(String(200))
    horario_trabajo = Column(String(100))
    
    # Status and documents
    estado = Column(String(20), default="activo")  # activo, vencido, cancelado
    archivo_contrato = Column(String(500))  # Path to contract file
    comentarios = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    empleado = relationship("Empleado", back_populates="contratos")


class EmpleadoPuesto(Base):
    """Employee position assignment - Asignación de puesto"""
    __tablename__ = "rh_empleado_puesto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    puesto_id = Column(UUID(as_uuid=True), ForeignKey("rh_puesto.id"), nullable=False)
    
    # Assignment details
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    descripcion_responsabilidades = Column(Text)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    empleado = relationship("Empleado", back_populates="puestos")
    puesto = relationship("Puesto")


class Puesto(Base):
    """Job position - Puesto laboral"""
    __tablename__ = "rh_puesto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Position details
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    departamento = Column(SQLEnum(Departamento), nullable=False)
    
    # Requirements
    nivel_autoridad = Column(Integer, default=1)  # 1-10 scale
    nivel_responsabilidad = Column(Integer, default=1)  # 1-10 scale
    habilidades_requeridas = Column(JSONB)  # Skills required in JSON format
    experiencia_requerida = Column(Integer)  # Years of experience
    
    # Compensation
    salario_minimo = Column(Numeric(10, 2))
    salario_maximo = Column(Numeric(10, 2))
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


# ============================================================================
# ATTENDANCE AND TIME TRACKING (CONTROL DE ASISTENCIA)
# ============================================================================

class Asistencia(Base):
    """Attendance tracking - Control de asistencia"""
    __tablename__ = "rh_asistencia"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Attendance details
    fecha = Column(Date, nullable=False)
    hora_entrada = Column(DateTime(timezone=True))  # First entry of the day
    hora_salida = Column(DateTime(timezone=True))   # Last exit of the day
    estado = Column(SQLEnum(EstadoAsistencia), default=EstadoAsistencia.PRESENTE)
    
    # Break times
    hora_entrada_comida = Column(DateTime(timezone=True))
    hora_salida_comida = Column(DateTime(timezone=True))
    
    # Additional time tracking
    horas_extras = Column(Float, default=0.0)  # Hours worked beyond standard
    minutos_tarde = Column(Integer, default=0)  # Minutes late arrival
    minutos_temprano = Column(Integer, default=0)  # Minutes early departure
    
    # Status
    verificada = Column(Boolean, default=False)  # Verified by supervisor
    autorizada = Column(Boolean, default=False)  # Authorized if irregularities
    
    # Metadata
    comentarios = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    empleado = relationship("Empleado", back_populates="asistencias")


class Incapacidad(Base):
    """Medical leave - Incapacidad médica"""
    __tablename__ = "rh_incapacidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Leave details
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    duracion_dias = Column(Integer, nullable=False)  # Calculated from dates
    tipo_incapacidad = Column(String(50), nullable=False)  # Enfermedad general, accidente, maternidad
    causa = Column(String(200))
    clave_tipo_incapacidad = Column(String(10))  # SAT classification
    
    # Medical information
    numero_documento = Column(String(50))  # Medical certificate number
    institucion_emisora = Column(String(100))  # Issuing institution
    firma_autorizada = Column(String(100))  # Authorized signature
    
    # Status
    estado = Column(String(20), default="activa")  # activa, concluida, cancelada
    verificada = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    archivo_documento = Column(String(500))  # Path to medical certificate
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    empleado = relationship("Empleado", back_populates="incapacidades")


class Vacacion(Base):
    """Vacation tracking - Control de vacaciones"""
    __tablename__ = "rh_vacacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Vacation details
    anio = Column(Integer, nullable=False)  # Year for vacation period
    periodo_inicio = Column(Date, nullable=False)  # Start date of vacation period
    periodo_fin = Column(Date, nullable=False)  # End date of vacation period
    dias_correspondientes = Column(Integer, nullable=False)  # Days entitled
    dias_disfrutados = Column(Integer, default=0)  # Days actually taken
    dias_pendientes = Column(Integer, nullable=False)  # Remaining days
    
    # Request details
    fecha_solicitud = Column(Date, nullable=False)
    fecha_inicio_disfrute = Column(Date, nullable=False)
    fecha_fin_disfrute = Column(Date, nullable=False)
    dias_a_disfrutar = Column(Integer, nullable=False)  # Days to be taken
    motivo = Column(String(200))
    
    # Authorization
    autorizado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    fecha_autorizacion = Column(DateTime(timezone=True))
    estado = Column(String(20), default="pendiente")  # pendiente, autorizado, rechazado
    
    # Payment details
    pago_calculado = Column(Numeric(10, 2))  # Calculated payment amount
    pago_real = Column(Numeric(10, 2))  # Actual payment amount
    fecha_pago = Column(Date)  # Date of payment
    
    # Metadata
    comentarios = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    empleado = relationship("Empleado", back_populates="vacaciones")
    autorizado_por = relationship("Empleado", remote_side=[id])


# ============================================================================
# PAYROLL (NÓMINA)
# ============================================================================

class Nomina(Base):
    """Payroll records - Nóminas"""
    __tablename__ = "rh_nomina"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    periodo_pago_id = Column(UUID(as_uuid=True), ForeignKey("rh_periodo_pago.id"), nullable=False)
    
    # Payroll details
    tipo_nomina = Column(SQLEnum(TipoNomina), default=TipoNomina.ORDINARIA)
    numero_nota = Column(String(50))  # Payroll note number
    fecha_pago = Column(Date, nullable=False)
    fecha_inicial_pago = Column(Date, nullable=False)  # Start of payment period
    fecha_final_pago = Column(Date, nullable=False)  # End of payment period
    
    # Earnings
    percepciones_totales = Column(Numeric(12, 2), default=0.00)
    horas_extras_pagadas = Column(Numeric(10, 2), default=0.00)
    bonos_pagados = Column(Numeric(10, 2), default=0.00)
    
    # Deductions
    deducciones_totales = Column(Numeric(12, 2), default=0.00)
    isr_retencion = Column(Numeric(10, 2), default=0.00)
    seguridad_social_descuento = Column(Numeric(10, 2), default=0.00)
    infonavit_descuento = Column(Numeric(10, 2), default=0.00)
    otros_descuentos = Column(Numeric(10, 2), default=0.00)
    
    # Net amounts
    subsidio_causado = Column(Numeric(10, 2), default=0.00)  # Government subsidy
    subsidio_entregado = Column(Numeric(10, 2), default=0.00)  # Actually delivered
    total_otro_pago = Column(Numeric(10, 2), default=0.00)  # Other payments
    importe_total_neto = Column(Numeric(12, 2), default=0.00)  # Final net amount
    
    # CFDI fields (Mexican tax receipt)
    uuid_cfdi = Column(String(36))  # UUID of the tax receipt
    folio_fiscal = Column(String(36))  # Fiscal folio number
    fecha_timbrado = Column(DateTime(timezone=True))  # Date of tax stamp
    sello_digital_cfdi = Column(Text)  # Digital seal
    cadena_original = Column(Text)  # Original string for validation
    
    # Status
    estado = Column(String(20), default="emitida")  # emitida, cancelada, pagada
    fecha_cancelacion = Column(DateTime(timezone=True))
    motivo_cancelacion = Column(String(200))
    
    # Metadata
    comentarios = Column(Text)
    archivo_xml = Column(String(500))  # Path to XML file
    archivo_pdf = Column(String(500))  # Path to PDF file
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    empleado = relationship("Empleado", back_populates="nominas")
    periodo_pago = relationship("PeriodoPago")


class PeriodoPago(Base):
    """Payroll periods - Periodos de nómina"""
    __tablename__ = "rh_periodo_pago"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Period details
    nombre = Column(String(100), nullable=False)  # e.g., "Quincena 1 Enero 2023"
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    descripcion = Column(Text)
    
    # Dates
    fecha_inicio_periodo = Column(Date, nullable=False)
    fecha_fin_periodo = Column(Date, nullable=False)
    fecha_pago_nomina = Column(Date, nullable=False)  # Scheduled payment date
    
    # Type and frequency
    tipo_periodo = Column(String(20), nullable=False)  # quincenal, mensual, semanal
    frecuencia_pago = Column(Integer, default=2)  # Number of payments per month
    
    # Status
    cerrado = Column(Boolean, default=False)  # If period is closed for modifications
    fecha_cierre = Column(DateTime(timezone=True))  # Date when period was closed
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Percepcion(Base):
    """Payroll earnings - Percepciones de nómina"""
    __tablename__ = "rh_percepcion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("rh_nomina.id"), nullable=False)
    
    # Earning details
    tipo_percepcion = Column(SQLEnum(TipoPercepcion), nullable=False)
    clave = Column(String(20), nullable=False)  # SAT key
    concepto = Column(String(200), nullable=False)  # Description
    importe_gravado = Column(Numeric(10, 2), default=0.00)  # Taxable amount
    importe_exento = Column(Numeric(10, 2), default=0.00)  # Exempt amount
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    nomina = relationship("Nomina")


class Deduccion(Base):
    """Payroll deductions - Deducciones de nómina"""
    __tablename__ = "rh_deduccion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nomina_id = Column(UUID(as_uuid=True), ForeignKey("rh_nomina.id"), nullable=False)
    
    # Deduction details
    tipo_deduccion = Column(SQLEnum(TipoDeduccion), nullable=False)
    clave = Column(String(20), nullable=False)  # SAT key
    concepto = Column(String(200), nullable=False)  # Description
    importe = Column(Numeric(10, 2), nullable=False)  # Amount deducted
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    nomina = relationship("Nomina")


# ============================================================================
# MODELOS ESPECÍFICOS DE RECURSOS HUMANOS
# ============================================================================

class Anuncio(Base):
    """Anuncios del tablón de anuncios de RH - Announcements board for HR"""
    __tablename__ = "rh_anuncio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    tipo = Column(String(50), nullable=False)  # capacitacion, noticia, evento, etc.
    fecha_publicacion = Column(Date, nullable=False, default=func.current_date())
    fecha_expiracion = Column(Date)
    publico = Column(Boolean, default=True)  # Si es visible para todos o solo para ciertos roles
    
    # Relación con empleados que han visto el anuncio
    vistas = relationship("VistaAnuncio", back_populates="anuncio")
    
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class VistaAnuncio(Base):
    """Registro de vistas de anuncios por empleado - Record of announcements viewed by employee"""
    __tablename__ = "rh_vista_anuncio"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    anuncio_id = Column(UUID(as_uuid=True), ForeignKey("rh_anuncio.id"), nullable=False)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    fecha_vista = Column(DateTime(timezone=True), server_default=func.now())
    
    anuncio = relationship("Anuncio", back_populates="vistas")
    empleado = relationship("Empleado")


class Vacacion(Base):
    """Vacaciones de los empleados - Employee vacations"""
    __tablename__ = "rh_vacacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    dias_solicitados = Column(Integer, nullable=False)
    estado = Column(String(20), default="pendiente")  # pendiente, aprobado, rechazado, cancelado
    comentarios = Column(Text)
    fecha_aprobacion = Column(DateTime(timezone=True))
    aprobado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    
    empleado = relationship("Empleado", foreign_keys=[empleado_id])
    aprobador = relationship("Empleado", foreign_keys=[aprobado_por_id])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Incapacidad(Base):
    """Incapacidades de los empleados - Employee disabilities/medical leaves"""
    __tablename__ = "rh_incapacidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    tipo_incapacidad = Column(String(50), nullable=False)  # enfermedad, accidente, maternidad, etc.
    documento_soporte = Column(String(500))  # Ruta al archivo digital subido
    estado = Column(String(20), default="registrado")  # registrado, aprobado, rechazado
    comentarios = Column(Text)
    
    empleado = relationship("Empleado")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SolicitudEquipo(Base):
    """Solicitudes de equipo de cómputo - Computer equipment requests"""
    __tablename__ = "rh_solicitud_equipo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    tipo_equipo = Column(String(100), nullable=False)  # laptop, desktop, monitor, etc.
    descripcion_equipo = Column(Text)
    estado_equipo = Column(String(20), default="nuevo")  # nuevo, heredado
    necesita_correo = Column(Boolean, default=False)
    tipo_correo = Column(String(20), default="nuevo")  # nuevo, heredado
    departamento_destino = Column(String(100), nullable=False)
    empleado_asignado_nombre = Column(String(200), nullable=False)
    jefe_departamento_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    carpetas_compartidas = Column(Boolean, default=False)
    descripcion_carpetas = Column(Text)
    estado = Column(String(20), default="pendiente")  # pendiente, aprobado, rechazado, entregado
    
    empleado = relationship("Empleado", foreign_keys=[empleado_id])
    jefe_departamento = relationship("Empleado", foreign_keys=[jefe_departamento_id])
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

