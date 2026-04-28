"""
Agent API routes: Endpoints for managing local agents
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.crud import agents as crud_agents
from app.schemas import agents as schemas_agents
from app.api.deps import get_current_usuario_activo, check_permiso


router = APIRouter()


# Agent Type Endpoints
@router.post("/tipos/", response_model=schemas_agents.AgentTipo)
def create_agent_tipo(
    agent_tipo: schemas_agents.AgentTipoCreate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Create a new agent type"""
    # Check permission
    check_permiso(current_usuario, "agent_tipo", "create")
    
    return crud_agents.create_agent_tipo(db, agent_tipo)


@router.get("/tipos/{tipo_id}", response_model=schemas_agents.AgentTipo)
def get_agent_tipo(
    tipo_id: UUID,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get an agent type by ID"""
    # Check permission
    check_permiso(current_usuario, "agent_tipo", "read")
    
    db_agent_tipo = crud_agents.get_agent_tipo(db, tipo_id)
    if not db_agent_tipo:
        raise HTTPException(status_code=404, detail="Agent type not found")
    return db_agent_tipo


@router.get("/tipos/", response_model=List[schemas_agents.AgentTipo])
def get_agent_tipos(
    skip: int = 0,
    limit: int = 100,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get all agent types"""
    # Check permission
    check_permiso(current_usuario, "agent_tipo", "read")
    
    return crud_agents.get_agent_tipos(db, skip=skip, limit=limit)


@router.put("/tipos/{tipo_id}", response_model=schemas_agents.AgentTipo)
def update_agent_tipo(
    tipo_id: UUID,
    agent_tipo: schemas_agents.AgentTipoUpdate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Update an agent type"""
    # Check permission
    check_permiso(current_usuario, "agent_tipo", "update")
    
    db_agent_tipo = crud_agents.update_agent_tipo(db, tipo_id, agent_tipo)
    if not db_agent_tipo:
        raise HTTPException(status_code=404, detail="Agent type not found")
    return db_agent_tipo


@router.delete("/tipos/{tipo_id}")
def delete_agent_tipo(
    tipo_id: UUID,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Delete an agent type"""
    # Check permission
    check_permiso(current_usuario, "agent_tipo", "delete")
    
    success = crud_agents.delete_agent_tipo(db, tipo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent type not found")
    return {"message": "Agent type deleted successfully"}


# Installed Agent Endpoints
@router.post("/instalados/", response_model=schemas_agents.AgentInstalado)
def create_agent_instalado(
    agent_instalado: schemas_agents.AgentInstaladoCreate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Register a new installed agent"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "create")
    
    return crud_agents.create_agent_instalado(db, agent_instalado)


@router.get("/instalados/{agente_id}", response_model=schemas_agents.AgentInstalado)
def get_agent_instalado(
    agente_id: UUID,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get an installed agent by ID"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "read")
    
    db_agent = crud_agents.get_agent_instalado(db, agente_id)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent


@router.get("/instalados/", response_model=List[schemas_agents.AgentInstalado])
def get_agent_instalados(
    skip: int = 0,
    limit: int = 100,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get all installed agents"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "read")
    
    # For now we'll just query all agents, could be enhanced with filters
    return db.query(crud_agents.models.AgentInstalado).offset(skip).limit(limit).all()


@router.put("/instalados/{agente_id}", response_model=schemas_agents.AgentInstalado)
def update_agent_instalado(
    agente_id: UUID,
    agent_instalado: schemas_agents.AgentInstaladoUpdate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Update an installed agent"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "update")
    
    db_agent = crud_agents.update_agent_instalado(db, agente_id, agent_instalado)
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent


@router.delete("/instalados/{agente_id}")
def delete_agent_instalado(
    agente_id: UUID,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Delete an installed agent"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "delete")
    
    success = crud_agents.delete_agent_instalado(db, agente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}


# Agent Heartbeat Endpoint (Public - for agents to report status)
@router.post("/instalados/{agente_id}/heartbeat")
def agent_heartbeat(
    agente_id: UUID,
    db: Session = Depends(get_db)
):
    """Endpoint for agents to send heartbeat signals"""
    success = crud_agents.register_agent_heartbeat(db, agente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Heartbeat received successfully"}


# Agent Task Endpoints
@router.post("/tareas/", response_model=schemas_agents.AgentTarea)
def create_agent_tarea(
    tarea: schemas_agents.AgentTareaCreate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Create a new agent task"""
    # Check permission
    check_permiso(current_usuario, "agent_tarea", "create")
    
    return crud_agents.create_agent_tarea(db, tarea)


@router.get("/tareas/{tarea_id}", response_model=schemas_agents.AgentTarea)
def get_agent_tarea(
    tarea_id: UUID,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get an agent task by ID"""
    # Check permission
    check_permiso(current_usuario, "agent_tarea", "read")
    
    db_tarea = crud_agents.get_agent_tarea(db, tarea_id)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_tarea


@router.get("/tareas/", response_model=List[schemas_agents.AgentTarea])
def get_agent_tareas(
    skip: int = 0,
    limit: int = 100,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Get all agent tasks"""
    # Check permission
    check_permiso(current_usuario, "agent_tarea", "read")
    
    # For now we'll just query all tasks, could be enhanced with filters
    return db.query(crud_agents.models.AgentTarea).offset(skip).limit(limit).all()


@router.put("/tareas/{tarea_id}", response_model=schemas_agents.AgentTarea)
def update_agent_tarea(
    tarea_id: UUID,
    tarea_update: schemas_agents.AgentTareaUpdate,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Update an agent task"""
    # Check permission
    check_permiso(current_usuario, "agent_tarea", "update")
    
    db_tarea = crud_agents.update_agent_tarea(db, tarea_id, tarea_update)
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_tarea


# Special endpoint for assigning tasks to available agents automatically
@router.post("/asignar-tarea/", response_model=schemas_agents.AgentTaskResponse)
def assign_task_to_available_agent(
    tipo_agente_nombre: str,
    tipo_tarea: str,
    parametros: str,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Assign a task to an available agent of the specified type"""
    # Check permission
    check_permiso(current_usuario, "agent_tarea", "create")
    
    # Validate agent type
    agent_tipo = crud_agents.get_agent_tipo_by_name(db, tipo_agente_nombre)
    if not agent_tipo:
        raise HTTPException(status_code=404, detail=f"Agent type '{tipo_agente_nombre}' not found")
    
    # Assign task to an available agent
    assigned_task = crud_agents.assign_task_to_available_agent(
        db, 
        tipo_agente_nombre, 
        tipo_tarea, 
        parametros
    )
    
    if not assigned_task:
        return schemas_agents.AgentTaskResponse(
            success=False,
            message=f"No available agents of type '{tipo_agente_nombre}' found"
        )
    
    return schemas_agents.AgentTaskResponse(
        success=True,
        message="Task assigned successfully",
        task_id=assigned_task.id,
        resultado_url=assigned_task.resultado_url
    )


# Registration endpoint for agents to register themselves
@router.post("/registro/", response_model=schemas_agents.AgentRegistrationResponse)
def register_new_agent(
    nombre_maquina: str,
    tipo_agente_nombre: str,
    direccion_ip: str = None,
    sistema_operativo: str = None,
    version_sistema: str = None,
    current_usuario: dict = Depends(get_current_usuario_activo),
    db: Session = Depends(get_db)
):
    """Endpoint for agents to register themselves on first installation"""
    # Check permission
    check_permiso(current_usuario, "agent_instalado", "create")
    
    # Get the agent type
    agent_tipo = crud_agents.get_agent_tipo_by_name(db, tipo_agente_nombre)
    if not agent_tipo:
        raise HTTPException(status_code=404, detail=f"Agent type '{tipo_agente_nombre}' not found")
    
    # Check if an agent with this machine name and type already exists
    existing_agent = crud_agents.get_agent_instalado_by_machine_and_tipo(
        db, 
        nombre_maquina, 
        agent_tipo.id
    )
    
    if existing_agent:
        # Update existing agent
        updated_agent = crud_agents.update_agent_instalado(
            db, 
            existing_agent.id, 
            schemas_agents.AgentInstaladoUpdate(
                direccion_ip=direccion_ip,
                sistema_operativo=sistema_operativo,
                version_sistema=version_sistema,
                activo=True
            )
        )
        
        return schemas_agents.AgentRegistrationResponse(
            success=True,
            message="Agent updated successfully",
            agent_id=updated_agent.id,
            token_acceso=updated_agent.token_acceso
        )
    
    # Generate a secure token for the new agent
    import secrets
    import string
    token_acceso = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    # Create new agent
    new_agent = schemas_agents.AgentInstaladoCreate(
        tipo_agente_id=agent_tipo.id,
        nombre_maquina=nombre_maquina,
        direccion_ip=direccion_ip,
        sistema_operativo=sistema_operativo,
        version_sistema=version_sistema,
        token_acceso=token_acceso
    )
    
    created_agent = crud_agents.create_agent_instalado(db, new_agent)
    
    return schemas_agents.AgentRegistrationResponse(
        success=True,
        message="Agent registered successfully",
        agent_id=created_agent.id,
        token_acceso=created_agent.token_acceso
    )