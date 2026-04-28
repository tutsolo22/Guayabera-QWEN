"""
CRM API Router: Customer relationship management, interactions, marketing campaigns
Specialized for textile business customer management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.crm import (
    ClienteCreate, ClienteUpdate, ClienteResponse,
    ContactoClienteCreate, ContactoClienteUpdate, ContactoClienteResponse,
    InteraccionClienteCreate, InteraccionClienteUpdate, InteraccionClienteResponse,
    OportunidadCreate, OportunidadUpdate, OportunidadResponse,
    ActividadOportunidadCreate, ActividadOportunidadUpdate, ActividadOportunidadResponse,
    CampañaMarketingCreate, CampañaMarketingUpdate, CampañaMarketingResponse,
    LeadCreate, LeadUpdate, LeadResponse,
    CampaniaClienteCreate, CampaniaClienteUpdate, CampaniaClienteResponse
)
from app.crud.crm import (
    create_cliente, get_cliente, get_cliente_by_codigo,
    get_clientes, update_cliente, delete_cliente,
    create_contacto_cliente, get_contacto_cliente, get_contactos_by_cliente,
    update_contacto_cliente, delete_contacto_cliente,
    create_interaccion_cliente, get_interaccion_cliente, get_interacciones_by_cliente,
    update_interaccion_cliente, delete_interaccion_cliente,
    create_oportunidad, get_oportunidad, get_oportunidades_by_cliente,
    get_oportunidades_by_vendedor, update_oportunidad, delete_oportunidad,
    create_actividad_oportunidad, get_actividad_oportunidad, get_actividades_by_oportunidad,
    update_actividad_oportunidad, delete_actividad_oportunidad,
    create_campania_marketing, get_campania_marketing, get_campanias_marketing,
    update_campania_marketing, delete_campania_marketing,
    create_lead, get_lead, get_leads_by_campania,
    update_lead, delete_lead,
    create_campania_cliente, get_campania_cliente, get_clientes_by_campania,
    update_campania_cliente, delete_campania_cliente
)

router = APIRouter(prefix="/crm", tags=["CRM"])

# ============================================================================
# CUSTOMER ENDPOINTS
# ============================================================================

@router.post("/customers/", response_model=ClienteResponse)
def create_customer(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    try:
        return create_cliente(db=db, cliente_data=cliente)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/customers/{cliente_id}", response_model=ClienteResponse)
def get_customer(cliente_id: str, db: Session = Depends(get_db)):
    """Get a customer by ID"""
    cliente = get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return cliente


@router.get("/customers/code/{codigo_cliente}", response_model=ClienteResponse)
def get_customer_by_code(codigo_cliente: str, db: Session = Depends(get_db)):
    """Get a customer by code"""
    cliente = get_cliente_by_codigo(db, codigo_cliente)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return cliente


@router.get("/customers/", response_model=List[ClienteResponse])
def get_customers(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    tipo_cliente: Optional[str] = None,
    segmento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of customers, optionally filtered"""
    return get_clientes(db, skip, limit, estado, tipo_cliente, segmento)


