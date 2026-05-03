"""
Helpdesk/Ticketing System Models: Support tickets, assignments, and tracking
Specialized for ERP system support
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

class PrioridadTicket(enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class EstadoTicket(enum.Enum):
    ABIERTO = "abierto"
    ASIGNADO = "asignado"
    EN_PROCESO = "en_proceso"
    EN_ESPERA = "en_espera"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"
    CANCELADO = "cancelado"


class CategoriaTicket(enum.Enum):
    SISTEMA = "sistema"
    USUARIO = "usuario"
    HARDWARE = "hardware"
    SOFTWARE = "software"
    SEGURIDAD = "seguridad"
    RED = "red"
    INTEGRACION = "integracion"
    RENDIMIENTO = "rendimiento"


class CanalEntrada(enum.Enum):
    WEB = "web"
    EMAIL = "email"
    TELEFONO = "telefono"
    CHAT = "chat"


# ============================================================================
# HELPDESK MODELS
# ============================================================================

class TicketSoporte(Base):
    """Support ticket management - Gestión de tickets de soporte"""
    __tablename__ = "hd_ticket_soporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Ticket identification
    folio = Column(String(20), unique=True, nullable=False, index=True)  # Folio único del ticket
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    
    # Classification
    categoria = Column(SQLEnum(CategoriaTicket), nullable=False)
    prioridad = Column(SQLEnum(PrioridadTicket), default=PrioridadTicket.MEDIA)
    canal_entrada = Column(SQLEnum(CanalEntrada), default=CanalEntrada.WEB)
    
    # Assignment and tracking
    solicitante_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Employee who opened the ticket
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Immediate supervisor of requester
    asignado_a_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Employee assigned to resolve
    departamento_id = Column(Integer, ForeignKey("departamentos.id"))  # Changed from UUID to Integer to match departamentos table - Department responsible
    
    # Approval tracking
    autorizado_por_supervisor = Column(Boolean, default=False)
    fecha_autorizacion_supervisor = Column(DateTime(timezone=True))
    fecha_notificacion_supervisor = Column(DateTime(timezone=True))
    
    # Status
    estado = Column(SQLEnum(EstadoTicket), default=EstadoTicket.ABIERTO)
    
    # Dates
    fecha_apertura = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_asignacion = Column(DateTime(timezone=True))
    fecha_resolucion = Column(DateTime(timezone=True))
    fecha_cierre = Column(DateTime(timezone=True))
    
    # SLA tracking
    fecha_limite_respuesta = Column(DateTime(timezone=True))  # Deadline for first response
    fecha_limite_resolucion = Column(DateTime(timezone=True))  # Deadline for resolution
    fecha_limite_cierre = Column(DateTime(timezone=True))  # Deadline for closure by user
    horas_acumuladas = Column(Float, default=0.0)  # Time spent on the ticket
    
    # Additional data
    etiquetas = Column(JSONB)  # Tags for the ticket
    datos_adicionales = Column(JSONB)  # Additional data for integration with Active Directory
    tipo_solicitud = Column(String(30), default="soporte")  # "soporte", "requisicion", "compra"
    
    # Requisition/compra related fields
    numero_requisicion = Column(String(30))  # For purchase requisitions
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"))  # Supplier for purchase req.
    cotizaciones = Column(JSONB)  # Quotations received
    autorizado_finanzas = Column(Boolean, default=False)  # Finance approval
    fecha_autorizacion_finanzas = Column(DateTime(timezone=True))
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    solicitante = relationship("Empleado", foreign_keys=[solicitante_id], backref="tickets_abiertos")
    supervisor = relationship("Empleado", foreign_keys=[supervisor_id])
    asignado_a = relationship("Empleado", foreign_keys=[asignado_a_id], backref="tickets_asignados")
    departamento = relationship("Departamento")
    proveedor = relationship("Proveedor")
    comentarios_ticket = relationship("ComentarioTicket", back_populates="ticket")
    historial_estado = relationship("HistorialEstado", back_populates="ticket")


class ComentarioTicket(Base):
    """Comments for support tickets - Comentarios para tickets de soporte"""
    __tablename__ = "hd_comentario_ticket"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("hd_ticket_soporte.id"), nullable=False)
    autor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    
    # Comment content
    contenido = Column(Text, nullable=False)
    es_interno = Column(Boolean, default=False)  # Internal note vs visible to requester
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ticket = relationship("TicketSoporte", back_populates="comentarios_ticket")
    autor = relationship("Empleado")


class HistorialEstado(Base):
    """State history for tickets - Historial de estados para tickets"""
    __tablename__ = "hd_historial_estado"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("hd_ticket_soporte.id"), nullable=False)
    estado_anterior = Column(SQLEnum(EstadoTicket))
    estado_nuevo = Column(SQLEnum(EstadoTicket), nullable=False)
    cambiado_por_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    motivo_cambio = Column(Text)  # Reason for the state change
    
    # Timestamps
    fecha_cambio = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Relationships
    ticket = relationship("TicketSoporte", back_populates="historial_estado")
    cambiado_por = relationship("Empleado")


class CategoriaSoporte(Base):
    """Categories for support tickets - Categorías para tickets de soporte"""
    __tablename__ = "hd_categoria_soporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Category details
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    color_hex = Column(String(7))  # Color for UI representation
    
    # Parent category (for hierarchical structure)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("hd_categoria_soporte.id"))
    
    # SLA defaults
    horas_respuesta = Column(Integer)  # Hours for first response
    horas_resolucion = Column(Integer)  # Hours for resolution
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    parent = relationship("CategoriaSoporte", remote_side=[id])
    subcategorias = relationship("CategoriaSoporte")


class SLA(Base):
    """Service Level Agreement definition - Definición de Acuerdos de Nivel de Servicio"""
    __tablename__ = "hd_sla"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # SLA details
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    
    # SLA metrics
    horas_para_respuesta = Column(Integer, nullable=False)  # Hours for first response
    horas_para_resolucion = Column(Integer, nullable=False)  # Hours for resolution
    nivel_objetivo = Column(Float, default=95.0)  # Target percentage of tickets resolved on time (%)
    
    # Application rules
    prioridad_aplicable = Column(SQLEnum(PrioridadTicket))  # Applies to specific priority
    categoria_aplicable = Column(SQLEnum(CategoriaTicket))  # Applies to specific category
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class DepartamentoSoporte(Base):
    """Support departments - Departamentos de soporte"""
    __tablename__ = "hd_departamento_soporte"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    departamento_id = Column(Integer, ForeignKey("departamentos.id"), nullable=False)  # Changed from UUID to Integer to match departamentos table
    
    # Department details
    es_grupo_soporte = Column(Boolean, default=False)  # Is this department a support group?
    horario_atencion = Column(JSONB)  # { "lunes": { "inicio": "09:00", "fin": "18:00" }, ... }
    tiempo_respuesta_promedio = Column(Float)  # Average response time in hours
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    departamento = relationship("Departamento")
    agentes = relationship("Empleado", secondary="hd_agente_departamento")
    tickets_asignados = relationship("TicketSoporte")


class AgenteDepartamento(Base):
    """Link between support agents and departments - Vínculo entre agentes y departamentos"""
    __tablename__ = "hd_agente_departamento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    departamento_soporte_id = Column(UUID(as_uuid=True), ForeignKey("hd_departamento_soporte.id"), nullable=False)
    
    # Agent details
    nivel_experiencia = Column(Integer, default=1)  # 1-5 level of expertise
    especialidades = Column(JSONB)  # Categories this agent specializes in
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
