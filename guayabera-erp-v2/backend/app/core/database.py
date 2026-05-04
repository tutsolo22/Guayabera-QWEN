from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from contextlib import asynccontextmanager
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Configurar metadatos con esquema personalizado si es necesario
metadata = MetaData(schema="public")

# Crear motor de base de datos asincrónico
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Crear sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=None,
    expire_on_commit=False
)

# Base para modelos
Base = declarative_base(metadata=metadata)


async def init_db():
    """Inicializar la base de datos"""
    from app.models.usuario import Usuario  # Importar modelos aquí para registrarlos
    from app.models.tenant import Tenant
    from app.models.admin import Admin
    from app.models.licencia import Licencia, TipoLicencia
    from app.models.token import TokenVerificacion
    
    async with engine.begin() as conn:
        # Crear tablas si no existen
        await conn.run_sync(Base.metadata.create_all)
        
    logger.info("Base de datos inicializada correctamente")


@asynccontextmanager
async def get_db():
    """Obtener sesión de base de datos"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()