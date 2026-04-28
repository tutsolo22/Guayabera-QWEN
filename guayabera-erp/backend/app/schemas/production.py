"""
Textile Production Schemas: Patterns, garments, manufacturing processes
Specialized for guayabera production and textile manufacturing
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
from datetime import datetime
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
# PRODUCTION SCHEMAS
# ============================================================================

# PatronPrenda Schemas
class PatronPrendaBase(BaseModel):
    codigo: str = Field(..., max_length=50, description="Código único del patrón")
    nombre: str = Field(..., max_length=200, description="Nombre del patrón")
    descripcion: Optional[str] = Field(None, description="Descripción del patrón")
    tipo_prenda: str = Field(..., description="Tipo de prenda")
    caracteristicas_especiales: Optional[str] = Field(None, description="Características especiales del patrón")
    estilo: Optional[str] = Field(None, max_length=100, description="Estilo del patrón")
    temporada: Optional[str] = Field(None, max_length=50, description="Temporada del diseño")
    genero: Optional[str] = Field(None, max_length=20, description="Género de la prenda")
    imagen_diseno: Optional[str] = Field(None, max_length=500, description="URL de la imagen del diseño")
    ficha_tecnica: Optional[str] = Field(None, max_length=500, description="URL de la ficha técnica")
    activo: bool = True
    es_plantilla: bool = False


class PatronPrendaCreate(PatronPrendaBase):
    pass


class PatronPrendaUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo_prenda: Optional[str] = None
    caracteristicas_especiales: Optional[str] = None
    estilo: Optional[str] = None
    temporada: Optional[str] = None
    genero: Optional[str] = None
    imagen_diseno: Optional[str] = None
    ficha_tecnica: Optional[str] = None
    activo: Optional[bool] = None
    es_plantilla: Optional[bool] = None


class PatronPrendaResponse(PatronPrendaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ComponentePatron Schemas
class ComponentePatronBase(BaseModel):
    patron_id: UUID4
    nombre: str = Field(..., max_length=100, description="Nombre del componente")
    tipo: str = Field(..., description="Tipo de componente")
    descripcion: Optional[str] = Field(None, description="Descripción del componente")
    cantidad_por_prenda: int = Field(default=1, ge=1, description="Cantidad del componente por prenda")
    posicion_x: Optional[float] = Field(None, description="Posición X en cm")
    posicion_y: Optional[float] = Field(None, description="Posición Y en cm")
    dimension_ancho: Optional[float] = Field(None, description="Ancho del componente en cm")
    dimension_alto: Optional[float] = Field(None, description="Alto del componente en cm")
    tolerancia: float = Field(default=0.5, ge=0, description="Tolerancia de corte en cm")
    tiene_boton: bool = False
    tiene_ojuelo: bool = False
    tiene_costura_decorativa: bool = False
    instrucciones_especiales: Optional[str] = Field(None, description="Instrucciones especiales")
    material_requerido_id: Optional[UUID4] = Field(None, description="ID del material requerido")


class ComponentePatronCreate(ComponentePatronBase):
    pass


class ComponentePatronUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad_por_prenda: Optional[int] = Field(None, ge=1)
    posicion_x: Optional[float] = None
    posicion_y: Optional[float] = None
    dimension_ancho: Optional[float] = None
    dimension_alto: Optional[float] = None
    tolerancia: Optional[float] = Field(None, ge=0)
    tiene_boton: Optional[bool] = None
    tiene_ojuelo: Optional[bool] = None
    tiene_costura_decorativa: Optional[bool] = None
    instrucciones_especiales: Optional[str] = None
    material_requerido_id: Optional[UUID4] = None


class ComponentePatronResponse(ComponentePatronBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# VariantePrenda Schemas
class VariantePrendaBase(BaseModel):
    patron_id: UUID4
    cliente_id: Optional[UUID4] = Field(None, description="Cliente para diseños personalizados")
    codigo: str = Field(..., max_length=50, description="Código único de la variante")
    nombre: str = Field(..., max_length=200, description="Nombre de la variante")
    descripcion: Optional[str] = Field(None, description="Descripción de la variante")
    talla: Optional[str] = Field(None, max_length=10, description="Talla de la prenda")
    medidas_especificas: Optional[Dict[str, Any]] = Field(None, description="Medidas personalizadas en formato JSON")
    color: Optional[str] = Field(None, max_length=50, description="Color de la prenda")
    tipo_tela: Optional[str] = Field(None, description="Tipo de tela")
    tipo_hilo: Optional[str] = Field(None, max_length=50, description="Tipo de hilo")
    tipo_boton: Optional[str] = Field(None, max_length=100, description="Tipo de botón")
    caracteristicas_adicionales: Optional[str] = Field(None, description="Características adicionales")
    tiempo_estimado_produccion: Optional[int] = Field(None, ge=0, description="Tiempo estimado en horas")
    costo_estimado: Optional[Decimal] = Field(None, description="Costo estimado de producción")
    activo: bool = True
    es_personalizada: bool = False


class VariantePrendaCreate(VariantePrendaBase):
    pass


class VariantePrendaUpdate(BaseModel):
    cliente_id: Optional[UUID4] = None
    codigo: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    talla: Optional[str] = None
    medidas_especificas: Optional[Dict[str, Any]] = None
    color: Optional[str] = None
    tipo_tela: Optional[str] = None
    tipo_hilo: Optional[str] = None
    tipo_boton: Optional[str] = None
    caracteristicas_adicionales: Optional[str] = None
    tiempo_estimado_produccion: Optional[int] = Field(None, ge=0)
    costo_estimado: Optional[Decimal] = None
    activo: Optional[bool] = None
    es_personalizada: Optional[bool] = None


class VariantePrendaResponse(VariantePrendaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# OrdenProduccion Schemas
class OrdenProduccionBase(BaseModel):
    variante_prenda_id: UUID4
    cliente_id: Optional[UUID4] = None
    almacen_salida_id: Optional[UUID4] = None
    folio: str = Field(..., max_length=30, description="Folio de la orden de producción")
    descripcion: Optional[str] = Field(None, description="Descripción de la orden")
    cantidad: int = Field(..., gt=0, description="Cantidad a producir")
    fecha_inicio: Optional[str] = Field(None, description="Fecha de inicio (YYYY-MM-DD)")
    fecha_entrega: Optional[str] = Field(None, description="Fecha de entrega estimada (YYYY-MM-DD)")
    prioridad: int = Field(default=1, ge=1, le=5, description="Prioridad (1-5)")
    estado: str = Field(default="borrador", description="Estado de la orden")
    porcentaje_completado: Decimal = Field(default=Decimal('0.00'), description="Porcentaje completado")
    costo_estimado_total: Optional[Decimal] = Field(None, description="Costo estimado total")
    costo_real_total: Optional[Decimal] = Field(None, description="Costo real total")


class OrdenProduccionCreate(OrdenProduccionBase):
    pass


class OrdenProduccionUpdate(BaseModel):
    variante_prenda_id: Optional[UUID4] = None
    cliente_id: Optional[UUID4] = None
    almacen_salida_id: Optional[UUID4] = None
    folio: Optional[str] = Field(None, max_length=30)
    descripcion: Optional[str] = None
    cantidad: Optional[int] = Field(None, gt=0)
    fecha_inicio: Optional[str] = None
    fecha_entrega: Optional[str] = None
    prioridad: Optional[int] = Field(None, ge=1, le=5)
    estado: Optional[str] = None
    porcentaje_completado: Optional[Decimal] = None
    costo_estimado_total: Optional[Decimal] = None
    costo_real_total: Optional[Decimal] = None


class OrdenProduccionResponse(OrdenProduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    fecha_estado_actual: datetime

    class Config:
        from_attributes = True


# ProcesoProduccion Schemas
class ProcesoProduccionBase(BaseModel):
    orden_produccion_id: UUID4
    responsable_id: Optional[UUID4] = None
    tipo: str = Field(..., description="Tipo de proceso")
    descripcion: Optional[str] = Field(None, description="Descripción del proceso")
    numero_secuencia: Optional[int] = Field(None, description="Número de secuencia del proceso")
    fecha_inicio_planificada: Optional[str] = Field(None, description="Fecha de inicio planificada")
    fecha_fin_planificada: Optional[str] = Field(None, description="Fecha de fin planificada")
    fecha_inicio_real: Optional[datetime] = Field(None, description="Fecha de inicio real")
    fecha_fin_real: Optional[datetime] = Field(None, description="Fecha de fin real")
    estado: str = Field(default="pendiente", description="Estado del proceso")
    observaciones: Optional[str] = Field(None, description="Observaciones del proceso")


class ProcesoProduccionCreate(ProcesoProduccionBase):
    pass


class ProcesoProduccionUpdate(BaseModel):
    responsable_id: Optional[UUID4] = None
    descripcion: Optional[str] = None
    numero_secuencia: Optional[int] = None
    fecha_inicio_planificada: Optional[str] = None
    fecha_fin_planificada: Optional[str] = None
    fecha_inicio_real: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None


class ProcesoProduccionResponse(ProcesoProduccionBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ListaMateriales Schemas
class ListaMaterialesBase(BaseModel):
    variante_prenda_id: UUID4
    codigo: str = Field(..., max_length=50, description="Código único de la lista")
    nombre: str = Field(..., max_length=200, description="Nombre de la lista")
    descripcion: Optional[str] = Field(None, description="Descripción de la lista")
    activo: bool = True


class ListaMaterialesCreate(ListaMaterialesBase):
    pass


class ListaMaterialesUpdate(BaseModel):
    variante_prenda_id: Optional[UUID4] = None
    codigo: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class ListaMaterialesResponse(ListaMaterialesBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# MaterialLista Schemas
class MaterialListaBase(BaseModel):
    lista_materiales_id: UUID4
    producto_id: UUID4
    cantidad_requerida: Decimal = Field(..., ge=0, description="Cantidad requerida del material")
    unidad_medida: Optional[str] = Field(None, max_length=10, description="Unidad de medida")
    desperdicio_porcentaje: Decimal = Field(default=Decimal('0.00'), ge=0, le=100, description="Porcentaje de desperdicio")
    notas: Optional[str] = Field(None, description="Notas sobre el material")


class MaterialListaCreate(MaterialListaBase):
    pass


class MaterialListaUpdate(BaseModel):
    lista_materiales_id: Optional[UUID4] = None
    producto_id: Optional[UUID4] = None
    cantidad_requerida: Optional[Decimal] = Field(None, ge=0)
    unidad_medida: Optional[str] = None
    desperdicio_porcentaje: Optional[Decimal] = Field(None, ge=0, le=100)
    notas: Optional[str] = None


class MaterialListaResponse(MaterialListaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True