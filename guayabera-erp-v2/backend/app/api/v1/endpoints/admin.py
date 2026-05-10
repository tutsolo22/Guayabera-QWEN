from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta
import secrets
import string
from typing import List, Optional

from app.core.config import settings
from app.core.database import get_db
from app.models.usuario import Usuario
from app.models.admin import Admin
from app.models.tenant import Tenant, TenantCorporation
from app.models.licencia import Licencia, TipoLicencia
from app.models.token import TokenVerificacion
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.schemas.tenant import TenantCreate, TenantUpdate
from app.schemas.licencia import LicenciaCreate, LicenciaUpdate
from app.core.security import get_password_hash
from app.api.deps import get_current_admin

router = APIRouter()

def generar_token_unico(longitud: int = 32) -> str:
    """Genera un token único seguro"""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(longitud))

def enviar_invitacion_correo(destinatario: str, asunto: str, cuerpo: str):
    """Función para enviar correos electrónicos de invitación"""
    # Aquí iría la lógica real para enviar correos
    # Por ahora solo imprimimos para simular
    print(f"Invitación enviada a: {destinatario}")
    print(f"Asunto: {asunto}")
    print(f"Cuerpo: {cuerpo}")

@router.post("/crear-tenant")
async def crear_tenant(
    tenant_data: TenantCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para que el superadmin cree nuevos tenants
    """
    # Verificar si ya existe un tenant con el mismo nombre o dominio
    stmt = select(Tenant).where(
        (Tenant.name == tenant_data.name) | (Tenant.subdomain == tenant_data.subdomain)
    )
    result = await db.execute(stmt)
    existing_tenant = result.scalar_one_or_none()
    
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tenant con ese nombre o subdominio"
        )
    
    # Crear el nuevo tenant
    nuevo_tenant = Tenant(
        name=tenant_data.name,
        subdomain=tenant_data.subdomain,
        schema_name=f"tenant_{tenant_data.subdomain}",
        contact_email=tenant_data.contact_email,
        descripcion=tenant_data.descripcion,
        is_active=True
    )
    
    db.add(nuevo_tenant)
    await db.commit()
    await db.refresh(nuevo_tenant)
    
    return {
        "mensaje": "Tenant creado exitosamente",
        "tenant_id": nuevo_tenant.id
    }

@router.post("/invitar-tenant-admin")
async def invitar_tenant_admin(
    email: str,
    tenant_id: str,
    background_tasks: BackgroundTasks,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para invitar a un administrador de tenant mediante correo electrónico
    """
    # Verificar que el tenant existe
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant no encontrado"
        )
    
    # Verificar que no exista un usuario con ese email
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email"
        )
    
    # Generar token de verificación
    token_verificacion = generar_token_unico()
    expiracion = datetime.utcnow() + timedelta(hours=24)  # El enlace expira en 24 horas
    
    # Guardar el token con referencia al tenant
    nuevo_token = TokenVerificacion(
        tipo_token="invitacion_tenant_admin",
        token=token_verificacion,
        expira_en=expiracion,
        usado=False,
        tenant_id=tenant_id,
        destinatario_email=email
    )
    
    db.add(nuevo_token)
    await db.commit()
    
    # Enviar correo con el enlace de verificación
    enlace_verificacion = f"{settings.FRONTEND_URL}/crear-contrasena/{token_verificacion}"
    cuerpo_correo = f"""
    Hola,
    
    Ha sido invitado como administrador del tenant "{tenant.name}" en Guayabera ERP Suite.
    
    Por favor haga clic en el siguiente enlace para crear su contraseña y activar su cuenta:
    {enlace_verificacion}
    
    Este enlace es válido por 24 horas. Si no solicitó este registro, puede ignorar este mensaje.
    
    Saludos,
    Equipo de Guayabera ERP Suite
    """
    
    # Enviar correo en segundo plano
    background_tasks.add_task(
        enviar_invitacion_correo,
        email,
        "Invitación como Administrador de Tenant - Guayabera ERP Suite",
        cuerpo_correo
    )
    
    return {
        "mensaje": "Invitación enviada exitosamente",
        "expiracion_token": expiracion.isoformat()
    }

