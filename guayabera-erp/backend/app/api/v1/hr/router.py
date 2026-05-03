"""
Human Resources API Router
Specialized for textile manufacturing companies
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.schemas.hr import (
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse,
    ContratoCreate, ContratoUpdate, ContratoResponse,
    EmpleadoPuestoCreate, EmpleadoPuestoUpdate, EmpleadoPuestoResponse,
    PuestoCreate, PuestoUpdate, PuestoResponse,
    AsistenciaCreate, AsistenciaUpdate, AsistenciaResponse,
    IncapacidadCreate, IncapacidadUpdate, IncapacidadResponse,
    VacacionCreate, VacacionUpdate, VacacionResponse,
    NominaCreate, NominaUpdate, NominaResponse,
    PeriodoPagoCreate, PeriodoPagoUpdate, PeriodoPagoResponse,
    PercepcionCreate, PercepcionUpdate, PercepcionResponse,
    DeduccionCreate, DeduccionUpdate, DeduccionResponse
)
from app.crud.hr import (
    create_empleado, get_empleado, get_empleado_by_codigo, get_empleado_by_rfc,
    get_empleados, update_empleado, delete_empleado,
    create_contrato, get_contrato, get_contrato_by_numero,
    get_contratos_by_empleado, update_contrato, delete_contrato,
    create_empleado_puesto, get_empleado_puesto, get_empleado_puestos_activos,
    update_empleado_puesto, delete_empleado_puesto,
    create_puesto, get_puesto, get_puesto_by_codigo,
    get_puestos, update_puesto, delete_puesto,
    create_asistencia, get_asistencia, get_asistencias_by_empleado_fecha,
    get_asistencias_by_fecha, update_asistencia, delete_asistencia,
    create_incapacidad, get_incapacidad, get_incapacidades_by_empleado,
    update_incapacidad, delete_incapacidad,
    create_vacacion, get_vacacion, get_vacaciones_by_empleado,
    update_vacacion, delete_vacacion,
    create_nomina, get_nomina, get_nominas_by_empleado,
    update_nomina, delete_nomina,
    create_periodo_pago, get_periodo_pago, get_periodo_pago_by_codigo,
    get_periodos_pago, update_periodo_pago, delete_periodo_pago,
    create_percepcion, get_percepcion, get_percepciones_by_nomina,
    update_percepcion, delete_percepcion,
    create_deduccion, get_deduccion, get_deducciones_by_nomina,
    update_deduccion, delete_deduccion
)

router = APIRouter(prefix="/hr", tags=["Human Resources"])

# ============================================================================
# EMPLOYEE ENDPOINTS
# ============================================================================

@router.post("/employees/", response_model=EmpleadoResponse)
def create_employee(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    # Check if employee code already exists
    existing_empleado = get_empleado_by_codigo(db, empleado.codigo)
    if existing_empleado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this code already exists"
        )
    
    # Check if RFC already exists
    if empleado.rfc:
        existing_rfc = get_empleado_by_rfc(db, empleado.rfc)
        if existing_rfc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee with this RFC already exists"
            )
    
    return create_empleado(db=db, empleado_data=empleado)


@router.get("/employees/{empleado_id}", response_model=EmpleadoResponse)
def get_employee(empleado_id: str, db: Session = Depends(get_db)):
    """Get an employee by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    empleado = get_empleado(db, uuid_obj)
    if not empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return empleado


