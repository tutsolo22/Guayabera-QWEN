from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from typing import AsyncGenerator
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Metadata object para controlar nuestro esquema de base de datos
metadata = MetaData(schema="public")

# Configurar motor asincrónico
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Crear un generador local de sesiones
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para modelos
Base = declarative_base(metadata=metadata)

# Importaciones de modelos después de crear la Base para evitar problemas de importación circular
from app.models.usuario import Usuario  # noqa: F401
from app.models.tenant import Tenant  # noqa: F401
from app.models.admin import Admin  # noqa: F401
from app.models.licencia import Licencia, TipoLicencia  # noqa: F401
from app.models.token import TokenVerificacion  # noqa: F401


async def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        
    logger.info("Base de datos inicializada correctamente")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Obtiene una sesión de base de datos para dependencias de FastAPI.
    
    Yields:
        db_session: Sesión de base de datos
    """
    async with AsyncSessionLocal() as session:
        yield session

# Alias for backwards compatibility with existing endpoints
get_db = get_db_session