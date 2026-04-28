from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Date, Numeric, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class TipoMantenimiento(str, enum.Enum):
    preventivo = "preventivo"
    correctivo = "correctivo"
    predictivo = "predictivo"


class EstadoMantenimiento(str, enum.Enum):
    programado = "programado"
    en_progreso = "en_progreso"
    completado = "completado"
    cancelado = "cancelado"


class Equipo(Base):
    """Tabla de equipos/activos que requieren mantenimiento"""
    __tablename__ = "mantenimiento_equipos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    numero_serie = Column(String(100), unique=True)
    fecha_adquisicion = Column(Date)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("proveedores.id"))
    ubicacion = Column(String(200))
    estado = Column(String(50), default="activo")
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    activo = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    responsable = relationship("Empleado")
    proveedor = relationship("Proveedor")


class OrdenMantenimiento(Base):
    """Tabla de órdenes de mantenimiento"""
    __tablename__ = "mantenimiento_ordenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(50), unique=True, nullable=False)
    equipo_id = Column(UUID(as_uuid=True), ForeignKey("mantenimiento_equipos.id"), nullable=False)
    tipo = Column(SQLEnum(TipoMantenimiento), nullable=False)
    descripcion = Column(Text)
    fecha_solicitud = Column(Date, nullable=False)
    fecha_programada = Column(Date)
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True))
    estado = Column(SQLEnum(EstadoMantenimiento), default=EstadoMantenimiento.programado)
    prioridad = Column(SQLEnum('baja', 'media', 'alta', 'urgente', name='prioridad_mantenimiento'))
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))
    costo_estimado = Column(Numeric(10, 2))
    costo_real = Column(Numeric(10, 2))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    equipo = relationship("Equipo")
    responsable = relationship("Empleado")


class HistorialMantenimiento(Base):
    """Historial de mantenimientos realizados"""
    __tablename__ = "mantenimiento_historial"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    orden_id = Column(UUID(as_uuid=True), ForeignKey("mantenimiento_ordenes.id"), nullable=False)
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True), nullable=False)
    descripcion_trabajo = Column(Text)
    repuestos_utilizados = Column(Text)
    horas_trabajadas = Column(Integer)
    costo_total = Column(Numeric(10, 2))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    orden = relationship("OrdenMantenimiento")


class PlanMantenimiento(Base):
    """Planificación preventiva de mantenimiento"""
    __tablename__ = "mantenimiento_planes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    equipo_id = Column(UUID(as_uuid=True), ForeignKey("mantenimiento_equipos.id"), nullable=False)
    descripcion = Column(Text)
    frecuencia = Column(Integer, nullable=False)  # en días
    ultimo_mantenimiento = Column(Date)
    proximo_mantenimiento = Column(Date, nullable=False)
    activo = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    equipo = relationship("Equipo")