@router.put("/customers/{cliente_id}", response_model=ClienteResponse)
def update_customer(
    cliente_id: str, 
    cliente_data: ClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a customer"""
    updated_cliente = update_cliente(
        db=db, 
        cliente_id=cliente_id, 
        cliente_data=cliente_data
    )
    if not updated_cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return updated_cliente


@router.delete("/customers/{cliente_id}")
def delete_customer(cliente_id: str, db: Session = Depends(get_db)):
    """Soft delete a customer"""
    success = delete_cliente(db=db, cliente_id=cliente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return {"message": "Customer deactivated successfully"}


# ============================================================================
# CUSTOMER CONTACT ENDPOINTS
# ============================================================================

@router.post("/customer-contacts/", response_model=ContactoClienteResponse)
def create_customer_contact(contacto: ContactoClienteCreate, db: Session = Depends(get_db)):
    """Create a new customer contact"""
    return create_contacto_cliente(db=db, contacto_data=contacto)


@router.get("/customer-contacts/{contacto_id}", response_model=ContactoClienteResponse)
def get_customer_contact(contacto_id: str, db: Session = Depends(get_db)):
    """Get a customer contact by ID"""
    contacto = get_contacto_cliente(db, contacto_id)
    if not contacto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer contact not found"
        )
    return contacto


@router.get("/customers/{cliente_id}/contacts", response_model=List[ContactoClienteResponse])
def get_contacts_by_customer(cliente_id: str, db: Session = Depends(get_db)):
    """Get all contacts for a specific customer"""
    return get_contactos_by_cliente(db, cliente_id)


@router.put("/customer-contacts/{contacto_id}", response_model=ContactoClienteResponse)
def update_customer_contact(
    contacto_id: str, 
    contacto_data: ContactoClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a customer contact"""
    updated_contacto = update_contacto_cliente(
        db=db, 
        contacto_id=contacto_id, 
        contacto_data=contacto_data
    )
    if not updated_contacto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer contact not found"
        )
    return updated_contacto


@router.delete("/customer-contacts/{contacto_id}")
def delete_customer_contact(contacto_id: str, db: Session = Depends(get_db)):
    """Soft delete a customer contact"""
    success = delete_contacto_cliente(db=db, contacto_id=contacto_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer contact not found"
        )
    return {"message": "Customer contact deactivated successfully"}


# ============================================================================
# CUSTOMER INTERACTION ENDPOINTS
# ============================================================================

@router.post("/interactions/", response_model=InteraccionClienteResponse)
def create_customer_interaction(interaccion: InteraccionClienteCreate, db: Session = Depends(get_db)):
    """Create a new customer interaction"""
    return create_interaccion_cliente(db=db, interaccion_data=interaccion)


@router.get("/interactions/{interaccion_id}", response_model=InteraccionClienteResponse)
def get_customer_interaction(interaccion_id: str, db: Session = Depends(get_db)):
    """Get a customer interaction by ID"""
    interaccion = get_interaccion_cliente(db, interaccion_id)
    if not interaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer interaction not found"
        )
    return interaccion


@router.get("/customers/{cliente_id}/interactions", response_model=List[InteraccionClienteResponse])
def get_interactions_by_customer(
    cliente_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all interactions for a specific customer"""
    return get_interacciones_by_cliente(db, cliente_id, skip, limit)


@router.put("/interactions/{interaccion_id}", response_model=InteraccionClienteResponse)
def update_customer_interaction(
    interaccion_id: str, 
    interaccion_data: InteraccionClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a customer interaction"""
    updated_interaccion = update_interaccion_cliente(
        db=db, 
        interaccion_id=interaccion_id, 
        interaccion_data=interaccion_data
    )
    if not updated_interaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer interaction not found"
        )
    return updated_interaccion


@router.delete("/interactions/{interaccion_id}")
def delete_customer_interaction(interaccion_id: str, db: Session = Depends(get_db)):
    """Delete a customer interaction"""
    success = delete_interaccion_cliente(db=db, interaccion_id=interaccion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer interaction not found"
        )
    return {"message": "Customer interaction deleted successfully"}


# ============================================================================
# OPPORTUNITY ENDPOINTS
# ============================================================================

@router.post("/opportunities/", response_model=OportunidadResponse)
def create_opportunity(oportunidad: OportunidadCreate, db: Session = Depends(get_db)):
    """Create a new sales opportunity"""
    return create_oportunidad(db=db, oportunidad_data=oportunidad)


@router.get("/opportunities/{oportunidad_id}", response_model=OportunidadResponse)
def get_opportunity(oportunidad_id: str, db: Session = Depends(get_db)):
    """Get a sales opportunity by ID"""
    oportunidad = get_oportunidad(db, oportunidad_id)
    if not oportunidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return oportunidad


