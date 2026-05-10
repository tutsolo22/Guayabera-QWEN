from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from app.core.config import settings
from app.core.database import get_db
from app.models.admin import Admin
from app.models.usuario import Usuario

security = HTTPBearer()

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Admin:
    """
    Dependency to get the current authenticated admin user.
    This ensures that only authenticated admin users can access admin endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        user_type: Optional[str] = payload.get("user_type")
        
        if not email or user_type != "admin":
            raise credentials_exception
            
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    
    # Get admin from database
    stmt = select(Admin).where(Admin.email == email)
    result = await db.execute(stmt)
    admin = result.scalar_one_or_none()
    
    if admin is None:
        raise credentials_exception
        
    return admin

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Usuario:
    """
    Dependency to get the current authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: Optional[str] = payload.get("sub")
        # Allow both 'user' and 'admin' (or lack of type) as users, but depends on logic. We'll just check email.
        
        if not email:
            raise credentials_exception
            
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    
    # Get user from database
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    return user

# Alias for backwards compatibility
get_current_admin_user = get_current_admin