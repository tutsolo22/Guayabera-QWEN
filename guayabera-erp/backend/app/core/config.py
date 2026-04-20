from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os
import json


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # App
    APP_NAME: str = "GuayaberaERP"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://guayabera_user:guayabera_pass_2025@localhost:5432/guayabera_erp"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-this")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # CORS - NO se lee desde .env, valores por defecto
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000"
    ]
    
    # SAT México (para facturación)
    SAT_AMBIENTE: str = "pruebas"  # pruebas o produccion
    PAC_API_URL: str = "https://api.finkok.com/v1"
    
    # Configuración textil
    FABRIC_DEFAULT_WIDTH: float = 150.0  # cm
    SCALE_CM_TO_PX: float = 37.8


settings = Settings()
