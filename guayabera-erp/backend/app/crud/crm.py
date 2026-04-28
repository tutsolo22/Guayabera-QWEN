"""
CRM CRUD Operations: Customer relationship management, interactions, marketing campaigns
Specialized for textile business customer management
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID

from app.models.crm import (
    Cliente, ContactoCliente, InteraccionCliente,
    Oportunidad, ActividadOportunidad, CampañaMarketing,
    Lead, CampaniaCliente
)
from app.schemas.crm import (
    ClienteCreate, ClienteUpdate,
    ContactoClienteCreate, ContactoClienteUpdate,
    InteraccionClienteCreate, InteraccionClienteUpdate,
    OportunidadCreate, OportunidadUpdate,
    ActividadOportunidadCreate, ActividadOportunidadUpdate,
    CampañaMarketingCreate, CampañaMarketingUpdate,
    LeadCreate, LeadUpdate,
    CampaniaClienteCreate, CampaniaClienteUpdate
)


# ============================================================================
# CUSTOMER CRUD
# ============================================================================

def create_cliente(db: Session, cliente_data: ClienteCreate) -> Cliente:
    """Create a new customer"""
    # Check if customer code already exists
    existing_cliente = db.query(Cliente).filter(Cliente.codigo_cliente == cliente_data.codigo_cliente).first()
    if existing_cliente:
        raise ValueError(f"A customer with code {cliente_data.codigo_cliente} already exists")
    
    db_cliente = Cliente(**cliente_data.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_cliente(db: Session, cliente_id: UUID) -> Optional[Cliente]:
    """Get a customer by ID"""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()


def get_cliente_by_codigo(db: Session, codigo_cliente: str) -> Optional[Cliente]:
    """Get a customer by code"""
    return db.query(Cliente).filter(Cliente.codigo_cliente == codigo_cliente).first()


def get_clientes(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    estado: Optional[str] = None,
    tipo_cliente: Optional[str] = None,
    segmento: Optional[str] = None
) -> List[Cliente]:
    """Get list of customers, optionally filtered"""
    query = db.query(Cliente)
    
    if estado:
        query = query.filter(Cliente.estado == estado)
    if tipo_cliente:
        query = query.filter(Cliente.tipo_cliente == tipo_cliente)
    if segmento:
        query = query.filter(Cliente.segmento == segmento)
    
    return query.offset(skip).limit(limit).all()


def update_cliente(db: Session, cliente_id: UUID, cliente_data: ClienteUpdate) -> Optional[Cliente]:
    """Update a customer"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        update_data = cliente_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cliente, field, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, cliente_id: UUID) -> bool:
    """Soft delete a customer"""
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db_cliente.activo = False
        db_cliente.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# CUSTOMER CONTACT CRUD
# ============================================================================

def create_contacto_cliente(db: Session, contacto_data: ContactoClienteCreate) -> ContactoCliente:
    """Create a new customer contact"""
    db_contacto = ContactoCliente(**contacto_data.model_dump())
    db.add(db_contacto)
    db.commit()
    db.refresh(db_contacto)
    return db_contacto


def get_contacto_cliente(db: Session, contacto_id: UUID) -> Optional[ContactoCliente]:
    """Get a customer contact by ID"""
    return db.query(ContactoCliente).filter(ContactoCliente.id == contacto_id).first()


def get_contactos_by_cliente(db: Session, cliente_id: UUID) -> List[ContactoCliente]:
    """Get all contacts for a specific customer"""
    return db.query(ContactoCliente).filter(ContactoCliente.cliente_id == cliente_id).all()


def update_contacto_cliente(db: Session, contacto_id: UUID, contacto_data: ContactoClienteUpdate) -> Optional[ContactoCliente]:
    """Update a customer contact"""
    db_contacto = get_contacto_cliente(db, contacto_id)
    if db_contacto:
        update_data = contacto_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contacto, field, value)
        db.commit()
        db.refresh(db_contacto)
    return db_contacto


def delete_contacto_cliente(db: Session, contacto_id: UUID) -> bool:
    """Soft delete a customer contact"""
    db_contacto = get_contacto_cliente(db, contacto_id)
    if db_contacto:
        db_contacto.activo = False
        db_contacto.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# CUSTOMER INTERACTION CRUD
# ============================================================================

def create_interaccion_cliente(db: Session, interaccion_data: InteraccionClienteCreate) -> InteraccionCliente:
    """Create a new customer interaction"""
    db_interaccion = InteraccionCliente(**interaccion_data.model_dump())
    db.add(db_interaccion)
    db.commit()
    db.refresh(db_interaccion)
    
    # Update last contact date in customer
    cliente = db.query(Cliente).filter(Cliente.id == interaccion_data.cliente_id).first()
    if cliente:
        cliente.fecha_ultimo_contacto = func.now()
        db.commit()
    
    return db_interaccion


