"""
Project Management CRUD Operations: Project coordination, resource assignment, scheduling and milestones
Specialized for textile product development projects
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.project_management import (
    Proyecto, Tarea, RecursoProyecto, Recurso, RecursoTarea,
    HitoProyecto, ActividadProyecto
)
from app.schemas.project_management import (
    ProyectoCreate, ProyectoUpdate,
    TareaCreate, TareaUpdate,
    RecursoProyectoCreate, RecursoProyectoUpdate,
    RecursoCreate, RecursoUpdate,
    RecursoTareaCreate, RecursoTareaUpdate,
    HitoProyectoCreate, HitoProyectoUpdate,
    ActividadProyectoCreate, ActividadProyectoUpdate
)


# ============================================================================
# PROJECT CRUD
# ============================================================================

def create_proyecto(db: Session, proyecto_data: ProyectoCreate) -> Proyecto:
    """Create a new project"""
    # Check if project code already exists
    existing_proyecto = db.query(Proyecto).filter(Proyecto.codigo == proyecto_data.codigo).first()
    if existing_proyecto:
        raise ValueError(f"A project with code {proyecto_data.codigo} already exists")
    
    db_proyecto = Proyecto(**proyecto_data.model_dump())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto


def get_proyecto(db: Session, proyecto_id: UUID) -> Optional[Proyecto]:
    """Get a project by ID"""
    return db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()


def get_proyecto_by_codigo(db: Session, codigo: str) -> Optional[Proyecto]:
    """Get a project by code"""
    return db.query(Proyecto).filter(Proyecto.codigo == codigo).first()


def get_proyectos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    tipo_proyecto: Optional[str] = None,
    responsable_id: Optional[UUID] = None
) -> List[Proyecto]:
    """Get list of projects, optionally filtered"""
    query = db.query(Proyecto)
    
    if estado:
        query = query.filter(Proyecto.estado == estado)
    if tipo_proyecto:
        query = query.filter(Proyecto.tipo_proyecto == tipo_proyecto)
    if responsable_id:
        query = query.filter(Proyecto.responsable_id == responsable_id)
    
    return query.offset(skip).limit(limit).all()


def update_proyecto(db: Session, proyecto_id: UUID, proyecto_data: ProyectoUpdate) -> Optional[Proyecto]:
    """Update a project"""
    db_proyecto = get_proyecto(db, proyecto_id)
    if db_proyecto:
        update_data = proyecto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_proyecto, field, value)
        db.commit()
        db.refresh(db_proyecto)
    return db_proyecto


def delete_proyecto(db: Session, proyecto_id: UUID) -> bool:
    """Soft delete a project"""
    db_proyecto = get_proyecto(db, proyecto_id)
    if db_proyecto:
        db_proyecto.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# TASK CRUD
# ============================================================================

def create_tarea(db: Session, tarea_data: TareaCreate) -> Tarea:
    """Create a new task"""
    # Check if task code already exists
    existing_tarea = db.query(Tarea).filter(Tarea.codigo == tarea_data.codigo).first()
    if existing_tarea:
        raise ValueError(f"A task with code {tarea_data.codigo} already exists")
    
    db_tarea = Tarea(**tarea_data.model_dump())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea


def get_tarea(db: Session, tarea_id: UUID) -> Optional[Tarea]:
    """Get a task by ID"""
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()


def get_tarea_by_codigo(db: Session, codigo: str) -> Optional[Tarea]:
    """Get a task by code"""
    return db.query(Tarea).filter(Tarea.codigo == codigo).first()


def get_tareas_by_proyecto(db: Session, proyecto_id: UUID, skip: int = 0, limit: int = 100) -> List[Tarea]:
    """Get all tasks for a specific project"""
    return db.query(Tarea).filter(
        Tarea.proyecto_id == proyecto_id
    ).offset(skip).limit(limit).all()


def get_tareas_by_asignado(db: Session, asignado_a_id: UUID, skip: int = 0, limit: int = 100) -> List[Tarea]:
    """Get all tasks assigned to a specific employee"""
    return db.query(Tarea).filter(
        Tarea.asignado_a_id == asignado_a_id
    ).offset(skip).limit(limit).all()


def update_tarea(db: Session, tarea_id: UUID, tarea_data: TareaUpdate) -> Optional[Tarea]:
    """Update a task"""
    db_tarea = get_tarea(db, tarea_id)
    if db_tarea:
        update_data = tarea_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tarea, field, value)
        db.commit()
        db.refresh(db_tarea)
    return db_tarea


def delete_tarea(db: Session, tarea_id: UUID) -> bool:
    """Soft delete a task"""
    db_tarea = get_tarea(db, tarea_id)
    if db_tarea:
        db_tarea.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# PROJECT RESOURCE CRUD
# ============================================================================

def create_recurso_proyecto(db: Session, recurso_data: RecursoProyectoCreate) -> RecursoProyecto:
    """Create a new project resource assignment"""
    db_recurso = RecursoProyecto(**recurso_data.model_dump())
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso


def get_recurso_proyecto(db: Session, recurso_id: UUID) -> Optional[RecursoProyecto]:
    """Get a project resource assignment by ID"""
    return db.query(RecursoProyecto).filter(RecursoProyecto.id == recurso_id).first()


def get_recursos_by_proyecto(db: Session, proyecto_id: UUID) -> List[RecursoProyecto]:
    """Get all resources assigned to a specific project"""
    return db.query(RecursoProyecto).filter(
        RecursoProyecto.proyecto_id == proyecto_id
    ).all()


def update_recurso_proyecto(db: Session, recurso_id: UUID, recurso_data: RecursoProyectoUpdate) -> Optional[RecursoProyecto]:
    """Update a project resource assignment"""
    db_recurso = get_recurso_proyecto(db, recurso_id)
    if db_recurso:
        update_data = recurso_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recurso, field, value)
        db.commit()
        db.refresh(db_recurso)
    return db_recurso


def delete_recurso_proyecto(db: Session, recurso_id: UUID) -> bool:
    """Soft delete a project resource assignment"""
    db_recurso = get_recurso_proyecto(db, recurso_id)
    if db_recurso:
        db_recurso.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# RESOURCE CRUD
# ============================================================================

def create_recurso(db: Session, recurso_data: RecursoCreate) -> Recurso:
    """Create a new resource"""
    # Check if resource code already exists
    existing_recurso = db.query(Recurso).filter(Recurso.codigo == recurso_data.codigo).first()
    if existing_recurso:
        raise ValueError(f"A resource with code {recurso_data.codigo} already exists")
    
    db_recurso = Recurso(**recurso_data.model_dump())
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso


def get_recurso(db: Session, recurso_id: UUID) -> Optional[Recurso]:
    """Get a resource by ID"""
    return db.query(Recurso).filter(Recurso.id == recurso_id).first()


def get_recurso_by_codigo(db: Session, codigo: str) -> Optional[Recurso]:
    """Get a resource by code"""
    return db.query(Recurso).filter(Recurso.codigo == codigo).first()


def get_recursos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    tipo: Optional[str] = None,
    estado: Optional[str] = None
) -> List[Recurso]:
    """Get list of resources, optionally filtered"""
    query = db.query(Recurso)
    
    if tipo:
        query = query.filter(Recurso.tipo == tipo)
    if estado:
        query = query.filter(Recurso.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def update_recurso(db: Session, recurso_id: UUID, recurso_data: RecursoUpdate) -> Optional[Recurso]:
    """Update a resource"""
    db_recurso = get_recurso(db, recurso_id)
    if db_recurso:
        update_data = recurso_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recurso, field, value)
        db.commit()
        db.refresh(db_recurso)
    return db_recurso


def delete_recurso(db: Session, recurso_id: UUID) -> bool:
    """Soft delete a resource"""
    db_recurso = get_recurso(db, recurso_id)
    if db_recurso:
        db_recurso.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# TASK RESOURCE ASSIGNMENT CRUD
# ============================================================================

def create_recurso_tarea(db: Session, recurso_tarea_data: RecursoTareaCreate) -> RecursoTarea:
    """Create a new task-resource assignment"""
    db_recurso_tarea = RecursoTarea(**recurso_tarea_data.model_dump())
    db.add(db_recurso_tarea)
    db.commit()
    db.refresh(db_recurso_tarea)
    return db_recurso_tarea


def get_recurso_tarea(db: Session, recurso_tarea_id: UUID) -> Optional[RecursoTarea]:
    """Get a task-resource assignment by ID"""
    return db.query(RecursoTarea).filter(RecursoTarea.id == recurso_tarea_id).first()


def get_recursos_by_tarea(db: Session, tarea_id: UUID) -> List[RecursoTarea]:
    """Get all resources assigned to a specific task"""
    return db.query(RecursoTarea).filter(
        RecursoTarea.tarea_id == tarea_id
    ).all()


def update_recurso_tarea(db: Session, recurso_tarea_id: UUID, recurso_tarea_data: RecursoTareaUpdate) -> Optional[RecursoTarea]:
    """Update a task-resource assignment"""
    db_recurso_tarea = get_recurso_tarea(db, recurso_tarea_id)
    if db_recurso_tarea:
        update_data = recurso_tarea_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recurso_tarea, field, value)
        db.commit()
        db.refresh(db_recurso_tarea)
    return db_recurso_tarea


def delete_recurso_tarea(db: Session, recurso_tarea_id: UUID) -> bool:
    """Delete a task-resource assignment"""
    db_recurso_tarea = get_recurso_tarea(db, recurso_tarea_id)
    if db_recurso_tarea:
        db.delete(db_recurso_tarea)
        db.commit()
        return True
    return False


# ============================================================================
# PROJECT MILESTONE CRUD
# ============================================================================

def create_hito_proyecto(db: Session, hito_data: HitoProyectoCreate) -> HitoProyecto:
    """Create a new project milestone"""
    db_hito = HitoProyecto(**hito_data.model_dump())
    db.add(db_hito)
    db.commit()
    db.refresh(db_hito)
    return db_hito


def get_hito_proyecto(db: Session, hito_id: UUID) -> Optional[HitoProyecto]:
    """Get a project milestone by ID"""
    return db.query(HitoProyecto).filter(HitoProyecto.id == hito_id).first()


def get_hitos_by_proyecto(db: Session, proyecto_id: UUID) -> List[HitoProyecto]:
    """Get all milestones for a specific project"""
    return db.query(HitoProyecto).filter(
        HitoProyecto.proyecto_id == proyecto_id
    ).all()


def update_hito_proyecto(db: Session, hito_id: UUID, hito_data: HitoProyectoUpdate) -> Optional[HitoProyecto]:
    """Update a project milestone"""
    db_hito = get_hito_proyecto(db, hito_id)
    if db_hito:
        update_data = hito_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_hito, field, value)
        db.commit()
        db.refresh(db_hito)
    return db_hito


def delete_hito_proyecto(db: Session, hito_id: UUID) -> bool:
    """Delete a project milestone"""
    db_hito = get_hito_proyecto(db, hito_id)
    if db_hito:
        db.delete(db_hito)
        db.commit()
        return True
    return False


# ============================================================================
# PROJECT ACTIVITY CRUD
# ============================================================================

def create_actividad_proyecto(db: Session, actividad_data: ActividadProyectoCreate) -> ActividadProyecto:
    """Create a new project activity"""
    db_actividad = ActividadProyecto(**actividad_data.model_dump())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


def get_actividad_proyecto(db: Session, actividad_id: UUID) -> Optional[ActividadProyecto]:
    """Get a project activity by ID"""
    return db.query(ActividadProyecto).filter(ActividadProyecto.id == actividad_id).first()


def get_actividades_by_proyecto(db: Session, proyecto_id: UUID, skip: int = 0, limit: int = 100) -> List[ActividadProyecto]:
    """Get all activities for a specific project"""
    return db.query(ActividadProyecto).filter(
        ActividadProyecto.proyecto_id == proyecto_id
    ).offset(skip).limit(limit).all()


def get_actividades_by_empleado(db: Session, empleado_id: UUID, skip: int = 0, limit: int = 100) -> List[ActividadProyecto]:
    """Get all activities performed by a specific employee"""
    return db.query(ActividadProyecto).filter(
        ActividadProyecto.empleado_id == empleado_id
    ).offset(skip).limit(limit).all()


def update_actividad_proyecto(db: Session, actividad_id: UUID, actividad_data: ActividadProyectoUpdate) -> Optional[ActividadProyecto]:
    """Update a project activity"""
    db_actividad = get_actividad_proyecto(db, actividad_id)
    if db_actividad:
        update_data = actividad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_actividad, field, value)
        db.commit()
        db.refresh(db_actividad)
    return db_actividad


def delete_actividad_proyecto(db: Session, actividad_id: UUID) -> bool:
    """Delete a project activity"""
    db_actividad = get_actividad_proyecto(db, actividad_id)
    if db_actividad:
        db.delete(db_actividad)
        db.commit()
        return True
    return False