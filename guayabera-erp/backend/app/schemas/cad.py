"""
CAD Integration Schemas: Designs, patterns, and technical sheets
Specialized for textile manufacturing companies
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
# DESIGN SCHEMAS
# ============================================================================

class DisenoBase(BaseModel):
    codigo: str = Field(..., max_length=50, description="Código único del diseño")
    nombre: str = Field(..., max_length=200, description="Nombre del diseño")
    descripcion: Optional[str] = Field(None, description="Descripción del diseño")
    tipo_diseno: str = Field(..., description="Tipo de diseño")
    categoria: Optional[str] = Field(None, description="Categoría de la prenda")
    temporada: Optional[str] = Field(None, max_length=50, description="Temporada del diseño")
    colección: Optional[str] = Field(None, max_length=100, description="Colección a la que pertenece")
    composicion_tela: Optional[str] = Field(None, max_length=200, description="Composición de la tela")
    instrucciones_especiales: Optional[str] = Field(None, description="Instrucciones especiales del diseño")
    holgura_base: Optional[Decimal] = Field(default=Decimal('3.00'), description="Holgura base en cm")
    factor_multiplicacion_talla: Optional[Decimal] = Field(default=Decimal('1.0250'), description="Factor para escalado por tallas")
    estado: Optional[str] = Field(default="borrador", description="Estado del diseño")
    activo: bool = Field(default=True, description="¿Está activo el diseño?")
    fecha_creacion: date = Field(..., description="Fecha de creación del diseño")
    fecha_actualizacion: Optional[datetime] = Field(None, description="Fecha de actualización")
    disenador_id: Optional[UUID4] = Field(None, description="ID del diseñador")
    aprobador_id: Optional[UUID4] = Field(None, description="ID del aprobador")


class DisenoCreate(DisenoBase):
    pass


class DisenoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo_diseno: Optional[str] = None
    categoria: Optional[str] = None
    temporada: Optional[str] = Field(None, max_length=50)
    colección: Optional[str] = Field(None, max_length=100)
    composicion_tela: Optional[str] = Field(None, max_length=200)
    instrucciones_especiales: Optional[str] = None
    holgura_base: Optional[Decimal] = None
    factor_multiplicacion_talla: Optional[Decimal] = None
    estado: Optional[str] = None
    activo: Optional[bool] = None
    fecha_actualizacion: Optional[datetime] = None
    disenador_id: Optional[UUID4] = None
    aprobador_id: Optional[UUID4] = None


class DisenoResponse(DisenoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DESIGN SIZE SCHEMAS
# ============================================================================

class DisenoTallaBase(BaseModel):
    diseno_id: UUID4
    codigo_talla: str = Field(..., max_length=10, description="Código de la talla (ej: M, L, XL)")
    nombre_talla: str = Field(..., max_length=50, description="Nombre completo de la talla")
    genero: Optional[str] = Field(None, max_length=20, description="Género: hombre, mujer, niño, niña, unisex")
    grupo_etario: Optional[str] = Field(None, max_length=20, description="Grupo etario: adulto, infantil, juvenil")
    pecho: Optional[Decimal] = Field(None, description="Medida de pecho en cm")
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
    ajuste_especifico: Optional[str] = Field(None, description="Ajustes específicos para esta talla")


class DisenoTallaCreate(DisenoTallaBase):
    pass


class DisenoTallaUpdate(BaseModel):
    codigo_talla: Optional[str] = Field(None, max_length=10)
    nombre_talla: Optional[str] = Field(None, max_length=50)
    pecho: Optional[Decimal] = None
    cintura: Optional[Decimal] = None
    largo_total: Optional[Decimal] = None
    largo_manga: Optional[Decimal] = None
    ancho_manga: Optional[Decimal] = None
    hombros: Optional[Decimal] = None
    cadera: Optional[Decimal] = None
    entrepierna: Optional[Decimal] = None
    ajuste_especifico: Optional[str] = None


class DisenoTallaResponse(DisenoTallaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DESIGN COMPONENT SCHEMAS
# ============================================================================

class ComponenteDisenoBase(BaseModel):
    diseno_id: UUID4
    producto_id: Optional[UUID4] = Field(None, description="ID del producto asociado")
    nombre: str = Field(..., max_length=100, description="Nombre del componente")
    tipo_componente: str = Field(..., max_length=50, description="Tipo de componente")
    descripcion: Optional[str] = Field(None, description="Descripción del componente")
    cantidad_por_talla: Optional[int] = Field(default=1, ge=1, description="Cantidad por prenda")
    orientacion_tela: Optional[str] = Field(default="recto", max_length=20, description="Orientación de la tela")
    margen_costura: Optional[Decimal] = Field(default=Decimal('1.00'), description="Margen de costura en cm")
    tiene_grano: Optional[bool] = Field(default=True, description="¿Tiene dirección de grano?")
    sentido_grano: Optional[str] = Field(default="paralelo", max_length=20, description="Sentido del grano")
    instrucciones_corte: Optional[str] = Field(None, description="Instrucciones de corte")
    instrucciones_confeccion: Optional[str] = Field(None, description="Instrucciones de confección")
    datos_patron: Optional[Dict[str, Any]] = Field(None, description="Datos del patrón en formato JSON")


class ComponenteDisenoCreate(ComponenteDisenoBase):
    pass


class ComponenteDisenoUpdate(BaseModel):
    producto_id: Optional[UUID4] = None
    nombre: Optional[str] = Field(None, max_length=100)
    tipo_componente: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    cantidad_por_talla: Optional[int] = Field(None, ge=1)
    orientacion_tela: Optional[str] = Field(None, max_length=20)
    margen_costura: Optional[Decimal] = None
    tiene_grano: Optional[bool] = None
    sentido_grano: Optional[str] = Field(None, max_length=20)
    instrucciones_corte: Optional[str] = None
    instrucciones_confeccion: Optional[str] = None
    datos_patron: Optional[Dict[str, Any]] = None


class ComponenteDisenoResponse(ComponenteDisenoBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# TECHNICAL SHEET SCHEMAS
# ============================================================================

class FichaTecnicaBase(BaseModel):
    diseno_id: UUID4
    codigo: str = Field(..., max_length=50, description="Código único de la ficha técnica")
    version: Optional[str] = Field(default="1.0", max_length=20, description="Versión de la ficha")
    titulo: str = Field(..., max_length=200, description="Título de la ficha técnica")
    procesos: Optional[Dict[str, Any]] = Field(None, description="Procesos de manufactura")
    maquinaria_requerida: Optional[Dict[str, Any]] = Field(None, description="Maquinaria requerida")
    tiempos_estimados: Optional[Dict[str, Any]] = Field(None, description="Tiempos estimados por proceso")
    materiales_adicionales: Optional[Dict[str, Any]] = Field(None, description="Materiales adicionales")
    calidad_controles: Optional[Dict[str, Any]] = Field(None, description="Controles de calidad")
    archivo_pdf: Optional[str] = Field(None, max_length=500, description="Ruta al archivo PDF")
    archivo_imagen: Optional[str] = Field(None, max_length=500, description="Ruta al archivo de imagen")
    activa: Optional[bool] = Field(default=True, description="¿Está activa la ficha?")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable")


class FichaTecnicaCreate(FichaTecnicaBase):
    pass


class FichaTecnicaUpdate(BaseModel):
    version: Optional[str] = Field(None, max_length=20)
    titulo: Optional[str] = Field(None, max_length=200)
    procesos: Optional[Dict[str, Any]] = None
    maquinaria_requerida: Optional[Dict[str, Any]] = None
    tiempos_estimados: Optional[Dict[str, Any]] = None
    materiales_adicionales: Optional[Dict[str, Any]] = None
    calidad_controles: Optional[Dict[str, Any]] = None
    archivo_pdf: Optional[str] = Field(None, max_length=500)
    archivo_imagen: Optional[str] = Field(None, max_length=500)
    activa: Optional[bool] = None
    responsable_id: Optional[UUID4] = None


class FichaTecnicaResponse(FichaTecnicaBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# DESIGN HISTORY SCHEMAS
# ============================================================================

class HistoricoDisenoBase(BaseModel):
    diseno_id: UUID4
    tipo_cambio: str = Field(..., max_length=50, description="Tipo de cambio realizado")
    descripcion_cambio: Optional[str] = Field(None, description="Descripción del cambio")
    campos_modificados: Optional[Dict[str, Any]] = Field(None, description="Campos que fueron modificados")
    usuario_id: Optional[UUID4] = Field(None, description="ID del usuario que hizo el cambio")
    fecha_cambio: Optional[datetime] = Field(None, description="Fecha del cambio")


class HistoricoDisenoCreate(HistoricoDisenoBase):
    pass


class HistoricoDisenoUpdate(BaseModel):
    tipo_cambio: Optional[str] = Field(None, max_length=50)
    descripcion_cambio: Optional[str] = None
    campos_modificados: Optional[Dict[str, Any]] = None
    usuario_id: Optional[UUID4] = None


class HistoricoDisenoResponse(HistoricoDisenoBase):
    id: UUID4
    fecha_cambio: datetime

    class Config:
        from_attributes = True