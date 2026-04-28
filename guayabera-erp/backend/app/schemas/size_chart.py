"""
Size Chart Schemas: Standard Mexican sizing for clothing
Including sizes for men, women, boys, girls with standard measurements
"""

from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
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
# SIZE CHART SCHEMAS
# ============================================================================

class TablaTallaBase(BaseModel):
    codigo: str = Field(..., max_length=30, description="Código único de la tabla de tallas")
    nombre: str = Field(..., max_length=100, description="Nombre de la tabla de tallas")
    descripcion: Optional[str] = Field(None, description="Descripción de la tabla")
    tipo_prenda: str = Field(..., description="Tipo de prenda")
    genero: str = Field(..., description="Género: hombre, mujer, niño, niña, unisex")
    grupo_etario: Optional[str] = Field(None, description="Grupo etario: adulto, infantil, juvenil")
    activa: bool = Field(default=True, description="¿Está activa la tabla?")
    es_estandar_mexicano: Optional[bool] = Field(default=True, description="¿Es una tabla estándar mexicana?")
    creador_id: Optional[UUID4] = Field(None, description="ID del creador")


class TablaTallaCreate(TablaTallaBase):
    pass


class TablaTallaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    tipo_prenda: Optional[str] = None
    genero: Optional[str] = None
    grupo_etario: Optional[str] = None
    activa: Optional[bool] = None
    es_estandar_mexicano: Optional[bool] = None
    creador_id: Optional[UUID4] = None


class TablaTallaResponse(TablaTallaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SIZE SCHEMAS
# ============================================================================

class TallaBase(BaseModel):
    tabla_talla_id: UUID4
    codigo: str = Field(..., max_length=10, description="Código de la talla (ej: CH, M, G, EG, 1X)")
    nombre: str = Field(..., max_length=30, description="Nombre de la talla (ej: Chica, Mediana)")
    posicion_orden: Optional[int] = Field(None, description="Posición para ordenar tallas")
    pecho_bust: Optional[Decimal] = Field(None, description="Medida de pecho o busto en cm")
    cintura: Optional[Decimal] = Field(None, description="Medida de cintura en cm")
    cadera: Optional[Decimal] = Field(None, description="Medida de cadera en cm")
    largo_total: Optional[Decimal] = Field(None, description="Largo total en cm")
    largo_torso: Optional[Decimal] = Field(None, description="Largo de torso en cm")
    largo_manga: Optional[Decimal] = Field(None, description="Largo de manga en cm")
    ancho_manga: Optional[Decimal] = Field(None, description="Ancho de manga en cm")
    hombros: Optional[Decimal] = Field(None, description="Medida de hombros en cm")
    entrepierna: Optional[Decimal] = Field(None, description="Entrepierna en cm (para pantalones)")
    largo_tiro: Optional[Decimal] = Field(None, description="Largo de tiro en cm (para pantalones)")
    ancho_cadera: Optional[Decimal] = Field(None, description="Ancho de cadera en cm")
    cuello: Optional[Decimal] = Field(None, description="Circunferencia de cuello en cm")
    puño: Optional[Decimal] = Field(None, description="Circunferencia de puño en cm")
    largo_pantalon: Optional[Decimal] = Field(None, description="Largo de pantalón en cm")
    edad_minima: Optional[int] = Field(None, description="Edad mínima recomendada")
    edad_maxima: Optional[int] = Field(None, description="Edad máxima recomendada")
    notas: Optional[str] = Field(None, description="Notas adicionales sobre la talla")


class TallaCreate(TallaBase):
    pass


class TallaUpdate(BaseModel):
    codigo: Optional[str] = Field(None, max_length=10)
    nombre: Optional[str] = Field(None, max_length=30)
    posicion_orden: Optional[int] = None
    pecho_bust: Optional[Decimal] = None
    cintura: Optional[Decimal] = None
    cadera: Optional[Decimal] = None
    largo_total: Optional[Decimal] = None
    largo_torso: Optional[Decimal] = None
    largo_manga: Optional[Decimal] = None
    ancho_manga: Optional[Decimal] = None
    hombros: Optional[Decimal] = None
    entrepierna: Optional[Decimal] = None
    largo_tiro: Optional[Decimal] = None
    ancho_cadera: Optional[Decimal] = None
    cuello: Optional[Decimal] = None
    puño: Optional[Decimal] = None
    largo_pantalon: Optional[Decimal] = None
    edad_minima: Optional[int] = None
    edad_maxima: Optional[int] = None
    notas: Optional[str] = None


class TallaResponse(TallaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# SIZE REFERENCE SCHEMAS
# ============================================================================

class ReferenciaTallaBase(BaseModel):
    talla_id: UUID4
    sistema_referencia: str = Field(..., max_length=50, description="Sistema de referencia (US, EU, UK)")
    codigo_referencia: str = Field(..., max_length=10, description="Código en el sistema de referencia")


class ReferenciaTallaCreate(ReferenciaTallaBase):
    pass


class ReferenciaTallaUpdate(BaseModel):
    sistema_referencia: Optional[str] = Field(None, max_length=50)
    codigo_referencia: Optional[str] = Field(None, max_length=10)


class ReferenciaTallaResponse(ReferenciaTallaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True