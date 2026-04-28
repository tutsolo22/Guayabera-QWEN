"""
Requisition Management Models: Purchase requisitions, approvals, and tracking
Specialized for ERP system procurement
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

class EstadoRequisicion(enum.Enum):
    BORRADOR = "borrador"
    PENDIENTE_AUTORIZACION = "pendiente_autorizacion"
    AUTORIZADO = "autorizado"
    RECHAZADO = "rechazado"
    ORDEN_GENERADA = "orden_generada"
    PARCIALMENTE_RECIBIDO = "parcialmente_recibido"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class TipoRequisicion(enum.Enum):
    BIENES = "bienes"
    SERVICIOS = "servicios"
    EQUIPO_COMPUTO = "equipo_computo"
    MATERIA_PRIMA = "materia_prima"
    INSUMOS = "insumos"


# ============================================================================
# REQUISITION MODELS
# ============================================================================

class Requisicion(Base):
    """Purchase requisition management - Gestión de requisiciones de compra"""
    __tablename__ = "req_requisicion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Requisition identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # Ej: REQ-2023-0001
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    
    # Classification
    tipo_requisicion = Column(SQLEnum(TipoRequisicion), nullable=False)
    
    # Requester and approvers
    solicitante_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Employee who requested
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Immediate supervisor
    aprobador_finanzas_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Finance approver
    
    # Approval tracking
    autorizado_supervisor = Column(Boolean, default=False)
    fecha_autorizacion_supervisor = Column(DateTime(timezone=True))
    motivo_rechazo_supervisor = Column(Text)
    
    autorizado_finanzas = Column(Boolean, default=False)
    fecha_autorizacion_finanzas = Column(DateTime(timezone=True))
    motivo_rechazo_finanzas = Column(Text)
    
    # Status
    estado = Column(SQLEnum(EstadoRequisicion), default=EstadoRequisicion.BORRADOR)
    
    # Dates
    fecha_solicitud = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_aprobacion_supervisor = Column(DateTime(timezone=True))
    fecha_aprobacion_finanzas = Column(DateTime(timezone=True))
    fecha_vencimiento = Column(DateTime(timezone=True))  # Deadline for purchase orders
    
    # Financial data
    subtotal = Column(Numeric(12, 2), default=0.00)
    impuestos = Column(Numeric(12, 2), default=0.00)
    total = Column(Numeric(12, 2), default=0.00)
    
    # Related documents
    ticket_soporte_id = Column(UUID(as_uuid=True), ForeignKey("hd_ticket_soporte.id"))  # Related support ticket
    orden_compra_id = Column(UUID(as_uuid=True), ForeignKey("com_orden_compra.id"))  # Generated purchase order
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    solicitante = relationship("Empleado", foreign_keys=[solicitante_id])
    supervisor = relationship("Empleado", foreign_keys=[supervisor_id])
    aprobador_finanzas = relationship("Empleado", foreign_keys=[aprobador_finanzas_id])
    ticket_soporte = relationship("TicketSoporte")
    orden_compra = relationship("OrdenCompra")
    detalles = relationship("DetalleRequisicion", back_populates="requisicion")
    proveedores_cotizacion = relationship("ProveedorCotizacion", back_populates="requisicion")


class DetalleRequisicion(Base):
    """Requisition item details - Detalles de artículos en la requisición"""
    __tablename__ = "req_detalle_requisicion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requisicion_id = Column(UUID(as_uuid=True), ForeignKey("req_requisicion.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("alm_producto.id"))  # Related product if applicable
    
    # Item details
    descripcion = Column(Text, nullable=False)  # Description of the item
    cantidad = Column(Integer, nullable=False, default=1)
    unidad_medida = Column(String(20), default="unidad")  # Measurement unit
    
    # Pricing
    precio_unitario_estimado = Column(Numeric(10, 2), default=0.00)
    precio_total_estimado = Column(Numeric(12, 2), default=0.00)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    requisicion = relationship("Requisicion", back_populates="detalles")
    producto = relationship("Producto")


class ProveedorCotizacion(Base):
    """Supplier quotations for requisitions - Cotizaciones de proveedores para requisiciones"""
    __tablename__ = "req_proveedor_cotizacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requisicion_id = Column(UUID(as_uuid=True), ForeignKey("req_requisicion.id"), nullable=False)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"), nullable=False)
    
    # Quotation details
    archivo_cotizacion = Column(String(500))  # Path to quotation file
    comentarios = Column(Text)
    fecha_envio = Column(DateTime(timezone=True), server_default=func.now())
    es_ganador = Column(Boolean, default=False)  # Is this the selected quotation
    
    # Financial data
    subtotal = Column(Numeric(12, 2), default=0.00)
    impuestos = Column(Numeric(12, 2), default=0.00)
    total = Column(Numeric(12, 2), default=0.00)
    
    # Status
    activa = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    requisicion = relationship("Requisicion", back_populates="proveedores_cotizacion")
    proveedor = relationship("Proveedor")


class FormatoRequisicion(Base):
    """Requisition form template - Plantilla de formato de requisición"""
    __tablename__ = "req_formato"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Form details
    nombre = Column(String(100), nullable=False)  # Name of the form
    descripcion = Column(Text)
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # REQ-FORM-001
    
    # Form structure
    campos_formulario = Column(JSONB)  # Fields in the form as JSON
    campos_obligatorios = Column(JSONB)  # Required fields
    firma_autorizacion = Column(Boolean, default=True)  # Requires authorization signature
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))