def get_interaccion_cliente(db: Session, interaccion_id: UUID) -> Optional[InteraccionCliente]:
    """Get a customer interaction by ID"""
    return db.query(InteraccionCliente).filter(InteraccionCliente.id == interaccion_id).first()


def get_interacciones_by_cliente(db: Session, cliente_id: UUID, skip: int = 0, limit: int = 100) -> List[InteraccionCliente]:
    """Get all interactions for a specific customer"""
    return db.query(InteraccionCliente).filter(
        InteraccionCliente.cliente_id == cliente_id
    ).order_by(InteraccionCliente.fecha_interaccion.desc()).offset(skip).limit(limit).all()


def update_interaccion_cliente(db: Session, interaccion_id: UUID, interaccion_data: InteraccionClienteUpdate) -> Optional[InteraccionCliente]:
    """Update a customer interaction"""
    db_interaccion = get_interaccion_cliente(db, interaccion_id)
    if db_interaccion:
        update_data = interaccion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_interaccion, field, value)
        db.commit()
        db.refresh(db_interaccion)
    return db_interaccion


def delete_interaccion_cliente(db: Session, interaccion_id: UUID) -> bool:
    """Delete a customer interaction"""
    db_interaccion = get_interaccion_cliente(db, interaccion_id)
    if db_interaccion:
        db.delete(db_interaccion)
        db.commit()
        return True
    return False


# ============================================================================
# OPPORTUNITY CRUD
# ============================================================================

def create_oportunidad(db: Session, oportunidad_data: OportunidadCreate) -> Oportunidad:
    """Create a new sales opportunity"""
    db_oportunidad = Oportunidad(**oportunidad_data.model_dump())
    db.add(db_oportunidad)
    db.commit()
    db.refresh(db_oportunidad)
    return db_oportunidad


def get_oportunidad(db: Session, oportunidad_id: UUID) -> Optional[Oportunidad]:
    """Get a sales opportunity by ID"""
    return db.query(Oportunidad).filter(Oportunidad.id == oportunidad_id).first()


def get_oportunidades_by_cliente(db: Session, cliente_id: UUID, skip: int = 0, limit: int = 100) -> List[Oportunidad]:
    """Get all opportunities for a specific customer"""
    return db.query(Oportunidad).filter(
        Oportunidad.cliente_id == cliente_id
    ).offset(skip).limit(limit).all()


def get_oportunidades_by_vendedor(db: Session, vendedor_id: UUID, skip: int = 0, limit: int = 100) -> List[Oportunidad]:
    """Get all opportunities assigned to a specific salesperson"""
    return db.query(Oportunidad).filter(
        Oportunidad.vendedor_id == vendedor_id
    ).offset(skip).limit(limit).all()


def update_oportunidad(db: Session, oportunidad_id: UUID, oportunidad_data: OportunidadUpdate) -> Optional[Oportunidad]:
    """Update a sales opportunity"""
    db_oportunidad = get_oportunidad(db, oportunidad_id)
    if db_oportunidad:
        update_data = oportunidad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_oportunidad, field, value)
        db.commit()
        db.refresh(db_oportunidad)
    return db_oportunidad


def delete_oportunidad(db: Session, oportunidad_id: UUID) -> bool:
    """Soft delete a sales opportunity"""
    db_oportunidad = get_oportunidad(db, oportunidad_id)
    if db_oportunidad:
        db_oportunidad.activa = False
        db_oportunidad.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# OPPORTUNITY ACTIVITY CRUD
# ============================================================================

def create_actividad_oportunidad(db: Session, actividad_data: ActividadOportunidadCreate) -> ActividadOportunidad:
    """Create a new opportunity activity"""
    db_actividad = ActividadOportunidad(**actividad_data.model_dump())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


def get_actividad_oportunidad(db: Session, actividad_id: UUID) -> Optional[ActividadOportunidad]:
    """Get an opportunity activity by ID"""
    return db.query(ActividadOportunidad).filter(ActividadOportunidad.id == actividad_id).first()


def get_actividades_by_oportunidad(db: Session, oportunidad_id: UUID) -> List[ActividadOportunidad]:
    """Get all activities for a specific opportunity"""
    return db.query(ActividadOportunidad).filter(
        ActividadOportunidad.oportunidad_id == oportunidad_id
    ).order_by(ActividadOportunidad.fecha_vencimiento).all()


def update_actividad_oportunidad(db: Session, actividad_id: UUID, actividad_data: ActividadOportunidadUpdate) -> Optional[ActividadOportunidad]:
    """Update an opportunity activity"""
    db_actividad = get_actividad_oportunidad(db, actividad_id)
    if db_actividad:
        update_data = actividad_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_actividad, field, value)
        db.commit()
        db.refresh(db_actividad)
    return db_actividad


