"""
Helpdesk/Ticketing System CRUD Operations: Support tickets, assignments, and tracking
Specialized for ERP system support
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.helpdesk import (
    TicketSoporte, ComentarioTicket, HistorialEstado,
    CategoriaSoporte, SLA, DepartamentoSoporte, AgenteDepartamento
)
from app.schemas.helpdesk import (
    TicketSoporteCreate, TicketSoporteUpdate,
    ComentarioTicketCreate, ComentarioTicketUpdate,
    HistorialEstadoCreate,
    CategoriaSoporteCreate, CategoriaSoporteUpdate,
    SLACreate, SLAUpdate,
    DepartamentoSoporteCreate, DepartamentoSoporteUpdate,
    AgenteDepartamentoCreate, AgenteDepartamentoUpdate
)


# ============================================================================
# TICKET CRUD
# ============================================================================

def create_ticket_soporte(db: Session, ticket_data: TicketSoporteCreate) -> TicketSoporte:
    """Create a new support ticket"""
    # Generate unique folio if not provided
    if not ticket_data.folio:
        last_ticket = db.query(TicketSoporte).order_by(TicketSoporte.fecha_apertura.desc()).first()
        last_number = 1
        if last_ticket:
            try:
                last_number = int(last_ticket.folio.split('-')[1]) + 1
            except:
                last_number = 1
        ticket_data.folio = f"TICK-{last_number:05d}"
    
    # Get the supervisor for the requester
    from app.models.hr import Empleado
    solicitante = db.query(Empleado).filter(Empleado.id == ticket_data.solicitante_id).first()
    if solicitante and solicitante.jefe_directo_id:
        ticket_data.supervisor_id = solicitante.jefe_directo_id
    
    # Set deadline for user closure based on ticket type
    import datetime
    now = datetime.datetime.now()
    if ticket_data.tipo_solicitud in ['requisicion', 'compra']:
        # For purchases, give 48 hours after pre-closure for user to close
        ticket_data.fecha_limite_cierre = now + datetime.timedelta(hours=48)
    else:
        # For support tickets, give 48 hours after pre-closure for user to close
        ticket_data.fecha_limite_cierre = now + datetime.timedelta(hours=48)
    
    db_ticket = TicketSoporte(**ticket_data.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_ticket_soporte(db: Session, ticket_id: UUID) -> Optional[TicketSoporte]:
    """Get a support ticket by ID"""
    return db.query(TicketSoporte).filter(TicketSoporte.id == ticket_id).first()


def get_ticket_by_folio(db: Session, folio: str) -> Optional[TicketSoporte]:
    """Get a support ticket by folio"""
    return db.query(TicketSoporte).filter(TicketSoporte.folio == folio).first()


def get_tickets_by_estado(db: Session, estado: str, skip: int = 0, limit: int = 100) -> List[TicketSoporte]:
    """Get tickets by state"""
    return db.query(TicketSoporte).filter(TicketSoporte.estado == estado).offset(skip).limit(limit).all()


def get_tickets_by_solicitante(db: Session, solicitante_id: UUID, skip: int = 0, limit: int = 100) -> List[TicketSoporte]:
    """Get tickets by requester"""
    return db.query(TicketSoporte).filter(TicketSoporte.solicitante_id == solicitante_id).offset(skip).limit(limit).all()


def get_tickets_by_asignado(db: Session, asignado_a_id: UUID, skip: int = 0, limit: int = 100) -> List[TicketSoporte]:
    """Get tickets assigned to an employee"""
    return db.query(TicketSoporte).filter(TicketSoporte.asignado_a_id == asignado_a_id).offset(skip).limit(limit).all()


def update_ticket_soporte(db: Session, ticket_id: UUID, ticket_data: TicketSoporteUpdate) -> Optional[TicketSoporte]:
    """Update a support ticket"""
    db_ticket = get_ticket_soporte(db, ticket_id)
    if db_ticket:
        update_data = ticket_data.model_dump(exclude_unset=True)
        
        # If changing state, create a history entry
        if 'estado' in update_data and update_data['estado'] != db_ticket.estado:
            create_estado_historial(
                db,
                {
                    'ticket_id': ticket_id,
                    'estado_anterior': db_ticket.estado,
                    'estado_nuevo': update_data['estado'],
                    'cambiado_por_id': update_data.get('asignado_a_id', db_ticket.asignado_a_id) or db_ticket.solicitante_id
                }
            )
        
        # Handle supervisor notification and authorization
        if 'supervisor_id' in update_data and not db_ticket.fecha_notificacion_supervisor:
            # Send notification to supervisor
            db_ticket.fecha_notificacion_supervisor = func.now()
        
        # Handle supervisor authorization
        if 'autorizado_por_supervisor' in update_data and update_data['autorizado_por_supervisor']:
            db_ticket.autorizado_por_supervisor = True
            db_ticket.fecha_autorizacion_supervisor = func.now()
        
        # Handle finance authorization
        if 'autorizado_finanzas' in update_data and update_data['autorizado_finanzas']:
            db_ticket.autorizado_finanzas = True
            db_ticket.fecha_autorizacion_finanzas = func.now()
        
        # Handle pre-closure for purchase tickets
        if update_data.get('estado') == 'cerrado' and db_ticket.tipo_solicitud in ['requisicion', 'compra']:
            # Automatically close if past deadline
            if db_ticket.fecha_limite_cierre and datetime.datetime.now() > db_ticket.fecha_limite_cierre:
                db_ticket.estado = 'cerrado'
                db_ticket.fecha_cierre = func.now()
        
        for field, value in update_data.items():
            setattr(db_ticket, field, value)
        
        # Update assignment date if being assigned for the first time
        if db_ticket.asignado_a_id and not db_ticket.fecha_asignacion:
            db_ticket.fecha_asignacion = func.now()
        
        # Update resolution date if marked as resolved
        if db_ticket.estado == 'resuelto' and not db_ticket.fecha_resolucion:
            db_ticket.fecha_resolucion = func.now()
        
        # Update closing date if marked as closed
        if db_ticket.estado == 'cerrado' and not db_ticket.fecha_cierre:
            db_ticket.fecha_cierre = func.now()
            
        db.commit()
        db.refresh(db_ticket)
    return db_ticket


def delete_ticket_soporte(db: Session, ticket_id: UUID) -> bool:
    """Delete a support ticket"""
    db_ticket = get_ticket_soporte(db, ticket_id)
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
        return True
    return False


# ============================================================================
# COMMENT CRUD
# ============================================================================

def create_comentario_ticket(db: Session, comentario_data: ComentarioTicketCreate) -> ComentarioTicket:
    """Create a new ticket comment"""
    db_comentario = ComentarioTicket(**comentario_data.model_dump())
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario


def get_comentario_ticket(db: Session, comentario_id: UUID) -> Optional[ComentarioTicket]:
    """Get a ticket comment by ID"""
    return db.query(ComentarioTicket).filter(ComentarioTicket.id == comentario_id).first()


def get_comentarios_by_ticket(db: Session, ticket_id: UUID) -> List[ComentarioTicket]:
    """Get all comments for a specific ticket"""
    return db.query(ComentarioTicket).filter(ComentarioTicket.ticket_id == ticket_id).all()


def update_comentario_ticket(db: Session, comentario_id: UUID, comentario_data: ComentarioTicketUpdate) -> Optional[ComentarioTicket]:
    """Update a ticket comment"""
    db_comentario = get_comentario_ticket(db, comentario_id)
    if db_comentario:
        update_data = comentario_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comentario, field, value)
        db.commit()
        db.refresh(db_comentario)
    return db_comentario


def delete_comentario_ticket(db: Session, comentario_id: UUID) -> bool:
    """Delete a ticket comment"""
    db_comentario = get_comentario_ticket(db, comentario_id)
    if db_comentario:
        db.delete(db_comentario)
        db.commit()
        return True
    return False


# ============================================================================
# STATE HISTORY CRUD
# ============================================================================

def create_estado_historial(db: Session, historial_data: dict) -> HistorialEstado:
    """Create a new state history entry"""
    db_historial = HistorialEstado(**historial_data)
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


def get_estado_historial(db: Session, historial_id: UUID) -> Optional[HistorialEstado]:
    """Get a state history entry by ID"""
    return db.query(HistorialEstado).filter(HistorialEstado.id == historial_id).first()


def get_estado_historial_by_ticket(db: Session, ticket_id: UUID) -> List[HistorialEstado]:
    """Get all state history for a specific ticket"""
    return db.query(HistorialEstado).filter(HistorialEstado.ticket_id == ticket_id).order_by(HistorialEstado.fecha_cambio).all()


# ============================================================================
# SUPPORT CATEGORY CRUD
# ============================================================================

def create_categoria_soporte(db: Session, categoria_data: CategoriaSoporteCreate) -> CategoriaSoporte:
    """Create a new support category"""
    db_categoria = CategoriaSoporte(**categoria_data.model_dump())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def get_categoria_soporte(db: Session, categoria_id: UUID) -> Optional[CategoriaSoporte]:
    """Get a support category by ID"""
    return db.query(CategoriaSoporte).filter(CategoriaSoporte.id == categoria_id).first()


def get_categoria_soporte_by_codigo(db: Session, codigo: str) -> Optional[CategoriaSoporte]:
    """Get a support category by code"""
    return db.query(CategoriaSoporte).filter(CategoriaSoporte.codigo == codigo).first()


def get_categorias_soporte(db: Session, skip: int = 0, limit: int = 100, activa: Optional[bool] = None) -> List[CategoriaSoporte]:
    """Get list of support categories, optionally filtered"""
    query = db.query(CategoriaSoporte)
    
    if activa is not None:
        query = query.filter(CategoriaSoporte.activa == activa)
    
    return query.offset(skip).limit(limit).all()


def update_categoria_soporte(db: Session, categoria_id: UUID, categoria_data: CategoriaSoporteUpdate) -> Optional[CategoriaSoporte]:
    """Update a support category"""
    db_categoria = get_categoria_soporte(db, categoria_id)
    if db_categoria:
        update_data = categoria_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_categoria, field, value)
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def delete_categoria_soporte(db: Session, categoria_id: UUID) -> bool:
    """Delete a support category"""
    db_categoria = get_categoria_soporte(db, categoria_id)
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
        return True
    return False


# ============================================================================
# SLA CRUD
# ============================================================================

def create_sla(db: Session, sla_data: SLACreate) -> SLA:
    """Create a new SLA"""
    db_sla = SLA(**sla_data.model_dump())
    db.add(db_sla)
    db.commit()
    db.refresh(db_sla)
    return db_sla


def get_sla(db: Session, sla_id: UUID) -> Optional[SLA]:
    """Get an SLA by ID"""
    return db.query(SLA).filter(SLA.id == sla_id).first()


def get_sla_by_codigo(db: Session, codigo: str) -> Optional[SLA]:
    """Get an SLA by code"""
    return db.query(SLA).filter(SLA.codigo == codigo).first()


def get_slas(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[SLA]:
    """Get list of SLAs, optionally filtered"""
    query = db.query(SLA)
    
    if activo is not None:
        query = query.filter(SLA.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_sla(db: Session, sla_id: UUID, sla_data: SLAUpdate) -> Optional[SLA]:
    """Update an SLA"""
    db_sla = get_sla(db, sla_id)
    if db_sla:
        update_data = sla_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sla, field, value)
        db.commit()
        db.refresh(db_sla)
    return db_sla


def delete_sla(db: Session, sla_id: UUID) -> bool:
    """Delete an SLA"""
    db_sla = get_sla(db, sla_id)
    if db_sla:
        db.delete(db_sla)
        db.commit()
        return True
    return False


# ============================================================================
# SUPPORT DEPARTMENT CRUD
# ============================================================================

def create_departamento_soporte(db: Session, dept_data: DepartamentoSoporteCreate) -> DepartamentoSoporte:
    """Create a new support department"""
    db_dept = DepartamentoSoporte(**dept_data.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept


def get_departamento_soporte(db: Session, dept_id: UUID) -> Optional[DepartamentoSoporte]:
    """Get a support department by ID"""
    return db.query(DepartamentoSoporte).filter(DepartamentoSoporte.id == dept_id).first()


def get_departamento_soporte_by_departamento_id(db: Session, dept_id: UUID) -> Optional[DepartamentoSoporte]:
    """Get a support department by department ID"""
    return db.query(DepartamentoSoporte).filter(DepartamentoSoporte.departamento_id == dept_id).first()


def get_departamentos_soporte(db: Session, skip: int = 0, limit: int = 100, activo: Optional[bool] = None) -> List[DepartamentoSoporte]:
    """Get list of support departments, optionally filtered"""
    query = db.query(DepartamentoSoporte)
    
    if activo is not None:
        query = query.filter(DepartamentoSoporte.activo == activo)
    
    return query.offset(skip).limit(limit).all()


def update_departamento_soporte(db: Session, dept_id: UUID, dept_data: DepartamentoSoporteUpdate) -> Optional[DepartamentoSoporte]:
    """Update a support department"""
    db_dept = get_departamento_soporte(db, dept_id)
    if db_dept:
        update_data = dept_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_dept, field, value)
        db.commit()
        db.refresh(db_dept)
    return db_dept


def delete_departamento_soporte(db: Session, dept_id: UUID) -> bool:
    """Delete a support department"""
    db_dept = get_departamento_soporte(db, dept_id)
    if db_dept:
        db.delete(db_dept)
        db.commit()
        return True
    return False


# ============================================================================
# AGENT DEPARTMENT LINK CRUD
# ============================================================================

def create_agente_departamento(db: Session, link_data: AgenteDepartamentoCreate) -> AgenteDepartamento:
    """Create a new agent-department link"""
    db_link = AgenteDepartamento(**link_data.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def get_agente_departamento(db: Session, link_id: UUID) -> Optional[AgenteDepartamento]:
    """Get an agent-department link by ID"""
    return db.query(AgenteDepartamento).filter(AgenteDepartamento.id == link_id).first()


def get_agentes_by_departamento(db: Session, dept_id: UUID) -> List[AgenteDepartamento]:
    """Get all agents for a specific support department"""
    return db.query(AgenteDepartamento).filter(AgenteDepartamento.departamento_soporte_id == dept_id).all()


def get_departamentos_by_agente(db: Session, empleado_id: UUID) -> List[AgenteDepartamento]:
    """Get all support departments for a specific agent"""
    return db.query(AgenteDepartamento).filter(AgenteDepartamento.empleado_id == empleado_id).all()


def update_agente_departamento(db: Session, link_id: UUID, link_data: AgenteDepartamentoUpdate) -> Optional[AgenteDepartamento]:
    """Update an agent-department link"""
    db_link = get_agente_departamento(db, link_id)
    if db_link:
        update_data = link_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_link, field, value)
        db.commit()
        db.refresh(db_link)
    return db_link


def delete_agente_departamento(db: Session, link_id: UUID) -> bool:
    """Delete an agent-department link"""
    db_link = get_agente_departamento(db, link_id)
    if db_link:
        db.delete(db_link)
        db.commit()
        return True
    return False


def close_ticket_if_expired(db: Session, ticket_id: UUID) -> bool:
    """Close ticket automatically if expired"""
    db_ticket = get_ticket_soporte(db, ticket_id)
    if db_ticket and db_ticket.fecha_limite_cierre and datetime.datetime.now() > db_ticket.fecha_limite_cierre:
        if db_ticket.estado in ['pre-cerrado', 'resuelto']:
            db_ticket.estado = 'cerrado'
            db_ticket.fecha_cierre = func.now()
            db.commit()
            db.refresh(db_ticket)
            return True
    return False
