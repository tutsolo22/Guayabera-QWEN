"""
CRM Models: Customer relationship management, interactions, marketing campaigns
Specialized for textile business customer management
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


# ============================================================================
# ENUMS
# ============================================================================

class TipoCliente(enum.Enum):
    MAYOREO = "mayoreo"
    MENDEO = "mendeo"
    CORPORATIVO = "corporativo"
    PARTICULAR = "particular"
    PROFESIONAL = "profesional"


class EstadoCliente(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"
    PROSPECTO = "prospecto"


class TipoContacto(enum.Enum):
    CLIENTE = "cliente"
    CONTACTO = "contacto"
    PROVEEDOR = "proveedor"


class CanalInteraccion(enum.Enum):
    LLAMADA = "llamada"
    CORREO = "correo"
    VISITA = "visita"
    REDES_SOCIALES = "redes_sociales"
    WEB = "web"
    CHAT = "chat"


class EstadoOportunidad(enum.Enum):
    NUEVA = "nueva"
    CALIFICANDO = "calificando"
    PROPUESTA = "propuesta"
    NEGOCIACION = "negociacion"
    GANADA = "ganada"
    PERDIDA = "perdida"


class EstadoCampaña(enum.Enum):
    PROGRAMADA = "programada"
    ACTIVA = "activa"
    PAUSADA = "pausada"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class TipoCampaña(enum.Enum):
    EMAIL = "email"
    TELEFONO = "telefono"
    SOCIAL_MEDIA = "social_media"
    DIRECTA = "directa"
    EVENTO = "evento"


class PrioridadTarea(enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


# ============================================================================
# CRM MODELS
# ============================================================================

class Cliente(Base):
    """Customer management - Gestión de clientes"""
    __tablename__ = "crm_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    codigo_cliente = Column(String(30), unique=True, nullable=False, index=True)  # Unique client code
    nombre_comercial = Column(String(100), nullable=False)
    razon_social = Column(String(150))
    tipo_cliente = Column(SQLEnum(TipoCliente), default=TipoCliente.PARTICULAR)
    estado = Column(SQLEnum(EstadoCliente), default=EstadoCliente.PROSPECTO)
    
    # Contact information
    direccion = Column(Text)
    ciudad = Column(String(100))
    estado_provincia = Column(String(100))
    pais = Column(String(100), default="México")
    codigo_postal = Column(String(10))
    telefono = Column(String(20))
    email = Column(String(100))
    sitio_web = Column(String(150))
    
    # Financial information
    limite_credito = Column(Numeric(12, 2), default=0.00)
    dias_credito = Column(Integer, default=0)
    saldo_pendiente = Column(Numeric(12, 2), default=0.00)
    
    # Classification
    segmento = Column(String(50))  # Premium, estandar, etc.
    industria = Column(String(100))  # Sector al que pertenece el cliente
    fuente_origen = Column(String(50))  # Referido, publicidad, etc.
    
    # Relationship management
    vendedor_asignado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Assigned salesperson
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_ultimo_contacto = Column(DateTime(timezone=True))
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    datos_adicionales = Column(JSONB)  # Additional client-specific data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    vendedor_asignado = relationship("Empleado")
    oportunidades = relationship("Oportunidad", back_populates="cliente")
    interacciones = relationship("InteraccionCliente", back_populates="cliente")
    contactos = relationship("ContactoCliente", back_populates="cliente")


class ContactoCliente(Base):
    """Customer contact management - Gestión de contactos del cliente"""
    __tablename__ = "crm_contacto_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"), nullable=False)
    
    # Contact information
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(50))
    apellido_materno = Column(String(50))
    puesto = Column(String(100))
    departamento = Column(String(100))
    
    # Contact details
    telefono = Column(String(20))
    extension = Column(String(10))
    email = Column(String(100))
    skype = Column(String(50))
    
    # Status
    es_principal = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    cliente = relationship("Cliente", back_populates="contactos")


class InteraccionCliente(Base):
    """Customer interaction tracking - Seguimiento de interacciones con clientes"""
    __tablename__ = "crm_interaccion_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"), nullable=False)
    contacto_id = Column(UUID(as_uuid=True), ForeignKey("crm_contacto_cliente.id"))  # Specific contact involved
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Salesperson involved
    
    # Interaction details
    tipo_interaccion = Column(SQLEnum(CanalInteraccion), nullable=False)
    asunto = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Outcome and follow-up
    resultado = Column(String(100))  # Meeting result, call outcome, etc.
    proximo_seguimiento = Column(DateTime(timezone=True))  # Next follow-up date
    realizado = Column(Boolean, default=False)
    
    # Status
    fecha_interaccion = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cliente = relationship("Cliente", back_populates="interacciones")
    contacto = relationship("ContactoCliente")
    vendedor = relationship("Empleado")


class Oportunidad(Base):
    """Sales opportunity management - Gestión de oportunidades de venta"""
    __tablename__ = "crm_oportunidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"), nullable=False)
    vendedor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Assigned salesperson
    
    # Opportunity details
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    valor_estimado = Column(Numeric(12, 2), default=0.00)
    probabilidad_cierre = Column(Integer, default=0)  # Percentage (0-100)
    
    # Status and timeline
    estado = Column(SQLEnum(EstadoOportunidad), default=EstadoOportunidad.NUEVA)
    fecha_cierre_estimada = Column(Date)
    fecha_cierre_real = Column(Date)
    
    # Classification
    tipo_oportunidad = Column(String(50))  # Renovación, nuevo producto, etc.
    origen = Column(String(50))  # From campaign, referral, etc.
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    cliente = relationship("Cliente", back_populates="oportunidades")
    vendedor = relationship("Empleado")
    actividades = relationship("ActividadOportunidad", back_populates="oportunidad")


class ActividadOportunidad(Base):
    """Opportunity activity tracking - Seguimiento de actividades en oportunidades"""
    __tablename__ = "crm_actividad_oportunidad"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    oportunidad_id = Column(UUID(as_uuid=True), ForeignKey("crm_oportunidad.id"), nullable=False)
    asignado_a_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Assigned to employee
    
    # Activity details
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    tipo_actividad = Column(String(50))  # Meeting, call, demo, etc.
    prioridad = Column(SQLEnum(PrioridadTarea), default=PrioridadTarea.MEDIA)
    
    # Timeline
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_vencimiento = Column(DateTime(timezone=True))
    fecha_completada = Column(DateTime(timezone=True))
    
    # Status
    estado = Column(String(30), default="pendiente")  # pendiente, en_progreso, completada, cancelada
    completada = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    oportunidad = relationship("Oportunidad", back_populates="actividades")
    asignado_a = relationship("Empleado")


class CampañaMarketing(Base):
    """Marketing campaign management - Gestión de campañas de marketing"""
    __tablename__ = "crm_campania_marketing"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Campaign identification
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    tipo_campania = Column(SQLEnum(TipoCampaña), nullable=False)
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    estado = Column(SQLEnum(EstadoCampaña), default=EstadoCampaña.PROGRAMADA)
    
    # Target and budget
    presupuesto = Column(Numeric(12, 2), default=0.00)
    gastos_realizados = Column(Numeric(12, 2), default=0.00)
    objetivo = Column(Text)  # What the campaign aims to achieve
    
    # Performance metrics
    alcance_esperado = Column(Integer, default=0)
    alcance_real = Column(Integer, default=0)
    conversiones_esperadas = Column(Integer, default=0)
    conversiones_obtenidas = Column(Integer, default=0)
    
    # Management
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsible employee
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    responsable = relationship("Empleado")
    clientes_objetivo = relationship("Cliente", secondary="crm_campania_cliente")
    leads_generados = relationship("Lead", back_populates="campania")


class Lead(Base):
    """Potential customer lead - Lead potencial de cliente"""
    __tablename__ = "crm_lead"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campania_id = Column(UUID(as_uuid=True), ForeignKey("crm_campania_marketing.id"))  # Generated from campaign
    
    # Lead information
    nombre_completo = Column(String(150), nullable=False)
    empresa = Column(String(100))
    puesto = Column(String(100))
    email = Column(String(100), nullable=False)
    telefono = Column(String(20))
    
    # Lead qualification
    fuente = Column(String(50))  # How the lead was acquired
    calificacion = Column(Integer, default=0)  # Score from 0-100
    estado = Column(String(30), default="nuevo")  # nuevo, calificado, convertido, descartado
    
    # Conversion tracking
    cliente_convertido_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"))  # If converted to customer
    fecha_conversion = Column(DateTime(timezone=True))
    
    # Management
    asignado_a_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Assigned to employee
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    campania = relationship("CampañaMarketing", back_populates="leads_generados")
    cliente_convertido = relationship("Cliente")
    asignado_a = relationship("Empleado")


class CampaniaCliente(Base):
    """Association table between campaigns and customers - Tabla de asociación entre campañas y clientes"""
    __tablename__ = "crm_campania_cliente"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campania_id = Column(UUID(as_uuid=True), ForeignKey("crm_campania_marketing.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"), nullable=False)
    
    # Response tracking
    respondio = Column(Boolean, default=False)
    fecha_respuesta = Column(DateTime(timezone=True))
    tipo_respuesta = Column(String(50))  # positive, negative, neutral
    notas = Column(Text)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())