"""
Project Management API Router: Project coordination, resource assignment, scheduling and milestones
Specialized for textile product development projects
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.project_management import (
    ProyectoCreate, ProyectoUpdate, ProyectoResponse,
    TareaCreate, TareaUpdate, TareaResponse,
    RecursoProyectoCreate, RecursoProyectoUpdate, RecursoProyectoResponse,
    RecursoCreate, RecursoUpdate, RecursoResponse,
    RecursoTareaCreate, RecursoTareaUpdate, RecursoTareaResponse,
    HitoProyectoCreate, HitoProyectoUpdate, HitoProyectoResponse,
    ActividadProyectoCreate, ActividadProyectoUpdate, ActividadProyectoResponse
)
from app.crud.project_management import (
    create_proyecto, get_proyecto, get_proyecto_by_codigo,
    get_proyectos, update_proyecto, delete_proyecto,
    create_tarea, get_tarea, get_tarea_by_codigo,
    get_tareas_by_proyecto, get_tareas_by_asignado, update_tarea, delete_tarea,
    create_recurso_proyecto, get_recurso_proyecto, get_recursos_by_proyecto,
    update_recurso_proyecto, delete_recurso_proyecto,
    create_recurso, get_recurso, get_recurso_by_codigo,
    get_recursos, update_recurso, delete_recurso,
    create_recurso_tarea, get_recurso_tarea, get_recursos_by_tarea,
    update_recurso_tarea, delete_recurso_tarea,
    create_hito_proyecto, get_hito_proyecto, get_hitos_by_proyecto,
    update_hito_proyecto, delete_hito_proyecto,
    create_actividad_proyecto, get_actividad_proyecto, get_actividades_by_proyecto,
    get_actividades_by_empleado, update_actividad_proyecto, delete_actividad_proyecto
)

router = APIRouter(prefix="/project-management", tags=["Project Management"])

# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@router.post("/projects/", response_model=ProyectoResponse)
def create_project(proyecto: ProyectoCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    try:
        return create_proyecto(db=db, proyecto_data=proyecto)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/projects/{proyecto_id}", response_model=ProyectoResponse)
def get_project(proyecto_id: str, db: Session = Depends(get_db)):
    """Get a project by ID"""
    proyecto = get_proyecto(db, proyecto_id)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return proyecto


@router.get("/projects/code/{codigo}", response_model=ProyectoResponse)
def get_project_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a project by code"""
    proyecto = get_proyecto_by_codigo(db, codigo)
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return proyecto


