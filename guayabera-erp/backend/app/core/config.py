"""
Configuration module for GuayaberaERP
Handles environment variables and application settings
"""

import os
from typing import List, Optional
from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/guayabera_erp")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000").split(",")
    
    # Facturama settings
    FACTURAMA_API_KEY: str = os.getenv("FACTURAMA_API_KEY", "")
    FACTURAMA_EMAIL: str = os.getenv("FACTURAMA_EMAIL", "")
    USE_PRODUCTION_FACTURAMA: bool = os.getenv("USE_PRODUCTION_FACTURAMA", "False").lower() == "true"
    
    # Storage settings
    STATIC_FILES_PATH: str = os.getenv("STATIC_FILES_PATH", "./static")
    
    # Celery settings
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    """
    Cached settings instance to avoid reloading from environment multiple times
    """
    return Settings()


# Global settings instance
settings = get_settings()


def validate_facturama_config():
    """
    Validates that Facturama configuration is properly set
    """
    if not settings.FACTURAMA_API_KEY or not settings.FACTURAMA_EMAIL:
        print("⚠️ WARNING: Facturama API credentials are not configured.")
        print("Please set FACTURAMA_API_KEY and FACTURAMA_EMAIL environment variables.")
        print("Without these, electronic invoicing features will not work properly.")
        return False
    return True


# Validate Facturama config on import
validate_facturama_config()