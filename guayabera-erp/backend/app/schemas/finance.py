"""
Accounting schemas for request/response validation
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID
from decimal import Decimal


# ============= CUENTA CONTABLE =============

class CuentaContableBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=200)
    nivel: int = Field(..., ge=1, le=4)
    tipo: str  # activo, pasivo, capital, ingresos, costos, gastos
    naturaleza: Optional[str] = None  # deudora, acreedora
    es_cuenta_mayor: bool = False
    es_agrupadora: bool = False
    descripcion: Optional[str] = None
    cuenta_padre_id: Optional[UUID] = None
    requiere_centro_costos: bool = False
    requiere_documento_referencia: bool = False
    numero_cuenta_bancaria: Optional[str] = None
    banco_sat: Optional[str] = None


class CuentaContableCreate(CuentaContableBase):
    pass


class CuentaContableUpdate(BaseModel):
    nombre: Optional[str] = None
    activa: Optional[bool] = None
    descripcion: Optional[str] = None
    requiere_centro_costos: Optional[bool] = None


class CuentaContableResponse(CuentaContableBase):
    id: UUID
    activa: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CuentaContableTree(CuentaContableResponse):
    cuentas_hijas: List['CuentaContableTree'] = []


# ============= CENTRO DE COSTO =============

class CentroCostoBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None


class CentroCostoCreate(CentroCostoBase):
    pass


class CentroCostoUpdate(BaseModel):
    nombre: Optional[str] = None
    activo: Optional[bool] = None
    descripcion: Optional[str] = None


class CentroCostoResponse(CentroCostoBase):
    id: UUID
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= POLIZA CONTABLE =============

class MovimientoPolizaBase(BaseModel):
    cuenta_id: UUID
    centro_costo_id: Optional[UUID] = None
    cargo: Decimal = Field(default=0, ge=0)
    abono: Decimal = Field(default=0, ge=0)
    concepto: str = Field(..., min_length=3, max_length=500)
    referencia: Optional[str] = None
    documento_referencia: Optional[str] = None
    fecha_documento: Optional[date] = None

    @field_validator('cargo', 'abono')
    @classmethod
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError('Los montos no pueden ser negativos')
        return v


class MovimientoPolizaCreate(MovimientoPolizaBase):
    pass


class MovimientoPolizaResponse(MovimientoPolizaBase):
    id: UUID
    poliza_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class PolizaContableBase(BaseModel):
    tipo: str  # diario, ingreso, egreso
    fecha: date
    descripcion: str = Field(..., min_length=3)
    comentario_adicional: Optional[str] = None
    modulo_origen: Optional[str] = None
    referencia_externa: Optional[str] = None


class PolizaContableCreate(PolizaContableBase):
    movimientos: List[MovimientoPolizaCreate] = Field(..., min_length=2)

    @field_validator('movimientos')
    @classmethod
    def validate_poliza_balanced(cls, v):
        total_cargos = sum(m.cargo for m in v)
        total_abonos = sum(m.abono for m in v)
        if total_cargos != total_abonos:
            raise ValueError(
                f'La póliza no está cuadrada. Cargos: {total_cargos}, Abonos: {total_abonos}'
            )
        if total_cargos == 0:
            raise ValueError('La póliza debe tener montos mayores a cero')
        return v


class PolizaContableUpdate(BaseModel):
    descripcion: Optional[str] = None
    comentario_adicional: Optional[str] = None
    estado: Optional[str] = None


class PolizaContableResponse(PolizaContableBase):
    id: UUID
    numero: int
    estado: str
    total_cargos: Decimal
    total_abonos: Decimal
    esta_cuadrada: bool
    movimientos: List[MovimientoPolizaResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


class PolizaContableSummary(BaseModel):
    """Lightweight summary for lists"""
    id: UUID
    numero: int
    tipo: str
    fecha: date
    descripcion: str
    estado: str
    total_cargos: Decimal
    total_abonos: Decimal
    esta_cuadrada: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= BANCO =============

class BancoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    cuenta: str = Field(..., min_length=10, max_length=20)
    clabe: Optional[str] = Field(None, min_length=18, max_length=18)
    tipo_cuenta: Optional[str] = None
    moneda: str = "MXN"
    sucursal: Optional[str] = None
    cuenta_contable_id: Optional[UUID] = None
    descripcion: Optional[str] = None


class BancoCreate(BancoBase):
    pass


class BancoUpdate(BaseModel):
    nombre: Optional[str] = None
    saldo_actual: Optional[Decimal] = None
    activo: Optional[bool] = None


class BancoResponse(BancoBase):
    id: UUID
    saldo_actual: Decimal
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= MOVIMIENTO BANCARIO =============

class MovimientoBancarioBase(BaseModel):
    banco_id: UUID
    fecha: date
    descripcion: str = Field(..., min_length=3, max_length=500)
    referencia: Optional[str] = None
    tipo_movimiento: Optional[str] = None
    cargo: Decimal = Field(default=0, ge=0)
    abono: Decimal = Field(default=0, ge=0)
    saldo: Optional[Decimal] = None


class MovimientoBancarioCreate(MovimientoBancarioBase):
    pass


class MovimientoBancarioResponse(MovimientoBancarioBase):
    id: UUID
    conciliado: bool
    importado: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= ASIENTO CONTABLE =============

class AsientoContableResponse(BaseModel):
    id: UUID
    modulo_origen: str
    entidad_origen: str
    entidad_id: UUID
    referencia: Optional[str] = None
    poliza_id: Optional[UUID] = None
    estado: str
    fecha_procesado: Optional[datetime] = None
    datos_origen: Optional[dict] = None
    errores: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= PERIODO CONTABLE =============

class PeriodoContableBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    fecha_inicio: date
    fecha_fin: date


class PeriodoContableCreate(PeriodoContableBase):
    pass


class PeriodoContableUpdate(BaseModel):
    estado: Optional[str] = None


class PeriodoContableResponse(PeriodoContableBase):
    id: UUID
    estado: str
    fecha_cierre: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= BALANZA DE COMPROBACIÓN =============

class BalanzaComprobacionRequest(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    nivel_detalle: int = Field(default=4, ge=1, le=4)  # Level of detail
    solo_movimientos: bool = False  # Only accounts with movements


class BalanzaComprobacionLinea(BaseModel):
    cuenta_id: UUID
    cuenta_codigo: str
    cuenta_nombre: str
    nivel: int
    tipo: str
    saldo_inicial: Decimal
    cargos: Decimal
    abonos: Decimal
    saldo_final: Decimal


class BalanzaComprobacionResponse(BaseModel):
    fecha_desde: date
    fecha_hasta: date
    lineas: List[BalanzaComprobacionLinea]
    total_cargos: Decimal
    total_abonos: Decimal
    esta_cuadrada: bool


# ============= ESTADO DE RESULTADOS =============

class EstadoResultadosResponse(BaseModel):
    periodo_inicio: date
    periodo_fin: date
    ingresos: Decimal
    costos: Decimal
    utilidad_bruta: Decimal
    gastos_operacion: Decimal
    utilidad_operacion: Decimal
    otros_ingresos: Decimal
    otros_gastos: Decimal
    utilidad_neta: Decimal
