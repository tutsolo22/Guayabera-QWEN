from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
from pydantic import ValidationError

from app.core.database import get_db
from app.core.config import settings
from app.models.usuario import Usuario
from app.models.admin import Admin


security = HTTPBearer()


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPBearer = Depends(security)
):
    """
    Obtiene el usuario actual autenticado a partir del token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("email")
        user_type: str = payload.get("user_type")
        
        if email is None:
            raise credentials_exception
            
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    
    if user_type == "admin":
        result = await db.execute(Admin.__table__.select().where(Admin.email == email))
        user = result.fetchone()
        if user:
            return Admin(**user._mapping)
    else:
        result = await db.execute(Usuario.__table__.select().where(Usuario.email == email))
        user = result.fetchone()
        if user:
            return Usuario(**user._mapping)
    
    raise credentials_exception


async def get_current_admin_user(current_user = Depends(get_current_user)):
    """
    Obtiene el administrador actual autenticado
    """
    if not isinstance(current_user, Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación solo permitida para administradores"
        )
    
    return current_user