@router.get("/customers/{cliente_id}/opportunities", response_model=List[OportunidadResponse])
def get_opportunities_by_customer(
    cliente_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all opportunities for a specific customer"""
    return get_oportunidades_by_cliente(db, cliente_id, skip, limit)


@router.get("/salespeople/{vendedor_id}/opportunities", response_model=List[OportunidadResponse])
def get_opportunities_by_salesperson(
    vendedor_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all opportunities assigned to a specific salesperson"""
    return get_oportunidades_by_vendedor(db, vendedor_id, skip, limit)


@router.put("/opportunities/{oportunidad_id}", response_model=OportunidadResponse)
def update_opportunity(
    oportunidad_id: str, 
    oportunidad_data: OportunidadUpdate, 
    db: Session = Depends(get_db)
):
    """Update a sales opportunity"""
    updated_oportunidad = update_oportunidad(
        db=db, 
        oportunidad_id=oportunidad_id, 
        oportunidad_data=oportunidad_data
    )
    if not updated_oportunidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return updated_oportunidad


@router.delete("/opportunities/{oportunidad_id}")
def delete_opportunity(oportunidad_id: str, db: Session = Depends(get_db)):
    """Soft delete a sales opportunity"""
    success = delete_oportunidad(db=db, oportunidad_id=oportunidad_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return {"message": "Opportunity deactivated successfully"}


# ============================================================================
# OPPORTUNITY ACTIVITY ENDPOINTS
# ============================================================================

@router.post("/opportunity-activities/", response_model=ActividadOportunidadResponse)
def create_opportunity_activity(actividad: ActividadOportunidadCreate, db: Session = Depends(get_db)):
    """Create a new opportunity activity"""
    return create_actividad_oportunidad(db=db, actividad_data=actividad)


@router.get("/opportunity-activities/{actividad_id}", response_model=ActividadOportunidadResponse)
def get_opportunity_activity(actividad_id: str, db: Session = Depends(get_db)):
    """Get an opportunity activity by ID"""
    actividad = get_actividad_oportunidad(db, actividad_id)
    if not actividad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity activity not found"
        )
    return actividad


@router.get("/opportunities/{oportunidad_id}/activities", response_model=List[ActividadOportunidadResponse])
def get_activities_by_opportunity(oportunidad_id: str, db: Session = Depends(get_db)):
    """Get all activities for a specific opportunity"""
    return get_actividades_by_oportunidad(db, oportunidad_id)


@router.put("/opportunity-activities/{actividad_id}", response_model=ActividadOportunidadResponse)
def update_opportunity_activity(
    actividad_id: str, 
    actividad_data: ActividadOportunidadUpdate, 
    db: Session = Depends(get_db)
):
    """Update an opportunity activity"""
    updated_actividad = update_actividad_oportunidad(
        db=db, 
        actividad_id=actividad_id, 
        actividad_data=actividad_data
    )
    if not updated_actividad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity activity not found"
        )
    return updated_actividad


@router.delete("/opportunity-activities/{actividad_id}")
def delete_opportunity_activity(actividad_id: str, db: Session = Depends(get_db)):
    """Delete an opportunity activity"""
    success = delete_actividad_oportunidad(db=db, actividad_id=actividad_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity activity not found"
        )
    return {"message": "Opportunity activity deleted successfully"}


# ============================================================================
# MARKETING CAMPAIGN ENDPOINTS
# ============================================================================

@router.post("/marketing-campaigns/", response_model=CampañaMarketingResponse)
def create_marketing_campaign(campania: CampañaMarketingCreate, db: Session = Depends(get_db)):
    """Create a new marketing campaign"""
    return create_campania_marketing(db=db, campania_data=campania)


@router.get("/marketing-campaigns/{campania_id}", response_model=CampañaMarketingResponse)
def get_marketing_campaign(campania_id: str, db: Session = Depends(get_db)):
    """Get a marketing campaign by ID"""
    campania = get_campania_marketing(db, campania_id)
    if not campania:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marketing campaign not found"
        )
    return campania


