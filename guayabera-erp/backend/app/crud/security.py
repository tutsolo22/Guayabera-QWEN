"""
CRUD operations for security module
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.models.security import Usuario, Rol, Permiso, Auditoria
from app.core.security import get_password_hash


# ============= USUARIOS =============

def get_user_by_id(db: Session, user_id: UUID) -> Optional[Usuario]:
    """Get user by ID"""
    return db.query(Usuario).filter(Usuario.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[Usuario]:
    """Get user by username"""
    return db.query(Usuario).filter(Usuario.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[Usuario]:
    """Get user by email"""
    return db.query(Usuario).filter(Usuario.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    """Get all users"""
    return db.query(Usuario).offset(skip).limit(limit).all()


def create_user(
    db: Session,
    username: str,
    email: str,
    password: str,
    nombre: str,
    apellidos: str = None
) -> Usuario:
    """Create new user"""
    hashed_password = get_password_hash(password)
    db_user = Usuario(
        username=username,
        email=email,
        password_hash=hashed_password,
        nombre=nombre,
        apellidos=apellidos
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: UUID, update_data: dict) -> Optional[Usuario]:
    """Update user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def increment_failed_login(db: Session, user_id: UUID, max_attempts: int = 5) -> Usuario:
    """Increment failed login attempts"""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.intentos_fallidos += 1
        if db_user.intentos_fallidos >= max_attempts:
            db_user.bloqueado = True
        db.commit()
        db.refresh(db_user)
    return db_user


# ============= ROLES =============

def get_rol_by_id(db: Session, rol_id: UUID) -> Optional[Rol]:
    """Get role by ID"""
    return db.query(Rol).filter(Rol.id == rol_id).first()


def get_rol_by_name(db: Session, nombre: str) -> Optional[Rol]:
    """Get role by name"""
    return db.query(Rol).filter(Rol.nombre == nombre).first()


def get_roles(db: Session, activos_only: bool = True) -> List[Rol]:
    """Get all roles"""
    query = db.query(Rol)
    if activos_only:
        query = query.filter(Rol.activo == True)
    return query.all()


def create_rol(db: Session, nombre: str, descripcion: str = None, 
               permisos_ids: List[UUID] = None) -> Rol:
    """Create new role"""
    db_rol = Rol(nombre=nombre, descripcion=descripcion)
    
    if permisos_ids:
        permisos = db.query(Permiso).filter(Permiso.id.in_(permisos_ids)).all()
        db_rol.permisos = permisos
    
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol


def assign_rol_to_user(db: Session, user_id: UUID, rol_id: UUID) -> bool:
    """Assign role to user"""
    db_user = get_user_by_id(db, user_id)
    db_rol = get_rol_by_id(db, rol_id)
    
    if not db_user or not db_rol:
        return False
    
    if db_rol not in db_user.roles:
        db_user.roles.append(db_rol)
        db.commit()
    
    return True


# ============= PERMISOS =============

def get_permiso_by_id(db: Session, permiso_id: UUID) -> Optional[Permiso]:
    """Get permission by ID"""
    return db.query(Permiso).filter(Permiso.id == permiso_id).first()


def get_permisos(db: Session) -> List[Permiso]:
    """Get all permissions"""
    return db.query(Permiso).all()


def create_permiso(db: Session, modulo: str, accion: str, 
                   descripcion: str = None) -> Permiso:
    """Create new permission"""
    db_permiso = Permiso(
        modulo=modulo,
        accion=accion,
        descripcion=descripcion
    )
    db.add(db_permiso)
    db.commit()
    db.refresh(db_permiso)
    return db_permiso


def user_has_permission(db: Session, user_id: UUID, modulo: str, 
                        accion: str) -> bool:
    """Check if user has permission"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    # Check permissions through roles
    for rol in db_user.roles:
        for permiso in rol.permisos:
            if permiso.modulo == modulo and permiso.accion == accion:
                return True
    
    return False


# ============= AUDITORIA =============

def create_auditoria_registro(
    db: Session,
    usuario_id: UUID,
    usuario_nombre: str,
    accion: str,
    modulo: str,
    entidad: str,
    entidad_id: UUID,
    datos_anteriores: dict = None,
    datos_nuevos: dict = None,
    ip_address: str = None,
    nombre_maquina: str = None,
    user_agent: str = None
) -> Auditoria:
    """Create audit log entry"""
    db_auditoria = Auditoria(
        usuario_id=usuario_id,
        usuario_nombre=usuario_nombre,
        accion=accion,
        modulo=modulo,
        entidad=entidad,
        entidad_id=entidad_id,
        datos_anteriores=datos_anteriores,
        datos_nuevos=datos_nuevos,
        ip_address=ip_address,
        nombre_maquina=nombre_maquina,
        user_agent=user_agent
    )
    db.add(db_auditoria)
    db.commit()
    db.refresh(db_auditoria)
    return db_auditoria


def get_auditoria_logs(
    db: Session,
    modulo: str = None,
    usuario_id: UUID = None,
    fecha_desde: datetime = None,
    fecha_hasta: datetime = None,
    skip: int = 0,
    limit: int = 100
) -> List[Auditoria]:
    """Get audit logs with filters"""
    query = db.query(Auditoria)
    
    if modulo:
        query = query.filter(Auditoria.modulo == modulo)
    if usuario_id:
        query = query.filter(Auditoria.usuario_id == usuario_id)
    if fecha_desde:
        query = query.filter(Auditoria.timestamp >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Auditoria.timestamp <= fecha_hasta)
    
    return query.order_by(Auditoria.timestamp.desc()).offset(skip).limit(limit).all()
