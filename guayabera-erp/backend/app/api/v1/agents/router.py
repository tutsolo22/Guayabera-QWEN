"""
API Router para Agentes - Endpoints para interactuar con el sistema de agentes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Any, Dict, List
from pydantic import BaseModel, Field
import asyncio

from app.agents import orchestrator, AgentTask
from app.agents.database_agent import database_agent
from app.agents.testing_agent import testing_agent
from app.agents.uiux_agent import uiux_agent

router = APIRouter(prefix="/agents", tags=["agents"])


class TaskRequest(BaseModel):
    """Solicitud de tarea para agente"""
    agent_type: str = Field(..., description="Tipo de agente: database_agent, testing_agent, uiux_agent")
    action: str = Field(..., description="Acción a ejecutar")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parámetros para la acción")
    task_id: str = Field(default_factory=lambda: f"task_{asyncio.get_event_loop().time()}", description="ID único de tarea")


class TaskResponse(BaseModel):
    """Respuesta de tarea ejecutada"""
    success: bool
    message: str
    data: Dict[str, Any] = Field(default_factory=dict)


@router.get("/", response_model=List[Dict[str, Any]])
async def list_agents():
    """Listar todos los agentes disponibles"""
    return orchestrator.list_agents()


@router.get("/{agent_name}/status")
async def get_agent_status(agent_name: str):
    """Obtener estado de un agente específico"""
    agent = orchestrator.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{agent_name}' no encontrado")
    
    return {
        "name": agent.name,
        "version": agent.version,
        "status": agent.status.dict(),
        "capabilities": agent.get_capabilities()
    }


@router.post("/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """Ejecutar una tarea en un agente específico"""
    agent = orchestrator.get_agent(request.agent_type)
    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agente '{request.agent_type}' no encontrado. Agentes disponibles: {[a['name'] for a in orchestrator.list_agents()]}"
        )
    
    task = AgentTask(
        id=request.task_id,
        type=request.agent_type,
        description=f"{request.action} - {request.parameters}",
        parameters={
            "action": request.action,
            **request.parameters
        }
    )
    
    try:
        result = await agent.execute(task)
        
        if result.get("success"):
            return TaskResponse(
                success=True,
                message=result.get("message", "Tarea ejecutada exitosamente"),
                data=result
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Error al ejecutar la tarea")
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database/analyze")
async def analyze_database():
    """Analizar modelos de base de datos existentes"""
    result = await database_agent.execute(AgentTask(
        id="analyze_db",
        type="database_agent",
        description="Analizar modelos existentes",
        parameters={"action": "analyze_models"}
    ))
    
    return {"success": True, "data": result}


@router.post("/testing/coverage")
async def analyze_test_coverage():
    """Analizar cobertura de pruebas"""
    result = await testing_agent.execute(AgentTask(
        id="analyze_coverage",
        type="testing_agent",
        description="Analizar cobertura de tests",
        parameters={"action": "analyze_coverage"}
    ))
    
    return {"success": True, "data": result}


@router.post("/uiux/analyze")
async def analyze_ui_structure():
    """Analizar estructura UI/UX existente"""
    result = await uiux_agent.execute(AgentTask(
        id="analyze_ui",
        type="uiux_agent",
        description="Analizar estructura UI",
        parameters={"action": "analyze_ui"}
    ))
    
    return {"success": True, "data": result}


@router.get("/capabilities/{agent_name}")
async def get_agent_capabilities(agent_name: str):
    """Obtener capacidades específicas de un agente"""
    agent = orchestrator.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{agent_name}' no encontrado")
    
    return {
        "agent": agent_name,
        "capabilities": agent.get_capabilities()
    }
