"""
Configuration module for GuayaberaERP
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings  # Changed to pydantic-settings
from pydantic import PostgresDsn
from typing import List, Optional, Union
from functools import lru_cache

load_dotenv()


class Settings(BaseSettings):  # Using BaseSettings from pydantic-settings
    """
    Application settings loaded from environment variables
    """
    # App Configuration
    APP_NAME: str = os.getenv("APP_NAME", "Guayabera ERP")
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://guayabera_user:guayabera_pass_2025@localhost:5434/guayabera_erp")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Email Configuration
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True").lower() == "true"
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    
    # Facturama Configuration
    FACTURAMA_URL: str = os.getenv("FACTURAMA_URL", "https://apisandbox.facturama.mx")
    FACTURAMA_API_KEY: str = os.getenv("FACTURAMA_API_KEY", "")
    FACTURAMA_API_TOKEN: str = os.getenv("FACTURAMA_API_TOKEN", "")
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:3000").split(",")
    
    # Storage Configuration
    STORAGE_TYPE: str = os.getenv("STORAGE_TYPE", "local")  # local, s3, gcs
    LOCAL_STORAGE_PATH: str = os.getenv("LOCAL_STORAGE_PATH", "./storage")
    
    # AI Assistant Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # OCR Configuration
    OCR_PROVIDER: str = os.getenv("OCR_PROVIDER", "tesseract")  # tesseract, google_vision, aws_textract
    
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
    if not settings.FACTURAMA_API_KEY or not settings.FACTURAMA_API_TOKEN:
        print("⚠️ WARNING: Facturama API credentials are not configured.")
        print("Please set FACTURAMA_API_KEY and FACTURAMA_API_TOKEN environment variables.")
        print("Without these, electronic invoicing features will not work properly.")
        return False
    return True


# Validate Facturama config on import
validate_facturama_config()