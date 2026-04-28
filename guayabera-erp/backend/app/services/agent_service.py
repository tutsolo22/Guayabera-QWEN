"""
Agent Service: Handles communication with local agents for CAD operations and printing
"""

import asyncio
import json
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import agents as crud_agents
from app.schemas import agents as schemas_agents


class AgentCommunicationService:
    """
    Service to handle communication with local agents
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.timeout = 30  # seconds
    
    def send_task_to_agent(
        self, 
        agent_id: UUID, 
        task_type: str, 
        parameters: Dict[str, Any]
    ) -> schemas_agents.AgentTaskResponse:
        """
        Send a task to a specific agent
        """
        # Get the agent from DB
        agent = crud_agents.get_agent_instalado(self.db, agent_id)
        if not agent:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message=f"Agent with ID {agent_id} not found"
            )
        
        try:
            # Construct the URL to call the agent
            agent_url = f"http://{agent.direccion_ip}:{agent.puerto_servicio}/execute-task"
            
            # Prepare the payload
            payload = {
                "task_type": task_type,
                "parameters": parameters,
                "token": agent.token_acceso  # Authenticate with the agent
            }
            
            # Send the request to the agent
            response = requests.post(
                agent_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return schemas_agents.AgentTaskResponse(
                    success=True,
                    message=result.get("message", "Task completed successfully"),
                    resultado_url=result.get("result_url"),
                    task_id=UUID(result.get("task_id")) if result.get("task_id") else None
                )
            else:
                return schemas_agents.AgentTaskResponse(
                    success=False,
                    message=f"Agent returned error: {response.status_code} - {response.text}"
                )
                
        except requests.exceptions.ConnectionError:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message=f"Could not connect to agent at {agent.direccion_ip}:{agent.puerto_servicio}"
            )
        except requests.exceptions.Timeout:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message=f"Timeout while waiting for agent response (>{self.timeout}s)"
            )
        except Exception as e:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message=f"Error communicating with agent: {str(e)}"
            )
    
    def get_agent_status(self, agent_id: UUID) -> Dict[str, Any]:
        """
        Get the status of a specific agent
        """
        agent = crud_agents.get_agent_instalado(self.db, agent_id)
        if not agent:
            return {
                "success": False,
                "message": f"Agent with ID {agent_id} not found"
            }
        
        try:
            # Construct the URL to call the agent
            agent_url = f"http://{agent.direccion_ip}:{agent.puerto_servicio}/status"
            
            # Prepare the payload with authentication
            payload = {
                "token": agent.token_acceso
            }
            
            # Send the request to the agent
            response = requests.get(
                agent_url,
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "status": result.get("status", "unknown"),
                    "capabilities": result.get("capabilities", []),
                    "resources": result.get("resources", {}),
                    "message": "Status retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "message": f"Agent returned error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": f"Could not connect to agent at {agent.direccion_ip}:{agent.puerto_servicio}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting agent status: {str(e)}"
            }
    
    def send_print_job(
        self, 
        document_data: str, 
        printer_name: Optional[str] = None,
        copies: int = 1
    ) -> schemas_agents.AgentTaskResponse:
        """
        Send a print job to an available print agent
        """
        # Find an available print agent
        print_agent_tipo = crud_agents.get_agent_tipo_by_name(self.db, "PRINT")
        if not print_agent_tipo:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="Print agent type not found"
            )
        
        available_agents = crud_agents.get_active_agents_by_tipo(self.db, print_agent_tipo.id)
        if not available_agents:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="No available print agents found"
            )
        
        # Use the first available agent (simple load balancing)
        agent = available_agents[0]
        
        # Prepare print parameters
        print_params = {
            "document_data": document_data,
            "printer_name": printer_name,
            "copies": copies
        }
        
        # Send task to agent
        return self.send_task_to_agent(agent.id, "print_document", print_params)
    
    def generate_pattern_locally(
        self,
        pattern_definition: Dict[str, Any],
        output_format: str = "DXF"
    ) -> schemas_agents.AgentTaskResponse:
        """
        Generate a pattern using a local CAD agent
        """
        # Find an available CAD agent
        cad_agent_tipo = crud_agents.get_agent_tipo_by_name(self.db, "CAD")
        if not cad_agent_tipo:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="CAD agent type not found"
            )
        
        available_agents = crud_agents.get_active_agents_by_tipo(self.db, cad_agent_tipo.id)
        if not available_agents:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="No available CAD agents found"
            )
        
        # Use the first available agent (simple load balancing)
        agent = available_agents[0]
        
        # Prepare pattern generation parameters
        pattern_params = {
            "pattern_definition": pattern_definition,
            "output_format": output_format
        }
        
        # Send task to agent
        return self.send_task_to_agent(agent.id, "generate_pattern", pattern_params)
    
    def render_design_locally(
        self,
        design_data: Dict[str, Any],
        output_format: str = "PNG",
        resolution: int = 300
    ) -> schemas_agents.AgentTaskResponse:
        """
        Render a design using a local design agent
        """
        # Find an available design agent
        design_agent_tipo = crud_agents.get_agent_tipo_by_name(self.db, "DESIGN")
        if not design_agent_tipo:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="Design agent type not found"
            )
        
        available_agents = crud_agents.get_active_agents_by_tipo(self.db, design_agent_tipo.id)
        if not available_agents:
            return schemas_agents.AgentTaskResponse(
                success=False,
                message="No available design agents found"
            )
        
        # Use the first available agent (simple load balancing)
        agent = available_agents[0]
        
        # Prepare design rendering parameters
        render_params = {
            "design_data": design_data,
            "output_format": output_format,
            "resolution": resolution
        }
        
        # Send task to agent
        return self.send_task_to_agent(agent.id, "render_design", render_params)
    
    def get_available_agents_by_type(self, agent_type_name: str) -> List[schemas_agents.AgentInstalado]:
        """
        Get all available agents of a specific type
        """
        agent_tipo = crud_agents.get_agent_tipo_by_name(self.db, agent_type_name)
        if not agent_tipo:
            return []
        
        return crud_agents.get_active_agents_by_tipo(self.db, agent_tipo.id)


# Global instance creation function
def get_agent_service(db: Session) -> AgentCommunicationService:
    """
    Factory function to create an agent communication service instance
    """
    return AgentCommunicationService(db)