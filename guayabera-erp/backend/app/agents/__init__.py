"""
Agents Module - GuayaberaERP
Sistema de Agentes de Codificación Inteligente para desarrollo acelerado del ERP
"""

from .core import (
    BaseAgent,
    AgentStatus,
    AgentTask,
    AgentOrchestrator,
    orchestrator
)

from .database_agent import database_agent, DatabaseAgent
from .testing_agent import testing_agent, TestingAgent
from .uiux_agent import uiux_agent, UIUXAgent

# Registrar agentes en el orquestador
orchestrator.register_agent(database_agent)
orchestrator.register_agent(testing_agent)
orchestrator.register_agent(uiux_agent)

__all__ = [
    # Core
    "BaseAgent",
    "AgentStatus",
    "AgentTask",
    "AgentOrchestrator",
    "orchestrator",
    
    # Agents
    "database_agent",
    "DatabaseAgent",
    "testing_agent",
    "TestingAgent",
    "uiux_agent",
    "UIUXAgent",
]
