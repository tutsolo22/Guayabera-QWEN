"""
Advanced Accounting Schemas: Comprehensive accounting system with journal entries, financial statements, and reporting
Specialized for Mexican accounting compliance (SAT/NIF)
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class BaseSchema(BaseModel):
    id: Optional[UUID4] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# FISCAL PERIOD SCHEMAS
# ============================================================================

class PeriodoFiscalBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del periodo fiscal")
    codigo: str = Field(..., max_length=30, description="Código único del periodo fiscal")
    ano_fiscal: int = Field(..., ge=2000, le=2100, description="Año fiscal")
    fecha_inicio: date = Field(..., description="Fecha de inicio del periodo")
    fecha_fin: date = Field(..., description="Fecha de fin del periodo")
    estado: Optional[str] = Field(default="abierto", description="Estado del periodo (abierto/cerrado/bloqueado)")
    periodo_tipo: Optional[str] = Field(default="mensual", description="Tipo de periodo")
    cerrado_sat: Optional[bool] = Field(default=False, description="¿Está cerrado en el SAT?")
    cierre_contable_realizado: Optional[bool] = Field(default=False, description="¿Se realizó el cierre contable?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")


class PeriodoFiscalCreate(PeriodoFiscalBase):
    pass


class PeriodoFiscalUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, description="Estado del periodo")
    cerrado_sat: Optional[bool] = None
    cierre_contable_realizado: Optional[bool] = None
    comentarios: Optional[str] = None


class PeriodoFiscalResponse(PeriodoFiscalBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ACCOUNTING VOUCHER SCHEMAS
# ============================================================================

class PolizaContableBase(BaseModel):
    folio: str = Field(..., max_length=30, description="Folio único de la póliza")
    descripcion: Optional[str] = Field(None, description="Descripción de la póliza")
    tipo_poliza: str = Field(..., description="Tipo de póliza")
    fecha_emision: date = Field(..., description="Fecha de emisión")
    periodo_fiscal_id: UUID4 = Field(..., description="ID del periodo fiscal")
    estado: Optional[str] = Field(default="borrador", description="Estado de la póliza")
    total_debe: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total del debe")
    total_haber: Optional[Decimal] = Field(default=Decimal('0.00'), description="Total del haber")
    conciliada: Optional[bool] = Field(default=False, description="¿Está conciliada?")
    uuid_cfdi: Optional[str] = Field(None, max_length=36, description="UUID del CFDI")
    folio_fiscal: Optional[str] = Field(None, max_length=50, description="Folio fiscal")
    fecha_timbrado: Optional[datetime] = Field(None, description="Fecha de timbrado del CFDI")
    referencia_documento: Optional[str] = Field(None, max_length=100, description="Referencia al documento relacionado")
    usuario_elaboro_id: Optional[UUID4] = Field(None, description="ID del usuario que elaboró")
    usuario_autorizo_id: Optional[UUID4] = Field(None, description="ID del usuario que autorizó")


class PolizaContableCreate(PolizaContableBase):
    pass


class PolizaContableUpdate(BaseModel):
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    conciliada: Optional[bool] = None
    uuid_cfdi: Optional[str] = Field(None, max_length=36)
    folio_fiscal: Optional[str] = Field(None, max_length=50)
    fecha_timbrado: Optional[datetime] = None
    referencia_documento: Optional[str] = Field(None, max_length=100)
    usuario_autorizo_id: Optional[UUID4] = None


class PolizaContableResponse(PolizaContableBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# ACCOUNTING MOVEMENT SCHEMAS
# ============================================================================

class MovimientoContableBase(BaseModel):
    poliza_id: UUID4
    cuenta_id: UUID4
    tipo_movimiento: str = Field(..., description="Tipo de movimiento (debe/haber)")
    importe: Decimal = Field(..., description="Importe del movimiento")
    descripcion: Optional[str] = Field(None, description="Descripción del movimiento")
    uuid_cfdi: Optional[str] = Field(None, max_length=36, description="UUID del CFDI relacionado")
    referencia: Optional[str] = Field(None, max_length=100, description="Referencia del movimiento")
    conciliado: Optional[bool] = Field(default=False, description="¿Está conciliado?")
    fecha_conciliacion: Optional[datetime] = Field(None, description="Fecha de conciliación")


class MovimientoContableCreate(MovimientoContableBase):
    pass


class MovimientoContableUpdate(BaseModel):
    descripcion: Optional[str] = None
    uuid_cfdi: Optional[str] = Field(None, max_length=36)
    referencia: Optional[str] = Field(None, max_length=100)
    conciliado: Optional[bool] = None
    fecha_conciliacion: Optional[datetime] = None


class MovimientoContableResponse(MovimientoContableBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# FINANCIAL STATEMENT SCHEMAS
# ============================================================================

class EstadoFinancieroBase(BaseModel):
    nombre: str = Field(..., max_length=100, description="Nombre del estado financiero")
    tipo_estado: str = Field(..., max_length=50, description="Tipo de estado financiero")
    periodo_fiscal_id: UUID4 = Field(..., description="ID del periodo fiscal")
    contenido: Optional[Dict[str, Any]] = Field(None, description="Contenido del estado financiero en JSON")
    formato: Optional[str] = Field(default="vertical", max_length=20, description="Formato del estado")
    generado_por_id: Optional[UUID4] = Field(None, description="ID del usuario que generó")
    verificado: Optional[bool] = Field(default=False, description="¿Está verificado?")
    fecha_verificacion: Optional[datetime] = Field(None, description="Fecha de verificación")
    sellado_digital: Optional[str] = Field(None, max_length=255, description="Sellado digital para cumplimiento SAT")


class EstadoFinancieroCreate(EstadoFinancieroBase):
    pass


class EstadoFinancieroUpdate(BaseModel):
    contenido: Optional[Dict[str, Any]] = None
    verificado: Optional[bool] = None
    fecha_verificacion: Optional[datetime] = None
    sellado_digital: Optional[str] = Field(None, max_length=255)


class EstadoFinancieroResponse(EstadoFinancieroBase):
    id: UUID4
    fecha_generacion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# COST CENTER SCHEMAS
# ============================================================================

class CentroCostoBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único del centro de costo")
    nombre: str = Field(..., max_length=100, description="Nombre del centro de costo")
    descripcion: Optional[str] = Field(None, description="Descripción del centro de costo")
    tipo: Optional[str] = Field(None, max_length=50, description="Tipo de centro de costo")
    activo: bool = Field(default=True, description="¿Está activo?")
    padre_id: Optional[UUID4] = Field(None, description="ID del centro de costo padre")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable")


class CentroCostoCreate(CentroCostoBase):
    pass


class CentroCostoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    tipo: Optional[str] = Field(None, max_length=50)
    activo: Optional[bool] = None
    padre_id: Optional[UUID4] = None
    responsable_id: Optional[UUID4] = None


class CentroCostoResponse(CentroCostoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# BUDGETARY ENTRY SCHEMAS
# ============================================================================

class PartidaPresupuestalBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único de la partida")
    nombre: str = Field(..., max_length=100, description="Nombre de la partida presupuestal")
    descripcion: Optional[str] = Field(None, description="Descripción de la partida")
    presupuesto_original: Optional[Decimal] = Field(default=Decimal('0.00'), description="Presupuesto original")
    comprometido: Optional[Decimal] = Field(default=Decimal('0.00'), description="Monto comprometido")
    ejercido: Optional[Decimal] = Field(default=Decimal('0.00'), description="Monto ejercido")
    pagado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Monto pagado")
    periodo_fiscal_id: UUID4 = Field(..., description="ID del periodo fiscal")
    centro_costo_id: UUID4 = Field(..., description="ID del centro de costo")
    cuenta_contable_id: UUID4 = Field(..., description="ID de la cuenta contable")
    activo: bool = Field(default=True, description="¿Está activa?")


class PartidaPresupuestalCreate(PartidaPresupuestalBase):
    pass


class PartidaPresupuestalUpdate(BaseModel):
    descripcion: Optional[str] = None
    presupuesto_original: Optional[Decimal] = None
    comprometido: Optional[Decimal] = None
    ejercido: Optional[Decimal] = None
    pagado: Optional[Decimal] = None
    activo: Optional[bool] = None


class PartidaPresupuestalResponse(PartidaPresupuestalBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True