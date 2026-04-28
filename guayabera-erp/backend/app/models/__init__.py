"""
CRM models
"""

from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    company = Column(String(100))
    position = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interactions = relationship("Interaction", back_populates="customer")
    opportunities = relationship("SalesOpportunity", back_populates="customer")
    contacts = relationship("Contact", back_populates="customer")

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    position = Column(String(50))
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    customer = relationship("Customer", back_populates="contacts")
    interactions = relationship("Interaction", back_populates="contact")

class Interaction(Base):
    __tablename__ = 'interactions'
    
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)  # Llamada, Email, Reunión, etc.
    subject = Column(String(100), nullable=False)
    notes = Column(String(500))
    date = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    
    customer = relationship("Customer", back_populates="interactions")
    contact = relationship("Contact", back_populates="interactions")

class SalesOpportunity(Base):
    __tablename__ = 'sales_opportunities'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    value = Column(Integer)  # Valor estimado en USD
    probability = Column(Integer)  # Probabilidad de cierre en %
    status = Column(String(30))  # "Prospecto", "Negociación", "Cerrado ganado", "Cerrado perdido"
    expected_close_date = Column(DateTime)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    customer = relationship("Customer", back_populates="opportunities")
    stages = relationship("SalesStage", back_populates="opportunity")

class SalesStage(Base):
    __tablename__ = 'sales_stages'
    
    id = Column(Integer, primary_key=True)
    stage = Column(String(30), nullable=False)  # "Contacto inicial", "Presentación", "Propuesta", etc.
    description = Column(String(500))
    estimated_value = Column(Integer)
    probability = Column(Integer)  # Probabilidad de avance en %
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    opportunity_id = Column(Integer, ForeignKey('sales_opportunities.id'), nullable=False)
    
    opportunity = relationship("SalesOpportunity", back_populates="stages")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    due_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
    priority = Column(String(20))  # "Alta", "Media", "Baja"
    assigned_to_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    related_to_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    assigned_to = relationship("User", back_populates="assigned_tasks")
    related_to = relationship("Customer", back_populates="tasks")

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    customer = relationship("Customer", back_populates="notes")
    
class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    customer = relationship("Customer", back_populates="tags")
"""
Import all models so SQLAlchemy can find them
"""

from app.core.database import Base

from .admin import *
from .security import *
from .finance import *
from .supply_chain import *
from .production import *
from .hr import *
from .sales import *
from .inventory import *
from .cad import *
from .size_chart import *
from .helpdesk import *
from .requisitions import *
from .notifications import *
from .quality_control import *
from .advanced_accounting import *
from .logistics import *
from .crm import *
from .project_management import *
from .asset_management import *
from .business_intelligence import *
from .invoice import *
from .email_config import *
from .payroll import *
from .agents import *

__all__ = ["Base"] + admin.__all__ + security.__all__ + finance.__all__ + supply_chain.__all__ + production.__all__ + hr.__all__ + sales.__all__ + inventory.__all__ + cad.__all__ + size_chart.__all__ + helpdesk.__all__ + requisitions.__all__ + notifications.__all__ + quality_control.__all__ + advanced_accounting.__all__ + logistics.__all__ + crm.__all__ + project_management.__all__ + asset_management.__all__ + business_intelligence.__all__ + invoice.__all__ + email_config.__all__ + payroll.__all__ + agents.__all__
