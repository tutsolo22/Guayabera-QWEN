"""
Helpdesk/Ticketing System API Router: Support tickets, assignments, and tracking
Specialized for ERP system support
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.helpdesk import (
    TicketSoporteCreate, TicketSoporteUpdate, TicketSoporteResponse,
    ComentarioTicketCreate, ComentarioTicketUpdate, ComentarioTicketResponse,
    HistorialEstadoCreate, HistorialEstadoResponse,
    CategoriaSoporteCreate, CategoriaSoporteUpdate, CategoriaSoporteResponse,
    SLACreate, SLAUpdate, SLAResponse,
    DepartamentoSoporteCreate, DepartamentoSoporteUpdate, DepartamentoSoporteResponse,
    AgenteDepartamentoCreate, AgenteDepartamentoUpdate, AgenteDepartamentoResponse
)
from app.crud.helpdesk import (
    create_ticket_soporte, get_ticket_soporte, get_ticket_by_folio,
    get_tickets_by_estado, get_tickets_by_solicitante, get_tickets_by_asignado,
    update_ticket_soporte, delete_ticket_soporte,
    create_comentario_ticket, get_comentario_ticket, get_comentarios_by_ticket,
    update_comentario_ticket, delete_comentario_ticket,
    create_estado_historial, get_estado_historial, get_estado_historial_by_ticket,
    create_categoria_soporte, get_categoria_soporte, get_categoria_soporte_by_codigo,
    get_categorias_soporte, update_categoria_soporte, delete_categoria_soporte,
    create_sla, get_sla, get_sla_by_codigo, get_slas, update_sla, delete_sla,
    create_departamento_soporte, get_departamento_soporte, get_departamento_soporte_by_departamento_id,
    get_departamentos_soporte, update_departamento_soporte, delete_departamento_soporte,
    create_agente_departamento, get_agente_departamento, get_agentes_by_departamento,
    get_departamentos_by_agente, update_agente_departamento, delete_agente_departamento
)

router = APIRouter(prefix="/helpdesk", tags=["Helpdesk"])

# ============================================================================
# TICKET ENDPOINTS
# ============================================================================

@router.post("/tickets/", response_model=TicketSoporteResponse)
def create_support_ticket(ticket: TicketSoporteCreate, db: Session = Depends(get_db)):
    """Create a new support ticket"""
    # Check if ticket folio already exists
    if ticket.folio:
        existing_ticket = get_ticket_by_folio(db, ticket.folio)
        if existing_ticket:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ticket with this folio already exists"
            )
    
    return create_ticket_soporte(db=db, ticket_data=ticket)


@router.get("/tickets/{ticket_id}", response_model=TicketSoporteResponse)
def get_support_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """Get a support ticket by ID"""
    ticket = get_ticket_soporte(db, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket


@router.get("/tickets/folio/{folio}", response_model=TicketSoporteResponse)
def get_ticket_by_folio_endpoint(folio: str, db: Session = Depends(get_db)):
    """Get a support ticket by folio"""
    ticket = get_ticket_by_folio(db, folio)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return ticket


@router.get("/tickets/", response_model=List[TicketSoporteResponse])
def get_support_tickets(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    solicitante_id: Optional[str] = None,
    asignado_a_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of support tickets, optionally filtered"""
    if estado:
        return get_tickets_by_estado(db, estado, skip, limit)
    elif solicitante_id:
        return get_tickets_by_solicitante(db, solicitante_id, skip, limit)
    elif asignado_a_id:
        return get_tickets_by_asignado(db, asignado_a_id, skip, limit)
    else:
        return get_tickets_by_estado(db, "abierto", skip, limit)