@router.get("/marketing-campaigns/", response_model=List[CampañaMarketingResponse])
def get_marketing_campaigns(
    skip: int = 0, 
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of marketing campaigns, optionally filtered"""
    return get_campanias_marketing(db, skip, limit, estado)


@router.put("/marketing-campaigns/{campania_id}", response_model=CampañaMarketingResponse)
def update_marketing_campaign(
    campania_id: str, 
    campania_data: CampañaMarketingUpdate, 
    db: Session = Depends(get_db)
):
    """Update a marketing campaign"""
    updated_campania = update_campania_marketing(
        db=db, 
        campania_id=campania_id, 
        campania_data=campania_data
    )
    if not updated_campania:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marketing campaign not found"
        )
    return updated_campania


@router.delete("/marketing-campaigns/{campania_id}")
def delete_marketing_campaign(campania_id: str, db: Session = Depends(get_db)):
    """Soft delete a marketing campaign"""
    success = delete_campania_marketing(db=db, campania_id=campania_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Marketing campaign not found"
        )
    return {"message": "Marketing campaign deactivated successfully"}


# ============================================================================
# LEAD ENDPOINTS
# ============================================================================

@router.post("/leads/", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    return create_lead(db=db, lead_data=lead)


@router.get("/leads/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: str, db: Session = Depends(get_db)):
    """Get a lead by ID"""
    lead = get_lead(db, lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return lead


@router.get("/campaigns/{campania_id}/leads", response_model=List[LeadResponse])
def get_leads_by_campaign(
    campania_id: str, 
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all leads generated by a specific campaign"""
    return get_leads_by_campania(db, campania_id, skip, limit)


@router.put("/leads/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: str, 
    lead_data: LeadUpdate, 
    db: Session = Depends(get_db)
):
    """Update a lead"""
    updated_lead = update_lead(
        db=db, 
        lead_id=lead_id, 
        lead_data=lead_data
    )
    if not updated_lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return updated_lead


@router.delete("/leads/{lead_id}")
def delete_lead(lead_id: str, db: Session = Depends(get_db)):
    """Soft delete a lead"""
    success = delete_lead(db=db, lead_id=lead_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    return {"message": "Lead deactivated successfully"}


# ============================================================================
# CAMPAIGN-CUSTOMER RELATIONSHIP ENDPOINTS
# ============================================================================

@router.post("/campaign-customer-relations/", response_model=CampaniaClienteResponse)
def create_campaign_customer_relation(relacion: CampaniaClienteCreate, db: Session = Depends(get_db)):
    """Create a new campaign-customer relationship"""
    return create_campania_cliente(db=db, relacion_data=relacion)


@router.get("/campaign-customer-relations/{relacion_id}", response_model=CampaniaClienteResponse)
def get_campaign_customer_relation(relacion_id: str, db: Session = Depends(get_db)):
    """Get a campaign-customer relationship by ID"""
    relacion = get_campania_cliente(db, relacion_id)
    if not relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign-customer relationship not found"
        )
    return relacion


@router.get("/campaigns/{campania_id}/targeted-customers", response_model=List[CampaniaClienteResponse])
def get_customers_by_campaign(campania_id: str, db: Session = Depends(get_db)):
    """Get all customers targeted by a specific campaign"""
    return get_clientes_by_campania(db, campania_id)


@router.put("/campaign-customer-relations/{relacion_id}", response_model=CampaniaClienteResponse)
def update_campaign_customer_relation(
    relacion_id: str, 
    relacion_data: CampaniaClienteUpdate, 
    db: Session = Depends(get_db)
):
    """Update a campaign-customer relationship"""
    updated_relacion = update_campania_cliente(
        db=db, 
        relacion_id=relacion_id, 
        relacion_data=relacion_data
    )
    if not updated_relacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign-customer relationship not found"
        )
    return updated_relacion


@router.delete("/campaign-customer-relations/{relacion_id}")
def delete_campaign_customer_relation(relacion_id: str, db: Session = Depends(get_db)):
    """Delete a campaign-customer relationship"""
    success = delete_campania_cliente(db=db, relacion_id=relacion_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign-customer relationship not found"
        )
    return {"message": "Campaign-customer relationship deleted successfully"}