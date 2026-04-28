"""
CRM Schemas: Customer relationship management, interactions, marketing campaigns
Specialized for textile business customer management
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
# CUSTOMER SCHEMAS
# ============================================================================

class ClienteBase(BaseModel):
    codigo_cliente: str = Field(..., max_length=30, description="Código único del cliente")
    nombre_comercial: str = Field(..., max_length=100, description="Nombre comercial del cliente")
    razon_social: Optional[str] = Field(None, max_length=150, description="Razón social del cliente")
    tipo_cliente: Optional[str] = Field(default="particular", description="Tipo de cliente")
    estado: Optional[str] = Field(default="prospecto", description="Estado del cliente")
    direccion: Optional[str] = Field(None, description="Dirección del cliente")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad del cliente")
    estado_provincia: Optional[str] = Field(None, max_length=100, description="Estado o provincia del cliente")
    pais: Optional[str] = Field(default="México", max_length=100, description="País del cliente")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal del cliente")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del cliente")
    email: Optional[str] = Field(None, max_length=100, description="Email del cliente")
    sitio_web: Optional[str] = Field(None, max_length=150, description="Sitio web del cliente")
    limite_credito: Optional[Decimal] = Field(default=Decimal('0.00'), description="Límite de crédito del cliente")
    dias_credito: Optional[int] = Field(default=0, description="Días de crédito concedidos")
    saldo_pendiente: Optional[Decimal] = Field(default=Decimal('0.00'), description="Saldo pendiente del cliente")
    segmento: Optional[str] = Field(None, max_length=50, description="Segmento del cliente")
    industria: Optional[str] = Field(None, max_length=100, description="Industria del cliente")
    fuente_origen: Optional[str] = Field(None, max_length=50, description="Fuente de origen del cliente")
    vendedor_asignado_id: Optional[UUID4] = Field(None, description="ID del vendedor asignado")
    fecha_ultimo_contacto: Optional[datetime] = Field(None, description="Fecha del último contacto")
    activo: bool = Field(default=True, description="¿Está activo el cliente?")
    comentarios: Optional[str] = Field(None, description="Comentarios adicionales")
    datos_adicionales: Optional[Dict[str, Any]] = Field(None, description="Datos adicionales del cliente")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_comercial: Optional[str] = Field(None, max_length=100)
    razon_social: Optional[str] = Field(None, max_length=150)
    tipo_cliente: Optional[str] = None
    estado: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado_provincia: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    sitio_web: Optional[str] = Field(None, max_length=150)
    limite_credito: Optional[Decimal] = None
    dias_credito: Optional[int] = None
    saldo_pendiente: Optional[Decimal] = None
    segmento: Optional[str] = Field(None, max_length=50)
    industria: Optional[str] = Field(None, max_length=100)
    fuente_origen: Optional[str] = Field(None, max_length=50)
    vendedor_asignado_id: Optional[UUID4] = None
    fecha_ultimo_contacto: Optional[datetime] = None
    activo: Optional[bool] = None
    comentarios: Optional[str] = None
    datos_adicionales: Optional[Dict[str, Any]] = None


class ClienteResponse(ClienteBase):
    id: UUID4
    fecha_registro: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CUSTOMER CONTACT SCHEMAS
# ============================================================================

class ContactoClienteBase(BaseModel):
    cliente_id: UUID4
    nombre: str = Field(..., max_length=100, description="Nombre del contacto")
    apellido_paterno: Optional[str] = Field(None, max_length=50, description="Apellido paterno del contacto")
    apellido_materno: Optional[str] = Field(None, max_length=50, description="Apellido materno del contacto")
    puesto: Optional[str] = Field(None, max_length=100, description="Puesto del contacto")
    departamento: Optional[str] = Field(None, max_length=100, description="Departamento del contacto")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del contacto")
    extension: Optional[str] = Field(None, max_length=10, description="Extensión telefónica")
    email: Optional[str] = Field(None, max_length=100, description="Email del contacto")
    skype: Optional[str] = Field(None, max_length=50, description="Usuario de Skype")
    es_principal: Optional[bool] = Field(default=False, description="¿Es contacto principal?")
    activo: bool = Field(default=True, description="¿Está activo el contacto?")


class ContactoClienteCreate(ContactoClienteBase):
    pass


class ContactoClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido_paterno: Optional[str] = Field(None, max_length=50)
    apellido_materno: Optional[str] = Field(None, max_length=50)
    puesto: Optional[str] = Field(None, max_length=100)
    departamento: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    extension: Optional[str] = Field(None, max_length=10)
    email: Optional[str] = Field(None, max_length=100)
    skype: Optional[str] = Field(None, max_length=50)
    es_principal: Optional[bool] = None
    activo: Optional[bool] = None


class ContactoClienteResponse(ContactoClienteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CUSTOMER INTERACTION SCHEMAS
# ============================================================================

class InteraccionClienteBase(BaseModel):
    cliente_id: UUID4
    contacto_id: Optional[UUID4] = Field(None, description="ID del contacto involucrado")
    vendedor_id: Optional[UUID4] = Field(None, description="ID del vendedor involucrado")
    tipo_interaccion: str = Field(..., description="Tipo de interacción")
    asunto: str = Field(..., max_length=150, description="Asunto de la interacción")
    descripcion: Optional[str] = Field(None, description="Descripción de la interacción")
    resultado: Optional[str] = Field(None, max_length=100, description="Resultado de la interacción")
    proximo_seguimiento: Optional[datetime] = Field(None, description="Próximo seguimiento")
    realizado: Optional[bool] = Field(default=False, description="¿Ya se realizó la interacción?")


class InteraccionClienteCreate(InteraccionClienteBase):
    pass


class InteraccionClienteUpdate(BaseModel):
    contacto_id: Optional[UUID4] = None
    vendedor_id: Optional[UUID4] = None
    tipo_interaccion: Optional[str] = None
    asunto: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    resultado: Optional[str] = Field(None, max_length=100)
    proximo_seguimiento: Optional[datetime] = None
    realizado: Optional[bool] = None


class InteraccionClienteResponse(InteraccionClienteBase):
    id: UUID4
    fecha_interaccion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# OPPORTUNITY SCHEMAS
# ============================================================================

class OportunidadBase(BaseModel):
    cliente_id: UUID4
    vendedor_id: UUID4
    nombre: str = Field(..., max_length=150, description="Nombre de la oportunidad")
    descripcion: Optional[str] = Field(None, description="Descripción de la oportunidad")
    valor_estimado: Optional[Decimal] = Field(default=Decimal('0.00'), description="Valor estimado de la oportunidad")
    probabilidad_cierre: Optional[int] = Field(default=0, ge=0, le=100, description="Probabilidad de cierre (0-100%)")
    estado: Optional[str] = Field(default="nueva", description="Estado de la oportunidad")
    fecha_cierre_estimada: Optional[date] = Field(None, description="Fecha de cierre estimada")
    fecha_cierre_real: Optional[date] = Field(None, description="Fecha de cierre real")
    tipo_oportunidad: Optional[str] = Field(None, max_length=50, description="Tipo de oportunidad")
    origen: Optional[str] = Field(None, max_length=50, description="Origen de la oportunidad")
    activa: bool = Field(default=True, description="¿Está activa la oportunidad?")


class OportunidadCreate(OportunidadBase):
    pass


class OportunidadUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    valor_estimado: Optional[Decimal] = None
    probabilidad_cierre: Optional[int] = Field(None, ge=0, le=100)
    estado: Optional[str] = None
    fecha_cierre_estimada: Optional[date] = None
    fecha_cierre_real: Optional[date] = None
    tipo_oportunidad: Optional[str] = Field(None, max_length=50)
    origen: Optional[str] = Field(None, max_length=50)
    activa: Optional[bool] = None


class OportunidadResponse(OportunidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# OPPORTUNITY ACTIVITY SCHEMAS
# ============================================================================

class ActividadOportunidadBase(BaseModel):
    oportunidad_id: UUID4
    asignado_a_id: Optional[UUID4] = Field(None, description="ID del empleado asignado")
    titulo: str = Field(..., max_length=150, description="Título de la actividad")
    descripcion: Optional[str] = Field(None, description="Descripción de la actividad")
    tipo_actividad: Optional[str] = Field(None, max_length=50, description="Tipo de actividad")
    prioridad: Optional[str] = Field(default="media", description="Prioridad de la actividad")
    fecha_inicio: Optional[datetime] = Field(None, description="Fecha de inicio de la actividad")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento de la actividad")
    fecha_completada: Optional[datetime] = Field(None, description="Fecha de completado de la actividad")
    estado: Optional[str] = Field(default="pendiente", description="Estado de la actividad")
    completada: Optional[bool] = Field(default=False, description="¿Está completada la actividad?")


class ActividadOportunidadCreate(ActividadOportunidadBase):
    pass


class ActividadOportunidadUpdate(BaseModel):
    asignado_a_id: Optional[UUID4] = None
    titulo: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_actividad: Optional[str] = Field(None, max_length=50)
    prioridad: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    fecha_completada: Optional[datetime] = None
    estado: Optional[str] = None
    completada: Optional[bool] = None


class ActividadOportunidadResponse(ActividadOportunidadBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# MARKETING CAMPAIGN SCHEMAS
# ============================================================================

class CampañaMarketingBase(BaseModel):
    nombre: str = Field(..., max_length=150, description="Nombre de la campaña")
    descripcion: Optional[str] = Field(None, description="Descripción de la campaña")
    tipo_campania: str = Field(..., description="Tipo de campaña")
    fecha_inicio: date = Field(..., description="Fecha de inicio de la campaña")
    fecha_fin: date = Field(..., description="Fecha de fin de la campaña")
    estado: Optional[str] = Field(default="programada", description="Estado de la campaña")
    presupuesto: Optional[Decimal] = Field(default=Decimal('0.00'), description="Presupuesto de la campaña")
    gastos_realizados: Optional[Decimal] = Field(default=Decimal('0.00'), description="Gastos realizados en la campaña")
    objetivo: Optional[str] = Field(None, description="Objetivo de la campaña")
    alcance_esperado: Optional[int] = Field(default=0, ge=0, description="Alcance esperado de la campaña")
    alcance_real: Optional[int] = Field(default=0, ge=0, description="Alcance real de la campaña")
    conversiones_esperadas: Optional[int] = Field(default=0, ge=0, description="Conversiones esperadas de la campaña")
    conversiones_obtenidas: Optional[int] = Field(default=0, ge=0, description="Conversiones obtenidas de la campaña")
    responsable_id: Optional[UUID4] = Field(None, description="ID del responsable de la campaña")
    activa: bool = Field(default=True, description="¿Está activa la campaña?")


class CampañaMarketingCreate(CampañaMarketingBase):
    pass


class CampañaMarketingUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=150)
    descripcion: Optional[str] = None
    tipo_campania: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[str] = None
    presupuesto: Optional[Decimal] = None
    gastos_realizados: Optional[Decimal] = None
    objetivo: Optional[str] = None
    alcance_esperado: Optional[int] = Field(None, ge=0)
    alcance_real: Optional[int] = Field(None, ge=0)
    conversiones_esperadas: Optional[int] = Field(None, ge=0)
    conversiones_obtenidas: Optional[int] = Field(None, ge=0)
    responsable_id: Optional[UUID4] = None
    activa: Optional[bool] = None


class CampañaMarketingResponse(CampañaMarketingBase):
    id: UUID4
    fecha_creacion: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# LEAD SCHEMAS
# ============================================================================

class LeadBase(BaseModel):
    campania_id: Optional[UUID4] = Field(None, description="ID de la campaña que generó el lead")
    nombre_completo: str = Field(..., max_length=150, description="Nombre completo del lead")
    empresa: Optional[str] = Field(None, max_length=100, description="Empresa del lead")
    puesto: Optional[str] = Field(None, max_length=100, description="Puesto del lead")
    email: str = Field(..., max_length=100, description="Email del lead")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del lead")
    fuente: Optional[str] = Field(None, max_length=50, description="Fuente del lead")
    calificacion: Optional[int] = Field(default=0, ge=0, le=100, description="Calificación del lead (0-100)")
    estado: Optional[str] = Field(default="nuevo", description="Estado del lead")
    cliente_convertido_id: Optional[UUID4] = Field(None, description="ID del cliente al que se convirtió")
    fecha_conversion: Optional[datetime] = Field(None, description="Fecha de conversión a cliente")
    asignado_a_id: Optional[UUID4] = Field(None, description="ID del empleado asignado al lead")
    activo: bool = Field(default=True, description="¿Está activo el lead?")


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    campania_id: Optional[UUID4] = None
    nombre_completo: Optional[str] = Field(None, max_length=150)
    empresa: Optional[str] = Field(None, max_length=100)
    puesto: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    fuente: Optional[str] = Field(None, max_length=50)
    calificacion: Optional[int] = Field(None, ge=0, le=100)
    estado: Optional[str] = None
    cliente_convertido_id: Optional[UUID4] = None
    fecha_conversion: Optional[datetime] = None
    asignado_a_id: Optional[UUID4] = None
    activo: Optional[bool] = None


class LeadResponse(LeadBase):
    id: UUID4
    fecha_registro: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ============================================================================
# CAMPAIGN-CUSTOMER RELATIONSHIP SCHEMAS
# ============================================================================

class CampaniaClienteBase(BaseModel):
    campania_id: UUID4
    cliente_id: UUID4
    respondio: Optional[bool] = Field(default=False, description="¿Respondió el cliente?")
    fecha_respuesta: Optional[datetime] = Field(None, description="Fecha de respuesta del cliente")
    tipo_respuesta: Optional[str] = Field(None, max_length=50, description="Tipo de respuesta")
    notas: Optional[str] = Field(None, description="Notas sobre la interacción")
    activo: bool = Field(default=True, description="¿Está activa la relación?")


class CampaniaClienteCreate(CampaniaClienteBase):
    pass


class CampaniaClienteUpdate(BaseModel):
    respondio: Optional[bool] = None
    fecha_respuesta: Optional[datetime] = None
    tipo_respuesta: Optional[str] = Field(None, max_length=50)
    notas: Optional[str] = None
    activo: Optional[bool] = None


class CampaniaClienteResponse(CampaniaClienteBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True