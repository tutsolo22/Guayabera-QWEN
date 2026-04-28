"""
Advanced Accounting Models: Comprehensive accounting system with journal entries, financial statements, and reporting
Specialized for Mexican accounting compliance (SAT/NIF)
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

class TipoPoliza(enum.Enum):
    DIARIO = "diario"
    MAYOR = "mayor"
    BALANZA = "balanza"
    RESULTADOS = "resultados"
    CAPITAL_CONTABLE = "capital_contable"
    AUXILIAR = "auxiliar"


class TipoMovimiento(enum.Enum):
    DEBE = "debe"
    HABER = "haber"


class EstadoPoliza(enum.Enum):
    BORRADOR = "borrador"
    CONTABILIZADO = "contabilizado"
    CERRADO = "cerrado"
    CANCELADO = "cancelado"


class PeriodoContable(enum.Enum):
    MENSUAL = "mensual"
    TRIMESTRAL = "trimestral"
    SEMESTRAL = "semestral"
    ANUAL = "anual"


# ============================================================================
# ADVANCED ACCOUNTING MODELS
# ============================================================================

class PeriodoFiscal(Base):
    """Fiscal period management - Gestión de periodos fiscales"""
    __tablename__ = "acc_periodo_fiscal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Period identification
    nombre = Column(String(100), nullable=False)  # Ej: "Enero 2023", "Primer trimestre 2023"
    codigo = Column(String(30), unique=True, nullable=False, index=True)  # FY2023-M01, FY2023-Q1
    ano_fiscal = Column(Integer, nullable=False)
    
    # Period dates
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Status
    estado = Column(String(20), default="abierto")  # abierto, cerrado, bloqueado
    periodo_tipo = Column(SQLEnum(PeriodoContable), default=PeriodoContable.MENSUAL)
    
    # Compliance
    cerrado_sat = Column(Boolean, default=False)  # Closed in SAT system
    cierre_contable_realizado = Column(Boolean, default=False)
    
    # Metadata
    comentarios = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    polizas = relationship("PolizaContable", back_populates="periodo_fiscal")


class PolizaContable(Base):
    """Accounting voucher - Póliza contable"""
    __tablename__ = "acc_poliza_contable"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Voucher identification
    folio = Column(String(30), unique=True, nullable=False, index=True)  # Unique voucher number
    descripcion = Column(Text)
    tipo_poliza = Column(SQLEnum(TipoPoliza), nullable=False)
    
    # Dates and periods
    fecha_emision = Column(Date, nullable=False)
    periodo_fiscal_id = Column(UUID(as_uuid=True), ForeignKey("acc_periodo_fiscal.id"), nullable=False)
    
    # Status
    estado = Column(SQLEnum(EstadoPoliza), default=EstadoPoliza.BORRADOR)
    
    # Amounts
    total_debe = Column(Numeric(15, 2), default=0.00)
    total_haber = Column(Numeric(15, 2), default=0.00)
    conciliada = Column(Boolean, default=False)
    
    # Compliance
    uuid_cfdi = Column(String(36))  # UUID for CFDI linkage
    folio_fiscal = Column(String(50))  # Fiscal folio for SAT
    fecha_timbrado = Column(DateTime(timezone=True))  # CFDI stamp date
    
    # Metadata
    referencia_documento = Column(String(100))  # Reference to related document
    usuario_elaboro_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # User who created
    usuario_autorizo_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))  # User who authorized
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    periodo_fiscal = relationship("PeriodoFiscal", back_populates="polizas")
    movimientos = relationship("MovimientoContable", back_populates="poliza")
    usuario_elaboro = relationship("Usuario", foreign_keys=[usuario_elaboro_id])
    usuario_autorizo = relationship("Usuario", foreign_keys=[usuario_autorizo_id])


class MovimientoContable(Base):
    """Accounting entry/movement - Movimiento contable"""
    __tablename__ = "acc_movimiento_contable"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poliza_id = Column(UUID(as_uuid=True), ForeignKey("acc_poliza_contable.id"), nullable=False)
    cuenta_id = Column(UUID(as_uuid=True), ForeignKey("fin_cuenta_contable.id"), nullable=False)
    
    # Movement details
    tipo_movimiento = Column(SQLEnum(TipoMovimiento), nullable=False)  # Debe/Haber
    importe = Column(Numeric(15, 2), nullable=False)
    descripcion = Column(Text)
    
    # Compliance
    uuid_cfdi = Column(String(36))  # Related CFDI UUID
    referencia = Column(String(100))  # Reference for the movement
    
    # Status
    conciliado = Column(Boolean, default=False)
    fecha_conciliacion = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    poliza = relationship("PolizaContable", back_populates="movimientos")
    cuenta = relationship("CuentaContable")


class EstadoFinanciero(Base):
    """Financial statement - Estado financiero"""
    __tablename__ = "acc_estado_financiero"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Statement identification
    nombre = Column(String(100), nullable=False)  # Balance general, Estado de resultados, etc.
    tipo_estado = Column(String(50), nullable=False)  # balance_general, estado_resultados, etc.
    periodo_fiscal_id = Column(UUID(as_uuid=True), ForeignKey("acc_periodo_fiscal.id"), nullable=False)
    
    # Content and structure
    contenido = Column(JSONB)  # Complete statement in JSON format
    formato = Column(String(20), default="vertical")  # vertical, horizontal
    
    # Status
    generado_por_id = Column(UUID(as_uuid=True), ForeignKey("auth_usuario.id"))
    fecha_generacion = Column(DateTime(timezone=True), server_default=func.now())
    verificado = Column(Boolean, default=False)
    fecha_verificacion = Column(DateTime(timezone=True))
    
    # Compliance
    sellado_digital = Column(String(255))  # Digital seal for SAT compliance
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    periodo_fiscal = relationship("PeriodoFiscal")
    generado_por = relationship("Usuario")


class CentroCosto(Base):
    """Cost center - Centro de costo"""
    __tablename__ = "acc_centro_costo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Cost center identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Classification
    tipo = Column(String(50))  # operativo, administrativo, venta, etc.
    activo = Column(Boolean, default=True)
    
    # Hierarchy
    padre_id = Column(UUID(as_uuid=True), ForeignKey("acc_centro_costo.id"))  # Parent cost center
    
    # Metadata
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("rh_empleado.id"))  # Responsible employee
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    padre = relationship("CentroCosto", remote_side=[id])
    responsable = relationship("Empleado")
    movimientos = relationship("MovimientoContable")


class PartidaPresupuestal(Base):
    """Budgetary entry - Partida presupuestal"""
    __tablename__ = "acc_partida_presupuestal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Budget entry identification
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    # Budget amounts
    presupuesto_original = Column(Numeric(15, 2), default=0.00)
    comprometido = Column(Numeric(15, 2), default=0.00)  # Amount committed
    ejercido = Column(Numeric(15, 2), default=0.00)      # Amount exercised
    pagado = Column(Numeric(15, 2), default=0.00)        # Amount paid
    
    # Period and classification
    periodo_fiscal_id = Column(UUID(as_uuid=True), ForeignKey("acc_periodo_fiscal.id"), nullable=False)
    centro_costo_id = Column(UUID(as_uuid=True), ForeignKey("acc_centro_costo.id"), nullable=False)
    cuenta_contable_id = Column(UUID(as_uuid=True), ForeignKey("fin_cuenta_contable.id"), nullable=False)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
    
    # Relationships
    periodo_fiscal = relationship("PeriodoFiscal")
    centro_costo = relationship("CentroCosto")
    cuenta_contable = relationship("CuentaContable")