@router.get("/projects/", response_model=List[ProyectoResponse])
def get_projects(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    tipo_proyecto: Optional[str] = None,
    responsable_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of projects, optionally filtered"""
    responsable_uuid = UUID(responsable_id) if responsable_id else None
    return get_proyectos(db, skip, limit, estado, tipo_proyecto, responsable_uuid)


@router.put("/projects/{proyecto_id}", response_model=ProyectoResponse)
def update_project(
    proyecto_id: str, 
    proyecto_data: ProyectoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a project"""
    updated_proyecto = update_proyecto(
        db=db, 
        proyecto_id=proyecto_id, 
        proyecto_data=proyecto_data
    )
    if not updated_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return updated_proyecto


@router.delete("/projects/{proyecto_id}")
def delete_project(proyecto_id: str, db: Session = Depends(get_db)):
    """Soft delete a project"""
    success = delete_proyecto(db=db, proyecto_id=proyecto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"message": "Project deactivated successfully"}


# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@router.post("/tasks/", response_model=TareaResponse)
def create_task(tarea: TareaCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    try:
        return create_tarea(db=db, tarea_data=tarea)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tasks/{tarea_id}", response_model=TareaResponse)
def get_task(tarea_id: str, db: Session = Depends(get_db)):
    """Get a task by ID"""
    tarea = get_tarea(db, tarea_id)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return tarea


@router.get("/tasks/code/{codigo}", response_model=TareaResponse)
def get_task_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a task by code"""
    tarea = get_tarea_by_codigo(db, codigo)
    if not tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return tarea


@router.get("/projects/{proyecto_id}/tasks", response_model=List[TareaResponse])
def get_tasks_by_project(
    proyecto_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all tasks for a specific project"""
    return get_tareas_by_proyecto(db, proyecto_id, skip, limit)


@router.get("/employees/{empleado_id}/tasks", response_model=List[TareaResponse])
def get_tasks_by_employee(
    empleado_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all tasks assigned to a specific employee"""
    return get_tareas_by_asignado(db, empleado_id, skip, limit)


@router.put("/tasks/{tarea_id}", response_model=TareaResponse)
def update_task(
    tarea_id: str, 
    tarea_data: TareaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a task"""
    updated_tarea = update_tarea(
        db=db, 
        tarea_id=tarea_id, 
        tarea_data=tarea_data
    )
    if not updated_tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_tarea


@router.delete("/tasks/{tarea_id}")
def delete_task(tarea_id: str, db: Session = Depends(get_db)):
    """Soft delete a task"""
    success = delete_tarea(db=db, tarea_id=tarea_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deactivated successfully"}


# ============================================================================
# PROJECT RESOURCE ENDPOINTS
# ============================================================================

@router.post("/project-resources/", response_model=RecursoProyectoResponse)
def create_project_resource(recurso: RecursoProyectoCreate, db: Session = Depends(get_db)):
    """Create a new project resource assignment"""
    return create_recurso_proyecto(db=db, recurso_data=recurso)


@router.get("/project-resources/{recurso_id}", response_model=RecursoProyectoResponse)
def get_project_resource(recurso_id: str, db: Session = Depends(get_db)):
    """Get a project resource assignment by ID"""
    recurso = get_recurso_proyecto(db, recurso_id)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project resource assignment not found"
        )
    return recurso


@router.get("/projects/{proyecto_id}/resources", response_model=List[RecursoProyectoResponse])
def get_resources_by_project(proyecto_id: str, db: Session = Depends(get_db)):
    """Get all resources assigned to a specific project"""
    return get_recursos_by_proyecto(db, proyecto_id)


@router.put("/project-resources/{recurso_id}", response_model=RecursoProyectoResponse)
def update_project_resource(
    recurso_id: str, 
    recurso_data: RecursoProyectoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a project resource assignment"""
    updated_recurso = update_recurso_proyecto(
        db=db, 
        recurso_id=recurso_id, 
        recurso_data=recurso_data
    )
    if not updated_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project resource assignment not found"
        )
    return updated_recurso


@router.delete("/project-resources/{recurso_id}")
def delete_project_resource(recurso_id: str, db: Session = Depends(get_db)):
    """Soft delete a project resource assignment"""
    success = delete_recurso_proyecto(db=db, recurso_id=recurso_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project resource assignment not found"
        )
    return {"message": "Project resource assignment deactivated successfully"}


# ============================================================================
# RESOURCE ENDPOINTS
# ============================================================================

@router.post("/resources/", response_model=RecursoResponse)
def create_resource(recurso: RecursoCreate, db: Session = Depends(get_db)):
    """Create a new resource"""
    try:
        return create_recurso(db=db, recurso_data=recurso)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/resources/{recurso_id}", response_model=RecursoResponse)
def get_resource(recurso_id: str, db: Session = Depends(get_db)):
    """Get a resource by ID"""
    recurso = get_recurso(db, recurso_id)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return recurso


@router.get("/resources/code/{codigo}", response_model=RecursoResponse)
def get_resource_by_code(codigo: str, db: Session = Depends(get_db)):
    """Get a resource by code"""
    recurso = get_recurso_by_codigo(db, codigo)
    if not recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return recurso


@router.get("/resources/", response_model=List[RecursoResponse])
def get_resources(
    skip: int = 0, 
    limit: int = 100,
    tipo: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of resources, optionally filtered"""
    return get_recursos(db, skip, limit, tipo, estado)


@router.put("/resources/{recurso_id}", response_model=RecursoResponse)
def update_resource(
    recurso_id: str, 
    recurso_data: RecursoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a resource"""
    updated_recurso = update_recurso(
        db=db, 
        recurso_id=recurso_id, 
        recurso_data=recurso_data
    )
    if not updated_recurso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return updated_recurso


@router.delete("/resources/{recurso_id}")
def delete_resource(recurso_id: str, db: Session = Depends(get_db)):
    """Soft delete a resource"""
    success = delete_recurso(db=db, recurso_id=recurso_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return {"message": "Resource deactivated successfully"}


# ============================================================================
# TASK RESOURCE ASSIGNMENT ENDPOINTS
# ============================================================================

@router.post("/task-resources/", response_model=RecursoTareaResponse)
def create_task_resource_assignment(recurso_tarea: RecursoTareaCreate, db: Session = Depends(get_db)):
    """Create a new task-resource assignment"""
    return create_recurso_tarea(db=db, recurso_tarea_data=recurso_tarea)


@router.get("/task-resources/{recurso_tarea_id}", response_model=RecursoTareaResponse)
def get_task_resource_assignment(recurso_tarea_id: str, db: Session = Depends(get_db)):
    """Get a task-resource assignment by ID"""
    recurso_tarea = get_recurso_tarea(db, recurso_tarea_id)
    if not recurso_tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task-resource assignment not found"
        )
    return recurso_tarea


@router.get("/tasks/{tarea_id}/resources", response_model=List[RecursoTareaResponse])
def get_resources_by_task(tarea_id: str, db: Session = Depends(get_db)):
    """Get all resources assigned to a specific task"""
    return get_recursos_by_tarea(db, tarea_id)


@router.put("/task-resources/{recurso_tarea_id}", response_model=RecursoTareaResponse)
def update_task_resource_assignment(
    recurso_tarea_id: str, 
    recurso_tarea_data: RecursoTareaUpdate, 
    db: Session = Depends(get_db)
):
    """Update a task-resource assignment"""
    updated_recurso_tarea = update_recurso_tarea(
        db=db, 
        recurso_tarea_id=recurso_tarea_id, 
        recurso_tarea_data=recurso_tarea_data
    )
    if not updated_recurso_tarea:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task-resource assignment not found"
        )
    return updated_recurso_tarea


@router.delete("/task-resources/{recurso_tarea_id}")
def delete_task_resource_assignment(recurso_tarea_id: str, db: Session = Depends(get_db)):
    """Delete a task-resource assignment"""
    success = delete_recurso_tarea(db=db, recurso_tarea_id=recurso_tarea_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task-resource assignment not found"
        )
    return {"message": "Task-resource assignment deleted successfully"}


# ============================================================================
# PROJECT MILESTONE ENDPOINTS
# ============================================================================

@router.post("/milestones/", response_model=HitoProyectoResponse)
def create_project_milestone(hito: HitoProyectoCreate, db: Session = Depends(get_db)):
    """Create a new project milestone"""
    return create_hito_proyecto(db=db, hito_data=hito)


@router.get("/milestones/{hito_id}", response_model=HitoProyectoResponse)
def get_project_milestone(hito_id: str, db: Session = Depends(get_db)):
    """Get a project milestone by ID"""
    hito = get_hito_proyecto(db, hito_id)
    if not hito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project milestone not found"
        )
    return hito


@router.get("/projects/{proyecto_id}/milestones", response_model=List[HitoProyectoResponse])
def get_milestones_by_project(proyecto_id: str, db: Session = Depends(get_db)):
    """Get all milestones for a specific project"""
    return get_hitos_by_proyecto(db, proyecto_id)


@router.put("/milestones/{hito_id}", response_model=HitoProyectoResponse)
def update_project_milestone(
    hito_id: str, 
    hito_data: HitoProyectoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a project milestone"""
    updated_hito = update_hito_proyecto(
        db=db, 
        hito_id=hito_id, 
        hito_data=hito_data
    )
    if not updated_hito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project milestone not found"
        )
    return updated_hito


@router.delete("/milestones/{hito_id}")
def delete_project_milestone(hito_id: str, db: Session = Depends(get_db)):
    """Delete a project milestone"""
    success = delete_hito_proyecto(db=db, hito_id=hito_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project milestone not found"
        )
    return {"message": "Project milestone deleted successfully"}


# ============================================================================
# PROJECT ACTIVITY ENDPOINTS
# ============================================================================

@router.post("/activities/", response_model=ActividadProyectoResponse)
def create_project_activity(actividad: ActividadProyectoCreate, db: Session = Depends(get_db)):
    """Create a new project activity"""
    return create_actividad_proyecto(db=db, actividad_data=actividad)


@router.get("/activities/{actividad_id}", response_model=ActividadProyectoResponse)
def get_project_activity(actividad_id: str, db: Session = Depends(get_db)):
    """Get a project activity by ID"""
    actividad = get_actividad_proyecto(db, actividad_id)
    if not actividad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project activity not found"
        )
    return actividad


@router.get("/projects/{proyecto_id}/activities", response_model=List[ActividadProyectoResponse])
def get_activities_by_project(
    proyecto_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all activities for a specific project"""
    return get_actividades_by_proyecto(db, proyecto_id, skip, limit)


@router.get("/employees/{empleado_id}/activities", response_model=List[ActividadProyectoResponse])
def get_activities_by_employee(
    empleado_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all activities performed by a specific employee"""
    return get_actividades_by_empleado(db, empleado_id, skip, limit)


@router.put("/activities/{actividad_id}", response_model=ActividadProyectoResponse)
def update_project_activity(
    actividad_id: str, 
    actividad_data: ActividadProyectoUpdate, 
    db: Session = Depends(get_db)
):
    """Update a project activity"""
    updated_actividad = update_actividad_proyecto(
        db=db, 
        actividad_id=actividad_id, 
        actividad_data=actividad_data
    )
    if not updated_actividad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project activity not found"
        )
    return updated_actividad


@router.delete("/activities/{actividad_id}")
def delete_project_activity(actividad_id: str, db: Session = Depends(get_db)):
    """Delete a project activity"""
    success = delete_actividad_proyecto(db=db, actividad_id=actividad_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project activity not found"
        )
    return {"message": "Project activity deleted successfully"}