"""
Human Resources CRUD Operations
Specialized for textile manufacturing companies
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID
from datetime import date

from app.models.hr import (
    Departamento, Puesto, Empleado, Contrato, Horario, Asistencia, 
    Vacacion, Incapacidad, SolicitudEquipo, Anuncio, VistaAnuncio, EmpleadoPuesto
)
from app.models.payroll import Nomina, PeriodoNomina, Percepcion, Deduccion  # Cambiar PeriodoPago a PeriodoNomina
from app.schemas.hr import (
    DepartamentoCreate, DepartamentoUpdate, DepartamentoResponse,
    PuestoCreate, PuestoUpdate, PuestoResponse,
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse,
    ContratoCreate, ContratoUpdate, ContratoResponse,
    HorarioCreate, HorarioUpdate, HorarioResponse,
    AsistenciaCreate, AsistenciaUpdate, AsistenciaResponse,
    VacacionCreate, VacacionUpdate, VacacionResponse,
    IncapacidadCreate, IncapacidadUpdate, IncapacidadResponse,
    SolicitudEquipoCreate, SolicitudEquipoUpdate, SolicitudEquipoResponse,
    AnuncioCreate, AnuncioUpdate, AnuncioResponse,
    VistaAnuncioCreate, VistaAnuncioResponse,
    EmpleadoPuestoCreate, EmpleadoPuestoUpdate, EmpleadoPuestoResponse
)
from app.schemas.payroll import (  # Añadir importaciones de esquemas de nómina
    NominaCreate, NominaUpdate, NominaResponse,
    PeriodoNominaCreate, PeriodoNominaUpdate, PeriodoNominaResponse,  # Cambiar PeriodoPago por PeriodoNomina
    PercepcionCreate, PercepcionUpdate, PercepcionResponse,
    DeduccionCreate, DeduccionUpdate, DeduccionResponse
)


# ============================================================================
# EMPLOYEE CRUD
# ============================================================================

def create_empleado(db: Session, empleado_data: EmpleadoCreate) -> Empleado:
    """Create a new employee"""
    db_empleado = Empleado(**empleado_data.model_dump())
    db.add(db_empleado)
    db.commit()
    db.refresh(db_empleado)
    return db_empleado


def get_empleado(db: Session, empleado_id: UUID) -> Optional[Empleado]:
    """Get an employee by ID"""
    return db.query(Empleado).filter(Empleado.id == empleado_id).first()


def get_empleado_by_codigo(db: Session, codigo: str) -> Optional[Empleado]:
    """Get an employee by code"""
    return db.query(Empleado).filter(Empleado.codigo == codigo).first()


def get_empleado_by_rfc(db: Session, rfc: str) -> Optional[Empleado]:
    """Get an employee by RFC"""
    return db.query(Empleado).filter(Empleado.rfc == rfc).first()


def get_empleados(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    departamento: Optional[str] = None,
    activo: Optional[bool] = None
) -> List[Empleado]:
    """Get list of employees, optionally filtered"""
    query = db.query(Empleado)
    
    if departamento:
        query = query.filter(Empleado.departamento == departamento)
    if activo is not None:
        query = query.filter(Empleado.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_empleado(
    db: Session, 
    empleado_id: UUID, 
    empleado_data: EmpleadoUpdate
) -> Optional[Empleado]:
    """Update an employee"""
    db_empleado = get_empleado(db, empleado_id)
    if db_empleado:
        update_data = empleado_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_empleado, field, value)
        db.commit()
        db.refresh(db_empleado)
    return db_empleado


def delete_empleado(db: Session, empleado_id: UUID) -> bool:
    """Delete an employee"""
    db_empleado = get_empleado(db, empleado_id)
    if db_empleado:
        db.delete(db_empleado)
        db.commit()
        return True
    return False


# ============================================================================
# CONTRACT CRUD
# ============================================================================

def create_contrato(db: Session, contrato_data: ContratoCreate) -> Contrato:
    """Create a new employment contract"""
    db_contrato = Contrato(**contrato_data.model_dump())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato


def get_contrato(db: Session, contrato_id: UUID) -> Optional[Contrato]:
    """Get a contract by ID"""
    return db.query(Contrato).filter(Contrato.id == contrato_id).first()


def get_contrato_by_numero(db: Session, numero_contrato: str) -> Optional[Contrato]:
    """Get a contract by number"""
    return db.query(Contrato).filter(Contrato.numero_contrato == numero_contrato).first()


def get_contratos_by_empleado(db: Session, empleado_id: UUID) -> List[Contrato]:
    """Get all contracts for a specific employee"""
    return db.query(Contrato).filter(Contrato.empleado_id == empleado_id).all()


def update_contrato(
    db: Session, 
    contrato_id: UUID, 
    contrato_data: ContratoUpdate
) -> Optional[Contrato]:
    """Update a contract"""
    db_contrato = get_contrato(db, contrato_id)
    if db_contrato:
        update_data = contrato_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contrato, field, value)
        db.commit()
        db.refresh(db_contrato)
    return db_contrato


def delete_contrato(db: Session, contrato_id: UUID) -> bool:
    """Delete a contract"""
    db_contrato = get_contrato(db, contrato_id)
    if db_contrato:
        db.delete(db_contrato)
        db.commit()
        return True
    return False


# ============================================================================
# EMPLOYEE POSITION ASSIGNMENT CRUD
# ============================================================================

def create_empleado_puesto(db: Session, puesto_data: EmpleadoPuestoCreate) -> EmpleadoPuesto:
    """Create a new employee position assignment"""
    db_puesto = EmpleadoPuesto(**puesto_data.model_dump())
    db.add(db_puesto)
    db.commit()
    db.refresh(db_puesto)
    return db_puesto


def get_empleado_puesto(db: Session, puesto_id: UUID) -> Optional[EmpleadoPuesto]:
    """Get an employee position assignment by ID"""
    return db.query(EmpleadoPuesto).filter(EmpleadoPuesto.id == puesto_id).first()


def get_empleado_puestos_activos(db: Session, empleado_id: UUID) -> List[EmpleadoPuesto]:
    """Get all active position assignments for an employee"""
    return db.query(EmpleadoPuesto).filter(
        EmpleadoPuesto.empleado_id == empleado_id,
        EmpleadoPuesto.activo == True
    ).all()


def update_empleado_puesto(
    db: Session, 
    puesto_id: UUID, 
    puesto_data: EmpleadoPuestoUpdate
) -> Optional[EmpleadoPuesto]:
    """Update an employee position assignment"""
    db_puesto = get_empleado_puesto(db, puesto_id)
    if db_puesto:
        update_data = puesto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_puesto, field, value)
        db.commit()
        db.refresh(db_puesto)
    return db_puesto


def delete_empleado_puesto(db: Session, puesto_id: UUID) -> bool:
    """Delete an employee position assignment"""
    db_puesto = get_empleado_puesto(db, puesto_id)
    if db_puesto:
        db.delete(db_puesto)
        db.commit()
        return True
    return False


# ============================================================================
# DEPARTMENT CRUD
# ============================================================================

def create_departamento(db: Session, departamento_data: DepartamentoCreate) -> Departamento:
    """Create a new department"""
    db_departamento = Departamento(**departamento_data.model_dump())
    db.add(db_departamento)
    db.commit()
    db.refresh(db_departamento)
    return db_departamento


def get_departamento(db: Session, departamento_id: UUID) -> Optional[Departamento]:
    """Get a department by ID"""
    return db.query(Departamento).filter(Departamento.id == departamento_id).first()


def get_departamento_by_codigo(db: Session, codigo: str) -> Optional[Departamento]:
    """Get a department by code"""
    return db.query(Departamento).filter(Departamento.codigo == codigo).first()


def get_departamentos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None
) -> List[Departamento]:
    """Get list of departments, optionally filtered"""
    query = db.query(Departamento)
    
    if activo is not None:
        query = query.filter(Departamento.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_departamento(
    db: Session, 
    departamento_id: UUID, 
    departamento_data: DepartamentoUpdate
) -> Optional[Departamento]:
    """Update a department"""
    db_departamento = get_departamento(db, departamento_id)
    if db_departamento:
        update_data = departamento_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_departamento, field, value)
        db.commit()
        db.refresh(db_departamento)
    return db_departamento


def delete_departamento(db: Session, departamento_id: UUID) -> bool:
    """Delete a department"""
    db_departamento = get_departamento(db, departamento_id)
    if db_departamento:
        db.delete(db_departamento)
        db.commit()
        return True
    return False


# ============================================================================
# POSITION CRUD
# ============================================================================

def create_puesto(db: Session, puesto_data: PuestoCreate) -> Puesto:
    """Create a new job position"""
    db_puesto = Puesto(**puesto_data.model_dump())
    db.add(db_puesto)
    db.commit()
    db.refresh(db_puesto)
    return db_puesto


def get_puesto(db: Session, puesto_id: UUID) -> Optional[Puesto]:
    """Get a job position by ID"""
    return db.query(Puesto).filter(Puesto.id == puesto_id).first()


def get_puesto_by_codigo(db: Session, codigo: str) -> Optional[Puesto]:
    """Get a job position by code"""
    return db.query(Puesto).filter(Puesto.codigo == codigo).first()


def get_puestos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    departamento: Optional[str] = None,
    activo: Optional[bool] = None
) -> List[Puesto]:
    """Get list of positions, optionally filtered"""
    query = db.query(Puesto)
    
    if departamento:
        query = query.filter(Puesto.departamento == departamento)
    if activo is not None:
        query = query.filter(Puesto.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_puesto(
    db: Session, 
    puesto_id: UUID, 
    puesto_data: PuestoUpdate
) -> Optional[Puesto]:
    """Update a job position"""
    db_puesto = get_puesto(db, puesto_id)
    if db_puesto:
        update_data = puesto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_puesto, field, value)
        db.commit()
        db.refresh(db_puesto)
    return db_puesto


def delete_puesto(db: Session, puesto_id: UUID) -> bool:
    """Delete a job position"""
    db_puesto = get_puesto(db, puesto_id)
    if db_puesto:
        db.delete(db_puesto)
        db.commit()
        return True
    return False


# ============================================================================
# SCHEDULE CRUD
# ============================================================================

def create_horario(db: Session, horario_data: HorarioCreate) -> Horario:
    """Create a new schedule"""
    db_horario = Horario(**horario_data.model_dump())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario


def get_horario(db: Session, horario_id: UUID) -> Optional[Horario]:
    """Get a schedule by ID"""
    return db.query(Horario).filter(Horario.id == horario_id).first()


def get_horarios_by_empleado(db: Session, empleado_id: UUID) -> List[Horario]:
    """Get all schedules for an employee"""
    return db.query(Horario).filter(Horario.empleado_id == empleado_id).all()


def update_horario(
    db: Session, 
    horario_id: UUID, 
    horario_data: HorarioUpdate
) -> Optional[Horario]:
    """Update a schedule"""
    db_horario = get_horario(db, horario_id)
    if db_horario:
        update_data = horario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_horario, field, value)
        db.commit()
        db.refresh(db_horario)
    return db_horario


def delete_horario(db: Session, horario_id: UUID) -> bool:
    """Delete a schedule"""
    db_horario = get_horario(db, horario_id)
    if db_horario:
        db.delete(db_horario)
        db.commit()
        return True
    return False


# ============================================================================
# ATTENDANCE CRUD
# ============================================================================

def create_asistencia(db: Session, asistencia_data: AsistenciaCreate) -> Asistencia:
    """Create a new attendance record"""
    db_asistencia = Asistencia(**asistencia_data.model_dump())
    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia


def get_asistencia(db: Session, asistencia_id: UUID) -> Optional[Asistencia]:
    """Get an attendance record by ID"""
    return db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()


def get_asistencias_by_empleado_fecha(
    db: Session, 
    empleado_id: UUID, 
    fecha_inicio: date, 
    fecha_fin: date
) -> List[Asistencia]:
    """Get attendance records for an employee within a date range"""
    return db.query(Asistencia).filter(
        Asistencia.empleado_id == empleado_id,
        Asistencia.fecha >= fecha_inicio,
        Asistencia.fecha <= fecha_fin
    ).all()


def get_asistencias_by_fecha(db: Session, fecha: date) -> List[Asistencia]:
    """Get all attendance records for a specific date"""
    return db.query(Asistencia).filter(Asistencia.fecha == fecha).all()


def update_asistencia(
    db: Session, 
    asistencia_id: UUID, 
    asistencia_data: AsistenciaUpdate
) -> Optional[Asistencia]:
    """Update an attendance record"""
    db_asistencia = get_asistencia(db, asistencia_id)
    if db_asistencia:
        update_data = asistencia_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_asistencia, field, value)
        db.commit()
        db.refresh(db_asistencia)
    return db_asistencia


def delete_asistencia(db: Session, asistencia_id: UUID) -> bool:
    """Delete an attendance record"""
    db_asistencia = get_asistencia(db, asistencia_id)
    if db_asistencia:
        db.delete(db_asistencia)
        db.commit()
        return True
    return False


# ============================================================================
# EQUIPMENT REQUEST CRUD
# ============================================================================

def create_solicitud_equipo(db: Session, solicitud_data: SolicitudEquipoCreate) -> SolicitudEquipo:
    """Create a new equipment request"""
    db_solicitud = SolicitudEquipo(**solicitud_data.model_dump())
    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud


def get_solicitud_equipo(db: Session, solicitud_id: UUID) -> Optional[SolicitudEquipo]:
    """Get an equipment request by ID"""
    return db.query(SolicitudEquipo).filter(SolicitudEquipo.id == solicitud_id).first()


def get_solicitudes_equipo_by_empleado(db: Session, empleado_id: UUID) -> List[SolicitudEquipo]:
    """Get all equipment requests for an employee"""
    return db.query(SolicitudEquipo).filter(SolicitudEquipo.empleado_id == empleado_id).all()


def update_solicitud_equipo(
    db: Session, 
    solicitud_id: UUID, 
    solicitud_data: SolicitudEquipoUpdate
) -> Optional[SolicitudEquipo]:
    """Update an equipment request"""
    db_solicitud = get_solicitud_equipo(db, solicitud_id)
    if db_solicitud:
        update_data = solicitud_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_solicitud, field, value)
        db.commit()
        db.refresh(db_solicitud)
    return db_solicitud


def delete_solicitud_equipo(db: Session, solicitud_id: UUID) -> bool:
    """Delete an equipment request"""
    db_solicitud = get_solicitud_equipo(db, solicitud_id)
    if db_solicitud:
        db.delete(db_solicitud)
        db.commit()
        return True
    return False


# ============================================================================
# MEDICAL LEAVE CRUD
# ============================================================================

def create_incapacidad(db: Session, incapacidad_data: IncapacidadCreate) -> Incapacidad:
    """Create a new medical leave record"""
    db_incapacidad = Incapacidad(**incapacidad_data.model_dump())
    db.add(db_incapacidad)
    db.commit()
    db.refresh(db_incapacidad)
    return db_incapacidad


def get_incapacidad(db: Session, incapacidad_id: UUID) -> Optional[Incapacidad]:
    """Get a medical leave record by ID"""
    return db.query(Incapacidad).filter(Incapacidad.id == incapacidad_id).first()


def get_incapacidades_by_empleado(
    db: Session, 
    empleado_id: UUID,
    estado: Optional[str] = None
) -> List[Incapacidad]:
    """Get all medical leaves for an employee, optionally filtered by state"""
    query = db.query(Incapacidad).filter(Incapacidad.empleado_id == empleado_id)
    if estado:
        query = query.filter(Incapacidad.estado == estado)
    return query.all()


def update_incapacidad(
    db: Session, 
    incapacidad_id: UUID, 
    incapacidad_data: IncapacidadUpdate
) -> Optional[Incapacidad]:
    """Update a medical leave record"""
    db_incapacidad = get_incapacidad(db, incapacidad_id)
    if db_incapacidad:
        update_data = incapacidad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_incapacidad, field, value)
        db.commit()
        db.refresh(db_incapacidad)
    return db_incapacidad


def delete_incapacidad(db: Session, incapacidad_id: UUID) -> bool:
    """Delete a medical leave record"""
    db_incapacidad = get_incapacidad(db, incapacidad_id)
    if db_incapacidad:
        db.delete(db_incapacidad)
        db.commit()
        return True
    return False


# ============================================================================
# ANNOUNCEMENT CRUD
# ============================================================================

def create_anuncio(db: Session, anuncio_data: AnuncioCreate) -> Anuncio:
    """Create a new announcement"""
    db_anuncio = Anuncio(**anuncio_data.model_dump())
    db.add(db_anuncio)
    db.commit()
    db.refresh(db_anuncio)
    return db_anuncio


def get_anuncio(db: Session, anuncio_id: UUID) -> Optional[Anuncio]:
    """Get an announcement by ID"""
    return db.query(Anuncio).filter(Anuncio.id == anuncio_id).first()


def get_anuncios(db: Session, skip: int = 0, limit: int = 100) -> List[Anuncio]:
    """Get list of announcements"""
    return db.query(Anuncio).filter(Anuncio.activo == True).offset(skip).limit(limit).all()


def update_anuncio(
    db: Session, 
    anuncio_id: UUID, 
    anuncio_data: AnuncioUpdate
) -> Optional[Anuncio]:
    """Update an announcement"""
    db_anuncio = get_anuncio(db, anuncio_id)
    if db_anuncio:
        update_data = anuncio_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_anuncio, field, value)
        db.commit()
        db.refresh(db_anuncio)
    return db_anuncio


def delete_anuncio(db: Session, anuncio_id: UUID) -> bool:
    """Delete an announcement (soft delete)"""
    db_anuncio = get_anuncio(db, anuncio_id)
    if db_anuncio:
        db_anuncio.activo = False
        db_anuncio.deleted_at = func.now()
        db.commit()
        db.refresh(db_anuncio)
        return True
    return False


# ============================================================================
# VACATION CRUD
# ============================================================================

def create_vacacion(db: Session, vacacion_data: VacacionCreate) -> Vacacion:
    """Create a new vacation record"""
    db_vacacion = Vacacion(**vacacion_data.model_dump())
    db.add(db_vacacion)
    db.commit()
    db.refresh(db_vacacion)
    return db_vacacion


def get_vacacion(db: Session, vacacion_id: UUID) -> Optional[Vacacion]:
    """Get a vacation record by ID"""
    return db.query(Vacacion).filter(Vacacion.id == vacacion_id).first()


def get_vacaciones_by_empleado(
    db: Session, 
    empleado_id: UUID,
    anio: Optional[int] = None,
    estado: Optional[str] = None
) -> List[Vacacion]:
    """Get all vacations for an employee, optionally filtered by year and state"""
    query = db.query(Vacacion).filter(Vacacion.empleado_id == empleado_id)
    if anio:
        query = query.filter(Vacacion.anio == anio)
    if estado:
        query = query.filter(Vacacion.estado == estado)
    return query.all()


def update_vacacion(
    db: Session, 
    vacacion_id: UUID, 
    vacacion_data: VacacionUpdate
) -> Optional[Vacacion]:
    """Update a vacation record"""
    db_vacacion = get_vacacion(db, vacacion_id)
    if db_vacacion:
        update_data = vacacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vacacion, field, value)
        db.commit()
        db.refresh(db_vacacion)
    return db_vacacion


def delete_vacacion(db: Session, vacacion_id: UUID) -> bool:
    """Delete a vacation record"""
    db_vacacion = get_vacacion(db, vacacion_id)
    if db_vacacion:
        db.delete(db_vacacion)
        db.commit()
        return True
    return False


# ============================================================================
# ANNOUNCEMENT VIEW CRUD
# ============================================================================

def create_vista_anuncio(db: Session, vista_data: VistaAnuncioCreate) -> VistaAnuncio:
    """Register an announcement view"""
    db_vista = VistaAnuncio(**vista_data.model_dump())
    db.add(db_vista)
    db.commit()
    db.refresh(db_vista)
    return db_vista


def get_vista_anuncio(db: Session, vista_id: UUID) -> Optional[VistaAnuncio]:
    """Get an announcement view by ID"""
    return db.query(VistaAnuncio).filter(VistaAnuncio.id == vista_id).first()


def get_vistas_anuncio_by_anuncio(db: Session, anuncio_id: UUID) -> List[VistaAnuncio]:
    """Get all views for an announcement"""
    return db.query(VistaAnuncio).filter(VistaAnuncio.anuncio_id == anuncio_id).all()


def get_vistas_anuncio_by_empleado(db: Session, empleado_id: UUID) -> List[VistaAnuncio]:
    """Get all announcement views for an employee"""
    return db.query(VistaAnuncio).filter(VistaAnuncio.empleado_id == empleado_id).all()


# ============================================================================
# PAYROLL CRUD
# ============================================================================

def create_nomina(db: Session, nomina_data: NominaCreate) -> Nomina:
    """Create a new payroll record"""
    db_nomina = Nomina(**nomina_data.model_dump())
    db.add(db_nomina)
    db.commit()
    db.refresh(db_nomina)
    return db_nomina


def get_nomina(db: Session, nomina_id: UUID) -> Optional[Nomina]:
    """Get a payroll record by ID"""
    return db.query(Nomina).filter(Nomina.id == nomina_id).first()


def get_nominas_by_empleado(
    db: Session, 
    empleado_id: UUID,
    periodo_pago_id: Optional[UUID] = None
) -> List[Nomina]:
    """Get all payroll records for an employee, optionally filtered by period"""
    query = db.query(Nomina).filter(Nomina.empleado_id == empleado_id)
    if periodo_pago_id:
        query = query.filter(Nomina.periodo_pago_id == periodo_pago_id)
    return query.all()


def update_nomina(
    db: Session, 
    nomina_id: UUID, 
    nomina_data: NominaUpdate
) -> Optional[Nomina]:
    """Update a payroll record"""
    db_nomina = get_nomina(db, nomina_id)
    if db_nomina:
        update_data = nomina_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_nomina, field, value)
        db.commit()
        db.refresh(db_nomina)
    return db_nomina


def delete_nomina(db: Session, nomina_id: UUID) -> bool:
    """Delete a payroll record"""
    db_nomina = get_nomina(db, nomina_id)
    if db_nomina:
        db.delete(db_nomina)
        db.commit()
        return True
    return False


# ============================================================================
# PAYROLL PERIOD CRUD
# ============================================================================

def create_periodo_pago(db: Session, periodo_data: PeriodoNominaCreate) -> PeriodoNomina:
    """Create a new payroll period"""
    db_periodo = PeriodoNomina(**periodo_data.model_dump())
    db.add(db_periodo)
    db.commit()
    db.refresh(db_periodo)
    return db_periodo


def get_periodo_pago(db: Session, periodo_id: UUID) -> Optional[PeriodoNomina]:
    """Get a payroll period by ID"""
    return db.query(PeriodoNomina).filter(PeriodoNomina.id == periodo_id).first()


def get_periodo_pago_by_codigo(db: Session, codigo: str) -> Optional[PeriodoNomina]:
    """Get a payroll period by code"""
    return db.query(PeriodoNomina).filter(PeriodoNomina.codigo == codigo).first()


def get_periodos_pago(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tipo_periodo: Optional[str] = None,
    cerrado: Optional[bool] = None
) -> List[PeriodoNomina]:
    """Get list of payroll periods, optionally filtered"""
    query = db.query(PeriodoNomina)
    
    if tipo_periodo:
        query = query.filter(PeriodoNomina.tipo_periodo == tipo_periodo)
    if cerrado is not None:
        query = query.filter(PeriodoNomina.cerrado == cerrado)
    
    return query.offset(skip).limit(limit).all()


def update_periodo_pago(
    db: Session, 
    periodo_id: UUID, 
    periodo_data: PeriodoNominaUpdate
) -> Optional[PeriodoNomina]:
    """Update a payroll period"""
    db_periodo = get_periodo_pago(db, periodo_id)
    if db_periodo:
        update_data = periodo_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_periodo, field, value)
        db.commit()
        db.refresh(db_periodo)
    return db_periodo


def delete_periodo_pago(db: Session, periodo_id: UUID) -> bool:
    """Delete a payroll period"""
    db_periodo = get_periodo_pago(db, periodo_id)
    if db_periodo:
        db.delete(db_periodo)
        db.commit()
        return True
    return False


# ============================================================================
# EARNINGS CRUD
# ============================================================================

def create_percepcion(db: Session, percepcion_data: PercepcionCreate) -> Percepcion:
    """Create a new earning record"""
    db_percepcion = Percepcion(**percepcion_data.model_dump())
    db.add(db_percepcion)
    db.commit()
    db.refresh(db_percepcion)
    return db_percepcion


def get_percepcion(db: Session, percepcion_id: UUID) -> Optional[Percepcion]:
    """Get an earning record by ID"""
    return db.query(Percepcion).filter(Percepcion.id == percepcion_id).first()


def get_percepciones_by_nomina(db: Session, nomina_id: UUID) -> List[Percepcion]:
    """Get all earnings for a specific payroll record"""
    return db.query(Percepcion).filter(Percepcion.nomina_id == nomina_id).all()


def update_percepcion(
    db: Session, 
    percepcion_id: UUID, 
    percepcion_data: PercepcionUpdate
) -> Optional[Percepcion]:
    """Update an earning record"""
    db_percepcion = get_percepcion(db, percepcion_id)
    if db_percepcion:
        update_data = percepcion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_percepcion, field, value)
        db.commit()
        db.refresh(db_percepcion)
    return db_percepcion


def delete_percepcion(db: Session, percepcion_id: UUID) -> bool:
    """Delete an earning record"""
    db_percepcion = get_percepcion(db, percepcion_id)
    if db_percepcion:
        db.delete(db_percepcion)
        db.commit()
        return True
    return False


# ============================================================================
# DEDUCTIONS CRUD
# ============================================================================

def create_deduccion(db: Session, deduccion_data: DeduccionCreate) -> Deduccion:
    """Create a new deduction record"""
    db_deduccion = Deduccion(**deduccion_data.model_dump())
    db.add(db_deduccion)
    db.commit()
    db.refresh(db_deduccion)
    return db_deduccion


def get_deduccion(db: Session, deduccion_id: UUID) -> Optional[Deduccion]:
    """Get a deduction record by ID"""
    return db.query(Deduccion).filter(Deduccion.id == deduccion_id).first()


def get_deducciones_by_nomina(db: Session, nomina_id: UUID) -> List[Deduccion]:
    """Get all deductions for a specific payroll record"""
    return db.query(Deduccion).filter(Deduccion.nomina_id == nomina_id).all()


def update_deduccion(
    db: Session, 
    deduccion_id: UUID, 
    deduccion_data: DeduccionUpdate
) -> Optional[Deduccion]:
    """Update a deduction record"""
    db_deduccion = get_deduccion(db, deduccion_id)
    if db_deduccion:
        update_data = deduccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_deduccion, field, value)
        db.commit()
        db.refresh(db_deduccion)
    return db_deduccion


def delete_deduccion(db: Session, deduccion_id: UUID) -> bool:
    """Delete a deduction record"""
    db_deduccion = get_deduccion(db, deduccion_id)
    if db_deduccion:
        db.delete(db_deduccion)
        db.commit()
        return True
    return False