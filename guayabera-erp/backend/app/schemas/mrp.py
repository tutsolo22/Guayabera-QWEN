from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import uuid
import enum


class TipoEstado(str, enum.Enum):
    pendiente = "pendiente"
    programada = "programada"
    en_progreso = "en_progreso"
    completada = "completada"
    cancelada = "cancelada"


class PrioridadOrden(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    urgente = "urgente"


class TipoPrevision(str, enum.Enum):
    venta = "venta"
    proyecto = "proyecto"
    evento = "evento"
    promocion = "promocion"
    otros = "otros"


class TipoPrograma(str, enum.Enum):
    demanda_cliente = "demanda_cliente"
    prevision = "prevision"
    inventario_seguridad = "inventario_seguridad"
    muestra = "muestra"
    otros = "otros"


class EstadoPrograma(str, enum.Enum):
    borrador = "borrador"
    aprobado = "aprobado"
    en_ejecucion = "en_ejecucion"
    cerrado = "cerrado"


class RecetaBase(BaseModel):
    nombre: str = Field(..., max_length=200, description="Nombre de la receta")
    producto_final_id: UUID4 = Field(..., description="ID del producto resultante")
    descripcion: Optional[str] = Field(None, description="Descripción de la receta")
    rendimiento: Decimal = Field(..., description="Cantidad de producto final producido")
    activa: bool = Field(default=True, description="Si la receta está activa")
    version: int = Field(default=1, description="Versión de la receta")
    fecha_revision: Optional[date] = Field(None, description="Fecha de última revisión")


class RecetaCreate(RecetaBase):
    pass


class RecetaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    rendimiento: Optional[Decimal] = None
    activa: Optional[bool] = None
    version: Optional[int] = None
    fecha_revision: Optional[date] = None


class RecetaResponse(RecetaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IngredienteRecetaBase(BaseModel):
    receta_id: UUID4 = Field(..., description="ID de la receta")
    ingrediente_id: UUID4 = Field(..., description="ID del producto que es ingrediente")
    cantidad_requerida: Decimal = Field(..., description="Cantidad necesaria del ingrediente")
    unidad_medida: str = Field(..., max_length=20, description="Unidad de medida")
    secuencia: int = Field(default=1, description="Orden de utilización en el proceso")


class IngredienteRecetaCreate(IngredienteRecetaBase):
    pass


class IngredienteRecetaUpdate(BaseModel):
    cantidad_requerida: Optional[Decimal] = None
    unidad_medida: Optional[str] = Field(None, max_length=20)
    secuencia: Optional[int] = None


class IngredienteRecetaResponse(IngredienteRecetaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrdenProduccionBase(BaseModel):
    codigo: str = Field(..., max_length=50, description="Código único de la orden")
    producto_id: UUID4 = Field(..., description="ID del producto a fabricar")
    cantidad_programada: Decimal = Field(..., description="Cantidad a producir")
    cantidad_real: Optional[Decimal] = Field(default=0, description="Cantidad realmente producida")
    fecha_inicio: date = Field(..., description="Fecha programada de inicio")
    fecha_fin: Optional[date] = Field(None, description="Fecha programada de finalización")
    estado: TipoEstado = Field(default=TipoEstado.pendiente, description="Estado de la orden")
    prioridad: PrioridadOrden = Field(default=PrioridadOrden.media, description="Prioridad de la orden")
    observaciones: Optional[str] = Field(None, description="Observaciones sobre la orden")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable de la orden")


class OrdenProduccionCreate(OrdenProduccionBase):
    pass


class OrdenProduccionUpdate(BaseModel):
    cantidad_programada: Optional[Decimal] = None
    cantidad_real: Optional[Decimal] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[TipoEstado] = None
    prioridad: Optional[PrioridadOrden] = None
    observaciones: Optional[str] = None
    responsable_id: Optional[UUID4] = None


class OrdenProduccionResponse(OrdenProduccionBase):
    id: UUID4
    fecha_inicio_real: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConsumoMaterialBase(BaseModel):
    orden_produccion_id: UUID4 = Field(..., description="ID de la orden de producción")
    producto_id: UUID4 = Field(..., description="ID del material consumido")
    cantidad_requerida: Decimal = Field(..., description="Cantidad requerida")
    cantidad_consumida: Decimal = Field(default=0, description="Cantidad realmente consumida")
    unidad_medida: str = Field(..., max_length=20, description="Unidad de medida")
    fecha_consumo: Optional[date] = Field(None, description="Fecha de consumo")


class ConsumoMaterialCreate(ConsumoMaterialBase):
    pass


class ConsumoMaterialUpdate(BaseModel):
    cantidad_consumida: Optional[Decimal] = None
    fecha_consumo: Optional[date] = None


class ConsumoMaterialResponse(ConsumoMaterialBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PrevisionDemandaBase(BaseModel):
    producto_id: UUID4 = Field(..., description="ID del producto previsto")
    periodo_inicio: date = Field(..., description="Fecha de inicio del período")
    periodo_fin: date = Field(..., description="Fecha de fin del período")
    cantidad_prevista: Decimal = Field(..., description="Cantidad prevista")
    tipo_prevision: TipoPrevision = Field(..., description="Tipo de previsión")
    origen_datos: Optional[str] = Field(None, max_length=100, description="Origen de la previsión")
    confianza: Optional[float] = Field(None, description="Nivel de confianza en la previsión (0-100%)")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable de la previsión")


class PrevisionDemandaCreate(PrevisionDemandaBase):
    pass


class PrevisionDemandaUpdate(BaseModel):
    cantidad_prevista: Optional[Decimal] = None
    tipo_prevision: Optional[TipoPrevision] = None
    origen_datos: Optional[str] = Field(None, max_length=100)
    confianza: Optional[float] = None
    responsable_id: Optional[UUID4] = None


class PrevisionDemandaResponse(PrevisionDemandaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgramaMaestroProduccionBase(BaseModel):
    producto_id: UUID4 = Field(..., description="ID del producto programado")
    periodo_inicio: date = Field(..., description="Fecha de inicio del período")
    periodo_fin: date = Field(..., description="Fecha de fin del período")
    cantidad_programada: Decimal = Field(..., description="Cantidad programada")
    tipo_programa: TipoPrograma = Field(..., description="Tipo de programa")
    origen: Optional[str] = Field(None, max_length=100, description="Origen del programa")
    estado: EstadoPrograma = Field(default=EstadoPrograma.borrador, description="Estado del programa")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable del programa")


class ProgramaMaestroProduccionCreate(ProgramaMaestroProduccionBase):
    pass


class ProgramaMaestroProduccionUpdate(BaseModel):
    cantidad_programada: Optional[Decimal] = None
    tipo_programa: Optional[TipoPrograma] = None
    origen: Optional[str] = Field(None, max_length=100)
    estado: Optional[EstadoPrograma] = None
    responsable_id: Optional[UUID4] = None


class ProgramaMaestroProduccionResponse(ProgramaMaestroProduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True