def delete_actividad_oportunidad(db: Session, actividad_id: UUID) -> bool:
    """Delete an opportunity activity"""
    db_actividad = get_actividad_oportunidad(db, actividad_id)
    if db_actividad:
        db.delete(db_actividad)
        db.commit()
        return True
    return False


# ============================================================================
# MARKETING CAMPAIGN CRUD
# ============================================================================

def create_campania_marketing(db: Session, campania_data: CampañaMarketingCreate) -> CampañaMarketing:
    """Create a new marketing campaign"""
    db_campania = CampañaMarketing(**campania_data.model_dump())
    db.add(db_campania)
    db.commit()
    db.refresh(db_campania)
    return db_campania


def get_campania_marketing(db: Session, campania_id: UUID) -> Optional[CampañaMarketing]:
    """Get a marketing campaign by ID"""
    return db.query(CampañaMarketing).filter(CampañaMarketing.id == campania_id).first()


def get_campanias_marketing(db: Session, skip: int = 0, limit: int = 100, estado: Optional[str] = None) -> List[CampañaMarketing]:
    """Get list of marketing campaigns, optionally filtered"""
    query = db.query(CampañaMarketing)
    
    if estado:
        query = query.filter(CampañaMarketing.estado == estado)
    
    return query.offset(skip).limit(limit).all()


def update_campania_marketing(db: Session, campania_id: UUID, campania_data: CampañaMarketingUpdate) -> Optional[CampañaMarketing]:
    """Update a marketing campaign"""
    db_campania = get_campania_marketing(db, campania_id)
    if db_campania:
        update_data = campania_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_campania, field, value)
        db.commit()
        db.refresh(db_campania)
    return db_campania


def delete_campania_marketing(db: Session, campania_id: UUID) -> bool:
    """Soft delete a marketing campaign"""
    db_campania = get_campania_marketing(db, campania_id)
    if db_campania:
        db_campania.activa = False
        db_campania.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# LEAD CRUD
# ============================================================================

def create_lead(db: Session, lead_data: LeadCreate) -> Lead:
    """Create a new lead"""
    db_lead = Lead(**lead_data.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


def get_lead(db: Session, lead_id: UUID) -> Optional[Lead]:
    """Get a lead by ID"""
    return db.query(Lead).filter(Lead.id == lead_id).first()


def get_leads_by_campania(db: Session, campania_id: UUID, skip: int = 0, limit: int = 100) -> List[Lead]:
    """Get all leads generated by a specific campaign"""
    return db.query(Lead).filter(Lead.campania_id == campania_id).offset(skip).limit(limit).all()


def update_lead(db: Session, lead_id: UUID, lead_data: LeadUpdate) -> Optional[Lead]:
    """Update a lead"""
    db_lead = get_lead(db, lead_id)
    if db_lead:
        update_data = lead_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_lead, field, value)
        db.commit()
        db.refresh(db_lead)
    return db_lead


def delete_lead(db: Session, lead_id: UUID) -> bool:
    """Soft delete a lead"""
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db_lead.activo = False
        db_lead.deleted_at = func.now()
        db.commit()
        return True
    return False


# ============================================================================
# CAMPAIGN-CUSTOMER RELATIONSHIP CRUD
# ============================================================================

def create_campania_cliente(db: Session, relacion_data: CampaniaClienteCreate) -> CampaniaCliente:
    """Create a new campaign-customer relationship"""
    db_relacion = CampaniaCliente(**relacion_data.model_dump())
    db.add(db_relacion)
    db.commit()
    db.refresh(db_relacion)
    return db_relacion


def get_campania_cliente(db: Session, relacion_id: UUID) -> Optional[CampaniaCliente]:
    """Get a campaign-customer relationship by ID"""
    return db.query(CampaniaCliente).filter(CampaniaCliente.id == relacion_id).first()


def get_clientes_by_campania(db: Session, campania_id: UUID) -> List[CampaniaCliente]:
    """Get all customers targeted by a specific campaign"""
    return db.query(CampaniaCliente).filter(CampaniaCliente.campania_id == campania_id).all()


def update_campania_cliente(db: Session, relacion_id: UUID, relacion_data: CampaniaClienteUpdate) -> Optional[CampaniaCliente]:
    """Update a campaign-customer relationship"""
    db_relacion = get_campania_cliente(db, relacion_id)
    if db_relacion:
        update_data = relacion_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_relacion, field, value)
        db.commit()
        db.refresh(db_relacion)
    return db_relacion


def delete_campania_cliente(db: Session, relacion_id: UUID) -> bool:
    """Delete a campaign-customer relationship"""
    db_relacion = get_campania_cliente(db, relacion_id)
    if db_relacion:
        db.delete(db_relacion)
        db.commit()
        return True
    return False