@router.post("/crear-corporacion")
async def crear_corporacion(
    nombre: str,
    descripcion: Optional[str] = None,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para crear una corporación que agrupa varios tenants
    """
    # Verificar si ya existe una corporación con el mismo nombre
    stmt = select(TenantCorporation).where(TenantCorporation.name == nombre)
    result = await db.execute(stmt)
    existing_corp = result.scalar_one_or_none()
    
    if existing_corp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una corporación con ese nombre"
        )
    
    # Crear la nueva corporación
    nueva_corporacion = TenantCorporation(
        name=nombre,
        descripcion=descripcion
    )
    
    db.add(nueva_corporacion)
    await db.commit()
    await db.refresh(nueva_corporacion)
    
    return {
        "mensaje": "Corporación creada exitosamente",
        "corporation_id": nueva_corporacion.id
    }

@router.post("/asignar-tenant-a-corporacion")
async def asignar_tenant_a_corporacion(
    tenant_id: str,
    corporation_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para asignar un tenant a una corporación
    """
    # Verificar que el tenant existe
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant no encontrado"
        )
    
    # Verificar que la corporación existe
    stmt = select(TenantCorporation).where(TenantCorporation.id == corporation_id)
    result = await db.execute(stmt)
    corporation = result.scalar_one_or_none()
    
    if not corporation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corporación no encontrada"
        )
    
    # Actualizar el tenant con la corporación
    stmt = update(Tenant).where(Tenant.id == tenant_id).values(corporation_id=corporation_id)
    await db.execute(stmt)
    await db.commit()
    
    return {
        "mensaje": "Tenant asignado a corporación exitosamente"
    }

@router.post("/crear-licencia")
async def crear_licencia(
    licencia_data: LicenciaCreate,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para crear una nueva licencia
    """
    # Verificar que el tipo de licencia existe
    stmt = select(TipoLicencia).where(TipoLicencia.id == licencia_data.tipo_licencia_id)
    result = await db.execute(stmt)
    tipo_licencia = result.scalar_one_or_none()
    
    if not tipo_licencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipo de licencia no encontrado"
        )
    
    # Si se especifica tenant_id, verificar que existe
    if licencia_data.tenant_id:
        stmt = select(Tenant).where(Tenant.id == licencia_data.tenant_id)
        result = await db.execute(stmt)
        tenant = result.scalar_one_or_none()
        
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant no encontrado"
            )
    
    # Generar código único para la licencia
    codigo_licencia = generar_token_unico(16)
    
    # Crear la nueva licencia
    nueva_licencia = Licencia(
        tipo_licencia_id=licencia_data.tipo_licencia_id,
        codigo=codigo_licencia,  # Usar el código generado
        fecha_inicio=licencia_data.fecha_inicio or datetime.utcnow(),
        fecha_fin=licencia_data.fecha_fin,
        activa=licencia_data.activa,
        tenant_id=licencia_data.tenant_id
    )
    
    db.add(nueva_licencia)
    await db.commit()
    await db.refresh(nueva_licencia)
    
    return {
        "mensaje": "Licencia creada exitosamente",
        "licencia_id": nueva_licencia.id,
        "codigo": codigo_licencia
    }

@router.get("/tenants")
async def listar_tenants(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar todos los tenants (solo para superadmin)
    """
    stmt = select(Tenant).offset(skip).limit(limit)
    result = await db.execute(stmt)
    tenants = result.scalars().all()
    
    return {"tenants": tenants}

@router.get("/corporaciones")
async def listar_corporaciones(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar todas las corporaciones (solo para superadmin)
    """
    stmt = select(TenantCorporation).offset(skip).limit(limit)
    result = await db.execute(stmt)
    corporaciones = result.scalars().all()
    
    return {"corporaciones": corporaciones}

@router.get("/licencias")
async def listar_licencias(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar todas las licencias (solo para superadmin)
    """
    stmt = select(Licencia).offset(skip).limit(limit)
    result = await db.execute(stmt)
    licencias = result.scalars().all()
    
    return {"licencias": licencias}

@router.get("/licencias-por-tenant/{tenant_id}")
async def listar_licencias_por_tenant(
    tenant_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para listar licencias asociadas a un tenant específico
    """
    stmt = select(Licencia).where(Licencia.tenant_id == tenant_id)
    result = await db.execute(stmt)
    licencias = result.scalars().all()
    
    return {"licencias": licencias}

@router.put("/desactivar-tenant/{tenant_id}")
async def desactivar_tenant(
    tenant_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para desactivar un tenant (no eliminarlo completamente)
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant no encontrado"
        )
    
    # Actualizar el estado del tenant
    stmt = update(Tenant).where(Tenant.id == tenant_id).values(is_active=False)
    await db.execute(stmt)
    await db.commit()
    
    return {"mensaje": f"Tenant {tenant.name} desactivado exitosamente"}

@router.put("/activar-tenant/{tenant_id}")
async def activar_tenant(
    tenant_id: str,
    current_admin: Admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint para reactivar un tenant
    """
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant no encontrado"
        )
    
    # Actualizar el estado del tenant
    stmt = update(Tenant).where(Tenant.id == tenant_id).values(is_active=True)
    await db.execute(stmt)
    await db.commit()
    
    return {"mensaje": f"Tenant {tenant.name} activado exitosamente"}