@router.get("/employees/", response_model=List[EmpleadoResponse])
def get_employees(
    skip: int = 0, 
    limit: int = 100,
    departamento: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of employees, optionally filtered"""
    return get_empleados(
        db, 
        skip=skip, 
        limit=limit, 
        departamento=departamento, 
        activo=activo
    )


@router.put("/employees/{empleado_id}", response_model=EmpleadoResponse)
def update_employee(
    empleado_id: str, 
    empleado_data: EmpleadoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an employee"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    updated_empleado = update_empleado(
        db=db, 
        empleado_id=uuid_obj, 
        empleado_data=empleado_data
    )
    if not updated_empleado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return updated_empleado


@router.delete("/employees/{empleado_id}")
def delete_employee(empleado_id: str, db: Session = Depends(get_db)):
    """Delete an employee"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    success = delete_empleado(db=db, empleado_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    return {"message": "Employee deleted successfully"}


# ============================================================================
# CONTRACT ENDPOINTS
# ============================================================================

@router.post("/contracts/", response_model=ContratoResponse)
def create_contract(contract: ContratoCreate, db: Session = Depends(get_db)):
    """Create a new employment contract"""
    # Check if contract number already exists
    existing_contract = get_contrato_by_numero(db, contract.numero_contrato)
    if existing_contract:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contract with this number already exists"
        )
    
    return create_contrato(db=db, contrato_data=contract)


@router.get("/contracts/{contrato_id}", response_model=ContratoResponse)
def get_contract(contrato_id: str, db: Session = Depends(get_db)):
    """Get a contract by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid contract ID format")
    
    contrato = get_contrato(db, uuid_obj)
    if not contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    return contrato


@router.get("/employees/{empleado_id}/contracts", response_model=List[ContratoResponse])
def get_employee_contracts(empleado_id: str, db: Session = Depends(get_db)):
    """Get all contracts for a specific employee"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    return get_contratos_by_empleado(db, uuid_obj)


@router.put("/contracts/{contrato_id}", response_model=ContratoResponse)
def update_contract(
    contrato_id: str, 
    contrato_data: ContratoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a contract"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid contract ID format")
    
    updated_contrato = update_contrato(
        db=db, 
        contrato_id=uuid_obj, 
        contrato_data=contrato_data
    )
    if not updated_contrato:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    return updated_contrato


@router.delete("/contracts/{contrato_id}")
def delete_contract(contrato_id: str, db: Session = Depends(get_db)):
    """Delete a contract"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(contrato_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid contract ID format")
    
    success = delete_contrato(db=db, contrato_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )
    return {"message": "Contract deleted successfully"}


# ============================================================================
# EMPLOYEE POSITION ASSIGNMENT ENDPOINTS
# ============================================================================

@router.post("/employee-positions/", response_model=EmpleadoPuestoResponse)
def create_employee_position(puesto: EmpleadoPuestoCreate, db: Session = Depends(get_db)):
    """Create a new employee position assignment"""
    return create_empleado_puesto(db=db, puesto_data=puesto)


@router.get("/employee-positions/{puesto_id}", response_model=EmpleadoPuestoResponse)
def get_employee_position(puesto_id: str, db: Session = Depends(get_db)):
    """Get an employee position assignment by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    puesto = get_empleado_puesto(db, uuid_obj)
    if not puesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position assignment not found"
        )
    return puesto


@router.get("/employees/{empleado_id}/positions/active", response_model=List[EmpleadoPuestoResponse])
def get_employee_active_positions(empleado_id: str, db: Session = Depends(get_db)):
    """Get all active position assignments for an employee"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    return get_empleado_puestos_activos(db, uuid_obj)


@router.put("/employee-positions/{puesto_id}", response_model=EmpleadoPuestoResponse)
def update_employee_position(
    puesto_id: str, 
    puesto_data: EmpleadoPuestoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an employee position assignment"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    updated_puesto = update_empleado_puesto(
        db=db, 
        puesto_id=uuid_obj, 
        puesto_data=puesto_data
    )
    if not updated_puesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position assignment not found"
        )
    return updated_puesto


@router.delete("/employee-positions/{puesto_id}")
def delete_employee_position(puesto_id: str, db: Session = Depends(get_db)):
    """Delete an employee position assignment"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    success = delete_empleado_puesto(db=db, puesto_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position assignment not found"
        )
    return {"message": "Position assignment deleted successfully"}


