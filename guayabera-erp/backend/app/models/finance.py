"""
Accounting models: Chart of accounts, policies, journal entries
Inspired by CONTPAQi and Mexican SAT standards
"""

from sqlalchemy import (Column, String, Boolean, DateTime, ForeignKey, Text, 
                        Float, Integer, Date, Numeric, CheckConstraint)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class CuentaContable(Base):
    """Chart of accounts - Catálogo de cuentas"""
    __tablename__ = "cont_cuenta"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Account code structure (SAT Mexico standard)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    nivel = Column(Integer, nullable=False)  # 1=grupo, 2=genero, 3=cuenta, 4=subcuenta
    tipo = Column(String(50), nullable=False)  # activo, pasivo, capital, ingresos, costos, gastos
    naturaleza = Column(String(20))  # deudora, acreedora
    es_cuenta_mayor = Column(Boolean, default=False)
    es_agrupadora = Column(Boolean, default=False)
    
    # SAT mapping
    numero_cuenta_bancaria = Column(String(20))
    banco_sat = Column(String(100))  # Para cuentas bancarias
    
    # Status
    activa = Column(Boolean, default=True)
    requiere_centro_costos = Column(Boolean, default=False)
    requiere_documento_referencia = Column(Boolean, default=False)
    
    # Metadata
    descripcion = Column(Text)
    cuenta_padre_id = Column(UUID(as_uuid=True), ForeignKey("cont_cuenta.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cuenta_padre = relationship("CuentaContable", remote_side=[id], backref="cuentas_hijas")
    movimientos = relationship("MovimientoPoliza", back_populates="cuenta")


class CentroCosto(Base):
    """Cost centers for accounting distribution"""
    __tablename__ = "cont_centro_costo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PolizaContable(Base):
    """Accounting journal entries (pólizas)"""
    __tablename__ = "cont_poliza"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Policy identification
    numero = Column(Integer, nullable=False, index=True)
    tipo = Column(String(20), nullable=False)  # diario, ingreso, egreso
    fecha = Column(Date, nullable=False, index=True)
    
    # Header info
    descripcion = Column(Text, nullable=False)
    comentario_adicional = Column(Text)
    
    # Status and tracking
    estado = Column(String(20), default="borrador")  # borrador, revisada, aprobada, cancelada
    fecha_aprobacion = Column(DateTime(timezone=True))
    aprobado_por = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    # Totals (calculated)
    total_cargos = Column(Numeric(15, 2), default=0)
    total_abonos = Column(Numeric(15, 2), default=0)
    esta_cuadrada = Column(Boolean, default=False)
    
    # Reference to source module
    modulo_origen = Column(String(50))  # manual, ventas, compras, nomina, produccion
    referencia_externa = Column(String(100))  # ID del documento origen
    
    # Metadata
    preparado_por = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    revisado_por = Column(UUID(as_uuid=True), ForeignKey("seg_usuario.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    movimientos = relationship("MovimientoPoliza", back_populates="poliza", 
                              cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('total_cargos = total_abonos', name='poliza_cuadrada'),
    )


class MovimientoPoliza(Base):
    """Individual journal entry lines (partidas)"""
    __tablename__ = "cont_poliza_detalle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Links
    poliza_id = Column(UUID(as_uuid=True), ForeignKey("cont_poliza.id"), nullable=False)
    cuenta_id = Column(UUID(as_uuid=True), ForeignKey("cont_cuenta.id"), nullable=False)
    centro_costo_id = Column(UUID(as_uuid=True), ForeignKey("cont_centro_costo.id"))
    
    # Amounts
    cargo = Column(Numeric(15, 2), default=0)
    abono = Column(Numeric(15, 2), default=0)
    
    # Description
    concepto = Column(String(500), nullable=False)
    referencia = Column(String(100))  # Número de factura, OC, OP, etc.
    
    # Additional info
    documento_referencia = Column(String(100))  # UUID del documento origen
    fecha_documento = Column(Date)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    poliza = relationship("PolizaContable", back_populates="movimientos")
    cuenta = relationship("CuentaContable", back_populates="movimientos")
    centro_costo = relationship("CentroCosto")


class Banco(Base):
    """Bank accounts management"""
    __tablename__ = "cont_banco"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)  # BBVA, Banorte, etc.
    cuenta = Column(String(20), unique=True, nullable=False)
    clabe = Column(String(18), unique=True)
    tipo_cuenta = Column(String(50))  # cheques, ahorro, inversion
    moneda = Column(String(3), default="MXN")
    sucursal = Column(String(100))
    
    # Accounting link
    cuenta_contable_id = Column(UUID(as_uuid=True), ForeignKey("cont_cuenta.id"))
    
    # Balances
    saldo_actual = Column(Numeric(15, 2), default=0)
    saldo_fecha_corte = Column(Numeric(15, 2), default=0)
    fecha_ultimo_corte = Column(Date)
    
    # Status
    activo = Column(Boolean, default=True)
    
    # Metadata
    descripcion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cuenta_contable = relationship("CuentaContable")
    movimientos_bancarios = relationship("MovimientoBancario", back_populates="banco")


class MovimientoBancario(Base):
    """Bank statement lines for reconciliation"""
    __tablename__ = "cont_movimiento_bancario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    banco_id = Column(UUID(as_uuid=True), ForeignKey("cont_banco.id"), nullable=False)
    
    # Transaction info
    fecha = Column(Date, nullable=False, index=True)
    descripcion = Column(String(500), nullable=False)
    referencia = Column(String(50))  # Reference number
    tipo_movimiento = Column(String(50))  # deposito, retiro, transferencia, comision
    
    # Amounts
    cargo = Column(Numeric(15, 2), default=0)
    abono = Column(Numeric(15, 2), default=0)
    saldo = Column(Numeric(15, 2))
    
    # Reconciliation
    conciliado = Column(Boolean, default=False)
    fecha_conciliacion = Column(DateTime(timezone=True))
    poliza_id = Column(UUID(as_uuid=True), ForeignKey("cont_poliza.id"))
    
    # Metadata
    importado = Column(Boolean, default=False)  # Imported from bank file
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    banco = relationship("Banco", back_populates="movimientos_bancarios")
    poliza = relationship("PolizaContable")


class AsientoContable(Base):
    """Automatic accounting entries from other modules"""
    __tablename__ = "cont_asiento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Source tracking
    modulo_origen = Column(String(50), nullable=False)  # compras, ventas, nomina, produccion
    entidad_origen = Column(String(100), nullable=False)  # tipo de documento
    entidad_id = Column(UUID(as_uuid=True), nullable=False)
    referencia = Column(String(200))
    
    # Accounting link
    poliza_id = Column(UUID(as_uuid=True), ForeignKey("cont_poliza.id"))
    
    # Status
    estado = Column(String(20), default="pendiente")  # pendiente, procesado, cancelado
    fecha_procesado = Column(DateTime(timezone=True))
    
    # Data
    datos_origen = Column(JSONB)  # Snapshot of source document
    errores = Column(JSONB)  # Error details if failed
    
    # Metadata
    creado_por = Column(String(100))  # System or user
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    poliza = relationship("PolizaContable")


class PeriodoContable(Base):
    """Accounting periods for closing control"""
    __tablename__ = "cont_periodo"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(50), nullable=False)  # Enero 2025
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    
    # Status
    estado = Column(String(20), default="abierto")  # abierto, cerrado, en_cierre
    fecha_cierre = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
