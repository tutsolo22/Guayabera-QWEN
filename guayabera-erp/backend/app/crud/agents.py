"""
CRUD operations for agents
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
import secrets
import string

from app.models.agent import AgentTipo, AgentInstalado, AgentTarea
from app.schemas.agent import (
    AgentTipo as AgentTipoSchema,
    AgentInstalado as AgentInstaladoSchema,
    AgentTarea as AgentTareaSchema,
    AgentTipoCreate,
    AgentTipoUpdate,
    AgentInstaladoCreate,
    AgentInstaladoUpdate,
    AgentTareaCreate,
    AgentTareaUpdate
)


def get_agent_tipo(db: Session, tipo_id: UUID) -> Optional[AgentTipoSchema]:
    """Get an agent type by ID"""
    return db.query(AgentTipo).filter(AgentTipo.id == tipo_id).first()


def get_agent_tipo_by_name(db: Session, nombre: str) -> Optional[AgentTipoSchema]:
    """Get an agent type by name"""
    return db.query(AgentTipo).filter(AgentTipo.nombre == nombre).first()


def get_agent_tipos(db: Session, skip: int = 0, limit: int = 100) -> List[AgentTipoSchema]:
    """Get all agent types"""
    return db.query(AgentTipo).offset(skip).limit(limit).all()


def create_agent_tipo(db: Session, agent_tipo: AgentTipoCreate) -> AgentTipoSchema:
    """Create a new agent type"""
    db_agent_tipo = AgentTipo(**agent_tipo.model_dump())
    db.add(db_agent_tipo)
    db.commit()
    db.refresh(db_agent_tipo)
    return db_agent_tipo


def update_agent_tipo(db: Session, tipo_id: UUID, agent_tipo: AgentTipoUpdate) -> Optional[AgentTipoSchema]:
    """Update an agent type"""
    db_agent_tipo = get_agent_tipo(db, tipo_id)
    if db_agent_tipo:
        update_data = agent_tipo.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_agent_tipo, field, value)
        db.commit()
        db.refresh(db_agent_tipo)
    return db_agent_tipo


def delete_agent_tipo(db: Session, tipo_id: UUID) -> bool:
    """Delete an agent type"""
    db_agent_tipo = get_agent_tipo(db, tipo_id)
    if db_agent_tipo:
        db.delete(db_agent_tipo)
        db.commit()
        return True
    return False


def get_agent_instalado(db: Session, agente_id: UUID) -> Optional[AgentInstaladoSchema]:
    """Get an installed agent by ID"""
    return db.query(AgentInstalado).filter(AgentInstalado.id == agente_id).first()


def get_active_agents_by_tipo(db: Session, tipo_id: UUID) -> List[AgentInstaladoSchema]:
    """Get all active agents of a specific type"""
    return db.query(AgentInstalado).filter(
        AgentInstalado.tipo_agente_id == tipo_id,
        AgentInstalado.activo == True
    ).all()


def get_agent_instalado_by_machine_and_tipo(
    db: Session, 
    nombre_maquina: str, 
    tipo_agente_id: UUID
) -> Optional[AgentInstaladoSchema]:
    """Get an installed agent by machine name and type"""
    return db.query(AgentInstalado).filter(
        AgentInstalado.nombre_maquina == nombre_maquina,
        AgentInstalado.tipo_agente_id == tipo_agente_id
    ).first()


def create_agent_instalado(
    db: Session, 
    agent_instalado: AgentInstaladoCreate
) -> AgentInstaladoSchema:
    """Create a new installed agent"""
    # Generate a secure token if not provided
    token = agent_instalado.token_acceso
    if not token:
        token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    db_agent_instalado = AgentInstalado(
        tipo_agente_id=agent_instalado.tipo_agente_id,
        nombre_maquina=agent_instalado.nombre_maquina,
        direccion_ip=agent_instalado.direccion_ip,
        sistema_operativo=agent_instalado.sistema_operativo,
        version_sistema=agent_instalado.version_sistema,
        version_agente=agent_instalado.version_agente,
        puerto_servicio=agent_instalado.puerto_servicio,
        activo=agent_instalado.activo,
        token_acceso=token
    )
    
    db.add(db_agent_instalado)
    db.commit()
    db.refresh(db_agent_instalado)
    return db_agent_instalado


def update_agent_instalado(
    db: Session, 
    agente_id: UUID, 
    agent_instalado: AgentInstaladoUpdate
) -> Optional[AgentInstaladoSchema]:
    """Update an installed agent"""
    db_agent = get_agent_instalado(db, agente_id)
    if db_agent:
        update_data = agent_instalado.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_agent, field, value)
        db.commit()
        db.refresh(db_agent)
    return db_agent


def register_agent_heartbeat(db: Session, agente_id: UUID) -> bool:
    """Update the heartbeat timestamp for an agent"""
    db_agent = get_agent_instalado(db, agente_id)
    if db_agent:
        db_agent.ultima_heartbeat = db_agent.ultima_conexion = db.func.now()
        db.commit()
        return True
    return False


def delete_agent_instalado(db: Session, agente_id: UUID) -> bool:
    """Delete an installed agent"""
    db_agent = get_agent_instalado(db, agente_id)
    if db_agent:
        db.delete(db_agent)
        db.commit()
        return True
    return False


def get_agent_tarea(db: Session, tarea_id: UUID) -> Optional[AgentTareaSchema]:
    """Get an agent task by ID"""
    return db.query(AgentTarea).filter(AgentTarea.id == tarea_id).first()


def get_agent_tareas_by_agente(
    db: Session, 
    agente_id: UUID, 
    skip: int = 0, 
    limit: int = 100
) -> List[AgentTareaSchema]:
    """Get all tasks for an agent"""
    return db.query(AgentTarea).filter(
        AgentTarea.agente_id == agente_id
    ).offset(skip).limit(limit).all()


def get_agent_tareas_by_estado(
    db: Session, 
    estado: str, 
    skip: int = 0, 
    limit: int = 100
) -> List[AgentTareaSchema]:
    """Get all tasks with a specific state"""
    return db.query(AgentTarea).filter(
        AgentTarea.estado == estado
    ).offset(skip).limit(limit).all()


def create_agent_tarea(db: Session, tarea: AgentTareaCreate) -> AgentTareaSchema:
    """Create a new agent task"""
    db_tarea = AgentTarea(**tarea.model_dump())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea


def update_agent_tarea(
    db: Session, 
    tarea_id: UUID, 
    tarea_update: AgentTareaUpdate
) -> Optional[AgentTareaSchema]:
    """Update an agent task"""
    db_tarea = get_agent_tarea(db, tarea_id)
    if db_tarea:
        update_data = tarea_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tarea, field, value)
        db.commit()
        db.refresh(db_tarea)
    return db_tarea


def assign_task_to_available_agent(
    db: Session, 
    tipo_agente_nombre: str, 
    tipo_tarea: str, 
    parametros: str
) -> Optional[AgentTareaSchema]:
    """Assign a task to an available agent of the specified type"""
    # Find the agent type
    agent_tipo = get_agent_tipo_by_name(db, tipo_agente_nombre)
    if not agent_tipo:
        return None
    
    # Find an active agent of this type
    available_agents = get_active_agents_by_tipo(db, agent_tipo.id)
    if not available_agents:
        return None
    
    # Select the first available agent (simple load balancing)
    target_agent = available_agents[0]
    
    # Create the task
    tarea_create = AgentTareaCreate(
        agente_id=target_agent.id,
        tipo_tarea=tipo_tarea,
        parametros=parametros,
        estado="pending"
    )
    
    return create_agent_tarea(db, tarea_create)