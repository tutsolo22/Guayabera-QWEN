from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime  # Importar datetime


class TokenVerificacion(Base):
    """
    Modelo para representar tokens temporales de verificación
    para creación de cuenta y recuperación de contraseña
    """
    __tablename__ = "tokens_verificacion"

    id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    usuario_id: str = Column(String, ForeignKey('usuarios.id'), nullable=True)  # Para tokens de usuario
    admin_id: str = Column(String, ForeignKey('admins.id'), nullable=True)  # Para tokens de admin
    tipo_token: str = Column(String(20), nullable=False)  # "registro", "recuperacion", "activacion"
    token: str = Column(String, unique=True, nullable=False, index=True)  # El token real para uso
    usado: bool = Column(Boolean, default=False)  # Si ya fue utilizado
    expira_en: datetime = Column(DateTime(timezone=True), nullable=False)  # Fecha de expiración
    creado_en: datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TokenVerificacion(id={self.id}, tipo={self.tipo_token}, usado={self.usado})>"