@router.put("/tickets/{ticket_id}", response_model=TicketSoporteResponse)
def update_support_ticket(
    ticket_id: str, 
    ticket_data: TicketSoporteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a support ticket"""
    updated_ticket = update_ticket_soporte(
        db=db, 
        ticket_id=ticket_id, 
        ticket_data=ticket_data
    )
    if not updated_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return updated_ticket


@router.delete("/tickets/{ticket_id}")
def delete_support_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """Delete a support ticket"""
    success = delete_ticket_soporte(db=db, ticket_id=ticket_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    return {"message": "Ticket deleted successfully"}


# ============================================================================
# COMMENT ENDPOINTS
# ============================================================================

@router.post("/comments/", response_model=ComentarioTicketResponse)
def create_ticket_comment(comentario: ComentarioTicketCreate, db: Session = Depends(get_db)):
    """Create a new ticket comment"""
    return create_comentario_ticket(db=db, comentario_data=comentario)


@router.get("/comments/{comentario_id}", response_model=ComentarioTicketResponse)
def get_ticket_comment(comentario_id: str, db: Session = Depends(get_db)):
    """Get a ticket comment by ID"""
    comentario = get_comentario_ticket(db, comentario_id)
    if not comentario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return comentario


@router.get("/tickets/{ticket_id}/comments", response_model=List[ComentarioTicketResponse])
def get_ticket_comments(ticket_id: str, db: Session = Depends(get_db)):
    """Get all comments for a specific ticket"""
    return get_comentarios_by_ticket(db, ticket_id)


@router.put("/comments/{comentario_id}", response_model=ComentarioTicketResponse)
def update_ticket_comment(
    comentario_id: str, 
    comentario_data: ComentarioTicketUpdate, 
    db: Session = Depends(get_db)
):
    """Update a ticket comment"""
    updated_comentario = update_comentario_ticket(
        db=db, 
        comentario_id=comentario_id, 
        comentario_data=comentario_data
    )
    if not updated_comentario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return updated_comentario


@router.delete("/comments/{comentario_id}")
def delete_ticket_comment(comentario_id: str, db: Session = Depends(get_db)):
    """Delete a ticket comment"""
    success = delete_comentario_ticket(db=db, comentario_id=comentario_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return {"message": "Comment deleted successfully"}


# ============================================================================
# STATE HISTORY ENDPOINTS
# ============================================================================

@router.post("/state-history/", response_model=HistorialEstadoResponse)
def create_state_history(historial: HistorialEstadoCreate, db: Session = Depends(get_db)):
    """Create a new state history entry"""
    return create_estado_historial(db=db, historial_data=historial.dict())


@router.get("/state-history/{historial_id}", response_model=HistorialEstadoResponse)
def get_state_history(historial_id: str, db: Session = Depends(get_db)):
    """Get a state history entry by ID"""
    historial = get_estado_historial(db, historial_id)
    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="State history entry not found"
        )
    return historial


@router.get("/tickets/{ticket_id}/state-history", response_model=List[HistorialEstadoResponse])
def get_ticket_state_history(ticket_id: str, db: Session = Depends(get_db)):
    """Get all state history for a specific ticket"""
    return get_estado_historial_by_ticket(db, ticket_id)


# ============================================================================
# SUPPORT CATEGORY ENDPOINTS
# ============================================================================

@router.post("/categories/", response_model=CategoriaSoporteResponse)
def create_support_category(categoria: CategoriaSoporteCreate, db: Session = Depends(get_db)):
    """Create a new support category"""
    # Check if category code already exists
    existing_categoria = get_categoria_soporte_by_codigo(db, categoria.codigo)
    if existing_categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this code already exists"
        )
    
    return create_categoria_soporte(db=db, categoria_data=categoria)


@router.get("/categories/{categoria_id}", response_model=CategoriaSoporteResponse)
def get_support_category(categoria_id: str, db: Session = Depends(get_db)):
    """Get a support category by ID"""
    categoria = get_categoria_soporte(db, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return categoria


@router.get("/categories/", response_model=List[CategoriaSoporteResponse])
def get_support_categories(
    skip: int = 0, 
    limit: int = 100,
    activa: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of support categories, optionally filtered"""
    return get_categorias_soporte(db, skip, limit, activa)


@router.put("/categories/{categoria_id}", response_model=CategoriaSoporteResponse)
def update_support_category(
    categoria_id: str, 
    categoria_data: CategoriaSoporteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a support category"""
    updated_categoria = update_categoria_soporte(
        db=db, 
        categoria_id=categoria_id, 
        categoria_data=categoria_data
    )
    if not updated_categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return updated_categoria


@router.delete("/categories/{categoria_id}")
def delete_support_category(categoria_id: str, db: Session = Depends(get_db)):
    """Delete a support category"""
    success = delete_categoria_soporte(db=db, categoria_id=categoria_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return {"message": "Category deleted successfully"}


# ============================================================================
# SLA ENDPOINTS
# ============================================================================

@router.post("/slas/", response_model=SLAResponse)
def create_sla(sla: SLACreate, db: Session = Depends(get_db)):
    """Create a new SLA"""
    # Check if SLA code already exists
    existing_sla = get_sla_by_codigo(db, sla.codigo)
    if existing_sla:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SLA with this code already exists"
        )
    
    return create_sla(db=db, sla_data=sla)


@router.get("/slas/{sla_id}", response_model=SLAResponse)
def get_sla_by_id(sla_id: str, db: Session = Depends(get_db)):
    """Get an SLA by ID"""
    sla = get_sla(db, sla_id)
    if not sla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA not found"
        )
    return sla


@router.get("/slas/", response_model=List[SLAResponse])
def get_slas_list(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of SLAs, optionally filtered"""
    return get_slas(db, skip, limit, activo)


@router.put("/slas/{sla_id}", response_model=SLAResponse)
def update_sla_endpoint(
    sla_id: str, 
    sla_data: SLAUpdate, 
    db: Session = Depends(get_db)
):
    """Update an SLA"""
    updated_sla = update_sla(
        db=db, 
        sla_id=sla_id, 
        sla_data=sla_data
    )
    if not updated_sla:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA not found"
        )
    return updated_sla


@router.delete("/slas/{sla_id}")
def delete_sla_endpoint(sla_id: str, db: Session = Depends(get_db)):
    """Delete an SLA"""
    success = delete_sla(db=db, sla_id=sla_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA not found"
        )
    return {"message": "SLA deleted successfully"}


# ============================================================================
# SUPPORT DEPARTMENT ENDPOINTS
# ============================================================================

@router.post("/support-departments/", response_model=DepartamentoSoporteResponse)
def create_support_department(dept: DepartamentoSoporteCreate, db: Session = Depends(get_db)):
    """Create a new support department"""
    return create_departamento_soporte(db=db, dept_data=dept)


@router.get("/support-departments/{dept_id}", response_model=DepartamentoSoporteResponse)
def get_support_department(dept_id: str, db: Session = Depends(get_db)):
    """Get a support department by ID"""
    dept = get_departamento_soporte(db, dept_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support department not found"
        )
    return dept


@router.get("/departments/{departamento_id}/support", response_model=DepartamentoSoporteResponse)
def get_support_department_by_department_id(departamento_id: str, db: Session = Depends(get_db)):
    """Get a support department by department ID"""
    dept = get_departamento_soporte_by_departamento_id(db, departamento_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support department not found"
        )
    return dept


@router.get("/support-departments/", response_model=List[DepartamentoSoporteResponse])
def get_support_departments_list(
    skip: int = 0, 
    limit: int = 100,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of support departments, optionally filtered"""
    return get_departamentos_soporte(db, skip, limit, activo)


@router.put("/support-departments/{dept_id}", response_model=DepartamentoSoporteResponse)
def update_support_department(
    dept_id: str, 
    dept_data: DepartamentoSoporteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a support department"""
    updated_dept = update_departamento_soporte(
        db=db, 
        dept_id=dept_id, 
        dept_data=dept_data
    )
    if not updated_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support department not found"
        )
    return updated_dept


@router.delete("/support-departments/{dept_id}")
def delete_support_department(dept_id: str, db: Session = Depends(get_db)):
    """Delete a support department"""
    success = delete_departamento_soporte(db=db, dept_id=dept_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support department not found"
        )
    return {"message": "Support department deleted successfully"}


# ============================================================================
# AGENT DEPARTMENT LINK ENDPOINTS
# ============================================================================

@router.post("/agent-department-links/", response_model=AgenteDepartamentoResponse)
def create_agent_department_link(link: AgenteDepartamentoCreate, db: Session = Depends(get_db)):
    """Create a new agent-department link"""
    return create_agente_departamento(db=db, link_data=link)


@router.get("/agent-department-links/{link_id}", response_model=AgenteDepartamentoResponse)
def get_agent_department_link(link_id: str, db: Session = Depends(get_db)):
    """Get an agent-department link by ID"""
    link = get_agente_departamento(db, link_id)
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent-department link not found"
        )
    return link


