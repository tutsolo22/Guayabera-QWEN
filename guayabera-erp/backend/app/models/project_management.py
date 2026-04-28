"""
Project Management Models: Project coordination, resource assignment, scheduling and milestones
Specialized for textile product development projects
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

class EstadoProyecto(enum.Enum):
    PLANIFICACION = "planificacion"
    INICIADO = "iniciado"
    EJECUCION = "ejecucion"
    SUSPENDIDO = "suspendido"
    CANCELADO = "cancelado"
    COMPLETADO = "completado"


class PrioridadTarea(enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"


class EstadoTarea(enum.Enum):
    PENDIENTE = "pendiente"
    ASIGNADA = "asignada"
    EN_PROGRESO = "en_progreso"
    BLOQUEADA = "bloqueada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class TipoRecurso(enum.Enum):
    HUMANO = "humano"
    MATERIAL = "material"
    EQUIPO = "equipo"
    SERVICIO = "servicio"


class EstadoRecurso(enum.Enum):
    DISPONIBLE = "disponible"
    ASIGNADO = "asignado"
    MANTENIMIENTO = "mantenimiento"
    NO_DISPONIBLE = "no_disponible"


class TipoHitos(enum.Enum):
    ENTREGABLE = "entregable"
    DECISION = "decision"
    REVISON = "revision"
    APROBACION = "aprobacion"


# ============================================================================
# PROJECT MANAGEMENT MODELS
# ============================================================================

class Proyecto(Base):
    """Project management - Gestión de proyectos"""
    __tablename__ = "pm_proyecto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Project identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # Unique project code
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Project details
    tipo_proyecto = Column(String(50))  # Desarrollo de producto, mejora de proceso, etc.
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("crm_cliente.id"))  # Associated client
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)  # Project manager
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin_prevista = Column(Date, nullable=False)
    fecha_fin_real = Column(Date)
    
    # Budget and costs
    presupuesto_total = Column(Numeric(12, 2), default=0.00)
    costo_acumulado = Column(Numeric(12, 2), default=0.00)
    
    # Progress and status
    estado = Column(SQLEnum(EstadoProyecto), default=EstadoProyecto.PLANIFICACION)
    porcentaje_completado = Column(Integer, default=0)  # Percentage completed (0-100)
    
    # Metadata
    comentarios = Column(Text)
    datos_adicionales = Column(JSONB)  # Additional project-specific data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    cliente = relationship("Cliente")
    responsable = relationship("Empleado", back_populates="proyectos_responsable")
    tareas = relationship("Tarea", back_populates="proyecto")
    recursos = relationship("RecursoProyecto", back_populates="proyecto")
    hitos = relationship("HitoProyecto", back_populates="proyecto")


class Tarea(Base):
    """Task management - Gestión de tareas"""
    __tablename__ = "pm_tarea"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey("pm_proyecto.id"), nullable=False)
    
    # Task identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # Unique task code
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Assignment and priority
    asignado_a_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Assigned to employee
    prioridad = Column(SQLEnum(PrioridadTarea), default=PrioridadTarea.MEDIA)
    estado = Column(SQLEnum(EstadoTarea), default=EstadoTarea.PENDIENTE)
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin_prevista = Column(Date, nullable=False)
    fecha_fin_real = Column(Date)
    
    # Progress
    porcentaje_completado = Column(Integer, default=0)  # Percentage completed (0-100)
    duracion_estimada_horas = Column(Integer)  # Estimated duration in hours
    duracion_real_horas = Column(Integer, default=0)  # Real duration in hours
    
    # Dependencies
    tarea_padre_id = Column(UUID(as_uuid=True), ForeignKey("pm_tarea.id"))  # Parent task if applicable
    depende_de_id = Column(UUID(as_uuid=True), ForeignKey("pm_tarea.id"))  # Task dependency
    
    # Cost
    costo_estimado = Column(Numeric(10, 2), default=0.00)
    costo_real = Column(Numeric(10, 2), default=0.00)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    proyecto = relationship("Proyecto", back_populates="tareas")
    asignado_a = relationship("Empleado", foreign_keys=[asignado_a_id], back_populates="tareas_asignadas")
    tarea_padre = relationship("Tarea", remote_side=[id], back_populates="subtareas")
    subtareas = relationship("Tarea", back_populates="tarea_padre")
    depende_de = relationship("Tarea", remote_side=[id], foreign_keys=[depende_de_id])
    recursos = relationship("RecursoTarea", back_populates="tarea")


class RecursoProyecto(Base):
    """Project resource management - Gestión de recursos del proyecto"""
    __tablename__ = "pm_recurso_proyecto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey("pm_proyecto.id"), nullable=False)
    recurso_id = Column(UUID(as_uuid=True), ForeignKey("pm_recurso.id"), nullable=False)
    
    # Resource assignment details
    tipo_recurso = Column(SQLEnum(TipoRecurso), nullable=False)
    cantidad = Column(Integer, default=1)
    costo_unitario = Column(Numeric(10, 2), default=0.00)
    costo_total = Column(Numeric(12, 2), default=0.00)
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    proyecto = relationship("Proyecto", back_populates="recursos")
    recurso = relationship("Recurso", back_populates="proyectos")


class Recurso(Base):
    """Resource definition - Definición de recursos"""
    __tablename__ = "pm_recurso"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Resource identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # Unique resource code
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Resource details
    tipo = Column(SQLEnum(TipoRecurso), nullable=False)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"))  # If external service
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # If human resource
    costo_por_unidad = Column(Numeric(10, 2), default=0.00)
    
    # Availability
    estado = Column(SQLEnum(EstadoRecurso), default=EstadoRecurso.DISPONIBLE)
    capacidad_total = Column(Integer, default=1)  # For human resources, available hours/day
    capacidad_utilizada = Column(Integer, default=0)  # Hours/day currently allocated
    
    # Metadata
    comentarios = Column(Text)
    datos_especificos = Column(JSONB)  # Resource-specific data (specifications, etc.)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    proveedor = relationship("Proveedor")
    empleado = relationship("Empleado", back_populates="recursos_asociados")
    proyectos = relationship("RecursoProyecto", back_populates="recurso")
    tareas = relationship("RecursoTarea", back_populates="recurso")


class RecursoTarea(Base):
    """Task resource assignment - Asignación de recursos a tareas"""
    __tablename__ = "pm_recurso_tarea"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tarea_id = Column(UUID(as_uuid=True), ForeignKey("pm_tarea.id"), nullable=False)
    recurso_id = Column(UUID(as_uuid=True), ForeignKey("pm_recurso.id"), nullable=False)
    
    # Assignment details
    cantidad = Column(Integer, default=1)
    costo_unitario = Column(Numeric(10, 2), default=0.00)
    costo_total = Column(Numeric(12, 2), default=0.00)
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tarea = relationship("Tarea", back_populates="recursos")
    recurso = relationship("Recurso", back_populates="tareas")


class HitoProyecto(Base):
    """Project milestone - Hitos del proyecto"""
    __tablename__ = "pm_hito_proyecto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey("pm_proyecto.id"), nullable=False)
    
    # Milestone identification
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    tipo_hito = Column(SQLEnum(TipoHitos), nullable=False)
    
    # Timeline
    fecha_programada = Column(Date, nullable=False)
    fecha_real = Column(Date)
    
    # Status
    completado = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    proyecto = relationship("Proyecto", back_populates="hitos")


class ActividadProyecto(Base):
    """Project activity tracking - Seguimiento de actividades del proyecto"""
    __tablename__ = "pm_actividad_proyecto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey("pm_proyecto.id"), nullable=False)
    empleado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"), nullable=False)
    tarea_id = Column(UUID(as_uuid=True), ForeignKey("pm_tarea.id"))  # Optional, linked to specific task
    
    # Activity details
    descripcion = Column(Text, nullable=False)
    tipo_actividad = Column(String(50))  # reunión, informe, desarrollo, etc.
    horas_invertidas = Column(Integer, default=0)
    
    # Timeline
    fecha_registro = Column(Date, nullable=False, server_default=func.now())
    fecha_actividad = Column(Date, nullable=False)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    proyecto = relationship("Proyecto")
    empleado = relationship("Empleado", back_populates="actividades_proyecto")
    tarea = relationship("Tarea")