# ============================================================================
# POSITION ENDPOINTS
# ============================================================================

@router.post("/positions/", response_model=PuestoResponse)
def create_position(puesto: PuestoCreate, db: Session = Depends(get_db)):
    """Create a new job position"""
    # Check if position code already exists
    existing_puesto = get_puesto_by_codigo(db, puesto.codigo)
    if existing_puesto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position with this code already exists"
        )
    
    return create_puesto(db=db, puesto_data=puesto)


@router.get("/positions/{puesto_id}", response_model=PuestoResponse)
def get_position(puesto_id: str, db: Session = Depends(get_db)):
    """Get a job position by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    puesto = get_puesto(db, uuid_obj)
    if not puesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )
    return puesto


@router.get("/positions/", response_model=List[PuestoResponse])
def get_positions(
    skip: int = 0, 
    limit: int = 100,
    departamento: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of positions, optionally filtered"""
    return get_puestos(
        db, 
        skip=skip, 
        limit=limit, 
        departamento=departamento, 
        activo=activo
    )


@router.put("/positions/{puesto_id}", response_model=PuestoResponse)
def update_position(
    puesto_id: str, 
    puesto_data: PuestoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a job position"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    updated_puesto = update_puesto(
        db=db, 
        puesto_id=uuid_obj, 
        puesto_data=puesto_data
    )
    if not updated_puesto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )
    return updated_puesto


