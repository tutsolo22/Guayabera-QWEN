"""
Asset Management Models: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
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

class TipoActivo(enum.Enum):
    EQUIPO_COMPUTO = "equipo_computo"
    MAQUINARIA = "maquinaria"
    MOBILIARIO = "mobiliario"
    VEHICULO = "vehiculo"
    HERRAMIENTA = "herramienta"
    EDIFICIO = "edificio"
    TERRENO = "terreno"


class EstadoActivo(enum.Enum):
    ACTIVO = "activo"
    MANTENIMIENTO = "mantenimiento"
    BAJA = "baja"
    OBSOLETO = "obsoleto"
    ALMACEN = "almacen"


class TipoMantenimiento(enum.Enum):
    PREVENTIVO = "preventivo"
    CORRECTIVO = "correctivo"
    CALIBRACION = "calibracion"
    INSPECCION = "inspeccion"


class EstadoMantenimiento(enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class MetodoDepreciacion(enum.Enum):
    LINEA_RECTA = "linea_recta"
    SUMA_DIGITOS = "suma_digitos"
    DOBLE_SALDO = "doble_saldo"
    UNIDADES_PRODUCCION = "unidades_produccion"


# ============================================================================
# ASSET MANAGEMENT MODELS
# ============================================================================

class CategoriaActivo(Base):
    """Asset category management - Gestión de categorías de activos"""
    __tablename__ = "am_categoria_activo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Category identification
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # CAT-EQUIPO, CAT-MAQUINA, etc.
    
    # Depreciation defaults
    vida_util_anios = Column(Integer)  # Default useful life in years
    metodo_depreciacion = Column(SQLEnum(MetodoDepreciacion))  # Default depreciation method
    porcentaje_residual = Column(Float, default=0.0)  # Default residual percentage
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    activos = relationship("Activo", back_populates="categoria")


class Activo(Base):
    """Fixed asset management - Gestión de activos fijos"""
    __tablename__ = "am_activo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Asset identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # Unique asset code
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)
    tipo = Column(SQLEnum(TipoActivo), nullable=False)
    
    # Asset details
    marca = Column(String(100))
    modelo = Column(String(100))
    serie = Column(String(100))
    color = Column(String(50))
    caracteristicas = Column(Text)  # Technical specifications
    
    # Location and assignment
    ubicacion_actual = Column(String(150))  # Current location
    departamento_asignado_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # Department assigned
    empleado_asignado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Employee assigned
    
    # Acquisition and financial info
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("am_categoria_activo.id"), nullable=False)
    fecha_adquisicion = Column(Date, nullable=False)
    valor_adquisicion = Column(Numeric(12, 2), nullable=False)  # Purchase value
    valor_actual = Column(Numeric(12, 2))  # Current book value after depreciation
    vida_util_anios = Column(Integer, nullable=False)  # Useful life in years
    metodo_depreciacion = Column(SQLEnum(MetodoDepreciacion), nullable=False)  # Depreciation method
    porcentaje_residual = Column(Float, default=0.0)  # Residual percentage
    
    # Status
    estado = Column(SQLEnum(EstadoActivo), default=EstadoActivo.ACTIVO)
    fecha_baja = Column(Date)  # Date of asset disposal
    motivo_baja = Column(String(200))  # Reason for disposal
    
    # Maintenance tracking
    fecha_ultimo_mantenimiento = Column(Date)
    proximo_mantenimiento = Column(Date)  # Next scheduled maintenance
    
    # Metadata
    comentarios = Column(Text)
    imagen_url = Column(String(255))  # URL of asset image
    datos_adicionales = Column(JSONB)  # Additional asset-specific data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    categoria = relationship("CategoriaActivo", back_populates="activos")
    departamento_asignado = relationship("Departamento")
    empleado_asignado = relationship("Empleado")
    mantenimientos = relationship("MantenimientoActivo", back_populates="activo")
    depreciaciones = relationship("DepreciacionActivo", back_populates="activo")


class MantenimientoActivo(Base):
    """Asset maintenance tracking - Seguimiento de mantenimientos de activos"""
    __tablename__ = "am_mantenimiento_activo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("am_activo.id"), nullable=False)
    tecnico_asignado_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Assigned technician
    
    # Maintenance details
    tipo_mantenimiento = Column(SQLEnum(TipoMantenimiento), nullable=False)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text)
    
    # Schedule and completion
    fecha_solicitud = Column(Date, nullable=False, server_default=func.current_date())
    fecha_programada = Column(Date, nullable=False)
    fecha_inicio = Column(DateTime(timezone=True))  # When maintenance started
    fecha_fin = Column(DateTime(timezone=True))  # When maintenance finished
    fecha_realizacion = Column(Date)  # Actual realization date
    
    # Status and costs
    estado = Column(SQLEnum(EstadoMantenimiento), default=EstadoMantenimiento.PENDIENTE)
    costo = Column(Numeric(10, 2), default=0.00)  # Maintenance cost
    proveedor_servicio_id = Column(UUID(as_uuid=True), ForeignKey("com_proveedor.id"))  # Service provider if external
    
    # Results
    observaciones = Column(Text)
    repuestos_utilizados = Column(Text)  # Parts replaced
    proximo_mantenimiento = Column(Date)  # Next maintenance schedule
    
    # Metadata
    creado_por_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # Created by user
    completado_por_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # Completed by user
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activo = relationship("Activo", back_populates="mantenimientos")
    tecnico_asignado = relationship("Empleado", foreign_keys=[tecnico_asignado_id])
    proveedor_servicio = relationship("Proveedor")
    creado_por = relationship("Usuario", foreign_keys=[creado_por_id])
    completado_por = relationship("Usuario", foreign_keys=[completado_por_id])


class DepreciacionActivo(Base):
    """Asset depreciation tracking - Seguimiento de depreciación de activos"""
    __tablename__ = "am_depreciacion_activo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("am_activo.id"), nullable=False)
    
    # Depreciation details
    anio = Column(Integer, nullable=False)  # Year of depreciation
    mes = Column(Integer, nullable=False)  # Month of depreciation (1-12)
    metodo = Column(SQLEnum(MetodoDepreciacion), nullable=False)  # Method used
    
    # Values
    valor_entrada = Column(Numeric(12, 2), nullable=False)  # Starting value for this period
    depreciacion_periodo = Column(Numeric(12, 2), nullable=False)  # Depreciation for this period
    depreciacion_acumulada = Column(Numeric(12, 2), nullable=False)  # Accumulated depreciation
    valor_libros = Column(Numeric(12, 2), nullable=False)  # Book value after depreciation
    
    # Status
    procesado = Column(Boolean, default=False)  # Processed in accounting
    fecha_procesamiento = Column(DateTime(timezone=True))  # When processed
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activo = relationship("Activo", back_populates="depreciaciones")


class HistorialAsignacion(Base):
    """Asset assignment history - Historial de asignaciones de activos"""
    __tablename__ = "am_historial_asignacion"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("am_activo.id"), nullable=False)
    
    # Assignment details
    empleado_anterior_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Previous assignee
    empleado_nuevo_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # New assignee
    departamento_anterior_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # Previous department
    departamento_nuevo_id = Column(UUID(as_uuid=True), ForeignKey("rh_departamento.id"))  # New department
    
    # Location
    ubicacion_anterior = Column(String(150))  # Previous location
    ubicacion_nueva = Column(String(150))  # New location
    
    # Timeline
    fecha_inicio = Column(Date, nullable=False)  # Start date of assignment
    fecha_fin = Column(Date)  # End date of assignment (null if current)
    
    # Metadata
    motivo_cambio = Column(String(200))  # Reason for change
    realizado_por_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # Performed by user
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    activo = relationship("Activo")
    empleado_anterior = relationship("Empleado", foreign_keys=[empleado_anterior_id])
    empleado_nuevo = relationship("Empleado", foreign_keys=[empleado_nuevo_id])
    departamento_anterior = relationship("Departamento", foreign_keys=[departamento_anterior_id])
    departamento_nuevo = relationship("Departamento", foreign_keys=[departamento_nuevo_id])
    realizado_por = relationship("Usuario")