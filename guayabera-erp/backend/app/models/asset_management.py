"""
Asset Management Models: Fixed asset control, equipment maintenance, depreciation tracking
Specialized for textile manufacturing assets
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint, Enum as SQLEnum, Table)
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
    """Asset model for tracking company assets"""
    __tablename__ = "activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("am_categoria_activo.id"), nullable=False)  # Changed from categorias_activo to am_categoria_activo
    marca = Column(String(100))
    modelo = Column(String(100))
    numero_serie = Column(String(100), unique=True)
    valor_adquisicion = Column(Numeric(10, 2))
    fecha_adquisicion = Column(Date)
    vida_util_anios = Column(Integer)  # Expected useful life in years
    estado = Column(SQLEnum(EstadoActivo), default=EstadoActivo.ACTIVO)
    ubicacion_id = Column(UUID(as_uuid=True), ForeignKey("log_ubicacion_almacen.id"))  # Changed to correct warehouse location table
    imagen_url = Column(String(255))  # URL to asset photo
    garantia_fecha_fin = Column(Date)  # End of warranty date
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from usuarios to seg_usuario
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("proveedores_activos.id"))
    
    # Status
    activo = Column(Boolean, default=True)  # Whether asset is still in use
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    categoria = relationship("CategoriaActivo", back_populates="activos")
    ubicacion = relationship("UbicacionAlmacen", back_populates="activos")  # Changed to correct warehouse location class
    responsable = relationship("Usuario")  # Changed from Usuario to match correct model
    proveedor = relationship("ProveedorActivo", back_populates="activos")
    historial_mantenimiento = relationship("HistorialMantenimientoActivo", back_populates="activo")
    asignaciones = relationship("AsignacionActivo", back_populates="activo")


class HistorialMantenimientoActivo(Base):
    """Maintenance history for assets"""
    __tablename__ = "historial_mantenimiento_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("activos.id"), nullable=False)
    
    # Maintenance info
    tipo_mantenimiento = Column(SQLEnum(TipoMantenimiento), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_mantenimiento = Column(Date, nullable=False)
    costo = Column(Numeric(10, 2))
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("proveedores_activos.id"))
    tecnico_nombre = Column(String(100))  # Name of technician who performed maintenance
    duracion_horas = Column(Integer)  # Duration of maintenance in hours
    proximo_mantenimiento = Column(Date)  # Next scheduled maintenance date
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activo = relationship("Activo", back_populates="historial_mantenimiento")
    proveedor = relationship("ProveedorActivo")


class AsignacionActivo(Base):
    """Asset assignment model"""
    __tablename__ = "asignaciones_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("activos.id"), nullable=False)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"), nullable=False)  # Changed from usuarios to seg_usuario - Assigned user
    
    # Assignment info
    fecha_asignacion = Column(Date, nullable=False)
    fecha_devolucion = Column(Date)  # Return date, null if still assigned
    motivo_asignacion = Column(Text)
    estado_salida = Column(SQLEnum(EstadoActivo), nullable=False)  # Condition when assigned
    estado_retorno = Column(SQLEnum(EstadoActivo))  # Condition when returned, null if still assigned
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    activo = relationship("Activo", back_populates="asignaciones")
    usuario = relationship("Usuario")  # Changed from Usuario to match correct model


class ProveedorActivo(Base):
    """Asset provider model"""
    __tablename__ = "proveedores_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(200), nullable=False)
    contacto_nombre = Column(String(100))
    contacto_email = Column(String(100))
    contacto_telefono = Column(String(20))
    direccion = Column(String(255))
    sitio_web = Column(String(255))
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    activos = relationship("Activo", back_populates="proveedor")
    contratos = relationship("ContratoMantenimiento", back_populates="proveedor")


class ContratoMantenimiento(Base):
    """Maintenance contract model"""
    __tablename__ = "contratos_mantenimiento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("proveedores_activos.id"), nullable=False)
    numero_contrato = Column(String(100), unique=True, nullable=False)
    
    # Contract info
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    costo_anual = Column(Numeric(10, 2))
    cobertura = Column(Text)  # What is covered by the contract
    condiciones_especiales = Column(Text)
    archivo_url = Column(String(255))  # URL to contract document
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    proveedor = relationship("ProveedorActivo", back_populates="contratos")
    activos = relationship("Activo", secondary="activo_contrato_mantenimiento", back_populates="contratos")


# Association table for many-to-many relationship between assets and maintenance contracts
activo_contrato_mantenimiento = Table(
    "activo_contrato_mantenimiento",
    Base.metadata,
    Column("activo_id", UUID(as_uuid=True), ForeignKey("activos.id"), primary_key=True),
    Column("contrato_id", UUID(as_uuid=True), ForeignKey("contratos_mantenimiento.id"), primary_key=True)
)


class MantenimientoActivo(Base):
    """Asset maintenance model"""
    __tablename__ = "mantenimientos_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("activos.id"), nullable=False)
    tipo_mantenimiento = Column(SQLEnum(TipoMantenimiento), nullable=False)
    descripcion = Column(Text, nullable=False)
    fecha_programada = Column(Date, nullable=False)
    fecha_realizacion = Column(Date)
    costo_estimado = Column(Numeric(10, 2))
    costo_real = Column(Numeric(10, 2))
    estado = Column(SQLEnum(EstadoMantenimiento), default=EstadoMantenimiento.PENDIENTE)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from usuarios to seg_usuario - Technician responsible
    proveedor_id = Column(UUID(as_uuid=True), ForeignKey("proveedores_activos.id"))
    proximo_mantenimiento = Column(Date)  # Fecha del próximo mantenimiento programado
    observaciones = Column(Text)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

    # Relationships
    activo = relationship("Activo")
    responsable = relationship("Usuario")  # Changed from Usuario to match correct model
    proveedor = relationship("ProveedorActivo")


class DepreciacionActivo(Base):
    """Asset depreciation model"""
    __tablename__ = "depreciaciones_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("activos.id"), nullable=False)
    anio = Column(Integer, nullable=False)  # Year of depreciation
    mes = Column(Integer)  # Month of depreciation (nullable for annual calculations)
    metodo = Column(SQLEnum(MetodoDepreciacion), nullable=False)
    valor_adquisicion = Column(Numeric(10, 2), nullable=False)
    valor_residual = Column(Numeric(10, 2), default=0.0)
    vida_util_total = Column(Integer, nullable=False)  # Total useful life in months or years
    vida_util_restante = Column(Integer, nullable=False)  # Remaining useful life
    depreciacion_periodo = Column(Numeric(10, 2), nullable=False)  # Depreciation for this period
    depreciacion_acumulada = Column(Numeric(10, 2), nullable=False)  # Accumulated depreciation
    valor_libros = Column(Numeric(10, 2), nullable=False)  # Book value at the end of period
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activo = relationship("Activo")


class HistorialAsignacion(Base):
    """Asset assignment history model"""
    __tablename__ = "historial_asignaciones_activos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activo_id = Column(UUID(as_uuid=True), ForeignKey("activos.id"), nullable=False)
    empleado_anterior_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from usuarios to seg_usuario - Previous employee
    empleado_nuevo_id = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))  # Changed from usuarios to seg_usuario - New employee
    departamento_anterior_id = Column(Integer, ForeignKey("departamentos.id"))  # Changed from UUID to Integer to match departamentos
    departamento_nuevo_id = Column(Integer, ForeignKey("departamentos.id"))  # Changed from UUID to Integer to match departamentos
    ubicacion_anterior = Column(String(200))  # Previous location
    ubicacion_nueva = Column(String(200))  # New location
    fecha_inicio = Column(Date, nullable=False)  # Date when assignment started
    fecha_fin = Column(Date)  # Date when assignment ended
    motivo_transferencia = Column(Text)  # Reason for transfer
    estado_anterior = Column(SQLEnum(EstadoActivo))  # State when assigned
    estado_actual = Column(SQLEnum(EstadoActivo))  # State when returned/changed
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    activo = relationship("Activo")
    empleado_anterior = relationship("Usuario", foreign_keys=[empleado_anterior_id])  # Changed from Usuario to match correct model
    empleado_nuevo = relationship("Usuario", foreign_keys=[empleado_nuevo_id])  # Changed from Usuario to match correct model
    departamento_anterior = relationship("Departamento", foreign_keys=[departamento_anterior_id])
    departamento_nuevo = relationship("Departamento", foreign_keys=[departamento_nuevo_id])