@router.get("/departments/{dept_id}/agents", response_model=List[AgenteDepartamentoResponse])
def get_agents_by_department(dept_id: str, db: Session = Depends(get_db)):
    """Get all agents for a specific support department"""
    return get_agentes_by_departamento(db, dept_id)


@router.get("/agents/{empleado_id}/departments", response_model=List[AgenteDepartamentoResponse])
def get_departments_by_agent(empleado_id: str, db: Session = Depends(get_db)):
    """Get all support departments for a specific agent"""
    return get_departamentos_by_agente(db, empleado_id)


@router.put("/agent-department-links/{link_id}", response_model=AgenteDepartamentoResponse)
def update_agent_department_link(
    link_id: str, 
    link_data: AgenteDepartamentoUpdate, 
    db: Session = Depends(get_db)
):
    """Update an agent-department link"""
    updated_link = update_agente_departamento(
        db=db, 
        link_id=link_id, 
        link_data=link_data
    )
    if not updated_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent-department link not found"
        )
    return updated_link


@router.delete("/agent-department-links/{link_id}")
def delete_agent_department_link(link_id: str, db: Session = Depends(get_db)):
    """Delete an agent-department link"""
    success = delete_agente_departamento(db=db, link_id=link_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent-department link not found"
        )
    return {"message": "Agent-department link deleted successfully"}