@router.delete("/positions/{puesto_id}")
def delete_position(puesto_id: str, db: Session = Depends(get_db)):
    """Delete a job position"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(puesto_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid position ID format")
    
    success = delete_puesto(db=db, puesto_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )
    return {"message": "Position deleted successfully"}


# ============================================================================
# ATTENDANCE ENDPOINTS
# ============================================================================

@router.post("/attendance/", response_model=AsistenciaResponse)
def create_attendance(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
    """Create a new attendance record"""
    return create_asistencia(db=db, asistencia_data=asistencia)


@router.get("/attendance/{asistencia_id}", response_model=AsistenciaResponse)
def get_attendance(asistencia_id: str, db: Session = Depends(get_db)):
    """Get an attendance record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(asistencia_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid attendance ID format")
    
    asistencia = get_asistencia(db, uuid_obj)
    if not asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    return asistencia


@router.get("/attendance/", response_model=List[AsistenciaResponse])
def get_attendances_by_date(date: str, db: Session = Depends(get_db)):
    """Get all attendance records for a specific date"""
    from datetime import datetime
    try:
        attendance_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    
    return get_asistencias_by_fecha(db, attendance_date)


@router.get("/employees/{empleado_id}/attendance/", response_model=List[AsistenciaResponse])
def get_employee_attendance(
    empleado_id: str, 
    fecha_inicio: str, 
    fecha_fin: str, 
    db: Session = Depends(get_db)
):
    """Get attendance records for an employee within a date range"""
    from datetime import datetime
    try:
        start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        end_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    return get_asistencias_by_empleado_fecha(
        db, uuid_obj, start_date, end_date
    )


@router.put("/attendance/{asistencia_id}", response_model=AsistenciaResponse)
def update_attendance(
    asistencia_id: str, 
    asistencia_data: AsistenciaUpdate, 
    db: Session = Depends(get_db)
):
    """Update an attendance record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(asistencia_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid attendance ID format")
    
    updated_asistencia = update_asistencia(
        db=db, 
        asistencia_id=uuid_obj, 
        asistencia_data=asistencia_data
    )
    if not updated_asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    return updated_asistencia


@router.delete("/attendance/{asistencia_id}")
def delete_attendance(asistencia_id: str, db: Session = Depends(get_db)):
    """Delete an attendance record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(asistencia_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid attendance ID format")
    
    success = delete_asistencia(db=db, asistencia_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    return {"message": "Attendance record deleted successfully"}


# ============================================================================
# MEDICAL LEAVE ENDPOINTS
# ============================================================================

@router.post("/medical-leaves/", response_model=IncapacidadResponse)
def create_medical_leave(incapacidad: IncapacidadCreate, db: Session = Depends(get_db)):
    """Create a new medical leave record"""
    return create_incapacidad(db=db, incapacidad_data=incapacidad)


@router.get("/medical-leaves/{incapacidad_id}", response_model=IncapacidadResponse)
def get_medical_leave(incapacidad_id: str, db: Session = Depends(get_db)):
    """Get a medical leave record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(incapacidad_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid medical leave ID format")
    
    incapacidad = get_incapacidad(db, uuid_obj)
    if not incapacidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical leave record not found"
        )
    return incapacidad


@router.get("/employees/{empleado_id}/medical-leaves/", response_model=List[IncapacidadResponse])
def get_employee_medical_leaves(
    empleado_id: str, 
    estado: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """Get all medical leaves for an employee, optionally filtered by state"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    return get_incapacidades_by_empleado(db, uuid_obj, estado)


@router.put("/medical-leaves/{incapacidad_id}", response_model=IncapacidadResponse)
def update_medical_leave(
    incapacidad_id: str, 
    incapacidad_data: IncapacidadUpdate, 
    db: Session = Depends(get_db)
):
    """Update a medical leave record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(incapacidad_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid medical leave ID format")
    
    updated_incapacidad = update_incapacidad(
        db=db, 
        incapacidad_id=uuid_obj, 
        incapacidad_data=incapacidad_data
    )
    if not updated_incapacidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical leave record not found"
        )
    return updated_incapacidad


@router.delete("/medical-leaves/{incapacidad_id}")
def delete_medical_leave(incapacidad_id: str, db: Session = Depends(get_db)):
    """Delete a medical leave record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(incapacidad_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid medical leave ID format")
    
    success = delete_incapacidad(db=db, incapacidad_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical leave record not found"
        )
    return {"message": "Medical leave record deleted successfully"}


# ============================================================================
# VACATION ENDPOINTS
# ============================================================================

@router.post("/vacations/", response_model=VacacionResponse)
def create_vacation(vacacion: VacacionCreate, db: Session = Depends(get_db)):
    """Create a new vacation record"""
    return create_vacacion(db=db, vacacion_data=vacacion)


@router.get("/vacations/{vacacion_id}", response_model=VacacionResponse)
def get_vacation(vacacion_id: str, db: Session = Depends(get_db)):
    """Get a vacation record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(vacacion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vacation ID format")
    
    vacacion = get_vacacion(db, uuid_obj)
    if not vacacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacation record not found"
        )
    return vacacion


@router.get("/employees/{empleado_id}/vacations/", response_model=List[VacacionResponse])
def get_employee_vacations(
    empleado_id: str, 
    anio: Optional[int] = None, 
    estado: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """Get all vacations for an employee, optionally filtered by year and state"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    return get_vacaciones_by_empleado(db, uuid_obj, anio, estado)


@router.put("/vacations/{vacacion_id}", response_model=VacacionResponse)
def update_vacation(
    vacacion_id: str, 
    vacacion_data: VacacionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a vacation record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(vacacion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vacation ID format")
    
    updated_vacacion = update_vacacion(
        db=db, 
        vacacion_id=uuid_obj, 
        vacacion_data=vacacion_data
    )
    if not updated_vacacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacation record not found"
        )
    return updated_vacacion


@router.delete("/vacations/{vacacion_id}")
def delete_vacation(vacacion_id: str, db: Session = Depends(get_db)):
    """Delete a vacation record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(vacacion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vacation ID format")
    
    success = delete_vacacion(db=db, vacacion_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacation record not found"
        )
    return {"message": "Vacation record deleted successfully"}


# ============================================================================
# PAYROLL ENDPOINTS
# ============================================================================

@router.post("/payrolls/", response_model=NominaResponse)
def create_payroll(nomina: NominaCreate, db: Session = Depends(get_db)):
    """Create a new payroll record"""
    return create_nomina(db=db, nomina_data=nomina)


@router.get("/payrolls/{nomina_id}", response_model=NominaResponse)
def get_payroll(nomina_id: str, db: Session = Depends(get_db)):
    """Get a payroll record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(nomina_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payroll ID format")
    
    nomina = get_nomina(db, uuid_obj)
    if not nomina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    return nomina


@router.get("/employees/{empleado_id}/payrolls/", response_model=List[NominaResponse])
def get_employee_payrolls(
    empleado_id: str, 
    periodo_pago_id: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    """Get all payroll records for an employee, optionally filtered by period"""
    # Convert string to UUID
    try:
        uuid_empleado = UUID(empleado_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid employee ID format")
    
    uuid_periodo_pago = None
    if periodo_pago_id:
        try:
            uuid_periodo_pago = UUID(periodo_pago_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid period ID format"
            )
    
    return get_nominas_by_empleado(db, uuid_empleado, uuid_periodo_pago)


@router.put("/payrolls/{nomina_id}", response_model=NominaResponse)
def update_payroll(
    nomina_id: str, 
    nomina_data: NominaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a payroll record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(nomina_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payroll ID format")
    
    updated_nomina = update_nomina(
        db=db, 
        nomina_id=uuid_obj, 
        nomina_data=nomina_data
    )
    if not updated_nomina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    return updated_nomina


@router.delete("/payrolls/{nomina_id}")
def delete_payroll(nomina_id: str, db: Session = Depends(get_db)):
    """Delete a payroll record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(nomina_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payroll ID format")
    
    success = delete_nomina(db=db, nomina_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll record not found"
        )
    return {"message": "Payroll record deleted successfully"}


# ============================================================================
# PAYROLL PERIOD ENDPOINTS
# ============================================================================

@router.post("/payroll-periods/", response_model=PeriodoPagoResponse)
def create_payroll_period(periodo: PeriodoPagoCreate, db: Session = Depends(get_db)):
    """Create a new payroll period"""
    # Check if period code already exists
    existing_periodo = get_periodo_pago_by_codigo(db, periodo.codigo)
    if existing_periodo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payroll period with this code already exists"
        )
    
    return create_periodo_pago(db=db, periodo_data=periodo)


@router.get("/payroll-periods/{periodo_id}", response_model=PeriodoPagoResponse)
def get_payroll_period(periodo_id: str, db: Session = Depends(get_db)):
    """Get a payroll period by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(periodo_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period ID format")
    
    periodo = get_periodo_pago(db, uuid_obj)
    if not periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return periodo


@router.get("/payroll-periods/", response_model=List[PeriodoPagoResponse])
def get_payroll_periods(
    skip: int = 0, 
    limit: int = 100,
    tipo_periodo: Optional[str] = None,
    cerrado: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of payroll periods, optionally filtered"""
    return get_periodos_pago(
        db, 
        skip=skip, 
        limit=limit, 
        tipo_periodo=tipo_periodo, 
        cerrado=cerrado
    )


@router.put("/payroll-periods/{periodo_id}", response_model=PeriodoPagoResponse)
def update_payroll_period(
    periodo_id: str, 
    periodo_data: PeriodoPagoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a payroll period"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(periodo_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period ID format")
    
    updated_periodo = update_periodo_pago(
        db=db, 
        periodo_id=uuid_obj, 
        periodo_data=periodo_data
    )
    if not updated_periodo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return updated_periodo


@router.delete("/payroll-periods/{periodo_id}")
def delete_payroll_period(periodo_id: str, db: Session = Depends(get_db)):
    """Delete a payroll period"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(periodo_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid period ID format")
    
    success = delete_periodo_pago(db=db, periodo_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payroll period not found"
        )
    return {"message": "Payroll period deleted successfully"}


# ============================================================================
# EARNINGS ENDPOINTS
# ============================================================================

@router.post("/earnings/", response_model=PercepcionResponse)
def create_earning(percepcion: PercepcionCreate, db: Session = Depends(get_db)):
    """Create a new earning record"""
    return create_percepcion(db=db, percepcion_data=percepcion)


@router.get("/earnings/{percepcion_id}", response_model=PercepcionResponse)
def get_earning(percepcion_id: str, db: Session = Depends(get_db)):
    """Get an earning record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(percepcion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid earning ID format")
    
    percepcion = get_percepcion(db, uuid_obj)
    if not percepcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Earning record not found"
        )
    return percepcion


@router.get("/payrolls/{nomina_id}/earnings", response_model=List[PercepcionResponse])
def get_payroll_earnings(nomina_id: str, db: Session = Depends(get_db)):
    """Get all earnings for a specific payroll record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(nomina_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payroll ID format")
    
    return get_percepciones_by_nomina(db, uuid_obj)


@router.put("/earnings/{percepcion_id}", response_model=PercepcionResponse)
def update_earning(
    percepcion_id: str, 
    percepcion_data: PercepcionUpdate, 
    db: Session = Depends(get_db)
):
    """Update an earning record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(percepcion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid earning ID format")
    
    updated_percepcion = update_percepcion(
        db=db, 
        percepcion_id=uuid_obj, 
        percepcion_data=percepcion_data
    )
    if not updated_percepcion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Earning record not found"
        )
    return updated_percepcion


@router.delete("/earnings/{percepcion_id}")
def delete_earning(percepcion_id: str, db: Session = Depends(get_db)):
    """Delete an earning record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(percepcion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid earning ID format")
    
    success = delete_percepcion(db=db, percepcion_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Earning record not found"
        )
    return {"message": "Earning record deleted successfully"}


# ============================================================================
# DEDUCTIONS ENDPOINTS
# ============================================================================

@router.post("/deductions/", response_model=DeduccionResponse)
def create_deduction(deduccion: DeduccionCreate, db: Session = Depends(get_db)):
    """Create a new deduction record"""
    return create_deduccion(db=db, deduccion_data=deduccion)


@router.get("/deductions/{deduccion_id}", response_model=DeduccionResponse)
def get_deduction(deduccion_id: str, db: Session = Depends(get_db)):
    """Get a deduction record by ID"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(deduccion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid deduction ID format")
    
    deduccion = get_deduccion(db, uuid_obj)
    if not deduccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deduction record not found"
        )
    return deduccion


@router.get("/payrolls/{nomina_id}/deductions", response_model=List[DeduccionResponse])
def get_payroll_deductions(nomina_id: str, db: Session = Depends(get_db)):
    """Get all deductions for a specific payroll record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(nomina_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payroll ID format")
    
    return get_deducciones_by_nomina(db, uuid_obj)


@router.put("/deductions/{deduccion_id}", response_model=DeduccionResponse)
def update_deduction(
    deduccion_id: str, 
    deduccion_data: DeduccionUpdate, 
    db: Session = Depends(get_db)
):
    """Update a deduction record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(deduccion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid deduction ID format")
    
    updated_deduccion = update_deduccion(
        db=db, 
        deduccion_id=uuid_obj, 
        deduccion_data=deduccion_data
    )
    if not updated_deduccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deduction record not found"
        )
    return updated_deduccion


@router.delete("/deductions/{deduccion_id}")
def delete_deduction(deduccion_id: str, db: Session = Depends(get_db)):
    """Delete a deduction record"""
    # Convert string to UUID
    try:
        uuid_obj = UUID(deduccion_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid deduction ID format")
    
    success = delete_deduccion(db=db, deduccion_id=uuid_obj)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deduction record not found"
        )
    return {"message": "Deduction record deleted successfully"}