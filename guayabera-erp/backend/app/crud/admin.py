"""
CRUD operations for admin module
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID

from app.models.admin import Empresa, Sucursal, Configuracion, Moneda, Impuesto
from app.schemas.admin import EmpresaCreate, EmpresaUpdate, SucursalCreate


# ============= EMPRESA =============

def get_empresa(db: Session, empresa_id: UUID) -> Optional[Empresa]:
    """Get company by ID"""
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()


def get_empresa_by_rfc(db: Session, rfc: str) -> Optional[Empresa]:
    """Get company by RFC"""
    return db.query(Empresa).filter(Empresa.rfc == rfc).first()


def get_empresas(db: Session, skip: int = 0, limit: int = 100) -> List[Empresa]:
    """Get all companies"""
    return db.query(Empresa).offset(skip).limit(limit).all()


def create_empresa(db: Session, empresa: EmpresaCreate) -> Empresa:
    """Create new company"""
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


def update_empresa(db: Session, empresa_id: UUID, empresa: EmpresaUpdate) -> Optional[Empresa]:
    """Update company"""
    db_empresa = get_empresa(db, empresa_id)
    if not db_empresa:
        return None
    
    update_data = empresa.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


# ============= SUCURSAL =============

def get_sucursal(db: Session, sucursal_id: UUID) -> Optional[Sucursal]:
    """Get branch by ID"""
    return db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()


def get_sucursales_by_empresa(db: Session, empresa_id: UUID) -> List[Sucursal]:
    """Get all branches for a company"""
    return db.query(Sucursal).filter(
        Sucursal.empresa_id == empresa_id,
        Sucursal.activo == True
    ).all()


def create_sucursal(db: Session, sucursal: SucursalCreate) -> Sucursal:
    """Create new branch"""
    db_sucursal = Sucursal(**sucursal.dict())
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal


# ============= CONFIGURACION =============

def get_configuracion(db: Session, clave: str) -> Optional[Configuracion]:
    """Get configuration by key"""
    return db.query(Configuracion).filter(Configuracion.clave == clave).first()


def get_configuraciones(db: Session, modulo: Optional[str] = None) -> List[Configuracion]:
    """Get configurations, optionally filtered by module"""
    query = db.query(Configuracion)
    if modulo:
        query = query.filter(Configuracion.modulo == modulo)
    return query.all()


def create_or_update_configuracion(db: Session, clave: str, valor: str, tipo: str = "string", 
                                    descripcion: str = None, modulo: str = "admin") -> Configuracion:
    """Create or update configuration"""
    db_config = get_configuracion(db, clave)
    if db_config:
        db_config.valor = valor
        db_config.tipo = tipo
        db_config.descripcion = descripcion
        db.commit()
        db.refresh(db_config)
        return db_config
    else:
        db_config = Configuracion(
            clave=clave,
            valor=valor,
            tipo=tipo,
            descripcion=descripcion,
            modulo=modulo
        )
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config


# ============= MONEDA =============

def get_monedas(db: Session, activas_only: bool = True) -> List[Moneda]:
    """Get currencies"""
    query = db.query(Moneda)
    if activas_only:
        query = query.filter(Moneda.activa == True)
    return query.all()


def get_moneda_base(db: Session) -> Optional[Moneda]:
    """Get base currency"""
    return db.query(Moneda).filter(Moneda.es_base == True).first()


# ============= IMPUESTOS =============

def get_impuestos_activos(db: Session) -> List[Impuesto]:
    """Get active taxes"""
    return db.query(Impuesto).filter(
        Impuesto.activo == True,
        (Impuesto.vigente_hasta.is_(None)) | (Impuesto.vigente_hasta >= func.now())
    ).all()
