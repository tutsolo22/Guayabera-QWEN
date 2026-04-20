"""
Agent Core Module - GuayaberaERP
Sistema de Agentes de Codificación Inteligente
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class AgentStatus(BaseModel):
    """Estado del agente"""
    name: str
    status: str = "idle"  # idle, running, completed, error
    current_task: Optional[str] = None
    progress: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class AgentTask(BaseModel):
    """Tarea para el agente"""
    id: str
    type: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    priority: int = 1
    created_at: datetime = Field(default_factory=datetime.now)


class BaseAgent(ABC):
    """Clase base para todos los agentes"""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.status = AgentStatus(name=name)
        self.logger = logging.getLogger(f"agents.{name}")
    
    @abstractmethod
    async def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Ejecutar la tarea asignada"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Retornar las capacidades del agente"""
        pass
    
    def start_task(self, task: AgentTask):
        """Iniciar una tarea"""
        self.status.status = "running"
        self.status.current_task = task.description
        self.status.started_at = datetime.now()
        self.status.progress = 0.0
        self.logger.info(f"Iniciando tarea: {task.description}")
    
    def complete_task(self, result: Dict[str, Any]):
        """Completar una tarea exitosamente"""
        self.status.status = "completed"
        self.status.completed_at = datetime.now()
        self.status.progress = 100.0
        self.logger.info(f"Tarea completada: {self.status.current_task}")
        return result
    
    def fail_task(self, error: str):
        """Marcar tarea como fallida"""
        self.status.status = "error"
        self.status.error_message = error
        self.logger.error(f"Tarea fallida: {error}")
        return {"success": False, "error": error}
    
    def update_progress(self, progress: float):
        """Actualizar progreso de la tarea"""
        self.status.progress = min(100.0, max(0.0, progress))


class AgentOrchestrator:
    """Orquestador de agentes - coordina múltiples agentes"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.logger = logging.getLogger("agents.orchestrator")
    
    def register_agent(self, agent: BaseAgent):
        """Registrar un agente en el orquestador"""
        self.agents[agent.name] = agent
        self.logger.info(f"Agente registrado: {agent.name} v{agent.version}")
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """Obtener un agente por nombre"""
        return self.agents.get(name)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """Listar todos los agentes registrados"""
        return [
            {
                "name": agent.name,
                "version": agent.version,
                "status": agent.status.status,
                "capabilities": agent.get_capabilities()
            }
            for agent in self.agents.values()
        ]
    
    async def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Ejecutar una tarea con el agente apropiado"""
        agent = self.get_agent(task.type)
        if not agent:
            return {"success": False, "error": f"Agente '{task.type}' no encontrado"}
        
        try:
            return await agent.execute(task)
        except Exception as e:
            self.logger.error(f"Error ejecutando tarea: {str(e)}")
            return {"success": False, "error": str(e)}


# Singleton del orquestador
orchestrator = AgentOrchestrator()
